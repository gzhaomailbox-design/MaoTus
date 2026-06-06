# MaoTus

MaoTus 是一个用于管理 Vibe Coding 实践中沉淀出来的 skills 的仓库。

这个项目收集可复用的工作流、提示词、模板、规格文档和项目知识，让后续 AI 辅助开发会话能更快进入状态，并使用更准确的上下文。每个 skill 都应被当作一个小项目维护：有明确目的、触发条件、工作流、质量标准，以及必要的模板、脚本或参考材料。

## 当前 Skills

### ReMo

入口：[skills/remo/SKILL.md](skills/remo/SKILL.md)

ReMo 是 Repo Memory，是面向 Coding Agent 的自动项目记忆系统。它从 repo、文档、Git、任务过程和用户决策中提取高信号知识，自动组织为可路由的 Markdown knowledge。

ReMo 的目标是让未来 Coding Agent 更少读代码、更少重复推理、更少输出无效内容。它允许在任务边界和 Git checkpoint 自动写入正式 `.remo/knowledge/`，但每条知识必须保留 evidence、confidence、scope、source_paths、last_verified 和失效信号。

ReMo 安装后会把自己暴露到 Agent 入口：通用入口 `AGENTS.md` 和 Cursor 入口 `.cursor/rules/remo.mdc`。这样 Codex、Cursor 等 Agent 更容易在普通 coding 任务中先读取 `.remo/knowledge/index.md` 并执行 ReMo checkpoint。

规格文档：

- [Architecture](skills/remo/specs/architecture.md)
- [Metadata](skills/remo/specs/metadata.md)
- [Agent Protocol](skills/remo/specs/agent-protocol.md)
- [Commands](skills/remo/specs/commands.md)

### Linear 需求规划器

入口：[skills/linear-requirement-planner/SKILL.md](skills/linear-requirement-planner/SKILL.md)

Linear 需求规划器用于按 Linear issue ID 读取 brief 需求，结合当前项目实际情况生成中文实现计划。计划文档会包含：

- 问题、目标、非目标和用户场景。
- 功能需求、非功能需求、用户流程和边界情况。
- 可测试验收标准。
- 完整测试用例设计。
- 基于项目实际情况的实施说明。

计划文档按 milestone 放在 `docs/01_designing/milestone/` 下，并把计划摘要和预期 GitHub 链接评论回 Linear。创建计划时不调用 ReMo；只有计划被实际执行并产生稳定项目变化后，才默认调用 ReMo 更新项目记忆。

## 仓库结构

```text
.
├── AGENTS.md
├── README.md
├── skills/
│   ├── remo/
│   │   ├── specs/
│   │   ├── templates/
│   │   └── scripts/
│   └── linear-requirement-planner/
└── .remo/
    ├── config.yml
    ├── logs/
    └── knowledge/
```

每个 skill 的正式入口是：

```text
skills/<skill-name>/SKILL.md
```

如果 skill 需要模板、脚本、规格或参考材料，应放在对应 skill 目录内，例如：

```text
skills/<skill-name>/templates/
skills/<skill-name>/scripts/
skills/<skill-name>/specs/
skills/<skill-name>/references/
```

## 维护约定

- README、skills、模板、ReMo 日志和知识文件默认使用简体中文。
- 保留必要的路径、命令、API 名、产品名和技术术语原文。
- 新增 skill 时，先把工作流、接口和质量标准定义清楚。
- 删除、重命名或改变 skill 目的时，同步更新 README 和 `.remo/knowledge/project-overview.md`。
- 对外分享的 skill 不依赖个人或本地 Cursor 配置目录，仓库内 `skills/<skill-name>/SKILL.md` 是权威来源。

## Repo Memory

本仓库本身也使用 ReMo：

- `.remo/config.yml` 保存自动记忆配置。
- `.remo/knowledge/index.md` 是任务路由入口。
- `.remo/knowledge/` 保存供未来 Coding Agent 复用的正式项目知识。
- `.remo/logs/` 记录自动写入、Git checkpoint 和重要项目进展。

处理 MaoTus 自身时，先读 `.remo/knowledge/index.md` 做上下文路由。任务结束和 Git checkpoint 应自动更新相关 knowledge，并写入 `.remo/logs/YYYY/MM/DD/`。

可运行检查器确认结构、metadata 和索引：

```sh
sh skills/remo/scripts/remo-check.sh
```
