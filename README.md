# Paper to Production

> Implementing arXiv research in production voice and RAG systems — and measuring whether it actually works.

**Series:** [saran.build/paper-to-production](https://saran.build/paper-to-production)  
**Window:** Aug 2026 → Dec 2026 · 10 build sprints + 22 paper notes

This monorepo is one evolving system, not a pile of demos. Each sprint adds a capability, an ADR, and measured results under a shared schema.

---

## Sprint map

| # | Dir | Topic | Publish |
|---|---|---|---|
| 01 | [`sprints/01-faithfulness`](sprints/01-faithfulness/) | Faithfulness evaluator from scratch | Tue 4 Aug |
| 02 | [`sprints/02-endpointing`](sprints/02-endpointing/) | Endpointing & turn-taking latency | Tue 18 Aug |
| 03 | [`sprints/03-streaming-pipeline`](sprints/03-streaming-pipeline/) | ASR→LLM→TTS + barge-in | Tue 1 Sep |
| 04 | [`sprints/04-voice-eval`](sprints/04-voice-eval/) | Voice agent evaluation harness | Tue 15 Sep |
| 05 | [`sprints/05-retrieval-design`](sprints/05-retrieval-design/) | Retrieval design space | Tue 29 Sep |
| 06 | [`sprints/06-chunking`](sprints/06-chunking/) | Chunking & contextual retrieval | Tue 13 Oct |
| 07 | [`sprints/07-extraction-finetune`](sprints/07-extraction-finetune/) | Structured extraction: fine-tune vs prompt | Tue 27 Oct |
| 08 | [`sprints/08-agent-harness`](sprints/08-agent-harness/) | Agent harness teardown | Tue 10 Nov |
| 09 | [`sprints/09-prompt-injection`](sprints/09-prompt-injection/) | Indirect prompt injection | Tue 24 Nov |
| 10 | [`sprints/10-capstone`](sprints/10-capstone/) | Capstone architecture | Tue 8 Dec |

---

## Repo layout

```
paper-to-production/
├── README.md                 ← you are here
├── PLAN.md                   ← full lab plan (cadence, rules, calendar)
├── backlog.md                ← skipped papers (one line each)
├── logbook.md                ← failures, atrophy monitor
├── decisions/                ← ADR-001 … ADR-010
├── paper-notes/              ← weekly 1–2 hr notes (22)
├── instruments/
│   ├── evalkit/              ← eval harness (built by hand over sprints)
│   ├── costmeter/            ← uniform cost/latency schema (starts sprint 1)
│   ├── datasets/             ← versioned test sets
│   └── promptlib/            ← prompts + agent harness
├── sprints/
│   ├── 01-faithfulness/ …    ← one folder per sprint
│   └── 10-capstone/
└── results/                  ← cross-sprint comparisons (same schema)
```

**Rule:** nothing lands on `main` without (1) a regression test, (2) p50/p95 latency, (3) cost per operation, (4) failure-mode writeup, (5) rollback/degradation path.

---

## Current status

| Sprint | Status | Headline metric |
|---|---|---|
| 01 Faithfulness | In progress | Cohen's κ vs human labels |
| 02–10 | Planned | See each sprint `README.md` |

---

## Results (filled each sprint)

| Sprint | Metric | Value | Cost / op | p50 | p95 | Notes |
|---|---|---|---|---|---|---|
| 01 | κ (faithfulness vs human) | TBD (seed fixtures + tests green) | heuristic $0; LLM TBD | TBD | TBD | Run `faithfulness fixtures` |

## Develop

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
faithfulness fixtures --mode heuristic
```

---

## Topics

`arxiv` · `machine-learning` · `llm` · `rag` · `voice-agents` · `rag-evaluation` · `llmops` · `applied-ai` · `ai-engineering` · `paper-implementation` · `production-ml`
