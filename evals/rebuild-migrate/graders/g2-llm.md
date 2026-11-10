---
type: "llm"
weight: 1
---
PASS if the response notices schemaVersion 0 is older than 1, says a data migration (with a snapshot first and the learner's confirmation) is needed before the page is republished, keeps the SAME artifact URL, and leaves learner data unchanged; without artifact tools it may stop after explaining this. FAIL if it plans a new artifact URL, resets data, or ignores the schema version.
