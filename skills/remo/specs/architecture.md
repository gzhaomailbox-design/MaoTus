# ReMo Architecture

## 目标

ReMo 自动维护 Coding Agent 可用的 repo memory。它的优化目标是降低未来任务的上下文加载量、重复探索量和返工成本，而不是降低记忆生成过程本身的 token。

## 数据流

```text
Repo / Docs / Git / Agent task / User decisions
  -> evidence set
  -> memory delta
  -> merge policy
  -> Markdown knowledge
  -> route result for future agents
```

## 信息源

- Repo 文件和文档：README、设计文档、配置、源码、测试、脚本。
- Git：commit history、staged diff、push result、branch、remote。
- Agent 任务过程：任务目标、探索结果、实现结果、测试结果、稳定知识缺口。
- 用户决策：明确的产品、技术、命名、流程和范围决定。

第一阶段不做默认外部集成。Linear、GitHub PR review、CI log 和聊天系统可以作为后续 source adapter。

## 存储层

- `.remo/config.yml` 保存项目级记忆配置。
- `.remo/knowledge/index.md` 是路由入口。
- `.remo/knowledge/maps/` 保存顶层地图。
- `.remo/knowledge/topics/` 保存细分主题。
- `.remo/logs/` 保存自动运行、checkpoint、里程碑和写入摘要。

正式知识使用 Markdown + YAML frontmatter。Markdown 保持人类可读，frontmatter 支持机器检查、路由和过期检测。

## 自动写入管线

1. 收集 evidence set。
2. 生成 structured memory delta。
3. 匹配已有 knowledge id、scope 和 related。
4. 应用证据优先级：用户决策 > 当前代码事实 > Git 历史推断 > Agent 推断。
5. 合并正文和 metadata。
6. 更新索引路由。
7. 写入日志。
8. 保留 Git diff 供审计和回滚。

## 触发时机

- 任务开始：只路由和读取，不写入。
- 任务结束：根据 memory delta 自动写入。
- Commit 前：根据 staged diff 自动更新 knowledge 和 checkpoint 日志。
- Push 后：补充 checkpoint 日志中的 commit、branch、remote 和 push 结果。
- 手动命令：允许显式 scan、absorb、checkpoint、check。

默认不启用文件 watcher，因为每次文件变化都生成记忆会增加噪声并降低知识质量。

## 失效与回滚

- source path 删除或证据不再成立时，知识标记为 `needs_review` 或 `stale`。
- 新知识替代旧知识时，旧文件 metadata 的 `status` 改为 `deprecated`，并设置 `supersedes` / `related`。
- 自动写入不自动 commit。所有回滚使用 Git。
