from ..config import Config
from .base import Transcriber, TranscriptResult, TranscriptSegment


def get_transcriber(config: Config) -> Transcriber:
    if config.stt_engine == "local":
        from .whisper_local import LocalWhisperTranscriber

        return LocalWhisperTranscriber(
            model_size=config.whisper_model_size,
            device=config.whisper_device,
            compute_type=config.whisper_compute_type,
        )
    if config.stt_engine == "api":
        from .whisper_api import ApiWhisperTranscriber

        provider = config.providers["openai"]
        return ApiWhisperTranscriber(api_key=provider.api_key, base_url=provider.base_url)

    raise ValueError(f"Unknown STT_ENGINE '{config.stt_engine}' (expected 'local' or 'api')")


__all__ = ["get_transcriber", "Transcriber", "TranscriptResult", "TranscriptSegment"]
