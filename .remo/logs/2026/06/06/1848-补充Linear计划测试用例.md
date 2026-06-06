# 补充 Linear 计划测试用例

## 时间

2026-06-06 18:48 UTC+8

## 背景

用户确认 `linear-requirement-planner` 的目标不是只把 Linear issue 写成产品说明，而是根据 Linear 中的 brief 需求，结合当前项目实际情况，生成可执行实现计划；计划中必须包含完整测试用例。

## 结果

- 已将 `skills/linear-requirement-planner/SKILL.md` 升级到 `0.1.9`。
- 已明确角色为严格产品经理和实现计划设计者，要求结合当前项目代码、文档、架构和约定生成计划。
- 已新增 `## 测试用例设计` 模板，要求测试用例表格包含用例 ID、场景、前置条件、操作步骤、预期结果、类型和优先级。
- 已要求测试覆盖正向主流程、权限/角色、输入校验、边界值、空状态、错误状态、依赖失败、数据一致性、回归影响和相关非功能要求；不适用项必须说明原因。
- 已将 milestone 路径细节集中到 `## Milestone 文件夹规则`，减少 `SKILL.md` 中重复描述。
- 已新增 `## 执行阶段 ReMo 记忆` 模板说明：创建计划时不调用 ReMo；计划被执行并产生稳定项目变化后，如果当前项目或本机有 ReMo skill，执行者应默认调用 ReMo 更新项目记忆。
- 已更新 `.remo/knowledge/project-overview.md`，记录 Linear 需求规划器现在输出包含完整测试用例设计的实现计划。

## 证据

- Skill 入口：`skills/linear-requirement-planner/SKILL.md`
- 项目知识：`.remo/knowledge/project-overview.md`

## 后续

如果用户级 Cursor skill 或其他项目副本仍是旧版本，应按仓库 `0.1.9` 同步。
