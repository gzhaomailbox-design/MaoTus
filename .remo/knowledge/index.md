# ReMo Knowledge Index

## Memory Language

简体中文

## How To Use

任务开始时先读本索引。根据任务意图选择最小 knowledge 集合；只有当 knowledge 缺失、过期、冲突或不够具体时，再扫描 repo。

## Route Map

| Task Intent | Required Knowledge | Optional Knowledge |
| --- | --- | --- |
| 了解 MaoTus 项目定位、当前 skills、维护约定 | `project-overview.md` | `skills/remo/SKILL.md` |
| 设计、修改或实现 ReMo 自动记忆系统 | `project-overview.md`, `skills/remo/SKILL.md` | `skills/remo/specs/architecture.md`, `skills/remo/specs/agent-protocol.md`, `skills/remo/specs/metadata.md`, `skills/remo/specs/commands.md` |
| 修改 ReMo metadata、模板或检查规则 | `project-overview.md`, `skills/remo/specs/metadata.md` | `skills/remo/templates/knowledge-entry.md`, `skills/remo/scripts/remo-check.sh` |
| 修改 Agent 协议、AGENTS.md 或 Cursor rule | `project-overview.md`, `skills/remo/specs/agent-protocol.md` | `AGENTS.md`, `.cursor/rules/remo.mdc`, `skills/remo/templates/AGENTS.md`, `skills/remo/templates/remo-rule.mdc` |
| 准备 commit 或 push | `project-overview.md`, `skills/remo/specs/agent-protocol.md` | `sh skills/remo/scripts/remo-check.sh` |
| 处理 Linear 需求规划器 | `project-overview.md`, `skills/linear-requirement-planner/SKILL.md` | README |

## Knowledge Files

| File | Type | Status | When To Read |
| --- | --- | --- | --- |
| `project-overview.md` | map | active | MaoTus 项目高层上下文、ReMo 当前方向、skills 清单和维护约定 |

## Missing Knowledge

| Missing File | Creation Condition | Intended Use |
| --- | --- | --- |
| `maps/architecture.md` | MaoTus 出现稳定脚本、CLI、发布方式或多模块自动化后 | 技术结构、数据流和自动化边界 |
| `maps/modules.md` | skills 数量或共享脚本增加后 | skill/module 职责和边界 |
| `topics/conventions.md` | 文件命名、metadata、模板或测试规则稳定后 | 仓库维护和实现约定 |
| `topics/decisions.md` | 决策数量增加，需要集中索引后 | 长期产品和技术取舍 |

## Maintenance Rules

- 新增、删除、重命名或废弃 knowledge 文件时，更新本索引。
- 自动写入正式 knowledge 后，同步更新 Route Map 和 Knowledge Files。
- `status: stale` 或 `needs_review` 的文件可以被路由，但任务开始时必须重新验证。
- 日志文件不默认进入路由，除非某条日志是决策或事故的重要证据。

## Last Updated

2026-06-30
