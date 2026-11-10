# Changelog

All notable changes to this project are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Resume point

- **Current phase:** 8 done; waiting for the manual test on claude.ai (J5 and the full eval run moved after it by maintainer decision).
- **Last completed step:** Phase 8 gates passed (validate --strict x2, privacy tracked and history, gitleaks full history, consistency, links 182/0); zip built at dist/gcp-cert-coach-0.1.0.zip and verified. Phase now: waiting for the maintainer's manual test (CHECKLIST K).
- **Exact next step:** apply fixes from the manual test results, then J5 (5 cases x 3 models, with-plugin), one full run with and without plugin, fill evals/RESULTS.md placeholders, then Phase 9 (publish) after the maintainer confirms.
- **Open issues:** J3 below the bar in the trigger harness (K2e decides); J2 and J5 deferred until after the manual test; J7 CI never run (no remote).

### Build notes

Rules from the official documentation that were not reflected in `CLAUDE.md` or the specs, and how they were applied:

- **Plugin README `## Data` section and 40-word minimum** (pre-submission checklist). Added to `CLAUDE.md` → Structure; already covered by CHECKLIST B6.
- **Plugin folder limits** (pre-submission checklist): at most 512 files, every non-image file under 256 KiB, no `.DS_Store`, `Thumbs.db`, `desktop.ini`, `__MACOSX`, symlinks or binaries. Added to `CLAUDE.md`; enforced in CI and by `scripts/build-zip.sh`.
- **Upload zip layout** (plugins overview): the archive holds exactly one `.claude-plugin/plugin.json`, at the zip root or inside a single top-level folder.
- **SKILL.md frontmatter keys** (Claude Code skills reference): uploads outside Claude Code reject keys other than `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`. Skills in this plugin use only `name` and `description`. Added to `CLAUDE.md`.
- **`${CLAUDE_SKILL_DIR}` is not substituted on claude.ai chat** (skills how-to): the skill folder is copied into the sandbox, so references also give the path relative to `SKILL.md`. Added to `CLAUDE.md`.
- **Manifest details** (manifest reference): `author` is an object with `name` (and optional `url`); `homepage` must parse as a URL; plugin names must not start with `claude-` or `anthropic-`. Added to `CLAUDE.md`.
- **`claude plugin eval`** (plugin evals docs): needs Claude Code 2.1.269 or later; cases are directories with `prompt.md` (frontmatter + prompt) and `graders/*.md`; the eval directory must sit inside the plugin root (see below). Command added to `CLAUDE.md`.
- **`/skill-doctor`** reports per-skill context cost and usage (Claude Code 2.1.252 or later); used in Phase 6 as a cost and usage review.
- **Evaluation sandbox limits**: eval runs happen in Claude Code with read-only tools by default, where the tracker artifact database is not available. Eval cases therefore provide a tracker snapshot as a fixture and grade behavior (selection, scoring arithmetic, confirmation steps, planned write batches) rather than real database writes. Real database behavior is covered by the manual test (CHECKLIST K).
- **Privacy hardening** (maintainer spec update): native git hooks (`.githooks/`), personal denylist outside the repository, gitleaks in hooks and CI, repo-local commit identity using the GitHub noreply address.
- **Eval directory must be inside the plugin root** (`claude plugin eval` rejects `..`). `evals/` stays at the repository root per the layout rule; `scripts/run-evals.sh` stages a temporary plugin copy with the cases inside it and keeps reports local (`--no-publish`).
- **Eval runs need a standalone CLI login** (`claude auth login`); a desktop-app session does not authenticate the eval child processes.
- **`settings.pauseHistory`** (spec clarification): `pausedDaysTotal` alone cannot tell which paused days fall after a concept's `lastReviewed`, so completed pauses are also kept as `[{since, until}]`. ARCHITECTURE §5.2 and §6.5 updated.
- **Self-contained skill copies** (ADR 0006): `rebuild` ships its own copy of `tracker.html`, and `progress` its own copy of the browser progress check; `scripts/check-consistency.sh` (CI) keeps the copies identical and the plugin version equal in `plugin.json`, `marketplace.json`, `build_seed.py` and the template.
- **`modules.labs`**: informational list of lab titles per module, seeded from the pack and used by learn and challenge (ARCHITECTURE §5.2 addition).
- **Project instructions skills line**: `init` prints a second line for the Project instructions asking Claude to use the plugin's skills for every study request, because skills under-trigger on plain study requests (`evals/RESULTS.md`, trigger accuracy).
- **Seeding without code execution**: `init` builds the seed batches by hand from the pack files when the seed script cannot run, and says which path it used.

## [0.1.0] - release date set at publishing

First release.

### Added

- Marketplace `gcp-certification-coach` with one plugin, `gcp-cert-coach` (GCP Certification Coach).
- Nine skills: `init`, `learn`, `quiz`, `challenge`, `mock`, `progress`, `sync`, `rebuild`, `reset`.
- Tracker page template (schema version 1) published as a private artifact with a database: plan, exam-guide sections, review queue, skill tree, misconceptions, calibration, mock history, recent answers; mode and difficulty toggles; dark mode; phone width.
- Curated Associate Cloud Engineer pack built from the Google Skills learning path and the exam guide (titles and structure only), with exam-guide gap topics and scoring constants with rationale.
- Generated packs (beta) for other Google Cloud certifications.
- Mastery model: confidence-weighted updates, misconceptions, review intervals, decay with pause handling, coverage, readiness, plan estimate.
- Eval suite (37 cases) for `claude plugin eval`, trigger query sets, and results in `evals/RESULTS.md`.
- Privacy protection: pre-commit and pre-push hooks, privacy check with a personal denylist outside the repository, gitleaks, CI validation.
