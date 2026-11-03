#!/usr/bin/env python3
"""Read GPT Academic's declared capability registry without importing the application."""
from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path
from typing import Any

SCHEMA = "gpt-academic-capability-catalog/v1"
CORE_FILE = "core_functional.py"
PLUGIN_FILE = "crazy_functional.py"


class CatalogError(ValueError):
    pass


def _string(node: ast.AST | None) -> str | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return None


def _boolean(node: ast.AST | None) -> bool | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, bool):
        return node.value
    return None


def _dict_items(node: ast.AST) -> list[tuple[str, ast.AST]]:
    if not isinstance(node, ast.Dict):
        return []
    result: list[tuple[str, ast.AST]] = []
    for key, value in zip(node.keys, node.values):
        name = _string(key)
        if name is not None:
            result.append((name, value))
    return result


def _metadata(node: ast.AST) -> dict[str, ast.AST]:
    return {key: value for key, value in _dict_items(node)}


def _function(tree: ast.Module, name: str) -> ast.FunctionDef:
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return node
    raise CatalogError(f"missing function {name}")


def _parse(path: Path) -> ast.Module:
    try:
        return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (OSError, UnicodeError, SyntaxError) as exc:
        raise CatalogError(f"cannot parse {path}: {exc}") from exc


def _entry(kind: str, name: str, metadata: dict[str, ast.AST]) -> dict[str, Any]:
    group_text = _string(metadata.get("Group"))
    groups = (
        [item.strip() for item in group_text.split("|") if item.strip()]
        if group_text
        else ["prompt"] if kind == "prompt" else []
    )
    visible = _boolean(metadata.get("Visible"))
    if visible is None:
        visible = True
    return {
        "kind": kind,
        "name": name,
        "groups": groups,
        "description": _string(metadata.get("Info")) or "",
        "visible": visible,
        "as_button": _boolean(metadata.get("AsButton")) if kind == "plugin" else None,
    }


def _core_entries(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    function = _function(_parse(path), "get_core_functions")
    unavailable: list[str] = []
    for node in ast.walk(function):
        if isinstance(node, ast.Return):
            items = _dict_items(node.value)
            if items:
                return [
                    _entry("prompt", name, _metadata(value))
                    for name, value in items
                ], unavailable
            unavailable.append("get_core_functions return value is not a literal dictionary")
    raise CatalogError("get_core_functions has no return value")


def _plugin_dicts(function: ast.FunctionDef) -> tuple[list[ast.Dict], list[str]]:
    dictionaries: list[ast.Dict] = []
    unavailable: list[str] = []
    for node in ast.walk(function):
        if isinstance(node, ast.Assign):
            if any(isinstance(target, ast.Name) and target.id == "function_plugins" for target in node.targets):
                if isinstance(node.value, ast.Dict):
                    dictionaries.append(node.value)
                else:
                    unavailable.append("function_plugins assignment is not a literal dictionary")
            for target in node.targets:
                if (
                    isinstance(target, ast.Subscript)
                    and isinstance(target.value, ast.Name)
                    and target.value.id == "function_plugins"
                ):
                    name = _string(target.slice)
                    if name is not None and isinstance(node.value, ast.Dict):
                        dictionaries.append(ast.Dict(keys=[ast.Constant(name)], values=[node.value]))
                    else:
                        unavailable.append("non-literal function_plugins item assignment")
        elif (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "function_plugins"
            and node.func.attr == "update"
        ):
            if len(node.args) == 1 and isinstance(node.args[0], ast.Dict):
                dictionaries.append(node.args[0])
            else:
                unavailable.append("non-literal function_plugins.update call")
    return dictionaries, unavailable


def _plugin_entries(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    function = _function(_parse(path), "get_crazy_functions")
    dictionaries, unavailable = _plugin_dicts(function)
    entries: dict[str, dict[str, Any]] = {}
    for dictionary in dictionaries:
        for name, value in _dict_items(dictionary):
            entries[name] = _entry("plugin", name, _metadata(value))
    if not entries:
        raise CatalogError("no literal function_plugins entries found")
    return list(entries.values()), unavailable


def catalog(root: Path) -> dict[str, Any]:
    root = root.expanduser().resolve()
    core, core_unavailable = _core_entries(root / CORE_FILE)
    plugins, plugin_unavailable = _plugin_entries(root / PLUGIN_FILE)
    capabilities = sorted([*core, *plugins], key=lambda item: (item["kind"], item["name"]))
    return {
        "schema_version": SCHEMA,
        "sources": [CORE_FILE, PLUGIN_FILE],
        "capabilities": capabilities,
        "unavailable": sorted(set([*core_unavailable, *plugin_unavailable])),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = catalog(args.root)
    except CatalogError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False, sort_keys=True))
        return 1
    payload = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
