---
name: remo
description: Maintains Repo Memory for Vibe Coding projects by capturing milestone logs and distilled project knowledge. Use when the user mentions ReMo, Repo Memory, project memory, Vibe Coding knowledge, milestone logs, architecture notes, business process notes, or asks to preserve project context for future development.
---

# ReMo

ReMo means Repo Memory. It helps Vibe Coding projects keep two kinds of memory:

- Logs: chronological records of meaningful project progress, milestones, and decisions. Logs support retrospective review and are not assumed to be future context.
- Knowledge: distilled, stable project understanding such as architecture, business flows, product model, terminology, constraints, and FAQs. Knowledge is intended to reduce future codebase scanning and token usage.

ReMo's main purpose is context efficiency: read curated project knowledge first, scan the codebase only when the knowledge base is missing, stale, or too vague.

## Methodology

ReMo is a context-efficient project memory system for LLM-assisted development.

Use three principles:

- Route before read: read `.remo/knowledge/index.md` first, then load only the smallest relevant knowledge files.
- Distill before store: store stable understanding, not raw transcripts, command output, or obvious code facts.
- Evidence before trust: tie important claims to files, commits, PRs, logs, or explicit user decisions.

Use Context ROI to decide whether something belongs in ReMo:

```text
Will this memory save more future context than it costs to read?
```

Store high-ROI memory:

- Architecture boundaries and data flow.
- Cross-file business rules.
- Stable domain concepts and invariants.
- Important decisions and tradeoffs.
- Repeated pitfalls, constraints, and gotchas.
- Conventions future agents must follow.

Avoid low-ROI memory:

- File-by-file summaries with no insight.
- Code facts that are obvious from one small file.
- Temporary debugging noise.
- Full chat summaries.
- Raw diffs or command output without durable meaning.

Use SKR, Signal Knowledge Ratio, as the quality bar: every sentence should help future agents understand, decide, or avoid rediscovery.

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

Initialize this knowledge layout:

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

ReMo may be introduced after a project already exists. In that case, initialize all knowledge files above so future agents have stable destinations for project knowledge. Files may start as `Status: To be filled`, but they must explain what belongs there and what questions need investigation.

## Recommended Installation

For shared projects, keep the canonical ReMo source under `skills/remo/`.

To make ReMo persistent in a target project, install a project rule at:

```text
.cursor/rules/remo.mdc
```

Use [templates/remo-rule.mdc](templates/remo-rule.mdc) as the starting point. The rule should be `alwaysApply: true` so the agent performs a ReMo check during normal project work, even when the user does not explicitly mention ReMo.

## Memory Language

Before applying ReMo to a project for the first time, ask the user which language should be used for Repo Memory.

Record the answer in `.remo/knowledge/project-overview.md` or another appropriate knowledge file. After the language is recorded, keep future log filenames, log entries, and knowledge entries in that language unless the user changes the preference.

If the user changes the memory language later, update the project overview, knowledge index, and future entries. Existing entries may be translated when consistency matters.

## Workflow

### Initialize ReMo

When installing ReMo into an existing project:

1. Ask for the memory language.
2. Create `.remo/logs/` and `.remo/knowledge/`.
3. Create `.remo/knowledge/index.md`.
4. Create the baseline knowledge files:
   - `project-overview.md`
   - `architecture.md`
   - `domain-model.md`
   - `workflows.md`
   - `decisions.md`
   - `conventions.md`
   - `faq.md`
   - `glossary.md`
5. Fill what can be safely inferred from existing docs and top-level structure.
6. For unknown sections, write `Status: To be filled` and list specific open questions.
7. Add every baseline file to `index.md` with its purpose and task routing.
8. Create an installation log in `.remo/logs/` using the memory language.

Do not leave placeholder-only files. Even a newly initialized file should state what it is for, when to read it, and what is unknown.

### Initialize From GitHub History

If the project is connected to GitHub or another Git remote during initialization:

1. Inspect the default branch and commit history.
2. Group commits into meaningful phases, milestones, pivots, releases, bug-fix clusters, and architecture changes.
3. Create retrospective log entries for important historical moments only. Do not create one log per commit.
4. Use commit timestamps for log paths: `.remo/logs/YYYY/MM/DD/HHMM-title-in-memory-language.md`.
5. Use commit messages, changed file paths, tags, and merge commits as evidence.
6. Distill stable facts from history into the baseline knowledge files.
7. Mark lower-confidence conclusions as `Needs review` or list them under open questions.
8. Record the commit range or evidence source in each generated log or knowledge file.

Use history to improve accuracy, not to import noise. Prefer fewer, higher-signal retrospective logs.

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
3. Apply the Context ROI test. If the memory would not save future context or prevent likely mistakes, do not write it.
4. Update `.remo/knowledge/index.md` when creating, renaming, or changing the purpose of a knowledge file.
5. Keep entries concise and source-aware.
6. Separate facts from open questions.
7. Prefer updating an existing knowledge file over creating duplicates.
8. If the user has not asked to edit files, propose the memory entry before writing it.

### Commit And Push Checkpoint

Every commit and push must run a ReMo checkpoint.

Before committing:

1. Review the staged diff.
2. Create or update the relevant `.remo/logs/` entry for the work being committed.
3. Update affected `.remo/knowledge/` files so future agents can understand the change without rediscovering it.
4. Update `.remo/knowledge/index.md` if knowledge files were added, renamed, removed, or repurposed.
5. Include the ReMo updates in the same commit when they describe that commit's work.

After pushing:

1. Update the log entry with the commit hash, branch, remote, and push outcome when available.
2. If the push changed the published state or clarified project knowledge, update the relevant knowledge file.

Do not skip the checkpoint because a change feels small. If no durable knowledge changed, write that conclusion in the log with the reason, rather than inventing low-signal knowledge.

## Knowledge Routing

Use the smallest relevant context:

- Project direction or scope: read `index.md` and `project-overview.md`.
- Technical structure: read `index.md` and `architecture.md`.
- Business behavior: read `index.md`, `domain-model.md`, and `workflows.md`.
- Implementation style: read `index.md` and `conventions.md`.
- Prior tradeoffs: read `index.md` and `decisions.md`.
- Repeated issues: read `index.md` and `faq.md`.
- Terminology: read `index.md` and `glossary.md`.

If a baseline knowledge file is missing, create it before continuing and update the index.

## Log Entry Guidance

Create a log entry only when the project changes direction or crosses a useful checkpoint.

Good log triggers:

- Product direction, scope, or requirement changed.
- Architecture, module boundaries, or core data flow changed.
- A meaningful capability or end-to-end workflow became available.
- A durable decision was made, including why rejected options were not chosen.
- A major bug, incident, or risk changed future work.
- Git history reveals an important historical phase during initialization.

Do not log routine edits, minor fixes, typo changes, or one-off failed attempts unless they explain a durable project constraint.

Recommended filename:

```text
.remo/logs/YYYY/MM/DD/HHMM-title-in-memory-language.md
```

Store logs in year/month/day folders. Keep the file timestamp numeric for ordering within a day. The title segment should use the project's memory language.

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
- Focused on knowledge that future agents would otherwise rediscover by scanning multiple files.

A good ReMo log entry is:

- Useful for reconstructing how the project evolved.
- Focused on decisions, milestones, and reasons.
- Not a transcript of everything that happened.
- Still meaningful after weeks or months.
