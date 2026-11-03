# GPT Academic Skill package

Canonical source for one compiled `gpt-academic` Agent Skill.

GPT Academic prompt buttons and plugins remain application registry entries. They are not emitted as one Skill directory per menu item. `catalog_capabilities.py` reads the registry syntax without importing the application; the pinned `plugin-generator` validates, plans, and builds the declared package.

```sh
python packages/gpt-academic/source/skills/gpt-academic/scripts/catalog_capabilities.py \
  --root .
python -B -m unittest discover -s packages/gpt-academic/tests -v
```

A credentialed workflow-dispatch build uses the exact framework revision declared in `.github/workflows/skill-package.yml`. Generated BuildPlans and artifacts are not canonical source.
