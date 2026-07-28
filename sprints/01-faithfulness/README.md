# Sprint 01 — Faithfulness evaluator from scratch

**Publish:** Tue 4 Aug 2026 · **Status:** In progress  
**Dir:** `sprints/01-faithfulness/`  
**Blog slug:** `faithfulness-from-scratch`

> Implementing arXiv research in production voice and RAG systems — and measuring whether it actually works.

## Papers

| Role | Paper | Link |
|---|---|---|
| Primary | RAGAS: Automated Evaluation of RAG | https://arxiv.org/abs/2309.15217 |
| Supporting | FActScore: atomic fact decomposition | https://arxiv.org/abs/2305.14251 |
| Critical | Reliability without Validity (judge audit, MVVP) | https://arxiv.org/abs/2606.19544 |
| Optional | G-Eval | https://arxiv.org/abs/2303.16634 |
| Optional | Judging LLM-as-a-Judge (Zheng et al.) | https://arxiv.org/abs/2306.05685 |

## Build boundary

| Built unassisted | Can delegate |
|---|---|
| Atomic claim decomposition | RAG plumbing, fixtures, plotting, costmeter wiring |

## Headline metric

**Cohen's κ** with human labels — *not* raw agreement.

**Hook:** the gap between the evaluator score and human labels, and what the judge audit revealed about the numbers.

## Also ship

- [`costmeter`](../../instruments/costmeter/) v1 + OTel GenAI conventions
- Uniform results schema under [`results/`](results/)
- [`ADR-001`](../../decisions/ADR-001.md)

## Folder layout

```
01-faithfulness/
├── README.md          ← this file
├── CONTENT.md         ← blog / X / LinkedIn plan
├── ADR.md             ← pointer to decisions/ADR-001.md
├── src/               ← decompose, verify, score
├── notebooks/         ← exploration only; not source of truth
└── results/           ← run outputs (gitignored dumps; keep summaries)
```

## Production bar (must all pass before publish)

- [ ] Regression test fails when a known hallucination scores as faithful
- [ ] p50 / p95 latency recorded
- [ ] Cost per evaluation recorded
- [ ] Failure-mode section in CONTENT / blog draft
- [ ] Documented rollback / degradation path

## Week-of calendar

| When | What |
|---|---|
| Tue 28 Jul | ADR-001 + repo skeleton + 30–50 listing docs. Code only after spec. |
| Wed–Fri | Baseline RAG · claim decomposition (by hand) · scoring · ~75 labelled cases |
| Sat 1 Aug | RAGAS comparison · MVVP-lite · cost/latency · finalise ADR |
| Sun 2 Aug | Draft post |
| Tue 4 Aug | Blog 5:30pm IST → X thread 6:30pm |
| Wed 5 Aug | LinkedIn 8:30am IST |
