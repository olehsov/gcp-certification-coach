# Selecting concepts and questions

## Candidate concepts

A concept is a candidate when all of these hold:

- the concept and its module are not `archived`;
- the module is `examRelevant`;
- the module is `completed`, or it belongs to the `gaps` activity and `settings.mode` is `full`;
- the activity is not archived.

Pre-tests use the **next uncompleted module** instead: the lowest-order exam-relevant module that is not completed, in the lowest-order activity that has one (or the module the learner names).

Warm-ups use the candidates with the **highest effective level** (at least one answer), top `session.warmupQuestions`.

## Priority (normal sessions)

Rank candidates and fill the session in this order:

1. **Open misconception** on the concept (status `open`). Ask a question that targets the wrong belief in the misconception's `statement`, with wording different from every earlier question.
2. **Never asked** (`answers` is 0).
3. **Due or overdue**: answered before, and `daysSinceLastReviewed − pausedDays ≥ reviewInterval(level)`; most overdue first.
4. **Lowest effective level.**
5. **Skip** concepts whose last answer was correct with confidence 3 and that are still inside their review interval, unless nothing else is left.

## Interleaving

- Never more than `session.maxConsecutiveSameModule` questions in a row from one module; reorder the picks to alternate modules.
- Prefer one concept per question; a concept may appear twice in a session only when it has an open misconception or the session has fewer candidates than questions.

## No repeats

- Before asking, compare the new question with every `log.question` stored for that concept and with the questions already asked in this session. A question is a repeat when it tests the same fact with the same correct answer, even if reworded. Write a different question (another scenario, another facet of the concept, another format).

## Formats per session

Mostly `scenario` and `multi_select`; in every 5 questions include at least one other format (`command`, `explain`, `choose_service` or `why_wrong`) when the concept allows it. Vary difficulty: start with medium, go harder after correct confident answers, easier after a wrong one.

## Quick example

Candidates: A (open misconception, level 30), B (never asked), C (overdue by 4 days, level 55), D (level 70, not due), E (last answer correct and sure, not due).
Order: A, B, C, D; E only if more questions are needed. With A and D in the same module and a two-in-a-row limit, A, B, D, C is also fine; A, D, D would not be.
