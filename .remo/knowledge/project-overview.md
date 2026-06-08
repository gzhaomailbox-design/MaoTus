---
id: project-overview
title: MaoTus Project Overview
type: map
status: active
scope:
  - repo
confidence: high
last_verified: 2026-06-08
source_paths:
  - AGENTS.md
  - README.md
  - skills/remo/SKILL.md
  - skills/linear-requirement-planner/SKILL.md
  - .remo/config.yml
evidence:
  - type: file
    ref: README.md
  - type: file
    ref: skills/remo/SKILL.md
  - type: user_decision
    ref: 用户要求 ReMo 成为自动项目记忆系统
supersedes: []
related: []
---

# MaoTus Project Overview

## Summary

MaoTus 是一个用于管理 Vibe Coding 实践中沉淀出来的 skills 的仓库。当前重点是将 ReMo 从手动记忆协议升级为面向 Coding Agent 的自动项目记忆系统。

## When To Read

- 处理 MaoTus 项目定位、skill 结构或维护约定时读取。
- 设计、实现或调整 ReMo 自动记忆系统时读取。
- 准备 commit/push checkpoint 或判断是否需要更新 `.remo/knowledge/` 时读取。

## Current Knowledge

- MaoTus 的目标是成为一组可复用的 Vibe Coding skills 集合。
- 每个 skill 应有明确目的、触发条件、工作流、质量标准，以及必要模板、脚本或规格文档。
- 对外分享的 skill 以 `skills/<skill-name>/SKILL.md` 作为正式入口，不依赖个人或本地 Cursor 配置目录。
- README、skills、模板、ReMo 日志和知识文件默认使用简体中文；路径、命令、API 名、产品名和技术术语保留原文。
- `linear-requirement-planner` 位于 `skills/linear-requirement-planner/SKILL.md`，用于把 Linear brief 需求结合项目实际情况转成中文实现计划；计划完成后会把摘要和预期 GitHub 链接评论回 Linear，并用 `save_document` 把全文同步到关联 Linear Document 以便在线预览（不上传重复附件）。
- ReMo 位于 `skills/remo/SKILL.md`，当前方向是自动项目记忆系统：任务边界和 Git checkpoint 自动更新正式 Markdown knowledge。
- ReMo 安装后必须暴露到 Agent 常规入口：通用 `AGENTS.md` 和 Cursor `.cursor/rules/remo.mdc`。
- ReMo 使用 Markdown + YAML frontmatter 作为正式知识载体，并用 `.remo/knowledge/index.md` 做任务路由。
- ReMo 允许自动写入正式 knowledge，但必须保留 evidence、confidence、scope、source_paths、last_verified 和失效信号。
- ReMo 的优化目标是降低未来 Coding Agent 的上下文加载量、重复探索量和返工成本，而不是降低生成记忆本身的 token。
- 当前项目已配置 `.remo/config.yml`，启用 task_start route、task_end absorb、pre_commit checkpoint、post_push checkpoint，不启用默认 file watcher。

## Agent Guidance

- 处理 MaoTus 时先读 `.remo/knowledge/index.md`，再按 Route Map 读取最小 knowledge 集合。
- 修改 ReMo 自动记忆设计时，同时检查 `skills/remo/SKILL.md`、`skills/remo/specs/`、`AGENTS.md` 和 `.cursor/rules/remo.mdc`，避免 README、模板和规则副本互相冲突。
- 新增或重命名 knowledge 文件时，必须更新 `.remo/knowledge/index.md`。
- 自动写入 knowledge 后，运行 `sh skills/remo/scripts/remo-check.sh` 检查 frontmatter、路由和 source path。
- Commit/push 前后应留下 `.remo/logs/YYYY/MM/DD/` 记录，说明本次是否改变长期项目知识。

## Evidence

- `AGENTS.md`：通用 Coding Agent 入口，提醒 Codex 等 Agent 使用 ReMo。
- `README.md`：项目定位、skills 清单和维护约定。
- `skills/remo/SKILL.md`：ReMo 自动项目记忆系统的权威定义。
- `skills/remo/specs/`：自动系统的架构、metadata、Agent 协议和命令接口。
- `skills/linear-requirement-planner/SKILL.md`：Linear 需求规划器的权威入口。
- `.remo/config.yml`：当前项目的 ReMo 自动化配置。

## Invalidation Signals

- ReMo 不再以自动写入正式 knowledge 为目标。
- 知识载体从 Markdown + frontmatter 改成数据库或双轨存储。
- Agent 入口不再使用 `AGENTS.md` 或 Cursor rule。
- MaoTus 不再以 `skills/<skill-name>/SKILL.md` 作为 skill 权威入口。
- `.remo/config.yml` 的触发策略或 source 策略发生重大变化。
