"""Faithfulness evaluator (RAGAS-shaped): decompose → verify → score."""

from faithfulness.pipeline import FaithfulnessEvaluator, FaithfulnessResult
from faithfulness.score import compute_faithfulness

__all__ = ["FaithfulnessEvaluator", "FaithfulnessResult", "compute_faithfulness"]
