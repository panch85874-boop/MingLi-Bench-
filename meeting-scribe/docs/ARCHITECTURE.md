# Architecture

## Module boundaries

Each stage of the pipeline is an independent module that only depends on
plain dataclasses, never on a specific engine implementation:

- `meeting_scribe/audio/` — microphone capture to WAV. The only producer of
  audio files; recording and importing existing files converge here (both
  just become a path passed to `transcribe`).
- `meeting_scribe/transcribe/` — `Transcriber` ABC + two implementations
  (`LocalWhisperTranscriber`, `ApiWhisperTranscriber`), selected by
  `get_transcriber(config)`. Both return the same `TranscriptResult`.
- `meeting_scribe/diarize/` — `Diarizer` ABC + a pyannote.audio
  implementation. `assign_speakers()` is pure post-processing: it labels
  transcript segments by the speaker turn with the largest time overlap, so
  diarization is decoupled from whichever STT engine produced the segments.
- `meeting_scribe/summarize/` — `LLMClient` ABC with an OpenAI-compatible
  implementation (covers OpenRouter, native OpenAI, DeepSeek, and local
  Ollama, since they all speak the same chat-completions API) and an
  Anthropic implementation. `summarize_meeting()` builds a structured-JSON
  prompt and parses the response defensively (strips markdown fences, falls
  back to a plain-text summary if the model doesn't return valid JSON).
- `meeting_scribe/storage/` — SQLite schema + `Database` class. Owns the
  only writes to disk. Also owns the FTS5 index (see below).
- `meeting_scribe/search/` — thin layer over `Database.search()` that joins
  hits back to meeting metadata.
- `meeting_scribe/cli.py` — wires the above together; no business logic of
  its own beyond argument parsing and output formatting.

## Why trigram FTS5, not the default tokenizer

SQLite FTS5's default `unicode61` tokenizer splits on whitespace and
punctuation. Chinese/Japanese text has no spaces between words, so a whole
sentence becomes a single token — substring queries like searching for a
two-character word inside a longer sentence would never match.

The `trigram` tokenizer indexes every 3-character sliding window instead,
which makes substring search work regardless of language, at the cost of a
minimum query length: a MATCH query shorter than 3 characters produces zero
trigrams and matches nothing. Since 2-character words are extremely common
in Chinese, `Database.search()` detects short query tokens and falls back to
a plain `LIKE` scan over the same FTS5 table's columns (which — unlike
`MATCH` — works for any query length, just without index acceleration).
Given the expected scale of a personal/team meeting archive, that tradeoff
is fine.

## Data model

```
meetings (1) ──< segments        (transcript, one row per utterance)
         (1) ──< summaries       (usually one per meeting; latest wins)
         (1) ──< action_items    (extracted from the summary step)
```

`meeting_fts` is a denormalized full-text index: one row per transcript
(concatenated segment text) and one row per summary, tagged with
`source_type` so search results can distinguish "matched the transcript" vs.
"matched the summary".
