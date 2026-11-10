# Diff and apply rules

## Matching

1. **Activities**: by Google Skills URL (`urls.googleSkills`), else exact title, else the same position with a similar title.
2. **Modules** inside a matched activity: exact title; else same order with similar title (shared key words, small edits, renumbering) → rename; else unmatched.
3. **Concepts** inside a matched module: same rules as modules.
4. Unmatched tracker items → **removed**. Unmatched source items → **added**. Ask the learner when a pair is uncertain (for example a module split in two).

## Change types and effect

| Change | Apply | Progress |
|---|---|---|
| added activity, module or concept | `set` new document, `level: 0`, `completed: false`, `archived: false` | none yet |
| renamed or moved | `update` `title`, `order` | kept (id unchanged) |
| removed | `update` `archived: true` | kept in the database, hidden from quizzes, readiness and the page |
| restored (archived item back on the path) | `update` `archived: false` | resumes |
| hours or optional changed | `update` `hours`, `optional` | plan changes |
| section mapping changed | `update` `sections`, `weight`, `examRelevant` | readiness changes |
| exam-guide sections or weights changed | `update meta/settings.examGuide` | readiness changes |
| exam-guide objective added | propose mapping existing modules or a new gap topic | — |

Never delete documents during sync. Never reset levels during sync.

## Snapshot

Before applying, copy every document that the plan will update or archive to `snapshots/<snapshotId>/<collection>/<id>` (same body), plus `snapshots/<snapshotId>` with `{ts, reason: "sync", pluginVersion, counts: {activities, modules, concepts}}`. Added documents need no snapshot. To roll back, copy the snapshot bodies back with `set` (only on the learner's request).

## Example diff (shortened)

| Activity | Change | Item | Effect |
|---|---|---|---|
| Google Cloud Fundamentals: Core Infrastructure | added | module 7 "Generative AI in Google Cloud" | new, level 0, not completed; proposed sections: none (not on the exam) |
| Google Cloud Fundamentals: Core Infrastructure | removed | module "Prompt Engineering" | archived, data kept |
| Essential Google Cloud Infrastructure: Core Services | renamed | "Resource Management" → "Resource and Billing Management" | progress kept |
| Exam guide | unchanged | 5 sections, weights 20/17.5/25/20/17.5 | — |
