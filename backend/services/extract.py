import json
import logging

from services import llm_client

logger = logging.getLogger("extract")

_COMPETENCY_PROMPT = """\
Anda adalah asisten HR yang membaca deskripsi pekerjaan berikut dan mengekstrak daftar kompetensi \
(keterampilan/kemampuan) yang dibutuhkan.

Judul: {title}
Tanggung Jawab: {responsibilities}
Persyaratan: {requirements}
Kualifikasi: {qualifications}

Kembalikan HANYA JSON array (tanpa teks lain), setiap item berbentuk:
{{"competency_name": "<nama kompetensi>", "importance_level": <angka 1.0-3.0, 3.0=paling penting>}}

Contoh: [{{"competency_name": "JavaScript", "importance_level": 3.0}}, ...]"""


def extract_competencies(
    title: str, responsibilities: str, requirements: str, qualifications: str
) -> list[dict]:
    """Deepseek Flash -> structured list of {competency_name, importance_level} from a JD."""
    prompt = _COMPETENCY_PROMPT.format(
        title=title,
        responsibilities=responsibilities,
        requirements=requirements,
        qualifications=qualifications,
    )
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
        logger.warning("extract_competencies: failed to parse JSON, raw=%r", raw)
        return []

    if not isinstance(parsed, list):
        return []

    result = []
    for item in parsed:
        if isinstance(item, dict) and "competency_name" in item:
            result.append(
                {
                    "competency_name": str(item["competency_name"]),
                    "importance_level": float(item.get("importance_level", 1.0)),
                }
            )
    return result
