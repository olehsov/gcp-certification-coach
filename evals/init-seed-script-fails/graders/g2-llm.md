---
type: "llm"
weight: 1
---
Check three conditions. (1) The response says the seed script could not run (or that the batches are built without it) and that the write batches are built by hand from the pack files. (2) The response does not ask the learner to enable code execution, install anything or change any setting; telling the learner that publishing needs claude.ai or the desktop app does not count as asking for a setting change. (3) The response describes batches of at most 50 writes written in order, with meta/settings first, and a read-back check of the counts. PASS if all three hold. FAIL if any one fails, or the tree is invented.
