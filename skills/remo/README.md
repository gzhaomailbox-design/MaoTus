# ReMo

ReMo means Repo Memory. It is a Vibe Coding skill for continuously preserving project memory while a repo evolves.

ReMo keeps two kinds of memory separate:

- Logs record the iteration process: milestones, decisions, pivots, experiments, and important checkpoints.
- Knowledge records distilled project understanding: architecture, business flows, product model, terminology, constraints, and FAQs.

## Why It Exists

Vibe Coding projects often move quickly. Important reasoning can be buried in chats, diffs, failed attempts, or temporary context. ReMo gives the project a lightweight memory layer so future work can start from curated knowledge instead of scanning the whole codebase again.

The core loop is:

1. Read the knowledge index before broad codebase exploration.
2. Route the task to the smallest useful set of knowledge files.
3. Scan code only when the knowledge base is missing, stale, or not specific enough.
4. Write new stable understanding back to the knowledge base.
5. On every commit and push, create a ReMo log and update affected knowledge files.

## Methodology

ReMo uses Context-Efficient Project Memory:

- Route before read: use the index before scanning.
- Distill before store: save stable understanding, not raw noise.
- Evidence before trust: connect claims to files, commits, PRs, logs, or user decisions.

Use the Context ROI test:

```text
Will this memory save more future context than it costs to read?
```

Use SKR, Signal Knowledge Ratio, as the writing standard. Prefer short, high-signal memory that helps future agents understand, decide, or avoid rediscovery.

## Recommended Project Layout

```text
.remo/
├── logs/
└── knowledge/
```

`logs/` is for retrospective history. It does not need to be loaded into future agent context by default.

`knowledge/` is for stable project knowledge that can be loaded early to save tokens and reduce rediscovery.

The required knowledge entry point is:

```text
.remo/knowledge/index.md
```

Use it to map task types to relevant knowledge files.

When ReMo is introduced into an existing project, initialize the full baseline knowledge set:

```text
.remo/knowledge/
├── index.md
├── project-overview.md
├── architecture.md
├── domain-model.md
├── workflows.md
├── decisions.md
├── conventions.md
├── faq.md
└── glossary.md
```

Files can start as `Status: To be filled`, but they should still explain their purpose and list concrete open questions. This gives future agents stable destinations for knowledge instead of rediscovering where context should live.

If the project has a GitHub or Git remote, ReMo can improve initialization by reviewing commit history. It should group historical commits into meaningful phases and create retrospective logs only for important milestones, pivots, releases, bug-fix clusters, or architecture changes. The same evidence can make baseline knowledge more accurate.

## Recommended Installation

Use `skills/remo/` as the shared source of the skill. In each project that wants to follow ReMo continuously, install a project rule:

```text
.cursor/rules/remo.mdc
```

Start from [templates/remo-rule.mdc](templates/remo-rule.mdc), then set the project's memory language and memory paths.

Rules are the recommended way to make ReMo persistent because they remind the agent to run a ReMo check during normal project work, even when the user does not explicitly mention ReMo.

Commit and push are mandatory ReMo checkpoints. The commit should include the relevant ReMo log and knowledge updates for the work being published. After pushing, update the log with commit hash, branch, remote, and push outcome when available.

## First Version Scope

This first version is intentionally manual:

- No scripts.
- No hooks.
- No background monitoring.
- No automatic milestone detector.

Agents use the ReMo rule, workflow, and templates to decide when to suggest or write memory entries.

## Templates

- [Log Entry](templates/log-entry.md)
- [Knowledge Entry](templates/knowledge-entry.md)
- [Knowledge Index](templates/knowledge-index.md)
- [Baseline Knowledge](templates/baseline-knowledge.md)
- [ReMo Rule](templates/remo-rule.mdc)
