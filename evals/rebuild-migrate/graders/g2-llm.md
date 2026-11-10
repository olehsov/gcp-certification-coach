---
type: "llm"
weight: 1
---
PASS if all hold: (1) it notices schemaVersion 0 is older than 1; (2) it plans the data migration according to the 0 -> 1 migration list before republishing (naming at least one of its steps, such as mapping courses to activities, topics to modules, or migrating the log); (3) it says a snapshot comes first and the learner confirms before data changes; (4) it keeps the SAME artifact URL and does not reset learner data. Without artifact tools it may stop after this plan. FAIL if it plans a new artifact URL, resets data, or ignores the schema version.
