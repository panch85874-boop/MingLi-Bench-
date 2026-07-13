"""Microphone recording to a WAV file.

Kept deliberately separate from the transcription/summarization pipeline:
`record_to_wav` is the only entry point, and everything downstream just
consumes a path to an audio file — so imported audio (Zoom/Teams exports,
phone recordings, etc.) flows through the exact same pipeline.
"""

import signal
import sys
from pathlib import Path
from typing import Optional

SAMPLE_RATE = 16000  # matches what Whisper expects; avoids a resample step
CHANNELS = 1


class RecordingError(RuntimeError):
    pass


def record_to_wav(
    output_path: str,
    duration_seconds: Optional[float] = None,
    sample_rate: int = SAMPLE_RATE,
) -> str:
    """Record from the default microphone until Ctrl+C (or `duration_seconds`).

    Requires `sounddevice` + a working audio input device, which is often
    unavailable in headless/CI/container environments — raises
    `RecordingError` with a clear message in that case rather than a raw
    backend traceback.
    """
    try:
        import numpy as np
        import sounddevice as sd
        import soundfile as sf
    except ImportError as e:
        raise RecordingError(
            "Recording requires the 'sounddevice', 'soundfile' and 'numpy' "
            "packages. Install with: pip install -r requirements.txt"
        ) from e

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    chunks = []
    stop = {"requested": False}

    def handle_sigint(signum, frame):
        stop["requested"] = True

    def callback(indata, frames, time_info, status):
        chunks.append(indata.copy())
        if duration_seconds is not None:
            elapsed = sum(len(c) for c in chunks) / sample_rate
            if elapsed >= duration_seconds:
                raise sd.CallbackStop()

    previous_handler = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, handle_sigint)
    try:
        print("Recording... press Ctrl+C to stop.", file=sys.stderr)
        with sd.InputStream(
            samplerate=sample_rate, channels=CHANNELS, callback=callback
        ):
            while not stop["requested"]:
                sd.sleep(200)
                if duration_seconds is not None:
                    elapsed = sum(len(c) for c in chunks) / sample_rate
                    if elapsed >= duration_seconds:
                        break
    except sd.PortAudioError as e:
        raise RecordingError(
            f"No usable audio input device found: {e}. "
            "If you're recording system/meeting audio rather than a "
            "microphone, record with your OS/meeting app and pass the file "
            "to `meeting-scribe transcribe` instead."
        ) from e
    finally:
        signal.signal(signal.SIGINT, previous_handler)

    if not chunks:
        raise RecordingError("No audio captured.")

    audio = np.concatenate(chunks, axis=0)
    sf.write(output_path, audio, sample_rate)
    print(f"Saved recording to {output_path}", file=sys.stderr)
    return output_path
