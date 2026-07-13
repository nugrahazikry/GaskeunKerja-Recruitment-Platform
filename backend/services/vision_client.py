import base64
import logging

from openai import OpenAI

from config import STT_API_KEY, STT_BASE_URL, VISION_MODEL, VISION_PROVIDER

logger = logging.getLogger("vision_client")

# Vision is served via Groq, reusing the same base_url/key already set up for STT (Area 4 T3b) —
# SumoPod's deepseek-v4-pro was verified 2026-07-13 to NOT support vision (see plan.md decision log).
_client = OpenAI(api_key=STT_API_KEY, base_url=STT_BASE_URL)

_TRANSCRIBE_PROMPT = (
    "Gambar ini adalah halaman CV yang dipindai (scan), tanpa teks yang bisa diekstrak langsung. "
    "Baca dan tuliskan ulang SEMUA teks yang terlihat pada gambar ini secara verbatim (apa adanya), "
    "termasuk nama, kontak, riwayat pekerjaan, pendidikan, dan keterampilan. "
    "Jangan meringkas atau menafsirkan — hanya transkripsikan teksnya."
)

_DESCRIBE_PROMPT = (
    "Gambar ini muncul pada halaman CV yang sudah memiliki teks lain. "
    "Jelaskan secara singkat apa isi gambar ini (misalnya logo, foto profil, ikon, atau diagram) "
    "dalam satu atau dua kalimat."
)


def _image_to_data_url(image_bytes: bytes, mime_type: str = "image/png") -> str:
    b64 = base64.b64encode(image_bytes).decode("utf-8")
    return f"data:{mime_type};base64,{b64}"


def _caption(image_bytes: bytes, prompt: str, mime_type: str = "image/png") -> str:
    if VISION_PROVIDER != "groq":
        raise ValueError(f"Unsupported VISION_PROVIDER: {VISION_PROVIDER} (only 'groq' is implemented)")

    data_url = _image_to_data_url(image_bytes, mime_type)
    response = _client.chat.completions.create(
        model=VISION_MODEL,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": data_url}},
                ],
            }
        ],
        max_tokens=1024,
    )
    text = response.choices[0].message.content or ""
    usage = response.usage
    logger.info(
        "vision call model=%s prompt_tokens=%s completion_tokens=%s",
        VISION_MODEL,
        usage.prompt_tokens if usage else "?",
        usage.completion_tokens if usage else "?",
    )
    return text


def transcribe_image(image_bytes: bytes, mime_type: str = "image/png") -> str:
    """Verbatim read-out — use for images on pages with no extractable text (likely scanned)."""
    return _caption(image_bytes, _TRANSCRIBE_PROMPT, mime_type)


def describe_image(image_bytes: bytes, mime_type: str = "image/png") -> str:
    """Short caption — use for images on pages that already have extracted text (logos, photos, icons)."""
    return _caption(image_bytes, _DESCRIBE_PROMPT, mime_type)
