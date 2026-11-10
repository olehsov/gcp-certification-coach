---
type: "llm"
weight: 1
---
PASS if the response identifies module c2-m3 and FIRST asks a confirmation naming the titles ('Do you mean course 2 Google Cloud Fundamentals: Core Infrastructure, module Virtual Machines and Networks in the Cloud?'); since the learner already named the title in parentheses it may treat the title as given and ask one short confirmation instead. It writes nothing before the learner says yes: it may show the planned update (completed true, completedAt 2026-11-10) as pending and notes it could not be saved without a data tool. FAIL if it marks the module as done or claims the tracker was saved without asking, or picks a different module.
