---
name: challenge
description: Use whenever a Google Cloud certification learner asks for a challenge, a hands-on, practical or lab-style task to do in their own Google Cloud project ("give me a challenge", "practical exercise on least-privilege service accounts", "a challenge lab like the skill badges"), or submits challenge work, a step narrative or gcloud or kubectl output to be graded. Use it even when inventing a task directly seems simple: this skill picks concepts from the learner's tracker, grades against official documentation and records a mastery bonus. Gives tasks with GCP Certification Coach as a goal, constraints and success criteria with no step-by-step instructions, and scores each requirement 0 to 1 from the narrative and named verification commands. Not for multiple-choice practice (use quiz), mock exams (use mock), explaining a lab already done (use learn) or running commands on the learner's project.
---

# Challenge

A practical task that proves the learner can build something without a script to follow. Claude never runs commands in the learner's project; the learner does the work and submits evidence.

## When to use

- The learner wants a hands-on task, or submits work for a challenge already assigned.
- Not for multiple-choice practice (quiz, mock) or lab walk-throughs (learn).

## Preconditions

- A tracker (see Tracker access). Without one, a challenge can still be given and reviewed, but nothing is saved; say so.
- The learner has their own Google Cloud project (free trial or sandbox). Mention costs and cleanup in every task.

## Workflow: assign

```
- [ ] 1. Read settings, tree, concepts, open challenges
- [ ] 2. Pick 1–3 completed concepts that can be practiced hands-on
- [ ] 3. Write the task (goal, constraints, success criteria, verification commands)
- [ ] 4. Save the challenge as assigned
```

1. Read `meta/settings`, `modules`, `concepts`, open `misconceptions` and `challenges` with status `assigned`. If one is still assigned, offer to continue it instead of creating another.
2. Pick concepts from completed, exam-relevant modules where a learner can build something in a project: prefer concepts with an open misconception or a mid-range level (30–80). Avoid concepts with nothing to build (pricing theory, history).
3. Write the task with [references/challenge-format.md](references/challenge-format.md): goal, constraints, success criteria, 2–4 named verification commands, a cost and cleanup note, the redaction reminder, and what to submit. **No step list, no commands that perform the task, no console click path.** Ground each requirement in a documentation page you fetched; keep those links for the review, not the task.
4. Write `challenges/<id>`: `{ts, title, conceptIds, status: "assigned", score: null, bonusApplied: false, reviewSummary: null}`.

## Workflow: review a submission

```
- [ ] 1. Check the submission for personal data; ask for redaction if needed
- [ ] 2. Evaluate each success criterion against the evidence and documentation
- [ ] 3. Score 0–1 and compute the bonus
- [ ] 4. Write one batch; report
```

1. If the pasted output shows project ids, project numbers, emails, account names, keys or IP ranges tied to the learner, do not repeat them, and remind the learner to redact such values next time. None of these values is ever written to the tracker.
2. For each criterion: met (1), partly met (0.5) or not met (0), with one line of evidence from the narrative or command output and a documentation link when something is wrong or missing. Ask for one missing command output at most once before scoring.
3. `score` = mean of the criteria, rounded to two decimals. Status: `passed` when 1, `partial` when ≥ `challengeBonus.minScore`, else `failed`. When `score ≥ challengeBonus.minScore`: bonus = `challengeBonus.base + challengeBonus.perScore × score` points to **each** linked concept, added to its effective level (decay applied first), capped at 100, **not** limited by the daily gain cap, not counted as answers or days. When `score` reaches `challengeBonus.resolveMisconceptionsAtScore` (1.0), resolve open misconceptions on the linked concepts.
4. One batch: `update challenges/<id>` (`status`, `score`, `bonusApplied`, `reviewSummary`: three to five neutral sentences on what was built and what was missing, no raw output and no identifiers), and per linked concept `update concepts/<id>` (`level`, `bonus` += applied points; leave `answers`, `days`, `lastReviewed` unchanged), plus misconception updates. Report the per-criterion table, score, bonus per concept (before → after) and one suggestion to close the gaps.

## Output format

Task message: title, goal, constraints, success criteria (numbered), verification commands (code block, read-only commands only), what to submit, cost and cleanup, redaction reminder. Review message: criteria table, score, bonus lines, documentation links, next step. Commands and product names in English; prose in the learner's language.

## Tracker access

- **Locate:** a line `GCP Cert Coach tracker: <URL> (certification: <id>)` in the Project instructions or this conversation; otherwise the learner's artifact list, titles ending in "Cert Coach" (one: use it; several: ask which certification; none: offer `/gcp-cert-coach:init`). Never create a tracker here.
- **Schema:** if `meta/settings.schemaVersion` is above 1, ask the learner to update the plugin; below 1, suggest `/gcp-cert-coach:rebuild`.
- **Writes:** one batch per step above. Pass the version you read for each document you update; on a version conflict re-read once and redo; if it fails again, stop and report.
- **No data tool or database unavailable:** continue; if the conversation contains a tracker export, use it read-only. Say that nothing was saved and show the batch you would have written as a JSON code block.

## Feedback

When the learner disputes a review or suggests a change, write `feedback/<timestamp>-<4 random letters>` with `{ts, source: "learner", kind: "wrong_question" | "bug" | "improvement", text, logId: null, pluginVersion: settings.pluginVersion, status: "new"}`, a neutral `text` without personal data, and tell the learner it was recorded.

## Failure handling

- No completed hands-on concepts: suggest a quiz or marking progress first.
- The learner cannot run commands (no project): offer a design challenge instead (they describe the architecture and the exact commands they would run); score it the same way but cap the score at 0.5 and say why.
- The learner asks Claude to run the commands: decline; this plugin never acts on the learner's Google Cloud project.
