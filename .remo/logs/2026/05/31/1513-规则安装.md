# 2026-05-31 规则安装

## 类型

决策

## 摘要

ReMo 应将项目 rules 作为推荐安装机制。共享的 skill 源码保留在 `skills/remo/`，目标项目通过安装 `.cursor/rules/remo.mdc` 让 ReMo 检查持续生效。

## 背景

ReMo 需要帮助项目在 Vibe Coding 过程中持续更新记忆。skill 文件定义工作流，但项目 rule 更适合在日常工作中提醒 Agent 执行 ReMo 检查，不需要用户每次主动提到 ReMo。

## 关键信息

- `skills/remo/SKILL.md` 仍然是正式共享 skill 源码。
- `skills/remo/templates/remo-rule.mdc` 提供可安装的 rule 模板。
- 当前仓库使用 `.cursor/rules/remo.mdc` 作为第一个 ReMo rule 实践。
- 该 rule 使用 `alwaysApply: true`，用于在有意义的工作结束前执行 ReMo 检查。

## 决策或结果

采用项目 rules 作为让 ReMo 在用户项目中持续生效的推荐方式。

## 后续行动

- [ ] 如果 ReMo 超出初始模板范围，再增加独立安装指南。
- [ ] 只有在 rule 工作流被验证有价值之后，再考虑 hooks。

## 来源

- `skills/remo/SKILL.md`
- `skills/remo/README.md`
- `skills/remo/templates/remo-rule.mdc`
- `.cursor/rules/remo.mdc`
