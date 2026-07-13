<div align="center">

# Meeting Scribe

**A local-first CLI for recording, transcribing, summarizing and searching meetings.**

English | [中文](./README_zh.md)

</div>

---

## What this is

A small pipeline that takes a meeting from "we talked about it" to "I can find what we said":

```
Record / import audio
        │
        ▼
Speech-to-text (local faster-whisper, or a cloud Whisper API)
        │
        ▼
Speaker diarization (optional, pyannote.audio)
        │
        ▼
AI summary: key points / decisions / action items (any LLM you point it at)
        │
        ▼
SQLite storage + full-text search (transcripts and summaries, CJK-aware)
```

Every stage is swappable — STT engine, summarization model, whether to diarize — all driven by `.env`, no hard dependency on any single vendor.

This lives inside the [MingLi-Bench-](../) repository as a self-contained subdirectory — it has its own dependencies, tests and `.env`, and doesn't share any code with `mingli_bench/`.

## Install

```bash
git clone https://github.com/panch85874-boop/MingLi-Bench-.git
cd MingLi-Bench-/meeting-scribe
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# edit .env — at minimum set an LLM key for summarization
# (OPENROUTER_API_KEY is the easiest: one key, most models)
```

Speech-to-text defaults to local `faster-whisper` (no API key, no network call after the model is downloaded on first run). To use a cloud Whisper API instead, set `STT_ENGINE=api` and `OPENAI_API_KEY` in `.env`.

Speaker diarization is optional:

```bash
pip install -r requirements-diarize.txt
```

and requires a Hugging Face token that has accepted the model terms at [huggingface.co/pyannote/speaker-diarization-3.1](https://huggingface.co/pyannote/speaker-diarization-3.1), set as `HUGGINGFACE_TOKEN` in `.env`.

## Quick start

```bash
# 1. Record (Ctrl+C to stop), or use an audio file you already have
python -m meeting_scribe.cli record -o data/audio/weekly.wav

# 2. One shot: transcribe + AI summary + action items
python -m meeting_scribe.cli process data/audio/weekly.wav \
    --title "Weekly sync 2026-07-13" --diarize

# 3. Read the notes
python -m meeting_scribe.cli show 1

# 4. Later: "who owned the budget follow-up again?"
python -m meeting_scribe.cli search budget
```

Or run each stage separately:

```bash
python -m meeting_scribe.cli transcribe data/audio/weekly.wav --title "Weekly sync" --diarize
python -m meeting_scribe.cli summarize 1 --model anthropic/claude-sonnet-5
```

## CLI reference

| Command | Description |
|---|---|
| `record` | Record from the default microphone; stop with Ctrl+C or `--duration` |
| `transcribe AUDIO` | Transcribe and create a meeting record; `--diarize` adds speaker labels |
| `summarize MEETING_ID` | Generate summary, key points, decisions, action items via LLM |
| `process AUDIO` | `transcribe` + `summarize` in one call |
| `list` | List recent meetings |
| `show MEETING_ID` | Show summary / action items / transcript (`--transcript` includes the transcript) |
| `search QUERY` | Full-text search across every meeting's transcript and summary |
| `actions list` / `actions done ID` | Manage action items |
| `export MEETING_ID --format md\|json` | Export meeting notes |
| `stats` | Database statistics |

Every command accepts `--env-file` to point at a different config (e.g. a different model or database per project).

## Choosing a summarization model

`SUMMARY_MODEL` accepts:

- `provider/model` (e.g. `anthropic/claude-sonnet-5`, `openai/gpt-4o`) → routed through OpenRouter, one key for most models
- a bare native model name (`claude-*` → Anthropic, `deepseek-*` → DeepSeek, `gpt-*` → OpenAI) → routed to that provider's native API
- anything else (e.g. a self-hosted Ollama model like `qwen2.5`, `llama3`) → routed to `OLLAMA_BASE_URL`, no key required, fully offline

## Where your data lives

Meetings, transcripts, summaries and action items all live in a single SQLite file (`data/meetings.db` by default), indexed for full-text search (FTS5 with the trigram tokenizer, so substring search works for CJK text with no spaces, not just English). No external database, no cloud dependency — the whole thing can run entirely on your own machine.

## Development

```bash
pip install -r requirements-dev.txt
pytest
```

## License

[MIT License](./LICENSE)
