"""Round-3 Task 20: ordinal education-level comparison, used to derive a pass/fail eligibility
flag — kept entirely separate from the numeric match score, per the confirmed decision."""

_LEVEL_RANK = {"SMA": 0, "SMK": 0, "D3": 1, "S1": 2, "S2": 3, "S3": 4}


def meets_education(candidate_level: str | None, required_level: str | None) -> bool | None:
    """None means "not evaluable" (no requirement set, or candidate's level unknown) — the
    caller should render a neutral state, not a fail, for that case."""
    if not required_level:
        return None
    if not candidate_level:
        return None
    return _LEVEL_RANK.get(candidate_level, -1) >= _LEVEL_RANK.get(required_level, 999)
