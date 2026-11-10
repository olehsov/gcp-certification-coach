# Eval results: v0.1.0

All runs use `claude plugin eval` (Claude Code 2.1.311) through `scripts/run-evals.sh`, Sonnet as the agent model, Haiku as the judge (3 votes, majority), 1 run per arm. Reports stay local (`evals/results/`, gitignored). Scores are means over cases, 0 to 1.

## Contents

1. Summary
2. Runs
3. Per-case results
4. Grader changes
5. Trigger accuracy
6. Model comparison
7. Context cost (`/skill-doctor`)
8. Known limitations
9. v0.2.0 targeted runs

## 1. Summary

Pending: filled after the final full run (work in progress).

## 2. Runs

Pending: filled after the final full run (work in progress).

## 3. Per-case results

Pending: filled after the final full run (work in progress).

## 4. Grader changes

Every grader lives in `scripts/gen-evals.py` (cases are generated). Rule followed: a grader may change only when its old wording contradicted the specification or was too vague for the judge to apply consistently; a change must not stop checking a behavior the specification requires.

### 4.1 Before run 1 (setup fixes)

- Regex graders: `match: true` removed (`claude plugin eval` rejects the key and one invalid case aborts the whole run). Affects `learn-explain-format`, `learn-lab-breakdown`, `learn-language-uk`, `quiz-feedback-doc-link`; the patterns are unchanged.
- Fixture concept `c4-m2-k2` given level 50 so the scoring cases test real arithmetic (guess-correct stays 50; confident-wrong at medium gives 32.5). `quiz-guess-no-gain` and `quiz-confident-mistake-misconception` expect those numbers. The baseline in `BASELINE.md` used level 0, so those two cases are not strictly comparable with it; with/without arms of the same run are.
- Fixture `scoring` completed to match `packs/ace/scoring.yaml`, and `pauseHistory: []` added to the settings fixture, so skills do not fall back to defaults.
- Placeholder email in `challenge-redaction` changed to an `@example.com` address (privacy check); the case still checks that the email is not echoed.

### 4.2 After run 1

Seven LLM graders were reworded. Old and new wording, and why:

| Case | Old wording (key part) | New wording (key part) | Why |
|---|---|---|---|
| `init-first-step-language` | Asks the language **and** asks which certification, without publishing | Asks the language first, publishes nothing; asking the certification in the next message is correct; FAIL if the certification comes first | ARCHITECTURE §8 init lists "ask language → list current certifications" as separate steps, and the init skill asks one question per message. The old grader required both in one message. The README and ARCHITECTURE sequence diagrams were split into two messages to match. |
| `progress-pause` | "Sets paused {since: 2026-11-10}" and explains decay and auto-resume | Sets it, **or**, with no data tool, shows that exact change as the planned write and says it was not saved; FAIL if it claims the pause was saved | PRD §11 Risks ("Tracker database unavailable") and ARCHITECTURE §5.3 step 3: continue and tell the user what was not saved. The eval sandbox has no data tool, so a real write is impossible; the old grader rewarded claiming a save. |
| `sync-diff-before-apply` | Shows a diff, asks for confirmation before applying, explains snapshot and archive | Shows a diff, applies nothing, and states the apply procedure: learner confirmation (now or in a session that can write), snapshot first, removed items archived; FAIL if it claims changes or omits confirmation or snapshot | Same PRD rule for a session without a data tool; the snapshot and confirmation checks are kept and made explicit (stricter on "omits"). |
| `sync-removed-archived` | Snapshots before changing and archives c4-m3 instead of deleting | Same, where the snapshot and archive may be in the write plan it shows; FAIL if it deletes, omits the snapshot from the plan, or claims it applied changes | Same PRD rule. |
| `rebuild-migrate` | Reads settings, notices schema 0, plans a migration **according to the migration list**, republishes to the same URL without changing data | (1) notices schema 0; (2) plans the migration according to the 0 → 1 migration list, naming at least one of its steps; (3) snapshot first and learner confirmation; (4) same URL, no data reset; may stop after the plan without artifact tools | ARCHITECTURE §8 rebuild requires migrations from the list; the rebuild skill requires a snapshot and confirmation. An interim rewording (before this review) had dropped "according to the migration list", which made the grader easier without a spec reason; that requirement is restored here. |
| `quiz-no-repeat-30` | No new question repeats a logged question; all from completed modules | Same, plus: a question on the open misconception mc-001 with a new scenario is expected and is not a repeat; a repeat is the same stem or a paraphrase with the same answer | ARCHITECTURE §6.2 ("a later question on the same concept, with different wording, targets the misconception") and §6.6 (misconceptions first, "new wording each time"; "never repeat a question text"). The judge had failed a correct misconception re-test as a repeat. |
| `progress-no-browser-fallback` | Explains it cannot read the site and offers both fallbacks; FAIL if it invents progress | Three numbered conditions (cannot read the site here; offers the desktop app; offers typing progress manually); FAIL if it invents progress **or marks anything completed** | Not a spec conflict: the old rubric was vague and the judge split 2–1 on a correct answer. The new rubric checks the same behavior and adds a FAIL condition. |

The checklist note for J2 counted six grader fixes; the seventh (`sync-diff-before-apply`) was counted there as a skill fix because the sync skill also changed.

### 4.3 After the targeted re-run (run 2)

Three rubrics were rewritten as numbered conditions because the Haiku judge failed responses that met the old wording (0/3 and 1/3 votes). No requirement was dropped:

| Case | Change |
|---|---|
| `learn-explain-format` | Eight named parts; PASS needs six of eight including a final documentation list (old: FAIL if three or more missing, "ends with documentation links"). Same threshold. The learn skill now also says to put a next-step suggestion before the documentation list, because a response ended with a next-step line after it. |
| `learn-lab-breakdown` | Per command: what and why for all four; alternatives and production practices for at least three of four; documentation links. Stricter than before (old FAIL only if alternatives or production notes were missing "at all"). |
| `quiz-no-repeat-30` | Two numbered conditions with the repeat definition above; same meaning. |

## 5. Trigger accuracy

Tool: the skill-creator trigger evaluation (`scripts/run_eval.py`), Sonnet 5.5, 1 run per query, query sets in [triggers/](triggers/) (8 should-trigger, 8 should-not per skill). The runner registers one skill description at a time as a project command and sends each query as a fresh single-turn `claude -p`; a query counts as triggered only if Claude calls the skill.

| Skill | Positives triggered | False triggers |
|---|---|---|
| learn | 1/8 | 0/8 |
| quiz | 2/8 | 0/8 |
| challenge | 2/8 | 0/8 |
| mock | 2/8 | 0/8 |

Valid run: one test call before each skill and one after the last all answered normally. Two earlier rounds in the same session are discarded because the account hit its usage limit mid-run (refused calls count as misses). Before the description rewrite, an earlier session measured 5/8, 5/8, 5/8 and 6/8 with a different, since-lost query set, so the numbers are not directly comparable.

Reading the result:

- No false triggers: the descriptions never claim AWS, Azure, general coding or unrelated "quiz", "challenge" or "mock" requests.
- Under-triggering is strong in this setup. Claude answers single-turn study questions from its own knowledge instead of loading a skill; context-dependent replies ("next question", "B, confidence 2") have no prior question to refer to. The test environment also lists about 100 other commands and 60 other skills from the maintainer's own setup, which compete with the one under test.
- Inside the plugin eval (§3), where the whole plugin is installed and the prompt carries a tracker line, the `skill-fired` indicator shows the expected skill was called in most cases; the misses there are listed in §3.
- J3 target (at least 5/8 with 0 false triggers) is **not met** in this harness. Description tuning stopped here to save usage. Mitigation shipped in v0.1.0: `init` prints a second Project instructions line ("In this Project, use the gcp-cert-coach skills for every study request ..."), and the README quick start recommends the explicit commands (`/gcp-cert-coach:quiz` and others). The decisive check is triggering in a real claude.ai Project during the manual test (CHECKLIST K).

## 9. v0.2.0 targeted runs

Setup: Sonnet agent, Haiku judge (3 votes), with-plugin arm only (`--ablation none`); the without-plugin baseline from run 1 (0.39) is reused. Cases changed or added for the fixes from the manual test. One run per case unless noted.

| Batch | Cases | First result | After fixes |
|---|---|---|---|
| 1. New and changed cases | 14 | 10 pass | 14 pass |
| 2. quiz and mock regression | 12 | 9 pass | 12 pass |
| 3. progress, init, reset, rebuild regression | 12 | 12 pass | - |
| 4. sync, learn, challenge regression | 10 | 9 pass | 10 pass |

All 48 cases pass at least once after the fixes below. Judge flakes are recorded as such; no grader was loosened.

### Failures and what was done

| Case | Cause | Action |
|---|---|---|
| `quiz-ambiguous-letter-confirm` | Skill gap: scored "the third option" immediately | quiz step 5 now says: no letter named means no scoring and no key; state the letter read and ask. Passes |
| `reset-restore-from-snapshot` | Skill gap: restore message omitted what is overwritten and what is kept | reset restore section lists what the message must contain. Passes |
| `quiz-pretest` | Skill gap: first message no longer said the pre-test does not change levels | quiz pre-test text requires that sentence. Passes 2 of 2 |
| `progress-numbers-denied-asks-names` | Skill not fired (the response was correct) | Case prompt now carries the Project instructions line, the shipped trigger mitigation. Passes |
| `init-seed-script-fails` | Judge vote on a rubric that was not explicit | Rubric rewritten as three numbered conditions (same meaning). Passes |
| `quiz-feedback-doc-link`, `quiz-guess-no-gain` | Judge flake: responses met the rubric on reading (votes FAIL FAIL PASS and FAIL FAIL FAIL) | No change; both pass 2 of 2 on re-run |
| `challenge-evaluate-and-bonus` | Fixture incomplete: the submission lacked the VM identity output, so the skill (correctly) asked for it once before scoring | Fixture now includes that command output. Passes 2 of 2 |

### Grader and fixture changes (v0.2.0)

- `progress-mark-module`: now requires a confirmation with titles before any write (spec change A3).
- `init-summary-before-publish`: new condition, remaining hours with the practice buffer and a finish date (A5).
- `rebuild-same-url`: fixture tracker is at 0.1.0 so a rebuild is needed; `rebuild-already-up-to-date` covers the same-version path.
- Fixture settings carry `templateVersion` and `latestPluginVersion`; a complete reset snapshot with chunks is available for restore cases.

### Cost and time per quiz case (A9.5)

Same nine quiz cases, with-plugin arm, mean of run 1 (before) and the v0.2.0 runs (after). In these cases the tracker is an export in the prompt, so the measured effect is mostly fewer fetches and fewer turns, not the selective reads of a real database. Dollar cost is what `claude plugin eval` reports; no token counts are available, so tokens are not claimed.

| Measure | Before | After |
|---|---|---|
| Mean cost per case | $0.117 | $0.098 (-16%) |
| Mean time per case | 33.8 s | 22.3 s (-34%) |
| Turns, `quiz-no-repeat-30` | 19 | 5 |
| Turns, `quiz-warmup-after-pause` | 9 | 3 |
| Turns, `quiz-completed-only` | 8 | 3 |

Single-question cases (feedback, guess, misconception) did not get cheaper (about $0.10 each): their cost is dominated by the explanation of every option. The real-session saving (curated links, selective reads) needs the claude.ai re-test to confirm.
