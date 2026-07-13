"""Cloud speech-to-text via an OpenAI-compatible Whisper endpoint."""

from typing import Optional

from .base import Transcriber, TranscriptResult, TranscriptSegment


class ApiWhisperTranscriber(Transcriber):
    def __init__(self, api_key: str, base_url: Optional[str] = None, model: str = "whisper-1"):
        try:
            from openai import OpenAI
        except ImportError as e:
            raise ImportError(
                "API transcription requires the openai package. "
                "Install with: pip install openai"
            ) from e
        if not api_key:
            raise ValueError(
                "STT_ENGINE=api requires OPENAI_API_KEY to be set in .env"
            )

        self._client = OpenAI(api_key=api_key, base_url=base_url)
        self._model = model

    def transcribe(self, audio_path: str) -> TranscriptResult:
        with open(audio_path, "rb") as f:
            response = self._client.audio.transcriptions.create(
                model=self._model,
                file=f,
                response_format="verbose_json",
                timestamp_granularities=["segment"],
            )

        segments = getattr(response, "segments", None) or []
        result_segments = [
            TranscriptSegment(
                start=seg["start"] if isinstance(seg, dict) else seg.start,
                end=seg["end"] if isinstance(seg, dict) else seg.end,
                text=(seg["text"] if isinstance(seg, dict) else seg.text).strip(),
            )
            for seg in segments
        ]
        if not result_segments:
            # Some gateways only return the flat `text` field.
            text = getattr(response, "text", "") or ""
            if text.strip():
                result_segments = [TranscriptSegment(start=0.0, end=0.0, text=text.strip())]

        language = getattr(response, "language", None)
        return TranscriptResult(segments=result_segments, language=language)
