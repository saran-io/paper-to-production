# instruments/costmeter

Uniform cost + latency schema used by **every** sprint.

Starts in Sprint 01. Capstone cross-sprint comparison only works if this schema stays stable.

## Goals

- One record shape for tokens, $, wall time, model id, operation name
- OpenTelemetry GenAI semantic conventions where applicable
- Results readable by `results/` aggregators without per-sprint adapters

## Status

Scaffold — schema lands with Sprint 01 implementation.
