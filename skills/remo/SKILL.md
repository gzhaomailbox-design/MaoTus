---
name: remo
description: Maintains Repo Memory for Vibe Coding projects by capturing milestone logs and distilled project knowledge. Use when the user mentions ReMo, Repo Memory, project memory, Vibe Coding knowledge, milestone logs, architecture notes, business process notes, or asks to preserve project context for future development.
---

# ReMo

ReMo means Repo Memory. It helps Vibe Coding projects keep two kinds of memory:

- Logs: chronological records of meaningful project progress, milestones, and decisions. Logs support retrospective review and are not assumed to be future context.
- Knowledge: distilled, stable project understanding such as architecture, business flows, product model, terminology, constraints, and FAQs. Knowledge is intended to reduce future codebase scanning and token usage.

ReMo's main purpose is context efficiency: read curated project knowledge first, scan the codebase only when the knowledge base is missing, stale, or too vague.

## When To Use

Use ReMo when:

- The user explicitly asks to use ReMo or Repo Memory.
- A project reaches a meaningful milestone, decision, scope change, or implementation checkpoint.
- A stable piece of project knowledge emerges from exploration, implementation, debugging, or discussion.
- The user wants future agents to understand a project without rereading the whole codebase.

Do not use ReMo for:

- Low-value chat summaries.
- Temporary debugging noise.
- Raw command output unless it explains a durable decision.
- Unverified assumptions that should not guide future work.

## Target Project Layout

In each project managed by ReMo, prefer:

```text
.remo/
├── logs/
└── knowledge/
```

Use `logs/` for time-based project history. Use `knowledge/` for curated project knowledge.

Prefer this knowledge layout:

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

`index.md` is the required entry point. It maps task types to the smallest useful set of knowledge files.

## Recommended Installation

For shared projects, keep the canonical ReMo source under `skills/remo/`.

To make ReMo persistent in a target project, install a project rule at:

```text
.cursor/rules/remo.mdc
```

Use [templates/remo-rule.mdc](templates/remo-rule.mdc) as the starting point. The rule should be `alwaysApply: true` so the agent performs a ReMo check during normal project work, even when the user does not explicitly mention ReMo.

## Memory Language

Before applying ReMo to a project for the first time, ask the user which language should be used for Repo Memory.

Record the answer in `.remo/knowledge/project-overview.md` or another appropriate knowledge file. After the language is recorded, keep future log entries and knowledge entries in that language unless the user changes the preference.

If the user changes the memory language later, update the project overview, knowledge index, and future entries. Existing entries may be translated when consistency matters.

## Workflow

### Start Of Task

1. Check whether `.remo/knowledge/index.md` exists.
2. If it exists, read it before broad codebase exploration.
3. Use the index to select only the relevant knowledge files for the task.
4. Scan code only when the knowledge base is missing, stale, contradicted, or not specific enough.
5. If the project has no recorded memory language, ask the user before writing logs or knowledge entries.

### End Of Task

1. Decide whether the current work produced memory worth saving.
2. Classify it:
   - Use `logs/` for milestones, decisions, pivots, releases, experiments, and important iteration events.
   - Use `knowledge/` for stable knowledge that should help future work.
3. Update `.remo/knowledge/index.md` when creating, renaming, or changing the purpose of a knowledge file.
4. Keep entries concise and source-aware.
5. Separate facts from open questions.
6. Prefer updating an existing knowledge file over creating duplicates.
7. If the user has not asked to edit files, propose the memory entry before writing it.

## Knowledge Routing

Use the smallest relevant context:

- Project direction or scope: read `index.md` and `project-overview.md`.
- Technical structure: read `index.md` and `architecture.md`.
- Business behavior: read `index.md`, `domain-model.md`, and `workflows.md`.
- Implementation style: read `index.md` and `conventions.md`.
- Prior tradeoffs: read `index.md` and `decisions.md`.
- Repeated issues: read `index.md` and `faq.md`.
- Terminology: read `index.md` and `glossary.md`.

If a knowledge file is missing but the task reveals that category, create it or add it to the index as a known gap.

## Log Entry Guidance

Create a log entry when the project changes direction or crosses a useful checkpoint.

Recommended filename:

```text
.remo/logs/YYYY-MM-DD-HHMM-short-title.md
```

Use [templates/log-entry.md](templates/log-entry.md).

## Knowledge Entry Guidance

Create or update a knowledge entry when a durable project concept becomes clear.

Recommended filenames:

```text
.remo/knowledge/architecture.md
.remo/knowledge/business-flow.md
.remo/knowledge/product-model.md
.remo/knowledge/faq.md
.remo/knowledge/terminology.md
```

Use [templates/knowledge-entry.md](templates/knowledge-entry.md).

## Quality Bar

A good ReMo knowledge entry is:

- Abstract enough to survive minor code changes.
- Concrete enough to guide implementation.
- Short enough to load as context cheaply.
- Clear about confidence and unknowns.

A good ReMo log entry is:

- Useful for reconstructing how the project evolved.
- Focused on decisions, milestones, and reasons.
- Not a transcript of everything that happened.
