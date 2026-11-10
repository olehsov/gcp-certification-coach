# Generated pack (beta)

For any Google Cloud certification without a curated pack. The result is labeled `beta` everywhere (`packSource: "generated"`).

## Steps

```
- [ ] 1. Certification page and exam guide
- [ ] 2. Learning path outline
- [ ] 3. Map modules to exam-guide objectives
- [ ] 4. Gap topics with documentation links
- [ ] 5. Show the tree and get confirmation
- [ ] 6. Write the pack JSON and seed it
```

1. **Exam guide.** From https://cloud.google.com/learn/certification find the certification page and its exam guide. Record the guide URL, section names and weights (percentages), and objective ids with their titles only. Never copy the guide's text beyond titles.
2. **Learning path.** Find the matching certification learning path on Google Skills (https://www.skills.google/paths). Its pages render with JavaScript:
   - With the built-in browser (Claude desktop app): open the path, list its activities (courses and skill badges) with stated hours, then open each activity and read module titles and item titles. Skill badges: each lab is a module; the challenge lab is the last module. Note anything the path marks as optional.
   - Without a browser: ask the learner to paste the outline (activity titles, module titles, item titles), or to open this chat in the Claude desktop app. Do not invent a tree from memory.
3. **Mapping.** For each module: `sections` (objective ids it teaches), `weight` (`core` for modules that teach an objective directly, `support` for overviews), `examRelevant: false` for introductions, summaries, resources and study-tool modules. Concepts are the module's lecture items (drop quizzes, lab intros and reviews, overviews); for skill-badge labs, write 2–4 short original concept titles.
4. **Gaps.** Compare every considerations line of the guide with the module and concept titles. Topics the path does not cover become gap topics (aim for 10–15), each with 1–3 concepts, written originally, and 1–3 official documentation URLs per concept that you fetched and saw load.
5. **Confirm.** Show the activities, module counts per activity, the section mapping for each module (one line each) and the gap topics. Say it is a beta pack built automatically and may contain mapping mistakes. Continue only after the learner confirms or corrects it.
6. **Write the pack** as one JSON file with the same structure as the curated pack files:

```json
{
  "meta": {"certId": "pcd", "certName": "...", "certShortName": "PCD", "packSource": "generated", "packVersion": "generated",
           "examGuide": {"url": "...", "version": "current as of <date>", "sections": [{"id": "1", "name": "...", "weight": 20}]},
           "path": {"url": "...", "title": "...", "providers": {"googleSkills": "..."}}},
  "path": {"activities": [{"id": "c1", "order": 1, "kind": "course", "title": "...", "hours": 5, "optional": false,
            "urls": {"googleSkills": "..."},
            "modules": [{"id": "c1-m1", "order": 1, "title": "...", "sections": ["1.1"], "weight": "core", "examRelevant": true,
                         "hours": null, "concepts": [{"id": "c1-m1-k1", "order": 1, "title": "...", "docUrls": []}]}]}]},
  "gaps": {"activity": {"id": "gaps", "title": "Exam guide gaps", "hoursPerTopic": 1},
           "topics": [{"id": "g01", "order": 1, "title": "...", "sections": ["2.1"], "weight": "core",
                       "concepts": [{"id": "g01-k1", "order": 1, "title": "...", "docUrls": ["https://docs.cloud.google.com/..."]}]}]},
  "scoring": "<copy the whole content of assets/packs/ace/scoring.yaml as an object>"
}
```

Ids: activities `c<N>` for courses and `b<N>` for skill badges in path order, modules `<activityId>-m<N>`, concepts `<moduleId>-k<N>`, gaps `g<NN>`. The scoring constants are the same for every certification: copy them from the ACE pack's scoring.yaml.

Then run `build_seed.py --pack <file>.json` (see seeding.md) or build the batches by hand.
