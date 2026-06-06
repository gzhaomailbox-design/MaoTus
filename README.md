# MaoTus

MaoTus 是一个用于管理 Vibe Coding 实践中沉淀出来的 skills 的仓库。

这个项目收集可复用的工作流、提示词、模板和项目知识，让后续 AI 辅助开发会话能更快进入状态，并使用更准确的上下文。每个 skill 都应被当作一个小项目维护：有明确目的、触发条件、工作流、质量标准，以及必要的模板或辅助材料。

## 当前 Skills

### ReMo

入口：[skills/remo/SKILL.md](skills/remo/SKILL.md)

ReMo 是 Repo Memory，用于在仓库演进过程中持续保存项目记忆。它将两类内容分开：

- 过程日志：记录里程碑、决策、方向调整和重要检查点。
- 项目知识：沉淀架构、业务流程、产品模型、术语、约束和常见问题。

ReMo 的目标是上下文效率：未来任务先读整理过的知识，再决定是否需要扫描代码库。

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
├── README.md
├── skills/
│   ├── remo/
│   └── linear-requirement-planner/
└── .remo/
    ├── logs/
    └── knowledge/
```

每个 skill 的正式入口是：

```text
skills/<skill-name>/SKILL.md
```

如果 skill 需要模板、脚本或参考材料，应放在对应 skill 目录内，例如：

```text
skills/<skill-name>/templates/
skills/<skill-name>/scripts/
skills/<skill-name>/references/
```

## 维护约定

- README、skills、模板、ReMo 日志和知识文件默认使用简体中文。
- 保留必要的路径、命令、API 名、产品名和技术术语原文。
- 新增 skill 时，先把工作流定义清楚，第一版保持轻量。
- 只有当手动流程被验证有价值后，再加入脚本、hooks 或自动化。
- 删除、重命名或改变 skill 目的时，同步更新 README 和 `.remo/knowledge/project-overview.md`。
- 对外分享的 skill 不依赖个人或本地 Cursor 配置目录，仓库内 `skills/<skill-name>/SKILL.md` 是权威来源。

## Repo Memory

本仓库本身也使用 ReMo：

- `.remo/logs/` 记录重要项目进展。
- `.remo/knowledge/` 保存供未来任务复用的高信号项目知识。

处理 MaoTus 自身时，先读 `.remo/knowledge/index.md` 做上下文路由。重要里程碑写入 `.remo/logs/YYYY/MM/DD/`，稳定项目理解写入 `.remo/knowledge/`。

Commit 和 push 是 ReMo checkpoint：提交前应包含对应日志和必要知识更新；推送后在日志中记录 commit hash、分支、remote 和推送结果（可获取时）。
