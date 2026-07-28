"""Core data models for faithfulness evaluation."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class Claim(BaseModel):
    text: str
    supported: bool | None = None
    rationale: str | None = None


class ClaimVerdict(BaseModel):
    claim: str
    supported: bool
    rationale: str | None = None


class EvalExample(BaseModel):
    """One (question, contexts, answer) case, optionally with human labels."""

    id: str
    question: str
    contexts: list[str]
    answer: str
    bucket: str | None = None
    # Human labels at claim level (optional). If provided, used for κ.
    human_claims: list[ClaimVerdict] | None = None
    # Expected answer-level score band for fixtures (optional).
    expected_max_score: float | None = None
    notes: str | None = None


class FaithfulnessResult(BaseModel):
    example_id: str | None = None
    question: str
    answer: str
    contexts: list[str]
    claims: list[ClaimVerdict]
    score: float | None
    mode: Literal["heuristic", "llm", "scripted"] = "heuristic"
    error: str | None = None
    metadata: dict = Field(default_factory=dict)

    @property
    def n_claims(self) -> int:
        return len(self.claims)

    @property
    def n_supported(self) -> int:
        return sum(1 for c in self.claims if c.supported)
