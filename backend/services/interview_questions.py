import json
import logging

from services import llm_client

logger = logging.getLogger("interview_questions")

_QUESTION_PROMPT = """\
Anda adalah recruiter yang menyusun pertanyaan wawancara untuk posisi berikut:

Judul: {title}
Tanggung Jawab: {responsibilities}
Persyaratan: {requirements}

Buat 2-3 pertanyaan wawancara singkat dalam Bahasa Indonesia yang menguji kompetensi teknis \
dan pengalaman yang relevan untuk posisi ini. Setiap pertanyaan harus bisa dijawab lisan dalam \
1-2 menit.

Kembalikan HANYA JSON array berisi string pertanyaan, contoh:
["Pertanyaan pertama?", "Pertanyaan kedua?"]"""


def generate_questions(title: str, responsibilities: str, requirements: str) -> list[str]:
    """Deepseek Flash -> 2-3 Indonesian interview questions for a JD."""
    prompt = _QUESTION_PROMPT.format(title=title, responsibilities=responsibilities, requirements=requirements)
    raw = llm_client.chat_flash([{"role": "user", "content": prompt}])

    text = raw.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        logger.warning("generate_questions: failed to parse JSON, raw=%r", raw)
        return []

    if not isinstance(parsed, list):
        return []
    return [str(q) for q in parsed if isinstance(q, str)][:3]
