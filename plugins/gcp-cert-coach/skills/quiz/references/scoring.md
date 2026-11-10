# Scoring an answer

## Contents

1. Constants
2. Effective level
3. Level update
4. Daily gain cap
5. Misconceptions
6. Pre-tests and warm-ups
7. The write batch
8. Worked examples

## 1. Constants

Read everything from `settings.scoring`; the profile is `settings.scoring.profiles[settings.difficulty]`. Defaults if a key is missing (and suggest a rebuild):

| Key | Default |
|---|---|
| `alpha` | easy 0.15, medium 0.25, hard 0.35 |
| `confidenceMultiplier` | 1 → 0.0, 2 → 0.6, 3 → 1.0 |
| `beta[confidence][difficulty]` | 1: 0.10/0.08/0.05 · 2: 0.25/0.20/0.15 · 3: 0.40/0.35/0.30 (easy/medium/hard) |
| profile `dailyGainCap` | standard 25, hard 20 |
| profile `reviewIntervalDays` | standard 3/7/14, hard 2/5/10 for level < 60 / < 80 / ≥ 80 |
| profile `decayPerWeekOverdue` | standard 3, hard 5 |
| `misconception.resolveAfterConsecutiveCorrect` | 2 |
| `misconception.minConfidenceToResolve` | 2 |
| `history.recentAnswersKept` / `distinctDaysKept` | 5 / 10 |

## 2. Effective level

Before every update, compute the concept's effective level `L` from its stored `level`:

- `interval` = `reviewIntervalDays` for the stored level (below60, below80, atLeast80).
- `daysSince` = days from the date of `lastReviewed` to today (learner's local dates).
- `pausedDays` = days inside that span covered by `settings.pauseHistory` entries and the active pause.
- `overdue = daysSince − pausedDays − interval`.
- If the concept was never answered or `overdue ≤ 0`: `L = level`. Otherwise `L = max(0, level − decayPerWeekOverdue × overdue / 7)`.

## 3. Level update

With difficulty `d` and confidence `c`:

- Correct: `L' = L + alpha[d] × confidenceMultiplier[c] × (100 − L)`
- Wrong: `L' = L − beta[c][d] × L`

Then apply the daily gain cap (gains only), clamp to 0–100 and round to one decimal. Store `L'` as the new `level` (decay is now applied).

## 4. Daily gain cap

`gainedToday` = sum of `max(0, levelAfter − levelBefore)` over today's `log` entries for this concept with `kind` other than `pretest`. A gain may raise the level by at most `dailyGainCap − gainedToday` (never below zero). Losses are never capped. When the cap limits a gain, tell the learner ("daily gain limit reached for this concept; come back tomorrow").

## 5. Misconceptions

- **Create** (status `open`) when the answer is wrong with confidence 3, or wrong with confidence 2 and your explanation names a specific wrong belief. `statement` is one English sentence describing the wrong belief, not the question ("Believes a VM needs a downloaded key to call APIs as its attached service account."). Link it in the log entry's `misconceptionId`.
- **Refute**: a correct answer with confidence ≥ `minConfidenceToResolve` on a concept with an open misconception increments `consecutiveRefutations`; at `resolveAfterConsecutiveCorrect` set `status: "resolved"` and `resolvedAt`.
- **Reset**: a wrong answer on that concept sets `consecutiveRefutations` back to 0.
- Never create a second open misconception with the same belief on a concept; update the existing one.

## 6. Pre-tests and warm-ups

- Pre-test: log with `kind: "pretest"`, `levelBefore: null`, `levelAfter: null`; do not change `level`, `answers`, `correct`, `recent`, `days` or `lastReviewed`; do not create misconceptions. After the module is completed, the next normal session should ask the same concepts again (new wording) and tell the learner how they improved.
- Warm-up: `kind: "warmup"`, scored like a normal question.

## 7. The write batch

One batch per answer:

1. `update concepts/<id>` (with the version you read): `level`, `answers + 1`, `correct + (1 if correct)`, `recent` (append `{date, correct, confidence}`, keep the last `recentAnswersKept`), `days` (add today if missing, keep the last `distinctDaysKept`), `lastReviewed` (now).
2. `set log/<ISO timestamp>-<4 random letters>`: `ts`, `kind` (`quiz`, `pretest`, `warmup`), `conceptId`, `moduleId`, `format`, `difficulty`, `confidence`, `question` (full text with options), `answerKey`, `given`, `correct`, `docUrl`, `levelBefore` (`L`, the effective level), `levelAfter`, `misconceptionId`, `mockId: null`.
3. Misconception: `set misconceptions/<id>` (new: `conceptId`, `statement`, `status: "open"`, `createdAt`, `resolvedAt: null`, `consecutiveRefutations: 0`) or `update` (refutation counter, status).
4. Pause resume, if pending: `update meta/settings` (`paused: null`, `pausedDaysTotal`, `pauseHistory`, `updatedAt`).

## 8. Worked examples

Standard profile, concept not overdue, `L = 50`:

| Answer | Computation | New level |
|---|---|---|
| Correct, medium, confidence 1 | 50 + 0.25 × 0.0 × 50 | **50.0** (no gain for a guess) |
| Correct, medium, confidence 2 | 50 + 0.25 × 0.6 × 50 = 57.5 | **57.5** |
| Correct, hard, confidence 3 | 50 + 0.35 × 1.0 × 50 = 67.5, gain 17.5 ≤ 25 | **67.5** |
| Wrong, easy, confidence 3 | 50 − 0.40 × 50 | **30.0** + misconception |
| Wrong, medium, confidence 1 | 50 − 0.08 × 50 | **46.0** |

Decay: stored level 62, last reviewed 12 days ago, no pauses, standard profile: interval 7 (62 is below 80), overdue 5 days, `L = 62 − 3 × 5 / 7 = 59.9`. Score from 59.9.

Daily cap: earlier today the concept went 40 → 58 (gain 18). A new correct hard sure answer from 58 would give 58 + 0.35 × 42 = 72.7 (gain 14.7), but only 25 − 18 = 7 is left: new level **65.0**.
