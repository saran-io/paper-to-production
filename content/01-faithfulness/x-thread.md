# X — Build 01 Faithfulness

**Publish:** Tuesday, August 4, 2026 · **6:30 PM IST**  
**Status:** drafting  
**Rules:** no blog link until the last post. Honest to the repo seed-run state.

---

## Thread index

| # | Beat | Media |
|---|---|---|
| 1 | Hook | optional / none |
| 2 | Real problem | **`media/banner-x.png`** |
| 3 | What the papers gave me | — |
| 4 | What I built | **`media/architecture.png`** |
| 5 | Real test buckets | optional |
| 6 | Current repo results | optional |
| 7 | What is still not proven | — |
| 8 | Applied-engineering takeaway | — |
| 9 | Blog + repo links | — |

---

## POST 1 — Hook

```text
First build in paper-to-production:

I built a faithfulness evaluator for a real listing-style RAG problem.

Not “I implemented a paper.”

I took ideas from RAGAS, FActScore, and Reliability without Validity and turned them into a working evaluation loop with tests, audit hooks, and real failure cases.

🧵
```

---

## POST 2 — Real problem

```text
The problem was simple:

A RAG system can answer fluently and still invent prices, amenities, or merge facts across listings.

So the question is not:
“does the answer sound right?”

It is:
“are the claims in the answer actually supported by retrieved context?”
```

**Media:** [`media/banner-x.png`](media/banner-x.png) — 1600×900, headline reads *“Fluent answers can still be unsupported.”*

---

## POST 3 — What the papers gave me

```text
What each paper contributed:

• RAGAS -> evaluator shape
  decompose -> verify -> score

• FActScore -> atomic fact discipline
  coarse claims hide hallucinations

• Reliability without Validity -> judge audit
  don’t trust exact agreement alone
```

---

## POST 4 — What I built

```text
That became a real repo artifact:

decompose -> verify -> |V|/|S|

plus regression fixtures, cost/latency instrumentation, and an MVVP-lite judge audit path.
```

**Media:** [`media/architecture.png`](media/architecture.png)

---

## POST 5 — Real failure buckets

```text
The evaluator is shaped around listing-domain failures:

• fully supported
• partially supported
• contradictory
• correct but unsupported
• poor retrieval
• wrong price / feature
• facts merged across two properties
• empty retrieval
```

---

## POST 6 — Current repo results

```text
Current seed-run results (heuristic mode):

• cases: 8
• raw agreement: 1.0
• Cohen’s κ: 1.0
• hallucinated prices score 0.0
• partial answers score between 0 and 1

Promising for the harness.
Not enough to call it a production gate.
```

---

## POST 7 — What is still not proven

```text
What is still not proven:

• larger labelled set
• LLM-mode run
• stronger human-vs-judge validation
• realistic cost profile

This is exactly why the judge-audit paper matters.
```

---

## POST 8 — Takeaway

```text
Main takeaway from Build 01:

papers gave me the method shape.

The engineering value came from adapting that shape to domain failures and validating the evaluator before trusting the score.

That is the difference between reading papers and doing applied AI engineering.
```

---

## POST 9 — Link

```text
Full writeup:
https://saran.build/paper-to-production/faithfulness-from-scratch

Repo:
https://github.com/saran-io/paper-to-production
```
