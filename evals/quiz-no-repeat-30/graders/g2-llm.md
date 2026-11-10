---
type: "llm"
weight: 1
---
PASS if none of the 5 new questions repeats any question text already present in the log export (same stem or a trivially reworded duplicate asking the same thing with the same answer), and all 5 come from completed modules (c2-m1, c2-m2, c4-m2). FAIL if any new question duplicates a logged question or targets c2-m3 / c4-m3 topics.
