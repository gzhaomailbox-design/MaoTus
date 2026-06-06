# ReMo Metadata

## Frontmatter

除 `.remo/knowledge/index.md` 外，所有正式 knowledge 文件必须包含 YAML frontmatter：

```yaml
---
id: project-overview
title: Project Overview
type: map
status: active
scope:
  - repo
confidence: high
last_verified: 2026-06-06
source_paths:
  - README.md
  - skills/remo/SKILL.md
evidence:
  - type: file
    ref: README.md
supersedes: []
related: []
---
```

## 字段

- `id`：稳定标识，使用 kebab-case，重命名文件时也尽量保持不变。
- `title`：人类可读标题。
- `type`：`map | topic | decision | convention | workflow | module | faq | glossary`。
- `status`：`active | needs_review | stale | deprecated`。
- `scope`：适用范围，优先使用 repo、目录、模块或任务类型。
- `confidence`：`high | medium | low`。
- `last_verified`：最近验证日期，格式 `YYYY-MM-DD`。
- `source_paths`：支持知识的 repo 内路径。外部来源写入 `evidence`，不强塞进路径。
- `evidence`：证据列表，`type` 可为 `file | git | log | user_decision | agent_observation`。
- `supersedes`：被当前知识替代的 knowledge id。
- `related`：相关 knowledge id。

## 正文结构

每个 knowledge 文件正文固定包含：

```md
# Title

## Summary

## When To Read

## Current Knowledge

## Agent Guidance

## Evidence

## Invalidation Signals
```

## 置信度规则

- `high`：由当前代码、文档、Git 或用户决策直接支持。
- `medium`：由多处间接证据或 Agent 推断支持，但仍可能需要后续验证。
- `low`：只能用于 `needs_review`，不得作为未来实现的强约束。

## 过期规则

如果 `source_paths` 不存在、证据冲突、相关模块被重写或用户撤销决策，ReMo 必须将 `status` 改为 `needs_review` 或 `stale`，并在正文写明失效信号。
