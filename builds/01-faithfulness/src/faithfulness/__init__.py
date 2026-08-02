"""Faithfulness evaluator (RAGAS-shaped): decompose → verify → score."""

from faithfulness.mvvp import run_mvvp_audit
from faithfulness.pipeline import FaithfulnessEvaluator, FaithfulnessResult
from faithfulness.score import compute_faithfulness

__all__ = [
    "FaithfulnessEvaluator",
    "FaithfulnessResult",
    "compute_faithfulness",
    "run_mvvp_audit",
]
