import json

from click.testing import CliRunner

from meeting_scribe.cli import main
from meeting_scribe.transcribe.base import TranscriptResult, TranscriptSegment


class FakeTranscriber:
    def transcribe(self, audio_path):
        return TranscriptResult(
            segments=[
                TranscriptSegment(start=0.0, end=2.0, text="大家好", speaker="SPEAKER_00"),
                TranscriptSegment(start=2.0, end=4.0, text="今天討論預算", speaker="SPEAKER_00"),
            ],
            language="zh",
        )


class FakeLLMClient:
    def generate(self, system_prompt, user_prompt):
        return json.dumps(
            {
                "summary": "討論了預算。",
                "key_points": ["預算確認"],
                "decisions": ["核准預算"],
                "action_items": [{"description": "更新試算表", "owner": "小美", "due_date": None}],
            },
            ensure_ascii=False,
        )


def write_env(tmp_path):
    env_path = tmp_path / ".env"
    env_path.write_text(f"MEETING_SCRIBE_DB={tmp_path / 'meetings.db'}\n", encoding="utf-8")
    return str(env_path)


def test_list_empty(tmp_path):
    runner = CliRunner()
    env_file = write_env(tmp_path)
    result = runner.invoke(main, ["list", "--env-file", env_file])
    assert result.exit_code == 0
    assert "No meetings yet." in result.output


def test_transcribe_summarize_show_search_flow(tmp_path, monkeypatch):
    monkeypatch.setattr("meeting_scribe.transcribe.get_transcriber", lambda config: FakeTranscriber())
    monkeypatch.setattr("meeting_scribe.summarize.get_llm_client", lambda model, config: FakeLLMClient())

    audio_path = tmp_path / "meeting.wav"
    audio_path.write_bytes(b"fake audio")
    env_file = write_env(tmp_path)

    runner = CliRunner()

    result = runner.invoke(
        main, ["transcribe", str(audio_path), "--title", "預算會議", "--env-file", env_file]
    )
    assert result.exit_code == 0, result.output
    meeting_id = result.output.strip().splitlines()[-1]
    assert meeting_id.isdigit()

    result = runner.invoke(main, ["summarize", meeting_id, "--env-file", env_file])
    assert result.exit_code == 0, result.output

    result = runner.invoke(main, ["show", meeting_id, "--transcript", "--env-file", env_file])
    assert result.exit_code == 0, result.output
    assert "預算確認" in result.output
    assert "核准預算" in result.output
    assert "更新試算表" in result.output
    assert "大家好" in result.output

    result = runner.invoke(main, ["search", "預算", "--env-file", env_file])
    assert result.exit_code == 0, result.output
    assert f"[{meeting_id}]" in result.output

    result = runner.invoke(main, ["actions", "list", "--env-file", env_file])
    assert result.exit_code == 0, result.output
    assert "更新試算表" in result.output

    result = runner.invoke(main, ["export", meeting_id, "--format", "json", "--env-file", env_file])
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["meeting"]["title"] == "預算會議"
    assert payload["summary"]["summary_text"] == "討論了預算。"


def test_process_combines_transcribe_and_summarize(tmp_path, monkeypatch):
    monkeypatch.setattr("meeting_scribe.transcribe.get_transcriber", lambda config: FakeTranscriber())
    monkeypatch.setattr("meeting_scribe.summarize.get_llm_client", lambda model, config: FakeLLMClient())

    audio_path = tmp_path / "meeting.wav"
    audio_path.write_bytes(b"fake audio")
    env_file = write_env(tmp_path)

    runner = CliRunner()
    result = runner.invoke(main, ["process", str(audio_path), "--env-file", env_file])
    assert result.exit_code == 0, result.output
    meeting_id = result.output.strip().splitlines()[-1]

    result = runner.invoke(main, ["show", meeting_id, "--env-file", env_file])
    assert "討論了預算" in result.output


def test_show_unknown_meeting_errors(tmp_path):
    env_file = write_env(tmp_path)
    runner = CliRunner()
    result = runner.invoke(main, ["show", "999", "--env-file", env_file])
    assert result.exit_code != 0
    assert "No meeting with id 999" in result.output
