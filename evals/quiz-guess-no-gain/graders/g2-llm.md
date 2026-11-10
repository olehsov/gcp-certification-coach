---
type: "llm"
weight: 1
---
PASS if the response treats the correct guess as giving no level gain: concept c4-m2-k2 stays at level 50 (levelBefore 50, levelAfter 50, because the confidence multiplier for a guess is 0; the concept is not overdue, so no decay), and it still records the answer (a log entry with confidence 1 and correct true, answers incremented). FAIL if it reports any level increase for this concept.
