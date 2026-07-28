# Content plan — Sprint 01 Faithfulness

**Publish:** Tue 4 Aug 2026  
**Blog:** `saran.build/paper-to-production/faithfulness-from-scratch`  
**Working title:** My RAG scored 0.91 faithfulness. The real number was closer to 0.67.

## Thesis (one line)

You can implement RAGAS-style faithfulness in a weekend; you cannot trust the score until you run a judge audit and report chance-corrected agreement with humans.

## Surfaces

| Surface | When (IST) | Job |
|---|---|---|
| Blog | Tue 5:30pm | Canonical method + all numbers + ADR + limitations |
| X thread | Tue 6:30pm | Result-first; link only in last post |
| LinkedIn | Wed 8:30am | Judgment frame, not implementation tour |

---

## Blog outline

1. **Open with the gap** — e.g. 0.91 → ~0.67 (replace with measured numbers). Not “I implemented RAGAS.”
2. **Why faithfulness** — grounded answers for listing/voice RAG; hallucination ≠ bad retrieval.
3. **What the papers say**
   - RAGAS: extract statements → verify vs context → `|V|/|S|`
   - FActScore: atomicity bar for decomposition
   - Reliability without Validity: exact match lies; κ + MVVP
4. **Build** — pipeline diagram; 1–2 decomposition examples (good vs too-coarse).
5. **Test set** — buckets: fully supported · partially supported · contradictory · correct-but-unsupported · poor-retrieval · wrong price/feature · facts merged across two properties · empty retrieval.
6. **Results** — κ, raw agreement, RAGAS delta, cost, p50/p95.
7. **Judge audit** — what inflated the score (claim merge? Yes-bias? cache?).
8. **When I would not use this** — required closing section.
9. **ADR-001** embed + next sprint teaser (endpointing).

### Required closing

> **When I would not use this:** …

---

## X thread (8–10 posts)

| # | Beat |
|---|---|
| 1 | Result hook: score vs human/κ gap. **No link.** |
| 2 | Faithfulness in one sentence + formula |
| 3 | Image: decompose → verify → score |
| 4 | One bad decomposition that inflated the score |
| 5 | Chart: raw agreement vs κ |
| 6 | RAGAS vs mine on the same cases |
| 7 | Cost / latency per eval |
| 8 | **When I would not use this** |
| 9 | Blog link (last post only) |

**Timing:** Tue 6:30pm IST (= 9am ET).

### Draft hooks (pick one after numbers land)

- “My RAG system scored 0.91 faithfulness. The real number was 0.67. Here's the bug.”
- “Exact-match agreement said my judge was good. Cohen's κ said it wasn't. Same labels.”

---

## LinkedIn (150–250 words)

**Frame:** judgment, not pipeline.

Draft angle:

> I almost shipped a faithfulness number that was ~20 points too optimistic because I reported exact match instead of chance-corrected agreement with human labels.
>
> Built a RAGAS-shaped evaluator (decompose claims → check against retrieved context). Looked great on raw agreement. MVVP-style audit + Cohen's κ told a different story.
>
> Lesson: if your eval is an LLM judge, reliability without a chance-corrected human check is a vanity metric.

- Line breaks every 1–2 sentences.
- Link in **first comment**, not the body.
- Wed 8:30am IST.

---

## Offcuts (bank for later weeks)

- Claim-merge bug that padded faithfulness
- `costmeter` + OpenTelemetry GenAI conventions
- SelfCheckGPT as reference-free aside (https://arxiv.org/abs/2303.08896)
- An ADR detail that didn't fit the post

---

## Checklist before publish

- [ ] Numbers in blog match `results/` summary
- [ ] κ is the headline; raw agree is secondary
- [ ] “When I would not use this” present on blog + thread
- [ ] Series index linked: `saran.build/paper-to-production`
- [ ] Repo README results table updated
- [ ] X: no link in post 1
- [ ] LinkedIn: link in first comment
