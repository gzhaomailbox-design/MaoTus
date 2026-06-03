---
name: session-token-auditor
description: Estimate and explain token usage composition for Cursor sessions by analyzing local agent transcript JSONL files. Use when the user asks to inspect session token consumption, token breakdown, transcript cost composition, or why a Cursor session used many tokens.
---

# Session Token 分析器

## 版本

- 当前版本：0.1.1
- 更新日期：2026-06-03
- 版本状态：表格与树状拆解输出版本

使用本 skill 前先检查本节版本号与“更新记录”。如果用户需要真实计费 usage，而不是 transcript 估算，必须先说明当前版本无法从本地 transcript 还原真实模型计费 token。

## 更新记录

### 0.1.1 - 2026-06-03

- 将报告输出规范调整为结构化 Markdown 表格。
- 要求输出树状拆解图，展示总量到类别和典型大条目的分解关系。
- 同步更新脚本报告渲染，默认输出概览表、类别表、角色表、Top 条目表和树状拆解。

### 0.1.0 - 2026-06-03

- 建立 Cursor session transcript 的 token 消耗组成估算工作流。
- 新增标准库 Python 脚本 `scripts/analyze_session_tokens.py`，读取 JSONL transcript 并输出 Markdown breakdown。
- 明确当前输出是可解释估算，不是账单、模型 API usage 或精确 tokenizer 结果。

## 触发条件

当用户要求分析某个 Cursor 会话、session、agent transcript、token 消耗组成、上下文成本、用量 breakdown，或询问“为什么这个会话 token 用得多”时，使用本 skill。

## 输入

优先要求用户提供以下任一种输入：

- Cursor agent transcript JSONL 文件路径。
- 包含 transcript JSONL 的目录路径。
- 会话 ID；若用户只给 ID，先在当前项目的 agent transcript 目录中查找同名 JSONL。

如果找不到 transcript，先报告缺失信息并询问用户提供路径；不要伪造分析。

## 工作流

1. 定位 transcript。
   - 如果用户给出文件路径，直接读取该 JSONL。
   - 如果用户给出目录，查找目录下的 `.jsonl` 文件；多个候选时让用户选择。
   - 如果用户给出会话 ID，优先匹配 `<session-id>.jsonl`。

2. 运行估算脚本。

   ```bash
   python3 skills/session-token-auditor/scripts/analyze_session_tokens.py /path/to/session.jsonl
   ```

   常用选项：

   ```bash
   python3 skills/session-token-auditor/scripts/analyze_session_tokens.py /path/to/session.jsonl --top 15
   ```

3. 解读报告。
   - 先说明总估算 token 和最大消耗类别。
   - 使用报告中的表格说明类别、角色和最大条目，而不是只用散列项目符号。
   - 使用树状拆解图说明总量如何分解到类别和典型大条目。
   - 再指出 top entries 中最值得优化的来源，例如大段工具结果、重复上下文、长用户输入、过多文件内容或冗长 assistant 输出。
   - 如果 transcript 缺少真实 `usage` 字段，明确输出是估算。

4. 给出优化建议。
   - 优先建议减少高占比来源，而不是泛泛要求“少用 token”。
   - 对工具结果过大的场景，建议缩小搜索范围、分页读取、过滤输出或避免重复读取。
   - 对用户输入或附加上下文过大的场景，建议拆分任务、减少粘贴原文或改用文件路径引用。

## 输出格式

最终回复应包含：

````markdown
## 结论

[一句话说明总估算 token、最大来源和置信度]

## 组成

| 类别 | 估算 token | 占比 | 字符数 | 条目数 |
| --- | ---: | ---: | ---: | ---: |
| [类别 1] | [token] | [占比] | [字符数] | [条目数] |

## 树状拆解

```text
Session total
├── [类别 1] [token, 占比]
│   └── [最大条目摘要]
└── [类别 2] [token, 占比]
    └── [最大条目摘要]
```

## 最大条目

| 排名 | 行号 | 角色 | 类别 | 类型 | 估算 token | 摘要 |
| ---: | ---: | --- | --- | --- | ---: | --- |
| 1 | [line] | [role] | [category] | [kind] | [token] | [summary] |

## 优化建议

- [针对最大来源的具体建议]
````

## 估算口径

当前脚本使用启发式估算：

- ASCII 文本约按 `字符数 / 4` 估算。
- CJK 字符按接近 `字符数` 估算。
- 工具调用参数和工具结果会先序列化为紧凑 JSON，再估算 token。
- `system_reminder`、`user_info`、`git_status`、`rules`、`attached_files` 等嵌入在用户消息中的上下文，会从 `user` 文本中拆分到 `attached_context`。

## 限制

- 本 skill 不读取 Cursor 或模型服务的真实计费数据。
- 本 skill 不承诺与模型 tokenizer 完全一致；它用于发现 token 消耗结构和优化方向。
- 如果 transcript 已经过截断、压缩或缺少工具结果，报告只能反映文件中保留的内容。
- 不要把估算结果用于报销、计费争议或精确成本归因。
