---
name: remo
description: 自动维护 Coding Agent 可用的 Repo Memory。用户提到 ReMo、Repo Memory、自动项目记忆、项目知识、上下文路由、知识库、Agent 记忆、架构笔记、业务流程笔记、commit/push checkpoint，或要求让未来 Coding Agent 更高效、更省上下文时使用。
---

# ReMo

ReMo 是 Repo Memory 的缩写，是面向 Coding Agent 的自动项目记忆系统。

它持续从 repo 文件、文档、Git 历史、Git diff、Agent 任务过程和明确用户决策中提取高信号知识，并将这些知识组织成从顶层到细节的可路由 Markdown 知识库。目标不是节省生成记忆时的 token，而是降低未来 Coding Agent 的输入、输出和重复探索成本。

## 核心目标

- 自动组织项目知识：把项目目标、架构、领域模型、工作流、模块职责、约定、决策和常见坑沉淀到 `.remo/knowledge/`。
- 自动路由上下文：任务开始时先读取 `.remo/knowledge/index.md`，再按任务意图加载最小知识集合。
- 自动写入正式知识库：任务结束和 Git checkpoint 时，满足证据阈值的知识直接更新正式 Markdown 文件。
- 保持可审计：每条知识必须有来源、置信度、适用范围、最后验证时间和失效信号。
- 保持 Git 友好：自动写入通过普通文件 diff 呈现，回滚依赖 Git。

## 方法论

ReMo 使用 Context-Efficient Project Memory：

- Route before read：先路由到最小知识包，再决定是否扫描代码。
- Distill before store：保存稳定理解，而不是原始 transcript、命令输出或逐文件摘要。
- Evidence before trust：正式知识必须关联到文件、commit、diff、日志或明确用户决策。
- Auto-write with provenance：允许自动写入正式知识库，但每次写入都必须留下 provenance。
- Optimize future agent cost：优化目标是让未来 Agent 少读、少猜、少返工。

使用 Context ROI 判断某条内容是否应该进入 ReMo：

```text
这条记忆能否让未来 Coding Agent 少加载更多上下文、少重复推理，或避免高概率错误？
```

优先保存：

- 架构边界、模块职责和数据流。
- 跨文件业务规则、领域不变量和工作流。
- 稳定约定、测试策略和开发流程。
- 长期决策、被否定方案及原因。
- 重复出现的坑、事故经验和排查路径。
- 未来 Agent 必须遵守的项目特定规则。

避免保存：

- 从单个小文件即可看出的事实。
- 没有抽象价值的逐文件摘要。
- 临时调试噪声。
- 未验证且会误导未来实现的猜测。
- 完整聊天记录或原始 diff。

## 目标项目结构

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

- `.remo/config.yml`：记忆语言、自动化触发、证据阈值、忽略路径和知识层级。
- `.remo/knowledge/index.md`：必读入口，按任务意图路由到最小知识集合。
- `.remo/knowledge/maps/`：顶层地图，如 project、architecture、domain、workflows、modules。
- `.remo/knowledge/topics/`：细分主题页，如 testing、deployment、ui-conventions、feature-specific topics。
- `.remo/logs/`：自动运行、里程碑、checkpoint 和写入摘要；默认不作为任务上下文加载。
- **整个 `.remo/` 目录**（`config.yml`、`knowledge/`、`logs/` 等）默认纳入 Git 版本库（`config.yml` 的 `git.track_all: true`）。

轻量项目可以先只创建 `index.md` 和 `project-overview.md`，但所有已存在知识文件都必须被索引路由，且 `index.md` 必须记录未来应补齐的地图或主题。

## Markdown 知识接口

正式知识使用 Markdown + YAML frontmatter。所有 `.remo/knowledge/**/*.md` 除 `index.md` 外都必须包含：

```yaml
---
id: stable-id
title: Human readable title
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
```

正文固定包含：

- Summary
- When To Read
- Current Knowledge
- Agent Guidance
- Evidence
- Invalidation Signals

字段细节见 `skills/remo/specs/metadata.md`。

## 自动化触发

ReMo 默认在任务边界和 Git checkpoint 运行：

- 任务开始：读取 `index.md`，根据任务描述选择最小知识包；知识不足时再扫描 repo。
- 任务结束：Agent 提供本次任务的 memory delta；ReMo 根据证据阈值自动更新正式 knowledge。
- Commit 前：基于 staged diff 更新相关知识和日志。
- Push 后：在可获取时用 commit、branch、remote 和 push 结果补充日志。
- 手动命令：允许用户或 Agent 显式运行 `remo route`、`remo scan`、`remo absorb`、`remo checkpoint`、`remo check`。

不做默认文件 watcher。每次文件变化都自动写记忆容易引入噪声和成本，后续只有在有明确收益时再作为可选扩展。

## 自动写入安全规则

ReMo 允许自动写入正式 knowledge，但必须满足：

- 每条新增或更新知识至少有一个 evidence。
- `confidence: high` 需要代码/文档/Git/用户决策中至少一个强证据。
- `confidence: medium` 可以来自 Agent 推断，但必须写明来源和失效信号。
- `confidence: low` 不应指导实现；只能进入 `needs_review`。
- 用户明确决策优先级最高，其次是当前代码事实，再次是 Git 历史推断，最后是 Agent 推断。
- 当 source path 删除、证据不再成立或知识互相矛盾时，标记 `needs_review` 或 `stale`，不要静默删除。
- 自动写入不自动 commit，所有变化通过 Git diff 审计和回滚。

## 命令接口

ReMo 的长期 CLI 形态：

```sh
remo init
remo route "<task>"
remo scan
remo absorb --task "<summary>"
remo checkpoint --git
remo check
```

当前仓库提供轻量脚本：

```sh
sh skills/remo/scripts/remo-log-path.sh "中文标题"   # 生成本地时间日志路径（写入前必用）
sh skills/remo/scripts/remo-check.sh                   # remo check
```

脚本是 `remo check` 的可移植初版，负责检查 `.remo` 结构、knowledge frontmatter、索引路由、source path、Cursor rule 和 staged checkpoint 提醒。命令细节见 `skills/remo/specs/commands.md`。

## Agent 协议

### 任务开始

1. 读取 `.remo/knowledge/index.md`。
2. 根据任务描述选择最小知识集合。
3. 读取相关 map/topic。
4. 如果知识缺失、过期、冲突或不够具体，再扫描 repo。
5. 记录任务中发现的知识缺口，留给任务结束 absorb。

### 任务结束

1. 产出 structured memory delta：新增事实、更新事实、失效事实、证据、适用范围、置信度。
2. ReMo 将 delta 合并到现有 knowledge。
3. 更新 `last_verified`、`source_paths`、`evidence`、`related`。
4. 如新增、移动或废弃知识文件，更新 `index.md`。
5. 写入 ReMo 日志记录本次自动写入摘要。**禁止**自行推断、心算或手写 `YYYY/MM/DD/HHMM-` 前缀（Cursor 云端/会话时区 ≠ 仓库机器本地时区，会与 git commit 时区严重不符）。**必须**先运行：

```sh
sh skills/remo/scripts/remo-log-path.sh "中文标题"
```

将 stdout 作为日志路径再写入；`HHMM` 仅来自脚本内 `date`（仓库机器本地 24 小时制）。同日同分钟冲突时脚本自动追加 `-2`、`-3` 后缀。

### Git checkpoint

1. Commit 前检查 staged diff。
2. 判断 diff 是否改变长期项目理解。
3. 自动更新受影响 knowledge。
4. 写入 checkpoint 日志，说明更新了哪些知识；如没有长期知识变化，说明原因。
5. **`git status --short .remo/`**；有变更则 **`git add .remo/`**，与业务代码同批 stage、**同一 commit**。**禁止**只提交源码而遗漏 ReMo；**勿等用户提醒**「记得 ReMo」。仅当用户明确说不要提交 ReMo 时可例外。
6. 运行 `sh skills/remo/scripts/remo-check.sh`；staged 有业务改动但无 `.remo/` 时不得 commit。
7. Push 后补充 commit hash、branch、remote 和 push 结果。

## 安装方式

共享项目中，推荐将 ReMo 权威来源放在：

```text
skills/remo/SKILL.md
```

ReMo 安装后必须把自己暴露给 Coding Agent 的常规入口。默认安装以下文件：

```text
AGENTS.md
.cursor/rules/remo.mdc
```

`AGENTS.md` 是通用 Agent 入口，适合 Codex 和其他会读取仓库级 instructions 的 Coding Agent。`.cursor/rules/remo.mdc` 是 Cursor 入口。

如果目标项目已有 `AGENTS.md`，不要覆盖原文；追加或更新名为 `ReMo Project Memory` 的小节，内容以 `skills/remo/templates/AGENTS.md` 为准。

如果目标项目已有 `.cursor/rules/remo.mdc`，用 `skills/remo/templates/remo-rule.mdc` 同步更新。

Cursor 项目规则：

```text
.cursor/rules/remo.mdc
```

规则必须设置 `alwaysApply: true`，让 Agent 在普通任务中自动执行 ReMo 协议。

## 规格文档

- `skills/remo/specs/architecture.md`
- `skills/remo/specs/metadata.md`
- `skills/remo/specs/agent-protocol.md`
- `skills/remo/specs/commands.md`

## 质量标准

好的 ReMo 知识应当：

- 让未来 Agent 更快确定应该读什么、不该读什么。
- 能指导实现，而不是只描述存在什么文件。
- 有清晰证据、范围、置信度和失效信号。
- 在小幅代码变化后仍然有效，或能被自动标记为需要复核。
- 足够短，加载成本明显低于重新扫描和推理成本。
