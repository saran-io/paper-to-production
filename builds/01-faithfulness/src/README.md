# Sprint 01 — source

Python package: `faithfulness`

| Module | Role |
|---|---|
| `decompose.py` | Atomic claims (heuristic + LLM) |
| `verify.py` | Claim vs context (heuristic + LLM) |
| `score.py` | `|V|/|S|` |
| `metrics.py` | Cohen's κ + raw agreement |
| `pipeline.py` | End-to-end + costmeter |
| `cli.py` | `faithfulness fixtures` / `faithfulness one` |

## Quick start

```bash
# from repo root
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

pytest -q

# heuristic run on seed fixtures (no API key)
faithfulness fixtures --mode heuristic

# LLM mode (needs OPENAI_API_KEY)
pip install -e ".[dev,llm]"
faithfulness fixtures --mode llm
```
