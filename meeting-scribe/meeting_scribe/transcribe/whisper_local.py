"""Local speech-to-text via faster-whisper (CTranslate2). Default engine —
no API key, no network call, runs on CPU or GPU."""

from .base import Transcriber, TranscriptResult, TranscriptSegment


class LocalWhisperTranscriber(Transcriber):
    def __init__(
        self,
        model_size: str = "small",
        device: str = "cpu",
        compute_type: str = "int8",
    ):
        try:
            from faster_whisper import WhisperModel
        except ImportError as e:
            raise ImportError(
                "Local transcription requires faster-whisper. "
                "Install with: pip install faster-whisper"
            ) from e

        self._model = WhisperModel(model_size, device=device, compute_type=compute_type)

    def transcribe(self, audio_path: str) -> TranscriptResult:
        segments, info = self._model.transcribe(audio_path, vad_filter=True)
        result_segments = [
            TranscriptSegment(start=seg.start, end=seg.end, text=seg.text.strip())
            for seg in segments
        ]
        return TranscriptResult(segments=result_segments, language=info.language)
