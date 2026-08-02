# Testing Retrieval-Augmented Generation Systems with Chunk Coverage (2607.18155)

Date read: 2026-08-02
Time spent:
Status: `reading`
Source date: 2026-07-20
Source link: https://arxiv.org/abs/2607.18155

## Production issue

Chunking and retriever changes can look good on a few hand-picked prompts while still leaving most of the corpus retrieval space untested.

## Core claim

Per-query RAG metrics miss a suite-level testing problem. Track which corpus chunks are ever retrieved, then use uncovered chunks to guide new test selection or generation.

## What I would implement

Log retrieved chunk IDs in Sprint 06 experiments, compute chunk coverage across the evaluation suite, and compare coverage-guided query expansion against ad hoc prompt additions.

## What would have to be true

The retriever must expose stable chunk identifiers, retrieval must matter for correctness, and I need either a reusable query pool or a cheap way to synthesize additional test queries.

## What I would measure

Whether coverage-guided testing finds distinct retrieval failures earlier than the current prompt set, and whether chunk coverage rises without exploding evaluation cost.

## Failure modes / reasons to reject

Coverage can reward boilerplate or intentionally irrelevant chunks, and higher coverage does not guarantee better answer quality. If the signal does not correlate with new failure discovery on my own corpus, it is ceremony.

## Verdict

`BORROW`

## What changes the verdict

Upgrade to `BUILD` if chunk coverage consistently exposes retrieval blind spots in Sprint 06. Downgrade to `PARK` if it mostly measures corpus exhaustiveness without changing decisions.
