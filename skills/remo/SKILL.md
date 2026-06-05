---
name: remo
description: 通过里程碑日志和沉淀后的项目知识维护 Vibe Coding 项目的 Repo Memory。用户提到 ReMo、Repo Memory、项目记忆、Vibe Coding 知识、里程碑日志、架构笔记、业务流程笔记，或要求为未来开发保存项目上下文时使用。
---

# ReMo

ReMo 是 Repo Memory 的缩写。它帮助 Vibe Coding 项目保存两类记忆：

- 日志：按时间记录有意义的项目进展、里程碑和决策。日志用于回溯复盘，默认不作为未来任务上下文加载。
- 知识：沉淀后的稳定项目理解，例如架构、业务流程、产品模型、术语、约束和常见问题。知识用于减少未来代码扫描和 token 消耗。

ReMo 的核心目标是上下文效率：先读整理过的项目知识，只有当知识库缺失、过期或过于模糊时才扫描代码库。

## 方法论

ReMo 是面向 LLM 辅助开发的上下文高效项目记忆系统。

使用三条原则：

- Route before read：先读 `.remo/knowledge/index.md`，再只加载最小相关知识文件。
- Distill before store：保存稳定理解，而不是原始 transcript、命令输出或显而易见的代码事实。
- Evidence before trust：重要结论要关联到文件、commit、PR、日志或明确的用户决策。

使用 Context ROI 判断某条内容是否应该进入 ReMo：

```text
这条记忆节省的未来上下文，是否多于读取它本身消耗的上下文？
```

应保存高 ROI 记忆：

- 架构边界和数据流。
- 跨文件业务规则。
- 稳定领域概念和不变量。
- 重要决策和取舍。
- 重复出现的坑、约束和注意事项。
- 未来 Agent 必须遵守的约定。

避免低 ROI 记忆：

- 没有洞察的逐文件摘要。
- 从单个小文件即可看出的代码事实。
- 临时调试噪声。
- 完整聊天摘要。
- 缺少长期意义的原始 diff 或命令输出。

使用 SKR（Signal Knowledge Ratio）作为质量标准：每句话都应该帮助未来 Agent 理解、决策或避免重复发现。

## 何时使用

以下情况使用 ReMo：

- 用户明确要求使用 ReMo 或 Repo Memory。
- 项目达到有意义的里程碑、决策点、范围变化或实现检查点。
- 探索、实现、调试或讨论中产生了稳定项目知识。
- 用户希望未来 Agent 不必重读整个代码库也能理解项目。

不要将 ReMo 用于：

- 低价值聊天摘要。
- 临时调试噪声。
- 原始命令输出，除非它解释了长期有效的决策。
- 不应指导未来工作的未验证假设。

## 目标项目结构

每个由 ReMo 管理的项目推荐使用：

```text
.remo/
├── logs/
└── knowledge/
```

`logs/` 用于按时间记录项目历史。`knowledge/` 用于整理后的项目知识。

初始化以下知识结构：

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

`index.md` 是必需入口。它将任务类型映射到最小可用知识文件集合。

ReMo 可以后期引入已有项目。此时应初始化上述全部知识文件，让未来 Agent 有稳定的项目知识归档位置。文件可以从 `Status: To be filled` 开始，但必须说明这里应保存什么、还有哪些问题需要调查。

## 推荐安装方式

共享项目中，推荐将 ReMo 的权威来源放在 `skills/remo/`。

若要让 ReMo 在目标项目中持续生效，在以下位置安装项目规则：

```text
.cursor/rules/remo.mdc
```

以 [templates/remo-rule.mdc](templates/remo-rule.mdc) 为起点。规则应设置 `alwaysApply: true`，让 Agent 在普通项目工作中执行 ReMo 检查，即使用户没有明确提到 ReMo。

## 记忆语言

首次将 ReMo 应用于项目之前，询问用户 Repo Memory 应使用哪种语言。

将答案记录在 `.remo/knowledge/project-overview.md` 或其他合适的知识文件中。语言记录后，未来日志文件名、日志内容和知识条目都使用该语言，除非用户改变偏好。

如果用户之后修改记忆语言，更新项目概览、知识索引和后续条目。需要保持一致时，可以翻译已有条目。

## 工作流

### 初始化 ReMo

将 ReMo 安装到已有项目时：

1. 询问记忆语言。
2. 创建 `.remo/logs/` 和 `.remo/knowledge/`。
3. 创建 `.remo/knowledge/index.md`。
4. 创建基线知识文件：
   - `project-overview.md`
   - `architecture.md`
   - `domain-model.md`
   - `workflows.md`
   - `decisions.md`
   - `conventions.md`
   - `faq.md`
   - `glossary.md`
5. 从现有文档和顶层结构中填入可安全推断的事实。
6. 对未知部分写入 `Status: To be filled`，并列出具体待确认问题。
7. 将每个基线文件及其用途、任务路由加入 `index.md`。
8. 使用记忆语言在 `.remo/logs/` 中创建安装日志。

不要留下只有占位符的文件。即使是刚初始化的文件，也应说明用途、何时读取，以及哪些内容未知。

### 从 GitHub 历史初始化

如果初始化时项目已连接 GitHub 或其他 Git remote：

1. 检查默认分支和 commit 历史。
2. 将 commit 分组成有意义的阶段、里程碑、方向调整、发布、缺陷修复簇和架构变化。
3. 只为重要历史时刻创建回溯日志。不要每个 commit 创建一条日志。
4. 使用 commit 时间戳生成日志路径：`.remo/logs/YYYY/MM/DD/HHMM-记忆语言标题.md`。
5. 使用 commit message、变更文件路径、tag 和 merge commit 作为证据。
6. 将历史中的稳定事实沉淀到基线知识文件中。
7. 将低置信结论标记为 `Needs review`，或列入待确认问题。
8. 在每条生成的日志或知识文件中记录 commit 范围或证据来源。

使用历史来提升准确性，而不是导入噪声。优先创建更少、更高信号的回溯日志。

### 任务开始

1. 检查 `.remo/knowledge/index.md` 是否存在。
2. 如果存在，在大范围探索代码前先读取它。
3. 使用索引只选择任务相关的知识文件。
4. 只有当知识库缺失、过期、互相矛盾或不够具体时才扫描代码。
5. 如果项目尚未记录记忆语言，写入日志或知识前先询问用户。

### 任务结束

1. 判断当前工作是否产生了值得保存的记忆。
2. 分类：
   - 用 `logs/` 记录里程碑、决策、方向调整、发布、实验和重要迭代事件。
   - 用 `knowledge/` 记录应帮助未来工作的稳定知识。
3. 应用 Context ROI 判断。如果这条记忆不能节省未来上下文或避免高概率错误，不要写入。
4. 创建、重命名或改变知识文件用途时，更新 `.remo/knowledge/index.md`。
5. 条目保持简洁，并注明来源。
6. 区分事实和待确认问题。
7. 优先更新现有知识文件，避免创建重复主题。
8. 如果用户没有要求编辑文件，写入前先提出建议。

### Commit 和 Push 检查点

每次 commit 和 push 都必须执行 ReMo checkpoint。

提交前：

1. 检查 staged diff。
2. 为本次提交的工作创建或更新相关 `.remo/logs/` 条目。
3. 更新受影响的 `.remo/knowledge/` 文件，让未来 Agent 不必重新发现这次变化。
4. 如果新增、重命名、删除或改变了知识文件用途，更新 `.remo/knowledge/index.md`。
5. 如果 ReMo 更新描述的是本次提交的工作，将它们包含在同一个 commit 中。

推送后：

1. 在可获取时，用 commit hash、分支、remote 和 push 结果更新日志。
2. 如果 push 改变了发布状态或澄清了项目知识，更新相关知识文件。

不要因为改动看起来很小就跳过 checkpoint。如果没有长期知识变化，在日志中说明这个结论和原因，而不是编造低信号知识。

## 知识路由

使用最小相关上下文：

- 项目方向或范围：读取 `index.md` 和 `project-overview.md`。
- 技术结构：读取 `index.md` 和 `architecture.md`。
- 业务行为：读取 `index.md`、`domain-model.md` 和 `workflows.md`。
- 实现风格：读取 `index.md` 和 `conventions.md`。
- 历史取舍：读取 `index.md` 和 `decisions.md`。
- 重复问题：读取 `index.md` 和 `faq.md`。
- 术语：读取 `index.md` 和 `glossary.md`。

如果缺少基线知识文件，继续前先创建它并更新索引。

## 日志条目指南

只有当项目改变方向或跨过有价值的检查点时才创建日志条目。

适合写日志的触发条件：

- 产品方向、范围或需求发生变化。
- 架构、模块边界或核心数据流发生变化。
- 有意义的能力或端到端工作流可用了。
- 做出了长期决策，包括为什么没有选择被否定的方案。
- 重大 bug、事故或风险改变了未来工作。
- 初始化期间 Git 历史揭示了重要历史阶段。

不要记录日常编辑、小修复、错别字修改或一次性失败尝试，除非它们解释了长期项目约束。

推荐文件名：

```text
.remo/logs/YYYY/MM/DD/HHMM-记忆语言标题.md
```

日志按年/月/日分文件夹保存。文件时间戳保持数字，方便当天排序。标题段使用项目记忆语言。

使用 [templates/log-entry.md](templates/log-entry.md)。

## 知识条目指南

当长期有效的项目概念变清晰时，创建或更新知识条目。

推荐文件名：

```text
.remo/knowledge/architecture.md
.remo/knowledge/business-flow.md
.remo/knowledge/product-model.md
.remo/knowledge/faq.md
.remo/knowledge/terminology.md
```

使用 [templates/knowledge-entry.md](templates/knowledge-entry.md)。

## 质量标准

好的 ReMo 知识条目应当：

- 足够抽象，能经受小幅代码变化。
- 足够具体，能指导实现。
- 足够简短，能低成本加载为上下文。
- 清楚说明置信度和未知项。
- 聚焦未来 Agent 否则需要扫描多个文件才能重新发现的知识。

好的 ReMo 日志条目应当：

- 有助于重建项目演进过程。
- 聚焦决策、里程碑和原因。
- 不是完整过程转写。
- 数周或数月后仍然有意义。
