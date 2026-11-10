# ADR 0010: Cite curated documentation links first and fetch on demand

- Status: Accepted
- Date: 2026-11-10
- Amends: [ADR 0005](0005-documentation-grounding.md)

## Context

The manual test on claude.ai showed that fetching documentation for every quiz question was slow and expensive: init, one explanation and the start of one quiz used about 30% of a 5-hour Pro window. One session also could not reach `docs.cloud.google.com` and fell back to unverified links. Two skills also stated different numbers for the same fact (Dedicated Interconnect capacities).

## Decision

- Every concept in the curated pack carries `docUrls`. Quizzes, mocks and challenges cite them by default and fetch a page only when the concept has no `docUrl`, the fact is version-sensitive and not in `references/facts.md`, or the learner disputes it. At most one fetch per question, with a narrow request. If a fetch fails, say so and use the curated link.
- `learn` fetches at most two pages by default and offers "more detail".
- Numeric facts (capacities, SLAs, minimum durations, limits) live once in `references/facts.md`, each with its official page, checked at release time. A number in neither `facts.md` nor a page fetched in the session is not the tested point of a question.
- ADR 0005 still holds: every claim and question carries a documentation URL, and Claude says so when a fact is not confirmed.

## Consequences

- Faster, cheaper sessions; fewer failures when the documentation site is unreachable.
- Curated links can go stale between releases; `scripts/check-links.py` and release-time checks cover them, and a disputed fact triggers a fetch.
- `facts.md` is a maintenance item: verify it at each release.
