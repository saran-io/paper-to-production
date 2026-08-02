# Papers — Canonical Queue

Source of truth for what this repo is reading, building, publishing, parking, or rejecting.

The unit of decision here is not “interesting paper.”  
The unit is “paper that might fix a real production problem.”

## Status legend

- `candidate`: spotted, not yet committed
- `reading`: actively evaluating the paper
- `queued`: accepted for a note or build
- `building`: implementation underway
- `published`: note or build shipped
- `parked`: useful, but not urgent
- `rejected`: not worth implementation for this repo

## Intake checklist

Before adding a paper to the queue, write down:

1. The production issue
2. The implementation slice
3. The metric that would prove or disprove it
4. The likely reason it might fail in practice

If those four fields are weak, the paper stays out of the active queue.

## Active queue

| Status | Paper | Problem to fix | Planned output | Notes |
|---|---|---|---|---|
| `building` | RAGAS: Automated Evaluation of RAG ([2309.15217](https://arxiv.org/abs/2309.15217)) | unsupported RAG answers | Build 01 | core faithfulness loop |
| `building` | FActScore ([2305.14251](https://arxiv.org/abs/2305.14251)) | coarse decomposition hides hallucinations | Build 01 | atomic claim discipline |
| `building` | Reliability without Validity ([2606.19544](https://arxiv.org/abs/2606.19544)) | judge metrics can overstate confidence | Build 01 | κ and MVVP-lite audit |
| `queued` | Voice Activity Projection ([2205.09812](https://arxiv.org/abs/2205.09812)) | caller cutoffs from naive silence thresholds | Build 02 | endpointing teardown |
| `queued` | Next-Turn ([2606.18094](https://arxiv.org/abs/2606.18094)) | late turn detection in streaming voice | Build 02 | supporting comparison |
| `queued` | Semantic VAD ([2305.12450](https://arxiv.org/abs/2305.12450)) | semantic end-of-turn detection | Build 02 | supporting comparison |
| `queued` | Moshi ([2410.00037](https://arxiv.org/abs/2410.00037)) | slow voice response loops | Build 03 | streaming reference point |
| `queued` | Speculative decoding ([2211.17192](https://arxiv.org/abs/2211.17192)) | time-to-first-token / time-to-first-audio | Build 03 | serving lever |
| `queued` | PagedAttention / vLLM ([2309.06180](https://arxiv.org/abs/2309.06180)) | serving inefficiency | Build 03 | serving lever |
| `queued` | Full-Duplex-Bench v1 ([2503.04721](https://arxiv.org/abs/2503.04721)) | weak voice-agent evaluation | Build 04 | benchmark shape |
| `queued` | Dense Passage Retrieval ([2004.04906](https://arxiv.org/abs/2004.04906)) | unclear retrieval tradeoffs | Build 05 | decision table |
| `queued` | ColBERT ([2004.12832](https://arxiv.org/abs/2004.12832)) | retrieval quality vs latency tradeoff | Build 05 | late interaction comparison |
| `queued` | Contextual Retrieval ([anthropic.com](https://www.anthropic.com/news/contextual-retrieval)) | chunk context loss | Build 06 | chunking benchmark |
| `queued` | Late Chunking ([2409.04701](https://arxiv.org/abs/2409.04701)) | bad boundary behavior | Build 06 | chunking comparison |
| `queued` | LoRA ([2106.09685](https://arxiv.org/abs/2106.09685)) | extraction quality ceiling | Build 07 | fine-tune baseline |
| `queued` | QLoRA ([2305.14314](https://arxiv.org/abs/2305.14314)) | fine-tune cost pressure | Build 07 | lower-cost path |
| `queued` | Efficient Guided Generation ([2307.09702](https://arxiv.org/abs/2307.09702)) | invalid structured outputs | Build 07 | constrained decoding path |
| `queued` | The Harness Effect ([2607.06906](https://arxiv.org/abs/2607.06906)) | agent improvements attributed to the wrong lever | Build 08 | anchor paper |
| `queued` | Not what you've signed up for ([2302.12173](https://arxiv.org/abs/2302.12173)) | indirect prompt injection risk | Build 09 | attack framing |
| `queued` | Llama Guard ([2312.06674](https://arxiv.org/abs/2312.06674)) | weak guardrails for untrusted docs | Build 09 | defense path |

## Season 1 build map

| Sprint | Problem | Primary papers |
|---|---|---|
| 01 Faithfulness | unsupported answers in RAG | RAGAS, FActScore, Reliability without Validity |
| 02 Endpointing | caller interruption and turn latency | Voice Activity Projection, Next-Turn, Semantic VAD |
| 03 Streaming | slow voice loop | Moshi, speculative decoding, PagedAttention |
| 04 Voice eval | no convincing domain benchmark | Full-Duplex-Bench family, τ-Voice |
| 05 Retrieval | retrieval choice without decision discipline | DPR, ColBERT |
| 06 Chunking | retrieval failure from chunk boundaries | Contextual Retrieval, Late Chunking |
| 07 Extraction | prompt vs tune vs decode tradeoff | LoRA, QLoRA, Efficient Guided Generation |
| 08 Agent harness | harness claims without measurement | The Harness Effect and related harness papers |
| 09 Prompt injection | unsafe RAG on third-party docs | Greshake et al., Llama Guard |
| 10 Capstone | integrate all decisions | revisit all prior ADRs |

## Reading pool

These are in scope, but not yet committed to a build implementation.

| Status | Paper | Why it matters |
|---|---|---|
| `candidate` | G-Eval ([2303.16634](https://arxiv.org/abs/2303.16634)) | judge design reference |
| `candidate` | Judging LLM-as-a-Judge ([2306.05685](https://arxiv.org/abs/2306.05685)) | evaluator framing |
| `candidate` | Self-RAG ([2310.11511](https://arxiv.org/abs/2310.11511)) | retrieval/control loop ideas |
| `candidate` | HyDE ([2212.10496](https://arxiv.org/abs/2212.10496)) | retrieval query strategy |
| `candidate` | Always-On Agents survey ([2606.30306](https://arxiv.org/abs/2606.30306)) | background for long-running agents |
| `candidate` | AgingBench ([2605.26302](https://arxiv.org/abs/2605.26302)) | long-horizon reliability |
| `candidate` | Metacognition in LLMs ([2607.11881](https://arxiv.org/abs/2607.11881)) | reasoning about self-check claims |
| `reading` | Testing Retrieval-Augmented Generation Systems with Chunk Coverage ([2607.18155](https://arxiv.org/abs/2607.18155)) | suite-level retrieval test adequacy for Build 06 |
| `reading` | VAmoS Bench: Voice Agent Simulation Bench ([2607.27453](https://arxiv.org/abs/2607.27453)) | end-to-end containment benchmark shape for Build 04 |
| `reading` | RAGuard ([2607.26339](https://arxiv.org/abs/2607.26339)) | corpus-poisoning defense candidate for future prompt-injection / RAG safety work |

## Parked / buffer

Interesting papers that may become active when a real repo problem demands them.

| Status | Paper | Why parked |
|---|---|---|
| `parked` | FrugalGPT ([2305.05176](https://arxiv.org/abs/2305.05176)) | useful only if routing becomes an active cost bottleneck |
| `parked` | RouteLLM ([2406.18665](https://arxiv.org/abs/2406.18665)) | same reason as above |
| `parked` | When Is Routing Meaningful ([2607.09197](https://arxiv.org/abs/2607.09197)) | only matters after routing experiments exist |
| `parked` | Semantic entropy ([Nature](https://www.nature.com/articles/s41586-024-07421-0)) | useful if abstention becomes a top-level product requirement |
| `parked` | Failure as a Process ([2607.09510](https://arxiv.org/abs/2607.09510)) | promote if Build 08 needs deeper failure attribution |
| `parked` | OAT ([2607.12747](https://arxiv.org/abs/2607.12747)) | same as above |
| `parked` | Agent Limitations Taxonomy ([2607.05775](https://arxiv.org/abs/2607.05775)) | same as above |

## Out of scope by default

These do not belong in the active queue unless they change a real decision in this repo.

- foundations tourism
- broad “understand all LLMs” curricula
- robotics / VLA / world models without a direct repo use case
- paper collections that do not change an implementation decision

## Add a new paper

Use this row format when a new paper arrives:

| Status | Paper | Problem to fix | Planned output | Notes |
|---|---|---|---|---|
| `candidate` | Paper title ([id](https://arxiv.org/abs/...)) | one production issue | note / build / offcut | why it matters now |
