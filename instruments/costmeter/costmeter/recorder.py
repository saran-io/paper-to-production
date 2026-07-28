"""Record and aggregate CostEvents."""

from __future__ import annotations

import json
import statistics
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterator

from costmeter.schema import CostEvent

# Rough public list prices (USD / 1M tokens). Override via metadata if needed.
_DEFAULT_PRICES_PER_1M: dict[str, tuple[float, float]] = {
    "gpt-4o-mini": (0.15, 0.60),
    "gpt-4o": (2.50, 10.00),
    "gpt-4.1-mini": (0.40, 1.60),
}


def estimate_cost_usd(
    model: str | None,
    input_tokens: int,
    output_tokens: int,
    prices: dict[str, tuple[float, float]] | None = None,
) -> float:
    prices = prices or _DEFAULT_PRICES_PER_1M
    if not model:
        return 0.0
    key = model.lower()
    pair = None
    for name, p in prices.items():
        if name in key:
            pair = p
            break
    if pair is None:
        return 0.0
    inp, out = pair
    return (input_tokens / 1_000_000.0) * inp + (output_tokens / 1_000_000.0) * out


@dataclass
class OperationRecord:
    event: CostEvent


@dataclass
class CostMeter:
    sprint: str
    events: list[CostEvent] = field(default_factory=list)

    def record(self, event: CostEvent) -> CostEvent:
        event = event.with_totals()
        self.events.append(event)
        return event

    @contextmanager
    def track(
        self,
        operation: str,
        *,
        model: str | None = None,
        provider: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Iterator[dict[str, Any]]:
        """Context manager that fills latency; caller sets token counts on the handle."""
        handle: dict[str, Any] = {
            "input_tokens": 0,
            "output_tokens": 0,
            "cost_usd": None,
            "metadata": dict(metadata or {}),
            "success": True,
            "error": None,
            "model": model,
            "provider": provider,
        }
        start = time.perf_counter()
        try:
            yield handle
        except Exception as exc:  # noqa: BLE001 — record then re-raise
            handle["success"] = False
            handle["error"] = str(exc)
            raise
        finally:
            latency_ms = (time.perf_counter() - start) * 1000.0
            in_tok = int(handle.get("input_tokens") or 0)
            out_tok = int(handle.get("output_tokens") or 0)
            cost = handle.get("cost_usd")
            if cost is None:
                cost = estimate_cost_usd(handle.get("model") or model, in_tok, out_tok)
            self.record(
                CostEvent(
                    sprint=self.sprint,
                    operation=operation,
                    model=handle.get("model") or model,
                    provider=handle.get("provider") or provider,
                    input_tokens=in_tok,
                    output_tokens=out_tok,
                    cost_usd=float(cost or 0.0),
                    latency_ms=latency_ms,
                    success=bool(handle.get("success", True)),
                    error=handle.get("error"),
                    metadata=dict(handle.get("metadata") or {}),
                )
            )

    def total_cost_usd(self) -> float:
        return sum(e.cost_usd for e in self.events)

    def latency_ms_values(self, operation: str | None = None) -> list[float]:
        vals = [
            e.latency_ms
            for e in self.events
            if operation is None or e.operation == operation
        ]
        return vals

    def percentile(self, values: list[float], p: float) -> float | None:
        if not values:
            return None
        if len(values) == 1:
            return values[0]
        ordered = sorted(values)
        k = (len(ordered) - 1) * (p / 100.0)
        f = int(k)
        c = min(f + 1, len(ordered) - 1)
        if f == c:
            return ordered[f]
        return ordered[f] + (ordered[c] - ordered[f]) * (k - f)

    def summary(self) -> dict[str, Any]:
        lat = self.latency_ms_values()
        return {
            "sprint": self.sprint,
            "n_events": len(self.events),
            "total_cost_usd": round(self.total_cost_usd(), 6),
            "total_tokens": sum(e.total_tokens for e in self.events),
            "latency_ms_p50": self.percentile(lat, 50),
            "latency_ms_p95": self.percentile(lat, 95),
            "latency_ms_mean": statistics.mean(lat) if lat else None,
        }

    def dump_jsonl(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            for event in self.events:
                f.write(event.model_dump_json() + "\n")
