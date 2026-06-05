# 修正 Linear 计划目录层级

## 时间

2026-06-05 10:25 UTC+8

## 背景

用户指出 `linear-requirement-planner` 的 milestone 路径层级仍然不对：milestone 文件夹不应创建在 `docs/01_designing` 下面，而应该作为 `docs` 下的上层文件夹；design 文档应位于 milestone 文件夹内部。

## 结果

- 已将 `skills/linear-requirement-planner/SKILL.md` 升级到 `0.1.4`。
- 有 milestone 的计划路径改为 `docs/<YYYY-MM-DD>-<milestone-name>/01_designing/<issue-id>-<中文短标题>.md`。
- 无 milestone 的计划路径改为 `docs/未关联Milestone/01_designing/<issue-id>-<中文短标题>.md`。
- 已明确不要把 milestone 文件夹放在 `docs/01_designing/` 下。
- 已更新 `.remo/knowledge/project-overview.md` 中的 Linear 需求规划器路径说明。

## 证据

- Skill 入口：`skills/linear-requirement-planner/SKILL.md`
- 项目知识：`.remo/knowledge/project-overview.md`

## 后续

已同步用户级 Cursor skill `/Users/never/.cursor/skills/linear-requirement-planner/SKILL.md`，并确认本机已安装版本为 `0.1.4`。随后用户澄清最终路径格式后，已再次同步到 `0.1.5`。

## 更正

2026-06-05 10:28 UTC+8，用户明确最终格式应为 `docs/01_designing/<YYYY-MM-DD-milestone-name>/<issue>.md`。

- `0.1.4` 中把 milestone 文件夹移动到 `docs/` 下的理解不符合用户意图。
- 已升级到 `0.1.5`，恢复 milestone 文件夹位于 `docs/01_designing/` 下。
- 有 milestone 的计划路径为 `docs/01_designing/<YYYY-MM-DD>-<milestone-name>/<issue-id>-<中文短标题>.md`。
- 无 milestone 的计划路径为 `docs/01_designing/未关联Milestone/<issue-id>-<中文短标题>.md`。

## 二次更正

2026-06-05 10:39 UTC+8，用户明确还需要固定 `milestone/` 中间层。

- 已升级到 `0.1.6`。
- 最新执行规则为 `docs/01_designing/milestone/<YYYY-MM-DD>-<milestone-name>/<issue-id>-<中文短标题>.md`。
- 无 milestone 的路径为 `docs/01_designing/milestone/未关联Milestone/<issue-id>-<中文短标题>.md`。
- `0.1.4` 和 `0.1.5` 的路径口径均为历史中间口径，不再作为执行规则。
