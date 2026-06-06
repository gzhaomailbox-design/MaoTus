# Agent Instructions

## ReMo Project Memory

This repository uses ReMo to automatically maintain project memory for Coding Agents.

Before broad exploration:

1. Read `.remo/knowledge/index.md`.
2. Route the task to the smallest relevant knowledge set.
3. Scan the repo only when knowledge is missing, stale, contradicted, or not specific enough.

At task end:

1. Identify durable project knowledge created or invalidated by the work.
2. Update `.remo/knowledge/` automatically when evidence thresholds are met.
3. Update `.remo/knowledge/index.md` when knowledge files are added, renamed, deprecated, or repurposed.
4. Write a `.remo/logs/YYYY/MM/DD/` entry summarizing knowledge changes or explaining why no durable knowledge changed.

Before finishing meaningful work, run when practical:

```sh
sh skills/remo/scripts/remo-check.sh
```

Canonical ReMo source: `skills/remo/SKILL.md`.
