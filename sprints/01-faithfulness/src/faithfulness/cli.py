"""CLI: evaluate fixtures or a single example."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from dotenv import load_dotenv

from costmeter import CostMeter
from faithfulness.metrics import cohens_kappa
from faithfulness.models import ClaimVerdict, EvalExample
from faithfulness.pipeline import build_evaluator
from faithfulness.score import is_fully_faithful


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


def load_fixtures(path: Path) -> list[EvalExample]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        data = data.get("examples") or data.get("cases") or []
    return [EvalExample.model_validate(item) for item in data]


def cmd_eval_fixtures(args: argparse.Namespace) -> int:
    load_dotenv()
    fixtures_path = Path(args.fixtures)
    examples = load_fixtures(fixtures_path)
    meter = CostMeter(sprint="01-faithfulness")
    evaluator = build_evaluator(mode=args.mode, model=args.model, meter=meter)

    rows = []
    y_true: list[bool] = []
    y_pred: list[bool] = []
    regressions_failed = []

    for ex in examples:
        result = evaluator.evaluate_example(ex)
        rows.append(
            {
                "id": ex.id,
                "bucket": ex.bucket,
                "score": result.score,
                "n_claims": result.n_claims,
                "n_supported": result.n_supported,
                "claims": [c.model_dump() for c in result.claims],
            }
        )
        if ex.expected_max_score is not None and result.score is not None:
            if result.score > ex.expected_max_score:
                regressions_failed.append(
                    f"{ex.id}: score {result.score:.3f} > expected_max {ex.expected_max_score}"
                )
        if ex.human_claims:
            # Align by claim text where possible; else zip by order
            human_map = {h.claim.strip().lower(): h.supported for h in ex.human_claims}
            for pred in result.claims:
                key = pred.claim.strip().lower()
                if key in human_map:
                    y_true.append(human_map[key])
                    y_pred.append(pred.supported)

    summary = meter.summary()
    agreement = None
    if y_true:
        agreement = cohens_kappa(y_true, y_pred)

    out = {
        "mode": args.mode,
        "n_examples": len(examples),
        "results": rows,
        "costmeter": summary,
        "agreement": None
        if agreement is None
        else {
            "n": agreement.n,
            "raw_agreement": agreement.raw_agreement,
            "cohens_kappa": agreement.cohens_kappa,
        },
        "regressions_failed": regressions_failed,
    }

    out_path = Path(args.out) if args.out else None
    text = json.dumps(out, indent=2)
    if out_path:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text, encoding="utf-8")
        meter.dump_jsonl(out_path.with_suffix(".costmeter.jsonl"))
        print(f"Wrote {out_path}")
    else:
        print(text)

    if regressions_failed:
        print("REGRESSION FAILURES:", file=sys.stderr)
        for line in regressions_failed:
            print(f"  - {line}", file=sys.stderr)
        return 1
    return 0


def cmd_eval_one(args: argparse.Namespace) -> int:
    load_dotenv()
    meter = CostMeter(sprint="01-faithfulness")
    evaluator = build_evaluator(mode=args.mode, model=args.model, meter=meter)
    result = evaluator.evaluate(args.question, args.contexts, args.answer)
    print(result.model_dump_json(indent=2))
    print("costmeter:", json.dumps(meter.summary(), indent=2))
    if args.fail_if_faithful and is_fully_faithful(result.score):
        print("Expected non-faithful answer but score was 1.0", file=sys.stderr)
        return 1
    return 0


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Faithfulness evaluator (Sprint 01)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_fix = sub.add_parser("fixtures", help="Evaluate a fixtures JSON file")
    default_fixtures = (
        _repo_root()
        / "instruments"
        / "datasets"
        / "faithfulness"
        / "fixtures"
        / "seed_cases.json"
    )
    p_fix.add_argument(
        "--mode",
        choices=["heuristic", "llm"],
        default="heuristic",
        help="heuristic = CI-safe lexical baseline; llm = OpenAI decompose+verify",
    )
    p_fix.add_argument("--model", default="gpt-4o-mini")
    p_fix.add_argument("--fixtures", type=str, default=str(default_fixtures))
    p_fix.add_argument(
        "--out",
        type=str,
        default=str(
            _repo_root() / "sprints" / "01-faithfulness" / "results" / "fixture_run.json"
        ),
    )
    p_fix.set_defaults(func=cmd_eval_fixtures)

    p_one = sub.add_parser("one", help="Evaluate a single example")
    p_one.add_argument(
        "--mode",
        choices=["heuristic", "llm"],
        default="heuristic",
    )
    p_one.add_argument("--model", default="gpt-4o-mini")
    p_one.add_argument("--question", required=True)
    p_one.add_argument("--answer", required=True)
    p_one.add_argument(
        "--context",
        dest="contexts",
        action="append",
        required=True,
        help="Repeatable context passage",
    )
    p_one.add_argument(
        "--fail-if-faithful",
        action="store_true",
        help="Exit 1 if score is 1.0 (hallucination smoke)",
    )
    p_one.set_defaults(func=cmd_eval_one)

    args = parser.parse_args(argv)
    raise SystemExit(args.func(args))


if __name__ == "__main__":
    main()
