import ast
import json

def extract_plugins_from_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        tree = ast.parse(f.read())

    plugins = {}

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name in ['get_crazy_functions', 'get_core_functions']:
            for subnode in ast.walk(node):
                if isinstance(subnode, ast.Dict):
                    # We found a dictionary. Let's see if it looks like a plugin definition.
                    # This is a bit heuristic. We look for keys that are strings and values that are dictionaries.
                    for i, key in enumerate(subnode.keys):
                        if isinstance(key, ast.Constant) and isinstance(key.value, str):
                            val = subnode.values[i]
                            if isinstance(val, ast.Dict):
                                plugin_info = {}
                                for j, k in enumerate(val.keys):
                                    if isinstance(k, ast.Constant) and isinstance(k.value, str):
                                        v = val.values[j]
                                        if isinstance(v, ast.Constant):
                                            plugin_info[k.value] = v.value
                                        elif isinstance(v, ast.Call):
                                            # Handle HotReload(Func)
                                            # We just want the function name if possible, or just mark as code
                                            plugin_info[k.value] = "Function/Code"
                                if 'Info' in plugin_info or 'Prefix' in plugin_info:
                                    plugins[key.value] = plugin_info

                # specific handling for function_plugins.update({...})
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
                                    if 'Info' in plugin_info or 'Prefix' in plugin_info:
                                        plugins[key.value] = plugin_info

    return plugins

crazy = extract_plugins_from_file('crazy_functional.py')
core = extract_plugins_from_file('core_functional.py')

all_skills = {
    "Core Functions": core,
    "Crazy Functions": crazy
}

print(json.dumps(all_skills, indent=2, ensure_ascii=False))
