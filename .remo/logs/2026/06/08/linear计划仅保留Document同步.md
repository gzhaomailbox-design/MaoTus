# Linear 计划同步改为仅 Document（0.2.2）

## 任务

用户指出 0.2.1 会同时上传计划 `.md` 附件并创建 Linear Document，内容重复；要求只保留 Document 同步。

## 知识变更

### 更新

- `skills/linear-requirement-planner/SKILL.md`：升级到 `0.2.2`；移除步骤 8b 附件上传，Document 同步改为 8b。
- `.remo/knowledge/project-overview.md`：去掉附件同步说明，明确仅 Document + 评论。

### 新增知识

无新 knowledge 文件。

## 证据

- Skill 入口：`skills/linear-requirement-planner/SKILL.md`
- 用户级 skill 已同步：`/Users/never/.cursor/skills/linear-requirement-planner/SKILL.md`

## 检查

- `sh skills/remo/scripts/remo-check.sh`：通过
