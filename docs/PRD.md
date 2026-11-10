# Product Requirements: GCP Certification Coach

> Status: approved for v1 build
> Owner: repository maintainer
> Related: [ARCHITECTURE.md](ARCHITECTURE.md), [ADRs](adr/)

## 1. Summary

GCP Certification Coach is a Claude plugin that turns Claude into a structured study coach for Google Cloud certifications. It builds a skill tree from the official Google Skills learning path for a chosen certification, tracks what the learner has completed, explains topics and labs grounded in public Google Cloud documentation, runs exam-style quizzes only on completed material, and measures readiness with a mastery model that rewards honest, consistent knowledge rather than volume or lucky guesses.

Progress lives in a private, live tracker page (a Claude artifact with a database) that every command reads and updates.

The first certification pack is **Associate Cloud Engineer (ACE)**. Other Google Cloud certifications are supported through an auto-generated pack marked `beta`.

## 2. Problem

Learners preparing for a Google Cloud certification typically:

- Watch course videos and complete guided labs, but rarely test recall, so knowledge fades before the exam.
- Cannot tell which parts of the official exam guide the course does not cover.
- Overestimate readiness because lucky guesses and repeated easy questions look like progress.
- Lose track of what they studied and what needs review, especially after breaks.
- Get generic AI answers that are not grounded in current documentation.

## 3. Target users

| Persona | Description | Primary need |
|---|---|---|
| Course follower | Takes the official path on Coursera or Google Skills | Quizzes on what they just finished; know when they are ready |
| Exam-focused engineer | Already works with cloud, wants the certificate | Find and close gaps against the exam guide; realistic mock exams |
| Returning learner | Studies in bursts with long breaks | Resume without losing track; review what faded |

Users are assumed to be English-capable technical learners. Explanations can be given in another language chosen at setup.

## 4. Goals

1. **Learn more of what matters.** Coverage is driven by the official learning path and, optionally, by the official exam guide.
2. **Learn correctly.** Every factual claim and every question is grounded in public Google Cloud documentation with a link.
3. **Measure real readiness.** Mastery reflects recent, confident, correct answers across multiple days, not total answer count.
4. **Low friction.** One command to start, natural language for everything else, progress saved automatically.
5. **Reusable and shareable.** Public repository, installable by anyone, with no personal data inside.

## 5. Non-goals

The plugin must **not**:

- Reproduce course materials (videos, transcripts, slides, lab instructions) from Coursera or Google Skills.
- Reproduce official sample exam questions or exam guide text verbatim (structure and links only).
- Claim to be affiliated with, endorsed by, or a product of Google or Anthropic.
- Guarantee passing an exam or predict an exam score.
- Act on the learner's Google Cloud project (no `gcloud` execution on their behalf). Challenges are performed by the learner.
- Store personal information beyond learning progress.
- Support multiple certifications inside one tracker (one tracker per certification).
- Use subagents in v1 (they do not run in claude.ai chat).

## 6. Scope by version

### v1 (this build)

- Plugin with skills: `init`, `learn`, `quiz`, `challenge`, `mock`, `progress`, `sync`, `rebuild`, `reset`.
- Tracker artifact template with live database.
- Curated ACE pack: learning path tree, exam-guide gap block, cheat sheets.
- Auto-generated `beta` pack flow for any other Google Cloud certification.
- Modes: **Course** (learning path only) and **Full exam** (path plus exam-guide gaps).
- Difficulty: **Standard** and **Hard** thresholds.
- Mastery model with confidence ratings, misconception log, calibration, decay, daily gain cap.
- Pause with automatic resume and a warm-up after long breaks.
- Study plan and estimated finish date when no exam date is given.
- Feedback capture into the tracker for the maintenance loop.
- English source, runtime explanation language chosen at `init`.
- README with Mermaid diagrams, LICENSE (MIT code, CC BY 4.0 content), CHANGELOG, CONTRIBUTING.
- Evals, `claude plugin validate`, privacy check in CI.

### v2 (planned)

- Question-verification agent (Cowork and Claude Code) that checks answer keys against documentation.
- Optional Google Developer Knowledge MCP connector for documentation retrieval.
- Additional curated packs (for example Professional Cloud Architect, Professional Data Engineer).

### v3 (planned)

- Adapters for other agents and chat products (`AGENTS.md`, `GEMINI.md`, generic chat instructions) with a file-based progress fallback.
- Submission to Anthropic's plugin directory.

## 7. User stories (v1)

### Setup

- **US-1** As a learner, I run `init`, choose a certification from the current Google Cloud list, and get a tracker with the official learning path as a skill tree.
- **US-2** During `init` I choose: Course or Full exam mode, Standard or Hard difficulty, explanation language, and weekly study hours (default 7).
- **US-3** During `init` I mark what I already completed, either by typing it ("courses 1, 3, 4; course 6 modules 1-3") or by letting Claude read my progress page on Coursera or Google Skills in the built-in browser.
- **US-4** `init` gives me one line to paste into my Claude Project instructions so every chat in that Project uses this tracker.

### Learning

- **US-5** I ask to explain a service or topic and get a practical explanation with alternatives, best practices, exam relevance and documentation links.
- **US-6** I paste a lab and get a step-by-step breakdown: what each step does, why, other ways to do it, and production practice.

### Practice

- **US-7** I ask for a quiz and receive exam-style questions only from modules I completed, prioritizing untested concepts, open misconceptions and concepts due for review, never repeating a question I already answered.
- **US-8** With each answer I give a confidence rating (guess, think, sure). Lucky guesses do not raise mastery; confident mistakes are logged as misconceptions.
- **US-9** After each answer I see whether I was right, why, and why each other option is wrong, with a documentation link.
- **US-10** Before starting a new module I can take a 5-question pre-test about it that does not affect my levels.
- **US-11** I can take an optional hands-on challenge without step-by-step instructions, submit a step narrative plus outputs of verification commands, and earn a bonus to related concepts.
- **US-12** I can take a 50-question mock exam and get a per-section breakdown and a red, amber or green recommendation about booking the exam.

### Progress

- **US-13** I tell Claude "finished module 4 of course 6" (or ask it to check the website) and the tracker updates.
- **US-14** I can pause my plan; any learning command resumes it; after a break longer than 7 days the next session starts with a warm-up.
- **US-15** The tracker shows readiness, per-section mastery, coverage, review queue, misconceptions, calibration, mock history, plan and estimated finish date.
- **US-16** I can switch mode or difficulty at any time.

### Maintenance

- **US-17** `sync` re-reads the learning path and exam guide, shows a diff, and applies it only after I confirm, without losing progress.
- **US-18** `rebuild` updates the tracker page to the latest plugin version without touching data.
- **US-19** `reset` archives my progress, asks for explicit confirmation, then resets levels while keeping the tree.
- **US-20** I can say "this question is wrong" or "I'd like X to work differently", and Claude records it as feedback for the maintainer.

## 8. Functional requirements

| ID | Requirement |
|---|---|
| FR-1 | Quizzes include only modules marked completed, except explicit user requests (with a warning) and pre-tests. |
| FR-2 | Every question is tagged with a concept (submodule) and stored in full in the log; the same question is never asked twice. |
| FR-3 | Each answer is written to the tracker immediately in a single database batch (concept update, log entry, misconception if any). Mock exams are written in one batch at the end. |
| FR-4 | Mastery, thresholds, decay, review intervals and bonuses use the constants defined in ARCHITECTURE §6, stored in the tracker settings at `init`. |
| FR-5 | Every factual explanation and every question cites at least one public Google Cloud documentation URL. |
| FR-6 | The explanation language follows the `init` choice; Google Cloud terms, product names and commands stay in English. |
| FR-7 | Destructive operations (`reset`, applying `sync`) follow plan → show → confirm → execute, and archive data before removing it. |
| FR-8 | Commands locate the tracker from the Project instructions line, or from the user's artifact list, or ask; they never create a second tracker silently. |
| FR-9 | Browser-based progress checks degrade gracefully: no browser → ask to open the chat in the Claude desktop app or enter progress manually; not signed in → ask to sign in, then retry; unexpected page → show what was read and ask. Results are always confirmed before writing. |
| FR-10 | The tracker shows "course readiness" in Course mode and "exam readiness" in Full exam mode. |
| FR-11 | Without an exam date, the plan estimates a finish date from remaining hours and weekly pace. |
| FR-12 | Feedback items are stored in the tracker's `feedback` collection with no personal data. |

## 9. Success metrics

Measured with `claude plugin eval` and manual testing before each release:

- Each skill passes at least 3 eval cases and beats the no-plugin baseline.
- Quizzes never include uncompleted modules in eval scenarios.
- Zero repeated questions across a 30-question eval session.
- Every quiz answer in evals includes a documentation link.
- `claude plugin validate` passes; privacy check finds nothing.
- Manual end-to-end test in claude.ai: `init` → mark progress → quiz → tracker updates.

## 10. Constraints

- **Copyright:** only course and module titles (public outline metadata), original questions, and links to public documentation.
- **Trademarks:** "Google Cloud" and certification names are used descriptively. README and plugin description include a non-affiliation disclaimer.
- **Privacy:** the repository contains no personal data, artifact URLs, emails or account identifiers. CI blocks commits that contain them.
- **Platform:** v1 targets claude.ai chat, the Claude desktop app and Cowork (the surfaces where the tracker artifact works). Claude Code is used for maintenance only.
- **Skill format:** must follow Anthropic's skill authoring best practices (see CLAUDE.md).

## 11. Risks

| Risk | Mitigation |
|---|---|
| Generated question has a wrong answer key | Documentation link required; user can flag "wrong question" → feedback; v2 verification agent |
| Google changes the learning path or exam guide | `sync` with diff and confirmation; tracker warns when not synced for 30 days |
| Google Skills pages render only with JavaScript | Browser-based discovery in the desktop app; curated pack snapshot as fallback; manual entry |
| Inflated readiness | Confidence-weighted gains, multi-day requirement, coverage requirement, decay |
| Tracker database unavailable | Commands explain the problem and continue the learning activity without saving, telling the user what was not saved |
| Users confuse course readiness with exam readiness | Explicit labels; Full exam mode recommended before booking |
