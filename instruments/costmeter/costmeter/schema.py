"""Cost/latency event schema (OTel GenAI-inspired field names)."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, Field


class CostEvent(BaseModel):
    """One timed LLM (or pipeline) operation.

    Field names lean on OpenTelemetry GenAI conventions where practical:
    gen_ai.operation.name, gen_ai.request.model, gen_ai.usage.*
    """

    schema_version: Literal["costmeter.v1"] = "costmeter.v1"
    sprint: str
    operation: str  # e.g. faithfulness.decompose
    model: str | None = None
    provider: str | None = None

    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0

    cost_usd: float = 0.0
    latency_ms: float = 0.0

    success: bool = True
    error: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    ts: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def with_totals(self) -> CostEvent:
        total = self.input_tokens + self.output_tokens
        if self.total_tokens == 0 and total > 0:
            return self.model_copy(update={"total_tokens": total})
        return self
