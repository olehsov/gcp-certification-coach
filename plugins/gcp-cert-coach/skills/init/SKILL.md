---
name: init
description: Sets up GCP Certification Coach for one Google Cloud certification. Asks the explanation language, lists current Google Cloud certifications, builds the skill tree from the official Google Skills learning path (curated pack for Associate Cloud Engineer, generated beta pack for others), records mode, difficulty, weekly hours, exam date and what the learner already completed, then publishes a private tracker page with a database and prints the line to paste into Project instructions. Use when the learner says "start preparing for a Google Cloud certification", "set up the coach", "init", "choose a certification" or "create my tracker". Not for marking progress in an existing tracker (use progress), updating the tree from the live path (use sync) or refreshing the tracker page (use rebuild).
---

# Init

Create one tracker per certification: an artifact page with a database that every other skill of this plugin reads and writes.

## When to use

- The learner starts preparing for a certification or asks to set up the coach.
- Not when a tracker for that certification already exists (see the duplicate guard), and not for progress updates, sync or page refreshes.

## Preconditions

- The artifact tool with the `db` capability and the artifact data tool are available (claude.ai chat, the Claude desktop app or Cowork). Without them, explain that the tracker needs one of those surfaces and stop after step 5 with the summary, so nothing is lost.
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
4. **Pack.** Curated: read `${CLAUDE_SKILL_DIR}/assets/packs/<certId>/` (relative path `assets/packs/<certId>/`; ACE is `ace`): [pack.yaml](assets/packs/ace/pack.yaml), [path.yaml](assets/packs/ace/path.yaml), [gaps.yaml](assets/packs/ace/gaps.yaml), [scoring.yaml](assets/packs/ace/scoring.yaml). Generated: follow [references/generated-pack.md](references/generated-pack.md) and show the tree for confirmation before going on.
5. **Choices.** Ask in one message, with defaults: mode **Course** (learning path only) or **Full exam** (path plus exam-guide gaps; recommended before booking the exam); difficulty **Standard** or **Hard**; weekly study hours (default 7); exam date (optional). Explain each in one line.
6. **Initial progress.** Ask what is already done. Accept typed input such as "courses 1, 3, 4; course 6 modules 1-3" (numbers follow the path order on Google Skills; resolve them to ids and echo the titles back) or offer the browser check in [references/browser-progress-check.md](references/browser-progress-check.md). Never write completion marks the learner has not confirmed.
7. **Summary.** Show certification, pack type (beta if generated), mode, difficulty, language, pace, exam date, and the completed activities and modules by title, plus the estimated remaining hours. Ask for confirmation. Nothing is published before a yes.
8. **Publish.** Take `assets/tracker.html` (`${CLAUDE_SKILL_DIR}/assets/tracker.html`), replace `<title>GCP Cert Coach</title>` with `<title><Short name> Cert Coach</title>` (for example `ACE Cert Coach`), and publish it as a new artifact with the db capability and no other capabilities; keep the default access rules (the owner reads and writes). Publish exactly this file; do not edit its code.
9. **Seed.** Follow [references/seeding.md](references/seeding.md): build the write batches (script or by hand), translate `settings.ui` when the language is not English, and write the batches in order with the artifact data tool.
10. **Verify.** Read back `meta/settings` and one page of `activities`, `modules` and `concepts`; compare the counts with the seed summary. If something is missing, rewrite only the failed batch once; if it still fails, report what is missing.
11. **Hand-off.** Print, in a code block, the line `GCP Cert Coach tracker: <artifact URL> (certification: <certId>)` and tell the learner to paste it into the instructions of a Claude Project used only for this certification, so every chat there finds the tracker. Then suggest the next step: a quiz on a completed module, a pre-test on the next module, or an explanation.

## Output format

- One question per message during setup, except step 5, which bundles the choices.
- The final message contains: the tracker link, the Project instructions line in a code block, a two-line summary of the setup, and one suggested next command (`/gcp-cert-coach:quiz`, `/gcp-cert-coach:learn` or `/gcp-cert-coach:progress`).

## Failure handling

- Certification list unavailable: offer the curated ACE pack or ask the learner to name the certification.
- Pack file unreadable: say which file failed. For ACE, ask the learner to try again in a new chat; do not invent the tree.
- Publish fails: nothing was written; show the summary again and ask to retry.
- A seed batch fails: retry that batch once; if it fails again, report which collections are incomplete and that running init again later will offer to reuse the tracker.
- Database unavailable after publishing: keep the published URL, explain that seeding did not happen, and print the tracker line anyway so a later init can finish seeding into the same page.

## Feedback

When the learner disputes content or suggests a change, write `feedback/<timestamp>-<4 random letters>` with `{ts, source: "learner", kind: "wrong_question" | "bug" | "improvement", text, logId: null, pluginVersion: settings.pluginVersion, status: "new"}`. Write `text` as a neutral summary without names, emails, project ids or pasted output, and tell the learner it was recorded.

## Privacy

Store only learning progress and settings. Never store the learner's name, email, Google Cloud project ids or anything read from their account pages beyond completion marks.

## References

- [references/seeding.md](references/seeding.md): document shapes, batch plan, script usage, UI translation
- [references/generated-pack.md](references/generated-pack.md): building a beta pack for other certifications
- [references/browser-progress-check.md](references/browser-progress-check.md): reading progress from Google Skills or Coursera
- [scripts/build_seed.py](scripts/build_seed.py): builds the seed batches from a pack
- [assets/tracker.html](assets/tracker.html): the tracker page template
- [assets/packs/ace/README.md](assets/packs/ace/README.md): how the curated ACE pack was built
