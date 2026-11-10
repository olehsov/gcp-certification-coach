# Seeding the tracker database

## Contents

1. Build the batches
2. Document shapes (schema version 1)
3. Translating the page strings
4. Writing and verifying

## 1. Build the batches

Two paths produce the same documents. Pick one, and tell the learner which one was used in the seed message ("Seeded with the seed script" or "Seeded without the script: code execution is not available here").

### Path A: seed script (when code execution is available)

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/build_seed.py --pack ${CLAUDE_SKILL_DIR}/assets/packs/ace \
  --out /tmp/gcc-seed --mode full --difficulty standard --language uk --pace 7 \
  --start-date 2026-01-15 --completed "c2,c3,c4-m1,c4-m2"
```

On claude.ai chat the placeholder is not substituted: run it from the skill folder as `python3 scripts/build_seed.py --pack assets/packs/ace ...`. Add `--exam-date YYYY-MM-DD` when given. For a generated pack, pass `--pack <file>.json` (see generated-pack.md). If PyYAML is missing, run `pip install pyyaml` and retry. Use the learner's local date for `--start-date`.

The script prints a summary (batch count, document counts, completed modules, title) and writes `batch-01.json` … to the output folder. Each batch is a list of `{"op": "set", "path": "<collection>/<id>", "data": {...}}`. It also writes `ui-strings-en.json`.

Switch to path B when code execution is off (claude.ai with code execution disabled, or no code tool at all), when the script cannot start, or when PyYAML cannot be installed. Do not ask the learner to turn on code execution; path B needs nothing from them.

### Path B: by hand from the pack files

Read `pack.yaml`, `path.yaml`, `gaps.yaml` and `scoring.yaml` (for a generated pack, the JSON from generated-pack.md) and build the same `set` operations the script builds, in this order:

1. `meta/settings` from `pack.yaml` (`certId`, `certName`, `certShortName`, `packSource` default `curated`, `packVersion`, `examGuide {version, url, sections}`, `path {url, title, providers}`), the learner's choices (`mode`, `difficulty`, `language`, `paceHoursPerWeek`, `startDate`, `examDate` or null), `ui: {}` (filled in section 3), `scoring` = the whole parsed `scoring.yaml`, `schemaVersion: 1`, `pluginVersion` (the `PLUGIN_VERSION` constant in the tracker template's script), `paused: null`, `pausedDaysTotal: 0`, `pauseHistory: []`, and `lastSyncAt`, `createdAt`, `updatedAt` = now (UTC).
2. For each activity in `path.yaml`, in order: `activities/<id>`, then each of its `modules/<id>`, each followed by its `concepts/<id>`. Ids come from the pack; never invent or renumber them. Missing `optional` is false, missing `weight` is `core`, missing `examRelevant` is true, missing `labs`/`docUrls`/`sections` are empty lists. A module is `completed: true` with `completedAt: <startDate>` when the learner confirmed it or its whole activity in step 6; otherwise `completed: false`, `completedAt: null`.
3. The gaps activity from `gaps.yaml`: `activities/<gaps id, default gaps>` with `order` = number of path activities + 1, `kind: gaps`, `title` (default "Exam guide gaps"), `hours` = `hoursPerTopic` (default 1) × number of topics, `optional: false`, `urls: {}`. Each topic becomes `modules/<topic id>` with `activityId` = the gaps id, `examRelevant: true`, `hours` = `hoursPerTopic`, `labs: []`, `completed: false`, `completedAt: null`, followed by its concepts.
4. Every concept: `level: 0`, `answers: 0`, `correct: 0`, `recent: []`, `days: []`, `lastReviewed: null`, `bonus: 0`, `archived: false`. Every activity and module: `archived: false`.

Cut the list into batches of at most 50 operations in that order (settings first). Count activities, modules and concepts as you go; these counts replace the script's summary in the verify step. For the page strings in section 3, use the `EN` map at the top of the tracker template's script.

## 2. Document shapes (schema version 1)

Only seed what is listed. Timestamps are ISO 8601 UTC; dates are the learner's local `YYYY-MM-DD`.

- `meta/settings`: `schemaVersion: 1`, `pluginVersion`, `certId`, `certName`, `certShortName`, `packSource` (`curated` or `generated`), `packVersion`, `examGuide {version, url, sections[{id, name, weight}]}`, `path {url, title, providers}`, `mode`, `difficulty`, `language`, `ui` (object), `paceHoursPerWeek`, `startDate`, `examDate` (or null), `paused: null`, `pausedDaysTotal: 0`, `pauseHistory: []`, `lastSyncAt`, `scoring` (the whole scoring.yaml content, rationale included), `createdAt`, `updatedAt`.
- `activities/<id>`: `order`, `kind` (`course`, `skill_badge`, `gaps`), `title`, `hours`, `optional`, `urls {googleSkills, coursera}`, `archived: false`.
- `modules/<id>`: `activityId`, `order`, `title`, `sections` (objective ids), `weight` (`core` or `support`), `examRelevant`, `hours`, `labs` (titles, informational), `completed`, `completedAt`, `archived: false`.
- `concepts/<id>`: `moduleId`, `order`, `title`, `docUrls`, `level: 0`, `answers: 0`, `correct: 0`, `recent: []`, `days: []`, `lastReviewed: null`, `bonus: 0`, `archived: false`.

Gap topics are modules of the `gaps` activity. They are seeded in both modes; the page and the skills show them only in Full exam mode, so switching mode later needs no reseeding.

Collections created later by other skills: `log`, `misconceptions`, `mocks`, `challenges`, `feedback`, `snapshots`.

## 3. Translating the page strings

When `language` is not `en`, translate the values of `ui-strings-en.json` (or the `EN` map at the top of the tracker template's script) into the learner's language and put the result in `settings.ui` before writing batch 1. Rules:

- Keep the keys unchanged and every `{placeholder}` exactly as it is.
- Keep product names, `/gcp-cert-coach:init`, and the words "Google Cloud", "GCP" in English.
- Short labels stay short; the page is used at phone width.
- Leave `ui` empty for English.

## 4. Writing and verifying

1. Write the batches in order, one artifact data tool call per batch, as batch writes to the tracker you just published.
2. After the last batch, read `meta/settings` and list one page of `activities`, `modules` and `concepts`. Compare with the summary counts (a page may hold fewer documents than the collection; check that the documents you see exist and that `meta/settings.certId` is right).
3. If a batch failed, retry that batch once. Writes are idempotent (`set` on fixed ids), so repeating a batch is safe.
4. Tell the learner the tracker is filled and that the page updates live.
