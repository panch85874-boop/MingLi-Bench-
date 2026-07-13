"""Turn a raw transcript into a structured summary: key points, decisions,
and action items with owner/due-date extraction where the transcript states
them explicitly."""

import json
import re
from dataclasses import dataclass, field
from typing import List

from .llm_client import LLMClient

SYSTEM_PROMPT = (
    "你是一位專業的會議記錄整理助手。你會收到一份帶有說話人標記與時間戳的會議逐字稿，"
    "請仔細閱讀後，輸出結構化的會議摘要。務必只依據逐字稿內容整理，不要編造未提及的資訊。"
    "如果逐字稿是英文或其他語言，請用相同語言回覆；如果是中文則用繁體中文回覆。\n\n"
    "請務必只回傳一個 JSON 物件，不要加上任何說明文字或 markdown code fence，格式如下：\n"
    "{\n"
    '  "summary": "2-4 句話的會議整體摘要",\n'
    '  "key_points": ["重點一", "重點二", ...],\n'
    '  "decisions": ["會議中做出的決定一", ...],\n'
    '  "action_items": [\n'
    '    {"description": "待辦事項描述", "owner": "負責人或 null", "due_date": "期限或 null"}\n'
    "  ]\n"
    "}"
)


@dataclass
class ActionItemDraft:
    description: str
    owner: str = None
    due_date: str = None


@dataclass
class SummaryResult:
    summary: str
    key_points: List[str] = field(default_factory=list)
    decisions: List[str] = field(default_factory=list)
    action_items: List[ActionItemDraft] = field(default_factory=list)


def build_transcript_text(segments) -> str:
    lines = []
    for seg in segments:
        timestamp = f"[{_format_ts(seg.start)}]"
        lines.append(f"{timestamp} {seg.speaker}: {seg.text}")
    return "\n".join(lines)


def _format_ts(seconds: float) -> str:
    minutes, secs = divmod(int(seconds), 60)
    return f"{minutes:02d}:{secs:02d}"


def _extract_json(raw: str) -> dict:
    text = raw.strip()
    fence_match = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, re.DOTALL)
    if fence_match:
        text = fence_match.group(1)
    else:
        brace_start, brace_end = text.find("{"), text.rfind("}")
        if brace_start != -1 and brace_end != -1:
            text = text[brace_start : brace_end + 1]
    return json.loads(text)


def summarize_meeting(segments, client: LLMClient) -> SummaryResult:
    if not segments:
        return SummaryResult(summary="(空逐字稿，無內容可摘要)")

    transcript_text = build_transcript_text(segments)
    raw = client.generate(SYSTEM_PROMPT, transcript_text)
    try:
        data = _extract_json(raw)
    except (json.JSONDecodeError, ValueError):
        # Model didn't return valid JSON — degrade to a plain-text summary
        # rather than losing the whole run.
        return SummaryResult(summary=raw)

    action_items = [
        ActionItemDraft(
            description=item.get("description", "").strip(),
            owner=item.get("owner") or None,
            due_date=item.get("due_date") or None,
        )
        for item in data.get("action_items", [])
        if item.get("description", "").strip()
    ]
    return SummaryResult(
        summary=data.get("summary", "").strip(),
        key_points=[p for p in data.get("key_points", []) if p],
        decisions=[d for d in data.get("decisions", []) if d],
        action_items=action_items,
    )
