# instruments/costmeter

Uniform cost + latency schema used by **every** sprint.

```python
from costmeter import CostMeter

meter = CostMeter(sprint="01-faithfulness")
with meter.track("faithfulness.decompose", model="gpt-4o-mini") as h:
    h["input_tokens"] = 120
    h["output_tokens"] = 40
print(meter.summary())  # p50/p95, total_cost_usd, ...
```

## Schema

`CostEvent` (`costmeter.v1`): sprint, operation, model, tokens, cost_usd, latency_ms, OTel-inspired naming.

## Status

v1 landed with Sprint 01.
