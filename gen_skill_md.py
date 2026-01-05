import ast
import json
import os

def extract_plugins_from_file(filepath):
    """
    Extracts plugin information from a python file using AST parsing.
    Handles 'function_plugins = {...}' and 'function_plugins.update({...})'
    """
    if not os.path.exists(filepath):
        return {}

    with open(filepath, 'r', encoding='utf-8') as f:
        tree = ast.parse(f.read())

    plugins = {}

    for node in ast.walk(tree):
        # Look for function definitions that return the plugin dict (like get_crazy_functions)
        if isinstance(node, ast.FunctionDef) and node.name in ['get_crazy_functions', 'get_core_functions']:
            for subnode in ast.walk(node):
                # Handle initial assignment: function_plugins = { ... }
                # or return { ... }
                dict_node = None
                if isinstance(subnode, ast.Assign):
                    for target in subnode.targets:
                        if isinstance(target, ast.Name) and target.id == 'function_plugins':
                            if isinstance(subnode.value, ast.Dict):
                                dict_node = subnode.value
                elif isinstance(subnode, ast.Return):
                    if isinstance(subnode.value, ast.Dict):
                        dict_node = subnode.value

                if dict_node:
                    for i, key in enumerate(dict_node.keys):
                        if isinstance(key, ast.Constant) and isinstance(key.value, str):
                            val = dict_node.values[i]
                            if isinstance(val, ast.Dict):
                                plugin_info = {}
                                for j, k in enumerate(val.keys):
                                    if isinstance(k, ast.Constant) and isinstance(k.value, str):
                                        v = val.values[j]
                                        if isinstance(v, ast.Constant):
                                            plugin_info[k.value] = v.value
                                plugins[key.value] = plugin_info

                # Handle updates: function_plugins.update({ ... })
                if isinstance(subnode, ast.Call) and isinstance(subnode.func, ast.Attribute) and subnode.func.attr == 'update':
                     if len(subnode.args) > 0 and isinstance(subnode.args[0], ast.Dict):
                        d = subnode.args[0]
                        for i, key in enumerate(d.keys):
                            if isinstance(key, ast.Constant) and isinstance(key.value, str):
                                val = d.values[i]
                                if isinstance(val, ast.Dict):
                                    plugin_info = {}
                                    for j, k in enumerate(val.keys):
                                        if isinstance(k, ast.Constant) and isinstance(k.value, str):
                                            v = val.values[j]
                                            if isinstance(v, ast.Constant):
                                                plugin_info[k.value] = v.value
                                plugins[key.value] = plugin_info

    return plugins

def generate_skill_md(output_file='SKILL.md'):
    crazy_plugins = extract_plugins_from_file('crazy_functional.py')
    core_plugins = extract_plugins_from_file('core_functional.py')

    content = []
    content.append("# GPT Academic Skills")
    content.append("")
    content.append("This document lists the core capabilities available to the agent.")
    content.append("")

    content.append("## Core Functions")
    content.append("These are text processing functions usually applied to the current input.")
    content.append("")
    for name, info in core_plugins.items():
        desc = info.get('Prefix', '').strip()
        if not desc:
            # Try to get description from comments or other fields if available (limited by AST extraction)
            # For now, if prefix is code-like or empty, maybe skip or just list name
            pass

        # Clean up description (remove quotes, etc if extracted raw)
        desc = desc.replace('"', '').replace("'", "").strip()
        content.append(f"### {name}")
        if desc:
            content.append(f"- **Description**: {desc}")
        content.append("")

    content.append("## Crazy Functions (Plugins)")
    content.append("These are complex functions that can handle files, perform searches, etc.")
    content.append("")

    # Sort by Group
    grouped_plugins = {}
    for name, info in crazy_plugins.items():
        group = info.get('Group', 'Other')
        if group not in grouped_plugins:
            grouped_plugins[group] = []
        grouped_plugins[group].append((name, info))

    for group, plugins in grouped_plugins.items():
        content.append(f"### Group: {group}")
        for name, info in plugins:
            description = info.get('Info', 'No description available.')
            content.append(f"#### {name}")
            content.append(f"- **Description**: {description}")
            if 'AdvancedArgs' in info and info['AdvancedArgs']:
                reminder = info.get('ArgsReminder', '')
                content.append(f"- **Advanced Arguments**: {reminder}")
            content.append("")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(content))

    print(f"Successfully generated {output_file}")

if __name__ == '__main__':
    generate_skill_md()
