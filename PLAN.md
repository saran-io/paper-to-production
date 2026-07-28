# Paper to Production — Applied AI Engineering Lab

**Window:** 4 Aug 2026 → 8 Dec 2026 (buffers extend to mid-Jan 2027)
**Positioning:** Applied AI Engineer / AI-Native Implementation Architect — voice agents, RAG evaluation, production LLM systems.

---

## 0. Identity — locked

**Name:** `paper-to-production` — one string, everywhere.

**Tagline** (repo description, blog header, LinkedIn Featured):

> Implementing arXiv research in production voice and RAG systems — and measuring whether it actually works.

The final clause is load-bearing. It's what separates this from a tutorial repo. Never drop it.

| Surface | Form |
|---|---|
| GitHub | `github.com/<you>/paper-to-production` |
| Series index | `saran.build/paper-to-production` |
| Post | `saran.build/paper-to-production/faithfulness-from-scratch` |
| X / LinkedIn | "Paper to Production" as the first line of every post |
| Discovery call | "I run a paper-to-production series — I implement research techniques and measure them in production voice systems." |

**GitHub topics** (discovery lives here, not in the name):

```
arxiv · machine-learning · llm · rag · voice-agents · rag-evaluation
llmops · applied-ai · ai-engineering · paper-implementation · production-ml
```

**Blog tags:** `arxiv`, `paper-implementation`, `ml-systems`, `voice-ai`, `rag`, `evaluation`

**Breakout repo names** (create only once earned):
- `voice-evalkit` or `ragas-from-scratch` — whichever half of the harness spins out first
- `telephony-voice-bench` — the domain benchmark; the paper title writes itself

---

## 1. Cadence

Two tracks, different costs, do not conflate them.

| Track | Frequency | Time | Output |
|---|---|---|---|
| **Paper notes** | Weekly | 1–2 hrs | A note in `paper-notes/`. Feeds X + LinkedIn offcuts. |
| **Build sprints** | Biweekly | 15–25 hrs | Blog post + repo change + ADR + results. |

By 31 Dec: **22 paper notes + 10 deep builds**.

Distribution stays weekly throughout: 1 X post + 1 LinkedIn post every week, sprint week or not.

---

## 2. The two-week calendar

| Day | Build week | Publish week |
|---|---|---|
| Mon | Read paper, define baseline + metrics | Analyse what shipped, pick next paper |
| Tue | **Implement core method** · X post 6:30pm (offcut) | **Publish blog 5:30pm → X thread 6:30pm** |
| Wed | **Implement, build test set** | Read next paper, take notes |
| Thu | **Run experiments, chase failures** · LinkedIn 8:30am (lesson) | **LinkedIn 8:30am** (judgment framing) |
| Fri | Write ADR, clean repo, README | Prototype spike for next sprint |
| Sat | **Draft blog post** | Light / off |
| Sun | Edit, cut 30%, prep thread | Off |

**Bold cells need contiguous time.** Protect Wednesday evening and Saturday morning as real blocks. Everything else survives fragmentation.

**Timing rationale.** 6:30pm IST = 9am ET, peak US tech X. LinkedIn 8:30am IST catches the Indian commute and still reaches US viewers that evening (24–48hr half-life). Tue–Thu only. Blog goes live one hour before the thread so the link is warm.

---

## 3. Sprint plan

> arXiv IDs below are for lookup convenience — verify each before citing in a published post.

### Sprint 1 — Faithfulness evaluator from scratch
**Publish:** Tue 4 Aug · **Dir:** `sprints/01-faithfulness/`

| Role | Paper | Link |
|---|---|---|
| Primary | RAGAS: Automated Evaluation of RAG | https://arxiv.org/abs/2309.15217 |
| Supporting | FActScore: atomic fact decomposition | https://arxiv.org/abs/2305.14251 |
| **Critical** | Reliability without Validity (judge audit, MVVP) | https://arxiv.org/abs/2606.19544 |
| Optional | G-Eval | https://arxiv.org/abs/2303.16634 |
| Optional | Judging LLM-as-a-Judge (Zheng et al.) | https://arxiv.org/abs/2306.05685 |

**Build unassisted:** atomic claim decomposition.
**Headline metric:** chance-corrected agreement (Cohen's κ) with human labels — *not* raw agreement.
**Hook:** the gap between my evaluator and human labels, and what the judge audit revealed about my own numbers.
**Also ship:** `costmeter` v1, uniform schema, OTel GenAI conventions.

---

### Sprint 2 — Endpointing & turn-taking latency teardown
**Publish:** Tue 18 Aug · **Dir:** `sprints/02-endpointing/`

| Role | Paper | Link |
|---|---|---|
| Primary | Voice Activity Projection (Ekstedt & Skantze) | https://arxiv.org/abs/2205.09812 |
| Supporting | Next-Turn: duration-aware streaming endpoint detection | https://arxiv.org/abs/2606.18094 |
| Supporting | Semantic VAD | https://arxiv.org/abs/2305.12450 |
| Optional | Phoenix-VAD | https://arxiv.org/abs/2509.20410 |
| Optional | Easy Turn | https://arxiv.org/abs/2509.23938 |

**Build unassisted:** endpoint decision logic + latency instrumentation.
**Headline metric:** p50/p95 endpoint latency vs cut-off rate.
**Killer number:** cut-off rate when a caller spells an email address or reads back a phone number. Fixed silence timeouts fail exactly there.
**Experiment:** fixed-threshold VAD vs model-based turn detection, on your own call audio.

---

### Sprint 3 — Streaming pipeline: ASR→LLM→TTS, barge-in
**Publish:** Tue 1 Sep · **Dir:** `sprints/03-streaming-pipeline/`

| Role | Paper | Link |
|---|---|---|
| Primary | Moshi (full-duplex speech-text) | https://arxiv.org/abs/2410.00037 |
| Supporting | LLMVoX (streaming TTS, ACL Findings 2025) | search arXiv — verify ID |
| Serving | Fast inference via speculative decoding | https://arxiv.org/abs/2211.17192 |
| Serving | PagedAttention / vLLM | https://arxiv.org/abs/2309.06180 |

**Build unassisted:** barge-in state machine.
**Headline metric:** time-to-first-audio, broken out per stage.
**Angle nobody covers:** the serving layer. Everyone stops at "use a smaller model"; TTFT is attackable directly.

---

### Sprint 4 — Voice agent evaluation harness ★ paper candidate
**Publish:** Tue 15 Sep · **Dir:** `sprints/04-voice-eval/`

| Role | Paper | Link |
|---|---|---|
| Primary | Full-Duplex-Bench v1 | https://arxiv.org/abs/2503.04721 |
| Supporting | Full-Duplex-Bench v1.5 (overlap handling) | https://arxiv.org/abs/2507.23159 |
| Supporting | Full-Duplex-Bench v3 (tool use under disfluency) | https://arxiv.org/abs/2604.04847 |
| Supporting | τ-Voice (real-world domain benchmarking) | https://arxiv.org/abs/2603.13686 |

**Build unassisted:** scoring rubric + inter-annotator agreement.
**Headline metric:** task completion vs turn-taking score.
**The post:** where these benchmarks *don't* transfer — telephony compression, Indian-accented English, property vocabulary. That gap analysis is the paper's motivation section.
**Paper track:** expand dataset Oct–Nov, submit Jan–Feb for a mid-2027 venue (Interspeech, ACL/EMNLP eval workshops).

---

### Sprint 5 — Retrieval design space (one decision table)
**Publish:** Tue 29 Sep · **Dir:** `sprints/05-retrieval-design/`

| Role | Paper | Link |
|---|---|---|
| Primary | Dense Passage Retrieval | https://arxiv.org/abs/2004.04906 |
| Supporting | ColBERT (late interaction) | https://arxiv.org/abs/2004.12832 |

**Build unassisted:** hybrid fusion + scoring.
**Headline metric:** Recall@k vs latency vs $/1k queries.
**Format discipline:** one post with a decision table, not three posts. This area is saturated — compress it.

---

### Sprint 6 — Chunking & contextual retrieval
**Publish:** Tue 13 Oct · **Dir:** `sprints/06-chunking/`

| Role | Paper | Link |
|---|---|---|
| Primary | Contextual Retrieval (Anthropic) | https://www.anthropic.com/news/contextual-retrieval |
| Supporting | Late Chunking | https://arxiv.org/abs/2409.04701 |

**Build unassisted:** chunker + boundary evaluation.
**Headline metric:** retrieval failure rate by chunk strategy.
**Angle:** where production RAG actually breaks. Chunk boundaries, not embedding models.

---

### Sprint 7 — Structured extraction: fine-tune vs prompt
**Publish:** Tue 27 Oct · **Dir:** `sprints/07-extraction-finetune/`

| Role | Paper | Link |
|---|---|---|
| Primary | LoRA | https://arxiv.org/abs/2106.09685 |
| Supporting | QLoRA | https://arxiv.org/abs/2305.14314 |
| **High value** | Efficient Guided Generation (constrained decoding) | https://arxiv.org/abs/2307.09702 |

**Build unassisted:** extraction eval + cost model.
**Headline metric:** accuracy per dollar, fine-tuned vs prompted.
**The architect version:** the post is about *whether to fine-tune at all*, not how to run a training script. Guaranteed-valid JSON without retry loops is the underrated production win here.

---

### Sprint 8 — Agent harness teardown ★ strongest positioning post
**Publish:** Tue 10 Nov · **Dir:** `sprints/08-agent-harness/`

| Role | Paper | Link |
|---|---|---|
| **Anchor** | The Harness Effect (harness-only, models fixed) | https://arxiv.org/abs/2607.06906 |
| **Metric** | Scaling Laws for Agent Harnesses (EFC) | https://arxiv.org/abs/2605.29682 |
| **Counterweight** | Harnesses Are Not Uniformly Better | https://arxiv.org/abs/2605.21516 |
| **Service shape** | Life-Harness (adapt the interface, not the model) | https://arxiv.org/abs/2605.22166 |
| **Caution** | Harness Evolution, Rethought | https://arxiv.org/abs/2607.12227 |
| Foundation | ReAct | https://arxiv.org/abs/2210.03629 |
| Foundation | Reflexion | https://arxiv.org/abs/2303.11366 |
| Design vocab | MCP Server Patterns | https://arxiv.org/abs/2606.30317 |

**Build unassisted:** trajectory scorer.
**Headline metric:** task success + tool-call precision + your own throughput/rework numbers.
**Thesis:** the scaffold is the lever, not the model — cost per task moved more by orchestration than by the entire model menu.
**Include the counterweight.** Citing the result that evolved harnesses underperform plain parallel sampling under matched budgets is what makes you look like an adversarial reader rather than a hype-repeater.

---

### Sprint 9 — Indirect prompt injection via listing documents
**Publish:** Tue 24 Nov · **Dir:** `sprints/09-prompt-injection/`

| Role | Paper | Link |
|---|---|---|
| Primary | Not what you've signed up for (Greshake et al.) | https://arxiv.org/abs/2302.12173 |
| Defense | Llama Guard | https://arxiv.org/abs/2312.06674 |

**Build unassisted:** attack corpus for property documents.
**Headline metric:** attack success rate before/after defense.
**Why it lands:** concrete, underwritten, and a real threat when your RAG ingests third-party listing documents.

---

### Sprint 10 — Capstone
**Publish:** Tue 8 Dec · **Dir:** `sprints/10-capstone/`

Full system architecture. Every ADR revisited with hindsight. Cross-sprint cost/latency comparison on the uniform `costmeter` schema — this is only possible because the schema was fixed in sprint 1.

---

## 4. Buffer slots (3, unallocated)

| B | Topic | Papers | Best for |
|---|---|---|---|
| B1 | Routing & cascades — the cost story | FrugalGPT https://arxiv.org/abs/2305.05176 · RouteLLM https://arxiv.org/abs/2406.18665 · When Is Routing Meaningful https://arxiv.org/abs/2607.09197 | **Contract asset** — cost reduction sells itself in a discovery call |
| B2 | Abstention: when the agent says "I don't know" | Semantic entropy https://www.nature.com/articles/s41586-024-07421-0 | **Paper asset** — liability framing for wrong prices on a call |
| B3 | Agent failure attribution | Failure as a Process https://arxiv.org/abs/2607.09510 · OAT https://arxiv.org/abs/2607.12747 · Agent Limitations Taxonomy https://arxiv.org/abs/2607.05775 | Delivery skill + client incident reviews |

B1 experiment worth running regardless: test your router under paraphrase perturbation. Learned routers that look accurate on clean queries collapse under rewording. Two hours, and almost nobody does it.

Spend all three → capstone slides to mid-January. Spend none → finish 8 Dec.

---

## 5. Weekly paper-note track (22 weeks)

One paper, 1–2 hrs, Monday. Note goes in `paper-notes/`. Sprint-critical papers are scheduled the week *before* their sprint.

| Wk | Mon | Paper | Purpose |
|---|---|---|---|
| 1 | Aug 3 | RAGAS + FActScore | Sprint 1 |
| 2 | Aug 10 | Reliability without Validity | Sprint 1 (judge protocol) |
| 3 | Aug 17 | Voice Activity Projection | Sprint 2 |
| 4 | Aug 24 | Next-Turn / Semantic VAD | Sprint 2 |
| 5 | Aug 31 | Moshi | Sprint 3 |
| 6 | Sep 7 | Speculative decoding + PagedAttention | Sprint 3 |
| 7 | Sep 14 | Full-Duplex-Bench v1 + v3 | Sprint 4 |
| 8 | Sep 21 | τ-Voice | Sprint 4 |
| 9 | Sep 28 | DPR + ColBERT | Sprint 5 |
| 10 | Oct 5 | HyDE https://arxiv.org/abs/2212.10496 | Exploration |
| 11 | Oct 12 | Late Chunking | Sprint 6 |
| 12 | Oct 19 | Self-RAG https://arxiv.org/abs/2310.11511 | Exploration |
| 13 | Oct 26 | LoRA + QLoRA | Sprint 7 |
| 14 | Nov 2 | Guided generation (constrained decoding) | Sprint 7 |
| 15 | Nov 9 | The Harness Effect | Sprint 8 |
| 16 | Nov 16 | Harness scaling laws (EFC) | Sprint 8 |
| 17 | Nov 23 | Life-Harness + Harnesses Not Uniformly Better | Sprint 8 |
| 18 | Nov 30 | Greshake indirect prompt injection | Sprint 9 |
| 19 | Dec 7 | Llama Guard | Sprint 9 |
| 20 | Dec 14 | Always-On Agents survey https://arxiv.org/abs/2606.30306 | Exploration |
| 21 | Dec 21 | AgingBench https://arxiv.org/abs/2605.26302 | Exploration |
| 22 | Dec 28 | Metacognition in LLMs https://arxiv.org/abs/2607.11881 | Exploration → B2 |

**Swap freely.** Read the weekly DAIR.AI issue (github.com/dair-ai/AI-Papers-of-the-Week) in the Wednesday reading slot, 30 min cap. A paper earns a slot only if it would change a decision already in `decisions/`. Everything else gets one line in `backlog.md` with the arXiv ID and nothing more.

**Skip from that feed:** world models, VLA/robotics, diffusion-LLM RL, GFlowNet post-training, attention-architecture work. Interesting, but changes no decision in a voice agent you're shipping.

---

## 6. Paper note template

```markdown
# <Paper> (<arXiv ID>)
Date read: · Time spent:

## Claim
One paragraph, my words.

## What would have to be true for this to help my system
Preconditions. Be specific about scale, latency budget, data.

## What I'd measure
The single number that would tell me it worked.

## Verdict
BUILD / BORROW / IGNORE — and why.

## If IGNORE: what would change my mind
```

Twenty-two of these, with the IGNOREs reasoned rather than skipped, is the architect artifact. It's the thing that makes a discovery call go well when a buyer asks whether some technique they read about is worth doing.

---

## 7. Content plan

### X thread (8–12 posts, Tue 6:30pm IST)
- Open with the **result**, not the setup. *"My RAG system scored 0.91 faithfulness. The real number was 0.67. Here's the bug"* beats *"This week I implemented RAGAS."*
- One image per middle post: chart, code block, or decision table.
- Second-to-last post: **"when I would not use this."**
- Last post: blog link. **Never in post 1** — X suppresses link posts and you lose reach on the whole thread.

### LinkedIn (150–250 words, Wed 8:30am IST)
- Different framing entirely: not the implementation, the **judgment**. *"I spent a week deciding whether to fine-tune or prompt. I chose prompting. Here's the cost math."*
- No thread format. Link in the first comment, not the body.
- Line breaks every 1–2 sentences.

### Blog (saran.build, Tue 5:30pm IST)
Canonical artifact. Full method, all numbers, ADR embedded, genuinely limiting limitations section. Every post ends with **"when I would not use this."**

### Offcut bank (consolidation weeks)
Drawn from the prior sprint, one X + one LinkedIn per week:

- SelfCheckGPT as a reference-free hallucination check (https://arxiv.org/abs/2303.08896)
- Semantic caching hit rates on property FAQs
- OpenTelemetry GenAI conventions in `costmeter`
- The p95 that ruined a great-looking p50
- A chunking strategy that failed
- An ADR I reversed
- Agent rework rate for one sprint
- What I stopped delegating, and why

Offcuts are not filler. *"Here's the bug that made my faithfulness scores look 12 points better than they were"* often outperforms the polished post.

---

## 8. Repo

**Canonical monorepo: `paper-to-production`.** One system that gets progressively more capable — twelve standalone repos read as twelve exercises; one evolving system reads as architecture.

```
paper-to-production/
├── README.md              ← architecture diagram + results table, updated every sprint
├── decisions/             ADR-001 … ADR-010 (+ ADR-supersedes notes)
├── paper-notes/           22 notes
├── backlog.md             one line per skipped paper
├── logbook.md             failures, root causes, atrophy monitor
├── instruments/
│   ├── evalkit/           ← built by hand, never fully delegated
│   ├── costmeter/         ← uniform schema, all 10 sprints, OTel GenAI conventions
│   ├── datasets/          versioned, reused
│   └── promptlib/         prompts + the agent harness itself
├── sprints/
│   ├── 01-faithfulness/ … 10-capstone/
└── results/               same schema everywhere → capstone comparison possible
```

**Planned breakouts** (create only once earned, never on day one):
- `evalkit` → standalone ~sprint 4, once it handles both RAG and voice
- `telephony-voice-bench` → after sprint 4, if the domain benchmark holds up. This becomes the paper.

---

## 9. Rules

**Delegation boundary.** Agents do implementation, breadth, volume. You do specification, verification, diagnosis.

- **Spec before code, always.** ADR + numeric eval criteria before any agent touches the repo.
- **Anything an agent produces that you can't explain line by line doesn't reach `main`.** Not "reviewed" — explained.
- **One component per sprint built unassisted.** The 70/30 rep. Listed per sprint above.

**Tool split.** Claude Code for repo-wide work and ADR-to-scaffold. Codex for async batch sweeps and test-case generation. Cursor for tight loops where you're in the code.

**Production bar — nothing ships without all five:**
1. A regression test that fails when the technique breaks
2. p50/p95 latency
3. Cost per operation
4. Explicit failure-mode section
5. Documented rollback or degradation path

**Atrophy monitor** — three lines in `logbook.md` per sprint:
- What I delegated that I could not have written myself
- What the agent got wrong that I caught — and what I only caught late
- Root cause of the ugliest bug, and whether I found it or the agent did

If line one grows while line three keeps saying "the agent found it," you're getting faster and thinner. Catch it at sprint 4, not sprint 10.

---

## 10. Before 4 August

Higher priority than the first post. Content drives traffic to a profile; if the profile doesn't convert, the traffic is wasted.

- [ ] Create `paper-to-production` — public, tagline as description, all 11 topics set
- [ ] Blog series index page live at `saran.build/paper-to-production` (can be near-empty; it just needs to exist before post 1 links to it)
- [ ] LinkedIn headline that says what you *do*: "Applied AI engineer — voice agents, RAG evaluation, production LLM systems" ≫ "Founder | AI Enthusiast"
- [ ] LinkedIn Featured section pinned to the repo
- [ ] GitHub profile README as portfolio index, not a stats widget
- [ ] Oratolabs case study page — architecture, call volume, cost per call, task completion rate, what broke
- [ ] Work-with-me page — Audit / Build / Retain, with a booking link

---

## 11. Week one

| When | What |
|---|---|
| Tue 28 Jul | `decisions/ADR-001.md` — context, options, decision, consequences, revisit-if. Numeric eval criteria. Then repo skeleton. Then 30–50 listing docs. **Code only after the spec exists.** |
| Wed–Fri | Baseline RAG · claim decomposition (by hand) · faithfulness scoring · ~75 labelled cases |
| Sat 1 Aug | RAGAS comparison · judge validation run (MVVP) · cost/latency numbers · ADR-001 finalised. **Morning: the conversion layer above.** |
| Sun 2 Aug | Draft post |
| Tue 4 Aug | Publish 5:30pm → thread 6:30pm |
| Wed 5 Aug | LinkedIn 8:30am |

Test set composition (~75–100 cases): fully supported · partially supported · contradictory · correct-but-unsupported · poor-retrieval · wrong price or feature · facts merged across two properties.

---

## 12. Checkpoints

**By 18 Aug (post 2 live):** ≥20 outbound messages sent. If not, that's the thing to fix — not the paper count. Content is the easier half of this by a long way, and the lab expanding to fill the space is the predictable failure mode.

**Mid-Oct:** if no contract has landed and you're going all-in on visibility, weekly builds become defensible — you'd have the hours. Revisit with real data on what sprints 1–5 actually cost.

**Sprint 4 (mid-Sep):** decide whether the telephony benchmark is real. If yes, dataset expansion Oct–Nov, write Dec–Jan, submit Jan–Feb.
