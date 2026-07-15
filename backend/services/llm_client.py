import logging

from openai import OpenAI

from config import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL_FLASH, LLM_MODEL_PRO, LLM_TEMPERATURE_SCORING
from services import llm_cache
from services.retry import with_retry

logger = logging.getLogger("llm_client")

_client = OpenAI(api_key=LLM_API_KEY, base_url=LLM_BASE_URL, timeout=60.0)


@with_retry(max_attempts=3, backoff_seconds=1.0)
def _create_completion(model: str, messages: list[dict], temperature: float):
    return _client.chat.completions.create(model=model, messages=messages, temperature=temperature)


def chat(
    model: str,
    messages: list[dict],
    temperature: float = 0.7,
    bypass_cache: bool = False,
) -> str:
    """Chat completion through SumoPod, with disk caching keyed on (model, messages, temperature).

    Set bypass_cache=True to force a live API call even if a cached response exists
    (needed by determinism tests, which must prove independent calls agree, not replay a cache hit).
    """
    key = llm_cache.make_key(model, messages, temperature)

    if not bypass_cache:
        cached = llm_cache.get(key)
        if cached is not None:
            logger.info("cache hit model=%s tokens=0 (served from cache)", model)
            return cached["content"]

    response = _create_completion(model, messages, temperature)
    content = response.choices[0].message.content or ""
    usage = response.usage

    logger.info(
        "cache miss model=%s prompt_tokens=%s completion_tokens=%s total_tokens=%s",
        model,
        usage.prompt_tokens if usage else "?",
        usage.completion_tokens if usage else "?",
        usage.total_tokens if usage else "?",
    )

    llm_cache.set(key, {"content": content})
    return content


def chat_flash(messages: list[dict], temperature: float = 0.7, bypass_cache: bool = False) -> str:
    """Deepseek Flash — extraction, CV parse, question generation."""
    return chat(LLM_MODEL_FLASH, messages, temperature=temperature, bypass_cache=bypass_cache)


def chat_pro(messages: list[dict], bypass_cache: bool = False) -> str:
    """Deepseek Pro — skill-gap, rubric scoring. Always temperature=0 for determinism."""
    return chat(LLM_MODEL_PRO, messages, temperature=LLM_TEMPERATURE_SCORING, bypass_cache=bypass_cache)
