# FActScore (2305.14251)

Date read: 2026-07-30 · Time spent: ~45m

## Claim

Long-form factual precision should be scored at **atomic fact** granularity: split generations into one-fact units, then label each supported/unsupported against a knowledge source. Mixing facts in one sentence understates error rates.

## What would have to be true for this to help my system

- We apply atomicity to **RAG context** checking (not Wikipedia biographies)
- Decomposition is strict: no “2BHK and gym” mega-claims
- Human labels use the same atomic unit

## What I'd measure

Hallucination catch-rate on partial errors (wrong BHK inside an otherwise correct sentence) before vs after atomic decomposition.

## Nuances

- FActScore’s knowledge source is Wikipedia; ours is retrieved listing text
- Over-splitting creates noisy κ; under-splitting hides bugs — listing domain needs a style guide
- Length penalty in FActScore is less relevant for short voice answers

## Verdict

**BORROW** — atomicity discipline and decompose prompts; not the Wikipedia retrieval stack.

## If IGNORE: what would change my mind

—
