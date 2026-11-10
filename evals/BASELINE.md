# Baseline without the plugin

Run: `scripts/run-evals.sh --baseline --model sonnet --runs 1 -j 4` on 2026-11-10 with Claude Code 2.1.311. The plugin's skills were removed (empty plugin), `skill-fired` graders were dropped, and every other grader was scored. One run per case, so treat single scores as indicative. Cost: about $1.80.

**Mean score: 0.34** across 37 cases.

## Observed gaps

The prompts already contain a tracker export with settings and scoring constants, so a capable model infers a lot. What it does not do without instructions:

1. **Selection priority.** Asked for the next question, it picked the most overdue concept instead of the concept with an open misconception, and it did not warn when asked to quiz an uncompleted module (`quiz-completed-only`, `quiz-uncompleted-warning`).
2. **Misconceptions and scoring writes.** After a confident wrong answer it explained the options well but created no misconception record and did not apply the level formula (`quiz-confident-mistake-misconception`).
3. **Pre-tests and warm-ups.** It ran a pre-test question but did not say levels stay unchanged; after a 16-day pause it did not resume the plan or start a warm-up (`quiz-pretest`, `quiz-warmup-after-pause`).
4. **Feedback capture.** A disputed question was discussed but no feedback item was recorded or proposed (`quiz-wrong-question-feedback`).
5. **Destructive operations.** Reset and sync described the current state or a diff, but did not take a snapshot first, did not ask for an explicit confirmation phrase, and did not archive instead of delete (`reset-*`, `sync-*`).
6. **Setup flow.** It did not start with the language question, did not offer a confirmed second tracker when one exists, did not show a confirmation summary before publishing, and did not explain the beta generated-pack flow (`init-*`).
7. **Grounding and formats.** Explanations lacked official documentation links and the fixed explanation structure; the lab breakdown missed alternatives and production practice per step; course text was rewritten instead of declined (`learn-*`).
8. **Challenges.** It gave step-by-step instructions instead of a goal-and-constraints task, omitted the redaction reminder, and did not apply the bonus formula (`challenge-*`).
9. **Maintenance.** Rebuild did not plan a schema migration or promise the same URL; pause did not explain decay exclusion and automatic resume (`rebuild-*`, `progress-pause`, `progress-no-browser-fallback`).

Cases already passing without the plugin (mock verdict arithmetic, plan estimate, guess with no gain, Ukrainian explanations) remain in the suite as regression guards.

## Per-case scores

| Case | Score | Failed graders |
|---|---|---|
| `challenge-evaluate-and-bonus` | 0.50 | g2-llm |
| `challenge-no-steps` | 0.00 | g2-llm |
| `challenge-redaction` | 0.00 | g2-llm |
| `init-duplicate-guard` | 0.00 | g2-llm |
| `init-first-step-language` | 0.00 | g2-llm |
| `init-generated-pack-no-browser` | 0.00 | g2-llm |
| `init-summary-before-publish` | 0.00 | g2-llm, g3-llm |
| `learn-explain-format` | 0.50 | g3-regex |
| `learn-lab-breakdown` | 0.00 | g2-llm, g3-regex |
| `learn-language-uk` | 1.00 | – |
| `learn-no-course-text` | 0.00 | g2-llm |
| `mock-no-key-midway` | 1.00 | – |
| `mock-start-weighted` | 1.00 | – |
| `mock-verdict-hard` | 1.00 | – |
| `progress-browser-signed-out` | 1.00 | – |
| `progress-mark-module` | 1.00 | – |
| `progress-no-browser-fallback` | 0.00 | g2-llm |
| `progress-pause` | 0.00 | g2-llm |
| `progress-plan-estimate` | 1.00 | – |
| `quiz-completed-only` | 0.50 | g2-llm |
| `quiz-confident-mistake-misconception` | 0.00 | g2-llm, g3-llm |
| `quiz-feedback-doc-link` | 0.50 | g2-llm |
| `quiz-guess-no-gain` | 1.00 | – |
| `quiz-no-repeat-30` | 0.50 | g2-llm |
| `quiz-pretest` | 0.00 | g2-llm |
| `quiz-uncompleted-warning` | 0.00 | g2-llm |
| `quiz-warmup-after-pause` | 0.00 | g2-llm |
| `quiz-wrong-question-feedback` | 0.00 | g1-llm |
| `rebuild-migrate` | 0.00 | g2-llm |
| `rebuild-no-tracker` | 1.00 | – |
| `rebuild-same-url` | 0.00 | g2-llm |
| `reset-clear-completion` | 0.00 | g2-llm |
| `reset-confirm-snapshot` | 0.00 | g2-llm |
| `reset-keeps-tree` | 1.00 | – |
| `sync-diff-before-apply` | 0.00 | g2-llm |
| `sync-removed-archived` | 0.00 | g2-llm |
| `sync-renamed-keeps-data` | 0.00 | g2-llm |
