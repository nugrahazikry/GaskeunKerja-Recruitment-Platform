import logging

from openai import OpenAI

from config import STT_API_KEY, STT_BASE_URL, STT_LANGUAGE, STT_MODEL, STT_PROVIDER

logger = logging.getLogger("stt_client")

_client: OpenAI | None = None
if STT_PROVIDER in ("groq", "openai"):
    _client = OpenAI(api_key=STT_API_KEY, base_url=STT_BASE_URL)


def transcribe(audio_path: str) -> str:
    """Transcribe a webm audio file to text, per STT_PROVIDER (groq | openai | local)."""
    if STT_PROVIDER in ("groq", "openai"):
        with open(audio_path, "rb") as f:
            response = _client.audio.transcriptions.create(
                model=STT_MODEL,
                language=STT_LANGUAGE,
                file=f,
            )
        logger.info("transcribed provider=%s model=%s file=%s", STT_PROVIDER, STT_MODEL, audio_path)
        return response.text

    if STT_PROVIDER == "local":
        raise NotImplementedError(
            "STT_PROVIDER=local (faster-whisper) is not implemented yet — "
            "documented fallback per Area 4 T3b, build only if Groq becomes unavailable"
        )

    raise ValueError(f"Unknown STT_PROVIDER: {STT_PROVIDER}")
