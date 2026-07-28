"""Faithfulness score: |V| / |S|."""

from __future__ import annotations

import math

from faithfulness.models import ClaimVerdict


def compute_faithfulness(verdicts: list[ClaimVerdict]) -> float | None:
    """Return supported/total, or None when there are no claims (RAGAS-like NaN case)."""
    if not verdicts:
        return None
    supported = sum(1 for v in verdicts if v.supported)
    return supported / len(verdicts)


def is_fully_faithful(score: float | None, *, eps: float = 1e-9) -> bool:
    if score is None or (isinstance(score, float) and math.isnan(score)):
        return False
    return score >= 1.0 - eps
