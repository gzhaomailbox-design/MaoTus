---
id: stable-kebab-case-id
title: Knowledge Title
type: map | topic | decision | convention | workflow | module | faq | glossary
status: active | needs_review | stale | deprecated
scope:
  - repo
confidence: high | medium | low
last_verified: YYYY-MM-DD
source_paths:
  - path/to/source
evidence:
  - type: file | git | log | user_decision | agent_observation
    ref: path-or-commit-or-log
supersedes: []
related: []
---

# Knowledge Title

## Summary

用短段落说明这条知识帮助未来 Agent 少读什么、少猜什么、避免什么错误。

## When To Read

- 哪些任务应读取本文件。
- 哪些任务不需要读取本文件。

## Current Knowledge

- 稳定事实、规则或约定。
- 跨文件或跨模块的理解。
- 需要未来 Agent 遵守的约束。

## Agent Guidance

- 未来 Agent 应如何使用这条知识。
- 修改相关代码时应检查哪些证据。

## Evidence

- `path/to/source`：说明证据支持了什么。

## Invalidation Signals

- 哪些文件、模块、流程或用户决策变化后，本知识需要标记为 `needs_review` 或 `stale`。
