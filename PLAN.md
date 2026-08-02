# Paper to Production — Operating Plan

**Positioning:** applied AI engineer who reads new research, adapts it to real systems, and proves whether it fixes actual production problems.

**Season 1 window:** Tuesday, August 4, 2026 → Tuesday, December 8, 2026  
**Important:** this is the first operating season, not the end-state of the repo.

## 1. Core thesis

This lab is not a paper-summary project and not a foundation-notebook archive.

The standard for every build is:

1. Start from a real issue
2. Read the paper closely enough to isolate the useful claim
3. Implement the claim in a production-shaped slice
4. Measure cost, latency, reliability, and failure modes
5. Make a decision: adopt, adapt, park, or reject

The public takeaway should be:

> He can take research off arXiv, turn it into a system, and tell whether it belongs in production.

## 2. What counts as success

Each sprint should answer a question that matters in a live system.

| Area | Real problem |
|---|---|
| Voice agents | callers get cut off, responses arrive too late, evaluation is weak |
| RAG + evaluation | grounded answers still hallucinate, retrieval quality is hard to trust |
| Agent harnesses | orchestration changes results more than model choice |
| Production LLM systems | serving cost, latency, extraction reliability, and security determine viability |

Good output is not “implemented paper X.”  
Good output is “paper X improved or failed to improve problem Y under constraints Z.”

## 3. Operating tracks

| Track | Frequency | Output | Purpose |
|---|---|---|---|
| Paper notes | Weekly | note in `paper-notes/` | fast judgment and intake |
| Build sprints | Biweekly | code + ADR + results + content | production-shaped implementation |
| Queue maintenance | Ongoing | updates in `PAPERS.md` | keep the series evergreen |

## 4. Intake rules

[`PAPERS.md`](PAPERS.md) is the source of truth for the queue.

A new paper should only enter the queue if it has:

- A named production issue
- A plausible implementation slice
- A metric that can falsify the claim
- A reason it matters now, not “sometime later”

Status glossary:

- `candidate`: worth scanning, not committed
- `reading`: actively being evaluated
- `queued`: accepted for a future note or sprint
- `building`: implementation in progress
- `published`: implementation or note shipped
- `parked`: interesting but not urgent
- `rejected`: does not solve a real repo problem

## 5. Build selection logic

Choose the next sprint paper using this order:

1. Urgency of the production issue
2. Leverage if it works
3. Ability to produce a convincing measurement
4. Reusability of the resulting artifact
5. Content value as a secondary effect

Do not choose papers because they are famous, recent, or easy to turn into a thread.

## 6. Season 1 build map

| Sprint | Problem | Output |
|---|---|---|
| 01 Faithfulness | unsupported RAG answers | evaluator + judge audit |
| 02 Endpointing | turn-taking latency and caller cutoffs | endpoint policy + latency instrumentation |
| 03 Streaming pipeline | slow voice response | streaming pipeline + barge-in |
| 04 Voice eval | weak real-world benchmarking | domain voice evaluation harness |
| 05 Retrieval design | recall/latency/cost confusion | retrieval decision table |
| 06 Chunking | retrieval failure from boundaries | chunking benchmark |
| 07 Extraction | unreliable structured outputs | extraction comparison and cost model |
| 08 Agent harness | harness hype without discipline | trajectory scorer + harness comparison |
| 09 Prompt injection | unsafe document-grounded systems | attack corpus + defenses |
| 10 Capstone | fragmented learnings | cross-sprint system and ADR review |

## 7. Paper note standard

Every note should answer:

- What claim is the paper really making?
- What would have to be true for it to help my system?
- What metric would tell me it worked?
- Where would it break in practice?
- Is the verdict `BUILD`, `BORROW`, `PARK`, or `REJECT`?

Paper notes are not summaries. They are decision memos.

## 8. Sprint standard

A sprint is complete only when it includes:

- implementation
- dataset or test cases
- latency and cost measurement
- failure analysis
- ADR
- publish-ready explanation of when not to use it

If one of these is missing, the repo is drifting toward demo theater.

## 9. Shipping bar

Nothing lands on `main` without:

1. A regression test
2. Measured p50/p95 latency
3. Cost per operation
4. Failure-mode writeup
5. Rollback, fallback, or clear rejection path

## 10. Content discipline

The content exists to support the engineering proof, not replace it.

| Surface | Job |
|---|---|
| Blog | canonical method, numbers, failure modes, decision |
| X | result-first distribution |
| LinkedIn | judgment and engineering framing |

Every post should make the audience understand:

- the problem
- the experiment
- the measured outcome
- the engineering decision

## 11. Evergreen rule

After Tuesday, December 8, 2026, the repo should still be able to absorb a new paper announced on Wednesday, December 9, 2026 without structural changes.

That means:

- the queue cannot be hardcoded to ten papers
- the note template must work indefinitely
- each sprint must leave behind reusable instrumentation or evaluation assets
- paper selection must stay tied to real system problems
