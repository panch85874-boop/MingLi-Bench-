"""Plain dataclasses mirroring the SQLite schema."""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Meeting:
    id: Optional[int]
    title: str
    audio_path: str
    created_at: str
    duration_seconds: float = 0.0
    language: Optional[str] = None
    status: str = "recorded"  # recorded -> transcribed -> summarized


@dataclass
class Segment:
    id: Optional[int]
    meeting_id: int
    start: float
    end: float
    speaker: str
    text: str


@dataclass
class ActionItem:
    id: Optional[int]
    meeting_id: int
    description: str
    owner: Optional[str] = None
    due_date: Optional[str] = None
    status: str = "open"  # open -> done


@dataclass
class Summary:
    id: Optional[int]
    meeting_id: int
    summary_text: str
    key_points: List[str] = field(default_factory=list)
    decisions: List[str] = field(default_factory=list)
    model: str = ""
    created_at: str = ""
