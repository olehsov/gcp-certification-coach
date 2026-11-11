# ADR 0011: Data-only plugin folder: JSON page template and prebuilt seed

- Status: Accepted
- Date: 2026-11-11
- Supersedes: the seed-script part of the init design (`skills/init/scripts/build_seed.py`) and the `tracker.html` asset in ARCHITECTURE §3 and §5.1. ADR 0006 still holds (self-contained skills, configuration in the tracker).

## Context

The Claude directory refused version 0.2.3: only Verified organizations may ship files outside Markdown, plain text, JSON, YAML and PNG/JPEG/GIF/WebP/ICO. Types are detected by content, not by name. No file may start with `#!`, package-manager config files are rejected, and text must be UTF-8 without NUL bytes. The plugin shipped an HTML page template (two copies), a Python seed script, and a skill file that content detection also read as HTML (it quoted page tags in its first lines).

A Markdown file holding the page in an html fence was tested and is still detected as HTML (libmagic looks at the first 4 KiB). A JSON file is detected as JSON.

## Decision

- The plugin folder holds only Markdown, YAML, JSON and one PNG. `scripts/check-file-types.sh` enforces this with two content detectors (libmagic and Magika), a `#!` check, an extension allow-list and a package-manager denylist. It runs in the pre-push hook, in CI and before the zip is built.
- The tracker page is edited in `templates/tracker.html` (repository only, previewable in a browser). `scripts/build-plugin-data.py` generates `skills/{init,rebuild}/assets/tracker-template.json`: `{"format": "tracker-template", "version", "lines": [...]}`, one string per page line, byte-identical copies. `init` and `rebuild` join the lines, replace the title text, save an `.html` file and publish it. Joining by hand is the fallback without code execution.
- The curated ACE seed is generated offline by the same script into `skills/init/assets/packs/ace/seed/` (`batch-01..08.json`, `ui-strings-en.json`, `summary.json`), in the artifact data tool's batch entry shape. `init` writes the batches unchanged, then applies the learner's choices (settings, language strings, completion marks) as small pinned `update` batches, then reads back counts (13 activities, 86 modules, 284 concepts). `summary.json` carries the plan inputs, so the plan numbers match the page.
- Generated packs (beta) are seeded by Claude building the batches by hand from the pack JSON; no script exists on that path.
- `scripts/check-consistency.sh` regenerates the data into a temporary folder and fails when the shipped template JSON or seed differs, so the sources and the shipped files cannot drift.
- Skill text does not quote page tags: libmagic classifies a Markdown file as HTML when such tags appear near its start.

## Consequences

- The plugin runs no code of its own; the README's "runs" section says so.
- Seed equivalence with the old script was verified for three learner setups (documents and plan estimates equal, apart from timestamps).
- Editing the page or the pack requires running `scripts/build-plugin-data.py` (PyYAML) and committing the result; CI catches a forgotten run.
- Learner writes after the static seed update existing documents, so each is pinned with `if_version`.
