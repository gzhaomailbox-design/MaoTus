# 2026-05-31 16:25 GitHub 历史回溯

## 类型

决策

## 摘要

ReMo 初始化能力增加 GitHub/Git commit 历史回溯：当项目已经关联远程仓库时，可以根据 commit 历史生成更准确的历史日志和基线知识库。

## 背景

ReMo 可能被后期引入已有项目。此时项目的关键演进过程已经存在于 commit 历史里。如果只看当前文件结构，初始化出来的知识库可能缺少历史决策、架构演进和重要里程碑。

## 关键信息

- 初始化时如果发现 GitHub 或其他 Git remote，应检查默认分支和 commit 历史。
- commit 不应逐条转换为日志，而应聚合成阶段、里程碑、转向、发布、bug 修复簇或架构变化。
- 回溯日志使用 commit 时间生成 `.remo/logs/YYYY/MM/DD/HHMM-记忆语言标题.md`。
- commit message、变更文件路径、tag、merge commit 都可以作为证据。
- 从历史中提炼出的稳定事实应写入基线知识文件。
- 低置信度结论应标记为 `Needs review` 或写入开放问题。

## 决策或结果

ReMo 初始化流程新增 GitHub/Git 历史回溯能力，用于提高后期接入已有项目时的日志完整度和知识库准确度。

## 后续行动

- [ ] 未来可考虑提供辅助脚本，把 commit 历史聚合为候选日志草稿。
- [ ] 在 Sizz 等已有项目中实践该能力，验证回溯粒度是否合适。

## 来源

- `skills/remo/SKILL.md`
- `skills/remo/README.md`
- `skills/remo/templates/remo-rule.mdc`
- `.cursor/rules/remo.mdc`
- `.remo/knowledge/index.md`
- `.remo/knowledge/project-overview.md`
