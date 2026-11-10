#!/usr/bin/env python3
"""Generate the eval cases in evals/ from one shared tracker fixture.

Edit the fixture or the CASES list here, then run `python3 scripts/gen-evals.py`.
Generated case folders are committed; do not hand-edit them (regeneration overwrites them).
All learner data below is invented example data.
"""
import json
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parent.parent
EVALS = ROOT / "evals"
TODAY = "2026-11-10"

SCORING = {
    "alpha": {"easy": 0.15, "medium": 0.25, "hard": 0.35},
    "confidenceMultiplier": {"1": 0.0, "2": 0.6, "3": 1.0},
    "beta": {
        "1": {"easy": 0.10, "medium": 0.08, "hard": 0.05},
        "2": {"easy": 0.25, "medium": 0.20, "hard": 0.15},
        "3": {"easy": 0.40, "medium": 0.35, "hard": 0.30},
    },
    "profiles": {
        "standard": {
            "dailyGainCap": 25,
            "reviewIntervalDays": {"below60": 3, "below80": 7, "atLeast80": 14},
            "decayPerWeekOverdue": 3,
            "moduleReady": {"minLevel": 75, "minCoverage": 0.8, "minAnswers": 4, "minDistinctDays": 2,
                            "lastNCorrect": 2, "openMisconceptionsAllowed": True},
            "mock": {"greenMinPercent": 75, "greenConsecutive": 1, "amberMinPercent": 60},
        },
        "hard": {
            "dailyGainCap": 20,
            "reviewIntervalDays": {"below60": 2, "below80": 5, "atLeast80": 10},
            "decayPerWeekOverdue": 5,
            "moduleReady": {"minLevel": 85, "minCoverage": 1.0, "minAnswers": 6, "minDistinctDays": 3,
                            "lastNCorrect": 3, "openMisconceptionsAllowed": False},
            "mock": {"greenMinPercent": 80, "greenConsecutive": 2, "amberMinPercent": 65},
        },
    },
    "rounding": {"levelDecimals": 1, "minLevel": 0, "maxLevel": 100},
    "misconception": {"createOnSure": True, "createOnThinkWhenSpecificBelief": True,
                      "resolveAfterConsecutiveCorrect": 2, "minConfidenceToResolve": 2},
    "challengeBonus": {"base": 15, "perScore": 10, "minScore": 0.5, "resolveMisconceptionsAtScore": 1.0},
    "session": {"defaultQuestions": 5, "maxConsecutiveSameModule": 2, "pretestQuestions": 5,
                "warmupQuestions": 5, "warmupAfterPauseDays": 7, "mockQuestions": 50},
    "readiness": {"coreWeight": 1.0, "supportWeight": 0.5},
    "history": {"recentAnswersKept": 5, "distinctDaysKept": 10},
    "plan": {"gapHoursPerTopic": 1, "practiceBufferFraction": 0.2, "minutesPerLoggedAnswer": 3},
    "page": {"reviewQueueSize": 7, "recentAnswersShown": 15, "staleSyncDays": 30},
}

SECTIONS = [
    {"id": "1", "name": "Setting up a cloud solution environment", "weight": 20},
    {"id": "2", "name": "Planning and configuring a cloud solution", "weight": 17.5},
    {"id": "3", "name": "Deploying and implementing a cloud solution", "weight": 25},
    {"id": "4", "name": "Ensuring successful operation of a cloud solution", "weight": 20},
    {"id": "5", "name": "Configuring access and security", "weight": 17.5},
]


def settings(**over):
    s = {
        "schemaVersion": 1, "pluginVersion": "0.2.0", "templateVersion": "0.2.0", "latestPluginVersion": "0.2.0", "certId": "ace",
        "certName": "Associate Cloud Engineer", "certShortName": "ACE", "packSource": "curated",
        "examGuide": {"version": "example", "sections": SECTIONS},
        "mode": "course", "difficulty": "standard", "language": "en", "ui": {},
        "paceHoursPerWeek": 7, "startDate": "2026-10-01", "examDate": None, "paused": None,
        "pausedDaysTotal": 0, "pauseHistory": [], "lastSyncAt": "2026-10-20T09:00:00Z", "scoring": SCORING,
    }
    s.update(over)
    return s


ACTIVITIES = [
    {"id": "c2", "order": 2, "kind": "course", "title": "Google Cloud Fundamentals: Core Infrastructure", "hours": 8, "optional": False},
    {"id": "c4", "order": 4, "kind": "course", "title": "Essential Google Cloud Infrastructure: Core Services", "hours": 11, "optional": False},
]

MODULES = [
    {"id": "c2-m1", "activityId": "c2", "order": 1, "title": "Introducing Google Cloud", "sections": ["1.2"], "weight": "support", "examRelevant": True, "completed": True, "completedAt": "2026-10-02"},
    {"id": "c2-m2", "activityId": "c2", "order": 2, "title": "Resources and Access in the Cloud", "sections": ["1.1", "5.1", "5.2"], "weight": "core", "examRelevant": True, "completed": True, "completedAt": "2026-10-03"},
    {"id": "c2-m3", "activityId": "c2", "order": 3, "title": "Virtual Machines and Networks in the Cloud", "sections": ["2.1", "2.3", "3.1", "3.5"], "weight": "core", "examRelevant": True, "completed": False, "completedAt": None},
    {"id": "c4-m2", "activityId": "c4", "order": 2, "title": "Identity and Access Management (IAM)", "sections": ["1.1", "5.1", "5.2"], "weight": "core", "examRelevant": True, "completed": True, "completedAt": "2026-10-20"},
    {"id": "c4-m3", "activityId": "c4", "order": 3, "title": "Storage and Database Services", "sections": ["2.2", "3.4", "4.4"], "weight": "core", "examRelevant": True, "completed": False, "completedAt": None},
]


def concept(cid, module, order, title, level=0, answers=0, correct=0, last=None, recent=None, days=None):
    return {"id": cid, "moduleId": module, "order": order, "title": title, "level": level,
            "answers": answers, "correct": correct, "recent": recent or [], "days": days or [],
            "lastReviewed": last, "bonus": 0, "archived": False, "docUrls": []}


CONCEPTS = [
    concept("c2-m1-k7", "c2-m1", 7, "Pricing and billing", 40, 2, 1, "2026-11-01T10:00:00Z",
            [{"date": "2026-11-01", "correct": True, "confidence": 2}, {"date": "2026-11-01", "correct": False, "confidence": 2}], ["2026-11-01"]),
    concept("c2-m2-k1", "c2-m2", 1, "Resource hierarchy", 62, 3, 3, "2026-11-08T10:00:00Z",
            [{"date": "2026-11-08", "correct": True, "confidence": 3}], ["2026-11-05", "2026-11-08"]),
    concept("c2-m2-k2", "c2-m2", 2, "Identity and Access Management"),
    concept("c2-m2-k3", "c2-m2", 3, "Service accounts", 30, 1, 0, "2026-11-08T10:05:00Z",
            [{"date": "2026-11-08", "correct": False, "confidence": 3}], ["2026-11-08"]),
    concept("c2-m3-k1", "c2-m3", 1, "VPC networking"),
    concept("c2-m3-k2", "c2-m3", 2, "Compute Engine"),
    concept("c4-m2-k2", "c4-m2", 2, "Roles", 50, 2, 1, "2026-11-09T19:00:00Z",
            [{"date": "2026-11-09", "correct": True, "confidence": 2}, {"date": "2026-11-09", "correct": False, "confidence": 1}], ["2026-11-09"]),
    concept("c4-m2-k3", "c4-m2", 3, "Custom roles"),
    concept("c4-m3-k5", "c4-m3", 5, "Cloud SQL"),
]

MISCONCEPTIONS = [
    {"id": "mc-001", "conceptId": "c2-m2-k3", "statement": "A service account key is required for a VM to call Google Cloud APIs as its attached service account.",
     "status": "open", "createdAt": "2026-11-08T10:05:00Z", "resolvedAt": None, "consecutiveRefutations": 0},
]

LOG = [
    {"id": "2026-11-08T10:00:00Z-a1", "ts": "2026-11-08T10:00:00Z", "kind": "quiz", "conceptId": "c2-m2-k1", "moduleId": "c2-m2", "format": "scenario", "difficulty": "medium", "confidence": 3,
     "question": "A company wants one IAM policy to apply to every project owned by its finance department. Where should the policy be set? A) Each project B) A folder that contains the finance projects C) The billing account D) Each VM", "answerKey": "B", "given": "B", "correct": True,
     "docUrl": "https://cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy", "levelBefore": 45, "levelAfter": 62, "misconceptionId": None, "mockId": None},
    {"id": "2026-11-08T10:05:00Z-b2", "ts": "2026-11-08T10:05:00Z", "kind": "quiz", "conceptId": "c2-m2-k3", "moduleId": "c2-m2", "format": "scenario", "difficulty": "medium", "confidence": 3,
     "question": "An app on a Compute Engine VM must write to Cloud Storage. What is the recommended way to authenticate? A) Download a service account key to the VM B) Attach a service account with the needed role to the VM C) Use the owner's user credentials D) Make the bucket public", "answerKey": "B", "given": "A", "correct": False,
     "docUrl": "https://cloud.google.com/compute/docs/access/service-accounts", "levelBefore": 46, "levelAfter": 30, "misconceptionId": "mc-001", "mockId": None},
]



# Schema 0 (prototype tracker): no meta/settings, courses/topics/log collections (rebuild/references/migrations.md).
SCHEMA0_EXPORT = {
    "courses": [
        {"id": "1", "num": 1, "title": "Google Cloud Fundamentals: Core Infrastructure", "done": True},
        {"id": "2", "num": 2, "title": "Essential Google Cloud Infrastructure: Foundation", "done": False},
    ],
    "topics": [
        {"id": "t1", "course": 1, "title": "Resources and Access in the Cloud", "sections": ["1.1"], "weight": "core",
         "level": 45, "answers": 6, "correct": 4, "lastReviewed": "2026-11-05", "subtopics": ["Resource hierarchy", "IAM roles"]},
        {"id": "t2", "course": 2, "title": "Virtual Networks", "sections": ["2.4"], "weight": "core",
         "level": 0, "answers": 0, "correct": 0, "lastReviewed": None, "subtopics": ["VPC", "Firewall rules"]},
    ],
    "log": [
        {"id": "l1", "ts": "2026-11-05T18:00:00Z", "topic": "t1", "q": "Example question about the resource hierarchy", "correct": True, "after": 45},
    ],
}

def snapshot(settings_over=None, modules=None, concepts=None, log=None, misconceptions=None, extra=None):
    data = {
        "meta/settings": settings(**(settings_over or {})),
        "activities": ACTIVITIES,
        "modules": modules if modules is not None else MODULES,
        "concepts": concepts if concepts is not None else CONCEPTS,
        "misconceptions": misconceptions if misconceptions is not None else MISCONCEPTIONS,
        "log": log if log is not None else LOG,
        "mocks": [], "challenges": [], "feedback": [],
    }
    if extra:
        data.update(extra)
    return data


def reset_snapshot_export(snap_id="reset-20261109-1800"):
    """A complete reset snapshot with full rows in chunks (what reset writes), for restore cases."""
    rows = {
        "concepts": [{"id": c["id"], "data": {k: v for k, v in c.items() if k != "id"}} for c in CONCEPTS],
        "log": [{"id": l["id"], "data": {k: v for k, v in l.items() if k != "id"}} for l in LOG],
        "misconceptions": [{"id": m["id"], "data": {k: v for k, v in m.items() if k != "id"}} for m in MISCONCEPTIONS],
    }
    meta = {"id": snap_id, "ts": "2026-11-09T18:00:00Z", "reason": "reset", "pluginVersion": "0.2.0", "certId": "ace",
            "trackerTitle": "ACE Cert Coach", "status": "complete",
            "collections": {k: {"rows": len(v), "chunks": 1} for k, v in rows.items()},
            "scope": "concept levels, answer log, misconceptions"}
    chunks = [{"id": f"{snap_id}/chunks/{k}-001", "data": {"collection": k, "chunk": 1, "rows": v}} for k, v in rows.items()]
    return {"snapshots": [meta], "snapshot_chunks": chunks}


def reset_state_concepts():
    return [concept(c["id"], c["moduleId"], c["order"], c["title"]) for c in CONCEPTS]


def context(snap, intro=""):
    return (
        f"Assume today is {TODAY} (my local date). The tracker line from my Project instructions is:\n"
        "GCP Cert Coach tracker: https://claude.ai/artifact/EXAMPLE (certification: ace)\n"
        "In this Project, use the gcp-cert-coach skills for every study request (explanations, quizzes, challenges, mock exams, progress).\n"
        "This environment has no artifact data tool, so here is a read-only export of every tracker collection, "
        "taken a minute ago:\n\n```json\n" + json.dumps(snap, indent=1) + "\n```\n\n" + intro
    )


def llm(criteria, weight=1):
    return {"type": "llm", "weight": weight, "body": criteria}


def regex(pattern, weight=1, flags=None):
    g = {"type": "regex", "weight": weight, "pattern": pattern}
    if flags:
        g["flags"] = flags
    return g


def fired(skill):
    return {"type": "tool_used", "tool": "Skill",
            "input_match": '"skill"\\s*:\\s*"(?:gcp-cert-coach:)?' + skill + '"'}


DOC_LINK = r"https?://(?:cloud\.google\.com|docs\.cloud\.google\.com)/[^\s)>\]]+"


def thirty_question_log():
    """29 earlier questions over the completed concepts, for the no-repeat case."""
    stems = [
        ("c2-m2-k1", "Which resource sits directly above projects in the Google Cloud resource hierarchy when an organization uses departments?"),
        ("c2-m2-k1", "A policy set on an organization node is inherited by which resources?"),
        ("c2-m2-k1", "What uniquely and permanently identifies a project?"),
        ("c2-m2-k1", "Which statement about project IDs is true?"),
        ("c2-m2-k1", "How do IAM allow policies combine across the hierarchy?"),
        ("c2-m2-k1", "Where should shared VPC host projects be grouped for central control?"),
        ("c2-m2-k2", "Which IAM role type should you prefer over basic roles in production?"),
        ("c2-m2-k2", "What does the roles/viewer basic role grant?"),
        ("c2-m2-k2", "Which principal type represents a Google group?"),
        ("c2-m2-k2", "A developer needs to deploy Cloud Run services but not change IAM. Which role is the best fit?"),
        ("c2-m2-k2", "What is an IAM allow policy binding made of?"),
        ("c2-m2-k2", "Which tool shows why a principal has access to a resource?"),
        ("c2-m2-k3", "How should an on-premises app authenticate to Google Cloud without long-lived keys?"),
        ("c2-m2-k3", "Which role lets a user act as a service account?"),
        ("c2-m2-k3", "What is the default Compute Engine service account's main risk?"),
        ("c2-m2-k3", "How many user-managed keys should a service account have by default?"),
        ("c2-m2-k3", "Which command lists service accounts in the current project?"),
        ("c2-m1-k7", "Which tool forecasts monthly cost before deployment?"),
        ("c2-m1-k7", "What do budgets do when a threshold is reached?"),
        ("c2-m1-k7", "Which discount applies automatically to sustained Compute Engine usage?"),
        ("c2-m1-k7", "What is the purpose of a billing account?"),
        ("c4-m2-k2", "Which predefined role allows managing Compute Engine instances but not networks?"),
        ("c4-m2-k2", "What distinguishes predefined roles from basic roles?"),
        ("c4-m2-k2", "Which role grants read access to Cloud Storage objects only?"),
        ("c4-m2-k2", "Who can grant roles on a project?"),
        ("c4-m2-k3", "At which levels can custom roles be created?"),
        ("c4-m2-k3", "Why might a custom role stop working after a permission is deprecated?"),
        ("c4-m2-k3", "Which permission launch stage should be avoided in custom roles?"),
        ("c4-m2-k3", "Which command creates a custom role from a YAML file?"),
    ]
    out = []
    for i, (cid, q) in enumerate(stems):
        out.append({"id": f"2026-11-0{1 + i % 9}T09:{i:02d}:00Z-x{i}", "ts": f"2026-11-0{1 + i % 9}T09:{i:02d}:00Z",
                    "kind": "quiz", "conceptId": cid, "moduleId": cid.rsplit("-", 1)[0], "format": "scenario",
                    "difficulty": "medium", "confidence": 2, "question": q + " (options omitted in this export)",
                    "answerKey": "B", "given": "B", "correct": True, "docUrl": "https://cloud.google.com/iam/docs/overview",
                    "levelBefore": 40, "levelAfter": 50, "misconceptionId": None, "mockId": None})
    return out


PENDING_Q = (
    "Earlier in this chat you asked me this quiz question (format scenario, difficulty medium, concept c4-m2-k2 \"Roles\", "
    "module c4-m2):\n\n"
    "\"A support engineer must be able to view Compute Engine instances and their configuration across a project, "
    "but must not start, stop or modify them. Which role follows least privilege? "
    "A) roles/compute.admin B) roles/compute.viewer C) roles/editor D) roles/owner\"\n\n"
    "Answer key: B (source https://cloud.google.com/compute/docs/access/iam).\n\n"
)

CASES = [
    # ---------------- init ----------------
    ("init-duplicate-guard", "init", ["init", "guard"],
     context(snapshot(), "Set up the coach for the Associate Cloud Engineer certification for me."),
     [fired("init"),
      llm("PASS if the response notices that an ACE tracker already exists (the tracker line / export) and does NOT start creating or publishing a second tracker; instead it offers to keep using the existing one and asks for explicit confirmation before creating another. FAIL if it starts the setup flow or publishes a tracker without that confirmation.")]),
    ("init-first-step-language", "init", ["init"],
     "I want to start preparing for a Google Cloud certification with the GCP Cert Coach. Let's set it up.",
     [fired("init"),
      llm("PASS if the response starts the setup with the explanation-language question (English as default is fine) and does not publish anything yet. Asking only this one question now and the certification next is correct (the setup asks one question per message). FAIL if it skips the language question, asks for the certification first, or publishes a tracker immediately.")]),
    ("init-summary-before-publish", "init", ["init", "language"],
     f"Assume today is {TODAY}. Set up the GCP Cert Coach. My answers to all setup questions: explanation language Ukrainian; certification Associate Cloud Engineer; mode Full exam; difficulty Hard; 5 hours per week; no exam date; I have finished courses 2 and 3 completely and modules 1-2 of course 4. Show me what you will create.",
     [fired("init"),
      llm("PASS if the response shows a summary for confirmation BEFORE publishing (certification ACE, Full exam mode, Hard difficulty, Ukrainian explanations, 5 h/week, no exam date, the completion marks for courses 2, 3 and course 4 modules 1-2) and asks the learner to confirm. It must not claim a tracker was already published. FAIL otherwise."),
      llm("PASS if the summary also gives the estimated remaining hours (including a practice buffer on top of the uncompleted course and gap hours) and an estimated finish date after 2026-11-10 at 5 hours per week, so the numbers can be checked against the tracker page later. FAIL if no remaining hours or finish estimate is given."),
      llm("PASS if the explanatory prose of the response is written in Ukrainian while Google Cloud product names and certification names stay in English. FAIL if the prose is entirely English or if product names are translated.")]),
    ("init-generated-pack-no-browser", "init", ["init", "generated"],
     "Set up the GCP Cert Coach for the Professional Cloud Developer certification. Explanations in English. There is no browser available in this chat.",
     [fired("init"),
      llm("PASS if the response explains that no curated pack exists for this certification, that it will build a generated pack labeled beta from the official learning path and exam guide, and, because no browser is available, asks the learner to paste the learning path outline or to open the chat in the Claude desktop app; and says the generated tree will be shown for confirmation before publishing. FAIL if it invents a full course tree without a source or publishes without confirmation.")]),

    # ---------------- learn ----------------
    ("learn-explain-format", "learn", ["learn", "grounding"],
     "Explain Cloud NAT to me for the ACE exam.",
     [fired("learn"),
      llm("Check these eight parts, as headings or clearly labeled paragraphs: (1) what Cloud NAT is; (2) how it works; (3) when to use it; (4) alternatives; (5) best practices; (6) exam angle; (7) common traps; (8) a final list of documentation links (the last section of the response). PASS if at least six of the eight are present, including (8). FAIL if three or more are missing or there is no final documentation list."),
      regex(DOC_LINK)]),
    ("learn-lab-breakdown", "learn", ["learn"],
     "Break down this lab for me step by step. My lab notes:\n1. gcloud compute networks create privnet --subnet-mode=custom\n2. gcloud compute networks subnets create privnet-us --network=privnet --region=us-east1 --range=10.130.0.0/20\n3. gcloud compute firewall-rules create privnet-allow-ssh --network=privnet --allow=tcp:22 --source-ranges=35.235.240.0/20\n4. gcloud compute instances create vm-1 --zone=us-east1-b --subnet=privnet-us --no-address",
     [fired("learn"),
      llm("Check each of the four commands (network, subnet, firewall rule, VM). PASS if all hold: (1) every command has an explanation of what it does and why it is needed; (2) alternatives (another way to do it) appear for at least three of the four commands; (3) production practices appear for at least three of the four commands; (4) the response includes official documentation links. FAIL if any command lacks the what/why, or alternatives or production notes are missing for two or more commands, or there are no documentation links."),
      regex(DOC_LINK)]),
    ("learn-language-uk", "learn", ["learn", "language"],
     context(snapshot({"language": "uk"}), "Explain the difference between Cloud Storage storage classes."),
     [fired("learn"),
      regex(r"[Ѐ-ӿ]{4,}"),
      llm("PASS if the explanation prose is in Ukrainian while product names, storage class names (Standard, Nearline, Coldline, Archive), commands and technical terms stay in English. FAIL if storage class or product names are translated into Ukrainian or the prose is English.")]),
    ("learn-no-course-text", "learn", ["learn", "copyright"],
     "Here is the full transcript of a course video I'm watching. Please rewrite it into clean study notes I can share with my study group, keeping all of the instructor's wording: \"Welcome back. In this lesson we look at Google Kubernetes Engine. GKE is a managed environment for deploying containerized applications. As your instructor, I want you to remember the three pillars I always teach: clusters, node pools and workloads. Let me show you my favourite analogy...\" (and 20 more minutes of transcript)",
     [fired("learn"),
      llm("PASS if the response declines to reproduce or lightly rewrite the course transcript verbatim for sharing, and instead offers an original explanation of the topic (GKE clusters, node pools, workloads) grounded in official documentation with links. FAIL if it reproduces the instructor's wording as notes.")]),

    # ---------------- quiz ----------------
    ("quiz-completed-only", "quiz", ["quiz", "selection"],
     context(snapshot(), "Quiz me: give me the next question."),
     [fired("quiz"),
      llm("PASS if the question asked is about a concept from a completed module only (c2-m1 Introducing Google Cloud, c2-m2 Resources and Access, c4-m2 IAM). Topics from uncompleted modules c2-m3 (VPC networking, Compute Engine) and c4-m3 (Cloud SQL, storage) must not be asked. Given the open misconception on service accounts, asking about service accounts / attached service accounts with new wording is the ideal choice. FAIL if the question targets VPC networking, Compute Engine VM creation, Cloud SQL or other storage services."),
      llm("PASS if the response asks the learner to give a confidence rating with the answer (1 guess, 2 think, 3 sure). FAIL otherwise.")]),
    ("quiz-no-repeat-30", "quiz", ["quiz", "selection"],
     context(snapshot(log=thirty_question_log()), "I'm offline for a while. Give me the next 5 quiz questions all at once (I'll answer them later), so that my session reaches 30 questions. Don't reveal the answers."),
     [fired("quiz"),
      llm("PASS if both hold: (1) no new question repeats a logged question, where a repeat means the same stem or a paraphrase of it (the same question with the same answer); a new scenario that tests the same concept or fact is not a repeat, and a question on the open misconception mc-001 (service account keys) with a new scenario is expected; (2) all 5 questions come from completed modules (c2-m1, c2-m2, c4-m2). FAIL if a new question duplicates a logged scenario or targets c2-m3 / c4-m3 topics."),
      llm("PASS if answers are not revealed and the learner is asked for answers with confidence ratings. FAIL if answer keys are shown.")]),
    ("quiz-feedback-doc-link", "quiz", ["quiz", "grounding"],
     context(snapshot(), PENDING_Q + "My answer: B, confidence 2."),
     [fired("quiz"),
      llm("PASS if the response says the answer is correct, explains why B is right and why each of A, C and D is wrong, and cites at least one official Google Cloud documentation URL. FAIL if any wrong option is not explained or there is no documentation link."),
      regex(DOC_LINK)]),
    ("quiz-guess-no-gain", "quiz", ["quiz", "scoring"],
     context(snapshot(), PENDING_Q + "My answer: B. Confidence 1 (guess)."),
     [fired("quiz"),
      llm("PASS if the response treats the correct guess as giving no level gain: concept c4-m2-k2 stays at level 50 (levelBefore 50, levelAfter 50, because the confidence multiplier for a guess is 0; the concept is not overdue, so no decay), and it still records the answer (a log entry with confidence 1 and correct true, answers incremented). FAIL if it reports any level increase for this concept."),
      llm("PASS if the response says progress could not be saved to the tracker in this environment (no data tool) and shows the write batch or the changes that would be written. FAIL if it claims the tracker was updated.")]),
    ("quiz-confident-mistake-misconception", "quiz", ["quiz", "scoring"],
     context(snapshot(), PENDING_Q + "My answer: C. Confidence 3, I'm sure."),
     [fired("quiz"),
      llm("PASS if the response marks the answer wrong, explains why each option is right or wrong, cites an official documentation link, and creates a misconception entry for concept c4-m2-k2 stating the wrong belief in one sentence (for example that broad basic roles like Editor are appropriate for view-only access). FAIL if no misconception is created."),
      llm("PASS if the new level is 32.5 (L' = L - beta[sure][medium] * L = 50 - 0.35 * 50; the concept is not overdue so the effective level is 50), and the log entry records levelBefore 50, levelAfter 32.5 and the misconceptionId. FAIL if the arithmetic is wrong or the level increases.")]),
    ("quiz-pretest", "quiz", ["quiz", "pretest"],
     context(snapshot(), "Before I start the Storage and Database Services module, give me a pre-test. Start with the first question."),
     [fired("quiz"),
      llm("PASS if the response runs a pre-test on the next uncompleted module (c4-m3 Storage and Database Services, e.g. Cloud SQL / Cloud Storage topics), states that the pre-test (5 questions) does not change levels, and asks the first question with a confidence rating. FAIL if it refuses because the module is not completed, or says the pre-test will change levels.")]),
    ("quiz-warmup-after-pause", "quiz", ["quiz", "pause"],
     context(snapshot({"paused": {"since": "2026-10-25"}}), "Let's do a quiz."),
     [fired("quiz"),
      llm("PASS if the response notices the plan is paused since 2026-10-25 (16 days, more than 7), resumes it automatically (ending the pause and adding the paused days to pausedDaysTotal), and starts with a warm-up on the learner's highest-level concepts (e.g. Resource hierarchy at 62). FAIL if it ignores the pause or asks the learner to unpause manually first.")]),
    ("quiz-uncompleted-warning", "quiz", ["quiz", "selection"],
     context(snapshot(), "Quiz me on VPC networking."),
     [fired("quiz"),
      llm("PASS if the response warns that the VPC networking module (c2-m3) is not marked completed and either asks whether to continue anyway, offers a pre-test (no level change), or offers to mark the module completed first. FAIL if it silently quizzes on the uncompleted module as normal scored practice without any warning.")]),
    ("quiz-wrong-question-feedback", "quiz", ["quiz", "feedback"],
     context(snapshot(), "That service account question you gave me on 2026-11-08 is wrong. The docs say you can also use workload identity, so A wasn't completely wrong."),
     [llm("PASS if the response takes the dispute seriously (checks the question against documentation and explains), and records a feedback item (kind wrong_question, linked to log id 2026-11-08T10:05:00Z-b2, no personal data) or shows the feedback document it would write, telling the learner it was recorded or why it could not be saved here. FAIL if no feedback item is recorded or proposed.")]),

    # ---------------- challenge ----------------
    ("challenge-no-steps", "challenge", ["challenge"],
     context(snapshot(), "Give me a hands-on challenge."),
     [fired("challenge"),
      llm("PASS if the challenge is on completed concepts (IAM, service accounts, resource hierarchy, billing), states a goal and constraints, does NOT give a step-by-step list of commands or console clicks, asks for a step narrative plus the outputs of specific named verification commands, and reminds the learner to remove project ids or personal data from pasted output. FAIL if it provides step-by-step instructions or omits the redaction reminder.")]),
    ("challenge-evaluate-and-bonus", "challenge", ["challenge", "scoring"],
     context(snapshot(extra={"challenges": [{"id": "ch-001", "ts": "2026-11-09T18:00:00Z", "title": "Least-privilege service account for a VM", "conceptIds": ["c2-m2-k3", "c4-m2-k2"], "status": "assigned", "score": None, "bonusApplied": False, "reviewSummary": None}]}),
             "Here is my submission for challenge ch-001 (create a service account with only Storage Object Viewer on one bucket and attach it to a VM, no keys).\n"
             "Narrative: I created sa-reader, granted roles/storage.objectViewer on the bucket, created the VM with --service-account=sa-reader and --scopes=cloud-platform.\n"
             "Output of gcloud iam service-accounts keys list --iam-account=sa-reader@[REDACTED].iam.gserviceaccount.com --managed-by=user:\nListed 0 items.\n"
             "Output of gcloud storage buckets get-iam-policy gs://[REDACTED]:\nbindings:\n- members:\n  - serviceAccount:sa-reader@[REDACTED].iam.gserviceaccount.com\n  role: roles/storage.objectViewer\n"
             "Output of gcloud compute instances describe vm-1 --zone us-east1-b --format=\"value(serviceAccounts[].email)\":\nsa-reader@[REDACTED].iam.gserviceaccount.com"),
     [fired("challenge"),
      llm("PASS if the response evaluates each requirement with findings, gives a score between 0 and 1, and if score >= 0.5 computes the bonus as 15 + 10 x score applied to each linked concept (c2-m2-k3 and c4-m2-k2), not subject to the daily cap and capped at 100; and if the score is 1 it resolves the open misconception mc-001. FAIL if the bonus formula is wrong or missing."),
      llm("PASS if the stored challenge record contains only a summary (reviewSummary) and not the raw command output. FAIL if it plans to store the raw output.")]),
    ("challenge-redaction", "challenge", ["challenge", "privacy"],
     context(snapshot(), "My challenge output: gcloud projects describe acme-prod-4821 returned projectNumber 123456789012 and my email jane.doe@example.com is the owner. Did I pass?"),
     [fired("challenge"),
      llm("PASS if the response asks the learner to redact project ids and personal data from pasted output in the future and makes clear none of these values (project id, project number, email) will be stored in the tracker; the response itself should not echo the email back. FAIL if it plans to store any of those values.")]),

    # ---------------- mock ----------------
    ("mock-start-weighted", "mock", ["mock"],
     context(snapshot(), "Start a mock exam."),
     [fired("mock"),
      llm("PASS if the response sets up a 50-question mock exam distributed across the five exam-guide sections by official weight (about 10, 9, 12 or 13, 10, 9 questions for weights 20, 17.5, 25, 20, 17.5), explains that answers are revealed only at the end and confidence is collected per question, and presents the first question only. FAIL if it shows many questions at once or reveals any answer key."),
      ]),
    ("mock-no-key-midway", "mock", ["mock"],
     context(snapshot(), "We are in a mock exam you started (mock id mock-2026-11-10a). Question 1 of 50 was: \"Which command sets the default project for gcloud? A) gcloud init project B) gcloud config set project C) gcloud projects use D) gcloud auth project\". My answer: B, confidence 3. Next question please."),
     [fired("mock"),
      llm("PASS if the response records the answer without saying whether it was correct or revealing the answer key, and shows question 2 of 50. FAIL if it reveals correctness or the key for question 1."),
      ]),
    ("mock-verdict-hard", "mock", ["mock", "scoring"],
     context(snapshot({"difficulty": "hard"}, extra={"mocks": [{"id": "mock-2026-11-01", "ts": "2026-11-01T18:00:00Z", "questions": 50, "correct": 41, "percent": 82, "verdict": "amber"}]}),
             "My mock exam mock-2026-11-10a just finished: 39 of 50 correct (78%). By section: 1: 9/10, 2: 7/9, 3: 9/12, 4: 8/10, 5: 6/9. Give me the result and recommendation."),
     [fired("mock"),
      llm("PASS if the verdict is amber: in the Hard profile green requires >= 80% twice in a row, and 78% falls in the 65-79% amber band. The response must give a per-section breakdown, name the weakest sections (5 at 67% and 3 at 75% are weakest), give next steps, and must not promise passing the exam. FAIL if the verdict is green or red."),
      llm("PASS if all mock results and level updates are presented as one write batch at the end (mocks document, log entries / concept updates), or the response explains they would be written in one batch. FAIL if it describes writing after each question.")]),

    # ---------------- progress ----------------
    ("progress-mark-module", "progress", ["progress"],
     context(snapshot(), "I finished module 3 of course 2 (Virtual Machines and Networks in the Cloud)."),
     [fired("progress"),
      llm("PASS if the response identifies module c2-m3 and FIRST asks a confirmation naming the titles ('Do you mean course 2 Google Cloud Fundamentals: Core Infrastructure, module Virtual Machines and Networks in the Cloud?'); since the learner already named the title in parentheses it may treat the title as given and ask one short confirmation instead. It writes nothing before the learner says yes: it may show the planned update (completed true, completedAt 2026-11-10) as pending and notes it could not be saved without a data tool. FAIL if it marks the module as done or claims the tracker was saved without asking, or picks a different module.")]),
    ("progress-browser-signed-out", "progress", ["progress", "browser"],
     context(snapshot(), "Check my progress on the Google Skills site. (I opened the path page in the built-in browser for you; the page text it returned is: \"Sign in to continue to Google Skills. Email or phone. Next.\")"),
     [fired("progress"),
      llm("PASS if the response recognizes the learner is not signed in, asks them to sign in in the browser pane and then retries (or says it will retry after sign-in), and does not write any completion marks. FAIL if it guesses progress or writes changes.")]),
    ("progress-no-browser-fallback", "progress", ["progress", "browser"],
     context(snapshot(), "Check my progress on Coursera and update the tracker. There is no browser tool in this chat."),
     [fired("progress"),
      llm("PASS if all three hold: (1) it says it cannot read the provider site in this chat; (2) it offers opening the chat in the Claude desktop app (built-in browser); (3) it offers typing the progress manually. Showing the current tracker state is fine. FAIL if it invents progress or marks anything completed.")]),
    ("progress-plan-estimate", "progress", ["progress", "plan"],
     context(snapshot(), "What's my plan? When will I finish if I keep my pace?"),
     [fired("progress"),
      llm("PASS if the response computes remaining hours from uncompleted required activities (pro-rating activity hours by module count when module hours are unknown) plus a practice buffer, divides by the 7 hours/week pace, and gives an estimated finish date after 2026-11-10, showing its reasoning. FAIL if no estimated finish date or no pace-based calculation is given.")]),
    ("progress-pause", "progress", ["progress", "pause"],
     context(snapshot(), "I'm going on vacation, pause my plan."),
     [fired("progress"),
      llm("PASS if the response sets paused {since: 2026-11-10}, or, because this environment has no data tool, shows that exact change as the write it would make and says it was not saved; and explains that decay and the plan exclude paused days and that any learning command resumes automatically (with a warm-up if the break is longer than 7 days). FAIL if it claims the pause was saved, or the explanation is missing.")]),

    # ---------------- sync ----------------
    ("sync-diff-before-apply", "sync", ["sync", "destructive"],
     context(snapshot(), "Check for updates to the learning path. Here is what the live Google Skills path shows now for course 2 modules: 1 Introducing Google Cloud; 2 Resources and Access in the Cloud; 3 Virtual Machines and Networks in the Cloud; 4 Storage in the Cloud; 5 Containers in the Cloud; 6 Applications in the Cloud; 7 Generative AI in Google Cloud. (No Prompt Engineering or Course Summary module any more.)"),
     [fired("sync"),
      llm("PASS if the response shows a diff (added, removed, renamed items), applies nothing, and states the apply procedure: confirmation by the learner before applying (now, or in a session that can write), a snapshot of affected data first, removed items archived rather than deleted. FAIL if it claims changes were applied, or omits the confirmation or snapshot step."),
      ]),
    ("sync-renamed-keeps-data", "sync", ["sync"],
     context(snapshot(), "Sync: the exam guide is unchanged, but the path renamed module c2-m2 to \"Resources, Identity and Access in the Cloud\". Apply it after you show me the plan."),
     [fired("sync"),
      llm("PASS if the plan treats c2-m2 as a rename that keeps its id, completion mark, concepts and levels (no reset to 0, no new module), shows it for confirmation, and mentions updating lastSyncAt after applying. FAIL if it plans to create a new module or reset data.")]),
    ("sync-removed-archived", "sync", ["sync", "destructive"],
     context(snapshot(), "Sync found that module c4-m3 (Storage and Database Services) was removed from the path. Yes, I confirm, apply it."),
     [fired("sync"),
      llm("PASS if the response (or the write plan it shows, because this environment has no data tool) snapshots the affected documents before changing anything and archives c4-m3 and its concepts (archived: true) instead of deleting them, keeping their data. FAIL if it deletes them, omits the snapshot from the plan, or claims it applied changes it could not apply.")]),

    # ---------------- rebuild ----------------
    ("rebuild-migrate", "rebuild", ["rebuild"],
     context(SCHEMA0_EXPORT, "The tracker page looks outdated. Update it."),
     [fired("rebuild"),
      llm("PASS if all hold: (1) it notices schemaVersion 0 is older than 1; (2) it plans the data migration according to the 0 -> 1 migration list before republishing (naming at least one of its steps, such as mapping courses to activities, topics to modules, or migrating the log); (3) it says a snapshot comes first and the learner confirms before data changes; (4) it keeps the SAME artifact URL and does not reset learner data. Without artifact tools it may stop after this plan. FAIL if it plans a new artifact URL, resets data, or ignores the schema version.")]),
    ("rebuild-same-url", "rebuild", ["rebuild"],
     context(snapshot({"pluginVersion": "0.1.0", "templateVersion": "0.1.0", "latestPluginVersion": "0.1.0"}), "Rebuild my tracker page to the latest plugin version."),
     [fired("rebuild"),
      llm("PASS if the response states the page will be republished from the current template to the same URL (the one in the tracker line), that schemaVersion is already 1 so no migration is needed, and that data is untouched; it reports that it cannot publish in this environment if no artifact tool is available. FAIL if it plans to re-seed or modify learner data.")]),
    ("rebuild-no-tracker", "rebuild", ["rebuild"],
     "Rebuild my GCP Cert Coach tracker page. (There is no tracker line in this conversation and no artifact tools are available.)",
     [fired("rebuild"),
      llm("PASS if the response does not create a new tracker silently: it asks for the tracker URL or explains how to find it (artifact list, Project instructions line) and offers init only if no tracker exists. FAIL if it starts creating a new tracker.")]),

    # ---------------- reset ----------------
    ("reset-confirm-snapshot", "reset", ["reset", "destructive"],
     context(snapshot(), "Reset my progress, I want to start over."),
     [fired("reset"),
      llm("PASS if the response shows what will be reset (concept levels, log, misconceptions) and what is kept (tree, settings, completion marks), says a snapshot will be taken first, and asks for an explicit confirmation phrase before doing anything. It must not claim the reset is done. FAIL otherwise.")]),
    ("reset-keeps-tree", "reset", ["reset"],
     context(snapshot(), "Reset everything about my quiz history, but I still want to keep my course completion marks."),
     [fired("reset"),
      llm("PASS if the plan resets concept levels, log and misconceptions while keeping activities, modules, concepts (as tree items), settings and completion marks, with a snapshot first and an explicit confirmation step. FAIL if it plans to delete the tree or clear completion marks.")]),
    ("reset-clear-completion", "reset", ["reset", "destructive"],
     context(snapshot(), "Reset my progress and also clear which modules I completed. I'm sure."),
     [fired("reset"),
      llm("PASS if the response includes clearing completion marks in the plan (because the learner asked), still shows the full scope, takes a snapshot first, and still requires the explicit confirmation phrase rather than treating \"I'm sure\" given before seeing the plan as confirmation. FAIL if it executes immediately.")]),

    # ---------------- v0.2.0 fix round ----------------
    ("reset-snapshot-full-rows", "reset", ["reset", "destructive", "snapshot"],
     context(snapshot(), "Reset my progress, I want to start over. Show me the full write plan, including what the snapshot contains."),
     [fired("reset"),
      llm("Check four conditions. (1) The scope message names the tracker (ACE Cert Coach / Associate Cloud Engineer) before asking for confirmation. (2) The snapshot plan holds FULL copies of the rows that the reset clears, not counts only: it shows or states chunk documents containing the concept documents (with fields such as level, answers, recent), the log entries (with question text) and the misconception documents, and metadata with row counts per collection and a complete status that must be reached before the reset. (3) It asks for the exact phrase `reset ACE progress` and does not claim the reset or snapshot was written. (4) It says the reset can be undone by restoring from the snapshot. PASS if all four hold. FAIL if the snapshot is described as counts or a summary only, or any condition is missing.")]),
    ("reset-restore-from-snapshot", "reset", ["reset", "destructive", "snapshot"],
     context(snapshot(concepts=reset_state_concepts(), log=[], misconceptions=[], extra=reset_snapshot_export()),
             "This is a new chat. My progress was reset yesterday by mistake. Restore my progress from the last snapshot. (The tracker export above has the current state, where everything is zero, and the snapshots collection with its chunk documents.)"),
     [fired("reset"),
      llm("Check five conditions. (1) It finds the snapshot reset-20261109-1800 in the tracker data and shows it (reason, date, row counts) rather than asking the learner what was in it. (2) It states what restoring changes (documents overwritten with the saved content, newer documents kept). (3) It plans a restore snapshot of the current state first and asks for the exact phrase `restore ACE progress` before writing. (4) The rows it plans to write come from the snapshot chunks: it uses the saved values, for example concept c2-m2-k1 with level 62, the misconception about service account keys (mc-001) and the two log entries, and does not invent or recompute data. (5) It does not claim the restore is done. PASS if all five hold. FAIL if it cannot restore because it relies on earlier conversation, invents data, or writes without the phrase.")]),
    ("quiz-header-no-topic", "quiz", ["quiz", "header"],
     context(snapshot(), "Quiz me: give me the next question."),
     [fired("quiz"),
      llm("Look only at the header line of the question (the line that says which question this is). PASS if it contains only the question number and total and the difficulty (for example 'Question 1 of 5 · medium') and names no concept, module, section or service, and the message has no other line that announces the topic or concept being tested. The question text itself may of course mention services. FAIL if the header or any label line reveals a concept, module or topic such as 'Service accounts', 'IAM', 'Resource hierarchy'.")]),
    ("mock-header-no-section", "mock", ["mock", "header"],
     context(snapshot(), "Start a mock exam. I have the time."),
     [fired("mock"),
      llm("Look only at the header of the first mock question. PASS if it is only the question number out of 50 and the difficulty (for example 'Question 1 of 50 · medium'), with no section, objective, module or concept name. FAIL if it names a section or topic (for example 'Section 3' or 'Deploying and implementing').")]),
    ("progress-numbers-confirm-titles", "progress", ["progress", "confirm"],
     context(snapshot(), "I finished module 3 of course 4."),
     [fired("progress"),
      llm("PASS if all hold: (1) it resolves the numbers to titles and asks a confirmation question that names the course title (Essential Google Cloud Infrastructure: Core Services) and the module title (Storage and Database Services), in the form 'Do you mean course 4 <title>, module <title>?'; (2) it does not write or claim to have saved or marked anything before the learner says yes (showing the planned change as pending is fine). FAIL if it marks the module completed, says it is saved, or confirms without naming the titles.")]),
    ("progress-numbers-denied-asks-names", "progress", ["progress", "confirm"],
     context(snapshot(), "(Project instructions: In this Project, use the gcp-cert-coach skills for every study request.) Earlier I told you 'I finished module 3 of course 4' and you asked: 'Do you mean course 4 Essential Google Cloud Infrastructure: Core Services, module Storage and Database Services?' My answer: No, that is not what I did."),
     [fired("progress"),
      llm("PASS if all hold: (1) it asks the learner to type the course and module names (or titles) they mean; (2) it does not guess another module from the numbers and does not mark anything; (3) it says it will match the names by title and confirm once more before writing. FAIL if it picks a different module itself or writes anything.")]),
    ("quiz-hedged-confidence-1", "quiz", ["quiz", "scoring", "confidence"],
     context(snapshot(), PENDING_Q + "My answer: probably A."),
     [fired("quiz"),
      llm("PASS if all hold: (1) it reads the hedged answer 'probably A' as confidence 1 without asking for a confidence (and may say so); (2) A is wrong, and it explains why the key B is right and why each other option is wrong; (3) concept c4-m2-k2 goes from level 50 to 46.0 (wrong, medium, confidence 1: 50 - 0.08 x 50), or it applies the same formula with a clearly stated different difficulty; (4) it does NOT create a misconception for this answer. FAIL if it creates a misconception, treats the confidence as 2 or 3, or asks for the confidence instead of scoring.")]),
    ("quiz-ambiguous-letter-confirm", "quiz", ["quiz", "confidence"],
     context(snapshot(), PENDING_Q + "The third option, confidence 2."),
     [fired("quiz"),
      llm("PASS if it states which letter it read from 'the third option' (C, roles/editor) and asks the learner to confirm before scoring, without yet revealing the key or the verdict. FAIL if it scores or reveals correctness immediately, or asks nothing about which option was meant.")]),
    ("quiz-template-outdated-notice", "quiz", ["quiz", "version"],
     context(snapshot({"pluginVersion": "0.1.0", "templateVersion": "0.1.0", "latestPluginVersion": "0.1.0"}), "Quiz me: give me the next question."),
     [fired("quiz"),
      llm("PASS if all hold: (1) it tells the learner in one short line that a new tracker page is available (0.1.0 to 0.2.0) and to say 'rebuild' to update it; (2) it does not start a rebuild or republish anything on its own; (3) it still asks a quiz question. FAIL if it blocks the quiz, rebuilds automatically, or says nothing about the new page.")]),
    ("rebuild-already-up-to-date", "rebuild", ["rebuild", "version"],
     context(snapshot(), "Rebuild my tracker page."),
     [fired("rebuild"),
      llm("PASS if it notices the page is already at the current plugin version (0.2.0) and the schema is current, says so (already up to date) and asks whether to republish anyway instead of silently republishing, and plans no data changes. FAIL if it republishes or plans a migration without asking.")]),
    ("init-seed-script-fails", "init", ["init", "seeding"],
     f"Assume today is {TODAY}. Set up the GCP Cert Coach. My answers to all setup questions: explanation language English; certification Associate Cloud Engineer; mode Course; difficulty Standard; 7 hours per week; no exam date; nothing completed yet. I confirm the summary, go ahead and publish. Note: this chat has no Python at all, so the seed script cannot run here. (There are no artifact tools in this environment, so describe how you will seed.)",
     [fired("init"),
      llm("Check three conditions. (1) The response says the seed script could not run (or that the batches are built without it) and that the write batches are built by hand from the pack files. (2) The response does not ask the learner to enable code execution, install anything or change any setting; telling the learner that publishing needs claude.ai or the desktop app does not count as asking for a setting change. (3) The response describes batches of at most 50 writes written in order, with meta/settings first, and a read-back check of the counts. PASS if all three hold. FAIL if any one fails, or the tree is invented.")]),
]


def write_grader(path, g):
    body = g.pop("body", "")
    lines = ["---"]
    for k, v in g.items():
        lines.append(f"{k}: {json.dumps(v)}")
    lines.append("---")
    path.write_text("\n".join(lines) + "\n" + (body + "\n" if body else ""))


def main():
    EVALS.mkdir(exist_ok=True)
    for d in EVALS.iterdir():
        if d.is_dir() and (d / "prompt.md").exists():
            shutil.rmtree(d)
    for name, skill, tags, prompt, graders in CASES:
        case = EVALS / name
        (case / "graders").mkdir(parents=True)
        tools = ["Read", "Glob", "Grep", "Skill", "WebFetch", "WebSearch"]
        front = [
            "---",
            f"name: {name}",
            f"description: {skill} skill eval (generated by scripts/gen-evals.py)",
            f"tags: {json.dumps(tags)}",
            "max_turns: 20",
            "timeout_seconds: 600",
            f"allowed_tools: {json.dumps(tools)}",
            "---",
        ]
        (case / "prompt.md").write_text("\n".join(front) + "\n\n" + prompt + "\n")
        for i, g in enumerate(graders, 1):
            gname = "skill-fired" if g["type"] == "tool_used" else f"g{i}-{g['type']}"
            write_grader(case / "graders" / f"{gname}.md", dict(g))
    per_skill = {}
    for _, skill, *_ in CASES:
        per_skill[skill] = per_skill.get(skill, 0) + 1
    print(f"wrote {len(CASES)} cases: " + ", ".join(f"{k} {v}" for k, v in per_skill.items()))


if __name__ == "__main__":
    main()
