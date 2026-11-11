---
name: progress
description: "Updates and reports study progress in the GCP Certification Coach tracker. Marks courses, skill badges and modules completed from what the learner types or from their Google Skills or Coursera progress page in the built-in browser (always confirmed before writing), pauses and resumes the plan, changes mode, difficulty, weekly hours or exam date, and reports status, readiness per exam-guide section, the review queue and the study plan with an estimated finish date. Use when the learner says \"I finished module 4 of course 6\", \"mark course 2 done\", \"check my progress on the site\", \"status\", \"how am I doing\", \"what's my plan\", \"when will I finish\", \"pause my plan\", \"I'm back\", \"switch to full exam mode\" or \"make it harder\". Not for setting up a tracker (use init), practice questions (use quiz) or updating the tree from the live path (use sync)."
---

# Progress

Keep the tracker in step with what the learner actually studied, and tell them where they stand.

## When to use

- Marking completion, browser progress checks, pause and resume, settings changes, status and plan questions.
- Not for setup (init), the tree structure itself (sync) or practice (quiz, mock, challenge).

## Preconditions

- A tracker (see Tracker access). Without one, offer `/gcp-cert-coach:init`.
- The built-in browser only for site checks (Claude desktop app).

## Workflow

Pick the branch that matches the request; several can run in one turn.

```
- [ ] 1. Locate the tracker; read settings, then only what the branch needs
- [ ] 2. Run the branch: mark | browser check | pause/resume | settings | status and plan
- [ ] 3. Confirm before any write; write one batch
- [ ] 4. Report and suggest the next step
```

**Mark completion.** Course platforms number modules differently, so a number is never trusted on its own. Resolve what the learner names to ids: "course N" is the N-th activity in path order (`activities.order`), "module M" is the M-th module of that activity, skill badges count as activities. Then **always ask before writing**: "Do you mean course N <course title>, module(s) <module titles>?" and write nothing until a yes. On a "no", ask the learner to type the course and module names, match them by title, confirm the match again, then write. When the learner gives titles instead of numbers, match by title and write after one short confirmation. Then write one batch: `update modules/<id>` with `completed: true`, `completedAt` (today unless the learner gives a date). Marking a whole activity marks all its modules. Un-marking works the same way on request. Then suggest a quiz on the new module (or a re-test if a pre-test was taken on it).

**Browser check.** Follow [references/browser-progress-check.md](references/browser-progress-check.md): no browser → offer the desktop app or typed progress; sign-in page → ask the learner to sign in in the browser pane, then retry; unexpected page → show what was read and ask. Always show the proposed marks and wait for a yes before writing.

**Pause and resume.** Pause: `update meta/settings` with `paused: {since: today}`; explain that decay and the plan stop counting while paused and that any learning command (quiz, learn, challenge, mock) resumes it, with a warm-up if the break lasts more than `settings.scoring.session.warmupAfterPauseDays` days. Resume ("I'm back"): `paused: null`, `pausedDaysTotal` += paused days, append `{since, until: today}` to `pauseHistory`.

**Settings.** Mode (`course` or `full`), difficulty (`standard` or `hard`), `paceHoursPerWeek`, `examDate`, `language` (then also translate `settings.ui`, keeping keys and `{placeholders}`). State the effect in one line before writing (for example "Hard raises the ready threshold to level 85 and needs no open misconceptions"). One `update meta/settings` with `updatedAt`. The page's mode and difficulty toggles do the same.

**Status and plan.** Compute with [references/status-and-plan.md](references/status-and-plan.md) (the plan estimate is the single formula in [references/plan-estimate.md](references/plan-estimate.md), the same one the page and `init` use): readiness (labeled "Course readiness" in Course mode, "Exam readiness" in Full exam mode), section scores with official weights, module statuses, review queue (top 7), open misconceptions, calibration, last mock verdict, plan (remaining hours, pace, estimated finish date, or required pace and on-track status when an exam date is set). No writes.

## Output format

- Confirmation prompts list titles, not ids.
- Status: a short headline (readiness and label), a section table, the next three actions from the review queue, the plan line, and a pointer to the tracker page for detail.
- Prose in the learner's language; product names in English.

## Tracker access

- **Locate:** a line `GCP Cert Coach tracker: <URL> (certification: <id>)` in the Project instructions or this conversation; otherwise the learner's artifact list, titles ending in "Cert Coach" (one: use it; several: ask which certification; none: offer `/gcp-cert-coach:init`). Never create a tracker here.
- **Version:** Plugin version: 0.2.2. On the `meta/settings` read, compare versions. `schemaVersion` below 1: stop and offer `/gcp-cert-coach:rebuild` first; above 1: ask the learner to update the plugin. `templateVersion` (missing means `pluginVersion`) older than the plugin version: say once per session, in one line, "A new tracker page is available (x → y). Say 'rebuild' to update it."; never rebuild on your own. `latestPluginVersion` older than the plugin version: include it in the settings write this skill makes anyway; never write only for this.
- **Reads:** read `meta/settings` first. Marking and pause or settings changes need only `activities` and `modules`. Status and plan need `modules`, `concepts`, open `misconceptions` and the last 50 `log` entries; never list the whole `log`.
- **Writes:** one batch per confirmed change. Pass the version you read for each document you update; on a version conflict re-read once and redo; if it fails again, stop and report.
- **No data tool or database unavailable:** if the conversation contains a tracker export, use it read-only for status and plan. For changes, say that nothing was saved and show the batch you would have written as a JSON code block.

## References

- [references/status-and-plan.md](references/status-and-plan.md): readiness, statuses, queue, calibration
- [references/plan-estimate.md](references/plan-estimate.md): the plan estimate formula
- [references/browser-progress-check.md](references/browser-progress-check.md): reading Google Skills or Coursera

## Feedback

When the learner reports a problem or suggests a change, write `feedback/<timestamp>-<4 random letters>` with `{ts, source: "learner", kind: "bug" | "improvement" | "wrong_question", text, logId: null, pluginVersion: settings.pluginVersion, status: "new"}`, a neutral `text` without personal data, and tell the learner it was recorded.

## Failure handling

- Ambiguous course or module number: list the candidates with titles and ask. A learner's "no" to the resolved titles is never retried with a guess; ask for the names.
- A module title not in the tree: suggest `/gcp-cert-coach:sync` (the path may have changed).
- Browser check fails midway: keep the marks already confirmed, report what was not read, offer typed input.
