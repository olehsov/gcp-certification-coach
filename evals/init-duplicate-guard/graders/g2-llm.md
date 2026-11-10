---
type: "llm"
weight: 1
---
PASS if the response notices that an ACE tracker already exists (the tracker line / export) and does NOT start creating or publishing a second tracker; instead it offers to keep using the existing one and asks for explicit confirmation before creating another. FAIL if it starts the setup flow or publishes a tracker without that confirmation.
