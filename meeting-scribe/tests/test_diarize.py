from meeting_scribe.diarize.base import SpeakerTurn, assign_speakers
from meeting_scribe.transcribe.base import TranscriptSegment


def test_assign_speakers_picks_max_overlap():
    segments = [
        TranscriptSegment(start=0.0, end=3.0, text="hello"),
        TranscriptSegment(start=3.0, end=6.0, text="world"),
    ]
    turns = [
        SpeakerTurn(start=0.0, end=3.5, speaker="SPEAKER_00"),
        SpeakerTurn(start=3.5, end=6.0, speaker="SPEAKER_01"),
    ]
    result = assign_speakers(segments, turns)
    assert result[0].speaker == "SPEAKER_00"
    assert result[1].speaker == "SPEAKER_01"


def test_assign_speakers_no_turns_keeps_default():
    segments = [TranscriptSegment(start=0.0, end=1.0, text="hi", speaker="SPEAKER_00")]
    result = assign_speakers(segments, [])
    assert result[0].speaker == "SPEAKER_00"
