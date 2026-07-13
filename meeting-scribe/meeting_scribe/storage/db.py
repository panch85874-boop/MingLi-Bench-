"""SQLite storage layer: meetings, transcript segments, summaries, action
items, and a full-text search index over everything.

FTS5 is used when the local SQLite build supports it (true for the vast
majority of Python installs); otherwise search silently falls back to a
``LIKE``-based scan so the tool still works.
"""

import json
import sqlite3
from contextlib import closing
from pathlib import Path
from typing import Iterable, List, Optional

from .models import ActionItem, Meeting, Segment, Summary

SCHEMA = """
CREATE TABLE IF NOT EXISTS meetings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    audio_path TEXT NOT NULL,
    created_at TEXT NOT NULL,
    duration_seconds REAL NOT NULL DEFAULT 0,
    language TEXT,
    status TEXT NOT NULL DEFAULT 'recorded'
);

CREATE TABLE IF NOT EXISTS segments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    meeting_id INTEGER NOT NULL REFERENCES meetings(id) ON DELETE CASCADE,
    start REAL NOT NULL,
    end REAL NOT NULL,
    speaker TEXT NOT NULL DEFAULT 'SPEAKER_00',
    text TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_segments_meeting ON segments(meeting_id);

CREATE TABLE IF NOT EXISTS summaries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    meeting_id INTEGER NOT NULL REFERENCES meetings(id) ON DELETE CASCADE,
    summary_text TEXT NOT NULL,
    key_points TEXT NOT NULL DEFAULT '[]',
    decisions TEXT NOT NULL DEFAULT '[]',
    model TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_summaries_meeting ON summaries(meeting_id);

CREATE TABLE IF NOT EXISTS action_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    meeting_id INTEGER NOT NULL REFERENCES meetings(id) ON DELETE CASCADE,
    description TEXT NOT NULL,
    owner TEXT,
    due_date TEXT,
    status TEXT NOT NULL DEFAULT 'open'
);
CREATE INDEX IF NOT EXISTS idx_action_items_meeting ON action_items(meeting_id);
"""

FTS_SCHEMA = """
CREATE VIRTUAL TABLE IF NOT EXISTS meeting_fts USING fts5(
    title, source_type UNINDEXED, text, meeting_id UNINDEXED,
    tokenize = "trigram case_sensitive 0"
);
"""
# The trigram tokenizer matches arbitrary substrings without word segmentation,
# which is what makes search usable for CJK text (Chinese/Japanese meeting
# notes have no spaces between words, so the default unicode61 tokenizer would
# treat a whole sentence as one token).

FALLBACK_FTS_SCHEMA = """
CREATE TABLE IF NOT EXISTS meeting_fts_fallback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    source_type TEXT,
    text TEXT,
    meeting_id INTEGER
);
"""


class Database:
    def __init__(self, db_path: str):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.has_fts5 = self._init_schema()

    def _init_schema(self) -> bool:
        with self.conn:
            self.conn.executescript(SCHEMA)
            try:
                self.conn.executescript(FTS_SCHEMA)
                return True
            except sqlite3.OperationalError:
                self.conn.executescript(FALLBACK_FTS_SCHEMA)
                return False

    def close(self):
        self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    # ------------------------------------------------------------------
    # Meetings
    # ------------------------------------------------------------------
    def create_meeting(
        self,
        title: str,
        audio_path: str,
        created_at: str,
        duration_seconds: float = 0.0,
        language: Optional[str] = None,
        status: str = "recorded",
    ) -> int:
        with self.conn:
            cur = self.conn.execute(
                "INSERT INTO meetings (title, audio_path, created_at, duration_seconds, "
                "language, status) VALUES (?, ?, ?, ?, ?, ?)",
                (title, audio_path, created_at, duration_seconds, language, status),
            )
            return cur.lastrowid

    def update_meeting_status(self, meeting_id: int, status: str):
        with self.conn:
            self.conn.execute(
                "UPDATE meetings SET status = ? WHERE id = ?", (status, meeting_id)
            )

    def get_meeting(self, meeting_id: int) -> Optional[Meeting]:
        row = self.conn.execute(
            "SELECT * FROM meetings WHERE id = ?", (meeting_id,)
        ).fetchone()
        return self._row_to_meeting(row) if row else None

    def list_meetings(self, limit: int = 50) -> List[Meeting]:
        rows = self.conn.execute(
            "SELECT * FROM meetings ORDER BY created_at DESC LIMIT ?", (limit,)
        ).fetchall()
        return [self._row_to_meeting(r) for r in rows]

    def delete_meeting(self, meeting_id: int):
        with self.conn:
            self.conn.execute("DELETE FROM meetings WHERE id = ?", (meeting_id,))
            self.conn.execute(
                "DELETE FROM segments WHERE meeting_id = ?", (meeting_id,)
            )
            self.conn.execute(
                "DELETE FROM summaries WHERE meeting_id = ?", (meeting_id,)
            )
            self.conn.execute(
                "DELETE FROM action_items WHERE meeting_id = ?", (meeting_id,)
            )
            if self.has_fts5:
                self.conn.execute(
                    "DELETE FROM meeting_fts WHERE meeting_id = ?", (meeting_id,)
                )
            else:
                self.conn.execute(
                    "DELETE FROM meeting_fts_fallback WHERE meeting_id = ?",
                    (meeting_id,),
                )

    @staticmethod
    def _row_to_meeting(row: sqlite3.Row) -> Meeting:
        return Meeting(
            id=row["id"],
            title=row["title"],
            audio_path=row["audio_path"],
            created_at=row["created_at"],
            duration_seconds=row["duration_seconds"],
            language=row["language"],
            status=row["status"],
        )

    # ------------------------------------------------------------------
    # Segments (transcript)
    # ------------------------------------------------------------------
    def add_segments(self, meeting_id: int, segments: Iterable[Segment]):
        meeting = self.get_meeting(meeting_id)
        title = meeting.title if meeting else ""
        with self.conn:
            for seg in segments:
                self.conn.execute(
                    "INSERT INTO segments (meeting_id, start, end, speaker, text) "
                    "VALUES (?, ?, ?, ?, ?)",
                    (meeting_id, seg.start, seg.end, seg.speaker, seg.text),
                )
            full_text = " ".join(seg.text for seg in segments)
            if full_text.strip():
                self._index_fts(meeting_id, title, "transcript", full_text)

    def get_segments(self, meeting_id: int) -> List[Segment]:
        rows = self.conn.execute(
            "SELECT * FROM segments WHERE meeting_id = ? ORDER BY start ASC",
            (meeting_id,),
        ).fetchall()
        return [
            Segment(
                id=r["id"],
                meeting_id=r["meeting_id"],
                start=r["start"],
                end=r["end"],
                speaker=r["speaker"],
                text=r["text"],
            )
            for r in rows
        ]

    # ------------------------------------------------------------------
    # Summaries
    # ------------------------------------------------------------------
    def add_summary(
        self,
        meeting_id: int,
        summary_text: str,
        key_points: List[str],
        decisions: List[str],
        model: str,
        created_at: str,
    ) -> int:
        meeting = self.get_meeting(meeting_id)
        title = meeting.title if meeting else ""
        with self.conn:
            cur = self.conn.execute(
                "INSERT INTO summaries (meeting_id, summary_text, key_points, decisions, "
                "model, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                (
                    meeting_id,
                    summary_text,
                    json.dumps(key_points, ensure_ascii=False),
                    json.dumps(decisions, ensure_ascii=False),
                    model,
                    created_at,
                ),
            )
            searchable = "\n".join([summary_text, *key_points, *decisions])
            self._index_fts(meeting_id, title, "summary", searchable)
            return cur.lastrowid

    def get_summary(self, meeting_id: int) -> Optional[Summary]:
        row = self.conn.execute(
            "SELECT * FROM summaries WHERE meeting_id = ? ORDER BY id DESC LIMIT 1",
            (meeting_id,),
        ).fetchone()
        if not row:
            return None
        return Summary(
            id=row["id"],
            meeting_id=row["meeting_id"],
            summary_text=row["summary_text"],
            key_points=json.loads(row["key_points"]),
            decisions=json.loads(row["decisions"]),
            model=row["model"],
            created_at=row["created_at"],
        )

    # ------------------------------------------------------------------
    # Action items
    # ------------------------------------------------------------------
    def add_action_items(self, meeting_id: int, items: Iterable[ActionItem]):
        with self.conn:
            for item in items:
                self.conn.execute(
                    "INSERT INTO action_items (meeting_id, description, owner, due_date, "
                    "status) VALUES (?, ?, ?, ?, ?)",
                    (meeting_id, item.description, item.owner, item.due_date, item.status),
                )

    def get_action_items(
        self, meeting_id: int, status: Optional[str] = None
    ) -> List[ActionItem]:
        if status:
            rows = self.conn.execute(
                "SELECT * FROM action_items WHERE meeting_id = ? AND status = ? ORDER BY id",
                (meeting_id, status),
            ).fetchall()
        else:
            rows = self.conn.execute(
                "SELECT * FROM action_items WHERE meeting_id = ? ORDER BY id",
                (meeting_id,),
            ).fetchall()
        return [
            ActionItem(
                id=r["id"],
                meeting_id=r["meeting_id"],
                description=r["description"],
                owner=r["owner"],
                due_date=r["due_date"],
                status=r["status"],
            )
            for r in rows
        ]

    def update_action_item_status(self, item_id: int, status: str):
        with self.conn:
            self.conn.execute(
                "UPDATE action_items SET status = ? WHERE id = ?", (status, item_id)
            )

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------
    def _index_fts(self, meeting_id: int, title: str, source_type: str, text: str):
        if self.has_fts5:
            self.conn.execute(
                "INSERT INTO meeting_fts (title, source_type, text, meeting_id) "
                "VALUES (?, ?, ?, ?)",
                (title, source_type, text, meeting_id),
            )
        else:
            self.conn.execute(
                "INSERT INTO meeting_fts_fallback (title, source_type, text, meeting_id) "
                "VALUES (?, ?, ?, ?)",
                (title, source_type, text, meeting_id),
            )

    # The trigram tokenizer only emits tokens for runs of 3+ characters, so a
    # MATCH query built from a shorter term (very common in Chinese, e.g. a
    # 2-character word like 預算) silently matches nothing. Below that length
    # we scan with LIKE instead — same virtual table, just bypassing MATCH.
    _TRIGRAM_MIN_LEN = 3

    def search(self, query: str, limit: int = 20) -> List[dict]:
        query = query.strip()
        if not query:
            return []
        tokens = query.split()

        if self.has_fts5 and all(len(t) >= self._TRIGRAM_MIN_LEN for t in tokens):
            rows = self.conn.execute(
                "SELECT meeting_id, title, source_type, "
                "snippet(meeting_fts, 2, '[', ']', '...', 12) AS snippet "
                "FROM meeting_fts WHERE meeting_fts MATCH ? "
                "ORDER BY rank LIMIT ?",
                (self._fts_query(tokens), limit),
            ).fetchall()
        elif self.has_fts5:
            # Short-token fallback: scan the fts5 table's columns directly
            # (a plain WHERE ... LIKE, not a MATCH) so short CJK words still work.
            clauses = " AND ".join(["(title LIKE ? OR text LIKE ?)"] * len(tokens))
            params = [p for t in tokens for p in (f"%{t}%", f"%{t}%")]
            rows = self.conn.execute(
                f"SELECT meeting_id, title, source_type, text AS snippet "
                f"FROM meeting_fts WHERE {clauses} LIMIT ?",
                (*params, limit),
            ).fetchall()
        else:
            clauses = " AND ".join(["(title LIKE ? OR text LIKE ?)"] * len(tokens))
            params = [p for t in tokens for p in (f"%{t}%", f"%{t}%")]
            rows = self.conn.execute(
                f"SELECT meeting_id, title, source_type, text AS snippet "
                f"FROM meeting_fts_fallback WHERE {clauses} LIMIT ?",
                (*params, limit),
            ).fetchall()
        return [
            {
                "meeting_id": r["meeting_id"],
                "title": r["title"],
                "source_type": r["source_type"],
                "snippet": r["snippet"],
            }
            for r in rows
        ]

    @staticmethod
    def _fts_query(tokens: List[str]) -> str:
        """Quote each token so punctuation/CJK text can't break FTS5 syntax."""
        escaped = [f'"{t.replace(chr(34), chr(34) * 2)}"' for t in tokens]
        return " ".join(escaped)
