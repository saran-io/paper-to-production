"""CLI: fixtures, one-shot, MVVP audit, RAGAS compare."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from dotenv import load_dotenv

from costmeter import CostMeter
from faithfulness.compare_ragas import compare_to_ragas, write_comparison
from faithfulness.models import EvalExample
from faithfulness.mvvp import agreement_on_dataset, run_mvvp_audit
from faithfulness.pipeline import build_evaluator
from faithfulness.score import is_fully_faithful


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


def _default_seed() -> Path:
    return (
        _repo_root()
        / "instruments"
        / "datasets"
        / "faithfulness"
        / "fixtures"
        / "seed_cases.json"
    )


def _default_labelled() -> Path:
    return (
        _repo_root()
        / "instruments"
        / "datasets"
        / "faithfulness"
        / "fixtures"
        / "labelled_v1.json"
    )


def load_fixtures(path: Path) -> list[EvalExample]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        data = data.get("examples") or data.get("cases") or []
    return [EvalExample.model_validate(item) for item in data]


def cmd_eval_fixtures(args: argparse.Namespace) -> int:
    load_dotenv()
    examples = load_fixtures(Path(args.fixtures))
    meter = CostMeter(sprint="01-faithfulness")
    evaluator = build_evaluator(mode=args.mode, model=args.model, meter=meter)

    rows = []
    results = []
    regressions_failed = []

    for ex in examples:
        result = evaluator.evaluate_example(ex)
        results.append(result)
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
        if (
            args.check_expected
            and ex.expected_max_score is not None
            and result.score is not None
            and result.score > ex.expected_max_score
        ):
            regressions_failed.append(
                f"{ex.id}: score {result.score:.3f} > expected_max {ex.expected_max_score}"
            )

    agreement = agreement_on_dataset(examples, results)
    out = {
        "mode": args.mode,
        "n_examples": len(examples),
        "results": rows,
        "costmeter": meter.summary(),
        "agreement": None
        if agreement is None
        else {
            "n": agreement.n,
            "raw_agreement": agreement.raw_agreement,
            "cohens_kappa": agreement.cohens_kappa,
        },
        "regressions_failed": regressions_failed,
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    meter.dump_jsonl(out_path.with_suffix(".costmeter.jsonl"))
    print(f"Wrote {out_path}")
    if agreement:
        print(
            f"κ={agreement.cohens_kappa:.3f}  raw={agreement.raw_agreement:.3f}  n={agreement.n}"
        )

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


def cmd_audit(args: argparse.Namespace) -> int:
    load_dotenv()
    examples = load_fixtures(Path(args.fixtures))
    report = run_mvvp_audit(
        examples,
        mode=args.mode,
        model=args.model,
        n_replicates=args.replicates,
        max_examples=args.max_examples,
    )
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")
    print(f"Wrote {out_path}")
    if report.agreement:
        print(
            f"κ={report.agreement['cohens_kappa']:.3f}  "
            f"raw={report.agreement['raw_agreement']:.3f}  "
            f"n={report.agreement['n']}"
        )
    print(
        f"stability={report.replicate_summary['mean_pairwise_stability']:.3f}  "
        f"order_bias={report.order_bias_summary['mean_disagreement_rate']:.3f}  "
        f"paradox={report.paradox_flag}"
    )
    for note in report.notes:
        print(f"- {note}")
    return 1 if report.paradox_flag and args.fail_on_paradox else 0


def cmd_compare(args: argparse.Namespace) -> int:
    load_dotenv()
    examples = load_fixtures(Path(args.fixtures))
    if args.max_examples:
        examples = examples[: args.max_examples]
    report = compare_to_ragas(examples, mode=args.mode, model=args.model)
    out_path = Path(args.out)
    write_comparison(report, out_path)
    print(f"Wrote {out_path}")
    print(f"ragas_available={report['ragas_available']}")
    if report.get("agreement_vs_human"):
        a = report["agreement_vs_human"]
        print(f"κ vs human={a['cohens_kappa']:.3f}  raw={a['raw_agreement']:.3f}")
    if report.get("note"):
        print(report["note"])
    return 0


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Faithfulness evaluator (Build 01)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    results_dir = _repo_root() / "builds" / "01-faithfulness" / "results"

    p_fix = sub.add_parser("fixtures", help="Evaluate a fixtures JSON file")
    p_fix.add_argument("--mode", choices=["heuristic", "llm"], default="heuristic")
    p_fix.add_argument("--model", default="gpt-4o-mini")
    p_fix.add_argument("--fixtures", type=str, default=str(_default_seed()))
    p_fix.add_argument("--out", type=str, default=str(results_dir / "fixture_run.json"))
    p_fix.add_argument(
        "--check-expected",
        action="store_true",
        default=True,
        help="Fail if score exceeds expected_max_score (default on for seed CI)",
    )
    p_fix.add_argument(
        "--no-check-expected",
        action="store_false",
        dest="check_expected",
    )
    p_fix.set_defaults(func=cmd_eval_fixtures)

    p_one = sub.add_parser("one", help="Evaluate a single example")
    p_one.add_argument("--mode", choices=["heuristic", "llm"], default="heuristic")
    p_one.add_argument("--model", default="gpt-4o-mini")
    p_one.add_argument("--question", required=True)
    p_one.add_argument("--answer", required=True)
    p_one.add_argument("--context", dest="contexts", action="append", required=True)
    p_one.add_argument("--fail-if-faithful", action="store_true")
    p_one.set_defaults(func=cmd_eval_one)

    p_audit = sub.add_parser("audit", help="MVVP-lite judge audit (κ, replicates, order bias)")
    p_audit.add_argument("--mode", choices=["heuristic", "llm"], default="heuristic")
    p_audit.add_argument("--model", default="gpt-4o-mini")
    p_audit.add_argument("--fixtures", type=str, default=str(_default_labelled()))
    p_audit.add_argument("--replicates", type=int, default=3)
    p_audit.add_argument("--max-examples", type=int, default=None)
    p_audit.add_argument("--out", type=str, default=str(results_dir / "mvvp_audit.json"))
    p_audit.add_argument("--fail-on-paradox", action="store_true")
    p_audit.set_defaults(func=cmd_audit)

    p_cmp = sub.add_parser("compare", help="Compare our scores to RAGAS (if installed)")
    p_cmp.add_argument("--mode", choices=["heuristic", "llm"], default="heuristic")
    p_cmp.add_argument("--model", default="gpt-4o-mini")
    p_cmp.add_argument("--fixtures", type=str, default=str(_default_seed()))
    p_cmp.add_argument("--max-examples", type=int, default=None)
    p_cmp.add_argument("--out", type=str, default=str(results_dir / "ragas_compare.json"))
    p_cmp.set_defaults(func=cmd_compare)

    args = parser.parse_args(argv)
    raise SystemExit(args.func(args))


if __name__ == "__main__":
    main()
