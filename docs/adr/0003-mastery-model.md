# ADR 0003: Bounded mastery level with confidence weighting

- Status: Accepted
- Date: 2026-11-10

## Context

Readiness must reflect real, durable knowledge. Two models were considered.

## Options

1. **Accumulating points** (more points for confident answers, a high target to finish). Rejected: points only grow, so volume of easy questions reaches "ready"; old mistakes never count; no notion of forgetting.
2. **Bounded level 0–100 per concept** that rises on correct answers and falls on mistakes, with step size depending on question difficulty and the learner's confidence.

## Decision

Option 2, with these rules (exact constants in ARCHITECTURE §6):

- Correct answer: level moves toward 100 by a fraction of the remaining gap. The fraction depends on difficulty and is multiplied by confidence: **guess = 0**, think = 0.6, sure = 1.0.
- Wrong answer: level drops by a fraction of the current level. Honest "guess" mistakes cost little; confident mistakes cost most and create a misconception entry.
- "Ready" is not a single number. It requires a level threshold **and** concept coverage, a minimum number of answers across several distinct days, recent correct answers with at least "think" confidence, and no open misconceptions (Hard).
- Daily gain cap per concept, so one long evening is not counted as durable knowledge.
- Decay after the review interval passes (paused time excluded).
- Two difficulty profiles: Standard and Hard.
- Calibration (accuracy of "sure" answers) is shown to the learner.

## Consequences

- Honest confidence ratings are rewarded; overconfidence is visible.
- Constants live in the tracker settings with a rationale for each, so they can be tuned without code changes.
