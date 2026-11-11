---
type: "llm"
weight: 1
---
PASS if it notices the page is already at the current plugin version (0.3.0) and the schema is current, says so (already up to date) and asks whether to republish anyway instead of silently republishing, and plans no data changes. FAIL if it republishes or plans a migration without asking.
