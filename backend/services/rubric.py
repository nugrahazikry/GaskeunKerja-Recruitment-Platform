import json
import logging

from services import llm_client
from services.rubric_data import RUBRIC_CRITERIA

logger = logging.getLogger("rubric")

_SCORING_PROMPT = """\
Anda adalah recruiter yang menilai jawaban wawancara kandidat berikut, terhadap pertanyaan yang diberikan.

Pertanyaan: {question}
Jawaban (transkrip): {transcript}

Nilai jawaban ini pada 3 kriteria berikut, masing-masing skala 1-5:

{criteria_descriptions}

Kembalikan HANYA JSON: {{"clarity": <1-5>, "clarity_rationale": "<alasan singkat>", \
"relevance": <1-5>, "relevance_rationale": "<alasan singkat>", \
"technical_depth": <1-5>, "technical_depth_rationale": "<alasan singkat>", \
"summary": "<ringkasan poin-poin utama jawaban, 2-3 kalimat, untuk recruiter>"}}"""


def _build_criteria_text() -> str:
    parts = []
    for key, criterion in RUBRIC_CRITERIA.items():
        levels = "\n".join(f"  {lvl}: {desc}" for lvl, desc in criterion["levels"].items())
        parts.append(f"{criterion['name']}:\n{levels}")
    return "\n\n".join(parts)


def score_answer(question: str, transcript: str, bypass_cache: bool = False) -> dict:
    """Deepseek Pro, temperature=0 (enforced by chat_pro) -> rubric scores + summary.

    bypass_cache is exposed for Area 5 QA T3 (determinism test) — a test that hits the
    Area 4 disk cache after its first call would just replay the same response and prove
    nothing about the LLM's actual determinism.
    """
    prompt = _SCORING_PROMPT.format(
        question=question, transcript=transcript, criteria_descriptions=_build_criteria_text()
    )
    raw = llm_client.chat_pro([{"role": "user", "content": prompt}], bypass_cache=bypass_cache)

    text = raw.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        logger.warning("score_answer: failed to parse JSON, raw=%r", raw)
        parsed = {}

    def _clamp_score(value) -> int:
        try:
            v = int(value)
        except (TypeError, ValueError):
            return 1
        return max(1, min(5, v))

    return {
        "clarity": _clamp_score(parsed.get("clarity")),
        "clarity_rationale": parsed.get("clarity_rationale", ""),
        "relevance": _clamp_score(parsed.get("relevance")),
        "relevance_rationale": parsed.get("relevance_rationale", ""),
        "technical_depth": _clamp_score(parsed.get("technical_depth")),
        "technical_depth_rationale": parsed.get("technical_depth_rationale", ""),
        "summary": parsed.get("summary", ""),
    }
