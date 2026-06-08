# Linear 规划 skill 0.2.3–0.2.4 升级

## 任务

同步外部编辑后的 `linear-requirement-planner` skill 到仓库并提交 GitHub。

## 知识变更

### 更新

- `skills/linear-requirement-planner/SKILL.md`：
  - **0.2.3**：最终回复附带本地计划文档路径，可用 `open_resource` 打开。
  - **0.2.4**：新增 `## 澄清闸门`；阻塞型缺口必须 `AskQuestion`，不得用待确认或默认口径绕过；步骤 7 前自检清单。
- `.remo/knowledge/project-overview.md`：补充 AskQuestion 澄清闸门与本地路径回复说明。

### 新增知识

无新 knowledge 文件。

## 证据

- Skill 入口：`skills/linear-requirement-planner/SKILL.md`
- 外部编辑来源：`/Users/never/.cursor/skills/linear-requirement-planner/SKILL.md`（0.2.4）

## 检查

- `sh skills/remo/scripts/remo-check.sh`：通过
