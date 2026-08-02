"""Atomic claim decomposition.

Heuristic path is CI-safe. LLM path follows RAGAS/FActScore prompting.
Sprint rule: treat decompose prompts as the craft you own — iterate by hand.
"""

from __future__ import annotations

import json
import re
from typing import Protocol

from faithfulness.models import Claim

DECOMPOSE_SYSTEM = """You extract atomic factual claims from answers about property listings.
Rules:
- Each claim is ONE independent fact (price, BHK, amenity, location, size, etc.).
- Do not merge two facts with "and".
- Do not invent facts that are not in the answer.
- Skip pure pleasantries ("Happy to help").
- Return JSON: {"claims": ["...", "..."]}
"""

DECOMPOSE_USER = """Question: {question}

Answer: {answer}

Extract atomic claims as JSON."""


class Decomposer(Protocol):
    def decompose(self, question: str, answer: str) -> list[Claim]: ...


_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+|\n+")
_AND_SPLIT = re.compile(r"\s+and\s+", re.IGNORECASE)


def _clean(s: str) -> str:
    s = s.strip().strip("-•* ").strip()
    s = re.sub(r"\s+", " ", s)
    return s


def _split_conjunctions(sentence: str) -> list[str]:
    """Split mild 'and' conjunctions when both sides look like short facts."""
    sentence = _clean(sentence)
    if not sentence:
        return []
    # Avoid splitting "1 and 2 BHK" style — only split if both sides have content words
    parts = _AND_SPLIT.split(sentence)
    if len(parts) == 1:
        return [sentence]
    if all(len(p.split()) <= 12 for p in parts) and all(p.strip() for p in parts):
        # Keep subject on later parts when pattern is "X is A and B"
        m = re.match(
            r"^(?P<sub>.+?\b(?:is|has|includes|offers|features|contains)\b)\s+(?P<rest>.+)$",
            sentence,
            re.IGNORECASE,
        )
        if m and len(parts) == 2:
            subj = m.group("sub").strip()
            # "Unit 4B is 2BHK and has a gym" already handled poorly — fall back to raw parts
            return [_clean(p) for p in parts if _clean(p)]
        return [_clean(p) for p in parts if _clean(p)]
    return [sentence]


class HeuristicDecomposer:
    """Deterministic decomposer for fixtures/CI. Prefer LLMDecomposer for real eval."""

    def decompose(self, question: str, answer: str) -> list[Claim]:
        del question  # RAGAS includes question for context; heuristic ignores
        answer = answer.strip()
        if not answer:
            return []
        claims: list[Claim] = []
        for sentence in _SENTENCE_SPLIT.split(answer):
            sentence = _clean(sentence)
            if not sentence:
                continue
            # Drop soft filler
            if re.fullmatch(r"(sure|ok|okay|happy to help|of course)[.!]?", sentence, re.I):
                continue
            for piece in _split_conjunctions(sentence):
                if piece and piece not in {c.text for c in claims}:
                    claims.append(Claim(text=piece))
        return claims


class ScriptedDecomposer:
    """Returns predetermined claims for a given answer fingerprint (tests)."""

    def __init__(self, mapping: dict[str, list[str]]):
        self.mapping = mapping

    def decompose(self, question: str, answer: str) -> list[Claim]:
        del question
        key = answer.strip()
        if key not in self.mapping:
            raise KeyError(f"No scripted claims for answer: {key!r}")
        return [Claim(text=c) for c in self.mapping[key]]


class LLMDecomposer:
    def __init__(self, client, model: str = "gpt-4o-mini", temperature: float = 0.0):
        self.client = client
        self.model = model
        self.temperature = temperature
        self.last_usage: dict[str, int] = {"input_tokens": 0, "output_tokens": 0}

    def decompose(self, question: str, answer: str) -> list[Claim]:
        if not answer.strip():
            return []
        resp = self.client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": DECOMPOSE_SYSTEM},
                {
                    "role": "user",
                    "content": DECOMPOSE_USER.format(question=question, answer=answer),
                },
            ],
        )
        usage = getattr(resp, "usage", None)
        if usage:
            self.last_usage = {
                "input_tokens": int(getattr(usage, "prompt_tokens", 0) or 0),
                "output_tokens": int(getattr(usage, "completion_tokens", 0) or 0),
            }
        content = resp.choices[0].message.content or "{}"
        data = json.loads(content)
        raw = data.get("claims") or data.get("statements") or []
        return [Claim(text=_clean(str(c))) for c in raw if _clean(str(c))]
