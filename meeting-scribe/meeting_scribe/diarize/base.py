"""Speaker diarization interface: assign a speaker label to each
(start, end) span of audio. Kept separate from transcription so any STT
engine can be paired with any diarizer."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List


@dataclass
class SpeakerTurn:
    start: float
    end: float
    speaker: str


class Diarizer(ABC):
    @abstractmethod
    def diarize(self, audio_path: str) -> List[SpeakerTurn]:
        raise NotImplementedError


def assign_speakers(segments, turns: List[SpeakerTurn]):
    """Label each transcript segment with the speaker whose turn overlaps it
    the most. Segments with no overlapping turn keep their existing label."""
    if not turns:
        return segments
    for seg in segments:
        best_turn, best_overlap = None, 0.0
        for turn in turns:
            overlap = min(seg.end, turn.end) - max(seg.start, turn.start)
            if overlap > best_overlap:
                best_turn, best_overlap = turn, overlap
        if best_turn is not None:
            seg.speaker = best_turn.speaker
    return segments
