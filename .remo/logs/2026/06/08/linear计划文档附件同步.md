# Linear 计划同步升级（0.2.0 → 0.2.1）

## 任务

升级 `linear-requirement-planner` skill：计划完成后除评论摘要和预期 GitHub 链接外，还要把最新计划文档作为 issue 附件上传，并用 `save_document` 把全文同步到关联 Linear Document 以便在线预览。

## 知识变更

### 更新

- `skills/linear-requirement-planner/SKILL.md`：升级到 `0.2.1`；新增步骤 8b（附件）、8c（Document 全文）和 `## Linear 计划同步规则`。
- `.remo/knowledge/project-overview.md`：补充 linear skill 的评论、附件、Document 三路同步说明；`last_verified` 更新为 `2026-06-08`。

### 新增知识

无新 knowledge 文件；行为变更写入既有 skill 与 project overview。

## 证据

- Skill 入口：`skills/linear-requirement-planner/SKILL.md`
- Linear MCP：`save_comment`、`prepare_attachment_upload`、`create_attachment_from_upload`、`save_document`
- 用户级 skill 已同步：`/Users/never/.cursor/skills/linear-requirement-planner/SKILL.md`

## 检查

- `sh skills/remo/scripts/remo-check.sh`：通过
