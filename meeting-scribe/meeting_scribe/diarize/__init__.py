from ..config import Config
from .base import Diarizer, SpeakerTurn, assign_speakers


def get_diarizer(config: Config) -> Diarizer:
    from .pyannote_diarizer import PyannoteDiarizer

    return PyannoteDiarizer(hf_token=config.huggingface_token)


__all__ = ["get_diarizer", "Diarizer", "SpeakerTurn", "assign_speakers"]
