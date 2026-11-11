#!/usr/bin/env python3
"""Check links in tracked Markdown and YAML files.

Relative links must point to an existing file. External http(s) links must return HTTP 200
(after redirects). Placeholder URLs (with <...>, {...}, EXAMPLE, example.com) and links to the
repository itself before it is published are skipped.

Usage: python3 scripts/check-links.py [--offline]   (--offline checks relative links only)
"""
import concurrent.futures
import pathlib
import re
import subprocess
import sys
import urllib.error
import urllib.request

ROOT = pathlib.Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip())
SKIP = re.compile(r"[<{]|EXAMPLE|example\.(com|org)|localhost|claude\.ai/(customize|directory)|github\.com/olehsov/gcp-certification-coach")
MD_LINK = re.compile(r"\]\(([^)\s]+)\)")
URL = re.compile(r"https?://[^\s)\"'<>`\]]+")


def files():
    out = subprocess.run(["git", "ls-files", "*.md", "*.yaml", "*.yml"], cwd=ROOT, capture_output=True, text=True, check=True).stdout
    return [ROOT / f for f in out.split()]


def check_url(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (link-check)"})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return url, r.status
    except urllib.error.HTTPError as e:
        return url, e.code
    except Exception as e:  # network errors are reported, not hidden
        return url, f"error: {e.__class__.__name__}"


def main():
    offline = "--offline" in sys.argv
    bad, urls = [], {}
    for f in files():
        text = f.read_text(encoding="utf-8")
        for link in MD_LINK.findall(text) if f.suffix == ".md" else []:
            if link.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = (f.parent / link.split("#")[0]).resolve()
            if not target.exists():
                bad.append(f"{f.relative_to(ROOT)}: missing relative link {link}")
        for u in URL.findall(text):
            u = u.rstrip(".,;:")
            if not SKIP.search(u):
                urls.setdefault(u, f.relative_to(ROOT))
    if not offline:
        with concurrent.futures.ThreadPoolExecutor(8) as ex:
            for url, status in ex.map(check_url, urls):
                if status != 200:
                    bad.append(f"{urls[url]}: {url} -> {status}")
    print(f"check-links: {len(urls)} external URL(s){' (not fetched)' if offline else ''}, {len(bad)} problem(s)")
    for b in bad:
        print("  " + b)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
