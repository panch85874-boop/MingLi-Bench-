from meeting_scribe.storage import ActionItem, Database, Segment


def make_db(tmp_path):
    return Database(str(tmp_path / "meetings.db"))


def test_create_and_get_meeting(tmp_path):
    with make_db(tmp_path) as db:
        meeting_id = db.create_meeting(
            title="週會", audio_path="a.wav", created_at="2026-07-13T10:00:00Z"
        )
        meeting = db.get_meeting(meeting_id)
        assert meeting.title == "週會"
        assert meeting.status == "recorded"


def test_list_meetings_order(tmp_path):
    with make_db(tmp_path) as db:
        db.create_meeting(title="A", audio_path="a.wav", created_at="2026-01-01T00:00:00Z")
        db.create_meeting(title="B", audio_path="b.wav", created_at="2026-02-01T00:00:00Z")
        meetings = db.list_meetings()
        assert [m.title for m in meetings] == ["B", "A"]


def test_segments_round_trip(tmp_path):
    with make_db(tmp_path) as db:
        meeting_id = db.create_meeting(title="Standup", audio_path="a.wav", created_at="now")
        db.add_segments(
            meeting_id,
            [
                Segment(id=None, meeting_id=meeting_id, start=0.0, end=2.0, speaker="SPEAKER_00", text="大家好"),
                Segment(id=None, meeting_id=meeting_id, start=2.0, end=4.0, speaker="SPEAKER_01", text="我們開始吧"),
            ],
        )
        segments = db.get_segments(meeting_id)
        assert [s.text for s in segments] == ["大家好", "我們開始吧"]
        assert segments[0].speaker == "SPEAKER_00"


def test_summary_round_trip(tmp_path):
    with make_db(tmp_path) as db:
        meeting_id = db.create_meeting(title="Planning", audio_path="a.wav", created_at="now")
        db.add_summary(
            meeting_id,
            summary_text="討論了第三季計畫。",
            key_points=["預算確認", "時程調整"],
            decisions=["延後兩週上線"],
            model="anthropic/claude-sonnet-5",
            created_at="now",
        )
        summary = db.get_summary(meeting_id)
        assert summary.summary_text == "討論了第三季計畫。"
        assert summary.key_points == ["預算確認", "時程調整"]
        assert summary.decisions == ["延後兩週上線"]


def test_action_items_status(tmp_path):
    with make_db(tmp_path) as db:
        meeting_id = db.create_meeting(title="Kickoff", audio_path="a.wav", created_at="now")
        db.add_action_items(
            meeting_id,
            [ActionItem(id=None, meeting_id=meeting_id, description="寄送會議紀錄", owner="小明", due_date="2026-07-20")],
        )
        items = db.get_action_items(meeting_id)
        assert len(items) == 1
        assert items[0].status == "open"

        db.update_action_item_status(items[0].id, "done")
        done_items = db.get_action_items(meeting_id, status="done")
        assert len(done_items) == 1
        assert db.get_action_items(meeting_id, status="open") == []


def test_search_finds_cjk_substring(tmp_path):
    """Regression guard: FTS5's default tokenizer treats a whole CJK
    sentence as one token, which would make substring queries fail. This
    project configures the trigram tokenizer instead."""
    with make_db(tmp_path) as db:
        meeting_id = db.create_meeting(title="產品規劃會議", audio_path="a.wav", created_at="now")
        db.add_segments(
            meeting_id,
            [Segment(id=None, meeting_id=meeting_id, start=0.0, end=1.0, speaker="SPEAKER_00", text="我們需要在下週前完成新版登入頁面的設計")],
        )
        hits = db.search("登入頁面")
        assert any(h["meeting_id"] == meeting_id for h in hits)


def test_search_short_cjk_term(tmp_path):
    """A common 2-character Chinese word is shorter than the trigram
    tokenizer's minimum token length — must still be findable."""
    with make_db(tmp_path) as db:
        meeting_id = db.create_meeting(title="財務會議", audio_path="a.wav", created_at="now")
        db.add_segments(
            meeting_id,
            [Segment(id=None, meeting_id=meeting_id, start=0.0, end=1.0, speaker="SPEAKER_00", text="今天討論預算分配")],
        )
        hits = db.search("預算")
        assert any(h["meeting_id"] == meeting_id for h in hits)


def test_search_across_summary_and_transcript(tmp_path):
    with make_db(tmp_path) as db:
        meeting_id = db.create_meeting(title="Retro", audio_path="a.wav", created_at="now")
        db.add_segments(
            meeting_id,
            [Segment(id=None, meeting_id=meeting_id, start=0.0, end=1.0, speaker="SPEAKER_00", text="deployment pipeline is flaky")],
        )
        db.add_summary(
            meeting_id,
            summary_text="Team agreed to fix the flaky pipeline.",
            key_points=[],
            decisions=[],
            model="test",
            created_at="now",
        )
        hits = db.search("flaky")
        source_types = {h["source_type"] for h in hits if h["meeting_id"] == meeting_id}
        assert "transcript" in source_types
        assert "summary" in source_types


def test_search_empty_query_returns_nothing(tmp_path):
    with make_db(tmp_path) as db:
        assert db.search("") == []
        assert db.search("   ") == []


def test_delete_meeting_cascades(tmp_path):
    with make_db(tmp_path) as db:
        meeting_id = db.create_meeting(title="Temp", audio_path="a.wav", created_at="now")
        db.add_segments(
            meeting_id,
            [Segment(id=None, meeting_id=meeting_id, start=0.0, end=1.0, speaker="SPEAKER_00", text="hello world")],
        )
        db.delete_meeting(meeting_id)
        assert db.get_meeting(meeting_id) is None
        assert db.get_segments(meeting_id) == []
        assert db.search("hello") == []
