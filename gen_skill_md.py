import ast
import json
import os
import re

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
                                        elif isinstance(v, ast.Call):
                                            # Handle HotReload(Func) or similar
                                            # Extract function name if possible
                                            if hasattr(v.func, 'id'): # Direct call
                                                plugin_info[k.value] = f"Calls: {v.func.id}"
                                            elif isinstance(v.func, ast.Name):
                                                plugin_info[k.value] = f"Calls: {v.func.id}"
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

def clean_text(text):
    if not text:
        return ""
    # Remove surrounding quotes if they were extracted literally (though AST usually handles this)
    # But clean up newlines and extra spaces
    text = text.strip()
    # Replace multiple newlines with a single newline
    text = re.sub(r'\n+', '\n', text)
    return text

def categorize_core_function(name):
    """Maps core functions to categories."""
    mapping = {
        "学术语料润色": "Academic",
        "查找语法错误": "Text Processing",
        "参考文献转Bib": "Academic",
        "中译英": "Translation",
        "学术英中互译": "Academic",
        "英译中": "Translation",
        "解释代码": "Coding",
        "总结绘制脑图": "Utility",
        "找图片": "Utility",
    }
    return mapping.get(name, "General")

def map_crazy_group(group_str):
    """Maps the Chinese group names to English categories."""
    if not group_str:
        return "General"

    # Handle multi-groups like "对话|编程"
    groups = group_str.split('|')
    primary_group = groups[0]

    mapping = {
        "对话": "Chat & General",
        "编程": "Coding",
        "学术": "Academic",
        "智能体": "Agent Tools",
        "画图": "Image Generation",
        "图像": "Image Generation"
    }

    return mapping.get(primary_group, primary_group)

def generate_skill_md(output_file='SKILL.md'):
    crazy_plugins = extract_plugins_from_file('crazy_functional.py')
    core_plugins = extract_plugins_from_file('core_functional.py')

    all_skills = {} # Category -> list of skills

    # Process Core Plugins
    for name, info in core_plugins.items():
        category = categorize_core_function(name)
        if category not in all_skills:
            all_skills[category] = []

        description = info.get('Prefix', '')
        if not description:
             # Try to construct a description if prefix is missing or code
             description = f"Performs {name} on the input text."
        else:
             # Sometimes Prefix is a prompt. We can say "Uses the following prompt prefix: ..."
             # or just present it as description.
             description = f"Applies the following prompt/logic: {clean_text(description)}"

        all_skills[category].append({
            "name": name,
            "description": description,
            "type": "Core Function (Immediate Text Action)",
            "usage": "Select this function to process the current text in the input area."
        })

    # Process Crazy Plugins
    for name, info in crazy_plugins.items():
        raw_group = info.get('Group', 'General')
        category = map_crazy_group(raw_group)

        if category not in all_skills:
            all_skills[category] = []

        description = info.get('Info', 'No specific description provided.')
        usage = "Call this plugin via the plugin menu or Void Terminal."

        args_info = []
        if 'AdvancedArgs' in info and info['AdvancedArgs']:
            reminder = info.get('ArgsReminder', '')
            if reminder:
                args_info.append(f"**Advanced Arguments**: {clean_text(reminder)}")

        # Extract implied arguments from description
        # Many plugins say "输入参数为..." (Input parameter is...)
        input_param_hint = "Check description for input requirements (usually file path or text)."
        if "输入参数" in description:
            # simple extraction attempt
            match = re.search(r"输入参数.*", description)
            if match:
                input_param_hint = match.group(0)

        usage += f" {input_param_hint}"

        skill_entry = {
            "name": name,
            "description": clean_text(description),
            "type": "Plugin (Complex Task)",
            "usage": usage,
            "details": args_info
        }
        all_skills[category].append(skill_entry)

    # Sort categories
    sorted_categories = sorted(all_skills.keys())

    content = []
    content.append("# GPT Academic Agent Skills Index")
    content.append("")
    content.append("This document provides a comprehensive index of the tools and skills available to the Code CLI Agent within the GPT Academic environment. Use this reference to understand what actions can be performed.")
    content.append("")

    for category in sorted_categories:
        content.append(f"## {category}")
        content.append("")

        skills = all_skills[category]
        # Sort skills by name
        skills.sort(key=lambda x: x['name'])

        for skill in skills:
            content.append(f"### {skill['name']}")
            content.append(f"- **Type**: {skill['type']}")
            content.append(f"- **Description**: {skill['description']}")
            content.append(f"- **Usage Instruction**: {skill['usage']}")
            if 'details' in skill and skill['details']:
                for detail in skill['details']:
                    content.append(f"- {detail}")
            content.append("")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(content))

    print(f"Successfully generated {output_file}")

if __name__ == '__main__':
    generate_skill_md()
