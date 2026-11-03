---
name: gpt-academic
description: Use when an agent must discover and select a registered GPT Academic prompt or plugin, prepare its input, or explain the boundary between the application registry and published Agent Skills.
compatibility: Requires an existing GPT Academic checkout and runtime. Python 3.11+ is required for the bundled read-only catalog script; application execution remains owned by GPT Academic.
metadata:
  version: "0.1.0-alpha.1"
---

# GPT Academic

1. Identify whether the request is an immediate prompt action or an application plugin.
2. Run `scripts/catalog_capabilities.py --root <gpt-academic-checkout>` to observe the exact names declared by `core_functional.py` and `crazy_functional.py`. Do not import the application merely to enumerate its registry.
3. Treat catalog entries as GPT Academic capabilities, not independently published Skills. This package publishes one `gpt-academic` Skill.
4. Select the exact registered display name and preserve its declared group, visibility, description, and button status. Never infer a capability from a translated or normalized name.
5. Collect the input required by that capability—text, path, URL, archive, identifier, or advanced arguments—before requesting execution.
6. GPT Academic owns model access, file handling, plugin execution, network effects, and runtime results. The catalog script grants none of those authorities.
7. Require explicit confirmation before destructive entries such as deleting history or clearing caches, and report missing or dynamically unavailable registry data instead of inventing it.

Read `references/CONTRACT.md` for registry ownership, catalog schema, naming rules, and execution boundaries.
