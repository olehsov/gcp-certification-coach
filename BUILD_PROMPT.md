# Build prompt for Claude Code

Open Claude Code in the folder that contains this file, `CLAUDE.md`, `CHECKLIST.md` and `docs/`, then paste the prompt below.

---

You are building v0.1.0 of the `gcp-cert-coach` plugin ("GCP Certification Coach") in this repository.

**Source of truth.** Read `CLAUDE.md`, `docs/PRD.md`, `docs/ARCHITECTURE.md`, every file in `docs/adr/`, `docs/seed/ace-path-snapshot.yaml`, `docs/seed/tracker-v0-reference.html` and `CHECKLIST.md` before writing anything. Follow them exactly. If something in them is ambiguous or contradicts the official Anthropic documentation, stop and ask me, proposing the fix.

**Working method.**
- Keep `CHECKLIST.md` up to date as you go: tick items and add a short evidence note (file path, command output summary). Use `[~]` with an explanation for any deviation.
- Track your phases in a task list.
- Commit locally after each phase with a conventional commit message. Do not create or push to a GitHub repository until phase 9.
- Everything you write is in English. Never put personal data in any file (see CLAUDE.md Privacy).

## Phase 0: Learn the rules

1. Fetch and read the official documentation listed in `CLAUDE.md` → "Official documentation to follow", including the Claude Code docs index to find the current pages for plugin creation, components, manifest reference, marketplaces and `claude plugin eval`.
2. Clone or browse `anthropics/knowledge-work-plugins` and study the `productivity` plugin's layout.
3. Write a short note at the top of `CHANGELOG.md` under "Unreleased → Build notes" listing any rule from the docs that is not already reflected in `CLAUDE.md` or the specs, and update those files accordingly.
4. Check `gh auth status` and that `gcp-certification-coach` is available on my account. Report the GitHub handle you will use as `author` (handle only).

## Phase 1: Scaffold

Create the structure from ARCHITECTURE §3: marketplace, plugin folder, manifest, nine empty skill folders, root documents (README stub, LICENSE MIT, LICENSE-CONTENT CC BY 4.0, CHANGELOG, CONTRIBUTING), `.gitignore`, `scripts/check-privacy.sh`, `scripts/privacy-allowlist.txt`, `scripts/setup-hooks.sh`, `.githooks/pre-commit`, `.githooks/pre-push`, `.github/workflows/validate.yml`. Run `claude plugin validate` on the empty plugin once to confirm the skeleton parses.

**Privacy setup, before the first commit:**

a. Create `scripts/check-privacy.sh`, `scripts/privacy-allowlist.txt`, `scripts/setup-hooks.sh`, `.githooks/pre-commit`, `.githooks/pre-push`, `.gitignore` and the CI workflow as described in CLAUDE.md → Privacy. Run `scripts/setup-hooks.sh`.
b. Ask me to create `~/.config/gcp-cert-coach/denylist.txt` myself. Do not ask for its contents and do not read it into the conversation.
c. Check whether gitleaks is installed; if not, give me the install command and continue (hooks skip it when absent, CI always runs it).
d. Prove the pre-commit hook works: stage a file with a fake email, confirm the commit is blocked, then remove it.
e. Prove the pre-push hook works: push to a throwaway local bare remote (outside the repo), confirm it runs all checks, then delete that remote.
f. Scan everything already committed with the privacy check (and gitleaks if available) and report the result.

## Phase 2: Evals before skills

Following evaluation-driven development from the skill best practices:

1. Run representative tasks without the plugin and record the gaps in `evals/BASELINE.md`.
2. Write at least 3 eval cases per skill in the format `claude plugin eval` expects, covering every case listed in CHECKLIST C3.
3. Write `evals/README.md`.

## Phase 3: ACE pack

1. Using the built-in browser or web fetch, re-verify `docs/seed/ace-path-snapshot.yaml` against the live Google Skills path (https://www.skills.google/paths/11) and the exam guide (https://cloud.google.com/learn/certification/guides/cloud-engineer). The Google Skills pages render activities with JavaScript; if you cannot read them, ask me to paste the outline.
2. Fill in the three skill badges (their labs as modules, the challenge lab, sections, hours, optional flag).
3. Verify every gap topic against the exam guide and attach 1–3 working official documentation URLs per gap concept.
4. Produce `skills/init/assets/packs/ace/` (`pack.yaml`, `path.yaml`, `gaps.yaml`, `scoring.yaml` with every constant from ARCHITECTURE §6 and a rationale each, `README.md`).
5. Write the learn cheat sheets listed in CHECKLIST G7.

## Phase 4: Tracker template

Build `skills/init/assets/tracker.html` from the prototype in `docs/seed/tracker-v0-reference.html`, rewritten in English to schema v1 and the page sections in ARCHITECTURE §5.4, following the artifact page contract in `CLAUDE.md`.

## Phase 5: Skills

Write the nine skills per ARCHITECTURE §8 and the CLAUDE.md skill rules, with their reference files. Then run the validator loop until clean: `claude plugin validate` → fix → repeat.

## Phase 6: Measure and tune

1. Run `claude plugin eval` and compare with the baseline; iterate on skills until every case passes and the plugin beats the baseline. Summarize in `evals/RESULTS.md`.
2. Use the skill-creator skill to tune each `description` for trigger accuracy, especially between `learn`, `quiz`, `challenge` and `mock`.
3. Run `/skill-doctor`; fix or explain each finding.
4. Run a subset of evals with Haiku, Sonnet and Opus; record differences and adjust instructions so all three work.

## Phase 7: Documentation

Write the root README (CHECKLIST I1, I2) with Mermaid diagrams adapted from ARCHITECTURE §10, the plugin README, CONTRIBUTING and the CHANGELOG entry. Check that every link resolves.

## Phase 8: Hand-off for manual test

1. Run `scripts/check-privacy.sh` and the full quality gates (CHECKLIST J).
2. Zip the plugin folder so it uploads on claude.ai (single top-level folder or its contents, with `.claude-plugin/plugin.json` at the right depth).
3. Stop and give me: the zip path, the exact manual test steps from CHECKLIST K, and a summary of open checklist items. Wait for my test results and fix anything I report.

## Phase 9: Publish (only after I confirm)

1. Create the public repository `gcp-certification-coach` on my account with the description "Claude plugin that coaches you for Google Cloud certifications: skill tree from the official learning path, exam-style quizzes, mastery tracking. Not affiliated with Google or Anthropic." and the topics from ADR 0009.
2. Before pushing, scan the full git history with `gitleaks detect` and the privacy check; stop if anything is found. Push, confirm CI is green, create release `v0.1.0` from the CHANGELOG. After pushing, enable secret scanning and push protection (or tell me where to click).
3. Verify installation from the public repository through claude.ai → Customize → Plugins → Add marketplace (ask me to do the click-through if you cannot).
4. Final pass over `CHECKLIST.md`: every item `[x]` or `[~]` with explanation. Report the result to me.
