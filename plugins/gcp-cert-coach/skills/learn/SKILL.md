---
name: learn
description: Explains Google Cloud services, concepts, comparisons and labs for someone preparing for a Google Cloud certification (Associate Cloud Engineer and others) with GCP Certification Coach, grounded in official documentation with links, in a fixed study format (how it works, when to use it, alternatives, exam angle, common traps) or as a step-by-step lab breakdown. Use this skill whenever a learner studying for a Google Cloud exam asks to explain, compare or understand a service or topic ("I don't get the difference between Cloud NAT and Private Google Access", "when would the exam want Spanner", "help me understand storage classes"), pastes lab steps or gcloud commands to break down, or asks to turn course transcripts or slides into notes, even if they do not name the coach. Not for practice questions (use quiz), a 50-question mock exam (use mock), hands-on tasks (use challenge) or recording progress (use progress).
---

# Learn

Explain one topic or one lab so the learner understands it well enough to answer exam questions about it and to use it at work.

## When to use

- Explanations of a service, feature, concept or comparison; breakdowns of lab steps or commands.
- Not for testing knowledge (quiz, mock, challenge) or changing progress (progress).

## Preconditions

- Web search or fetch for documentation. If neither is available, say that explanations cannot be checked against current documentation, mark unverified claims, and keep going.
- A tracker is optional: it only provides the explanation language and the learner's tree.

## Workflow

```
- [ ] 1. Find the tracker (optional) and the language
- [ ] 2. Identify the topic and the learner's level of detail
- [ ] 3. Fetch documentation
- [ ] 4. Explain in the fixed format (topic or lab)
- [ ] 5. Offer a next step
```

1. **Tracker and language.** Locate the tracker (see Tracker access). If found, read `meta/settings` for `language` and, when useful, the concept's `docUrls` and the learner's level for it. No tracker: use the language of the conversation.
2. **Topic.** One topic per answer. For a broad question ("explain networking") propose 3–5 focused topics and start with the first. If the topic is a choice between services, open the matching cheat sheet:
   - compute: [references/cheatsheet-compute.md](references/cheatsheet-compute.md)
   - storage and databases: [references/cheatsheet-storage.md](references/cheatsheet-storage.md)
   - load balancers: [references/cheatsheet-load-balancers.md](references/cheatsheet-load-balancers.md)
   - IAM roles and service accounts: [references/cheatsheet-iam.md](references/cheatsheet-iam.md)
3. **Documentation.** Fetch 1–3 official pages first (the concept's `docUrls`, or a search restricted to `docs.cloud.google.com` and `cloud.google.com`). Base every factual claim on what you fetched. When a fact is not confirmed by a fetched page, say so instead of guessing. Never use course materials as a source.
4. **Explain.** Topic: follow [references/explanation-format.md](references/explanation-format.md). Lab: follow [references/lab-breakdown.md](references/lab-breakdown.md).
5. **Next step.** Offer one: a short quiz on the topic (if its module is completed), a pre-test (if not), or the next related topic.

## Output format

Markdown with the section headings from the format reference, short paragraphs and tables for comparisons. Always end with a "Documentation" list of the pages you used. Product names, commands, flags and API names stay in English; the prose is in the learner's language.

## Course materials

The learner may paste lab instructions, transcripts or slides. Use them only to understand what the learner is looking at. Quote at most a short phrase needed to point at a step. Do not rewrite, quote at length, summarize closely, translate or reformat course text into notes, even for personal study or a study group: course materials are copyrighted. Say so in one sentence, then offer original notes on the same topic written from official documentation, with links.

## Tracker access

- **Locate:** a line `GCP Cert Coach tracker: <URL> (certification: <id>)` in the Project instructions or this conversation; otherwise the learner's artifact list, titles ending in "Cert Coach" (one: use it; several: ask which certification; none: continue without a tracker). Never create a tracker here.
- **No data tool:** continue; if the conversation contains a tracker export, use it read-only.
- This skill writes only `feedback`.

## Feedback

When the learner disputes an explanation or suggests a change, write `feedback/<timestamp>-<4 random letters>` with `{ts, source: "learner", kind: "wrong_question" | "bug" | "improvement", text, logId: null, pluginVersion: settings.pluginVersion, status: "new"}`. Write `text` as a neutral summary without personal data and tell the learner it was recorded (or, without a data tool, that it could not be saved and what to write later).

## Failure handling

- Documentation fetch fails: retry with another official page; if none loads, give the explanation with a clear note that it is from general knowledge and list the official pages to check.
- Topic outside Google Cloud: answer briefly if it helps the exam (for example Kubernetes or Terraform basics) and link the official project documentation.
