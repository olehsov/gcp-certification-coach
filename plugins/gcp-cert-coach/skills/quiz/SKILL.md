---
name: quiz
description: Runs exam-style practice questions for Google Cloud certification prep with GCP Certification Coach: one question at a time on modules the learner completed, a confidence rating (1 guess, 2 think, 3 sure), an explanation of every option with an official documentation link, and mastery, misconception and review updates in the tracker; also 5-question pre-tests on the next module (no level change) and warm-ups after a break. Use this skill whenever a Google Cloud learner wants to be quizzed or tested ("quiz me", "test me on IAM roles", "practice questions", "next question", "pre-test", "I'm back, let's practice"), replies to a quiz question with a letter and a confidence ("B, confidence 2"), or says a practice question or its answer key was wrong. Not for a full 50-question mock exam (use mock), hands-on tasks (use challenge) or explanations without testing (use learn).
---

# Quiz

Short practice sessions that measure real knowledge: only completed material, confidence-weighted scoring, no repeated questions, every answer grounded in documentation.

## When to use

- Practice questions, pre-tests on the next module, the learner's answer to a question asked earlier, disputes about a question.
- Not for mock exams (mock), hands-on challenges (challenge) or plain explanations (learn).

## Preconditions

- A tracker (see Tracker access). Without one, offer `/gcp-cert-coach:init`; if the learner wants questions anyway, ask which topics they completed and say nothing will be saved.
- Web search or fetch for documentation.

## Workflow

```
- [ ] 1. Locate the tracker; read settings, tree, misconceptions, recent log
- [ ] 2. Resume a pause (warm-up if the break was long)
- [ ] 3. Choose the session type and the concepts
- [ ] 4. For each question: fetch docs, ask, wait for answer + confidence
- [ ] 5. Score, explain every option, write one batch
- [ ] 6. Session summary
```

1. **Read.** `meta/settings` (mode, difficulty, language, scoring), `activities`, `modules`, `concepts`, open `misconceptions`, and `log` entries for the candidate concepts (all their question texts, to avoid repeats). Take every constant from `settings.scoring`; use the defaults in [references/scoring.md](references/scoring.md) only for missing keys and suggest `/gcp-cert-coach:rebuild`.
2. **Pause.** If `settings.paused` is set, resume automatically: in the same batch as the first answer (or alone, before the first question) set `paused: null`, add the paused days to `pausedDaysTotal` and append `{since, until: today}` to `pauseHistory`. Tell the learner the plan resumed. If the pause lasted more than `session.warmupAfterPauseDays` days, this session is a **warm-up**: `session.warmupQuestions` questions on the highest effective-level concepts, scored normally.
3. **Session type and selection** — follow [references/selection.md](references/selection.md):
   - **Normal** (default, `session.defaultQuestions` questions): only exam-relevant concepts of completed, non-archived modules (plus gap topics in Full exam mode), in the priority order: open misconception, never asked, due or overdue, lowest effective level.
   - **Pre-test**: on request, `session.pretestQuestions` questions on the next uncompleted module; logged as `kind: "pretest"`, no level change.
   - **Uncompleted module requested**: warn that the module is not marked completed and offer three choices: mark it completed first (then normal scoring), a pre-test (no level change), or quiz anyway with normal scoring. Proceed only after the learner chooses.
4. **Ask.** For each question, fetch the concept's documentation (its `docUrls`, else a search restricted to `docs.cloud.google.com` and `cloud.google.com`), then write one original question in exam style following [references/question-formats.md](references/question-formats.md). Show one question at a time with its number ("2 of 5"), and ask for the answer and a confidence: **1 guess, 2 think, 3 sure**. Never reveal the key before the answer. If the learner answers without a confidence, ask for it before scoring.
5. **Score and explain.** Apply [references/scoring.md](references/scoring.md): effective level, update formula, daily gain cap, misconception rules. Then reply with: correct or not; why the key is right; why **each** other option is wrong; the source link; the level change (before → after, and "no gain for a correct guess" when that applies); a misconception line when one was created or resolved. Write **one batch** right away (concept update, log entry, misconception create or update, pause resume if pending). Then ask the next question.
6. **Summary.** After the last question: score, level changes per concept, module status changes (for example practicing → ready), open misconceptions, and one suggestion (next session, review a concept, or learn a topic).

## Output format

- Question message: a header line ("Question 2 of 5 · <concept title> · <difficulty>"), the question in English, the options as A–D (or a numbered list for multi-select), and one line asking for the letter(s) and confidence 1/2/3, in the learner's language.
- Feedback message: verdict, explanation per option, documentation link(s), level line. Product names and question text stay in English; explanations are in the learner's language.

## Tracker access

- **Locate:** a line `GCP Cert Coach tracker: <URL> (certification: <id>)` in the Project instructions or this conversation; otherwise the learner's artifact list, titles ending in "Cert Coach" (one: use it; several: ask which certification; none: offer `/gcp-cert-coach:init`). Never create a tracker here.
- **Schema:** if `meta/settings.schemaVersion` is above 1, ask the learner to update the plugin; below 1, suggest `/gcp-cert-coach:rebuild`.
- **Writes:** one batch per answer with the artifact data tool. Pass the version you read for each document you update; on a version conflict re-read that document once, recompute and redo; if it fails again, stop and report.
- **No data tool or database unavailable:** keep quizzing. If the conversation contains a tracker export, use it read-only. Say plainly after each answer that nothing was saved, and show the batch you would have written as a JSON code block.

## Feedback

When the learner says a question or key is wrong, check it against the documentation and answer honestly (if the key was wrong, say so, correct the log entry's `correct` and the concept level in the same batch, and apologize briefly). Either way write `feedback/<timestamp>-<4 random letters>` with `{ts, source: "learner", kind: "wrong_question", text, logId, pluginVersion: settings.pluginVersion, status: "new"}`; for other suggestions use `kind: "improvement"` or `"bug"`. Keep `text` neutral and free of personal data, and tell the learner it was recorded.

## Failure handling

- No completed exam-relevant modules: say so, offer a pre-test on the first module or `/gcp-cert-coach:progress` to mark modules.
- Documentation cannot be fetched for a concept: pick another concept; if none can be fetched, ask questions only on facts you can link, and say so.
- The learner stops mid-session: everything answered is already saved; give the summary so far.
