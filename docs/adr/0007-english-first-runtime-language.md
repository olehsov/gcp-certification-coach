# ADR 0007: English source, learner-chosen explanation language

- Status: Accepted
- Date: 2026-11-10

## Decision

- Everything in the repository is English: skills, descriptions, references, docs, README, code comments, tracker default strings.
- `init` asks for the explanation language. Claude then explains, gives feedback and writes tracker UI strings in that language.
- Google Cloud product names, technical terms, commands, flags and exam-style question text stay in English, because the exam is in English and documentation searches work best in English.
- The tracker template reads UI strings from `settings.ui` with English fallbacks; `init` writes a translated `settings.ui` when a non-English language is chosen.

## Consequences

- One codebase for all users.
- Questions remain exam-realistic.
