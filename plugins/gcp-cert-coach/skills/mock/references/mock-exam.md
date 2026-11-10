# Mock exam details

## Question counts by section

`count = 50 × weight / 100` per section; take the floor of each, then give the remaining questions to the sections with the largest fractional parts (ties: higher weight first).

Example for weights 20, 17.5, 25, 20, 17.5: raw 10, 8.75, 12.5, 10, 8.75 → floors 10, 8, 12, 10, 8 (48) → +1 to the two sections with .75 → **10, 9, 12, 10, 9**.

## Picking concepts

- A module counts toward every section in its `sections` list (objective `3.1` belongs to section 3).
- Within a section, spread questions across modules in proportion to their concept counts; prefer concepts with open misconceptions, low effective level and never-asked concepts, but include some strong concepts too, as the real exam does.
- Skip archived items and modules with `examRelevant: false`. Include gap topics only in Full exam mode.
- Never repeat a question already in `log` for that concept.

## Scoring the answers at the end

Process the 50 answers in the order they were asked, each with the quiz rules: effective level of the concept, then `L' = L + alpha[d] × m[c] × (100 − L)` when correct or `L' = L − beta[c][d] × L` when wrong, daily gain cap per concept, clamp, one decimal; create or update misconceptions (wrong with confidence 3 always; wrong with confidence 2 when a specific wrong belief is evident; a correct answer with confidence ≥ 2 counts toward resolving). A concept asked twice is updated twice, in order. Constants come from `settings.scoring`.

## Verdict examples

| Profile | This mock | Previous mock | Verdict |
|---|---|---|---|
| Standard | 76% | – | green |
| Standard | 72% | 80% | amber |
| Hard | 82% | 78% | amber (green needs two in a row at 80%+) |
| Hard | 81% | 84% | green |
| Hard | 63% | – | red |

## bySection shape

```json
{"1": {"questions": 10, "correct": 8}, "2": {"questions": 9, "correct": 6}, "3": {"questions": 12, "correct": 9},
 "4": {"questions": 10, "correct": 7}, "5": {"questions": 9, "correct": 5}}
```

`durationMinutes`: minutes from the first question to the last answer, when the conversation shows it; otherwise omit.
