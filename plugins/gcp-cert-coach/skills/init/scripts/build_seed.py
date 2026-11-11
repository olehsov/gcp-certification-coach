#!/usr/bin/env python3
"""Build the tracker database seed for GCP Cert Coach from a certification pack.

Reads a curated pack folder (pack.yaml, path.yaml, gaps.yaml, scoring.yaml) or a generated
pack JSON file with the same structure, applies the learner's setup choices, and writes:

  <out>/batch-01.json ... batch-NN.json   write batches, at most 50 operations each
  <out>/summary.json                      counts per collection and remaining-hours estimate
  <out>/ui-strings-en.json                English UI strings of the tracker page (to translate)

Each batch is a JSON list of {"op": "set", "path": "<collection>/<docId>", "data": {...}}.
Send the batches in order with the artifact data tool, one tool call per batch.

Usage (paths relative to the init skill folder):
  python3 scripts/build_seed.py --pack assets/packs/ace --out /tmp/seed \
      --mode full --difficulty standard --language en --pace 7 \
      --start-date 2026-01-15 [--exam-date 2026-03-01] [--completed "c2,c3,c4-m1,c4-m2"]

--completed takes activity ids (all modules) and/or module ids, comma-separated.
Requires PyYAML for curated packs (`pip install pyyaml` if the import fails).
"""
import argparse
import datetime as dt
import json
import pathlib
import re
import sys

PLUGIN_VERSION = "0.2.1"  # keep equal to plugin.json "version" (checked in CI)
SCHEMA_VERSION = 1
SKILLS_LINE = "In this Project, use the gcp-cert-coach skills for every study request (explanations, quizzes, challenges, mock exams, progress)."  # second Project instructions line (init step 11)
BATCH_SIZE = 50  # ARCHITECTURE 5.1: seed in batches of at most 50 writes


def load_pack(pack: str) -> dict:
    p = pathlib.Path(pack)
    if p.is_file() and p.suffix == ".json":
        return json.loads(p.read_text(encoding="utf-8"))
    try:
        import yaml  # noqa: PLC0415
    except ImportError:
        sys.exit("build_seed: PyYAML is missing. Run `pip install pyyaml` and retry.")
    read = lambda name: yaml.safe_load((p / name).read_text(encoding="utf-8"))  # noqa: E731
    meta = read("pack.yaml")
    return {"meta": meta, "path": read("path.yaml"), "gaps": read("gaps.yaml"), "scoring": read("scoring.yaml")}


def ui_strings(template: pathlib.Path) -> dict:
    """Extract the EN fallback map from the tracker template (keys and English values)."""
    src = template.read_text(encoding="utf-8")
    block = src[src.index("const EN = {"): src.index("};", src.index("const EN = {"))]
    return {k: json.loads('"' + v + '"') for k, v in re.findall(r'(\w+):"((?:[^"\\]|\\.)*)"', block)}


def estimate_plan(acts, gaps, completed, mode, pace, today, exam_date, scoring) -> dict:
    """Plan estimate; same formula as references/plan-estimate.md and the tracker page (nothing logged yet)."""
    pc = scoring.get("plan", {})
    gap_h, buf_f = pc.get("gapHoursPerTopic", 1), pc.get("practiceBufferFraction", 0.2)
    required = remaining = 0.0
    for x in acts:
        if x.get("optional"):
            continue
        required += x.get("hours") or 0
        mods = x["modules"]
        for m in mods:
            if m["id"] not in completed:
                remaining += m["hours"] if m.get("hours") is not None else ((x.get("hours") or 0) / len(mods) if mods else 0)
    if mode == "full" and gaps.get("topics"):
        n = len(gaps["topics"])
        per = gaps.get("activity", {}).get("hoursPerTopic", gap_h)
        required += n * per
        remaining += n * per
    remaining += max(0.0, required * buf_f)  # nothing logged at setup
    out = {"requiredHours": round(required, 2), "remainingHours": round(remaining, 1),
           "paceHoursPerWeek": pace}
    if exam_date:
        weeks = max((dt.date.fromisoformat(exam_date) - dt.date.fromisoformat(today)).days, 1) / 7
        out["requiredPaceHoursPerWeek"] = round(remaining / weeks, 1)
        out["onTrack"] = remaining / weeks <= pace
    else:
        out["estimatedFinish"] = (dt.date.fromisoformat(today) + dt.timedelta(days=round(remaining / pace * 7))).isoformat()
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pack", required=True, help="pack folder (curated) or generated pack .json")
    ap.add_argument("--out", required=True)
    ap.add_argument("--mode", choices=["course", "full"], default="course")
    ap.add_argument("--difficulty", choices=["standard", "hard"], default="standard")
    ap.add_argument("--language", default="en", help="BCP-47 tag, e.g. en, uk, de")
    ap.add_argument("--pace", type=float, default=7.0, help="study hours per week")
    ap.add_argument("--start-date", required=True, help="learner's local date YYYY-MM-DD")
    ap.add_argument("--exam-date", default=None)
    ap.add_argument("--completed", default="", help="activity and/or module ids, comma-separated")
    ap.add_argument("--template", default=None, help="tracker.html path (default: ../assets/tracker.html)")
    a = ap.parse_args()

    for d in [a.start_date] + ([a.exam_date] if a.exam_date else []):
        dt.date.fromisoformat(d)  # raises a clear error on a bad date
    pack = load_pack(a.pack)
    meta, path, gaps, scoring = pack["meta"], pack["path"], pack.get("gaps") or {}, pack["scoring"]
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    acts = path["activities"]
    act_ids = {x["id"] for x in acts}
    mod_ids = {m["id"] for x in acts for m in x["modules"]} | {t["id"] for t in gaps.get("topics", [])}
    done = {s.strip() for s in a.completed.split(",") if s.strip()}
    unknown = done - act_ids - mod_ids
    if unknown:
        sys.exit("build_seed: unknown ids in --completed: " + ", ".join(sorted(unknown))
                 + ". Use activity ids like c2 or module ids like c4-m2.")
    completed_mods = {m["id"] for x in acts for m in x["modules"] if x["id"] in done or m["id"] in done}

    ops = []
    settings = {
        "schemaVersion": SCHEMA_VERSION, "pluginVersion": PLUGIN_VERSION,
        "templateVersion": PLUGIN_VERSION, "latestPluginVersion": PLUGIN_VERSION,
        "certId": meta["certId"], "certName": meta["certName"], "certShortName": meta["certShortName"],
        "packSource": meta.get("packSource", "curated"), "packVersion": meta.get("packVersion"),
        "examGuide": {"version": meta["examGuide"].get("version"), "url": meta["examGuide"]["url"],
                      "sections": meta["examGuide"]["sections"]},
        "path": {"url": meta["path"]["url"], "title": meta["path"]["title"], "providers": meta["path"].get("providers", {})},
        "mode": a.mode, "difficulty": a.difficulty, "language": a.language, "ui": {},
        "paceHoursPerWeek": a.pace, "startDate": a.start_date, "examDate": a.exam_date,
        "paused": None, "pausedDaysTotal": 0, "pauseHistory": [], "lastSyncAt": now,
        "scoring": scoring, "createdAt": now, "updatedAt": now,
    }
    ops.append({"op": "set", "path": "meta/settings", "data": settings})

    def concept_doc(c, module_id):
        return {"moduleId": module_id, "order": c["order"], "title": c["title"], "docUrls": c.get("docUrls", []),
                "level": 0, "answers": 0, "correct": 0, "recent": [], "days": [], "lastReviewed": None,
                "bonus": 0, "archived": False}

    counts = {"activities": 0, "modules": 0, "concepts": 0}
    for x in acts:
        ops.append({"op": "set", "path": f"activities/{x['id']}", "data": {
            "order": x["order"], "kind": x["kind"], "title": x["title"], "hours": x.get("hours"),
            "optional": bool(x.get("optional")), "urls": x.get("urls") or {}, "archived": False}})
        counts["activities"] += 1
        for m in x["modules"]:
            c_done = m["id"] in completed_mods
            ops.append({"op": "set", "path": f"modules/{m['id']}", "data": {
                "activityId": x["id"], "order": m["order"], "title": m["title"], "sections": m.get("sections", []),
                "weight": m.get("weight", "core"), "examRelevant": bool(m.get("examRelevant", True)),
                "hours": m.get("hours"), "labs": m.get("labs", []), "completed": c_done,
                "completedAt": a.start_date if c_done else None, "archived": False}})
            counts["modules"] += 1
            for c in m["concepts"]:
                ops.append({"op": "set", "path": f"concepts/{c['id']}", "data": concept_doc(c, m["id"])})
                counts["concepts"] += 1

    if gaps.get("topics"):
        g = gaps.get("activity", {})
        ops.append({"op": "set", "path": f"activities/{g.get('id', 'gaps')}", "data": {
            "order": len(acts) + 1, "kind": "gaps", "title": g.get("title", "Exam guide gaps"),
            "hours": g.get("hoursPerTopic", 1) * len(gaps["topics"]), "optional": False, "urls": {}, "archived": False}})
        counts["activities"] += 1
        for t in gaps["topics"]:
            ops.append({"op": "set", "path": f"modules/{t['id']}", "data": {
                "activityId": g.get("id", "gaps"), "order": t["order"], "title": t["title"], "sections": t["sections"],
                "weight": t.get("weight", "core"), "examRelevant": True, "hours": g.get("hoursPerTopic", 1),
                "labs": [], "completed": False, "completedAt": None, "archived": False}})
            counts["modules"] += 1
            for c in t["concepts"]:
                ops.append({"op": "set", "path": f"concepts/{c['id']}", "data": concept_doc(c, t["id"])})
                counts["concepts"] += 1

    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    for old in out.glob("batch-*.json"):
        old.unlink()
    batches = [ops[i:i + BATCH_SIZE] for i in range(0, len(ops), BATCH_SIZE)]
    for i, b in enumerate(batches, 1):
        (out / f"batch-{i:02d}.json").write_text(json.dumps(b, ensure_ascii=False, indent=1), encoding="utf-8")

    template = pathlib.Path(a.template) if a.template else pathlib.Path(__file__).resolve().parent.parent / "assets" / "tracker.html"
    (out / "ui-strings-en.json").write_text(json.dumps(ui_strings(template), ensure_ascii=False, indent=1), encoding="utf-8")

    plan = estimate_plan(acts, gaps, completed_mods, a.mode, a.pace, a.start_date, a.exam_date, scoring)
    summary = {"batches": len(batches), "operations": len(ops), "counts": counts,
               "completedModules": sorted(completed_mods), "title": f"{meta['certShortName']} Cert Coach",
               "trackerLine": f"GCP Cert Coach tracker: <artifact URL> (certification: {meta['certId']})",
               "skillsLine": SKILLS_LINE, "plan": plan}
    (out / "summary.json").write_text(json.dumps(summary, indent=1), encoding="utf-8")
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
