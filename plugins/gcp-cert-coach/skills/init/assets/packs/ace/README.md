# ACE pack

Curated certification pack for **Associate Cloud Engineer**, read by the `init` skill and copied into the learner's tracker database. Pack version and verification date are in [pack.yaml](pack.yaml).

## Files

| File | Content |
|---|---|
| [pack.yaml](pack.yaml) | Certification names, exam-guide URL, sections with official weights, objective titles, learning-path URLs |
| [path.yaml](path.yaml) | 12 activities (9 courses, 3 skill badges) → 70 modules → 243 concepts, with order, hours, optional flags, exam-guide sections, weight, `examRelevant`, lab titles and documentation URLs for core concepts |
| [gaps.yaml](gaps.yaml) | 16 exam-guide gap topics (41 concepts) for Full exam mode, each concept with 1–3 documentation URLs |
| [scoring.yaml](scoring.yaml) | Every scoring constant from the mastery model with a rationale per constant |

## How it was built

1. **Learning path.** Activities, module titles and item titles come from the public outline of the Google Skills path "Associate Cloud Engineer Certification" (https://www.skills.google/paths/11), read in a browser on the verification date. Durations are the provider's stated hours. None of the activities is marked optional on the path, so none is optional here.
2. **Concepts.** For courses, concepts are the lecture items of each module; quizzes, lab intros and reviews, module overviews and demos that duplicate a lecture were dropped, and some titles were shortened. For skill badges, each lab is a module, and its concepts are **original summaries** of the skills the lab practices. Lab titles are listed per module as `labs`.
3. **Exam-guide mapping.** Every exam-relevant module maps to objective ids of the official exam guide (https://cloud.google.com/learn/certification/guides/cloud-engineer) and is weighted `core` or `support` (support counts half in readiness). Introductions, summaries, resources and study-tool modules are `examRelevant: false`: tracked for completion, never quizzed.
4. **Gaps.** Each considerations line of the exam guide was compared with the module and lecture titles. Topics the path does not cover, or covers only in passing, became gap topics. Their concepts are written originally.
5. **Documentation links.** Every URL points to public Google documentation (`docs.cloud.google.com`, `cloud.google.com`, or the Google Workspace help center for Google Cloud Directory Sync) and returned HTTP 200 on the verification date. Canonical (post-redirect) URLs are used.

## Content rules

- Titles and structure only. No course descriptions, transcripts, slides, lab instructions, quiz questions or exam-guide text beyond section and objective titles.
- Course, module and certification titles are names of third-party works, used as factual references. Google Cloud and related marks belong to Google LLC. This pack is not affiliated with or endorsed by Google.
- Pack content is licensed under CC BY 4.0 (see `LICENSE-CONTENT` in the repository).

## Updating

Run the `sync` skill in a tracker to compare a learner's tree with the live path and exam guide. To update this pack itself, re-read the same two pages, regenerate the YAML, re-check every URL, and bump `packVersion` and `lastVerified` in `pack.yaml`.
