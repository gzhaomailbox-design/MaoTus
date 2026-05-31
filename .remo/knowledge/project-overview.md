# 项目概览

## 记忆语言

简体中文

## 摘要

MaoTus 是一个用于管理 Vibe Coding 实践中沉淀出来的 skills 的仓库。它的第一个 skill 是 ReMo，也就是 Repo Memory，用于保存项目过程日志和抽象后的项目知识。

## 适用范围

这份知识适用于整个 MaoTus 仓库。后续处理项目定位、skill 结构、新 skill 创建或 ReMo 实践时，应优先读取这份知识。

## 当前理解

- MaoTus 的目标是成为一组可复用的 Vibe Coding skills 集合。
- 每个 skill 都应被当作一个小项目来管理，具备清晰目的、使用规则，以及必要的模板或辅助材料。
- 对外分享的 skill 以 `skills/<skill-name>/SKILL.md` 作为正式入口，不依赖个人或本地 Cursor 配置目录。
- ReMo 推荐通过 `.cursor/rules/remo.mdc` 安装到目标项目中，让 Agent 在日常任务过程中持续执行 ReMo 检查。
- ReMo 的核心目标是节省上下文：先读 `.remo/knowledge/index.md` 做上下文路由，再按任务读取少量知识文件，只有知识不足时才扫描代码库。
- ReMo 既是 MaoTus 的第一个 skill，也是这个仓库的第一个实践案例。
- ReMo 将 `.remo/logs/` 和 `.remo/knowledge/` 分开，避免回溯历史和未来上下文混在一起。
- 当前项目的记忆语言是简体中文，`.remo/logs/` 和 `.remo/knowledge/` 下的文件应默认使用中文。

## 实践指导

新增未来 skills 时，延续 ReMo 的方式：先把工作流定义清楚，第一版保持轻量，只有在手动流程被验证有价值之后再加入自动化。

处理 MaoTus 自身时，先读 `.remo/knowledge/index.md` 判断需要哪些上下文。重要里程碑写入 `.remo/logs/`，稳定项目理解写入 `.remo/knowledge/`。日志和知识默认使用简体中文。

新增、删除、重命名知识文件，或改变某个知识文件的用途时，必须同步更新 `.remo/knowledge/index.md`。

## 相关文件

- `skills/remo/SKILL.md`
- `skills/remo/README.md`
- `skills/remo/templates/remo-rule.mdc`
- `.cursor/rules/remo.mdc`
- `.remo/knowledge/index.md`
- `.remo/logs/2026-05-31-project-start.md`

## 未决问题

- 未来所有 skills 是否都统一放在 `skills/` 下。
- ReMo 后续是否需要加入脚本或 Cursor hooks 来实现自动化。

## 最后更新

2026-05-31
