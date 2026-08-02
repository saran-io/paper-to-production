# Reliability without Validity (2606.19544)

Date read: 2026-07-30 · Time spent: ~60m

## Claim

LLM-as-a-judge validation that reports only exact-match agreement systematically overstates discriminative ability. Use chance-corrected metrics (Cohen’s κ). Also measure consistency (replicates) and bias (position/order). High stability with high bias is a paradox, not a win. Distilled as MVVP.

## What would have to be true for this to help my system

- We have human labels on the same claim units the judge scores
- We can re-run ≥3 times at temperature 0 with cache disabled
- We adapt position bias to claim-order / context-order for Yes/No NLI-style verification

## What I'd measure

Headline: Cohen’s κ vs humans. Secondary: raw agreement (to show the gap), replicate stability, order-disagreement rate.

## Nuances

- κ can look “low” while still useful — report honestly
- Pairwise AB/BA position bias doesn’t map 1:1 to faithfulness; order audit is the adaptation
- A stable wrong judge is worse than a noisy one — paradox flag matters for CI gates

## Verdict

**BUILD** — MVVP-lite in `faithfulness audit`; κ is the Sprint 1 headline metric.

## If IGNORE: what would change my mind

—
