import importlib
import os
import shutil
import re

def sanitize_name(name):
    # Replace non-alphanumeric characters with underscores, but keep Chinese characters if desired?
    # For file systems, safer to stick to ascii or simple chars.
    # But user might want Chinese names. Let's strip special chars.
    # name = re.sub(r'[^\w\s-]', '', name)
    name = name.strip().replace(" ", "-").replace("/", "-").replace("\\", "-")
    return name

def generate_skills():
    # Setup directories
    base_dir = "skills"
    if os.path.exists(base_dir):
        shutil.rmtree(base_dir)
    os.makedirs(base_dir)

    # 1. Process Core Functions (Prompts)
    import core_functional
    importlib.reload(core_functional)
    core_funcs = core_functional.get_core_functions()

    for name, meta in core_funcs.items():
        safe_name = sanitize_name(name)
        skill_dir = os.path.join(base_dir, f"prompt_{safe_name}")
        os.makedirs(skill_dir, exist_ok=True)

        # Extract content
        prefix = meta.get("Prefix", "")
        suffix = meta.get("Suffix", "")

        # Try to extract a description from the prefix if possible, or just use name
        description = f"Execute the '{name}' prompt."

        content = f"""---
name: {safe_name}
description: {description}
type: prompt
---

# {name}

## Instructions
The following text is the prefix that will be added to the user input:

```text
{prefix}
```

The following text is the suffix that will be added to the user input:

```text
{suffix}
```

## Usage
Provide the input text that needs to be processed.
"""
        with open(os.path.join(skill_dir, "SKILL.md"), "w", encoding="utf-8") as f:
            f.write(content)

    # 2. Process Crazy Functions (Tools)
    try:
        from crazy_functional import get_crazy_functions
        crazy_funcs = get_crazy_functions()
    except Exception as e:
        print(f"Error loading crazy functions: {e}")
        crazy_funcs = {}

    for name, meta in crazy_funcs.items():
        safe_name = sanitize_name(name)
        skill_dir = os.path.join(base_dir, f"tool_{safe_name}")
        os.makedirs(skill_dir, exist_ok=True)

        info = meta.get("Info", "No description available.")
        group = meta.get("Group", "General")

        content = f"""---
name: {safe_name}
description: {info}
type: tool
group: {group}
---

# {name}

## Description
{info}

## Type
Tool / Plugin

## Group
{group}

## Implementation
This skill is backed by a Python function in the `crazy_functions` module.
"""
        with open(os.path.join(skill_dir, "SKILL.md"), "w", encoding="utf-8") as f:
            f.write(content)

    print(f"Generated {len(core_funcs)} prompts and {len(crazy_funcs)} tools in '{base_dir}/'.")

if __name__ == "__main__":
    generate_skills()
