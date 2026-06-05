---
name: linear-requirement-planner
description: 按 issue ID 读取 Linear 问题，判断它是否是软件需求，对模糊点提出严格的产品经理澄清问题，在 docs/01_designing/milestone/<YYYY-MM-DD-milestone-name> 下创建需求规划文档，并把计划摘要和预期 GitHub 链接评论回 Linear。用户提供 Linear issue ID 并要求转成产品或软件需求计划时使用。
---

# Linear 需求规划器

## 版本

- 当前版本：0.1.6
- 更新日期：2026-06-05
- 版本状态：Milestone 固定目录版本

使用或同步本 skill 前，先检查本节版本号与“更新记录”。如果用户级 Cursor skill、其他项目副本或历史文档中的版本更旧，默认以本仓库版本为准；如果版本更新但行为有差异，先阅读更新记录再执行需求规划。

## 更新记录

### 0.1.6 - 2026-06-05

- 明确最终路径格式为 `docs/01_designing/milestone/<YYYY-MM-DD-milestone-name>/<issue>.md`。
- 所有 milestone 计划文档都必须位于 `docs/01_designing/milestone/` 下，不能直接放在 `docs/01_designing/` 下。
- 无 milestone 的计划路径为 `docs/01_designing/milestone/未关联Milestone/<issue-id>-<中文短标题>.md`。

### 0.1.5 - 2026-06-05

- 已废弃的中间口径：曾明确路径格式为 `docs/01_designing/<YYYY-MM-DD-milestone-name>/<issue>.md`。
- Milestone 文件夹位于 `docs/01_designing/` 下，文件夹名由创建日期和 milestone 名称组成。
- 无 milestone 的计划路径为 `docs/01_designing/未关联Milestone/<issue-id>-<中文短标题>.md`。

### 0.1.4 - 2026-06-05

- 已废弃的中间口径：曾误解为 milestone 文件夹应位于 `docs` 下。
- 该口径已被后续版本覆盖；执行时必须以最新版本的 milestone 路径规则为准。

### 0.1.3 - 2026-06-04

- Milestone 文件夹命名改为“创建日期 + milestone 名字”，格式为 `YYYY-MM-DD-<milestone-name>`。
- 已存在的 milestone 文件夹必须复用，不因后续日期变化而创建第二个同名 milestone 文件夹。
- 无 milestone 的 issue 仍放入 `docs/01_designing/未关联Milestone/`。

### 0.1.2 - 2026-06-04

- 需求计划文档不再平铺在 `docs/01_designing` 下。
- 如果 Linear issue 关联 milestone，则放在 `docs/01_designing/<milestone-folder>/` 下；每个 milestone 一个文件夹，相关 design 放入同一文件夹。
- 如果 Linear issue 没有关联 milestone，则放在 `docs/01_designing/未关联Milestone/` 下。

### 0.1.1 - 2026-06-04

- 计划文档创建或更新后，只生成预期 GitHub 链接，不要求提交或推送。
- 如果本地文件路径、仓库 remote 和当前分支足以推导链接，直接生成预期 GitHub 链接，不再反复询问用户是否提交或推送。
- Linear 评论仍可包含计划摘要和预期 GitHub 链接，但必须明确该链接只有在当前分支推送到远端后才可访问。

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
   - 先确定 Linear issue 关联的 milestone。
   - 如果 issue 关联 milestone，在 `docs/01_designing/milestone/<milestone-folder>/` 下创建或更新 Markdown 文档；每个 milestone 只创建一个对应文件夹，相关 design 都放在该文件夹中。
   - 如果 issue 没有关联 milestone，在 `docs/01_designing/milestone/未关联Milestone/` 下创建或更新 Markdown 文档；不要把无 milestone 的计划平铺到 `docs/01_designing` 根目录。
   - `<milestone-folder>` 使用 milestone 文件夹首次创建日期加 milestone 名称生成，格式为 `YYYY-MM-DD-<milestone-name>`。
   - 日期使用创建该 milestone 文件夹当天的本地日期；如果对应 milestone 文件夹已存在，必须复用已有文件夹，不要因为日期变化创建新文件夹。
   - `<milestone-name>` 保留中文、英文、数字和常用连接符；把 `/`、空格和不适合作为路径的字符替换为 `-`，并去掉首尾连接符。
   - Markdown 文件名使用 issue ID 加中文简短标题，例如 `docs/01_designing/milestone/2026-06-04-支付里程碑/LIN-123-结账流程重设计.md`。
   - 文档文件名和文档内章节标题默认使用简体中文；除 Linear 原始字段名、产品专有名词、API 名称或必要英文 UI 文案外，不要把章节标题写成英文。
   - 如果相关文档已存在，先读取并更新它，不要创建重复文档。

7. 创建或更新计划后，把计划同步到 Linear issue 评论。
   - 先生成计划文档的预期 GitHub 地址，不要只使用本地文件路径。链接应指向当前仓库、当前分支上的计划文档；只要能从 git remote、当前分支和计划文档路径推导出 URL，就直接生成预期链接。
   - 不要为了让链接立即可访问而要求用户提交或推送；也不要反复询问是否需要提交或推送。
   - 如果当前分支尚未推送，或计划文档尚未提交，评论中仍使用预期 GitHub 链接，并明确“该链接在当前分支推送到远端后可访问”。
   - 只有当缺少 git remote、无法识别 GitHub 仓库地址、无法确认当前分支，或本地路径无法映射到仓库相对路径时，才向用户说明阻塞并询问如何处理。
   - 评论内容必须包含：计划摘要、计划文档预期 GitHub 链接、创建或更新时间。
   - 调用 Linear MCP 写评论前，必须先读取 `save_comment` 工具 descriptor。
   - 使用 Linear `save_comment` 工具，传入 `issueId` 和 Markdown `body` 创建顶层评论。
   - 评论正文使用简体中文；保留 Linear issue ID、GitHub URL、产品名和必要英文术语。

## GitHub 预期链接规则

生成预期 GitHub 链接时：

1. 从 git remote 推导仓库 URL。
   - 支持 `git@github.com:owner/repo.git`。
   - 支持 `https://github.com/owner/repo.git`。
2. 使用当前分支名作为 `blob/<branch>`。
3. 使用计划文档相对仓库根目录的路径。
4. 输出格式：

```text
https://github.com/<owner>/<repo>/blob/<branch>/<path>
```

该链接是预期链接，不代表文件已经提交或远端已经存在。除非用户明确要求，否则不要为了链接可访问而执行 commit 或 push。

## Milestone 文件夹规则

创建计划文档前，必须先判断 Linear issue 是否有关联 milestone。

- 有 milestone：路径为 `docs/01_designing/milestone/<YYYY-MM-DD>-<milestone-name>/<issue-id>-<中文短标题>.md`。
- 无 milestone：路径为 `docs/01_designing/milestone/未关联Milestone/<issue-id>-<中文短标题>.md`。
- 不要把计划文档直接放在 `docs/01_designing/` 根目录。
- 不要把计划文档直接放在 `docs/01_designing/<milestone-folder>/`；必须保留固定的 `milestone/` 中间目录。
- 如果目标 milestone 文件夹不存在，创建该文件夹。
- 新建 milestone 文件夹时，文件夹名前缀日期使用创建当天的本地日期，例如 `2026-06-04-支付里程碑`。
- 如果 `docs/01_designing/milestone` 下已存在同一 milestone 名称的日期前缀文件夹，复用已有文件夹；不要创建新的日期前缀文件夹。
- 如果目标文件夹中已有同一 issue ID 开头的计划文档，更新已有文档，不要创建重复文档。
- 生成预期 GitHub 链接时，必须使用最终分层后的相对路径。

Milestone 信息来源优先级：

1. Linear issue 的明确 milestone 字段。
2. Linear issue 关系中明确表示 milestone 的字段。
3. 如果 Linear 返回数据没有 milestone，视为无 milestone；不要用 project、release、label 或用户故事标题猜测 milestone。

## 计划文档模板

使用以下结构：

```markdown
# [Linear Issue ID] [需求标题]

## 来源

- Linear 问题：[Issue ID]
- Linear 标题：[Title]
- 状态：[Status]
- 负责人：[Owner if available]
- Milestone：[Milestone name 或 未关联Milestone]
- 文档路径：[docs/01_designing/milestone/<YYYY-MM-DD>-<milestone-name>/<file>.md 或 docs/01_designing/milestone/未关联Milestone/<file>.md]

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
- Linear 评论必须包含计划摘要、预期 GitHub 链接和时间；如果没有成功写入评论，最终回复必须明确说明原因。
- 计划文档必须位于 `docs/01_designing/milestone/<milestone-folder>/` 或 `docs/01_designing/milestone/未关联Milestone/` 下，不得平铺在 `docs/01_designing` 根目录，也不得直接放在 `docs/01_designing/<milestone-folder>/`。
