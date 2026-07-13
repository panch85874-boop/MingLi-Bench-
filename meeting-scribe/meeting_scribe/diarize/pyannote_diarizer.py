"""Speaker diarization via pyannote.audio. Optional — requires
`pip install -r requirements-diarize.txt` and a Hugging Face token that has
accepted the pyannote/speaker-diarization-3.1 model terms."""

from typing import List, Optional

from .base import Diarizer, SpeakerTurn


class PyannoteDiarizer(Diarizer):
    def __init__(self, hf_token: Optional[str]):
        try:
            from pyannote.audio import Pipeline
        except ImportError as e:
            raise ImportError(
                "Diarization requires pyannote.audio. "
                "Install with: pip install -r requirements-diarize.txt"
            ) from e
        if not hf_token:
            raise ValueError(
                "Diarization requires HUGGINGFACE_TOKEN in .env — accept the model "
                "terms at https://huggingface.co/pyannote/speaker-diarization-3.1 "
                "and create a token at https://huggingface.co/settings/tokens"
            )

        self._pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-3.1", use_auth_token=hf_token
        )

    def diarize(self, audio_path: str) -> List[SpeakerTurn]:
        diarization = self._pipeline(audio_path)
        turns = []
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            turns.append(SpeakerTurn(start=turn.start, end=turn.end, speaker=speaker))
        return turns
