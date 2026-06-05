# ReMo

ReMo 是 Repo Memory 的缩写，是一个在仓库演进过程中持续保存项目记忆的 Vibe Coding skill。

ReMo 将两类记忆分开保存：

- 日志记录迭代过程：里程碑、决策、方向调整、实验和重要检查点。
- 知识记录沉淀后的项目理解：架构、业务流程、产品模型、术语、约束和常见问题。

## 为什么需要它

Vibe Coding 项目通常推进很快，重要推理容易散落在对话、diff、失败尝试或临时上下文里。ReMo 给项目增加一层轻量记忆，让未来任务从整理过的知识开始，而不是每次重新扫描整个代码库。

核心循环是：

1. 大范围探索代码前先读知识索引。
2. 将任务路由到最小必要知识文件集合。
3. 只有当知识库缺失、过期或不够具体时才扫描代码。
4. 将新的稳定理解写回知识库。
5. 每次 commit 和 push 时创建 ReMo 日志，并更新受影响的知识文件。

## 方法论

ReMo 使用 Context-Efficient Project Memory：

- Route before read：扫描前先使用索引。
- Distill before store：保存稳定理解，而不是原始噪声。
- Evidence before trust：重要结论要关联到文件、commit、PR、日志或用户决策。

使用 Context ROI 判断：

```text
这条记忆节省的未来上下文，是否多于读取它本身消耗的上下文？
```

使用 SKR（Signal Knowledge Ratio）作为写作标准。优先写短而高信号的记忆，帮助未来 Agent 理解、决策或避免重复发现。

## 推荐项目结构

```text
.remo/
├── logs/
└── knowledge/
```

`logs/` 用于回溯历史，默认不需要加载进未来 Agent 的上下文。

`knowledge/` 用于稳定项目知识，可在任务早期加载，以节省 token 并减少重复探索。

必需的知识入口是：

```text
.remo/knowledge/index.md
```

使用它将任务类型映射到相关知识文件。

当 ReMo 后期引入已有项目时，初始化完整基线知识集合：

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

文件可以从 `Status: To be filled` 开始，但仍应说明用途并列出具体待确认问题。这样未来 Agent 会有稳定的知识归档位置，而不是重新判断上下文应该放在哪里。

如果项目有 GitHub 或其他 Git remote，ReMo 可以通过回顾 commit 历史提升初始化质量。它应将历史 commit 分组成有意义的阶段，只为重要里程碑、方向调整、发布、缺陷修复簇或架构变化创建回溯日志。同一批证据也可用于校准基线知识。

## 推荐安装方式

使用 `skills/remo/` 作为 skill 的共享来源。每个需要持续执行 ReMo 的项目都应安装项目规则：

```text
.cursor/rules/remo.mdc
```

从 [templates/remo-rule.mdc](templates/remo-rule.mdc) 开始，然后设置项目的记忆语言和记忆路径。

推荐用规则让 ReMo 持续生效，因为规则会在普通项目工作中提醒 Agent 执行 ReMo 检查，即使用户没有显式提到 ReMo。

Commit 和 push 是强制 ReMo checkpoint。提交应包含本次发布工作对应的 ReMo 日志和知识更新。推送后，在可获取时用 commit hash、分支、remote 和 push 结果更新日志。

## 第一版范围

第一版刻意保持手动：

- 不包含脚本。
- 不包含 hooks。
- 不包含后台监控。
- 不包含自动里程碑检测。

Agent 通过 ReMo 规则、工作流和模板判断何时建议或写入记忆条目。

## Templates

- [日志条目](templates/log-entry.md)
- [知识条目](templates/knowledge-entry.md)
- [知识索引](templates/knowledge-index.md)
- [基线知识](templates/baseline-knowledge.md)
- [ReMo Rule](templates/remo-rule.mdc)
