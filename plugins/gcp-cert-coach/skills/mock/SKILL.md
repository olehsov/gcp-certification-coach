---
name: mock
description: Use whenever a Google Cloud certification learner wants a mock exam, a full-length practice exam or an exam simulation ("full mock exam", "practice exam like the real one"), asks whether they are ready to book the exam, answers a question of a mock in progress ("question 12 of 50: C, confidence 3"), or reports practice-exam results to get a verdict. Use it even when it seems simple to answer directly: this skill weights questions by the official exam-guide sections, reads the learner's tracker and saves the result. Runs a 50-question mock with GCP Certification Coach, one question at a time with a confidence rating and no answers until the end, then a per-section breakdown, the weakest concepts and a red, amber or green recommendation about booking the exam, saved to the tracker in one batch. Not for short practice sessions or single questions (use quiz), hands-on tasks (use challenge) or explanations (use learn).
---

# Mock exam

A realistic rehearsal: 50 questions, exam pacing, no feedback until the end, then an honest recommendation. Advice only; never a prediction of the real result.

## When to use

- A full mock exam, or continuing one in progress in this conversation.
- Not for short sessions (quiz).

## Preconditions

- A tracker (see Tracker access). Without one, a mock can still run; results are shown but not saved.
- Web search or fetch for documentation to ground answer keys.

## Workflow

```
- [ ] 1. Read settings, tree, previous mocks; warn if coverage is low
- [ ] 2. Plan 50 questions by section weight
- [ ] 3. Ask questions one at a time; record answers and confidence; reveal nothing
- [ ] 4. Grade, compute section scores and the verdict
- [ ] 5. Write everything in one batch at the end
- [ ] 6. Report and next steps
```

1. **Read** `meta/settings`, `modules`, `concepts`, `mocks`, open `misconceptions`. The mock covers every exam-relevant module of the current mode, completed or not, because the real exam does. If fewer than half of the exam-relevant modules are completed, say the result will mostly show untouched material and ask whether to continue or quiz first.
2. **Plan** with [references/mock-exam.md](references/mock-exam.md): question counts per section by official weight (largest remainder), concepts spread across modules mapped to each section, formats mostly `scenario` and `multi_select`, difficulty mix about 30% easy, 50% medium, 20% hard. Mock id: `mock-<YYYY-MM-DD>-<4 random letters>`.
3. **Ask** one question at a time: "Question n of 50 · Section x", the question in English, options, and a request for the answer and confidence (1 guess, 2 think, 3 sure). After each answer reply only "Recorded." plus the next question; never say whether an answer was right. Keep each question, key, documentation URL, answer and confidence in the conversation. The learner may pause and continue later in the same conversation; offer that every 10 questions.
4. **Grade** at the end: per question correct or not; per section `{questions, correct}`; `percent` overall. Verdict from the profile `settings.scoring.profiles[difficulty].mock`:
   - green: `percent ≥ greenMinPercent` and, when `greenConsecutive` is 2, the previous mock was also at or above it;
   - amber: `percent ≥ amberMinPercent` and not green;
   - red: below `amberMinPercent`.
5. **Write** after grading, as one batch (if the data tool limits batch size, send consecutive batches right away with the `mocks` document last): for every question a `log` entry (`kind: "mock"`, `mockId`, full question, key, given, correct, confidence, `docUrl`, `levelBefore`, `levelAfter`), the concept updates computed question by question with the normal scoring rules (effective level, update formula, daily gain cap, misconceptions; see the mock-exam reference), and `mocks/<mockId>`: `{ts, questions: 50, correct, percent, bySection, durationMinutes, verdict}`.
6. **Report**: overall percent and verdict with its rule ("Hard: green needs 80% in two mocks in a row"), a section table (questions, correct, percent, official weight), the 5 weakest concepts, misconceptions created, then the answer review: for each wrong answer the key, a one-line reason and a documentation link (offer the full review of all 50 on request). End with next steps (quiz the weakest sections, learn specific topics, re-take a mock after N days) and the reminder that this is advice, not a pass prediction.

## Output format

Question messages are short and identical in structure. The final report uses tables for sections and wrong answers. Questions and product names in English; the rest in the learner's language.

## Tracker access

- **Locate:** a line `GCP Cert Coach tracker: <URL> (certification: <id>)` in the Project instructions or this conversation; otherwise the learner's artifact list, titles ending in "Cert Coach" (one: use it; several: ask which certification; none: offer `/gcp-cert-coach:init`). Never create a tracker here.
- **Schema:** if `meta/settings.schemaVersion` is above 1, ask the learner to update the plugin; below 1, suggest `/gcp-cert-coach:rebuild`.
- **Writes:** only at the end, as described. Pass the version you read for each concept you update; on a version conflict re-read that concept once, recompute and redo; if it fails again, stop and report what was not saved.
- **No data tool or database unavailable:** run the mock and report; say nothing was saved and show the `mocks` document and a short list of the concept changes as JSON.

## Feedback

When the learner disputes a question, check it against the documentation, correct the grading if the key was wrong, and write `feedback/<timestamp>-<4 random letters>` with `{ts, source: "learner", kind: "wrong_question", text, logId, pluginVersion: settings.pluginVersion, status: "new"}` (neutral text, no personal data). Tell the learner it was recorded.

## Failure handling

- The conversation ends before question 50: nothing is written. When the learner returns in the same conversation, continue; in a new conversation, start a new mock.
- The learner wants to stop early: offer to grade the questions answered so far as a partial mock (`questions` = number answered, verdict marked "partial, not comparable") or to discard it.
