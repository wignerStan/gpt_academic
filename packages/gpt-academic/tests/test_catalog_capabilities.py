from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "source/skills/gpt-academic/scripts/catalog_capabilities.py"
)
spec = importlib.util.spec_from_file_location("catalog_capabilities", SCRIPT)
catalog_capabilities = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(catalog_capabilities)


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def write(self, name: str, content: str) -> None:
        (self.root / name).write_text(content, encoding="utf-8")

    def test_extracts_literal_prompt_and_plugin_registry_without_importing(self):
        self.write(
            "core_functional.py",
            """
raise RuntimeError('must not execute')

def get_core_functions():
    return {
        'Translate': {'Visible': False},
        'Polish': {},
    }
""",
        )
        self.write(
            "crazy_functional.py",
            """
raise RuntimeError('must not execute')

def get_crazy_functions():
    function_plugins = {
        'Parse': {'Group': 'Coding|Academic', 'Info': 'Parse a project', 'AsButton': True},
    }
    function_plugins.update({
        'Search': {'Group': 'Research', 'Info': 'Search sources', 'AsButton': False},
    })
    function_plugins['Save'] = {'Group': 'Chat', 'Info': 'Save conversation'}
    return function_plugins
""",
        )
        result = catalog_capabilities.catalog(self.root)
        self.assertEqual(result["schema_version"], catalog_capabilities.SCHEMA)
        self.assertEqual(
            [(item["kind"], item["name"]) for item in result["capabilities"]],
            [
                ("plugin", "Parse"),
                ("plugin", "Save"),
                ("plugin", "Search"),
                ("prompt", "Polish"),
                ("prompt", "Translate"),
            ],
        )
        parse = result["capabilities"][0]
        self.assertEqual(parse["groups"], ["Coding", "Academic"])
        self.assertEqual(parse["description"], "Parse a project")
        self.assertTrue(parse["as_button"])
        translate = result["capabilities"][-1]
        self.assertFalse(translate["visible"])
        self.assertEqual(result["unavailable"], [])

    def test_reports_non_literal_registry_extension(self):
        self.write(
            "core_functional.py",
            "def get_core_functions():\n    return {'Prompt': {}}\n",
        )
        self.write(
            "crazy_functional.py",
            """
def dynamic():
    return {}

def get_crazy_functions():
    function_plugins = {'Plugin': {}}
    function_plugins.update(dynamic())
    return function_plugins
""",
        )
        result = catalog_capabilities.catalog(self.root)
        self.assertIn("non-literal function_plugins.update call", result["unavailable"])
        json.dumps(result, ensure_ascii=False, sort_keys=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
