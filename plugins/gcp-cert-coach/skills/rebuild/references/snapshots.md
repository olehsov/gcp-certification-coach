# Snapshots and restore

Used by reset, sync and rebuild. A snapshot holds full copies of documents, so it can be restored in a new chat without any conversation context.

## Contents

1. Format
2. Taking a snapshot
3. Restoring

## 1. Format

- `snapshots/<snapId>` (metadata): `{ts, reason, pluginVersion, certId, trackerTitle, status, collections, scope}`.
  - `reason`: `reset`, `sync`, `migration` or `restore`. Ids: `<reason>-<YYYYMMDD-HHMM>`.
  - `status`: `writing` until verified, then `complete`.
  - `collections`: `{"<name>": {"rows": <n>, "chunks": <n>}}` for every collection copied.
  - `scope`: one line describing what the snapshot protects.
- `snapshots/<snapId>/chunks/<collection>-<NNN>` (NNN from 001): `{collection, chunk, rows: [{id, data}]}`. `data` is the full document exactly as read (all fields). Chunk size: at most 100 rows, at most 25 for `log` (long question texts), so one write stays small.
- Never store counts only. A snapshot without chunks is not a snapshot.

## 2. Taking a snapshot

```
- [ ] 1. Read every document that will change or be removed (all fields)
- [ ] 2. Write the metadata with status "writing"
- [ ] 3. Write the chunks in batches of at most 50 writes
- [ ] 4. Read the chunks back and compare row counts per collection
- [ ] 5. Set status "complete"
```

- If the data tool can save reads to files and write documents from files, use that so rows do not pass through the conversation.
- Step 4: the sum of `rows` over a collection's chunks must equal `collections.<name>.rows` and the number read in step 1. Any mismatch: rewrite the failed chunk once; if it still fails, stop. **No destructive step before `status: "complete"`.**
- Collections to copy: reset: `concepts`, `log`, `misconceptions`, plus `modules`, `mocks`, `challenges` when in scope. sync: every document it will update or archive. rebuild migration: every document the migration changes or removes.

## 3. Restoring

Triggered by "restore my progress from the last snapshot" or similar, only from a new instruction by the learner.

```
- [ ] 1. List snapshots with status complete, newest first
- [ ] 2. Show the chosen snapshot and what restoring changes
- [ ] 3. Take a restore snapshot of the current state
- [ ] 4. Ask for the confirmation phrase
- [ ] 5. Write the rows back in batches
- [ ] 6. Read back and compare counts
```

1. Show for each: id, reason, date, tracker title, row counts. Default: the newest `complete` one. Skip `writing` ones.
2. Tell the learner: documents in the snapshot are overwritten with their saved content; documents created after the snapshot (for example newer log entries) are kept unless they share an id; the tree and settings are untouched unless they are in the snapshot.
3. Take a snapshot `restore-<YYYYMMDD-HHMM>` of the documents about to be overwritten (section 2), so the restore can be undone.
4. Ask for the exact phrase `restore <certShortName> progress`.
5. **Rows come only from the snapshot chunks, never from earlier messages or memory.** `set` each row at `<collection>/<id>` with its saved `data`, in batches of at most 50. If a chunk is missing or the row counts do not match the metadata, say the snapshot is not restorable, write nothing, and stop.
6. Read back the restored collections; report counts restored per collection.
