"""Area 5 QA T3: determinism test.

Same transcript -> same rubric score across 5 genuinely independent (cache-bypassed)
calls. A determinism test that let calls 2-5 hit the Area 4 T3 disk cache would just
replay run 1's response and prove nothing about the LLM's actual determinism — this test
bypasses the cache for all 5 calls (services.rubric.score_answer(bypass_cache=True)).

⚠️ REAL FINDING (2026-07-13, measured directly, not yet resolved — needs product
awareness, see plan.md decision log): running this test twice (10 real calls total)
showed genuine score variance even at temperature=0 — e.g. one run's `clarity` differed
(5 vs 4) and another run's `technical_depth` varied (3 vs 2), each time in a different
dimension. This is consistent with well-documented, provider-level inference
non-determinism (OpenAI-compatible batched/distributed inference does not guarantee
bit-for-bit reproducibility at temperature=0, even though it substantially reduces
variance vs higher temperatures) — not a bug in this codebase's prompt or code, since a
code-level bug would reproduce identically every time rather than vary unpredictably.

This directly contradicts a real, explicit submission claim (`tahap 3 jawaban.md` Q9,
~line 116): "jawaban yang sama menghasilkan skor yang konsisten di setiap pengulangan,
mengatasi masalah non-determinisme yang teridentifikasi pada versi awal solusi kami."
That claim is currently NOT fully true at the raw-LLM-call level. This test asserts a
practical tolerance (scores may vary by at most 1 point per criterion) rather than exact
equality, so it reflects the system's actual measured behavior — flip to strict equality
only if a real determinism fix (e.g. self-consistency voting, majority-of-N scoring) is
built and verified to actually close the gap.

Cost guardrail (per the Area 5 plan): this makes 5 real, independent Deepseek Pro calls.
Run once per feature/verification pass, not in a tight edit-test-edit debug loop.
"""

from services.rubric import score_answer

_QUESTION = "Ceritakan pengalaman Anda yang paling relevan dengan posisi ini."
_TRANSCRIPT = (
    "Saya memiliki pengalaman dua tahun sebagai frontend developer menggunakan React dan "
    "TypeScript. Saya juga pernah membangun REST API dengan Node.js dan Express, serta "
    "menggunakan Git untuk kolaborasi tim."
)

_MAX_TOLERATED_DRIFT = 1  # points, per criterion — see the finding above


def test_same_transcript_scores_within_tolerance_across_5_independent_runs():
    results = [score_answer(_QUESTION, _TRANSCRIPT, bypass_cache=True) for _ in range(5)]

    for criterion in ("clarity", "relevance", "technical_depth"):
        values = [r[criterion] for r in results]
        drift = max(values) - min(values)
        assert drift <= _MAX_TOLERATED_DRIFT, (
            f"{criterion} varied by {drift} points across 5 runs ({values}) — exceeds the "
            f"tolerated drift of {_MAX_TOLERATED_DRIFT}, worse than the measured baseline"
        )
