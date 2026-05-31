# 知识索引

## 记忆语言

简体中文

## 使用方式

在扫描代码库之前，先阅读本索引。根据任务类型选择最小必要知识文件；只有当知识缺失、过期、互相矛盾或不够具体时，再按需扫描代码库。

## 任务路由

| 任务类型 | 优先阅读 |
| --- | --- |
| 了解项目定位、范围、当前方向 | `project-overview.md` |
| 了解 ReMo 的目标和当前设计 | `project-overview.md` |
| 新增或调整 skill 项目 | `project-overview.md` |
| 判断是否需要更新项目知识 | `project-overview.md` |
| 判断日志或知识是否详略得当 | `project-overview.md`，并参考 `skills/remo/SKILL.md` 的 Methodology 和 Quality Bar |
| 准备 commit 或 push | `project-overview.md`，并执行 `skills/remo/SKILL.md` 的 Commit And Push Checkpoint |
| 将 ReMo 后期安装到已有项目 | `project-overview.md`，并参考 `skills/remo/templates/knowledge-index.md` 和 `skills/remo/templates/baseline-knowledge.md` |
| 根据 GitHub commit 历史回溯项目日志和知识 | `project-overview.md`，并参考 `skills/remo/SKILL.md` 的初始化流程 |
| 查找尚未沉淀的技术架构、业务流程、约定、FAQ | 查看下方“已知缺口” |

## 当前知识文件

### `project-overview.md`

说明 MaoTus 的项目定位、ReMo 的角色、记忆语言、当前实践方式和未决问题。

适合在处理项目方向、skill 结构、ReMo 规则、知识库维护时优先阅读。

## 已知缺口

这些文件代表未来可能需要沉淀的知识类型；当前项目还没有足够内容，因此暂不创建空文件。

- `architecture.md`：当仓库出现稳定技术结构、脚本、自动化或发布方式时创建。
- `domain-model.md`：当 MaoTus 形成明确的 skill 元模型、分类体系或数据结构时创建。
- `workflows.md`：当 ReMo 或其他 skills 形成可复用工作流时创建。
- `decisions.md`：当技术或产品决策变多，需要集中索引时创建。
- `conventions.md`：当文件命名、skill 编写、模板风格形成稳定约定时创建。
- `faq.md`：当重复问题出现时创建。
- `glossary.md`：当术语变多，且需要统一解释时创建。

## 维护规则

- 新增、删除、重命名知识文件时，必须更新本索引。
- 知识文件用途发生变化时，必须更新“当前知识文件”说明。
- 不要为了完整目录而创建空知识文件；只在有稳定内容时创建。
- 日志文件不列入本索引，除非某条日志成为重要决策来源。
- `.remo/logs/` 按年月日分文件夹存储，路径格式为 `.remo/logs/YYYY/MM/DD/HHMM-记忆语言标题.md`。
- `.remo/logs/` 的文件名标题段和日志内容都应使用当前记忆语言。
- `.remo/knowledge/` 的知识内容应使用当前记忆语言。
- ReMo 初始化到已有项目时，应创建完整基线知识文档集合，并用 `Status: To be filled` 标记尚未确认的内容。
- 如果项目关联了 GitHub 或其他 Git remote，初始化时应分析 commit 历史，把重要阶段回溯成高信号日志，并用历史证据校准基线知识文件。
- 写入日志或知识前必须应用 Context ROI：只有当记忆能减少未来上下文成本、避免重复推理或降低错误风险时才写入。
- 使用 SKR 作为写作标准：每句话都应帮助未来 Agent 理解、决策或避免重复发现。
- 每次 commit 和 push 都是强制 ReMo checkpoint：必须生成或更新日志，并同步受影响的知识文件和索引。

## 最后更新

2026-05-31
