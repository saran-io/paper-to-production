"""Optional comparison against the RAGAS library faithfulness metric.

RAGAS paper shape: decompose → verify vs context → |V|/|S|.
This module runs *our* evaluator and, when `ragas` is installed, the library
on the same fixtures for a delta table.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from costmeter import CostMeter
from faithfulness.models import EvalExample
from faithfulness.mvvp import agreement_on_dataset
from faithfulness.pipeline import build_evaluator


def _try_ragas_scores(examples: list[EvalExample]) -> list[dict[str, Any]] | None:
    try:
        from datasets import Dataset
        from ragas import evaluate
        from ragas.metrics import faithfulness
    except ImportError:
        return None

    rows = {
        "question": [e.question for e in examples],
        "answer": [e.answer for e in examples],
        "contexts": [e.contexts for e in examples],
    }
    ds = Dataset.from_dict(rows)
    result = evaluate(ds, metrics=[faithfulness])
    # ragas returns scores per row under 'faithfulness'
    scores = result["faithfulness"]
    out = []
    for ex, score in zip(examples, scores, strict=False):
        out.append({"id": ex.id, "ragas_faithfulness": float(score) if score == score else None})
    return out


def compare_to_ragas(
    examples: list[EvalExample],
    *,
    mode: str = "heuristic",
    model: str = "gpt-4o-mini",
) -> dict[str, Any]:
    meter = CostMeter(sprint="01-faithfulness")
    evaluator = build_evaluator(mode=mode, model=model, meter=meter)  # type: ignore[arg-type]

    ours = []
    results = []
    for ex in examples:
        r = evaluator.evaluate_example(ex)
        results.append(r)
        ours.append(
            {
                "id": ex.id,
                "our_score": r.score,
                "n_claims": r.n_claims,
                "n_supported": r.n_supported,
            }
        )

    ragas_rows = _try_ragas_scores(examples)
    agreement = agreement_on_dataset(examples, results)

    merged = []
    ragas_by_id = {r["id"]: r for r in (ragas_rows or [])}
    for row in ours:
        item = dict(row)
        if row["id"] in ragas_by_id:
            item["ragas_faithfulness"] = ragas_by_id[row["id"]]["ragas_faithfulness"]
            if row["our_score"] is not None and item["ragas_faithfulness"] is not None:
                item["delta_our_minus_ragas"] = row["our_score"] - item["ragas_faithfulness"]
        merged.append(item)

    return {
        "mode": mode,
        "n_examples": len(examples),
        "ragas_available": ragas_rows is not None,
        "note": None
        if ragas_rows is not None
        else "Install optional deps: pip install '.[ragas]' (and set OPENAI_API_KEY)",
        "agreement_vs_human": None
        if agreement is None
        else {
            "n": agreement.n,
            "raw_agreement": agreement.raw_agreement,
            "cohens_kappa": agreement.cohens_kappa,
        },
        "rows": merged,
        "costmeter": meter.summary(),
    }


def write_comparison(report: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
