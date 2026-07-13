"""Provider-agnostic LLM client for the summarization step.

Mirrors the routing convention used elsewhere in this account's tooling:
a `provider/model` name routes through OpenRouter (one key, most models);
a bare name is matched by prefix to a native provider; anything
unrecognized falls back to a local Ollama server (no key required).
"""

from abc import ABC, abstractmethod
from typing import Optional

from ..config import Config


class LLMClient(ABC):
    @abstractmethod
    def generate(self, system_prompt: str, user_prompt: str) -> str:
        raise NotImplementedError


class OpenAICompatibleClient(LLMClient):
    """Used for OpenRouter, native OpenAI, DeepSeek, and local Ollama —
    all speak the OpenAI chat-completions API."""

    def __init__(self, model: str, api_key: Optional[str], base_url: Optional[str]):
        try:
            from openai import OpenAI
        except ImportError as e:
            raise ImportError("pip install openai") from e
        self._client = OpenAI(api_key=api_key, base_url=base_url)
        self._model = model

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        response = self._client.chat.completions.create(
            model=self._model,
            temperature=0.2,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        return response.choices[0].message.content.strip()


class AnthropicClient(LLMClient):
    def __init__(self, model: str, api_key: Optional[str], base_url: Optional[str]):
        try:
            from anthropic import Anthropic
        except ImportError as e:
            raise ImportError("pip install anthropic") from e
        self._client = Anthropic(api_key=api_key, base_url=base_url)
        self._model = model

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        response = self._client.messages.create(
            model=self._model,
            max_tokens=4096,
            temperature=0.2,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        return "".join(block.text for block in response.content if block.type == "text").strip()


def _resolve_provider(model_name: str) -> str:
    if "/" in model_name:
        return "openrouter"
    if model_name.startswith("claude-"):
        return "anthropic"
    if model_name.startswith("deepseek-"):
        return "deepseek"
    if model_name.startswith(("gpt-", "o1-", "o3-", "o4-")):
        return "openai"
    return "ollama"


def get_llm_client(model_name: str, config: Config) -> LLMClient:
    provider = _resolve_provider(model_name)
    provider_config = config.providers[provider]

    # OpenRouter model ids keep their `provider/model` prefix in the request.
    model = model_name

    if provider == "anthropic":
        return AnthropicClient(
            model=model, api_key=provider_config.api_key, base_url=provider_config.base_url
        )
    return OpenAICompatibleClient(
        model=model, api_key=provider_config.api_key, base_url=provider_config.base_url
    )
