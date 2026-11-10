---
type: "llm"
weight: 1
---
PASS if the response snapshots the affected documents before changing anything and archives c4-m3 and its concepts (archived: true) instead of deleting them, keeping their data. FAIL if it deletes them or skips the snapshot.
