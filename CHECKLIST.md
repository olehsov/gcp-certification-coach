# Release checklist: v0.1.0

Every item must be checked before the repository is made public. The builder checks items as they are done and adds a short note or file path as evidence. Items map to the PRD (US-, FR-), ARCHITECTURE (§) and ADRs.

Legend: `[ ]` open · `[x]` done · `[~]` done with a deviation (explain in the note)

## A. Preparation

- [x] A1 Read PRD, ARCHITECTURE, all ADRs and CLAUDE.md — also docs/seed/* and BUILD_PROMPT.md
- [x] A2 Read the official docs listed in CLAUDE.md and note any rule that differs from these specs (update the specs, log in CHANGELOG) — CHANGELOG.md "Build notes"; CLAUDE.md updated (README `## Data`, file limits, frontmatter keys, relative paths on chat, eval command)
- [x] A3 Studied the `productivity` plugin in `anthropics/knowledge-work-plugins` as a structural reference — relative `source`, object `author`, skills-only layout, page template shipped inside the plugin
- [x] A4 Confirmed `gh` is authenticated and the repository name `gcp-certification-coach` is free on the owner's account — `gh auth status` ok (scopes repo, workflow); `gh repo view` → not found; author is the repository owner's public GitHub handle

## B. Repository structure (ADR 0009, ARCHITECTURE §3)

- [ ] B1 `.claude-plugin/marketplace.json` at repo root listing `gcp-cert-coach` from `./plugins/gcp-cert-coach`
- [ ] B2 `plugins/gcp-cert-coach/.claude-plugin/plugin.json` with `name: gcp-cert-coach`, `displayName: GCP Certification Coach`, `version: 0.1.0`, description with non-affiliation disclaimer, `author` (public GitHub handle only), `license: MIT`, homepage and repository URLs
- [ ] B3 Nine skill folders: `init`, `learn`, `quiz`, `challenge`, `mock`, `progress`, `sync`, `rebuild`, `reset`; folder name equals `name`
- [ ] B4 No `bin/` inside the plugin; only `plugin.json` inside the plugin's `.claude-plugin/`
- [ ] B5 `docs/`, `evals/`, `scripts/`, `.github/` outside the plugin folder
- [ ] B6 `README.md`, `LICENSE` (MIT), `LICENSE-CONTENT` (CC BY 4.0), `CHANGELOG.md`, `CONTRIBUTING.md` at repo root; plugin `README.md` (≥ 40 words: what it does, how to use it, what data it sends) and `LICENSE` inside the plugin folder

## C. Evals first (best practices: evaluation-driven development)

- [ ] C1 Baseline run without the plugin on representative tasks; failures documented in `evals/BASELINE.md`
- [ ] C2 At least 3 eval cases per skill (27+ total) in the format required by `claude plugin eval`
- [ ] C3 Cases cover at minimum: quiz uses only completed modules; no repeated question in a 30-question session; documentation link in every answer; guess-correct gives no gain; confident mistake creates a misconception; reset asks for confirmation and snapshots first; sync shows a diff before applying; init refuses a duplicate tracker without confirmation; progress browser check asks to sign in when signed out; explanation language follows settings while terms stay English
- [ ] C4 `evals/README.md` explains how to run them

## D. Skills (ARCHITECTURE §8, CLAUDE.md skill rules)

For each of the nine skills:

- [ ] D1 Frontmatter valid: `name` rules, third-person `description` ≤ 1024 chars with triggers and "not for" guidance
- [ ] D2 Body < 500 lines with purpose, when to use, preconditions, step checklist, output format, failure handling, links to every reference file
- [ ] D3 References one level deep; files > 100 lines start with a table of contents
- [ ] D4 Tracker locating procedure (§5.3) included where needed
- [ ] D5 Writes follow FR-3 (one batch per answer; mock in one batch at the end) with version pinning and one retry on conflict
- [ ] D6 No hardcoded surface-specific tool names; no time-sensitive phrasing; consistent terminology

Skill-specific:

- [ ] D7 `init`: language → certification list → curated or generated pack → mode, difficulty, pace, exam date → initial progress (manual or browser) → confirm → publish → seed in ≤ 50-write batches → read-back verify → print Project instructions line (US-1..4)
- [ ] D8 `init`: translates `settings.ui` for non-English languages; duplicate-tracker guard
- [ ] D9 `learn`: explanation format and lab breakdown format; documentation links; no course text reproduction (US-5, US-6)
- [ ] D10 `quiz`: selection priority §6.6; confidence 1/2/3; scoring §6.1; misconceptions §6.2; interleaving; no repeats; pre-test and warm-up modes; auto-resume (US-7..10, US-14)
- [ ] D11 `challenge`: no step-by-step; narrative + verification command outputs; redaction reminder; score and bonus §6.7; summary only stored (US-11)
- [ ] D12 `mock`: 50 questions weighted by sections; key revealed at end; one batch; verdict per profile (US-12)
- [ ] D13 `progress`: mark modules; browser check with all FR-9 fallbacks; confirm before writing; pause; mode and difficulty change; plan §6.9 (US-13..16)
- [ ] D14 `sync`: plan → diff → confirm → snapshot → apply; archived not deleted; `lastSyncAt` (US-17)
- [ ] D15 `rebuild`: schema migration list; republish to the same URL; data untouched (US-18)
- [ ] D16 `reset`: show scope → snapshot → explicit confirmation → reset; keeps tree and settings (US-19)
- [ ] D17 Feedback capture available from every skill (US-20, FR-12)

## E. Tracker template (ARCHITECTURE §5)

- [ ] E1 `skills/init/assets/tracker.html` follows the artifact page contract in CLAUDE.md
- [ ] E2 Implements schema v1 collections and all page sections in §5.4
- [ ] E3 Readiness label switches between "Course readiness" and "Exam readiness" (FR-10)
- [ ] E4 Effective level and decay computed for display (§6.5), statuses per §6.4
- [ ] E5 Mode and difficulty toggles write `meta/settings`; everything else read-only
- [ ] E6 UI strings from `settings.ui` with English fallbacks
- [ ] E7 Empty state, 10-second timeout message, "not synced for 30 days" notice, `beta` badge for generated packs
- [ ] E8 Works at 400 px, light and dark themes, reduced motion respected

## F. Scoring and configuration (ADR 0003, 0006, ARCHITECTURE §6)

- [ ] F1 All constants from §6 present in the pack's scoring file with a `rationale` per value
- [ ] F2 `init` copies scoring into `settings.scoring`; other skills read constants only from the tracker
- [ ] F3 Standard and Hard profiles complete
- [ ] F4 Verified on claude.ai that a skill can read its own `references/` and `assets/` (ADR 0006 build-time check); result noted here

## G. ACE pack (ARCHITECTURE §7, docs/seed/ace-path-snapshot.yaml)

- [ ] G1 Path re-verified against the live Google Skills path; all activities present, including the three skill badges with their modules
- [ ] G2 Optional flags mirror the path
- [ ] G3 Exam-guide sections and weights verified against the live exam guide; version recorded
- [ ] G4 Every exam-relevant module mapped to sections and weight
- [ ] G5 Gaps verified against the exam guide; 1–3 official doc URLs per gap concept, each URL fetched and working
- [ ] G6 Doc URLs for core concepts where obvious (optional for v0.1.0, but no broken links)
- [ ] G7 Cheat sheets in `skills/learn/references/`: compute choice, storage choice, load balancer choice, IAM role types and service accounts; original text, with links
- [ ] G8 Pack `README.md` with sources and verification date; no copied course text

## H. Generated packs (ARCHITECTURE §7.2)

- [ ] H1 Flow documented in `init` references; result labeled `beta`; learner confirms the tree before publishing
- [ ] H2 Fallback when no browser: paste outline or open in desktop app

## I. Documentation

- [ ] I1 Root `README.md`: what it is, who it's for, features, install (claude.ai Add marketplace; Claude Code command), quick start, command reference, modes and difficulty, how mastery works, privacy and data, FAQ, roadmap, contributing, license, disclaimer
- [ ] I2 Mermaid diagrams in README: component overview, `init` sequence, quiz sequence, module status states, data model (render-checked on GitHub)
- [ ] I3 `CONTRIBUTING.md`: how to add a pack, run evals, privacy rules, commit style
- [ ] I4 `CHANGELOG.md` with 0.1.0 entry
- [ ] I5 `evals/README.md`; `docs/` up to date with any deviations made during the build

## J. Quality gates

- [ ] J1 `claude plugin validate ./plugins/gcp-cert-coach` passes
- [ ] J2 `claude plugin eval` passes and beats the baseline; results summarized in `evals/RESULTS.md`
- [ ] J3 Descriptions tuned with the skill-creator skill for trigger accuracy (no false triggers between `quiz`, `mock`, `challenge`, `learn`)
- [ ] J4 `/skill-doctor` report reviewed; issues fixed or explained
- [ ] J5 Tested with Haiku, Sonnet and Opus; notes in `evals/RESULTS.md`
- [ ] J6 `scripts/check-privacy.sh` passes (emails, claude.ai artifact URLs, qwiklabs, project-id and billing-account patterns, API keys, non-English text in skills and templates, personal denylist from `~/.config/gcp-cert-coach/denylist.txt` when present)
- [ ] J7 `.github/workflows/validate.yml` runs plugin validate, the privacy check and gitleaks on push and pull request
- [ ] J8 All links in README and docs resolve
- [x] J9 `.githooks/pre-commit` runs the privacy check and gitleaks on staged files; tested by staging a fake email and confirming the commit is blocked — staged `leak-test.txt` with an invented address → "pre-commit: BLOCKED", exit 1; file removed
- [x] J10 `.gitignore` covers zips, eval run outputs, transcripts, `.env*`, `*.local.*` — `.gitignore` (also `evals/results/` written by `claude plugin eval`, OS files)
- [ ] J11 Full git history scanned once before publishing (gitleaks detect and the privacy check over all commits); nothing found
- [ ] J12 Maintainer has created the personal denylist outside the repository (Claude Code asks; never sees or commits its contents)
- [ ] J13 `.githooks/pre-push` runs the history scan, privacy check and plugin validate; tested once by pushing to a throwaway local bare remote
- [x] J14 `scripts/setup-hooks.sh` exists, is idempotent, and is documented in `CONTRIBUTING.md` — second run prints "already set"

## K. Manual end-to-end test on claude.ai (maintainer, before publishing)

- [ ] K1 Plugin zipped and uploaded via Customize → Plugins → Add → Upload plugin
- [ ] K2 In a new Project: `init` for ACE in a non-English language; tracker published and filled
- [ ] K3 Mark progress manually and via browser check
- [ ] K4 Quiz of 5 questions: only completed modules, confidence collected, tracker updates live
- [ ] K5 Pause, then quiz: plan resumes
- [ ] K6 `rebuild` keeps data; `reset` snapshots and asks for confirmation
- [ ] K7 Issues found are fixed and re-tested

## L. Publish

- [ ] L1 Maintainer confirms publishing
- [ ] L2 Public repository `gcp-certification-coach` created with description and topics from ADR 0009
- [ ] L3 Pushed; CI green
- [ ] L3a Secret scanning and push protection enabled in repository settings
- [ ] L4 Release `v0.1.0` with notes from CHANGELOG
- [ ] L5 Verified install from the public repo via Add marketplace on claude.ai
- [ ] L6 Social preview image added (optional)

## M. Decisions trace (from the design conversation)

Confirm each decision is implemented or explicitly deferred:

- [ ] M1 Plugin, not single skill; agents deferred to v2
- [ ] M2 Generic engine for any Google Cloud certification; curated ACE pack first; generated packs labeled beta
- [ ] M3 Tree from the Google Skills path (variable number of activities); optionality mirrors the path
- [ ] M4 Optional "Exam guide gaps" layer via Course / Full exam mode toggle
- [ ] M5 Standard / Hard profiles
- [ ] M6 Confidence: guess-correct = 0 gain; confident mistakes create misconceptions; calibration shown
- [ ] M7 Module-level completion marking; concept-level questioning and coverage
- [ ] M8 Question formats: scenario, multi-select, command recognition, explain in own words, choose a service, why others are wrong; interleaving
- [ ] M9 Pre-tests on the next module, no level change
- [ ] M10 Optional challenges with narrative + command output verification and bonus
- [ ] M11 Mock exams with red / amber / green recommendation (advice only)
- [ ] M12 Pause with automatic resume; warm-up after > 7 days
- [ ] M13 No exam date → plan from remaining hours and pace (default 7 h/week)
- [ ] M14 Write after every answer, one batch
- [ ] M15 Documentation via web search now; Developer Knowledge MCP in v2
- [ ] M16 One certification per Project per tracker; Project instructions line
- [ ] M17 Browser progress check with all fallbacks; never write without confirmation
- [ ] M18 `sync`, `rebuild`, `reset` separated by risk; reset archives first
- [ ] M19 Feedback collection for the maintenance loop
- [ ] M20 English everywhere; runtime explanation language
- [ ] M21 No personal data; CI privacy check
- [ ] M22 Copyright: titles and structure only; original questions; doc links
- [ ] M23 Non-affiliation disclaimer; MIT + CC BY 4.0
- [ ] M24 Public repo `gcp-certification-coach`, plugin `gcp-cert-coach`, display name GCP Certification Coach, topics set
