#!/usr/bin/env python3
"""Generate the data files shipped in the plugin from repository-level sources.

The plugin folder may only hold Markdown, text, JSON, YAML and images (directory rules), so the tracker
page and the ACE seed are shipped as JSON, generated here (never edited by hand):

  templates/tracker.html  ->  skills/init/assets/tracker-template.json
                              skills/rebuild/assets/tracker-template.json   (byte-identical copies)
  the ACE pack YAML (skills/init/assets/packs/ace/*.yaml)
                          ->  skills/init/assets/packs/ace/seed/batch-NN.json, ui-strings-en.json, summary.json

Usage:  python3 scripts/build-plugin-data.py [--out-root DIR]   (needs PyYAML; --out-root defaults to the repo root)
        scripts/check-consistency.sh runs it into a temp dir and diffs the result against the shipped files.
"""
import argparse
import json
import pathlib
import re
import sys

try:
    import yaml
except ImportError:
    sys.exit("build-plugin-data: PyYAML is missing (pip install pyyaml)")

ROOT = pathlib.Path(__file__).resolve().parent.parent
PLUGIN = pathlib.Path("plugins/gcp-cert-coach/skills")
PACK = PLUGIN / "init/assets/packs/ace"
SCHEMA_VERSION = 1
BATCH_SIZE = 50  # ARCHITECTURE 5.1: writes in batches of at most 50
SKILLS_LINE = "In this Project, use the gcp-cert-coach skills for every study request (explanations, quizzes, challenges, mock exams, progress)."


def dump(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=1) + "\n"


def ui_strings(src: str) -> dict:
    start = src.index("const EN = {")
    block = src[start: src.index("};", start)]
    return {k: json.loads('"' + v + '"') for k, v in re.findall(r'(\w+):"((?:[^"\\]|\\.)*)"', block)}


def build_seed(pack_dir: pathlib.Path, version: str) -> tuple[list, dict]:
    read = lambda n: yaml.safe_load((pack_dir / n).read_text(encoding="utf-8"))  # noqa: E731
    meta, path, gaps, scoring = read("pack.yaml"), read("path.yaml"), read("gaps.yaml") or {}, read("scoring.yaml")
    acts = path["activities"]
    ops = [{"op": "set", "path": "meta/settings", "data": {
        "schemaVersion": SCHEMA_VERSION, "pluginVersion": version, "templateVersion": version,
        "latestPluginVersion": version,
        "certId": meta["certId"], "certName": meta["certName"], "certShortName": meta["certShortName"],
        "packSource": meta.get("packSource", "curated"), "packVersion": meta.get("packVersion"),
        "examGuide": {"version": meta["examGuide"].get("version"), "url": meta["examGuide"]["url"],
                      "sections": meta["examGuide"]["sections"]},
        "path": {"url": meta["path"]["url"], "title": meta["path"]["title"],
                 "providers": meta["path"].get("providers", {})},
        "mode": "course", "difficulty": "standard", "language": "en", "ui": {},
        "paceHoursPerWeek": 7, "startDate": None, "examDate": None,
        "paused": None, "pausedDaysTotal": 0, "pauseHistory": [], "lastSyncAt": None,
        "scoring": scoring, "createdAt": None, "updatedAt": None}}]

    def concept(c, module_id):
        return {"op": "set", "path": f"concepts/{c['id']}", "data": {
            "moduleId": module_id, "order": c["order"], "title": c["title"], "docUrls": c.get("docUrls", []),
            "level": 0, "answers": 0, "correct": 0, "recent": [], "days": [], "lastReviewed": None,
            "bonus": 0, "archived": False}}

    counts = {"activities": 0, "modules": 0, "concepts": 0}
    plan_modules = {}  # resolved hours of each module of a required (non-optional) activity
    required_course = 0.0
    for x in acts:
        ops.append({"op": "set", "path": f"activities/{x['id']}", "data": {
            "order": x["order"], "kind": x["kind"], "title": x["title"], "hours": x.get("hours"),
            "optional": bool(x.get("optional")), "urls": x.get("urls") or {}, "archived": False}})
        counts["activities"] += 1
        mods = x["modules"]
        if not x.get("optional"):
            required_course += x.get("hours") or 0
        for m in mods:
            ops.append({"op": "set", "path": f"modules/{m['id']}", "data": {
                "activityId": x["id"], "order": m["order"], "title": m["title"], "sections": m.get("sections", []),
                "weight": m.get("weight", "core"), "examRelevant": bool(m.get("examRelevant", True)),
                "hours": m.get("hours"), "labs": m.get("labs", []), "completed": False,
                "completedAt": None, "archived": False}})
            counts["modules"] += 1
            if not x.get("optional"):
                h = m["hours"] if m.get("hours") is not None else ((x.get("hours") or 0) / len(mods) if mods else 0)
                plan_modules[m["id"]] = round(h, 4)
            for c in m["concepts"]:
                ops.append(concept(c, m["id"]))
                counts["concepts"] += 1
    gap_topics, gap_per = 0, 1
    if gaps.get("topics"):
        g = gaps.get("activity", {})
        gap_per = g.get("hoursPerTopic", scoring.get("plan", {}).get("gapHoursPerTopic", 1))
        gap_topics = len(gaps["topics"])
        ops.append({"op": "set", "path": f"activities/{g.get('id', 'gaps')}", "data": {
            "order": len(acts) + 1, "kind": "gaps", "title": g.get("title", "Exam guide gaps"),
            "hours": g.get("hoursPerTopic", 1) * gap_topics, "optional": False, "urls": {}, "archived": False}})
        counts["activities"] += 1
        for t in gaps["topics"]:
            ops.append({"op": "set", "path": f"modules/{t['id']}", "data": {
                "activityId": g.get("id", "gaps"), "order": t["order"], "title": t["title"], "sections": t["sections"],
                "weight": t.get("weight", "core"), "examRelevant": True, "hours": g.get("hoursPerTopic", 1),
                "labs": [], "completed": False, "completedAt": None, "archived": False}})
            counts["modules"] += 1
            for c in t["concepts"]:
                ops.append(concept(c, t["id"]))
                counts["concepts"] += 1

    # Entries use the artifact data tool's batch shape: {op, collection, doc_id, data}.
    for o in ops:
        o["collection"], o["doc_id"] = o.pop("path").rsplit("/", 1)
        o["data"] = o.pop("data")
    pc = scoring.get("plan", {})
    summary = {
        "title": f"{meta['certShortName']} Cert Coach", "certId": meta["certId"], "pluginVersion": version,
        "operations": len(ops), "batches": -(-len(ops) // BATCH_SIZE), "counts": counts,
        "trackerLine": f"GCP Cert Coach tracker: <artifact URL> (certification: {meta['certId']})",
        "skillsLine": SKILLS_LINE,
        "planInputs": {
            "note": "Inputs for the plan estimate (references/plan-estimate.md) at setup, when nothing is logged yet.",
            "requiredCourseHours": round(required_course, 2), "gapTopics": gap_topics,
            "gapHoursPerTopic": gap_per, "practiceBufferFraction": pc.get("practiceBufferFraction", 0.2),
            "moduleHours": plan_modules}}
    return ops, summary


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out-root", default=str(ROOT))
    out_root = pathlib.Path(ap.parse_args().out_root)

    src = (ROOT / "templates/tracker.html").read_text(encoding="utf-8")
    m = re.search(r'^const PLUGIN_VERSION = "([^"]+)"', src, re.M)
    if not m:
        sys.exit("build-plugin-data: PLUGIN_VERSION not found in templates/tracker.html")
    version = m.group(1)

    template = dump({"format": "tracker-template", "version": version, "lines": src.split("\n")})
    for skill in ("init", "rebuild"):
        p = out_root / PLUGIN / skill / "assets/tracker-template.json"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(template, encoding="utf-8")

    ops, summary = build_seed(ROOT / PACK, version)
    seed = out_root / PACK / "seed"
    seed.mkdir(parents=True, exist_ok=True)
    for old in seed.glob("*.json"):
        old.unlink()
    for i in range(0, len(ops), BATCH_SIZE):
        (seed / f"batch-{i // BATCH_SIZE + 1:02d}.json").write_text(dump(ops[i:i + BATCH_SIZE]), encoding="utf-8")
    (seed / "ui-strings-en.json").write_text(dump(ui_strings(src)), encoding="utf-8")
    (seed / "summary.json").write_text(dump(summary), encoding="utf-8")
    print(f"build-plugin-data: version {version}, {len(ops)} writes in {summary['batches']} batches, counts {summary['counts']}")


if __name__ == "__main__":
    main()
