# ReMo Commands

## `remo init`

初始化 `.remo/config.yml`、`.remo/knowledge/index.md`、基础 maps/topics 和项目规则。

默认行为：

- 记忆语言来自用户选择或项目默认。
- 创建 `project-overview.md`。
- 若 repo 已有足够结构，创建 `maps/architecture.md`、`maps/modules.md`、`topics/conventions.md`。
- 安装或更新 `AGENTS.md` 的 `ReMo Project Memory` 小节，使用 `skills/remo/templates/AGENTS.md`。
- 安装或更新 `.cursor/rules/remo.mdc`，使用 `skills/remo/templates/remo-rule.mdc`。
- 写入安装日志。

安装入口规则时不得覆盖无关内容。已有 `AGENTS.md` 时只替换同名 ReMo 小节；没有同名小节时追加到文件末尾。

## `remo route "<task>"`

根据任务描述输出最小 knowledge 文件列表。

输出应包含：

- 必读文件。
- 可选文件。
- 缺失或过期的知识。
- 是否需要扫描 repo。

## `remo scan`

扫描 repo、文档、Git diff 或 Git history，输出 evidence set。`scan` 本身不写正式 knowledge。

## `remo absorb --task "<summary>"`

吸收任务结束时的 memory delta，并自动更新正式 knowledge。

必须：

- 合并重复主题。
- 更新 metadata。
- 更新 `index.md`。
- 写入日志。

## `remo checkpoint --git`

基于 staged diff、commit 或 push 结果更新 knowledge 和日志。

Commit 前必须说明：

- 哪些长期知识发生变化。
- 哪些 knowledge 被更新。
- 如果没有更新，为什么没有长期知识变化。

## `remo check`

检查：

- `.remo/config.yml` 是否存在。
- `.remo/knowledge/index.md` 是否存在。
- knowledge frontmatter 是否包含必需字段。
- `source_paths` 是否存在。
- 已有 knowledge 是否被索引提及。
- `AGENTS.md` 是否包含 ReMo Project Memory 小节和 `skills/remo/SKILL.md`。
- `.cursor/rules/remo.mdc` 是否指向 ReMo 权威来源。
- staged changes 是否需要 checkpoint 日志。

当前 `skills/remo/scripts/remo-check.sh` 是该命令的轻量 shell 实现。

## `remo-log-path`（脚本）

生成 ReMo 日志文件路径，供 Agent 写入前调用：

```sh
sh skills/remo/scripts/remo-log-path.sh "简体中文标题"
```

- 使用仓库机器本地 `date` 生成 `YYYY/MM/DD/HHMM-` 前缀。
- 禁止 Agent 自行推断或手写前缀（避免 Cursor 云端/会话时区与本地 git 时区不一致）。
- 同日同分钟冲突时自动追加 `-2`、`-3` 等后缀。
