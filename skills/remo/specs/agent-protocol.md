# ReMo Agent Protocol

## 任务开始

Agent 必须：

1. 读取 `.remo/knowledge/index.md`。
2. 根据任务描述选择最小 knowledge 集合。
3. 读取相关 map/topic。
4. 只有当 knowledge 缺失、过期、冲突或不够具体时才扫描 repo。
5. 记录发现的知识缺口，供任务结束时自动吸收。

## 任务过程

Agent 在探索和实现过程中收集：

- 新的稳定项目事实。
- 被证伪或过期的旧知识。
- 用户明确决策。
- 重复出现的问题或排查路径。
- 未来 Agent 不应重新发现的上下文。

不要保存临时尝试、完整命令输出、逐文件摘要或没有证据的猜测。

## 任务结束

Agent 生成 memory delta，并由 ReMo 自动合并到正式 knowledge：

```yaml
task: short summary
new_knowledge:
  - title: string
    scope: [repo]
    confidence: high
    evidence:
      - type: file
        ref: path
    summary: string
updated_knowledge:
  - id: existing-id
    change: string
stale_knowledge:
  - id: existing-id
    reason: string
```

ReMo 合并后必须更新索引和日志。日志文件名必须为 `.remo/logs/YYYY/MM/DD/HHMM-简体中文标题.md`（`HHMM` 为 24 小时制本地时间，同日多条须唯一）；模板见 `skills/remo/templates/log-entry.md`。

## Commit Checkpoint

Commit 前：

1. 检查 staged diff。
2. 判断是否改变长期项目理解。
3. 自动更新相关 knowledge。
4. 写入 checkpoint 日志。
5. 如果没有长期知识变化，在日志写明原因。
6. 将本次 `.remo/` 下新增或修改的文件与代码变更一并纳入 Git stage（整个 `.remo/` 目录默认受版本库跟踪）。

Push 后：

1. 补充 commit hash、branch、remote 和 push 结果。
2. 如果 push 改变发布状态或项目事实，更新相关 knowledge。

## 冲突优先级

1. 用户明确决策。
2. 当前代码和文档。
3. Git 历史和 commit message。
4. Agent 观察和推断。

较低优先级不得覆盖较高优先级，只能标记为待复核。
