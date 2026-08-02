# Logbook

Failures, root causes, and the atrophy monitor. One block per build.

---

## Build 01 — Faithfulness

**Dates:** 2026-07-28 → 2026-07-30 (implementation pass)

### Atrophy monitor

- What I delegated that I could not have written myself: scaffolding volume (fixtures generator, CLI wiring); I must still own atomic decompose judgment by hand.
- What the agent got wrong that I caught — and what I only caught late: heuristic false positives when context union hid entity binding; fixture expected_max needed tightening.
- Root cause of the ugliest bug, and whether I found it or the agent did: decimal price token split (`1.8` → `1`/`8`) — caught in CLI smoke, fixed in verify normalize.

### Failures / notes

- RAGAS library compare not installed in CI (`ragas_available=False`) — optional `[ragas]` extra.
- Heuristic κ on seed can look perfect (1.0) because labels were written to match heuristic-friendly claims — LLM mode + hand labels are the real audit.
- Grow `labelled_v1.json` toward 75+ with human spot-checks before publish.
