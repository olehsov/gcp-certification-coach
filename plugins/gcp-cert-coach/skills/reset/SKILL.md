---
name: reset
description: Resets study progress in the GCP Certification Coach tracker after naming the tracker, showing exactly what will be reset and kept, taking a restorable snapshot of the data and receiving an explicit confirmation phrase; can also restore progress from a snapshot in any chat. Resets concept levels, the answer log and misconceptions while keeping the skill tree, settings and completion marks, unless the learner asks to clear completion marks or mock history too. Use when the learner says "reset my progress", "start over", "clear my quiz history", "wipe my levels", "begin again from zero", or "restore my progress from the last snapshot", "undo the reset". Not for removing one wrong answer or disputing a question (use quiz), changing difficulty or mode (use progress), updating the tree (use sync) or fixing the page (use rebuild).
---

# Reset

A destructive operation, done carefully: plan → show → snapshot → explicit confirmation → execute. The snapshot holds full copies of what is removed, so the reset can be undone later, even in a new chat.

## When to use

- The learner wants to start over with levels and history, or to restore progress from a snapshot.
- Not for single corrections (quiz), settings (progress), tree changes (sync) or page problems (rebuild).

## Preconditions

- A tracker with a working artifact data tool (see Tracker access). Without the data tool, show the scope and the snapshot plan as in Tracker access, change nothing, and say a session on claude.ai or the desktop app is needed.
- Snapshot format and restore procedure: [references/snapshots.md](references/snapshots.md).

## Workflow: reset

```
- [ ] 1. Locate the tracker; count what exists
- [ ] 2. Show the scope: what is reset, what is kept
- [ ] 3. Take the snapshot (full copies, verified)
- [ ] 4. Ask for the confirmation phrase
- [ ] 5. Execute in batches
- [ ] 6. Report
```

1. **Count** documents in `concepts` with progress (answers > 0 or level > 0), `log`, `misconceptions`, `mocks`, `challenges`, and modules marked completed. Read the tracker's title (the artifact title, `<certShortName> Cert Coach`) and `certName`.
2. **Scope.** Start the message with the tracker: "This resets **<tracker title>** (<certName>)." By default:
   - **Reset:** every concept's `level` 0, `answers` 0, `correct` 0, `recent` [], `days` [], `lastReviewed` null, `bonus` 0; all `log` documents removed; all `misconceptions` removed.
   - **Kept:** activities, modules and concepts (the tree), `meta/settings`, completion marks, `mocks`, `challenges`, `feedback`, existing snapshots.
   - Add completion marks (`completed: false`, `completedAt: null` on every module) or mocks and challenges only when the learner asked for that. Show the scope with the counts, and say that a full snapshot will be taken first and that the reset can be undone by restoring from it.
3. **Snapshot** before asking, following [references/snapshots.md](references/snapshots.md) section 2: id `reset-<YYYYMMDD-HHMM>`, full copies (every field) of every document that will change or be removed, chunked, read back and verified, `status: "complete"`. If the snapshot cannot be completed, stop: no reset without a complete snapshot.
4. **Confirm.** Ask the learner to type the exact phrase `reset <certShortName> progress` (for example `reset ACE progress`). Anything else, including "yes" or "I'm sure" said before the scope was shown, is not confirmation. If the learner changes the scope, take the snapshot again for any newly included collection.
5. **Execute** in batches of at most 50 writes: concept updates; `log` and `misconceptions` deletes; module updates only if completion marks were included; `mocks` and `challenges` deletes only if included. Then `update meta/settings` with `updatedAt`.
6. **Report:** what was reset (counts), what was kept, the snapshot id, how to restore ("say: restore my progress from the last snapshot"), and a next step (a pre-test or a quiz on a completed module).

## Workflow: restore

Follow [references/snapshots.md](references/snapshots.md) section 3. The restore message must contain: the tracker named; the snapshot (id, reason, date, row counts per collection); what restoring changes (documents in the snapshot are overwritten with their saved content, documents created after the snapshot are kept, the tree, settings and completion marks are untouched unless in the snapshot); the saved values it will bring back (read from the snapshot chunks); a restore snapshot of the current state taken first; and the phrase `restore <certShortName> progress` to type. Then write the rows back **from the snapshot chunks only** (never from this conversation), read back and report counts. In a session without the data tool, show this same message and say nothing was restored. Restore works in a new chat: everything needed is in the tracker.

## Output format

Scope message: the tracker named first, two short lists (reset, kept) with counts, the snapshot note, and the confirmation phrase in a code block. Result message: counts, snapshot id, how to restore, next step. Prose in the learner's language.

## Tracker access

- **Locate:** a line `GCP Cert Coach tracker: <URL> (certification: <id>)` in the Project instructions or this conversation; otherwise the learner's artifact list, titles ending in "Cert Coach" (one: use it; several: ask which certification; none: nothing to reset). Never create a tracker here.
- **Version:** Plugin version: 0.2.0. On the `meta/settings` read, compare versions. `schemaVersion` below 1: stop and offer `/gcp-cert-coach:rebuild` first; above 1: ask the learner to update the plugin. `templateVersion` (missing means `pluginVersion`) older than the plugin version: say once per session, in one line, "A new tracker page is available (x → y). Say 'rebuild' to update it."; never rebuild on your own. `latestPluginVersion` older than the plugin version: include it in the settings write this skill makes anyway; never write only for this.
- **Writes:** pass the version you read for each document you update; on a version conflict re-read once and redo; if it fails again, stop, report what was done and point to the snapshot.
- **No data tool or database unavailable:** change nothing. If the conversation contains a tracker export, show the scope with counts and the snapshot plan (metadata plus chunk documents, as JSON), say nothing was changed, and that the reset needs claude.ai or the Claude desktop app. A restore request without the data tool: explain the same.

## Feedback

When the learner reports a problem or suggests a change, write `feedback/<timestamp>-<4 random letters>` with `{ts, source: "learner", kind: "bug" | "improvement", text, logId: null, pluginVersion: settings.pluginVersion, status: "new"}` (neutral text, no personal data) and tell the learner it was recorded. Feedback is never deleted by reset.

## Failure handling

- A batch fails during execute: stop, report which collections are fully reset, partly reset or untouched, and offer to finish or to restore from the snapshot.
- A snapshot lacks chunks or its counts do not match: say it cannot be restored; never rebuild its data from the conversation.

## References

- [references/snapshots.md](references/snapshots.md): snapshot format, verification, restore
