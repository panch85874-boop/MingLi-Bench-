"""Configuration loading from .env / environment variables."""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


def _find_env_file(start: Path) -> Optional[Path]:
    for directory in (start, *start.parents):
        candidate = directory / ".env"
        if candidate.is_file():
            return candidate
    return None


@dataclass
class ProviderConfig:
    api_key: Optional[str]
    base_url: Optional[str]


@dataclass
class Config:
    db_path: str
    stt_engine: str
    whisper_model_size: str
    whisper_device: str
    whisper_compute_type: str
    huggingface_token: Optional[str]
    summary_model: str
    providers: dict = field(default_factory=dict)


def load_config(env_file: Optional[str] = None) -> Config:
    """Load configuration from a .env file (or the process environment)."""
    if env_file:
        load_dotenv(env_file, override=True)
    else:
        found = _find_env_file(Path.cwd())
        if found:
            load_dotenv(found, override=False)

    providers = {
        "openrouter": ProviderConfig(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url=os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
        ),
        "openai": ProviderConfig(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL"),
        ),
        "anthropic": ProviderConfig(
            api_key=os.getenv("ANTHROPIC_API_KEY"),
            base_url=os.getenv("ANTHROPIC_BASE_URL"),
        ),
        "deepseek": ProviderConfig(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
        ),
        "ollama": ProviderConfig(
            api_key="ollama",  # OpenAI SDK requires a non-empty key even when unused
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1"),
        ),
    }

    return Config(
        db_path=os.getenv("MEETING_SCRIBE_DB", "./data/meetings.db"),
        stt_engine=os.getenv("STT_ENGINE", "local"),
        whisper_model_size=os.getenv("WHISPER_MODEL_SIZE", "small"),
        whisper_device=os.getenv("WHISPER_DEVICE", "cpu"),
        whisper_compute_type=os.getenv("WHISPER_COMPUTE_TYPE", "int8"),
        huggingface_token=os.getenv("HUGGINGFACE_TOKEN") or None,
        summary_model=os.getenv("SUMMARY_MODEL", "anthropic/claude-sonnet-5"),
        providers=providers,
    )
