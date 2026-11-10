# ADR 0006: Self-contained skills; shared configuration lives in the tracker database

- Status: Accepted (verify during build)
- Date: 2026-11-10

## Context

Several skills need the same data: scoring constants, thresholds, mode, language, the certification tree. Skill files can reference files in their own folder; reading another skill's folder (`../quiz/references/...`) is not guaranteed to work on every surface.

## Decision

- Each skill references only files inside its own folder, one level deep.
- `init` copies everything other skills need into the tracker database: `settings` (mode, difficulty, language, pace, scoring constants, exam-guide sections and weights, pack metadata) and the tree (`activities`, `modules`, `concepts`).
- Other skills read that data from the database at the start of each run.
- Certification packs live in `skills/init/assets/packs/<certId>/`. Cheat sheets for explanations live in `skills/learn/references/`.
- Small, stable rules that several skills need (for example, how to locate the tracker) are repeated briefly in each `SKILL.md` rather than shared.

## Build-time verification

The builder must confirm on claude.ai that a skill can read its own `references/` and `assets/` files. If cross-skill reads turn out to be reliable, this ADR may be revisited, but the database remains the source of truth for runtime configuration.

## Consequences

- Changing a threshold for an existing learner is a database update, not a code change.
- `rebuild` migrates settings when `schemaVersion` changes.
