#!/usr/bin/env python3
"""Estimate token composition for Cursor agent transcript JSONL files."""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


CATEGORY_LABELS = {
    "user_input": "用户输入",
    "attached_context": "附加上下文",
    "assistant_text": "Assistant 文本",
    "tool_use": "工具调用",
    "tool_result": "工具结果",
    "other": "其他内容",
}

CONTEXT_TAGS = (
    "timestamp",
    "user_info",
    "git_status",
    "rules",
    "agent_skills",
    "agent_transcripts",
    "system_reminder",
    "attached_files",
    "plugin_info",
    "linter_errors",
    "terminal_files_information",
)


@dataclass
class Entry:
    line: int
    role: str
    category: str
    kind: str
    chars: int
    tokens: int
    summary: str


def is_cjk(char: str) -> bool:
    codepoint = ord(char)
    return (
        0x3400 <= codepoint <= 0x4DBF
        or 0x4E00 <= codepoint <= 0x9FFF
        or 0xF900 <= codepoint <= 0xFAFF
        or 0x3040 <= codepoint <= 0x30FF
        or 0xAC00 <= codepoint <= 0xD7AF
    )


def estimate_tokens(text: str) -> int:
    """Approximate mixed-language tokens without external tokenizer packages."""
    score = 0.0
    for char in text:
        if char.isspace():
            score += 0.10
        elif is_cjk(char):
            score += 1.00
        elif ord(char) < 128:
            score += 0.25
        else:
            score += 0.50
    return max(1, math.ceil(score)) if text else 0


def compact_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def summarize(text: str, limit: int = 140) -> str:
    normalized = re.sub(r"\s+", " ", text).strip()
    if len(normalized) <= limit:
        return normalized
    return normalized[: limit - 1].rstrip() + "..."


def make_entry(line: int, role: str, category: str, kind: str, text: str) -> Entry:
    return Entry(
        line=line,
        role=role or "unknown",
        category=category,
        kind=kind,
        chars=len(text),
        tokens=estimate_tokens(text),
        summary=summarize(text),
    )


def strip_user_query(text: str) -> tuple[list[str], str]:
    queries = re.findall(r"<user_query>\s*(.*?)\s*</user_query>", text, flags=re.DOTALL)
    remainder = re.sub(r"<user_query>\s*.*?\s*</user_query>", "", text, flags=re.DOTALL)
    return queries, remainder


def split_known_context(text: str) -> tuple[str, str]:
    context_parts: list[str] = []
    remaining = text
    for tag in CONTEXT_TAGS:
        pattern = rf"<{tag}(?:\s[^>]*)?>.*?</{tag}>"
        matches = re.findall(pattern, remaining, flags=re.DOTALL)
        context_parts.extend(matches)
        remaining = re.sub(pattern, "", remaining, flags=re.DOTALL)
    return "\n".join(context_parts), remaining.strip()


def classify_text(line: int, role: str, text: str, kind: str) -> Iterable[Entry]:
    if not text:
        return []

    if role == "user":
        query_parts, remainder = strip_user_query(text)
        context_text, remaining_user_text = split_known_context(remainder)

        entries: list[Entry] = []
        for query in query_parts:
            if query.strip():
                entries.append(make_entry(line, role, "user_input", kind, query.strip()))
        if remaining_user_text:
            entries.append(make_entry(line, role, "user_input", kind, remaining_user_text))
        if context_text.strip():
            entries.append(make_entry(line, role, "attached_context", kind, context_text))
        return entries

    if role == "assistant":
        return [make_entry(line, role, "assistant_text", kind, text)]

    return [make_entry(line, role, "other", kind, text)]


def classify_content_block(line: int, role: str, block: Any) -> Iterable[Entry]:
    if isinstance(block, str):
        return classify_text(line, role, block, "text")

    if not isinstance(block, dict):
        return [make_entry(line, role, "other", type(block).__name__, repr(block))]

    block_type = str(block.get("type") or "unknown")

    if block_type == "text":
        return classify_text(line, role, str(block.get("text") or ""), "text")

    if block_type == "tool_use":
        tool_name = str(block.get("name") or "unknown_tool")
        payload = {"name": tool_name, "input": block.get("input")}
        return [make_entry(line, role, "tool_use", tool_name, compact_json(payload))]

    if block_type == "tool_result":
        tool_name = str(block.get("tool_use_id") or block.get("name") or "tool_result")
        return [make_entry(line, role, "tool_result", tool_name, compact_json(block))]

    return [make_entry(line, role, "other", block_type, compact_json(block))]


def parse_transcript(path: Path) -> list[Entry]:
    entries: list[Entry] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            if not raw_line.strip():
                continue
            try:
                row = json.loads(raw_line)
            except json.JSONDecodeError as exc:
                entries.append(
                    make_entry(line_number, "unknown", "other", "invalid_json", f"{exc}: {raw_line}")
                )
                continue

            role = str(row.get("role") or row.get("message", {}).get("role") or "unknown")
            message = row.get("message") if isinstance(row.get("message"), dict) else row
            content = message.get("content") if isinstance(message, dict) else None

            if isinstance(content, list):
                for block in content:
                    entries.extend(classify_content_block(line_number, role, block))
            elif isinstance(content, str):
                entries.extend(classify_text(line_number, role, content, "text"))
            else:
                entries.append(make_entry(line_number, role, "other", "message", compact_json(row)))
    return entries


def percent(part: int, total: int) -> str:
    if total == 0:
        return "0.0%"
    return f"{part / total * 100:.1f}%"


def md_cell(value: object) -> str:
    text = str(value)
    return text.replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ")


def tree_label(entry: Entry) -> str:
    label = CATEGORY_LABELS.get(entry.category, entry.category)
    return f"L{entry.line} {entry.role}/{label}/{entry.kind}: {entry.tokens} token - {entry.summary}"


def render_report(path: Path, entries: list[Entry], top_n: int) -> str:
    total_tokens = sum(entry.tokens for entry in entries)
    total_chars = sum(entry.chars for entry in entries)
    by_category: dict[str, dict[str, int]] = defaultdict(lambda: {"tokens": 0, "chars": 0, "count": 0})
    by_role: dict[str, int] = defaultdict(int)
    entries_by_category: dict[str, list[Entry]] = defaultdict(list)

    for entry in entries:
        by_category[entry.category]["tokens"] += entry.tokens
        by_category[entry.category]["chars"] += entry.chars
        by_category[entry.category]["count"] += 1
        by_role[entry.role] += entry.tokens
        entries_by_category[entry.category].append(entry)

    sorted_categories = sorted(
        by_category.items(),
        key=lambda item: item[1]["tokens"],
        reverse=True,
    )
    top_entries = sorted(entries, key=lambda entry: entry.tokens, reverse=True)[:top_n]

    lines = [
        "# Session Token 估算报告",
        "",
        "## 概览",
        "",
        "| 指标 | 值 |",
        "| --- | ---: |",
        f"| Transcript | `{md_cell(path)}` |",
        f"| 消息条目数 | {len(entries)} |",
        f"| 总字符数 | {total_chars} |",
        f"| 总估算 token | {total_tokens} |",
        "| 估算口径 | ASCII 约 4 字符/token，CJK 约 1 字符/token，空白字符低权重；非真实计费 usage |",
        "",
        "## 按类别组成",
        "",
        "| 类别 | 估算 token | 占比 | 字符数 | 条目数 |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]

    for category, stats in sorted_categories:
        label = CATEGORY_LABELS.get(category, category)
        lines.append(
            f"| {md_cell(label)} | {stats['tokens']} | {percent(stats['tokens'], total_tokens)} | "
            f"{stats['chars']} | {stats['count']} |"
        )

    lines.extend(["", "## 树状拆解", "", "```text"])
    lines.append(f"Session total: {total_tokens} token, {total_chars} chars")
    for category_index, (category, stats) in enumerate(sorted_categories):
        label = CATEGORY_LABELS.get(category, category)
        is_last_category = category_index == len(sorted_categories) - 1
        category_branch = "└──" if is_last_category else "├──"
        child_prefix = "    " if is_last_category else "│   "
        lines.append(
            f"{category_branch} {label}: {stats['tokens']} token "
            f"({percent(stats['tokens'], total_tokens)}), {stats['count']} entries"
        )

        category_top_entries = sorted(
            entries_by_category[category],
            key=lambda entry: entry.tokens,
            reverse=True,
        )[:3]
        for entry_index, entry in enumerate(category_top_entries):
            entry_branch = "└──" if entry_index == len(category_top_entries) - 1 else "├──"
            lines.append(f"{child_prefix}{entry_branch} {tree_label(entry)}")
    lines.extend(["```", "", "## 按角色组成", "", "| 角色 | 估算 token | 占比 |", "| --- | ---: | ---: |"])
    for role, tokens in sorted(by_role.items(), key=lambda item: item[1], reverse=True):
        lines.append(f"| {md_cell(role)} | {tokens} | {percent(tokens, total_tokens)} |")

    lines.extend(
        [
            "",
            f"## Top {top_n} 最大条目",
            "",
            "| 排名 | 行号 | 角色 | 类别 | 类型 | 估算 token | 字符数 | 摘要 |",
            "| ---: | ---: | --- | --- | --- | ---: | ---: | --- |",
        ]
    )
    for rank, entry in enumerate(top_entries, start=1):
        label = CATEGORY_LABELS.get(entry.category, entry.category)
        lines.append(
            f"| {rank} | {entry.line} | {md_cell(entry.role)} | {md_cell(label)} | "
            f"{md_cell(entry.kind)} | {entry.tokens} | {entry.chars} | {md_cell(entry.summary)} |"
        )

    lines.extend(["", "## 优化线索", ""])
    if sorted_categories:
        leading_category, leading_stats = sorted_categories[0]
        leading_label = CATEGORY_LABELS.get(leading_category, leading_category)
        lines.append(
            f"- 最大来源是{leading_label}，占 {percent(leading_stats['tokens'], total_tokens)}；"
            "优先检查该类别中的 Top 条目。"
        )
    if any(entry.category == "tool_use" for entry in top_entries):
        lines.append("- Top 条目包含工具调用参数；检查是否传入了过长计划、查询、补丁或重复上下文。")
    if any(entry.category == "tool_result" for entry in top_entries):
        lines.append("- Top 条目包含工具结果；考虑缩小搜索范围、分页读取、过滤输出或避免重复读取大文件。")
    if any(entry.category == "attached_context" for entry in top_entries):
        lines.append("- Top 条目包含附加上下文；考虑拆分任务、减少一次性附带的规则/文件/状态信息。")
    if any(entry.category == "user_input" for entry in top_entries):
        lines.append("- Top 条目包含用户输入；若是长文本，可改为引用文件路径或分阶段分析。")
    if not top_entries:
        lines.append("- 未发现可分析条目；请确认 transcript JSONL 包含消息内容。")

    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Estimate token composition for a Cursor agent transcript JSONL file.",
    )
    parser.add_argument("transcript", type=Path, help="Path to a transcript .jsonl file")
    parser.add_argument("--top", type=int, default=10, help="Number of largest entries to show")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.top < 1:
        parser.error("--top must be at least 1")

    transcript = args.transcript.expanduser()
    if not transcript.exists():
        print(f"Transcript not found: {transcript}", file=sys.stderr)
        return 1
    if not transcript.is_file():
        print(f"Transcript is not a file: {transcript}", file=sys.stderr)
        return 1

    entries = parse_transcript(transcript)
    print(render_report(transcript, entries, args.top))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
