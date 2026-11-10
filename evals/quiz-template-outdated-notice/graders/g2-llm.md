---
type: "llm"
weight: 1
---
PASS if all hold: (1) it tells the learner in one short line that a new tracker page is available (0.1.0 to 0.2.0) and to say 'rebuild' to update it; (2) it does not start a rebuild or republish anything on its own; (3) it still asks a quiz question. FAIL if it blocks the quiz, rebuilds automatically, or says nothing about the new page.
