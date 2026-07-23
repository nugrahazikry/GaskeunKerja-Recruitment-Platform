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


_EDUCATION_PROMPT = """\
Anda membaca persyaratan kualifikasi dari sebuah lowongan pekerjaan berikut. Tentukan jenjang \
pendidikan minimum dan jurusan yang disyaratkan, jika disebutkan secara eksplisit.

Kualifikasi: {qualifications}

Kembalikan HANYA JSON (tanpa teks lain) berbentuk:
{{"required_education_level": "<salah satu dari: SMA, SMK, D3, S1, S2, S3, atau null jika tidak disebutkan>", \
"required_major": "<jurusan yang disyaratkan, atau null jika tidak disebutkan/tidak spesifik>"}}"""


def extract_education_requirement(qualifications: str) -> dict:
    """Round-3 Task 20: a small parallel extraction call (separate from extract_competencies) —
    reads the same Kualifikasi text to find a required education level/major, if the JD states one.
    Kept as its own call rather than folded into the competency-list prompt so the competency
    schema (a JSON array) doesn't have to change shape to carry two extra scalar fields."""
    prompt = _EDUCATION_PROMPT.format(qualifications=qualifications)
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
        logger.warning("extract_education_requirement: failed to parse JSON, raw=%r", raw)
        return {"required_education_level": None, "required_major": None}

    if not isinstance(parsed, dict):
        return {"required_education_level": None, "required_major": None}

    _VALID_LEVELS = {"SMA", "SMK", "D3", "S1", "S2", "S3"}
    level = parsed.get("required_education_level")
    if not isinstance(level, str) or level.upper() not in _VALID_LEVELS:
        level = None
    else:
        level = level.upper()

    major = parsed.get("required_major")
    if not isinstance(major, str) or not major.strip():
        major = None

    return {"required_education_level": level, "required_major": major}
