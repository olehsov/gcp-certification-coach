---
type: "llm"
weight: 1
---
PASS if the response reads the current settings, notices schemaVersion 0 is older than 1, plans a data migration according to the migration list before republishing, and republishes the template to the SAME artifact URL without changing learner data. FAIL if it creates a new artifact URL or resets data.
