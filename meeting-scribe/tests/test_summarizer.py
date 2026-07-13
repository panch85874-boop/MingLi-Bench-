import json

from meeting_scribe.summarize.summarizer import (
    ActionItemDraft,
    SummaryResult,
    build_transcript_text,
    summarize_meeting,
)
from meeting_scribe.transcribe.base import TranscriptSegment


class FakeLLMClient:
    def __init__(self, response: str):
        self.response = response
        self.last_call = None

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        self.last_call = (system_prompt, user_prompt)
        return self.response


def make_segments():
    return [
        TranscriptSegment(start=0.0, end=2.0, text="大家好，我們開始週會", speaker="SPEAKER_00"),
        TranscriptSegment(start=2.0, end=5.0, text="這週我完成了登入頁面", speaker="SPEAKER_01"),
    ]


def test_build_transcript_text_includes_speaker_and_timestamp():
    text = build_transcript_text(make_segments())
    assert "SPEAKER_00" in text
    assert "[00:00]" in text
    assert "登入頁面" in text


def test_summarize_meeting_parses_plain_json():
    payload = {
        "summary": "討論了本週進度。",
        "key_points": ["登入頁面已完成"],
        "decisions": ["下週開始測試"],
        "action_items": [{"description": "撰寫測試案例", "owner": "小華", "due_date": "2026-07-20"}],
    }
    client = FakeLLMClient(json.dumps(payload, ensure_ascii=False))
    result = summarize_meeting(make_segments(), client)

    assert isinstance(result, SummaryResult)
    assert result.summary == "討論了本週進度。"
    assert result.key_points == ["登入頁面已完成"]
    assert result.decisions == ["下週開始測試"]
    assert len(result.action_items) == 1
    assert isinstance(result.action_items[0], ActionItemDraft)
    assert result.action_items[0].owner == "小華"


def test_summarize_meeting_strips_markdown_fence():
    payload = {"summary": "OK", "key_points": [], "decisions": [], "action_items": []}
    fenced = f"這是分析：\n```json\n{json.dumps(payload)}\n```"
    client = FakeLLMClient(fenced)
    result = summarize_meeting(make_segments(), client)
    assert result.summary == "OK"


def test_summarize_meeting_falls_back_to_plain_text_on_bad_json():
    client = FakeLLMClient("抱歉，我無法產生 JSON。")
    result = summarize_meeting(make_segments(), client)
    assert result.summary == "抱歉，我無法產生 JSON。"
    assert result.key_points == []
    assert result.action_items == []


def test_summarize_meeting_empty_segments_short_circuits():
    client = FakeLLMClient("should not be called")
    result = summarize_meeting([], client)
    assert client.last_call is None
    assert "空逐字稿" in result.summary


def test_summarize_meeting_drops_action_items_without_description():
    payload = {
        "summary": "x",
        "key_points": [],
        "decisions": [],
        "action_items": [{"description": "  ", "owner": None}, {"description": "follow up", "owner": None}],
    }
    client = FakeLLMClient(json.dumps(payload))
    result = summarize_meeting(make_segments(), client)
    assert len(result.action_items) == 1
    assert result.action_items[0].description == "follow up"
