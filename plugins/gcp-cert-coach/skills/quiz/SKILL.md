---
name: quiz
description: "Use whenever a Google Cloud certification learner wants to be quizzed, tested or given practice questions on any Google Cloud topic (\"quiz me\", \"test me on IAM roles\", \"practice questions on GKE\", \"pre-test\", \"I'm back, let's practice\"), asks for the next question, answers a practice question with a letter and a confidence (\"B, confidence 2\", \"probably B\"), or says a practice question or its answer key was wrong. Use it even when writing a question directly seems simple: this skill picks concepts from the learner's tracker, scores confidence and records mastery. Runs exam-style questions with GCP Certification Coach one at a time on completed modules, with a confidence rating (1 guess, 2 think, 3 sure), every option explained with an official documentation link, and mastery, misconception and review updates; also 5-question pre-tests on the next module and warm-ups after a break. Not for a full 50-question mock exam (use mock), hands-on tasks (use challenge) or explanations without testing (use learn)."
---

# Quiz

Short practice sessions that measure real knowledge: only completed material, confidence-weighted scoring, no repeated questions, every answer grounded in documentation.

## When to use

- Practice questions, pre-tests on the next module, the learner's answer to a question asked earlier, disputes about a question.
- Not for mock exams (mock), hands-on challenges (challenge) or plain explanations (learn).

## Preconditions

- A tracker (see Tracker access). Without one, offer `/gcp-cert-coach:init`; if the learner wants questions anyway, ask which topics they completed and say nothing will be saved.
- Documentation: the concept's curated `docUrls` first; web fetch only when needed (step 4).
- Numbers in questions come from [references/facts.md](references/facts.md) or a page fetched this session.

## Workflow

```
- [ ] 1. Locate the tracker; read settings, completed modules, their concepts, open misconceptions
- [ ] 2. Resume a pause (warm-up if the break was long)
- [ ] 3. Plan the whole session in one step
- [ ] 4. For each question: ask, wait for answer + confidence
- [ ] 5. Score, explain every option, write one batch
- [ ] 6. Session summary
```

1. **Read selectively, once.** `meta/settings` (mode, difficulty, language, scoring); `modules` with `completed` true (plus the gap topics in Full exam mode); `concepts` for those modules only (filter by `moduleId`, in chunks if the filter has a size limit); open `misconceptions`. Never list the whole `concepts` or `log` collection. After the plan in step 3 has chosen the concepts, read the last 50 `log` entries for those concepts only (for the no-repeat check and the daily gain cap). Take every constant from `settings.scoring`; use the defaults in [references/scoring.md](references/scoring.md) only for missing keys and suggest `/gcp-cert-coach:rebuild`.
2. **Pause.** If `settings.paused` is set, resume automatically: in the same batch as the first answer (or alone, before the first question) set `paused: null`, add the paused days to `pausedDaysTotal` and append `{since, until: today}` to `pauseHistory`. Tell the learner the plan resumed. If the pause lasted more than `session.warmupAfterPauseDays` days, this session is a **warm-up**: `session.warmupQuestions` questions on the highest effective-level concepts, scored normally.
3. **Plan the session** in one step with [references/selection.md](references/selection.md), from what you have read; do not read again per question:
   - **Normal** (default, `session.defaultQuestions` questions): only exam-relevant concepts of completed, non-archived modules (plus gap topics in Full exam mode), in the priority order: open misconception, never asked, due or overdue, lowest effective level. Decide for every question the concept, the format and the difficulty, and keep the plan to yourself.
   - **Pre-test**: on request, `session.pretestQuestions` questions on the next uncompleted module; logged as `kind: "pretest"`, no level change. Say so in the first message ("this pre-test does not change your levels"), and name the module being previewed once, before the first question (the header itself stays topic-free).
   - **Uncompleted module requested**: warn that the module is not marked completed and offer three choices: mark it completed first (then normal scoring), a pre-test (no level change), or quiz anyway with normal scoring. Proceed only after the learner chooses.
4. **Ask.** One question at a time, written from the plan, original, in exam style, following [references/question-formats.md](references/question-formats.md). Ground it in the concept's curated `docUrls` and [references/facts.md](references/facts.md). Fetch a page only when the concept has no `docUrl`, the fact is version-sensitive and not in `facts.md`, or the learner disputes it: at most one fetch per question, with a narrow request for the one fact needed. If the fetch fails, say so and cite the curated link. The question header is **only** `Question N of M · <difficulty>`: never the concept, module or section name, never any topic hint (the header must not reveal the answer). Ask for the answer and a confidence: **1 guess or unsure, 2 fairly confident, 3 sure**. Never reveal the key before the answer.
5. **Read the answer** with [references/answer-parsing.md](references/answer-parsing.md) before any scoring. Hedges ("probably B", "I think", "A or B") are confidence 1. If the message does not name a letter ("the third option", "the Bigtable one"), do not score and do not reveal the key: reply only with the letter you read ("I read that as C, `roles/editor`. Is that your answer?") plus the confidence question if it is missing, and score after the learner confirms. The same goes for unclear wording or a missing confidence.
6. **Score and explain.** Apply [references/scoring.md](references/scoring.md): effective level, update formula, daily gain cap, misconception rules (confidence 1 never creates one). Reply with: correct or not; why the key is right; why **each** other option is wrong; the source link (the curated `docUrl` unless you fetched another); the level change as a bare line ("Level 50 → 57.5", no concept name needed; "no gain for a correct guess" when that applies); a misconception line when one was created or resolved. Write **one batch** right away (concept update, log entry, misconception create or update, pause resume if pending). Then ask the next question.
7. **Summary.** After the last question: score, level changes per concept (naming the concepts is fine now), module status changes (for example practicing → ready), open misconceptions, and one suggestion (next session, review a concept, or learn a topic). If this conversation already holds a finished session summary, add one line: for the next study session a new chat is faster and cheaper; the tracker keeps all state.

## Output format

- Question message: a header line ("Question 2 of 5 · medium" and nothing else), the question in English, the options as A–D (or a numbered list for multi-select), and one line asking for the letter(s) and confidence (1 guess or unsure, 2 fairly confident, 3 sure), in the learner's language.
- Feedback message: verdict, explanation per option, documentation link(s), level line. Product names and question text stay in English; explanations are in the learner's language.

## Tracker access

- **Locate:** a line `GCP Cert Coach tracker: <URL> (certification: <id>)` in the Project instructions or this conversation; otherwise the learner's artifact list, titles ending in "Cert Coach" (one: use it; several: ask which certification; none: offer `/gcp-cert-coach:init`). Never create a tracker here.
- **Version:** Plugin version: 0.3.0. On the `meta/settings` read, compare versions. `schemaVersion` below 1: stop and offer `/gcp-cert-coach:rebuild` first; above 1: ask the learner to update the plugin. `templateVersion` (missing means `pluginVersion`) older than the plugin version: say once per session, in one line, "A new tracker page is available (x → y). Say 'rebuild' to update it."; never rebuild on your own. `latestPluginVersion` older than the plugin version: include it in the settings write this skill makes anyway; never write only for this.
- **Writes:** one batch per answer with the artifact data tool. Pass the version you read for each document you update; on a version conflict re-read that document once, recompute and redo; if it fails again, stop and report.
- **No data tool or database unavailable:** keep quizzing. If the conversation contains a tracker export, use it read-only. Say plainly after each answer that nothing was saved, and show the batch you would have written as a JSON code block.

## Feedback

When the learner says a question or key is wrong, check it against the documentation and answer honestly (if the key was wrong, say so, correct the log entry's `correct` and the concept level in the same batch, and apologize briefly). Either way write `feedback/<timestamp>-<4 random letters>` with `{ts, source: "learner", kind: "wrong_question", text, logId, pluginVersion: settings.pluginVersion, status: "new"}`; for other suggestions use `kind: "improvement"` or `"bug"`. Keep `text` neutral and free of personal data, and tell the learner it was recorded.

## References

- [references/selection.md](references/selection.md): candidates, priority, interleaving, no repeats
- [references/question-formats.md](references/question-formats.md): formats and difficulty
- [references/scoring.md](references/scoring.md): level formulas, cap, misconceptions, batch
- [references/answer-parsing.md](references/answer-parsing.md): letters, hedges, confidence
- [references/facts.md](references/facts.md): verified numeric facts

## Failure handling

- No completed exam-relevant modules: say so, offer a pre-test on the first module or `/gcp-cert-coach:progress` to mark modules.
- A fetch fails: say so and use the curated link; a concept with neither a curated link nor a loadable page is replaced by another concept, and if none works, ask only about facts in `facts.md`, and say so.
- The learner stops mid-session: everything answered is already saved; give the summary so far.
