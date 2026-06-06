# ReMo

ReMo 是 Repo Memory 的缩写，是面向 Coding Agent 的自动项目记忆系统。

它从 repo、文档、Git、任务过程和用户决策中提取高信号知识，自动组织为可路由的 Markdown knowledge。目标是让未来 Coding Agent 更少读代码、更少重复推理、更少输出无效内容，从而更高效也更省钱。

## 核心循环

1. 任务开始先读 `.remo/knowledge/index.md`。
2. 根据任务意图路由到最小 knowledge 集合。
3. 只有知识缺失、过期或不够具体时才扫描 repo。
4. 任务结束和 Git checkpoint 自动写入正式 knowledge。
5. 每条知识带 evidence、confidence、scope、source_paths 和失效信号。

## 项目结构

```text
.remo/
├── config.yml
├── knowledge/
│   ├── index.md
│   ├── project-overview.md
│   ├── maps/
│   └── topics/
└── logs/
```

`knowledge/` 是未来 Agent 的上下文入口。`logs/` 是时间线和自动写入审计记录，默认不加载进任务上下文。

## 自动写入

ReMo 允许自动更新正式 Markdown knowledge，但必须保留 provenance：

- 知识必须有 evidence。
- 置信度必须明确。
- source path 必须可追踪。
- 过期或冲突时标记 `needs_review` 或 `stale`。
- 自动写入不自动 commit，回滚依赖 Git diff。

## 命令形态

长期 CLI：

```sh
remo init
remo route "<task>"
remo scan
remo absorb --task "<summary>"
remo checkpoint --git
remo check
```

当前仓库提供轻量检查器：

```sh
sh skills/remo/scripts/remo-check.sh
```

安装到项目时，ReMo 应同时写入 Agent 入口：

- `AGENTS.md`：通用 Coding Agent / Codex 入口。
- `.cursor/rules/remo.mdc`：Cursor 入口。

已有 `AGENTS.md` 时，只追加或更新 `ReMo Project Memory` 小节，不覆盖其他项目说明。

## 规格文档

- [Architecture](specs/architecture.md)
- [Metadata](specs/metadata.md)
- [Agent Protocol](specs/agent-protocol.md)
- [Commands](specs/commands.md)

## Templates

- [日志条目](templates/log-entry.md)
- [知识条目](templates/knowledge-entry.md)
- [知识索引](templates/knowledge-index.md)
- [基线知识](templates/baseline-knowledge.md)
- [ReMo Rule](templates/remo-rule.mdc)
