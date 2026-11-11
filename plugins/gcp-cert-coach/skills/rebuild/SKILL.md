---
name: rebuild
description: "Updates the GCP Certification Coach tracker page to the current plugin version without touching learner data. Reads the current page and settings, migrates the tracker database when its schema version is older, and republishes the page template to the same artifact URL. Use when the learner says \"rebuild\", \"update the tracker page\", \"the tracker looks outdated or broken\", \"the page shows old sections\", after a plugin update, or when another skill reports an older schema version. Not for checking the learning path or exam guide for changes (use sync), resetting progress (use reset) or creating a tracker (use init)."
---

# Rebuild

Replace the page code, keep the data. The URL stays the same, so the Project instructions line keeps working.

## When to use

- After a plugin update, when the page looks broken or outdated, or when a skill finds `schemaVersion` below 1.
- Not for tree changes (sync), progress (reset, progress) or a new tracker (init).

## Preconditions

- An existing tracker (see Tracker access). Rebuild never creates one; with no tracker, ask for its URL or offer `/gcp-cert-coach:init`.
- The artifact tool (read and publish) and the artifact data tool.

## Workflow

```
- [ ] 1. Locate the tracker; read the page and meta/settings
- [ ] 2. Decide: migration needed or page only
- [ ] 3. Show the plan and confirm
- [ ] 4. Migrate data (if needed), with a snapshot first
- [ ] 5. Republish the template to the same URL
- [ ] 6. Update settings and verify
```

1. **Read** the current page (artifact read) and `meta/settings`. Note `schemaVersion` (a tracker without `meta/settings` but with `courses`/`topics` collections is schema 0), `pluginVersion`, `templateVersion` (missing means `pluginVersion`) and the `PLUGIN_VERSION` constant in the template you ship.
2. **Decide.** `schemaVersion` = 1 and `templateVersion` equal to the shipped version: say "Already up to date (<version>). Republish anyway?" and republish only on a yes (a learner who reports a broken page counts as a yes). `schemaVersion` = 1 and an older template: page only. Lower: run the migrations in [references/migrations.md](references/migrations.md) in order. Higher than 1: stop; the plugin is older than the tracker, ask the learner to update the plugin.
3. **Plan.** Tell the learner what will happen: page republished to the same URL; data unchanged, or, when a migration is needed, each migration step by its short name from [references/migrations.md](references/migrations.md) (for 0 → 1: choose the pack, map courses to activities, map topics to modules, migrate the log, write the new tree, archive the old collections), with the snapshot first. Show this plan even when the session cannot write (no artifact tools), so the learner knows what the rebuild will do. Ask for confirmation when a migration is needed; a page-only rebuild needs no confirmation beyond the request.
4. **Migrate** (only when needed): take a snapshot of every document the migration changes or removes, following [references/snapshots.md](references/snapshots.md) (id `migration-<YYYYMMDD-HHMM>`, full copies, verified), then apply the steps in batches of at most 50 writes.
5. **Republish** [assets/tracker.html](assets/tracker.html) (`${CLAUDE_SKILL_DIR}/assets/tracker.html`) to the **same artifact URL**, replacing `<title>GCP Cert Coach</title>` with `<title><certShortName> Cert Coach</title>`. Keep the db capability; leave the capability declaration as it is (do not clear it). Publish exactly this file; do not edit its code.
6. **Finish:** `update meta/settings` with `pluginVersion`, `templateVersion` and `latestPluginVersion` (all the `PLUGIN_VERSION` constant in the template's script), `schemaVersion: 1` after a migration, `updatedAt`. If `settings.language` is not English and `settings.ui` lacks keys used by the new template (compare with the `EN` map in the template's script, including newly added labels and help texts), translate every missing key, keeping `{placeholders}`. Ask the learner to reload the page and confirm it shows their data.

## Output format

A short plan, then a result: URL (unchanged), version before → after (page and data), migrations applied (or "none"), snapshot id when one was taken.

## Tracker access

- **Locate:** a line `GCP Cert Coach tracker: <URL> (certification: <id>)` in the Project instructions or this conversation; otherwise the learner's artifact list, titles ending in "Cert Coach" (one: use it; several: ask which certification; none: ask for the URL or offer `/gcp-cert-coach:init`). Never create a tracker here.
- **Version:** Plugin version: 0.2.2. Schema newer than 1: stop and ask the learner to update the plugin. Rebuild is the skill that fixes an older schema or template; it never asks the learner to rebuild.
- **Writes:** pass the version you read for each document you update; on a version conflict re-read once and redo; if it fails again, stop and report.
- **No artifact or data tool:** explain that rebuilding needs claude.ai or the Claude desktop app, and change nothing.

## References

- [references/migrations.md](references/migrations.md): schema migrations
- [references/snapshots.md](references/snapshots.md): snapshot format
- [assets/tracker.html](assets/tracker.html): the page template

## Feedback

When the learner reports a page problem, write `feedback/<timestamp>-<4 random letters>` with `{ts, source: "learner", kind: "bug", text, logId: null, pluginVersion: settings.pluginVersion, status: "new"}` (neutral description, no personal data) and tell the learner it was recorded.

## Failure handling

- Publish to the same URL is refused (no edit access): stop; never publish to a new URL, because that would create a second tracker.
- Migration fails midway: stop, report which steps completed, and point to the snapshot; do not republish the new page until the data matches its schema.
