"""Command-line interface. `python -m meeting_scribe.cli --help` for details."""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import click

from .config import Config, load_config
from .storage import ActionItem, Database, Segment
from .storage.models import Meeting


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _get_config(env_file: Optional[str]) -> Config:
    return load_config(env_file)


def _get_db(config: Config) -> Database:
    return Database(config.db_path)


def _require_meeting(db: Database, meeting_id: int) -> Meeting:
    meeting = db.get_meeting(meeting_id)
    if meeting is None:
        raise click.ClickException(f"No meeting with id {meeting_id}")
    return meeting


env_file_option = click.option(
    "--env-file", default=None, help="Path to a .env file (default: auto-discovered)."
)


@click.group()
def main():
    """Local-first meeting recording, transcription, summarization and search."""


# ----------------------------------------------------------------------
# record
# ----------------------------------------------------------------------
@main.command()
@click.option("--output", "-o", default=None, help="WAV output path (default: data/audio/<timestamp>.wav).")
@click.option("--duration", "-d", type=float, default=None, help="Stop automatically after N seconds.")
def record(output: Optional[str], duration: Optional[float]):
    """Record audio from the default microphone until Ctrl+C."""
    from .audio import RecordingError, record_to_wav

    output = output or f"data/audio/{_now_iso().replace(':', '-')}.wav"
    try:
        record_to_wav(output, duration_seconds=duration)
    except RecordingError as e:
        raise click.ClickException(str(e))
    click.echo(output)


# ----------------------------------------------------------------------
# transcribe
# ----------------------------------------------------------------------
@main.command()
@click.argument("audio_path", type=click.Path(exists=True, dir_okay=False))
@click.option("--title", "-t", default=None, help="Meeting title (default: audio filename).")
@click.option("--diarize/--no-diarize", default=False, help="Label segments by speaker (requires pyannote.audio).")
@env_file_option
def transcribe(audio_path: str, title: Optional[str], diarize: bool, env_file: Optional[str]):
    """Transcribe an audio file and store it as a new meeting."""
    config = _get_config(env_file)
    meeting_id = _transcribe_audio(config, audio_path, title, diarize)
    click.echo(meeting_id)


def _transcribe_audio(config: Config, audio_path: str, title: Optional[str], diarize: bool) -> int:
    from .transcribe import get_transcriber

    title = title or Path(audio_path).stem
    transcriber = get_transcriber(config)
    click.echo(f"Transcribing with engine='{config.stt_engine}'...", err=True)
    result = transcriber.transcribe(audio_path)

    if diarize:
        from .diarize import assign_speakers, get_diarizer

        click.echo("Running speaker diarization...", err=True)
        diarizer = get_diarizer(config)
        turns = diarizer.diarize(audio_path)
        result.segments = assign_speakers(result.segments, turns)

    duration = result.segments[-1].end if result.segments else 0.0

    with _get_db(config) as db:
        meeting_id = db.create_meeting(
            title=title,
            audio_path=str(audio_path),
            created_at=_now_iso(),
            duration_seconds=duration,
            language=result.language,
            status="transcribed",
        )
        db.add_segments(
            meeting_id,
            [
                Segment(id=None, meeting_id=meeting_id, start=s.start, end=s.end, speaker=s.speaker, text=s.text)
                for s in result.segments
            ],
        )
    return meeting_id


# ----------------------------------------------------------------------
# summarize
# ----------------------------------------------------------------------
@main.command()
@click.argument("meeting_id", type=int)
@click.option("--model", "-m", default=None, help="Override the summarization model (default: SUMMARY_MODEL in .env).")
@env_file_option
def summarize(meeting_id: int, model: Optional[str], env_file: Optional[str]):
    """Summarize a meeting's transcript into key points, decisions and action items."""
    config = _get_config(env_file)
    _summarize_meeting(config, meeting_id, model)
    click.echo(f"Summarized meeting {meeting_id}")


def _summarize_meeting(config: Config, meeting_id: int, model: Optional[str]):
    from .summarize import get_llm_client, summarize_meeting

    model = model or config.summary_model
    with _get_db(config) as db:
        _require_meeting(db, meeting_id)
        segments = db.get_segments(meeting_id)
        if not segments:
            raise click.ClickException(
                f"Meeting {meeting_id} has no transcript yet — run `transcribe` first."
            )

        client = get_llm_client(model, config)
        result = summarize_meeting(segments, client)

        db.add_summary(
            meeting_id,
            summary_text=result.summary,
            key_points=result.key_points,
            decisions=result.decisions,
            model=model,
            created_at=_now_iso(),
        )
        db.add_action_items(
            meeting_id,
            [
                ActionItem(
                    id=None,
                    meeting_id=meeting_id,
                    description=item.description,
                    owner=item.owner,
                    due_date=item.due_date,
                )
                for item in result.action_items
            ],
        )
        db.update_meeting_status(meeting_id, "summarized")


# ----------------------------------------------------------------------
# process (transcribe + summarize)
# ----------------------------------------------------------------------
@main.command()
@click.argument("audio_path", type=click.Path(exists=True, dir_okay=False))
@click.option("--title", "-t", default=None)
@click.option("--diarize/--no-diarize", default=False)
@click.option("--model", "-m", default=None)
@env_file_option
def process(audio_path: str, title: Optional[str], diarize: bool, model: Optional[str], env_file: Optional[str]):
    """Transcribe and summarize an audio file in one step."""
    config = _get_config(env_file)
    meeting_id = _transcribe_audio(config, audio_path, title, diarize)
    _summarize_meeting(config, meeting_id, model)
    click.echo(meeting_id)


# ----------------------------------------------------------------------
# list
# ----------------------------------------------------------------------
@main.command(name="list")
@click.option("--limit", "-n", type=int, default=50)
@env_file_option
def list_meetings(limit: int, env_file: Optional[str]):
    """List recent meetings."""
    config = _get_config(env_file)
    with _get_db(config) as db:
        meetings = db.list_meetings(limit=limit)
    if not meetings:
        click.echo("No meetings yet.")
        return
    for m in meetings:
        click.echo(f"[{m.id}] {m.title}  ({m.status}, {m.created_at})")


# ----------------------------------------------------------------------
# show
# ----------------------------------------------------------------------
@main.command()
@click.argument("meeting_id", type=int)
@click.option("--transcript", is_flag=True, help="Include the full transcript.")
@env_file_option
def show(meeting_id: int, transcript: bool, env_file: Optional[str]):
    """Show a meeting's summary, action items and (optionally) transcript."""
    config = _get_config(env_file)
    with _get_db(config) as db:
        meeting = _require_meeting(db, meeting_id)
        summary = db.get_summary(meeting_id)
        actions = db.get_action_items(meeting_id)
        segments = db.get_segments(meeting_id) if transcript else []

    click.echo(f"# {meeting.title}")
    click.echo(f"id={meeting.id} status={meeting.status} created_at={meeting.created_at} "
               f"duration={meeting.duration_seconds:.0f}s language={meeting.language}")

    if summary:
        click.echo("\n## 摘要\n" + summary.summary_text)
        if summary.key_points:
            click.echo("\n## 重點")
            for p in summary.key_points:
                click.echo(f"- {p}")
        if summary.decisions:
            click.echo("\n## 決議")
            for d in summary.decisions:
                click.echo(f"- {d}")
    else:
        click.echo("\n(尚未產生摘要 — 執行 `summarize` 指令)")

    if actions:
        click.echo("\n## 待辦事項")
        for a in actions:
            owner = f" @{a.owner}" if a.owner else ""
            due = f" (期限: {a.due_date})" if a.due_date else ""
            mark = "x" if a.status == "done" else " "
            click.echo(f"- [{mark}] #{a.id} {a.description}{owner}{due}")

    if transcript:
        click.echo("\n## 逐字稿")
        from .summarize import build_transcript_text

        click.echo(build_transcript_text(segments))


# ----------------------------------------------------------------------
# search
# ----------------------------------------------------------------------
@main.command()
@click.argument("query")
@click.option("--limit", "-n", type=int, default=20)
@env_file_option
def search(query: str, limit: int, env_file: Optional[str]):
    """Full-text search across every meeting's transcript and summary."""
    config = _get_config(env_file)
    from .search import search_meetings

    with _get_db(config) as db:
        hits = search_meetings(db, query, limit=limit)
    if not hits:
        click.echo("No matches.")
        return
    for hit in hits:
        click.echo(f"[{hit.meeting_id}] {hit.title} ({hit.source_type}, {hit.created_at})")
        click.echo(f"    {hit.snippet}")


# ----------------------------------------------------------------------
# actions
# ----------------------------------------------------------------------
@main.group()
def actions():
    """Manage action items."""


@actions.command(name="list")
@click.option("--meeting-id", type=int, default=None)
@click.option("--status", type=click.Choice(["open", "done"]), default=None)
@env_file_option
def actions_list(meeting_id: Optional[int], status: Optional[str], env_file: Optional[str]):
    """List action items, optionally filtered by meeting or status."""
    config = _get_config(env_file)
    with _get_db(config) as db:
        if meeting_id is not None:
            meetings = [_require_meeting(db, meeting_id)]
        else:
            meetings = db.list_meetings(limit=10_000)
        for m in meetings:
            items = db.get_action_items(m.id, status=status)
            for item in items:
                owner = f" @{item.owner}" if item.owner else ""
                due = f" (期限: {item.due_date})" if item.due_date else ""
                mark = "x" if item.status == "done" else " "
                click.echo(f"[{mark}] #{item.id} (meeting {m.id} · {m.title}) {item.description}{owner}{due}")


@actions.command(name="done")
@click.argument("item_id", type=int)
@env_file_option
def actions_done(item_id: int, env_file: Optional[str]):
    """Mark an action item as done."""
    config = _get_config(env_file)
    with _get_db(config) as db:
        db.update_action_item_status(item_id, "done")
    click.echo(f"Marked action item {item_id} as done.")


# ----------------------------------------------------------------------
# export
# ----------------------------------------------------------------------
@main.command()
@click.argument("meeting_id", type=int)
@click.option("--format", "fmt", type=click.Choice(["md", "json"]), default="md")
@click.option("--output", "-o", default=None, help="Output path (default: stdout).")
@env_file_option
def export(meeting_id: int, fmt: str, output: Optional[str], env_file: Optional[str]):
    """Export a meeting's notes as Markdown or JSON."""
    config = _get_config(env_file)
    with _get_db(config) as db:
        meeting = _require_meeting(db, meeting_id)
        summary = db.get_summary(meeting_id)
        actions_items = db.get_action_items(meeting_id)
        segments = db.get_segments(meeting_id)

    if fmt == "json":
        payload = {
            "meeting": vars(meeting),
            "summary": vars(summary) if summary else None,
            "action_items": [vars(a) for a in actions_items],
            "segments": [vars(s) for s in segments],
        }
        content = json.dumps(payload, ensure_ascii=False, indent=2)
    else:
        lines = [f"# {meeting.title}", "", f"_{meeting.created_at}_", ""]
        if summary:
            lines += ["## 摘要", summary.summary_text, ""]
            if summary.key_points:
                lines += ["## 重點", *[f"- {p}" for p in summary.key_points], ""]
            if summary.decisions:
                lines += ["## 決議", *[f"- {d}" for d in summary.decisions], ""]
        if actions_items:
            lines += ["## 待辦事項"]
            for a in actions_items:
                owner = f" @{a.owner}" if a.owner else ""
                due = f" (期限: {a.due_date})" if a.due_date else ""
                mark = "x" if a.status == "done" else " "
                lines.append(f"- [{mark}] {a.description}{owner}{due}")
            lines.append("")
        if segments:
            lines += ["## 逐字稿"]
            from .summarize import build_transcript_text

            lines.append(build_transcript_text(segments))
        content = "\n".join(lines)

    if output:
        Path(output).write_text(content, encoding="utf-8")
        click.echo(output)
    else:
        click.echo(content)


# ----------------------------------------------------------------------
# stats
# ----------------------------------------------------------------------
@main.command()
@env_file_option
def stats(env_file: Optional[str]):
    """Print database statistics."""
    config = _get_config(env_file)
    with _get_db(config) as db:
        meetings = db.list_meetings(limit=1_000_000)
    total = len(meetings)
    summarized = sum(1 for m in meetings if m.status == "summarized")
    total_duration = sum(m.duration_seconds for m in meetings)
    click.echo(f"Meetings: {total} (summarized: {summarized})")
    click.echo(f"Total recorded duration: {total_duration / 60:.1f} minutes")
    click.echo(f"Database: {config.db_path}")


if __name__ == "__main__":
    main()
