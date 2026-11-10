---
name: sync
description: Checks the GCP Certification Coach tracker against the live Google Skills learning path and the official Google Cloud exam guide, shows a diff (added, removed and renamed activities, modules and concepts, exam-guide sections, weights and version), and applies it only after the learner confirms, taking a snapshot first, archiving removed items instead of deleting them and keeping all progress on renamed items. Use when the learner says "sync", "check for updates to the course or exam guide", "the course changed", "a module is missing", or when the tracker shows it was not synced for 30 days. Not for marking modules completed (use progress), refreshing the tracker page code (use rebuild) or starting over (use reset).
---

# Sync

Keep the tree current without losing progress. Destructive changes follow plan → show → confirm → snapshot → apply.

## When to use

- The path or exam guide may have changed, the page shows the stale-sync notice, or a module the learner sees is missing.
- Not for completion marks (progress), page code (rebuild) or resetting levels (reset).

## Preconditions

- A tracker (see Tracker access) with a working data tool; sync never runs in read-only mode except to show the diff.
- Web fetch for the exam guide; the built-in browser for Google Skills pages (they render with JavaScript). Without a browser, ask the learner to paste the current outline or to open the chat in the Claude desktop app.

## Workflow

```
- [ ] 1. Read the tracker tree and settings
- [ ] 2. Read the live learning path and exam guide
- [ ] 3. Build the diff
- [ ] 4. Show the diff and ask for confirmation
- [ ] 5. Snapshot the documents that will change
- [ ] 6. Apply in batches
- [ ] 7. Update lastSyncAt and report
```

1. **Read** `meta/settings`, `activities`, `modules`, `concepts` (archived included).
2. **Live sources.** Exam guide: `settings.examGuide.url` — section names and weights, objective ids and titles only. Path: `settings.path.url` and each activity page — activity titles, stated hours, optional marks, module titles and item titles (as in the generated-pack rules: drop quizzes, lab intros and reviews; skill-badge labs are modules). If the learner pasted an outline, use it instead and say so.
3. **Diff** with [references/diff-and-apply.md](references/diff-and-apply.md): match by id where the source gives one, else by order and title similarity; classify every difference as added, removed, renamed, moved, changed hours or optional flag, or section mapping change; and compare exam-guide version, sections and weights.
4. **Show** the diff grouped by activity, with counts and the effect on progress for each item ("renamed: keeps level and completion", "removed: archived, hidden from quizzes, data kept", "added: level 0, not completed"). For new modules, propose `sections`, `weight` and `examRelevant`. Ask for an explicit yes. Partial approval ("only the renames") is fine.
5. **Snapshot** before any change: `set snapshots/<snapshotId>` (`ts`, `reason: "sync"`, `pluginVersion`, `counts`) and copies of every document that will be updated or archived under `snapshots/<snapshotId>/<collection>/<id>`. Snapshot id: `sync-<YYYYMMDD-HHMM>`.
6. **Apply** in batches of at most 50 writes: added items `set` with level 0 and not completed; renamed or moved items `update` title, order and fields while keeping id, level, answers, completion; removed items `update archived: true` (never delete); exam-guide changes `update meta/settings.examGuide`. New concepts get ids that do not collide with existing ones (next free `-k<N>`; new modules next free `-m<N>`).
7. **Finish:** `update meta/settings` with `lastSyncAt` (now) and `updatedAt`. Report what changed and what it means (for example "readiness may drop because a new core module was added"). With no differences, only update `lastSyncAt` and say the tracker is current.

## Output format

Diff tables per activity: change, item, before → after, effect on progress. A one-line summary with counts. Prose in the learner's language; titles as they appear on the source pages.

## Tracker access

- **Locate:** a line `GCP Cert Coach tracker: <URL> (certification: <id>)` in the Project instructions or this conversation; otherwise the learner's artifact list, titles ending in "Cert Coach" (one: use it; several: ask which certification; none: offer `/gcp-cert-coach:init`). Never create a tracker here.
- **Schema:** if `meta/settings.schemaVersion` is above 1, ask the learner to update the plugin; below 1, run `/gcp-cert-coach:rebuild` first.
- **Writes:** batches as above. Pass the version you read for each document you update; on a version conflict re-read once and redo; if it fails again, stop, report what was applied and point to the snapshot.
- **No data tool or database unavailable:** show the diff and the apply plan in order (snapshot of the affected documents first, then the changes, archived not deleted), say nothing was applied, and say that confirmation will be asked in a session that can write.

## Feedback

When the learner reports that the path or pack is wrong, write `feedback/<timestamp>-<4 random letters>` with `{ts, source: "learner", kind: "bug" | "improvement", text, logId: null, pluginVersion: settings.pluginVersion, status: "new"}` (neutral text, no personal data) and tell the learner it was recorded.

## Failure handling

- Live page unreadable or signed out: ask the learner to sign in or paste the outline; never treat an unreadable page as "everything removed".
- More than a third of the tree would be removed: stop and ask the learner to confirm the source is correct before showing an apply option.
- Apply fails midway: report applied and pending items; the snapshot holds the previous state.
