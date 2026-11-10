# ADR 0001: Ship as a plugin, not a single skill

- Status: Accepted
- Date: 2026-11-10

## Context

The coach needs several distinct actions (setup, explain, quiz, challenge, mock exam, progress, sync, rebuild, reset), shared conventions, a tracker template and certification content. A single skill would hold all of that in one `SKILL.md`, which conflicts with the 500-line guideline and makes triggering imprecise.

## Options

1. One skill with many reference files.
2. Several standalone skills installed separately.
3. One plugin bundling several skills, distributed through a marketplace repository.

## Decision

Option 3. One plugin `gcp-cert-coach` with one skill per action. The repository root is a marketplace (`.claude-plugin/marketplace.json`) and the plugin lives in `plugins/gcp-cert-coach/`.

## Consequences

- Installed once per account; available in claude.ai chat, the desktop app, Cowork and Claude Code.
- Each skill stays small, with a focused `description` for accurate triggering.
- Users run actions explicitly as `/gcp-cert-coach:<skill>` or by natural language.
- Updates flow from the GitHub repository ("Check for updates" or automatic sync).
- Skills must be self-contained (see ADR 0006).
