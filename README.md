# MaoTus

MaoTus 是一个用于管理 Vibe Coding 实践中沉淀出来的 skills 的仓库。

这个项目收集可复用的工作流、提示词、模板和项目知识，让后续 AI 辅助开发会话能更快进入状态，并使用更准确的上下文。

## 第一个 Skill：ReMo

第一个 skill 是 ReMo，也就是 Repo Memory。

ReMo 帮助 Vibe Coding 项目持续保存两类记忆：

- 过程日志：记录里程碑、决策、方向调整和迭代历史。
- 项目知识：沉淀架构、业务流程、产品模型、术语、约束和常见问题。

Skill 源文件和模板见 [skills/remo](skills/remo)。

## Repo Memory

本仓库本身也使用 ReMo：

- `.remo/logs/` 记录重要项目进展。
- `.remo/knowledge/` 保存供未来任务复用的高信号项目知识。
