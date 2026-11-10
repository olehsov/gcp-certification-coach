---
name: reset
description: Resets study progress in the GCP Certification Coach tracker after showing exactly what will be reset and kept, taking a snapshot of the current data and receiving an explicit confirmation phrase. Resets concept levels, the answer log and misconceptions while keeping the skill tree, settings and completion marks, unless the learner asks to clear completion marks or mock history too. Use when the learner says "reset my progress", "start over", "clear my quiz history", "wipe my levels" or "begin again from zero". Not for removing one wrong answer or disputing a question (use quiz), changing difficulty or mode (use progress), updating the tree (use sync) or fixing the page (use rebuild).
---

# Reset

A destructive operation, done carefully: plan → show → snapshot → explicit confirmation → execute.

## When to use

- The learner wants to start over with levels and history.
- Not for single corrections (quiz), settings (progress), tree changes (sync) or page problems (rebuild).

## Preconditions

- A tracker with a working artifact data tool (see Tracker access). Without the data tool, explain that nothing can be reset here and stop.

## Workflow

```
- [ ] 1. Locate the tracker; count what exists
- [ ] 2. Show the scope: what is reset, what is kept
- [ ] 3. Take the snapshot
- [ ] 4. Ask for the confirmation phrase
- [ ] 5. Execute in batches
- [ ] 6. Report
```

1. **Count** documents in `concepts` with progress (answers > 0 or level > 0), `log`, `misconceptions`, `mocks`, `challenges`, and modules marked completed.
2. **Scope.** By default:
   - **Reset:** every concept's `level` 0, `answers` 0, `correct` 0, `recent` [], `days` [], `lastReviewed` null, `bonus` 0; all `log` documents removed; all `misconceptions` removed.
   - **Kept:** activities, modules and concepts (the tree), `meta/settings`, completion marks, `mocks`, `challenges`, `feedback`, existing snapshots.
   - Add completion marks (`completed: false`, `completedAt: null` on every module) or mocks and challenges only when the learner asked for that. Show the scope with the counts, and say that a snapshot will be taken first and that the reset can be undone only by restoring from that snapshot.
3. **Snapshot** before asking: `set snapshots/<snapshotId>` with `{ts, reason: "reset", pluginVersion, counts}`, then copy every document that will change or be removed to `snapshots/<snapshotId>/<collection>/<id>` (batches of at most 50). Snapshot id: `reset-<YYYYMMDD-HHMM>`. If the snapshot fails, stop: no reset without a snapshot.
4. **Confirm.** Ask the learner to type the exact phrase `reset <certShortName> progress` (for example `reset ACE progress`). Anything else, including "yes" or "I'm sure" said before the scope was shown, is not confirmation. If the learner changes the scope, take the snapshot again for any newly included collection.
5. **Execute** in batches of at most 50 writes: concept updates; `log` and `misconceptions` deletes; module updates only if completion marks were included; `mocks` and `challenges` deletes only if included. Then `update meta/settings` with `updatedAt`.
6. **Report:** what was reset (counts), what was kept, the snapshot id, and a next step (a pre-test or a quiz on a completed module).

## Output format

Scope message: two short lists (reset, kept) with counts, the snapshot note, and the confirmation phrase in a code block. Result message: counts, snapshot id, next step. Prose in the learner's language.

## Tracker access

- **Locate:** a line `GCP Cert Coach tracker: <URL> (certification: <id>)` in the Project instructions or this conversation; otherwise the learner's artifact list, titles ending in "Cert Coach" (one: use it; several: ask which certification; none: nothing to reset). Never create a tracker here.
- **Writes:** pass the version you read for each document you update; on a version conflict re-read once and redo; if it fails again, stop, report what was done and point to the snapshot.
- **No data tool or database unavailable:** change nothing; explain that reset needs claude.ai or the Claude desktop app.

## Restoring

On request, restore from a snapshot by copying its documents back with `set` (after confirming which snapshot), then report the counts restored.

## Feedback

When the learner reports a problem or suggests a change, write `feedback/<timestamp>-<4 random letters>` with `{ts, source: "learner", kind: "bug" | "improvement", text, logId: null, pluginVersion: settings.pluginVersion, status: "new"}` (neutral text, no personal data) and tell the learner it was recorded. Feedback is never deleted by reset.

## Failure handling

- A batch fails during execute: stop, report which collections are fully reset, partly reset or untouched, and offer to finish or to restore from the snapshot.
