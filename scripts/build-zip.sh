#!/usr/bin/env bash
# Build the upload zip for claude.ai (Customize → Plugins → Add → Upload plugin).
# The archive holds one top-level folder, gcp-cert-coach/, with .claude-plugin/plugin.json inside it,
# and excludes OS files that the plugin directory rejects. Output: dist/gcp-cert-coach-<version>.zip
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT/plugins"
VERSION="$(python3 -c 'import json;print(json.load(open("gcp-cert-coach/.claude-plugin/plugin.json"))["version"])')"
OUT="$ROOT/dist/gcp-cert-coach-$VERSION.zip"
mkdir -p "$ROOT/dist" && rm -f "$OUT"
zip -qr -X "$OUT" gcp-cert-coach -x '*.DS_Store' '*Thumbs.db' '*desktop.ini' '*__MACOSX*'
count="$(unzip -Z1 "$OUT" | grep -c 'gcp-cert-coach/.claude-plugin/plugin.json$')"
[ "$count" = "1" ] || { echo "build-zip: expected exactly one plugin.json, found $count" >&2; exit 1; }
if unzip -Z1 "$OUT" | grep -v '^gcp-cert-coach/' | grep -q .; then
  echo "build-zip: entries outside gcp-cert-coach/" >&2; exit 1
fi
echo "build-zip: $OUT ($(unzip -Z1 "$OUT" | grep -vc '/$') files)"
