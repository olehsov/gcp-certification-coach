---
type: "llm"
weight: 1
---
PASS if the response shows a diff (added, removed, renamed items) and asks for confirmation before applying anything, and explains that it will snapshot affected data first, archive removed items rather than delete them, and keep data for renamed items. FAIL if it applies changes without asking.
