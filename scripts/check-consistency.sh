#!/usr/bin/env bash
# Checks that duplicated skill files stay identical and that version numbers agree.
# Skills are self-contained (ADR 0006), so a few files exist in two skill folders on purpose.
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT"
P=plugins/gcp-cert-coach
fail=0
same() { if ! cmp -s "$1" "$2"; then echo "check-consistency: $1 and $2 differ: edit the template in init and copy it to rebuild"; fail=1; fi; }
same $P/skills/init/assets/tracker-template.json $P/skills/rebuild/assets/tracker-template.json
# Generated data (template JSON and ACE seed) must equal a fresh run of the generator on templates/tracker.html and the pack YAML.
if python3 -c 'import yaml' 2>/dev/null; then
  tmp=$(mktemp -d); python3 scripts/build-plugin-data.py --out-root "$tmp" >/dev/null
  for f in skills/init/assets/tracker-template.json skills/rebuild/assets/tracker-template.json; do
    cmp -s "$tmp/$P/$f" "$P/$f" || { echo "check-consistency: $P/$f is stale: run scripts/build-plugin-data.py"; fail=1; }
  done
  if ! diff -r "$tmp/$P/skills/init/assets/packs/ace/seed" "$P/skills/init/assets/packs/ace/seed" >/dev/null; then
    echo "check-consistency: ACE seed is stale or edited by hand: run scripts/build-plugin-data.py"; fail=1
  fi
  rm -rf "$tmp"
elif [ -n "${CI:-}" ]; then echo "check-consistency: PyYAML is required in CI"; fail=1
else echo "check-consistency: WARNING PyYAML not installed, generated data not re-checked (pip install pyyaml)"; fi
# The browser check is shared by init and progress; only the cross-reference line differs.
if ! diff <(sed 3d $P/skills/init/references/browser-progress-check.md) <(sed 3d $P/skills/progress/references/browser-progress-check.md) >/dev/null; then
  echo "check-consistency: browser-progress-check.md differs between init and progress"; fail=1
fi
# Shared references: identical copies in every skill that uses them.
group() { local f="$1"; shift; local first="$1"; shift; for d in "$@"; do same "$P/skills/$first/references/$f" "$P/skills/$d/references/$f"; done; }
group snapshots.md reset sync rebuild
group plan-estimate.md progress init
group facts.md quiz learn mock challenge
group answer-parsing.md quiz mock
# The license shipped inside the plugin folder must match the root license (directory checklist).
if ! cmp -s LICENSE $P/LICENSE; then echo "check-consistency: $P/LICENSE differs from the root LICENSE"; fail=1; fi
v_manifest=$(python3 -c "import json;print(json.load(open('$P/.claude-plugin/plugin.json'))['version'])")
v_market=$(python3 -c "import json;print([p for p in json.load(open('.claude-plugin/marketplace.json'))['plugins'] if p['name']=='gcp-cert-coach'][0].get('version',''))")
v_seed=$(python3 -c "import json;print(json.load(open('$P/skills/init/assets/packs/ace/seed/summary.json'))['pluginVersion'])")
v_page=$(python3 -c "import json;print(json.load(open('$P/skills/init/assets/tracker-template.json'))['version'])")
v_src=$(sed -n 's/^const PLUGIN_VERSION = "\([^"]*\)".*/\1/p' templates/tracker.html)
for v in "$v_market" "$v_seed" "$v_page" "$v_src"; do
  if [ "$v" != "$v_manifest" ]; then echo "check-consistency: version mismatch (plugin.json $v_manifest, marketplace $v_market, seed $v_seed, template json $v_page, templates/tracker.html $v_src)"; fail=1; break; fi
done
for f in $P/skills/*/SKILL.md; do
  v=$(sed -n 's/.*Plugin version: \([0-9]*\.[0-9]*\.[0-9]*\).*/\1/p' "$f" | head -1)
  if [ -n "$v" ] && [ "$v" != "$v_manifest" ]; then echo "check-consistency: $f says plugin version $v, plugin.json says $v_manifest"; fail=1; fi
done
[ "$fail" = 0 ] && echo "check-consistency: ok (version $v_manifest)"
exit "$fail"
