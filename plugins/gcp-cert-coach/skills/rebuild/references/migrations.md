# Schema migrations

Run in order from the tracker's version to the current one (1). Snapshot first. Never delete learner history without a snapshot.

## Detecting the version

- `meta/settings.schemaVersion` present → that number.
- No `meta/settings`, but `courses` and `topics` collections → **0** (prototype tracker).

## 0 → 1

Schema 0 had `courses/{id}` `{num, title, done}`, `topics/{id}` `{course, title, sections, weight, level, answers, correct, lastReviewed, subtopics[]}` and `log/{id}` `{ts, topic, q, correct, after}`.

1. **Choose the pack.** Ask which certification the tracker is for (schema 0 was used for ACE). Build the full v1 tree from that pack as init does (settings with the learner's current choices, activities, modules, concepts), but do not write it yet.
2. **Map courses → activities** by title. For each matched course with `done: true`, mark all modules of the activity completed (`completedAt`: today).
3. **Map topics → modules** by title within the matched activity. For each matched module, give every concept of that module the topic's `level` and `lastReviewed`; leave concept `answers`, `correct`, `recent`, `days` at 0 or empty (the old counts were per topic and cannot be split). Unmatched topics: list them to the learner; their levels are not carried over.
4. **Log**: for each old entry write a v1 `log` document: `ts`, `kind: "quiz"`, `moduleId` (mapped), `conceptId: null`, `format: "scenario"`, `difficulty: "medium"`, `confidence: 2`, `question: q`, `answerKey: ""`, `given: ""`, `correct`, `docUrl: ""`, `levelBefore: null`, `levelAfter: after`, `misconceptionId: null`, `mockId: null`. Keep the old id.
5. **Write** the new settings (`schemaVersion: 1`) and tree in batches of at most 50, then the migrated log.
6. **Archive the old collections**: after the snapshot holds `courses` and `topics`, delete those documents (they are no longer read by anything). Tell the learner where the snapshot is.
7. Tell the learner that concept-level history starts now, so coverage and module status will build up again with the next quizzes, while levels were carried over.

## Adding a future migration

Add a section `N → N+1` with: what changed in the schema, the exact field transformations, what is snapshotted, and what the learner is told. Bump `SCHEMA_VERSION` in the tracker template and in init's `build_seed.py`, and update ARCHITECTURE §5.2.
