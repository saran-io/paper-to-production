"""Claim verification against retrieved context."""

from __future__ import annotations

import json
import re
from typing import Protocol

from faithfulness.models import Claim, ClaimVerdict

VERIFY_SYSTEM = """You check whether a claim can be inferred from the retrieved context only.
Rules:
- Yes only if the context supports the claim (paraphrase OK).
- No if missing, contradicted, or only true from world knowledge outside the context.
- Return JSON: {"supported": true|false, "rationale": "short reason"}
"""

VERIFY_USER = """Context:
{context}

Claim: {claim}

Is the claim supported by the context? JSON only."""


class Verifier(Protocol):
    def verify(self, claim: Claim, contexts: list[str]) -> ClaimVerdict: ...


def _normalize(text: str) -> str:
    text = text.lower()
    text = text.replace("₹", "rs ").replace("rs.", "rs ")
    text = re.sub(r"[^\w\s.]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _numbers(text: str) -> set[str]:
    # Extract before stripping dots so 1.8 stays intact
    lowered = text.lower().replace("₹", " ")
    return set(re.findall(r"\d+(?:\.\d+)?", lowered))


def _tokens(text: str) -> set[str]:
    stop = {
        "a",
        "an",
        "the",
        "is",
        "are",
        "was",
        "were",
        "has",
        "have",
        "with",
        "and",
        "of",
        "in",
        "to",
        "for",
        "on",
        "unit",
        "this",
        "that",
        "it",
    }
    return {t for t in _normalize(text).replace(".", " ").split() if t not in stop and len(t) > 1}


class HeuristicVerifier:
    """Lexical overlap verifier for CI/fixtures. Not a substitute for LLM NLI."""

    def __init__(self, min_overlap: float = 0.55):
        self.min_overlap = min_overlap

    def verify(self, claim: Claim, contexts: list[str]) -> ClaimVerdict:
        ctx_raw = "\n".join(contexts)
        ctx = _normalize(ctx_raw)
        claim_toks = _tokens(claim.text)
        if not claim_toks:
            return ClaimVerdict(
                claim=claim.text, supported=False, rationale="empty claim"
            )
        claim_nums = _numbers(claim.text)
        ctx_nums = _numbers(ctx_raw)
        missing_nums = claim_nums - ctx_nums
        if missing_nums:
            return ClaimVerdict(
                claim=claim.text,
                supported=False,
                rationale=f"numeric tokens not in context: {sorted(missing_nums)}",
            )

        present = {t for t in claim_toks if t in ctx.replace(".", " ")}
        overlap = len(present) / len(claim_toks)
        supported = overlap >= self.min_overlap
        return ClaimVerdict(
            claim=claim.text,
            supported=supported,
            rationale=f"token_overlap={overlap:.2f} present={sorted(present)}",
        )


class ScriptedVerifier:
    def __init__(self, mapping: dict[str, bool]):
        self.mapping = {k.strip().lower(): v for k, v in mapping.items()}

    def verify(self, claim: Claim, contexts: list[str]) -> ClaimVerdict:
        del contexts
        key = claim.text.strip().lower()
        if key not in self.mapping:
            raise KeyError(f"No scripted verdict for claim: {claim.text!r}")
        return ClaimVerdict(
            claim=claim.text,
            supported=self.mapping[key],
            rationale="scripted",
        )


class LLMVerifier:
    def __init__(self, client, model: str = "gpt-4o-mini", temperature: float = 0.0):
        self.client = client
        self.model = model
        self.temperature = temperature
        self.last_usage: dict[str, int] = {"input_tokens": 0, "output_tokens": 0}

    def verify(self, claim: Claim, contexts: list[str]) -> ClaimVerdict:
        context = "\n".join(contexts)
        resp = self.client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": VERIFY_SYSTEM},
                {
                    "role": "user",
                    "content": VERIFY_USER.format(context=context, claim=claim.text),
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
        supported = bool(data.get("supported"))
        if "supported" not in data and "verdict" in data:
            supported = str(data["verdict"]).strip().lower() in {"yes", "true", "y"}
        return ClaimVerdict(
            claim=claim.text,
            supported=supported,
            rationale=str(data.get("rationale") or data.get("explanation") or ""),
        )
