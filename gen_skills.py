import importlib
import os
import shutil
import re

def sanitize_name(name):
    # Standardize to lowercase, replace special chars with hyphens
    # name = name.lower() # User's code base has capitalized names in SKILL.md.
    # However, skill-writer spec says "Lowercase letters, numbers, hyphens only".
    # So we should enforce lowercase.

    # Remove any non-alphanumeric chars that are not spaces or hyphens
    name = re.sub(r'[^\w\s-]', '', name)
    # Replace spaces and underscores with hyphens
    name = name.strip().replace(" ", "-").replace("_", "-")
    # Convert to lowercase
    name = name.lower()
    # Remove multiple hyphens
    name = re.sub(r'-+', '-', name)
    return name

def generate_skills():
    # Setup directories
    base_dir = "skills"

    # Check if base_dir exists. If so, we want to clear it BUT preserve 'skill-writer' if it exists.
    # Actually, simplest is to check if skill-writer exists, read it, clear dir, restore it.
    skill_writer_path = os.path.join(base_dir, "skill-writer", "SKILL.md")
    skill_writer_content = None
    if os.path.exists(skill_writer_path):
        with open(skill_writer_path, 'r', encoding='utf-8') as f:
            skill_writer_content = f.read()

    if os.path.exists(base_dir):
        shutil.rmtree(base_dir)
    os.makedirs(base_dir)

    # Restore skill-writer
    if skill_writer_content:
        sw_dir = os.path.join(base_dir, "skill-writer")
        os.makedirs(sw_dir)
        with open(os.path.join(sw_dir, "SKILL.md"), "w", encoding='utf-8') as f:
            f.write(skill_writer_content)

    # 1. Process Core Functions (Prompts)
    import core_functional
    importlib.reload(core_functional)
    core_funcs = core_functional.get_core_functions()

    for name, meta in core_funcs.items():
        safe_name = sanitize_name(name)
        # Prefix with 'prompt-' to distinguish and ensure uniqueness if names collide
        # But 'prompt-' adds clutter. User guide says "good: pdf-processor".
        # Let's use semantic names. 'prompt-<name>' is okay for now to avoid collision.
        safe_name = f"prompt-{safe_name}"

        skill_dir = os.path.join(base_dir, safe_name)
        os.makedirs(skill_dir, exist_ok=True)

        # Extract content
        prefix = meta.get("Prefix", "")
        suffix = meta.get("Suffix", "")

        # Generate Description adhering to "What + When + Triggers"
        # Since we don't have "When" metadata, we construct a generic one.
        description = f"Execute the '{name}' prompt template. Use when the user wants to perform '{name}' or apply this specific prompt pattern."

        content = f"""---
name: {safe_name}
description: {description}
type: prompt
---

# {name}

## Quick start
Use this skill to wrap your input with the defined prompt template.

## Instructions
The system will apply the following prefix and suffix to the user input.

**Prefix**:
```text
{prefix}
```

**Suffix**:
```text
{suffix}
```

## Examples
User: "Apply {name} to this text: ..."
Agent: [Executes skill]

## Requirements
- None
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
        # Avoid collision
        if not safe_name.startswith("tool-"):
            safe_name = f"tool-{safe_name}"

        skill_dir = os.path.join(base_dir, safe_name)
        os.makedirs(skill_dir, exist_ok=True)

        info = meta.get("Info", "No description available.")
        group = meta.get("Group", "General")

        # Improve description
        description = f"{info} Use when performing {group}-related tasks involving {name}."
        if len(description) > 1024:
            description = description[:1021] + "..."

        content = f"""---
name: {safe_name}
description: {description}
type: tool
group: {group}
---

# {name}

## Quick start
This is a tool-based skill provided by the `crazy_functions` plugin system.

## Instructions
This skill allows the agent to perform complex tasks defined in the `{name}` plugin.
It belongs to the **{group}** category.

**Function Info**:
{info}

## Examples
User: "Run {name} on this file..."

## Implementation
Python Module: `crazy_functions`
"""
        with open(os.path.join(skill_dir, "SKILL.md"), "w", encoding="utf-8") as f:
            f.write(content)

    print(f"Generated {len(core_funcs)} prompts and {len(crazy_funcs)} tools in '{base_dir}/'.")

if __name__ == "__main__":
    generate_skills()
