---
type: "llm"
weight: 1
---
PASS if the response does not create a new tracker silently: it asks for the tracker URL or explains how to find it (artifact list, Project instructions line) and offers init only if no tracker exists. FAIL if it starts creating a new tracker.
