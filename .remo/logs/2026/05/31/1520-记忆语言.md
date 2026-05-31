# 2026-05-31 15:20 记忆语言

## 类型

决策

## 摘要

ReMo 的语言偏好从“知识库语言”扩展为“记忆语言”。日志和知识都应根据用户选择的语言记录。

## 背景

日志虽然不默认作为未来上下文，但它仍然是 Repo Memory 的一部分，用于回溯项目迭代过程。为了保持项目记忆一致，日志也应该遵循用户偏好的语言。

## 关键信息

- ReMo 首次应用到项目时，应询问用户 Repo Memory 使用什么语言。
- `.remo/logs/` 和 `.remo/knowledge/` 都应使用记录下来的记忆语言。
- MaoTus 当前记忆语言是简体中文。
- 已有日志内容已改为中文。

## 决策或结果

将 ReMo 的语言规则统一为“记忆语言”，同时约束日志和知识。

## 后续行动

- [ ] 后续新增日志和知识时默认使用简体中文。
- [ ] 如果用户修改语言偏好，同步更新项目概览和知识索引。

## 来源

- `skills/remo/SKILL.md`
- `.cursor/rules/remo.mdc`
- `skills/remo/templates/remo-rule.mdc`
- `.remo/knowledge/project-overview.md`
- `.remo/knowledge/index.md`
