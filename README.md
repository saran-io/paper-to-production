# Paper to Production

> Implementing new AI papers in production-shaped systems to fix real problems, then showing whether they hold up under latency, cost, and reliability constraints.

This repo exists to prove applied AI engineering skill in public:

1. Read the paper, not the hype
2. Reproduce the useful idea
3. Adapt it to a real use case
4. Measure whether it fixes the problem
5. Explain when I would not use it

The point is not “I implemented a paper.”  
The point is “I can decide whether new research belongs in a real system.”

## What this repo proves

- I work from real operational problems: hallucinations, retrieval misses, voice latency, agent failure, prompt injection.
- I implement research inside production-shaped systems, not notebook-only demos.
- I report tradeoffs, not only wins: failure modes, rollout limits, fallback paths, and when the paper should be rejected.

## Operating model

- Weekly: paper note in [`paper-notes/`](paper-notes/)
- Biweekly: deeper build in [`builds/`](builds/)
- Always open: new papers can enter the queue at any time through [`PAPERS.md`](PAPERS.md)

Season 1 runs from **Tuesday, August 4, 2026** through **Tuesday, December 8, 2026**.  
The repo does not end there. Season 1 is the first operating window, not the lifetime of the project.

## Season 1 builds

| # | Dir | Problem | Research angle | Publish |
|---|---|---|---|---|
| 01 | [`builds/01-faithfulness`](builds/01-faithfulness/) | RAG hallucination / unsupported answers | Faithfulness evaluator from scratch | Tue 4 Aug 2026 |
| 02 | [`builds/02-endpointing`](builds/02-endpointing/) | Voice cutoffs / turn-taking latency | Endpointing and turn detection | Tue 18 Aug 2026 |
| 03 | [`builds/03-streaming-pipeline`](builds/03-streaming-pipeline/) | Slow voice response | Streaming ASR→LLM→TTS and barge-in | Tue 1 Sep 2026 |
| 04 | [`builds/04-voice-eval`](builds/04-voice-eval/) | Weak voice QA and benchmarking | Voice evaluation harness | Tue 15 Sep 2026 |
| 05 | [`builds/05-retrieval-design`](builds/05-retrieval-design/) | Poor retrieval quality / cost tradeoffs | Retrieval design choices | Tue 29 Sep 2026 |
| 06 | [`builds/06-chunking`](builds/06-chunking/) | Retrieval failures from bad chunk boundaries | Chunking and contextual retrieval | Tue 13 Oct 2026 |
| 07 | [`builds/07-extraction-finetune`](builds/07-extraction-finetune/) | Unreliable structured extraction | Fine-tune vs prompt vs constrained decoding | Tue 27 Oct 2026 |
| 08 | [`builds/08-agent-harness`](builds/08-agent-harness/) | Agent scaffolds that look good but fail in practice | Agent harness teardown | Tue 10 Nov 2026 |
| 09 | [`builds/09-prompt-injection`](builds/09-prompt-injection/) | Unsafe document-grounded systems | Indirect prompt injection | Tue 24 Nov 2026 |
| 10 | [`builds/10-capstone`](builds/10-capstone/) | End-to-end system judgment | Cross-build architecture and decisions | Tue 8 Dec 2026 |

## How new papers enter

[`PAPERS.md`](PAPERS.md) is the canonical queue.

A paper earns a real slot only if it can answer all of these:

- What production issue does this help fix?
- What change would I actually implement?
- What metric would prove it worked?
- What would make me reject it after testing?

Status flow:

`candidate` → `reading` → `queued` → `building` → `published`  
or  
`candidate` → `parked` / `rejected`

## Repo layout

```
paper-to-production/
├── README.md
├── PLAN.md
├── PAPERS.md
├── backlog.md
├── logbook.md
├── decisions/
├── paper-notes/
├── content/
├── instruments/
│   ├── evalkit/
│   ├── costmeter/
│   ├── datasets/
│   └── promptlib/
├── builds/
└── results/
```

## Shipping bar

Nothing should land on `main` without:

1. A regression test
2. Measured latency
3. Measured cost
4. A failure-mode writeup
5. A clear decision or fallback path

## Current status

| Track | Status | Proof target |
|---|---|---|
| Build 01 | In progress | Cohen's κ vs human labels |
| Season 1 queue | Planned | One production problem per build |
| Evergreen intake | Active | New papers can be added any week |

## Develop

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
faithfulness fixtures --mode heuristic
```
