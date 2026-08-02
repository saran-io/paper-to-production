# VAmoS Bench: Voice Agent Simulation Bench (2607.27453)

Date read: 2026-08-02
Time spent:
Status: `reading`
Source date: 2026-07-29
Source link: https://arxiv.org/abs/2607.27453

## Production issue

Voice-agent evaluation can overfocus on WER, latency, and turn-taking while missing the main production question: did the system safely resolve the call without fake success or unsafe disclosure?

## Core claim

An end-to-end simulated phone benchmark with backend state, binary assertions, and adversarial scenarios is a better measure of production voice-agent quality than component metrics alone.

## What I would implement

Borrow the benchmark shape for Sprint 04: a stateful caller simulator, a tool-backed domain backend, and a grader that checks both spoken behavior and side effects against scenario assertions.

## What would have to be true

I would need a narrow domain, a controllable backend, scenario-specific assertions, and a way to replay or simulate audio interactions cheaply enough to run regression checks.

## What I would measure

Containment and assertion pass rate per scenario, plus safe redirect or refusal correctness on adversarial calls.

## Failure modes / reasons to reject

The current benchmark is banking-specific, and building a realistic simulator may cost more than the first repo sprint can absorb. A brittle simulator could create benchmark theater instead of useful evidence.

## Verdict

`BORROW`

## What changes the verdict

Upgrade to `BUILD` if Sprint 04 needs a domain-specific end-to-end benchmark and I can implement a minimal simulator quickly. Downgrade to `PARK` if simpler eval slices already surface the same failures.
