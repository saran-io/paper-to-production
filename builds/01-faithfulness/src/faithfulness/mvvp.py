"""MVVP-lite: Reliability without Validity applied to faithfulness judges.

Minimum Viable Validation Protocol (adapted from arXiv:2606.19544):
1. Chance-correct — Cohen's κ as headline (not raw agreement)
2. Replicate — ≥3 runs at temperature 0
3. Order audit — claim-order / context-order sensitivity for Yes/No verification
4. Report paradox — high stability + high bias is a failure mode
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Literal

from costmeter import CostMeter
from faithfulness.metrics import AgreementReport, cohens_kappa
from faithfulness.models import Claim, ClaimVerdict, EvalExample, FaithfulnessResult
from faithfulness.pipeline import FaithfulnessEvaluator, build_evaluator
from faithfulness.score import compute_faithfulness


def align_human_predictions(
    human: list[ClaimVerdict],
    predicted: list[ClaimVerdict],
) -> tuple[list[bool], list[bool]]:
    """Align human and model claim labels for κ.

    Prefer exact claim-text match; fall back to positional zip for leftovers.
    """
    y_true: list[bool] = []
    y_pred: list[bool] = []
    human_map = {h.claim.strip().lower(): h.supported for h in human}
    used_humans: set[str] = set()

    for pred in predicted:
        key = pred.claim.strip().lower()
        if key in human_map:
            y_true.append(human_map[key])
            y_pred.append(pred.supported)
            used_humans.add(key)

    # Positional fallback for unmatched predicted claims
    remaining_h = [h for h in human if h.claim.strip().lower() not in used_humans]
    remaining_p = [
        p for p in predicted if p.claim.strip().lower() not in used_humans
    ]
    for h, p in zip(remaining_h, remaining_p, strict=False):
        y_true.append(h.supported)
        y_pred.append(p.supported)

    return y_true, y_pred


def agreement_on_example(
    example: EvalExample, result: FaithfulnessResult
) -> AgreementReport | None:
    if not example.human_claims:
        return None
    y_true, y_pred = align_human_predictions(example.human_claims, result.claims)
    if not y_true:
        return None
    return cohens_kappa(y_true, y_pred)


def agreement_on_dataset(
    examples: list[EvalExample], results: list[FaithfulnessResult]
) -> AgreementReport | None:
    y_true: list[bool] = []
    y_pred: list[bool] = []
    by_id = {r.example_id: r for r in results}
    for ex in examples:
        result = by_id.get(ex.id)
        if not result or not ex.human_claims:
            continue
        t, p = align_human_predictions(ex.human_claims, result.claims)
        y_true.extend(t)
        y_pred.extend(p)
    if not y_true:
        return None
    return cohens_kappa(y_true, y_pred)


@dataclass
class ReplicateReport:
    n_runs: int
    pairwise_exact_match_mean: float
    score_stdev: float | None
    per_example: list[dict[str, Any]]


def _pairwise_exact_match(runs: list[list[ClaimVerdict]]) -> float:
    if len(runs) < 2:
        return 1.0
    matches = 0
    total = 0
    for i in range(len(runs)):
        for j in range(i + 1, len(runs)):
            a, b = runs[i], runs[j]
            n = min(len(a), len(b))
            for k in range(n):
                total += 1
                if a[k].supported == b[k].supported and a[k].claim.strip().lower() == b[
                    k
                ].claim.strip().lower():
                    matches += 1
            # length mismatch counts against stability
            total += abs(len(a) - len(b))
    return matches / total if total else 1.0


def replicate_evaluate(
    evaluator: FaithfulnessEvaluator,
    example: EvalExample,
    n_runs: int = 3,
) -> tuple[list[FaithfulnessResult], dict[str, Any]]:
    """Run the same example n times (MVVP replicate step)."""
    results = [evaluator.evaluate_example(example) for _ in range(n_runs)]
    scores = [r.score for r in results if r.score is not None]
    stdev = None
    if len(scores) >= 2:
        mean = sum(scores) / len(scores)
        stdev = (sum((s - mean) ** 2 for s in scores) / (len(scores) - 1)) ** 0.5
    stability = _pairwise_exact_match([r.claims for r in results])
    return results, {
        "example_id": example.id,
        "n_runs": n_runs,
        "scores": scores,
        "score_stdev": stdev,
        "pairwise_claim_stability": stability,
    }


def order_bias_verify(
    evaluator: FaithfulnessEvaluator,
    example: EvalExample,
) -> dict[str, Any]:
    """Adapted position/order audit for claim verification.

    Verifies claims in forward order vs reversed order; reports disagreement rate.
    Decomposition is held fixed from the first pass when possible.
    """
    first = evaluator.evaluate_example(example)
    claims = [Claim(text=c.claim) for c in first.claims]
    if len(claims) < 2:
        return {
            "example_id": example.id,
            "n_claims": len(claims),
            "disagreement_rate": 0.0,
            "note": "need ≥2 claims for order audit",
        }

    forward = [evaluator.verifier.verify(c, example.contexts) for c in claims]
    reversed_claims = list(reversed(claims))
    backward = [evaluator.verifier.verify(c, example.contexts) for c in reversed_claims]
    # map backward back to original order
    backward_by_text = {b.claim.strip().lower(): b.supported for b in backward}
    disagree = 0
    for f in forward:
        key = f.claim.strip().lower()
        if key in backward_by_text and backward_by_text[key] != f.supported:
            disagree += 1
    rate = disagree / len(forward) if forward else 0.0
    return {
        "example_id": example.id,
        "n_claims": len(forward),
        "disagreement_rate": rate,
        "forward_supported": sum(1 for f in forward if f.supported),
        "backward_supported": sum(1 for b in backward if b.supported),
    }


@dataclass
class MVVPReport:
    mode: str
    n_examples: int
    agreement: dict[str, Any] | None
    replicate_summary: dict[str, Any]
    order_bias_summary: dict[str, Any]
    paradox_flag: bool
    notes: list[str]
    costmeter: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def run_mvvp_audit(
    examples: list[EvalExample],
    *,
    mode: Literal["heuristic", "llm"] = "heuristic",
    model: str = "gpt-4o-mini",
    n_replicates: int = 3,
    max_examples: int | None = None,
) -> MVVPReport:
    """Run MVVP-lite across a labelled fixture set."""
    subset = examples[:max_examples] if max_examples else examples
    meter = CostMeter(sprint="01-faithfulness")
    evaluator = build_evaluator(mode=mode, model=model, meter=meter)

    results: list[FaithfulnessResult] = []
    replicate_rows: list[dict[str, Any]] = []
    order_rows: list[dict[str, Any]] = []

    for ex in subset:
        primary = evaluator.evaluate_example(ex)
        results.append(primary)

        _, rep = replicate_evaluate(evaluator, ex, n_runs=n_replicates)
        replicate_rows.append(rep)
        order_rows.append(order_bias_verify(evaluator, ex))

    agreement = agreement_on_dataset(subset, results)
    stab_vals = [r["pairwise_claim_stability"] for r in replicate_rows]
    bias_vals = [r["disagreement_rate"] for r in order_rows]
    mean_stab = sum(stab_vals) / len(stab_vals) if stab_vals else 0.0
    mean_bias = sum(bias_vals) / len(bias_vals) if bias_vals else 0.0

    # Paradox: very stable but order-sensitive (adapted thresholds from paper spirit)
    paradox = mean_stab > 0.95 and mean_bias > 0.10

    notes = [
        "Headline metric is Cohen's κ when human_claims are present.",
        "Order bias adapted from pairwise position bias for Yes/No claim verification.",
    ]
    if paradox:
        notes.append(
            "PARADOX: high replicate stability with material order disagreement — "
            "do not claim the judge is reliable yet."
        )
    if agreement is None:
        notes.append("No human_claims aligned — κ not computed.")

    return MVVPReport(
        mode=mode,
        n_examples=len(subset),
        agreement=None
        if agreement is None
        else {
            "n": agreement.n,
            "raw_agreement": agreement.raw_agreement,
            "cohens_kappa": agreement.cohens_kappa,
        },
        replicate_summary={
            "n_replicates": n_replicates,
            "mean_pairwise_stability": mean_stab,
            "per_example": replicate_rows,
        },
        order_bias_summary={
            "mean_disagreement_rate": mean_bias,
            "per_example": order_rows,
        },
        paradox_flag=paradox,
        notes=notes,
        costmeter=meter.summary(),
    )


def score_from_human_claims(human: list[ClaimVerdict]) -> float | None:
    """Oracle faithfulness if humans labelled every claim in the answer."""
    return compute_faithfulness(human)
