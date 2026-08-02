# Build 01 — Faithfulness evaluator from scratch

**Publish:** Tue 4 Aug 2026 · **Status:** Implementation landed (κ on full set + LLM runs pending your API key)  
**Dir:** `builds/01-faithfulness/`  
**Blog slug:** `faithfulness-from-scratch`

## Papers implemented

| Paper | What we built |
|---|---|
| RAGAS | `decompose → verify → score` pipeline + CLI |
| FActScore | Atomic decompose prompts / heuristic split discipline |
| Reliability w/o Validity | `faithfulness audit` MVVP-lite (κ, replicates, order bias) |

## Quick start

```bash
# from repo root
source .venv/bin/activate
pip install -e ".[dev]"

pytest -q

# CI seed fixtures (8 cases)
faithfulness fixtures --mode heuristic

# Labelled set (~53 cases from 30 listings)
faithfulness fixtures \
  --fixtures instruments/datasets/faithfulness/fixtures/labelled_v1.json \
  --no-check-expected \
  --out builds/01-faithfulness/results/labelled_run.json

# MVVP-lite judge audit
faithfulness audit --mode heuristic --max-examples 12

# Optional: RAGAS library delta (needs pip install '.[ragas]' + API key)
faithfulness compare --mode llm --fixtures instruments/datasets/faithfulness/fixtures/seed_cases.json
```

## Layout

```
src/faithfulness/
  decompose.py   # RAGAS step 1 + FActScore atomicity
  verify.py      # RAGAS step 2
  score.py       # |V|/|S|
  metrics.py     # Cohen's κ
  mvvp.py        # MVVP-lite audit
  compare_ragas.py
  pipeline.py
  cli.py
```

## Data

| Path | Contents |
|---|---|
| `instruments/datasets/listings/` | 30 property listings |
| `.../fixtures/seed_cases.json` | 8 CI / regression cases |
| `.../fixtures/labelled_v1.json` | ~53 labelled cases (grow toward 75–100) |

## Production bar

- [x] Regression: hallucination must not score fully faithful
- [x] p50/p95 + cost via `costmeter`
- [x] MVVP-lite audit command
- [x] RAGAS compare hook (optional deps)
- [ ] Fill κ with `--mode llm` on labelled set (needs `OPENAI_API_KEY`)
- [ ] Grow labels to ≥75 hand-checked cases
- [ ] Blog “when I would not use this”
