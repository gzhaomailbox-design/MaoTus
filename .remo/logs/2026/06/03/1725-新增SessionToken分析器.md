# 新增 Session Token 分析器

## 时间

2026-06-03 17:25 UTC+8

## 背景

用户希望新增一个 skill，用于查看某个 Cursor session 的 token 消耗组成；经确认，第一版目标是基于本地 session transcript 做可解释估算，并配套解析脚本，而不是接入真实计费 usage。

## 结果

- 已新增 `skills/session-token-auditor/SKILL.md`，定义触发条件、输入方式、估算口径、输出格式和限制。
- 已新增 `skills/session-token-auditor/scripts/analyze_session_tokens.py`，使用 Python 标准库解析 Cursor agent transcript JSONL，并按用户输入、附加上下文、Assistant 文本、工具调用和工具结果估算 token 组成。
- 已将 `session-token-auditor` 更新到 `0.1.1`，要求报告使用结构化 Markdown 表格和树状拆解图，脚本同步输出概览表、类别表、角色表、Top 条目表和树状拆解。
- 已更新 `.remo/knowledge/project-overview.md`，记录 `session-token-auditor` 作为仓库内正式 skill 的入口和能力边界。

## 验证

已使用本地样例 transcript 运行：

```bash
python3 skills/session-token-auditor/scripts/analyze_session_tokens.py /Users/never/.cursor/projects/Users-never-Documents-Coding-Code-MaoTus/agent-transcripts/f35471ba-81ed-404e-aaa6-b85422c70ce6/f35471ba-81ed-404e-aaa6-b85422c70ce6.jsonl --top 8
```

脚本成功输出总估算 token、类别占比、角色占比、Top 条目、优化线索；`0.1.1` 验证中已确认报告包含结构化表格和树状拆解图。

## 证据

- Skill 入口：`skills/session-token-auditor/SKILL.md`
- 解析脚本：`skills/session-token-auditor/scripts/analyze_session_tokens.py`
- 项目知识：`.remo/knowledge/project-overview.md`

## 后续

当前版本不读取真实模型 usage 或账单数据；若未来需要精确计费归因，应先找到包含真实 token usage 的数据源，再扩展本 skill。
