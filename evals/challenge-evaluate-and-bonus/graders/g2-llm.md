---
type: "llm"
weight: 1
---
PASS if the response evaluates each requirement with findings, gives a score between 0 and 1, and if score >= 0.5 computes the bonus as 15 + 10 x score applied to each linked concept (c2-m2-k3 and c4-m2-k2), not subject to the daily cap and capped at 100; and if the score is 1 it resolves the open misconception mc-001. FAIL if the bonus formula is wrong or missing.
