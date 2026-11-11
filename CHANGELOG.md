# Changelog

All notable changes to this project are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Resume point

- **Current phase:** v0.2.0 fix round complete (phases A, B, C); waiting for the claude.ai re-test and the maintainer's "publish".
- **Last completed step:** J5 model comparison and the full Sonnet run (48 of 48 after fixes, see `evals/RESULTS.md` §10); docs synced; seed files and build prompt removed from the repository (kept outside it); gates and zip rebuilt.
- **Exact next step:** the claude.ai re-test list (upload zip, rebuild, one quiz, progress with titles, reset and restore). Phase 9 (publish) only after the maintainer says "publish".
- **Open issues:** J3 below the bar in the trigger harness (K2e decides); J7 CI never run (no remote).

### Changed in the v0.2.0 fix round (phase C)

- `mock`: the opening message states the question count per exam-guide section (section names stay out of question headers).
- Evals: fixture carries both lines that `init` prints; `quiz-warmup-after-pause` rubric reworded to what a read-only response can show.
- Repository: removed `docs/seed/` and `BUILD_PROMPT.md` (superseded by the pack and the template).

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
- **Seeding without the script**: `init` builds the seed batches by hand from the pack files when the seed script cannot run (no tool to run it, a script error, PyYAML unavailable), and says which path it used. claude.ai has no separate code-execution toggle, so this path is verified by an eval rather than by switching a setting.

## [0.2.0] - release date set at publishing

Fixes from the manual test on claude.ai.

### Fixed

- **Reset snapshots are restorable.** Snapshots now hold full copies of every document that is removed (chunked, row counts verified, `status: complete` before anything is changed), and `reset` has an explicit restore path that reads only from the snapshot, so it works in a new chat. `sync` and `rebuild` use the same format. Reset names the tracker it will wipe in the confirmation.
- **Question headers no longer give the answer away.** Quiz, pre-test, warm-up and mock headers read `Question N of M · <difficulty>` only.
- **Module numbers are always confirmed.** Numbers typed in `init` or `progress` are resolved, then confirmed with titles ("Do you mean course N <title>, module(s) <titles>?") before anything is written; a "no" leads to typed names matched by title.
- **Hedged answers** ("probably B", "I think the first one", "A or B, leaning A") count as confidence 1 and never create a misconception; unclear confidence or an unclear letter is asked about. The scale is now 1 guess or unsure, 2 fairly confident, 3 sure.
- **One plan formula.** `init`, `progress` and the page use the same estimate (`plan-estimate.md`); the seed script prints it.
- **One source for numeric facts** (`facts.md`): fixes the inconsistent Dedicated Interconnect capacities (10, 100 and 400 Gbps) and others.

### Changed

- Tracker page: "concepts mastered" count, explanations for module level, coverage and the `level · correct/answers` format, a "How levels work" note, and an "outdated page" notice.
- Version check: `templateVersion` and `latestPluginVersion` in `meta/settings` (schema stays 1). Skills compare them on their existing settings read and mention a newer page once per session; `rebuild` at the same version asks before republishing.
- Faster, cheaper sessions: selective reads in quiz, challenge and progress; the whole quiz session is planned in one step; curated documentation links are cited by default and fetched only on demand; `learn` fetches at most two pages ([ADR 0010](docs/adr/0010-curated-links-first.md)).
- Skills suggest a new chat per study session when a thread is already long; README has a "Usage and cost" section.

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
