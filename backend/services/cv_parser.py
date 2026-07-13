import json
import logging

from services import llm_client

logger = logging.getLogger("cv_parser")

_PARSE_PROMPT = """\
Anda membaca teks CV kandidat berikut (nama asli sudah diganti dengan alias "{alias}" untuk privasi). \
Ekstrak informasi berikut dan kembalikan HANYA JSON (tanpa teks lain) berbentuk:
{{
  "skills": ["<keterampilan 1>", "<keterampilan 2>", ...],
  "experience": [{{"role": "<posisi>", "company": "<jika ada, else null>", "duration": "<jika ada, else null>", "summary": "<ringkasan singkat>"}}],
  "qualifications": ["<kualifikasi/pendidikan 1>", ...]
}}

Teks CV:
{cv_text}"""


def parse_cv_text(cv_text: str, alias: str) -> dict:
    """Deepseek Flash -> structured {skills, experience, qualifications} from redacted CV text.

    cv_text MUST already be PII-redacted before calling this — this function does not redact.
    """
    prompt = _PARSE_PROMPT.format(alias=alias, cv_text=cv_text)
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
        logger.warning("parse_cv_text: failed to parse JSON, raw=%r", raw)
        return {"skills": [], "experience": [], "qualifications": []}

    if not isinstance(parsed, dict):
        return {"skills": [], "experience": [], "qualifications": []}

    return {
        "skills": parsed.get("skills", []) if isinstance(parsed.get("skills"), list) else [],
        "experience": parsed.get("experience", []) if isinstance(parsed.get("experience"), list) else [],
        "qualifications": (
            parsed.get("qualifications", []) if isinstance(parsed.get("qualifications"), list) else []
        ),
    }
