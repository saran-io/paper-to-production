"""Tests for MVVP-lite / agreement alignment."""

from faithfulness.models import ClaimVerdict, EvalExample
from faithfulness.mvvp import (
    agreement_on_example,
    align_human_predictions,
    order_bias_verify,
    replicate_evaluate,
    run_mvvp_audit,
)
from faithfulness.pipeline import build_evaluator


def test_align_exact_match():
    human = [
        ClaimVerdict(claim="A", supported=True),
        ClaimVerdict(claim="B", supported=False),
    ]
    pred = [
        ClaimVerdict(claim="B", supported=False),
        ClaimVerdict(claim="A", supported=True),
    ]
    y_true, y_pred = align_human_predictions(human, pred)
    assert y_true == [False, True]
    assert y_pred == [False, True]


def test_mvvp_audit_heuristic_smoke():
    examples = [
        EvalExample(
            id="t1",
            question="q",
            contexts=["Unit 4B is priced at ₹1.2 Cr. Pool access."],
            answer="Unit 4B is priced at ₹1.2 Cr. It has pool access.",
            human_claims=[
                ClaimVerdict(claim="Unit 4B is priced at ₹1.2 Cr.", supported=True),
                ClaimVerdict(claim="It has pool access.", supported=True),
            ],
        )
    ]
    report = run_mvvp_audit(examples, mode="heuristic", n_replicates=2)
    assert report.n_examples == 1
    assert report.agreement is not None
    assert "mean_pairwise_stability" in report.replicate_summary
    d = report.to_dict()
    assert d["mode"] == "heuristic"


def test_order_bias_and_replicate():
    ex = EvalExample(
        id="t2",
        question="q",
        contexts=["Unit 4B is a 2BHK priced at ₹1.2 Cr with pool access."],
        answer="Unit 4B is a 2BHK. Unit 4B is priced at ₹1.2 Cr. Unit 4B has a gym.",
        human_claims=[
            ClaimVerdict(claim="Unit 4B is a 2BHK.", supported=True),
            ClaimVerdict(claim="Unit 4B is priced at ₹1.2 Cr.", supported=True),
            ClaimVerdict(claim="Unit 4B has a gym.", supported=False),
        ],
    )
    ev = build_evaluator(mode="heuristic")
    results, summary = replicate_evaluate(ev, ex, n_runs=2)
    assert len(results) == 2
    assert summary["n_runs"] == 2
    bias = order_bias_verify(ev, ex)
    assert "disagreement_rate" in bias


def test_agreement_on_example():
    ex = EvalExample(
        id="t3",
        question="q",
        contexts=["Pool access is included."],
        answer="It includes pool access.",
        human_claims=[ClaimVerdict(claim="It includes pool access.", supported=True)],
    )
    result = build_evaluator(mode="heuristic").evaluate_example(ex)
    report = agreement_on_example(ex, result)
    assert report is not None
    assert report.n >= 1
