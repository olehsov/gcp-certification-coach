#!/usr/bin/env bash
# Privacy check for the gcp-certification-coach repository.
#
# Usage:
#   scripts/check-privacy.sh              # tracked + untracked (not ignored) files in the working tree
#   scripts/check-privacy.sh --staged     # staged content only (used by .githooks/pre-commit)
#   scripts/check-privacy.sh --tracked    # all tracked files (used by .githooks/pre-push and CI)
#   scripts/check-privacy.sh --history    # every blob in every commit (one-off scan before publishing)
#   scripts/check-privacy.sh FILE...      # the given files
#
# Checks generic patterns (emails, claude.ai artifact URLs, Google Cloud project-id and
# billing-account patterns, API keys and tokens, lab accounts, non-English text inside
# plugins/) plus a personal denylist read from ~/.config/gcp-cert-coach/denylist.txt when
# that file exists (override the path with GCP_CERT_COACH_DENYLIST). The denylist lives
# outside the repository; its terms and the matching line text are never printed.
#
# False positives: add a narrowly scoped rule to scripts/privacy-allowlist.txt.
# Exit codes: 0 clean, 1 findings, 2 usage or environment error.
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null)" || { echo "check-privacy: not inside a git repository" >&2; exit 2; }
command -v python3 >/dev/null 2>&1 || { echo "check-privacy: python3 is required" >&2; exit 2; }
cd "$ROOT"

exec python3 -I - "$@" <<'PY'
import fnmatch, os, re, subprocess, sys, unicodedata

ALLOWLIST_FILE = "scripts/privacy-allowlist.txt"
DENYLIST_FILE = os.environ.get(
    "GCP_CERT_COACH_DENYLIST",
    os.path.expanduser("~/.config/gcp-cert-coach/denylist.txt"),
)

# Pattern name -> regex. Some literals are split so this file does not match itself.
PATTERNS = {
    "email address": r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}",
    "claude.ai artifact URL": r"claude\.(?:ai|site)/(?:code/)?(?:public/)?artifacts?/[A-Za-z0-9-]{6,}",
    "lab account or lab project": r"qwiklabs-gcp-[0-9a-z-]+|student[-_][0-9a-z-]+@qwiklabs\.net",
    "Google Cloud project id": (
        r"(?:--project[= ]|projects/|project[_-]?id[\"']?\s*[:=]\s*[\"']?)"
        r"(?!PROJECT|YOUR|\{|<|\$)([a-z][a-z0-9-]{4,28}[a-z0-9])\b"
    ),
    "billing account id": r"\b[0-9A-F]{6}-[0-9A-F]{6}-[0-9A-F]{6}\b",
    "Google API key": r"AIza[0-9A-Za-z_-]{35}",
    "Google OAuth token": r"ya29\.[0-9A-Za-z_-]{20,}",
    "Anthropic API key": r"sk-ant-[A-Za-z0-9_-]{20,}",
    "GitHub token": r"\bgh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,}",
    "AWS access key": r"\bAKIA[0-9A-Z]{16}\b",
    "Slack token": r"\bxox[abprs]-[A-Za-z0-9-]{10,}",
    "private key": "-----BEGIN [A-Z ]*" + "PRIVATE KEY-----",
    "service account key file": r"\"private_key_id\"\s*:\s*\"[0-9a-f]{20,}",
}
COMPILED = {k: re.compile(v) for k, v in PATTERNS.items()}

# Non-English text check applies to what users install (skills, templates, packs).
LANGUAGE_SCOPE = ("plugins/",)

def load_allowlist():
    rules = []
    if not os.path.exists(ALLOWLIST_FILE):
        return rules
    with open(ALLOWLIST_FILE, encoding="utf-8") as fh:
        for n, raw in enumerate(fh, 1):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            glob, sep, rx = line.partition("::")
            if not sep:
                glob, rx = "*", line
            try:
                rules.append((glob.strip(), re.compile(rx.strip())))
            except re.error as e:
                print(f"check-privacy: bad allowlist rule at {ALLOWLIST_FILE}:{n}: {e}", file=sys.stderr)
                sys.exit(2)
    return rules

def load_denylist():
    if not os.path.isfile(DENYLIST_FILE):
        return []
    terms = []
    with open(DENYLIST_FILE, encoding="utf-8", errors="replace") as fh:
        for raw in fh:
            t = raw.strip()
            if t and not t.startswith("#") and len(t) >= 3:
                terms.append(t.casefold())
    return terms

ALLOW = load_allowlist()
DENY = load_denylist()

# The repository owner's public GitHub handle is allowed in the manifests, license files and
# GitHub URLs (CLAUDE.md -> Privacy). It is masked there before denylist matching, so a denylist
# term that happens to be a substring of the handle does not flag it. Elsewhere it is not masked.
HANDLE_FILES = {
    ".claude-plugin/marketplace.json",
    "plugins/gcp-cert-coach/.claude-plugin/plugin.json",
    "LICENSE", "LICENSE-CONTENT", "plugins/gcp-cert-coach/LICENSE",
    "(commit metadata)",  # commit author identity is the owner handle + noreply address
}

def load_handle():
    try:
        import json
        with open("plugins/gcp-cert-coach/.claude-plugin/plugin.json", encoding="utf-8") as fh:
            name = json.load(fh).get("author", {}).get("name", "")
        return name if re.fullmatch(r"[A-Za-z0-9-]{2,39}", name or "") else ""
    except (OSError, ValueError):
        return ""

HANDLE = load_handle()
HANDLE_URL_RX = re.compile(r"github\.com/" + re.escape(HANDLE) + r"\b", re.I) if HANDLE else None
HANDLE_RX = re.compile(r"\b" + re.escape(HANDLE) + r"\b", re.I) if HANDLE else None

def mask_handle(path, line):
    if not HANDLE:
        return line
    line = HANDLE_URL_RX.sub(lambda m: " " * len(m.group(0)), line)
    if path in HANDLE_FILES:
        line = HANDLE_RX.sub(lambda m: " " * len(m.group(0)), line)
    return line

def allowed(path, text):
    return any(fnmatch.fnmatch(path, g) and rx.search(text) for g, rx in ALLOW)

def git(*args, binary=False):
    out = subprocess.run(["git", *args], check=True, capture_output=True).stdout
    return out if binary else out.decode("utf-8", "replace")

def is_binary(data):
    return b"\0" in data[:8192]

def foreign_letter(ch):
    # Letters beyond Latin Extended-B (Cyrillic, Greek, CJK, Arabic, ...).
    return ord(ch) > 0x24F and unicodedata.category(ch).startswith("L")

findings = 0

def report(path, lineno, what):
    global findings
    findings += 1
    print(f"  {path}:{lineno}: {what}")

def scan(path, data):
    if path == ALLOWLIST_FILE or is_binary(data):
        return
    text = data.decode("utf-8", "replace")
    check_lang = path.startswith(LANGUAGE_SCOPE)
    for lineno, line in enumerate(text.splitlines(), 1):
        for name, rx in COMPILED.items():
            for m in rx.finditer(line):
                if not allowed(path, m.group(0)):
                    report(path, lineno, name)
                    break
        if check_lang and any(foreign_letter(c) for c in line):
            if not allowed(path, "non-English text"):
                report(path, lineno, "non-English text")
        if DENY:
            low = mask_handle(path, line).casefold()
            if any(t in low for t in DENY):
                report(path, lineno, "personal denylist term (term not shown)")

def main(argv):
    mode = argv[0] if argv else "--worktree"
    targets = []  # (path, bytes)
    if mode == "--staged":
        names = [n for n in git("diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z").split("\0") if n]
        for n in names:
            targets.append((n, git("show", f":{n}", binary=True)))
    elif mode in ("--tracked", "--worktree"):
        names = [n for n in git("ls-files", "-z").split("\0") if n]
        if mode == "--worktree":
            names += [n for n in git("ls-files", "-z", "--others", "--exclude-standard").split("\0") if n]
        for n in sorted(set(names)):
            if os.path.isfile(n) and not os.path.islink(n):
                with open(n, "rb") as fh:
                    targets.append((n, fh.read()))
    elif mode == "--history":
        seen = set()
        revs = [r for r in git("rev-list", "--all").split() if r]
        for rev in revs:
            for entry in git("ls-tree", "-r", "-z", rev).split("\0"):
                if not entry:
                    continue
                meta, path = entry.split("\t", 1)
                _, kind, sha = meta.split()
                if kind != "blob" or sha in seen:
                    continue
                seen.add(sha)
                targets.append((f"{path}@{rev[:8]}", git("cat-file", "blob", sha, binary=True)))
        # Commit metadata: author/committer identities and messages.
        meta = git("log", "--all", "--format=%H%x00%an <%ae>%x00%cn <%ce>%x00%B%x01")
        for rec in meta.split("\x01"):
            rec = rec.strip("\n")
            if not rec:
                continue
            sha, author, committer, body = (rec.split("\0") + ["", "", ""])[:4]
            text = "\n".join([author, committer, body])
            targets.append((f"(commit metadata)@{sha}", text.encode("utf-8")))
    elif mode.startswith("-"):
        print(__doc__ or "usage: check-privacy.sh [--staged|--tracked|--history|FILE...]", file=sys.stderr)
        return 2
    else:
        for n in argv:
            with open(n, "rb") as fh:
                targets.append((os.path.relpath(n), fh.read()))

    print(f"check-privacy: scanning {len(targets)} file(s) [{mode}]"
          + (f", denylist: {len(DENY)} term(s)" if DENY else ", denylist: not found"))
    for path, data in targets:
        # History paths carry @commit; strip it for allowlist and scope matching.
        scan_path = path.rsplit("@", 1)[0] if mode == "--history" else path
        before = findings
        scan(scan_path, data)
        if mode == "--history" and findings > before:
            print(f"    (in commit {path.rsplit('@', 1)[1]})")
    if findings:
        print(f"check-privacy: {findings} finding(s). Remove the data, or add a narrowly scoped, "
              f"commented rule to {ALLOWLIST_FILE} for a false positive.")
        return 1
    print("check-privacy: clean")
    return 0

sys.exit(main(sys.argv[1:]))
PY
