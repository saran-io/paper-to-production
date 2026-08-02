"""End-to-end faithfulness pipeline with costmeter wiring."""

from __future__ import annotations

from typing import Literal

from costmeter import CostMeter

from faithfulness.decompose import Decomposer, HeuristicDecomposer, LLMDecomposer
from faithfulness.models import ClaimVerdict, EvalExample, FaithfulnessResult
from faithfulness.score import compute_faithfulness
from faithfulness.verify import HeuristicVerifier, LLMVerifier, Verifier


class FaithfulnessEvaluator:
    def __init__(
        self,
        decomposer: Decomposer | None = None,
        verifier: Verifier | None = None,
        *,
        meter: CostMeter | None = None,
        mode: Literal["heuristic", "llm", "scripted"] = "heuristic",
    ):
        self.decomposer = decomposer or HeuristicDecomposer()
        self.verifier = verifier or HeuristicVerifier()
        self.meter = meter or CostMeter(sprint="01-faithfulness")
        self.mode = mode

    def evaluate(
        self,
        question: str,
        contexts: list[str],
        answer: str,
        *,
        example_id: str | None = None,
    ) -> FaithfulnessResult:
        with self.meter.track(
            "faithfulness.decompose",
            model=getattr(self.decomposer, "model", None),
            provider="openai" if self.mode == "llm" else "local",
            metadata={"example_id": example_id},
        ) as dec_handle:
            claims = self.decomposer.decompose(question, answer)
            usage = getattr(self.decomposer, "last_usage", None)
            if usage:
                dec_handle["input_tokens"] = usage.get("input_tokens", 0)
                dec_handle["output_tokens"] = usage.get("output_tokens", 0)

        verdicts: list[ClaimVerdict] = []
        for claim in claims:
            with self.meter.track(
                "faithfulness.verify",
                model=getattr(self.verifier, "model", None),
                provider="openai" if self.mode == "llm" else "local",
                metadata={"example_id": example_id, "claim": claim.text},
            ) as ver_handle:
                verdict = self.verifier.verify(claim, contexts)
                usage = getattr(self.verifier, "last_usage", None)
                if usage:
                    ver_handle["input_tokens"] = usage.get("input_tokens", 0)
                    ver_handle["output_tokens"] = usage.get("output_tokens", 0)
            verdicts.append(verdict)

        score = compute_faithfulness(verdicts)
        return FaithfulnessResult(
            example_id=example_id,
            question=question,
            answer=answer,
            contexts=contexts,
            claims=verdicts,
            score=score,
            mode=self.mode,
            metadata={"n_claims": len(verdicts)},
        )

    def evaluate_example(self, example: EvalExample) -> FaithfulnessResult:
        return self.evaluate(
            example.question,
            example.contexts,
            example.answer,
            example_id=example.id,
        )


def build_evaluator(
    mode: Literal["heuristic", "llm"] = "heuristic",
    *,
    model: str = "gpt-4o-mini",
    meter: CostMeter | None = None,
) -> FaithfulnessEvaluator:
    meter = meter or CostMeter(sprint="01-faithfulness")
    if mode == "heuristic":
        return FaithfulnessEvaluator(
            HeuristicDecomposer(),
            HeuristicVerifier(),
            meter=meter,
            mode="heuristic",
        )
    try:
        from openai import OpenAI
    except ImportError as exc:  # pragma: no cover
        raise ImportError("Install llm extras: pip install '.[llm]'") from exc
    client = OpenAI()
    return FaithfulnessEvaluator(
        LLMDecomposer(client, model=model),
        LLMVerifier(client, model=model),
        meter=meter,
        mode="llm",
    )
