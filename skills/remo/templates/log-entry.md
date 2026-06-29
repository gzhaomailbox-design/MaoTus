# YYYY-MM-DD HH:MM 记忆语言标题

获取日志路径（**禁止**手写 `HHMM-` 或自行推断时区；Cursor 云端 Agent 必须用 shell 取仓库机器本地 `date`）：

```sh
sh skills/remo/scripts/remo-log-path.sh "记忆语言标题"
```

stdout 示例：`.remo/logs/YYYY/MM/DD/HHMM-记忆语言标题.md`

## Type

auto_absorb | git_checkpoint | milestone | decision | pivot | release | incident | retrospective

## Summary

用短段落说明 ReMo 这次记录或自动写入了什么。

## Trigger

- Task boundary
- Commit checkpoint
- Push checkpoint
- Manual command
- User decision

## Knowledge Changes

- Created:
- Updated:
- Marked stale:
- No durable change:

## Evidence

- 相关文件、commit、diff、用户决策、Agent observation 或外部引用。

## Commit And Push

- Commit：hash 或 `尚未提交`
- Branch：分支名
- Remote：相关时记录 remote 名称和 URL
- Push 结果：已推送、尚未推送、失败或不适用

## Follow-up

- [ ] 后续动作或待确认问题。
