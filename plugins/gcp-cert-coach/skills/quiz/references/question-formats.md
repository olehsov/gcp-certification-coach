# Question formats

All questions are original, in English, in the style of the certification exam: a realistic situation, one best answer (or an exact number of correct answers), plausible distractors that reflect real mistakes. Never reuse official sample questions or course quiz questions. Base the answer key on a documentation page you fetched; put its URL in `docUrl`.

| `format` | Shape | Answer the learner gives |
|---|---|---|
| `scenario` | 2–4 sentence situation with a requirement ("minimal operational overhead", "least privilege", "lowest cost"); options A–D | one letter |
| `multi_select` | Situation; options A–E; "Choose two." (state the number) | letters; correct only if exactly the right set |
| `command` | A task; options are four `gcloud`, `kubectl`, `bq` or `gsutil`/`gcloud storage` commands differing in a subcommand or flag | one letter |
| `explain` | "In two or three sentences, explain why …" | free text; correct when it states the key points you list privately before reading the answer (2–3 points); partial counts as wrong, but credit what was right in the feedback |
| `choose_service` | A requirement list; options are four services | one letter |
| `why_wrong` | A short proposed solution with one flaw; "What is wrong with this design?" options A–D | one letter |

Difficulty:

- `easy`: one fact, the requirement is explicit.
- `medium`: two constraints to weigh, distractors that are right in other situations.
- `hard`: several constraints, a subtle limit, scope or default, or a trade-off between two valid-looking answers.

Distractor rules:

- Each wrong option must be wrong for a reason you can state in one sentence with documentation behind it.
- Avoid "all of the above", "none of the above", and options that differ only in wording.
- Keep options similar in length so the longest is not a giveaway.

Feedback per option (after the answer), for example:

> **B — correct.** `roles/compute.viewer` grants read-only access to Compute Engine resources …
> **A — wrong.** `roles/compute.admin` can start, stop and modify instances, which breaks the requirement …
> **C — wrong.** Basic roles such as Editor grant write access across most services …
> **D — wrong.** Owner adds IAM management on top of Editor …
> Source: https://docs.cloud.google.com/compute/docs/access/iam
