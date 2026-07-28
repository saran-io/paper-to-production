# Placeholder — faithfulness pipeline

Implement after ADR-001 is locked:

1. `decompose(answer) -> list[Claim]`
2. `verify(claim, contexts) -> bool`
3. `score(verdicts) -> float`  # |V| / |S|
4. Wire through `instruments/costmeter`
5. Compare to human labels → Cohen's κ
