# Seeding the tracker database

## Contents

1. Build the batches
2. Document shapes (schema version 1)
3. Translating the page strings
4. Writing and verifying

## 1. Build the batches

Every write is one entry of the artifact data tool's batch action: `{op, collection, doc_id, data}`, at most 50 per call.

### Path A: curated pack (Associate Cloud Engineer)

The pack ships the complete seed as ready JSON in `assets/packs/ace/seed/` (`${CLAUDE_SKILL_DIR}/assets/packs/ace/seed/`):

- `batch-01.json` … `batch-08.json`: 384 `set` writes in order (`meta/settings` first, then 13 activities, 86 modules, 284 concepts), at most 50 each, with pack defaults and nothing completed. Pass each file's list as `writes` unchanged.
- `summary.json`: counts, the page title, the two hand-off lines, and `planInputs` for the plan estimate.
- `ui-strings-en.json`: the English page strings (to translate, section 3).

Sequence:

1. Write `batch-01` … `batch-08` in order, one tool call per batch, exactly as stored. Do not edit them.
2. Learner writes, small batches. All target existing documents, so read each one first to get its `version` (one `list` page of `modules` returns versions for many) and pin every entry with `if_version`:
   - `update meta/settings` with `mode` (`course` or `full`), `difficulty`, `language`, `ui` (section 3; omit for English), `paceHoursPerWeek`, `startDate`, `examDate` (omit when none), and `lastSyncAt`, `createdAt`, `updatedAt` = now (UTC).
   - `update modules/<id>` with `completed: true`, `completedAt: <startDate>` for each module the learner confirmed in step 6, including every module of a completed activity.
3. Verify (section 4).

The plan numbers for the init summary come from `summary.json` `planInputs` and [plan-estimate.md](plan-estimate.md) (at setup, nothing is logged, so the buffer is the full fraction of required hours): required = `requiredCourseHours` (+ `gapTopics` × `gapHoursPerTopic` in Full mode); remaining = the sum of `moduleHours` of uncompleted modules (+ the gap hours in Full mode) + `practiceBufferFraction` × required.

### Path B: generated pack (beta)

Build the same entries by hand from the pack JSON of [generated-pack.md](generated-pack.md), in this order, with the learner's choices applied directly:

1. `meta/settings` from the pack (`certId`, `certName`, `certShortName`, `packSource: "generated"`, `packVersion`, `examGuide {version, url, sections}`, `path {url, title, providers}`), the learner's choices (`mode`, `difficulty`, `language`, `paceHoursPerWeek`, `startDate`, `examDate` or null), `ui: {}` (filled in section 3), `scoring` = the whole `scoring` object, `schemaVersion: 1`, `pluginVersion`, `templateVersion` and `latestPluginVersion` (all three the `PLUGIN_VERSION` constant in the tracker template's script), `paused: null`, `pausedDaysTotal: 0`, `pauseHistory: []`, and `lastSyncAt`, `createdAt`, `updatedAt` = now (UTC).
2. For each activity, in order: `activities/<id>`, then each of its `modules/<id>`, each followed by its `concepts/<id>`. Ids come from the pack; never invent or renumber them. Missing `optional` is false, missing `weight` is `core`, missing `examRelevant` is true, missing `labs`/`docUrls`/`sections` are empty lists. A module is `completed: true` with `completedAt: <startDate>` when the learner confirmed it or its whole activity in step 6; otherwise `completed: false`, `completedAt: null`.
3. The gaps activity: `activities/<gaps id, default gaps>` with `order` = number of path activities + 1, `kind: gaps`, `title` (default "Exam guide gaps"), `hours` = `hoursPerTopic` (default 1) × number of topics, `optional: false`, `urls: {}`. Each topic becomes `modules/<topic id>` with `activityId` = the gaps id, `examRelevant: true`, `hours` = `hoursPerTopic`, `labs: []`, `completed: false`, `completedAt: null`, followed by its concepts.
4. Every concept: `level: 0`, `answers: 0`, `correct: 0`, `recent: []`, `days: []`, `lastReviewed: null`, `bonus: 0`, `archived: false`. Every activity and module: `archived: false`.

Cut the list into batches of at most 50 entries in that order (settings first), all `set`. Count activities, modules and concepts as you go; these counts are the expected totals in the verify step. Compute the plan estimate with [plan-estimate.md](plan-estimate.md) before the learner confirms the summary. For the page strings in section 3, use the `EN` map at the top of the tracker template's script.

## 2. Document shapes (schema version 1)

Only seed what is listed. Timestamps are ISO 8601 UTC; dates are the learner's local `YYYY-MM-DD`.

- `meta/settings`: `schemaVersion: 1`, `pluginVersion`, `templateVersion`, `latestPluginVersion`, `certId`, `certName`, `certShortName`, `packSource` (`curated` or `generated`), `packVersion`, `examGuide {version, url, sections[{id, name, weight}]}`, `path {url, title, providers}`, `mode`, `difficulty`, `language`, `ui` (object), `paceHoursPerWeek`, `startDate`, `examDate` (or null), `paused: null`, `pausedDaysTotal: 0`, `pauseHistory: []`, `lastSyncAt`, `scoring` (the whole scoring.yaml content, rationale included), `createdAt`, `updatedAt`.
- `activities/<id>`: `order`, `kind` (`course`, `skill_badge`, `gaps`), `title`, `hours`, `optional`, `urls {googleSkills, coursera}`, `archived: false`.
- `modules/<id>`: `activityId`, `order`, `title`, `sections` (objective ids), `weight` (`core` or `support`), `examRelevant`, `hours`, `labs` (titles, informational), `completed`, `completedAt`, `archived: false`.
- `concepts/<id>`: `moduleId`, `order`, `title`, `docUrls`, `level: 0`, `answers: 0`, `correct: 0`, `recent: []`, `days: []`, `lastReviewed: null`, `bonus: 0`, `archived: false`.

Gap topics are modules of the `gaps` activity. They are seeded in both modes; the page and the skills show them only in Full exam mode, so switching mode later needs no reseeding.

Collections created later by other skills: `log`, `misconceptions`, `mocks`, `challenges`, `feedback`, `snapshots`.

## 3. Translating the page strings

When `language` is not `en`, translate the values of `ui-strings-en.json` (or the `EN` map at the top of the tracker template's script) into the learner's language and put the result in `settings.ui` (path A: in the `meta/settings` update). Rules:

- Keep the keys unchanged and every `{placeholder}` exactly as it is.
- Keep product names, `/gcp-cert-coach:init`, and the words "Google Cloud", "GCP" in English.
- Short labels stay short; the page is used at phone width.
- Leave `ui` empty for English.

## 4. Writing and verifying

1. Write the batches in order, one artifact data tool call per batch, to the tracker you just published.
2. After the last write, read `meta/settings` and list one page of `activities`, `modules` and `concepts`. Compare with the expected counts: path A 13 activities, 86 modules, 284 concepts (`summary.json` `counts`); path B your own counts. A page may hold fewer documents than the collection; check that the documents you see exist, that `meta/settings.certId`, `mode` and `language` are right, and that the confirmed modules are `completed`.
3. If a batch failed, retry that batch once. Seed batches are `set` on fixed ids, so repeating one is safe; for a failed learner write, read the document again and pin the new version.
4. Tell the learner the tracker is filled and that the page updates live.
