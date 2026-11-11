---
name: init
description: "Sets up GCP Certification Coach for one Google Cloud certification. Asks the explanation language, lists current Google Cloud certifications, builds the skill tree from the official Google Skills learning path (curated pack for Associate Cloud Engineer, generated beta pack for others), records mode, difficulty, weekly hours, exam date and what the learner already completed, then publishes a private tracker page with a database and prints the line to paste into Project instructions. Use when the learner says \"start preparing for a Google Cloud certification\", \"set up the coach\", \"init\", \"choose a certification\" or \"create my tracker\". Not for marking progress in an existing tracker (use progress), updating the tree from the live path (use sync) or refreshing the tracker page (use rebuild)."
---

# Init

Create one tracker per certification: an artifact page with a database that every other skill of this plugin reads and writes.

## When to use

- The learner starts preparing for a certification or asks to set up the coach.
- Not when a tracker for that certification already exists (see the duplicate guard), and not for progress updates, sync or page refreshes.

## Preconditions

- The artifact tool with the `db` capability and the artifact data tool are available (claude.ai chat, the Claude desktop app or Cowork). Without them, still run steps 1–7 (language, certification, pack, choices, progress, summary) so the learner's answers and the tree are ready, then explain that publishing needs one of those surfaces and stop before step 8.
- Web search or fetch is available for the certification list and documentation. The built-in browser is optional (generated packs and progress checks).

## Workflow

Copy this checklist and tick it off as you go:

```
- [ ] 1. Duplicate guard
- [ ] 2. Explanation language
- [ ] 3. Certification (list current ones, learner chooses)
- [ ] 4. Pack: curated or generated (beta)
- [ ] 5. Mode, difficulty, weekly hours, exam date
- [ ] 6. Initial progress (typed or browser check)
- [ ] 7. Summary and confirmation
- [ ] 8. Publish the tracker page
- [ ] 9. Seed the database in batches of at most 50 writes
- [ ] 10. Read back and verify
- [ ] 11. Project instructions line and next steps
```

1. **Duplicate guard.** Look for an existing tracker for the chosen certification: a line `GCP Cert Coach tracker: <URL> (certification: <certId>)` in the Project instructions or conversation, or an artifact titled `<Short name> Cert Coach` in the learner's artifact list. If one exists, say so, offer to keep using it, and create another only after the learner explicitly confirms a second tracker. Repeat this check after step 3 once the certification is known.
2. **Language.** Ask which language the learner wants explanations in (default English). Use it for every message from here on. Product names, commands and exam-style questions stay in English.
3. **Certification.** Fetch the current list from https://cloud.google.com/learn/certification and show it grouped by level (Foundational, Associate, Professional). Mark Associate Cloud Engineer as "curated" and the others as "beta (generated)". One certification per tracker.
4. **Pack.** Curated: the pack is `${CLAUDE_SKILL_DIR}/assets/packs/<certId>/` (relative path `assets/packs/<certId>/`; ACE is `ace`). Read [path.yaml](assets/packs/ace/path.yaml) and [gaps.yaml](assets/packs/ace/gaps.yaml) for titles and ids (step 6); the ready seed is in `assets/packs/ace/seed/` (see step 9); [pack.yaml](assets/packs/ace/pack.yaml) and [scoring.yaml](assets/packs/ace/scoring.yaml) are already inside the seed. Generated: say that this certification gets a generated pack labeled beta, follow [references/generated-pack.md](references/generated-pack.md) (without a built-in browser, ask the learner to paste the learning path outline or to open the chat in the Claude desktop app), and show the tree for confirmation before going on.
5. **Choices.** Ask in one message, with defaults: mode **Course** (learning path only) or **Full exam** (path plus exam-guide gaps; recommended before booking the exam); difficulty **Standard** or **Hard**; weekly study hours (default 7); exam date (optional). Explain each in one line.
6. **Initial progress.** Ask what is already done. Accept typed input such as "courses 1, 3, 4; course 6 modules 1-3". Course platforms number modules differently, so resolve every number to ids (Google Skills path order) and always ask "Do you mean course N <course title>, module(s) <module titles>?" before accepting it. On a no, ask the learner to type the course and module names, match them by title and confirm again. Titles given directly need one short confirmation. Or offer the browser check in [references/browser-progress-check.md](references/browser-progress-check.md). Never write completion marks the learner has not confirmed.
7. **Summary.** Show certification, pack type (beta if generated), mode, difficulty, language, pace, exam date, and the completed activities and modules by title, plus the estimated remaining hours and finish date (or required pace). Compute these numbers with [references/plan-estimate.md](references/plan-estimate.md) (curated pack: from `assets/packs/ace/seed/summary.json`, `planInputs`); the page shows the same numbers. Ask for confirmation. Nothing is published before a yes.
8. **Publish.** Load `${CLAUDE_SKILL_DIR}/assets/tracker-template.json` (relative path `assets/tracker-template.json`): the page is its `lines` array, one string per line. With code execution, `json.load` it and join the lines with `"\n"` (do the same by hand when code execution is unavailable). On the first line (the page title), replace `GCP Cert Coach` with `<Short name> Cert Coach` (for example `ACE Cert Coach`), save the result as an `.html` file and publish that file as a new artifact with the db capability and no other capabilities; keep the default access rules (the owner reads and writes). Change nothing else in the page.
9. **Seed.** Follow [references/seeding.md](references/seeding.md): curated pack (path A) writes the ready batches in `assets/packs/ace/seed/` in order, then the learner's choices and completion marks as small batches; a generated pack (path B) builds the batches by hand from the pack JSON. Translate `settings.ui` when the language is not English. Nothing is run and nothing needs installing.
10. **Verify.** Read back `meta/settings` and one page of `activities`, `modules` and `concepts`; compare the counts with the expected ones (13 activities, 86 modules, 284 concepts on path A; your own counts on path B). If something is missing, rewrite only the failed batch once; if it still fails, report what is missing.
11. **Hand-off.** Print, in one code block, two lines: `GCP Cert Coach tracker: <artifact URL> (certification: <certId>)` and `In this Project, use the gcp-cert-coach skills for every study request (explanations, quizzes, challenges, mock exams, progress).` (keep both in English, whatever the explanation language). Tell the learner to paste them into the instructions of a Claude Project used only for this certification, so every chat there finds the tracker. Then suggest the next step: a quiz on a completed module, a pre-test on the next module, or an explanation.

## Output format

- One question per message during setup, except step 5, which bundles the choices.
- The final message contains: the tracker link, the two Project instructions lines in one code block, a two-line summary of the setup, and one suggested next command (`/gcp-cert-coach:quiz`, `/gcp-cert-coach:learn` or `/gcp-cert-coach:progress`).

## Failure handling

- Certification list unavailable: offer the curated ACE pack or ask the learner to name the certification.
- Pack file unreadable: say which file failed. For ACE, ask the learner to try again in a new chat; do not invent the tree.
- Publish fails: nothing was written; show the summary again and ask to retry.
- A seed batch fails: retry that batch once; if it fails again, report which collections are incomplete and that running init again later will offer to reuse the tracker.
- Database unavailable after publishing: keep the published URL, explain that seeding did not happen, and print the tracker line anyway so a later init can finish seeding into the same page.

## Feedback

When the learner disputes content or suggests a change, write `feedback/<timestamp>-<4 random letters>` with `{ts, source: "learner", kind: "wrong_question" | "bug" | "improvement", text, logId: null, pluginVersion: settings.pluginVersion, status: "new"}`. Write `text` as a neutral summary without names, emails, project ids or pasted output, and tell the learner it was recorded.

## Version

Plugin version: 0.3.0. The seeded settings record it as `pluginVersion`, `templateVersion` and `latestPluginVersion`.

## Privacy

Store only learning progress and settings. Never store the learner's name, email, Google Cloud project ids or anything read from their account pages beyond completion marks.

## References

- [references/plan-estimate.md](references/plan-estimate.md): the plan estimate formula
- [references/seeding.md](references/seeding.md): ready seed batches, by-hand batches, document shapes, UI translation
- [references/generated-pack.md](references/generated-pack.md): building a beta pack for other certifications
- [references/browser-progress-check.md](references/browser-progress-check.md): reading progress from Google Skills or Coursera
- [assets/tracker-template.json](assets/tracker-template.json): the tracker page, as a JSON array of lines
- [assets/packs/ace/seed/summary.json](assets/packs/ace/seed/summary.json): counts and plan inputs of the ready ACE seed
- [assets/packs/ace/README.md](assets/packs/ace/README.md): how the curated ACE pack was built
