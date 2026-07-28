# RAGAS + FActScore (2309.15217 · 2305.14251)

Date read: 2026-07-28 · Time spent:

## Claim

RAGAS scores RAG faithfulness by decomposing an answer into statements and checking each against retrieved context (`|V|/|S|`), without needing reference answers. FActScore pushes the same idea further with finer atomic facts verified against a knowledge source (typically Wikipedia).

## What would have to be true for this to help my system

- Answers are claim-like (prices, amenities, facts) rather than pure dialogue filler.
- Retrieved context is the intended ground truth for “faithful,” not the open web.
- We can afford a second LLM pass (or cheaper verifier) per evaluation.
- We will calibrate against human labels — RAGAS alone does not prove validity.

## What I'd measure

Cohen's κ between automated claim-support labels and human labels on a domain set (~75+ cases). Secondary: raw agreement, cost/eval, p95 latency.

## Verdict

**BUILD** — faithfulness shaped like RAGAS; atomicity discipline from FActScore; judge audit from Reliability without Validity (next note / same sprint).

## If IGNORE: what would change my mind

—
