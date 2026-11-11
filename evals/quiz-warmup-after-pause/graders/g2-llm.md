---
type: "llm"
weight: 1
---
PASS if the response notices the plan is paused since 2026-10-25 (16 days, more than 7), resumes it automatically (it says the plan resumed; in read-only mode it may say the resume would be recorded), and starts a warm-up (shorter, scored normally) with a first question on a topic the learner already knows well (Resource hierarchy or IAM, the highest levels in the export). FAIL if it ignores the pause, asks the learner to unpause manually first, or starts on a concept the learner has not answered before.
