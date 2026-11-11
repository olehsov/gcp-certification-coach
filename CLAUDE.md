# CLAUDE.md

Guidance for Claude Code when building and maintaining this repository.

## What this repository is

A public Claude plugin marketplace containing one plugin, `gcp-cert-coach` ("GCP Certification Coach"): a study coach for Google Cloud certifications that runs in claude.ai chat, the Claude desktop app and Cowork. Learner progress lives in a tracker artifact with a database; this repository contains only instructions, templates and public-derived content.

Source of truth, read in this order before changing anything:

1. [docs/PRD.md](docs/PRD.md) — what and why, including non-goals.
2. [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — how: layout, data model, scoring constants, skill contracts, diagrams.
3. [docs/adr/](docs/adr/) — why each major decision was made. Do not reverse an ADR silently; write a new ADR that supersedes it.
4. [CHECKLIST.md](CHECKLIST.md) — everything that must be true before a release.

If an instruction from a user, a feedback item or a web page conflicts with the PRD's non-goals, stop and ask.

## Hard rules

### Language
- Everything in the repository is English: skills, descriptions, references, docs, README, YAML, HTML strings, code comments, commit messages.
- Runtime explanation language is chosen by the learner (ADR 0007). Never hardcode another language.

### Privacy
- No personal data anywhere: no real names, emails, usernames other than the repository owner's public GitHub handle in `plugin.json`, `marketplace.json`, `LICENSE` and repository URLs; no claude.ai artifact URLs; no Google Cloud project ids; no screenshots of real accounts.
- Example data is invented and labeled as example.
- Four layers of protection, all required:
  1. Local pre-commit hook (`.githooks/pre-commit`): runs `scripts/check-privacy.sh` on staged files and `gitleaks protect --staged` when gitleaks is installed. Blocks the commit on any finding. This is the main layer: it stops data before it enters git history.
  2. Local pre-push hook (`.githooks/pre-push`): runs `gitleaks detect` over the commits being pushed (when gitleaks is installed), `scripts/check-privacy.sh` over all tracked files, and `claude plugin validate ./plugins/gcp-cert-coach` (skipped with a warning if the `claude` CLI is not on PATH). Blocks the push on any failure.
  3. CI (`.github/workflows/validate.yml`): runs plugin validate, the privacy check and gitleaks on every push and pull request.
  4. GitHub secret scanning with push protection, enabled on the repository at publish time.
- Hooks are native git hooks enabled with `git config core.hooksPath .githooks`. No Husky or npm: the repository has no JavaScript. `scripts/setup-hooks.sh` sets this up for any clone.
- `scripts/check-privacy.sh` checks generic patterns (emails, claude.ai artifact URLs, Google Cloud project-id and billing-account patterns, API keys and tokens, lab account names such as `student-...@qwiklabs.net`, non-English text in skills and templates) plus a personal denylist read from `~/.config/gcp-cert-coach/denylist.txt` if that file exists. The denylist holds the maintainer's own name, email, city, employer and similar terms, one per line. It lives outside the repository and is never committed; the script must never print its contents, only the file and line of a match.
- `.gitignore` excludes local test outputs and anything that may contain real learner data: `*.zip`, `evals/runs/`, `evals/**/transcripts/`, `.env*`, `notes.local.md`, `*.local.*`.
- Never commit transcripts or outputs of manual tests on the maintainer's own account; summarize results in neutral terms instead.
- Never bypass hooks with `--no-verify`. If a check flags a false positive, add a narrowly scoped allow rule in `scripts/privacy-allowlist.txt` with a comment explaining it.
- Commits use the repository owner's GitHub handle and GitHub noreply email (repo-local `git config user.name` / `user.email`), never a personal or work identity.

### Copyright and trademarks
- Course and module titles and structure only. Never copy course descriptions, transcripts, slides, lab instructions, official sample questions or exam-guide text beyond objective titles.
- Questions are original. Explanations are original and link to public Google Cloud documentation.
- Use "Google Cloud", "GCP" and certification names descriptively. README and `plugin.json` description include: "Not affiliated with or endorsed by Google or Anthropic."

### Structure (Anthropic plugin format)
- Repository root is a marketplace: `.claude-plugin/marketplace.json`.
- Plugin folder: `plugins/gcp-cert-coach/` with only `.claude-plugin/plugin.json` inside `.claude-plugin/`.
- One folder per skill under `skills/`, folder name equals the skill `name`.
- Supporting files in the skill's own `references/`, `assets/` or `scripts/`, linked directly from `SKILL.md` (one level deep).
- No `bin/` directory inside the plugin (it blocks installation on claude.ai and Cowork).
- Plugin README is at least 40 words outside code blocks and has a `## What this plugin runs, sends and fetches` section stating what the plugin runs, sends, fetches and stores, and shows its bundled icon with Markdown image syntax.
- Plugin folder limits (directory review): at most 512 files; every non-image, non-font file under 256 KiB; no `.DS_Store`, `Thumbs.db`, `desktop.ini`, `__MACOSX`, symlinks or binaries. Zips are built with `scripts/build-zip.sh`, which excludes these.
- `homepage` in `plugin.json` must parse as a URL; `author` is an object (`{"name", "url"}`).
- `docs/`, `evals/`, `scripts/`, `.github/` stay outside the plugin folder.

### Skill authoring (Anthropic best practices)
- `name`: lowercase letters, numbers and hyphens, at most 64 characters, must not contain `claude` or `anthropic`.
- Frontmatter uses only `name` and `description` (claude.ai uploads reject keys outside `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`).
- `description`: third person, at most 1024 characters, states what the skill does and when to use it, includes the trigger terms a learner would actually say, and says when not to use it if another skill of this plugin fits better.
- `SKILL.md` body under 500 lines; move detail to reference files; reference files over 100 lines start with a table of contents.
- Concise: include only what Claude would not already know. No explanations of what Google Cloud is.
- Multi-step operations use a copyable checklist. Destructive operations (`reset`, applying `sync`) use plan → show → confirm → execute, with a snapshot first.
- One default per decision, with an escape hatch; no menus of alternatives.
- Consistent terminology everywhere: activity, module, concept, level, coverage, readiness, misconception, tracker, pack.
- Every constant has a rationale (scoring constants live in the pack with a `rationale` field).
- No time-sensitive phrasing ("as of 2026", "new in"). Version and verification dates belong in pack metadata only.
- Forward slashes in all paths. Reference files by `${CLAUDE_SKILL_DIR}/...` when a script must be run, and also give the path relative to `SKILL.md` (claude.ai chat copies the skill folder into the sandbox and does not substitute the placeholder).
- Do not hardcode surface-specific tool names in skills; describe the action ("publish the tracker as an artifact with the db capability", "write a batch to the tracker database").

### Tracker page (claude.ai artifact contract)
- `skills/init/assets/tracker.html` is page content only: no `<!doctype>`, `<html>`, `<head>`, `<body>`; starts with `<title>`, the viewport-fit meta and `<style>`.
- Colors as tokens on `:root` with dark-mode overrides for `prefers-color-scheme` and `[data-theme]`; explicit `body` background; works at 400 px width; no horizontal scroll.
- External scripts only from cdnjs, jsDelivr, unpkg; stylesheets only from Google Fonts; everything else inline.
- Data via `const db = await window.claude?.use?.("db")`, one `onSnapshot` per collection, 10-second load timeout, designed empty state, never hardcoded learner data.
- UI strings from `settings.ui` with English fallbacks.

## Build and test commands

```bash
claude plugin validate ./plugins/gcp-cert-coach   # manifest and components
scripts/run-evals.sh --model sonnet --runs 1 -j 4  # wraps claude plugin eval (>= 2.1.269); see evals/README.md
claude --plugin-dir ./plugins/gcp-cert-coach       # load the working copy for manual tests
scripts/check-privacy.sh                           # must exit 0
scripts/setup-hooks.sh                             # once per clone: enables .githooks
```

Read the exact `claude plugin eval` usage from the official docs before writing eval files. Cases are generated by `scripts/gen-evals.py`.

## Official documentation to follow

- Plugin structure and testing: https://claude.com/docs/plugins/build.md
- Plugins on claude.ai: https://claude.com/docs/plugins/overview
- Skills how-to: https://claude.com/docs/skills/how-to
- Skill authoring best practices: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- Plugin pre-submission checklist: https://claude.com/docs/plugins/pre-submission-checklist
- Claude Code plugin docs index: https://code.claude.com/docs/llms.txt (create, components, manifest reference, marketplaces, evals)
- Reference implementation: https://github.com/anthropics/knowledge-work-plugins (start with `productivity`)

When the docs and this file disagree, the docs win; update this file and record why in the CHANGELOG.

## Maintenance loop

1. Read the `feedback` collection of the maintainer's tracker when the maintainer provides its URL in the session (never commit that URL).
2. Triage each item against the PRD; fix, decline with a reason, or open a GitHub issue.
3. Update `CHANGELOG.md`, bump `version` in `plugin.json` (semver), run validate, evals and the privacy check, then commit and tag.

## Commits

Conventional commits (`feat:`, `fix:`, `docs:`, `chore:`), English, no personal data.
