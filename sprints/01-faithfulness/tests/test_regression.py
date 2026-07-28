"""Pipeline + ADR regression: hallucination must not score fully faithful."""

import json
from pathlib import Path

import pytest

from costmeter import CostMeter
from faithfulness.decompose import ScriptedDecomposer
from faithfulness.models import EvalExample
from faithfulness.pipeline import FaithfulnessEvaluator, build_evaluator
from faithfulness.score import is_fully_faithful
from faithfulness.verify import ScriptedVerifier

ROOT = Path(__file__).resolve().parents[3]
FIXTURES = (
    ROOT
    / "instruments"
    / "datasets"
    / "faithfulness"
    / "fixtures"
    / "seed_cases.json"
)


def _load_examples() -> list[EvalExample]:
    data = json.loads(FIXTURES.read_text(encoding="utf-8"))
    return [EvalExample.model_validate(x) for x in data["examples"]]


def test_hallucination_regression_scripted():
    """Known bad answer with scripted claim verdicts must not be fully faithful."""
    decomposer = ScriptedDecomposer(
        {
            "Unit 4B is priced at ₹1.8 Cr and includes a gym.": [
                "Unit 4B is priced at ₹1.8 Cr",
                "Unit 4B includes a gym.",
            ]
        }
    )
    verifier = ScriptedVerifier(
        {
            "Unit 4B is priced at ₹1.8 Cr": False,
            "Unit 4B includes a gym.": False,
        }
    )
    meter = CostMeter(sprint="01-faithfulness")
    ev = FaithfulnessEvaluator(
        decomposer, verifier, meter=meter, mode="scripted"
    )
    result = ev.evaluate(
        question="What is the price of unit 4B?",
        contexts=[
            "Unit 4B is a 2BHK apartment priced at ₹1.2 Cr. It includes pool access."
        ],
        answer="Unit 4B is priced at ₹1.8 Cr and includes a gym.",
        example_id="hallucination_wrong_price",
    )
    assert result.score == 0.0
    assert not is_fully_faithful(result.score)
    assert meter.summary()["n_events"] >= 3  # 1 decompose + 2 verify


def test_merged_properties_scripted_partial():
    """Entity-binding mix: 1/3 claims supported → not fully faithful."""
    answer = (
        "Unit 4B is a 3BHK. Unit 4B is priced at ₹1.2 Cr. Unit 4B has a private gym."
    )
    decomposer = ScriptedDecomposer(
        {
            answer: [
                "Unit 4B is a 3BHK.",
                "Unit 4B is priced at ₹1.2 Cr.",
                "Unit 4B has a private gym.",
            ]
        }
    )
    verifier = ScriptedVerifier(
        {
            "Unit 4B is a 3BHK.": False,
            "Unit 4B is priced at ₹1.2 Cr.": True,
            "Unit 4B has a private gym.": False,
        }
    )
    result = FaithfulnessEvaluator(
        decomposer, verifier, mode="scripted"
    ).evaluate("Summarize unit 4B.", ["Unit 4B is a 2BHK priced at ₹1.2 Cr."], answer)
    assert result.score == pytest.approx(1 / 3)
    assert not is_fully_faithful(result.score)


def test_hallucination_regression_heuristic_fixture():
    examples = {e.id: e for e in _load_examples()}
    ex = examples["hallucination_wrong_price"]
    ev = build_evaluator(mode="heuristic")
    result = ev.evaluate_example(ex)
    assert result.score is not None
    assert result.score <= ex.expected_max_score
    assert not is_fully_faithful(result.score)


@pytest.mark.parametrize(
    "example_id",
    [
        "hallucination_wrong_price",
        "correct_but_unsupported",
        "contradictory_bhk",
        "empty_retrieval",
        "merged_two_properties",
    ],
)
def test_expected_max_score_fixtures(example_id: str):
    examples = {e.id: e for e in _load_examples()}
    ex = examples[example_id]
    ev = build_evaluator(mode="heuristic")
    result = ev.evaluate_example(ex)
    assert result.score is not None
    assert ex.expected_max_score is not None
    assert result.score <= ex.expected_max_score + 1e-9


def test_fully_supported_not_zero():
    examples = {e.id: e for e in _load_examples()}
    ex = examples["fully_supported_4b"]
    ev = build_evaluator(mode="heuristic")
    result = ev.evaluate_example(ex)
    assert result.score is not None
    assert result.score >= 0.66


def test_costmeter_records_operations():
    meter = CostMeter(sprint="01-faithfulness")
    ev = build_evaluator(mode="heuristic", meter=meter)
    ev.evaluate("q", ["ctx has pool"], "It has a pool.")
    ops = {e.operation for e in meter.events}
    assert "faithfulness.decompose" in ops
    assert "faithfulness.verify" in ops
    summary = meter.summary()
    assert summary["n_events"] >= 2
    assert "latency_ms_p50" in summary
