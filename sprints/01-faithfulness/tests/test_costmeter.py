"""costmeter unit tests."""

from costmeter import CostEvent, CostMeter
from costmeter.recorder import estimate_cost_usd


def test_estimate_cost_gpt4o_mini():
    cost = estimate_cost_usd("gpt-4o-mini", input_tokens=1_000_000, output_tokens=0)
    assert abs(cost - 0.15) < 1e-9


def test_track_records_latency():
    meter = CostMeter(sprint="01-faithfulness")
    with meter.track("faithfulness.decompose", model="gpt-4o-mini") as h:
        h["input_tokens"] = 100
        h["output_tokens"] = 20
    assert len(meter.events) == 1
    ev = meter.events[0]
    assert isinstance(ev, CostEvent)
    assert ev.operation == "faithfulness.decompose"
    assert ev.total_tokens == 120
    assert ev.latency_ms >= 0
    assert ev.cost_usd > 0
