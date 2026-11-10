---
type: "llm"
weight: 1
---
PASS if none of the 5 new questions repeats a question in the log export (same stem or a trivially reworded duplicate of the same scenario), and all 5 come from completed modules (c2-m1, c2-m2, c4-m2). A question that targets the open misconception mc-001 (service account keys) with a new scenario is expected and is not a repeat. FAIL if a new question duplicates a logged scenario or targets c2-m3 / c4-m3 topics.
