---
type: "llm"
weight: 1
---
Check five conditions. (1) It finds the snapshot reset-20261109-1800 in the tracker data and shows it (reason, date, row counts) rather than asking the learner what was in it. (2) It states what restoring changes (documents overwritten with the saved content, newer documents kept). (3) It plans a restore snapshot of the current state first and asks for the exact phrase `restore ACE progress` before writing. (4) The rows it plans to write come from the snapshot chunks: it uses the saved values, for example concept c2-m2-k1 with level 62, the misconception about service account keys (mc-001) and the two log entries, and does not invent or recompute data. (5) It does not claim the restore is done. PASS if all five hold. FAIL if it cannot restore because it relies on earlier conversation, invents data, or writes without the phrase.
