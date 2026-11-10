# Status and plan calculations

All constants come from `settings.scoring`; the profile is `scoring.profiles[settings.difficulty]`. These are the same rules the tracker page uses, so numbers in chat match the page.

## Contents

1. Effective level
2. Module level, coverage and status
3. Section scores and readiness
4. Review queue
5. Calibration
6. Plan

## 1. Effective level

`interval` = `reviewIntervalDays` for the stored level (< 60, < 80, ≥ 80). `overdue` = days since `lastReviewed` − paused days in that span (`pauseHistory` plus the active pause) − `interval`. Effective level = `level` when never answered or `overdue ≤ 0`, else `max(0, level − decayPerWeekOverdue × overdue / 7)`.

## 2. Module level, coverage and status

For an exam-relevant, non-archived module with concepts `C` (non-archived):

- level = mean effective level of `C`; coverage = share of `C` with at least one answer;
- answers = sum of `answers`; distinct days = union of `days`;
- recent = the last `moduleReady.lastNCorrect` log entries of the module (excluding pre-tests).

Status:

- `not_started`: not completed and no answers;
- `completed`: completed, no answers yet;
- `practicing`: at least one answer and not ready;
- `ready`: level ≥ `minLevel`, coverage ≥ `minCoverage`, answers ≥ `minAnswers`, distinct days ≥ `minDistinctDays`, every recent entry correct with confidence ≥ 2, and (Hard) no open misconception in the module;
- `review`: at least one answer and any of its concepts past its review interval (`overdue > 0`); this overrides ready and practicing.

## 3. Section scores and readiness

Use only modules in the current mode (the `gaps` activity counts only in Full exam mode), exam-relevant and not archived.

- A module belongs to section `s` when any of its `sections` starts with `s.`; a module can count in several sections.
- Section score = weighted mean of module levels, weight `readiness.coreWeight` for core modules and `readiness.supportWeight` for support modules. Untouched modules count as level 0.
- Readiness = sum of (section weight × section score) / 100, using the weights from `settings.examGuide.sections`.
- Label: "Course readiness" in Course mode, "Exam readiness" in Full exam mode. Course readiness is not exam readiness: say so when the learner asks about booking the exam.

## 4. Review queue

From concepts of completed exam-relevant modules (plus gap topics in Full exam mode), in order: open misconception; never asked; due or overdue (most overdue first); lowest effective level. Skip concepts whose last answer was correct with confidence 3 and that are inside their interval. Show the top `page.reviewQueueSize` (7).

## 5. Calibration

From `log` entries other than pre-tests: share correct when confidence is 3 ("correct when sure"), overall share correct, and share of answers marked guess. If "correct when sure" is well below overall accuracy, point out overconfidence; if many correct answers are guesses, encourage studying those concepts.

## 6. Plan

- Required activities: not optional, not archived, in the current mode.
- Remaining course hours = for each uncompleted module: its `hours` if known, else activity `hours` ÷ number of modules in the activity.
- Gaps (Full exam mode): `plan.gapHoursPerTopic` per uncompleted gap topic; required gap hours = that × all gap topics.
- Practice buffer = `plan.practiceBufferFraction` × total required hours − logged answers (excluding pre-tests) × `plan.minutesPerLoggedAnswer` / 60, floored at 0.
- Remaining = remaining course hours + remaining gap hours + practice buffer.
- Weeks = remaining ÷ `paceHoursPerWeek`. Estimated finish = today + weeks × 7 days + days of the active pause so far.
- With `examDate`: required pace = remaining ÷ weeks until the exam; on track when required pace ≤ `paceHoursPerWeek`. Report both.

Example: 40 remaining course hours, Course mode, total required 58.75 h, 20 logged answers → buffer 0.2 × 58.75 − 20 × 3 / 60 = 11.75 − 1 = 10.75 → remaining 50.75 h; at 7 h/week ≈ 7.25 weeks ≈ 51 days → finish = today + 51 days.
