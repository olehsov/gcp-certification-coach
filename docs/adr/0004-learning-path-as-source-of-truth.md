# ADR 0004: Google Skills learning path as the skill tree source, exam-guide gaps as an optional layer

- Status: Accepted
- Date: 2026-11-10

## Context

Learners take the same official content on Coursera or on Google Skills. The certification exam, however, tests the official exam guide, which the learning path does not fully cover.

## Options

1. Tie the tree to Coursera. Rejected: platform-specific.
2. Build a full parallel tree from the exam guide (~60 items). Rejected: duplicates the path and doubles the tracking burden.
3. Use the Google Skills certification learning path as the tree (any number of activities: courses and skill badges) and add an optional block of exam-guide gaps.

## Decision

Option 3.

- **Course mode:** tree = learning path activities → modules → concepts (submodules). Optionality mirrors the path: what is optional on Google Skills is optional here.
- **Full exam mode:** adds one extra activity, "Exam guide gaps", with ~10–15 topics not covered by the path, each linked to official documentation.
- Each module maps to exam-guide sections so readiness is weighted by official section weights.
- Course-level and module-level completion can be marked by the learner from either platform.

## Consequences

- One tree serves both Coursera and Google Skills learners.
- `sync` must detect changes in the path (added, removed, renamed activities and modules) and in the exam guide version.
- Intro, summary and "how to use the notebook" modules are tracked for completion but excluded from quizzes (`examRelevant: false`).
