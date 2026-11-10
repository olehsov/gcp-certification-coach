# Plan estimate (single formula)

The tracker page, `progress` and `init` all use this formula. Quote the number from here or from the seed script's summary, never from another calculation. Constants come from `settings.scoring.plan` (`gapHoursPerTopic` 1, `practiceBufferFraction` 0.2, `minutesPerLoggedAnswer` 3).

1. **Required activities:** not archived, not optional, in the current mode (the `gaps` activity only in Full exam mode).
2. **Required hours:** sum of activity `hours`; the gaps activity counts `gapHoursPerTopic` per gap topic.
3. **Remaining course hours:** for each uncompleted, non-archived module of a required course or skill badge: its `hours` if known, else activity `hours` divided by the number of its modules.
4. **Remaining gap hours (Full mode):** `gapHoursPerTopic` per uncompleted gap topic.
5. **Practice buffer:** `practiceBufferFraction` × required hours, minus logged answers (not pre-tests) × `minutesPerLoggedAnswer` / 60, not below 0. It is part of the plan even when the learner has completed everything else.
6. **Remaining** = remaining course hours + remaining gap hours + practice buffer.
7. **Estimated finish** = today + remaining / `paceHoursPerWeek` weeks + days of an active pause. With `examDate`: required pace = remaining / weeks until the exam; on track when it is at most `paceHoursPerWeek`.

Worked example (Course mode, required 58.75 h, uncompleted modules total 40 h, 20 logged answers): buffer = 0.2 × 58.75 − 20 × 3 / 60 = 10.75; remaining = 50.75 h; at 7 h per week = 7.25 weeks ≈ 51 days.

At setup (`init`), nothing is logged yet, so the buffer is the full 20% of required hours. The seed script prints `remainingHours` and `estimatedFinish`; on the by-hand path compute them with the steps above.
