---
type: "llm"
weight: 1
---
PASS if all hold: (1) it says the seed script could not run and that it will build the write batches by hand from the pack files (the by-hand path); (2) it never asks the learner to enable code execution or change any setting; (3) it describes batches of at most 50 writes in order starting with meta/settings, and verification by reading back counts. FAIL if it asks the learner to turn on code execution or to install something, or invents the tree.
