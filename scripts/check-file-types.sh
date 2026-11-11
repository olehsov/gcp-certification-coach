#!/usr/bin/env bash
# Directory file-type gate for the plugin folder (plugins/gcp-cert-coach).
# The Claude directory accepts only Markdown, plain text, JSON, YAML and PNG/JPEG/GIF/WebP/ICO images from
# non-verified publishers, detected by content (not by name). It also rejects files that start with "#!",
# package-manager config files, and text that is not UTF-8 or contains NUL bytes.
#
#   scripts/check-file-types.sh              # check; exit 1 on any finding
#   scripts/check-file-types.sh --inventory  # also print a table: file, libmagic, Magika, status
#   scripts/check-file-types.sh --require-magika   # fail (instead of warn) when Magika is not installed (CI)
#
# Detectors: libmagic via `file --mime-type` (always) and Magika (pip install magika==1.0.3; python module or CLI).
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT"
exec "${PYTHON:-python3}" - "$@" <<'PY'
import os, subprocess, sys, pathlib, shutil, json

DIR = pathlib.Path("plugins/gcp-cert-coach")
args = set(sys.argv[1:])
inventory, require_magika = "--inventory" in args, "--require-magika" in args

MIME_OK = {"text/plain", "application/json", "image/png", "image/jpeg", "image/gif", "image/webp",
           "image/vnd.microsoft.icon", "image/x-icon"}
LABEL_OK = {"markdown", "txt", "json", "yaml", "png", "jpeg", "gif", "webp", "ico"}
EXT_OK = {".md", ".txt", ".json", ".yaml", ".yml", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico"}
NO_EXT_OK = {"LICENSE"}
PKG_NAMES = {"package.json", "package-lock.json", "npm-shrinkwrap.json", "yarn.lock", "pnpm-lock.yaml", ".npmrc",
             ".yarnrc", ".yarnrc.yml", "pyproject.toml", "setup.py", "setup.cfg", "pipfile", "pipfile.lock",
             "poetry.lock", "uv.lock", "gemfile", "gemfile.lock", "go.mod", "go.sum", "cargo.toml", "cargo.lock",
             "composer.json", "composer.lock", "pom.xml", "build.gradle", "mix.exs", "pubspec.yaml", "bun.lockb"}
TEXT_MIME = {"text/plain", "application/json"}

files = sorted(p for p in DIR.rglob("*") if p.is_file() or p.is_symlink())

mk = None
try:
    from magika import Magika
    mk = Magika()
    def magika_label(p):
        r = mk.identify_path(p)
        o = getattr(r, "output", None) or r.prediction.output
        return o.label
except ImportError:
    if shutil.which("magika"):
        def magika_label(p):
            out = subprocess.run(["magika", "--json", str(p)], capture_output=True, text=True).stdout
            r = json.loads(out)[0]["result"]["value"]["output"]
            return r["label"]
        mk = True
if mk is None:
    msg = "check-file-types: Magika is not installed (pip install magika==1.0.3); only libmagic was checked"
    if require_magika:
        print(msg.replace("only libmagic was checked", "required"), file=sys.stderr); sys.exit(1)
    print("WARNING: " + msg, file=sys.stderr)

problems, rows = [], []
for p in files:
    rel = str(p.relative_to(DIR)); reasons = []
    if p.is_symlink():
        rows.append((rel, "symlink", "-", ["symlink"])); problems.append(f"{rel}: symlink"); continue
    mime = subprocess.run(["file", "-b", "--mime-type", str(p)], capture_output=True, text=True).stdout.strip()
    label = magika_label(p) if mk is not None else "-"
    ext = p.suffix.lower()
    if mime not in MIME_OK: reasons.append(f"libmagic says {mime}")
    if mk is not None and label not in LABEL_OK: reasons.append(f"Magika says {label}")
    if ext not in EXT_OK and not (ext == "" and p.name in NO_EXT_OK): reasons.append(f"extension {ext or '(none)'} not allowed")
    if p.name.lower() in PKG_NAMES: reasons.append("package-manager config file")
    data = p.read_bytes()
    if data.startswith(b"#!"): reasons.append("starts with #!")
    if mime in TEXT_MIME or ext in {".md", ".txt", ".json", ".yaml", ".yml"}:
        if b"\x00" in data: reasons.append("contains NUL byte")
        try: data.decode("utf-8")
        except UnicodeDecodeError: reasons.append("not valid UTF-8")
    rows.append((rel, mime, label, reasons))
    problems += [f"{rel}: {r}" for r in reasons]

if inventory:
    w = max(len(r[0]) for r in rows)
    print(f"{'file'.ljust(w)}  {'libmagic'.ljust(24)} {'Magika'.ljust(10)} status")
    for rel, mime, label, reasons in rows:
        print(f"{rel.ljust(w)}  {mime.ljust(24)} {label.ljust(10)} {'ok' if not reasons else 'NOT ALLOWED: ' + '; '.join(reasons)}")
    print(f"{len(rows)} files")
if problems:
    print("check-file-types: FAILED", file=sys.stderr)
    for x in problems: print("  " + x, file=sys.stderr)
    sys.exit(1)
print(f"check-file-types: ok ({len(rows)} files, all Markdown, text, JSON, YAML or PNG)")
PY
