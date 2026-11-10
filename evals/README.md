# Evals

Behavior tests for the `gcp-cert-coach` plugin, run with [`claude plugin eval`](https://code.claude.com/docs/en/plugin-evals) (Claude Code 2.1.269 or later).

## Layout

```
evals/
├── <case>/
│   ├── prompt.md            # frontmatter (name, tags, limits, allowed tools) + the learner's message
│   └── graders/
│       ├── skill-fired.md   # tool_used: the expected skill loaded (indicator, with-plugin arm only)
│       └── g<N>-<type>.md   # llm or regex graders: PASS/FAIL rubric
├── BASELINE.md              # gaps observed without the plugin
├── RESULTS.md               # results with the plugin, grader changes, triggers, models
├── triggers/                # trigger query sets for the skill-creator trigger evaluation
└── results/                 # run outputs (gitignored)
```

Cases are **generated** by [`scripts/gen-evals.py`](../scripts/gen-evals.py) from one shared, invented tracker fixture. Edit the generator, then run `python3 scripts/gen-evals.py`; do not hand-edit case folders.

## How cases model the tracker

Eval runs happen in Claude Code in an empty working directory, without the artifact data tool that the tracker database needs on claude.ai. Each case therefore pastes a read-only export of the tracker collections into the prompt and states that no data tool is available. Skills are expected to work from that export, say clearly that nothing was saved, and show the write batch they would have sent. Real database writes are covered by the manual test (CHECKLIST K).

`claude plugin eval` has no scripted multi-turn conversations, so multi-step flows are tested one turn at a time: the prompt describes the earlier turn (for example, the quiz question that was asked and its answer key) and the learner's reply.

## Running

`claude plugin eval` only accepts an eval directory inside the plugin root, and this repository keeps `evals/` outside the plugin folder. [`scripts/run-evals.sh`](../scripts/run-evals.sh) stages a temporary copy of the plugin with the cases inside it, runs the eval there with `--no-publish`, and writes results to `evals/results/<timestamp>/`.

```bash
claude auth login                                          # once; eval child processes use the CLI login
scripts/run-evals.sh --model sonnet --runs 1 -j 4          # full suite, with and without the plugin
scripts/run-evals.sh --tag quiz --model haiku              # one skill's cases
scripts/run-evals.sh --case 'quiz-*' --runs 3              # by name glob (one glob, no braces)
scripts/run-evals.sh --cases quiz-pretest,mock-verdict-hard --model haiku  # a named subset
scripts/run-evals.sh --baseline --model sonnet --runs 1    # no-plugin baseline only
```

Any other `claude plugin eval` option is passed through. WebFetch and WebSearch are granted so skills can ground answers in documentation.

Every run spends the CLI account's plan usage (each case is a full `claude` child process). Before a bulk run, make one test call (`claude -p "Reply with the single word OK."`); if it reports a usage or rate limit, do not start, because refused calls are scored as failures. Re-run only the cases you changed (`--cases`), and keep full runs for releases.

### Trigger accuracy

[triggers/](triggers/) holds 16 queries per skill for `learn`, `quiz`, `challenge` and `mock`. Run them with the skill-creator skill's `scripts/run_eval.py` from a scratch directory that has its own `.claude/` folder (the runner writes a temporary command file there), with `CLAUDECODE` unset; see [triggers/README.md](triggers/README.md) and the results in [RESULTS.md](RESULTS.md).

## Coverage

At least three cases per skill (37 in total). CHECKLIST C3 mapping:

| C3 requirement | Case(s) |
|---|---|
| Quiz uses only completed modules | `quiz-completed-only`, `quiz-uncompleted-warning` |
| No repeated question in a 30-question session | `quiz-no-repeat-30` |
| Documentation link in every answer | `quiz-feedback-doc-link`, `learn-explain-format`, `learn-lab-breakdown` |
| Guess-correct gives no gain | `quiz-guess-no-gain` |
| Confident mistake creates a misconception | `quiz-confident-mistake-misconception` |
| Reset asks for confirmation and snapshots first | `reset-confirm-snapshot`, `reset-clear-completion` |
| Sync shows a diff before applying | `sync-diff-before-apply` |
| Init refuses a duplicate tracker without confirmation | `init-duplicate-guard` |
| Progress browser check asks to sign in when signed out | `progress-browser-signed-out` |
| Explanation language follows settings, terms stay English | `learn-language-uk`, `init-summary-before-publish` |

## Privacy

Fixture data is invented. Never paste real tracker exports, artifact URLs or transcripts of your own sessions into cases; `results/` stays local and is gitignored.
