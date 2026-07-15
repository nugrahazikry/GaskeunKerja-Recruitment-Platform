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


_VOTES = 3  # self-consistency sample count — see score_answer() docstring


def _score_once(question: str, transcript: str, bypass_cache: bool) -> dict:
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


def _median_index(values: list[int]) -> int:
    """Index of the median value in a small odd-length list (ties broken toward the
    first occurrence) — used to pick one representative call's rationale/summary text
    rather than inventing a blended one."""
    sorted_pairs = sorted(range(len(values)), key=lambda i: values[i])
    return sorted_pairs[len(values) // 2]


def score_answer(question: str, transcript: str, bypass_cache: bool = False) -> dict:
    """Deepseek Pro, temperature=0 (enforced by chat_pro) -> rubric scores + summary.

    Self-consistency voting (added 2026-07-13, closes a real gap found during Area 5 QA
    T3): temperature=0 alone does not guarantee identical output on batched/distributed
    provider-side inference — measured directly, real ±1-point variance occurred across
    independent calls on an identical transcript. Calling the LLM _VOTES times per answer
    and taking the per-criterion MEDIAN is meaningfully more stable than trusting any
    single call, without fully eliminating variance (that would require control over the
    provider's serving infrastructure, which we don't have). The 2nd/3rd votes always
    bypass the cache — otherwise they'd just replay vote 1's cached response and defeat
    the entire purpose of voting.

    bypass_cache controls whether VOTE 1 hits the cache; votes 2-3 are always independent.
    """
    votes = [_score_once(question, transcript, bypass_cache=bypass_cache)]
    votes.extend(_score_once(question, transcript, bypass_cache=True) for _ in range(_VOTES - 1))

    clarity_values = [v["clarity"] for v in votes]
    relevance_values = [v["relevance"] for v in votes]
    depth_values = [v["technical_depth"] for v in votes]

    clarity_idx = _median_index(clarity_values)
    relevance_idx = _median_index(relevance_values)
    depth_idx = _median_index(depth_values)

    return {
        "clarity": sorted(clarity_values)[len(clarity_values) // 2],
        "clarity_rationale": votes[clarity_idx]["clarity_rationale"],
        "relevance": sorted(relevance_values)[len(relevance_values) // 2],
        "relevance_rationale": votes[relevance_idx]["relevance_rationale"],
        "technical_depth": sorted(depth_values)[len(depth_values) // 2],
        "technical_depth_rationale": votes[depth_idx]["technical_depth_rationale"],
        "summary": votes[clarity_idx]["summary"],
    }
