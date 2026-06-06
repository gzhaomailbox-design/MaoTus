# ReMo Knowledge Index

## Memory Language

[选择的记忆语言]

## How To Use

任务开始时先读取本索引。根据任务意图选择最小 knowledge 集合。只有当知识缺失、过期、冲突或不够具体时才扫描 repo。

## Route Map

| Task Intent | Required Knowledge | Optional Knowledge |
| --- | --- | --- |
| 项目方向、范围、当前状态 | `project-overview.md` | `maps/project.md` |
| 架构、模块边界、数据流 | `maps/architecture.md` | `maps/modules.md`, related topics |
| 领域实体、业务规则、不变量 | `maps/domain.md` | `topics/*` |
| 用户流程、运营流程、开发流程 | `maps/workflows.md` | related workflow topics |
| 编码约定、测试、命名、API 模式 | `topics/conventions.md` | `topics/testing.md` |
| 决策、取舍、被否定方案 | `topics/decisions.md` | related logs |
| 常见坑、排查路径、事故经验 | `topics/faq.md` | related logs |

## Knowledge Files

列出所有正式 knowledge 文件。所有已存在文件都必须在本节或 Route Map 中被提及。

| File | Type | Status | When To Read |
| --- | --- | --- | --- |
| `project-overview.md` | map | active | 项目高层上下文 |

## Missing Knowledge

列出应补齐但当前还没有足够证据生成的地图或主题。

| Missing File | Creation Condition | Intended Use |
| --- | --- | --- |
| `maps/architecture.md` | 架构边界、模块或运行方式稳定后 | 技术结构和数据流 |

## Maintenance Rules

- 新增、删除、重命名或废弃 knowledge 文件时，更新本索引。
- 自动写入正式 knowledge 后，同步更新 Route Map 和 Knowledge Files。
- `status: stale` 或 `needs_review` 的文件可以被路由，但必须在任务开始时提示需要重新验证。
- 日志文件不默认进入路由，除非某条日志是决策或事故的重要证据。

## Last Updated

YYYY-MM-DD
