import base64
import logging

from openai import OpenAI

from config import LLM_API_KEY, LLM_BASE_URL, STT_API_KEY, STT_BASE_URL, VISION_MODEL, VISION_PROVIDER

logger = logging.getLogger("vision_client")

# Provider switched 2026-07-15: vision now defaults to SumoPod's gemini/gemini-2.5-flash-lite
# (verified working via a real test call — image_tokens=258 confirmed real image ingestion,
# not the silent-failure behavior seen with SumoPod's deepseek-v4-pro on 2026-07-13). ~14%
# cheaper per image than the previous Groq Llama 4 Scout default. Groq is kept available as
# VISION_PROVIDER=groq for rollback, reusing the same client already set up for STT.
_groq_client = OpenAI(api_key=STT_API_KEY, base_url=STT_BASE_URL)
_sumopod_client = OpenAI(api_key=LLM_API_KEY, base_url=LLM_BASE_URL)

_TRANSCRIBE_PROMPT = (
    "Gambar ini berasal dari sebuah halaman CV. Baca dan tuliskan ulang SEMUA teks yang "
    "terlihat pada gambar ini secara verbatim (apa adanya), termasuk nama, kontak, riwayat "
    "pekerjaan, pendidikan, dan keterampilan, jika ada. Jika gambar ini murni dekoratif "
    "(misalnya logo, foto profil, atau ikon) tanpa teks yang bisa dibaca, katakan bahwa "
    "tidak ada teks yang ditemukan — jangan mengarang teks yang tidak benar-benar ada."
)


def _image_to_data_url(image_bytes: bytes, mime_type: str = "image/png") -> str:
    b64 = base64.b64encode(image_bytes).decode("utf-8")
    return f"data:{mime_type};base64,{b64}"


def _caption(image_bytes: bytes, prompt: str, mime_type: str = "image/png") -> str:
    if VISION_PROVIDER == "sumopod":
        client = _sumopod_client
    elif VISION_PROVIDER == "groq":
        client = _groq_client
    else:
        raise ValueError(f"Unsupported VISION_PROVIDER: {VISION_PROVIDER} (use 'sumopod' or 'groq')")

    data_url = _image_to_data_url(image_bytes, mime_type)
    response = client.chat.completions.create(
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
    """Verbatim read-out of any embedded CV image, called unconditionally on every
    embedded image regardless of whether its page also has separately-extracted text
    (2026-07-15 fix — see pdf_captioning.py's docstring for the real leak this closes)."""
    return _caption(image_bytes, _TRANSCRIBE_PROMPT, mime_type)
