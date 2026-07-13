"""Transcriber interface. Every engine returns the same shape so the rest of
the pipeline (diarization, storage, summarization) never needs to know which
engine produced the transcript."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class TranscriptSegment:
    start: float
    end: float
    text: str
    speaker: str = "SPEAKER_00"


@dataclass
class TranscriptResult:
    segments: List[TranscriptSegment]
    language: Optional[str] = None


class Transcriber(ABC):
    @abstractmethod
    def transcribe(self, audio_path: str) -> TranscriptResult:
        """Transcribe an audio file into timestamped segments."""
        raise NotImplementedError
