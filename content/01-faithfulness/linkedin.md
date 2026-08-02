# LinkedIn — Build 01 Faithfulness

**Publish:** Wednesday, August 5, 2026 · **8:30 AM IST**  
**Status:** drafting  
**Frame:** applied-engineering judgment, not “I implemented a paper.”  
**Link:** first comment only.

---

## POST — paste into LinkedIn

```text
The first build in my paper-to-production series was not “I implemented RAGAS.”

The real problem was simpler and more useful:

I wanted a way to tell whether a listing-style RAG answer was actually supported by retrieved context.

So I pulled three different things from three different papers:

RAGAS gave me the evaluator shape:
decompose -> verify -> score.

FActScore gave me the discipline to split answers into atomic claims, so one half-true sentence could not hide a hallucination.

Reliability without Validity gave me the part most people skip:
audit the judge itself with Cohen’s kappa, replicates, and bias checks.

That became a real repo artifact:
claim-level evaluation, regression fixtures, cost/latency instrumentation, and an audit path.

Current seed-run results are promising, but I do not want to overclaim from a small heuristic set.

That is the main lesson I am taking forward:

papers can give you the method shape, but the engineering value comes from adapting it to domain failures and validating the metric before trusting the number.
```

**Image:** [`media/banner-linkedin.png`](media/banner-linkedin.png) — 1200×1200, headline reads *“An unaudited metric is an ornament.”*

---

## First comment

```text
Full writeup:
https://saran.build/paper-to-production/faithfulness-from-scratch

Series:
https://saran.build/paper-to-production

Repo:
https://github.com/saran-io/paper-to-production
```

---

## Alt shorter version

```text
I did not want the first build in paper-to-production to be “I read RAGAS.”

I wanted it to answer a real question:

when a RAG system gives a fluent answer, how do I tell whether the claims are actually grounded in retrieved context?

RAGAS gave me the evaluator loop.
FActScore gave me atomic claim discipline.
Reliability without Validity gave me the judge-audit mindset.

That combination mattered more than any single paper.

The useful outcome was not a paper summary.

It was a working evaluator with tests, domain failure cases, and an explicit warning not to trust small-set wins too early.
```
