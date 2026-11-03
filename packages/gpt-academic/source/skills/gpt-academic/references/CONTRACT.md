# GPT Academic capability contract

## Authority

This package owns one Agent Skill for discovering and selecting capabilities already registered by GPT Academic. It does not own the application registry, execute prompts or plugins, configure models, read user files, use the network, or grant destructive authority.

The application remains authoritative:

- `core_functional.py:get_core_functions()` declares immediate prompt actions.
- `crazy_functional.py:get_crazy_functions()` declares application plugins.
- each dictionary key is the exact user-facing capability name;
- registry metadata such as `Group`, `Info`, `Visible`, and `AsButton` remains application data.

A menu entry is not automatically a separate Agent Skill. Publishing one generated `SKILL.md` per prompt or plugin duplicates the application registry, loses package ownership, and creates unstable names. The compiled package therefore contains one `gpt-academic` Skill plus this contract and a deterministic catalog script.

## Catalog

Run:

```sh
python packages/gpt-academic/source/skills/gpt-academic/scripts/catalog_capabilities.py \
  --root /absolute/path/to/gpt_academic
```

The script parses Python syntax without importing GPT Academic. It emits:

```json
{
  "schema_version": "gpt-academic-capability-catalog/v1",
  "sources": ["core_functional.py", "crazy_functional.py"],
  "capabilities": [
    {
      "kind": "prompt",
      "name": "学术语料润色",
      "groups": ["prompt"],
      "description": "",
      "visible": true,
      "as_button": null
    }
  ]
}
```

Output is sorted by `(kind, name)`. The parser reads literal registry dictionaries, `function_plugins.update({...})`, and direct `function_plugins["name"] = {...}` assignments. Non-literal or runtime-generated entries are reported in `unavailable`; they are not guessed.

## Naming

Keep exact application display names in catalog output, including Unicode and punctuation. Published Skill identity remains the stable kebab-case name `gpt-academic`. Do not turn display labels into directory names or frontmatter names.

## Execution

Cataloging is read-only observation. A host adapter must separately authorize and execute the selected GPT Academic capability. Preserve required input, advanced arguments, destructive warnings, and observed outcome. A catalog hit is not proof that optional dependencies or runtime services are available.
