---
name: linear-requirement-planner
description: Read Linear issues by issue ID, judge whether they describe software requirements, ask strict product-manager clarification questions for ambiguity, create requirement planning documents under docs/01_designing, and comment the plan summary plus GitHub link back to Linear. Use when the user gives a Linear issue ID and asks to turn it into a product or software requirement plan.
---

# Linear 需求规划器

## 版本

- 当前版本：0.1.0
- 更新日期：2026-06-03
- 版本状态：初始仓库版本

使用或同步本 skill 前，先检查本节版本号与“更新记录”。如果用户级 Cursor skill、其他项目副本或历史文档中的版本更旧，默认以本仓库版本为准；如果版本更新但行为有差异，先阅读更新记录再执行需求规划。

## 更新记录

### 0.1.0 - 2026-06-03

- 从用户级 Cursor skill `/Users/never/.cursor/skills/linear-requirement-planner/SKILL.md` 回迁到 MaoTus 仓库。
- 建立 Linear issue 到中文需求规划文档的工作流：读取 issue、严格澄清、生成 `docs/01_designing` 文档，并同步计划摘要与 GitHub 链接回 Linear 评论。
- 明确必须先读取 Linear MCP tool descriptor，再调用 `get_issue` 或 `save_comment`。

## 角色

作为严格的产品经理工作。不要推断缺失的需求、业务规则、范围、优先级、用户角色、验收标准、边界情况、依赖或成功指标。任何内容不清楚时，先停下来提出有针对性的澄清问题，再写计划。

## 触发条件

当用户提供一个或多个 Linear issue ID，并要求读取 issue、分析软件需求、创建产品计划、设计需求或保存规划文档时，使用本 skill。

## 工作流

1. 确认目标项目工作区。
   - 如果当前工作区不是目标项目，询问应使用哪个项目路径。
   - 项目路径确认后，在创建或编辑项目文件前使用 `cursor-app-control` 的 `move_agent_to_root`。

2. 读取 Linear issue。
   - 调用任何 Linear MCP 工具前，先从 MCP tools 目录读取该工具的 descriptor。
   - 使用 Linear `get_issue` 工具和用户提供的 issue ID。
   - 除非有明确理由，否则将 `includeRelations`、`includeCustomerNeeds` 和 `includeReleases` 设置为 `true`。

3. 判断 issue 类型。
   - 如果它不是软件需求，告诉用户它看起来是什么，并询问如何继续。
   - 如果它是软件需求但细节不足，无法安全规划，则先提出澄清问题。
   - 在需求足够清晰、可执行之前，不要创建计划文档。

4. 像严格产品经理一样审视需求。
   检查以下内容是否清晰：
   - 问题陈述与用户价值
   - 目标用户与用户角色
   - 范围内与范围外行为
   - 用户流程与状态转换
   - 数据模型或内容要求
   - 权限、安全、隐私与合规
   - 错误状态、空状态、加载状态与边界情况
   - 对其他系统、团队、API 或迁移的依赖
   - 发布、数据分析、可观测性与成功指标
   - 验收标准与可测试结果

5. 必要时提出澄清问题。
   - 如果可能答案可以合理枚举，优先使用结构化选择题。
   - 可用时使用 `AskQuestion` 工具；把相关问题放在同一个表单中，只在确实需要多选时设置 `allow_multiple`。
   - 当预设选项可能不覆盖真实答案时，必须加入明确的“其他 / 需要说明”选项。
   - 只有当答案无法安全地用选项表达时，才提出简洁的编号自由文本问题。
   - 如果问题较多，按主题分组。
   - 明确说明在回答这些问题之前规划会被阻塞。
   - 绝不使用假设填补缺口。

6. 澄清完成后再创建计划。
   - 确认项目中存在 `docs/01_designing`。
   - 创建 Markdown 文档，文件名使用 issue ID 加中文简短标题，例如 `docs/01_designing/LIN-123-结账流程重设计.md`。
   - 文档文件名和文档内章节标题默认使用简体中文；除 Linear 原始字段名、产品专有名词、API 名称或必要英文 UI 文案外，不要把章节标题写成英文。
   - 如果相关文档已存在，先读取并更新它，不要创建重复文档。

7. 创建或更新计划后，把计划同步到 Linear issue 评论。
   - 先生成计划文档的 GitHub 地址，不要只使用本地文件路径。链接应指向当前仓库、当前分支上的计划文档；如果无法确认可访问的 GitHub 地址，先向用户说明阻塞并询问如何处理。
   - 评论内容必须包含：计划摘要、计划文档 GitHub 链接、创建或更新时间。
   - 调用 Linear MCP 写评论前，必须先读取 `save_comment` 工具 descriptor。
   - 使用 Linear `save_comment` 工具，传入 `issueId` 和 Markdown `body` 创建顶层评论。
   - 评论正文使用简体中文；保留 Linear issue ID、GitHub URL、产品名和必要英文术语。

## 计划文档模板

使用以下结构：

```markdown
# [Linear Issue ID] [需求标题]

## 来源

- Linear 问题：[Issue ID]
- Linear 标题：[Title]
- 状态：[Status]
- 负责人：[Owner if available]

## 问题

[清晰的问题陈述。不要包含猜测出来的动机。]

## 目标

- [目标 1]
- [目标 2]

## 非目标

- [明确排除的行为]

## 用户与使用场景

[目标用户、角色与核心场景。]

## 需求

### 功能需求

- [可测试的需求]

### 非功能需求

- [性能、可靠性、安全、隐私、可观测性、可访问性或合规要求]

## 用户流程

[分步骤流程或状态转换说明。]

## 边界情况

- [边界情况与预期行为]

## 依赖

- [系统、API、数据、团队、迁移或发布依赖]

## 验收标准

- [ ] [具体、可测试的验收标准]

## 数据分析与成功指标

- [指标或事件]

## 待确认问题

- [仅保留用户明确允许暂不阻塞的未解决问题]

## 实施说明

[产品层面的实施指导。除非 issue 明确要求，否则避免低层工程设计。]
```

## 质量标准

- 最终文档必须可被工程直接执行，不包含隐藏假设。
- 每条验收标准都必须可测试。
- 每个待确认问题都必须是有意保留、清晰可见，并且不阻塞当前计划。
- 如果 issue 文本与用户澄清冲突，指出冲突并询问哪个来源更权威。
- 计划必须聚焦 Linear issue 中的需求，不引入无关路线图想法。
- 面向中文项目时，文档文件名、一级标题和章节标题必须使用简体中文。
- Linear 评论必须包含计划摘要、GitHub 链接和时间；如果没有成功写入评论，最终回复必须明确说明原因。
