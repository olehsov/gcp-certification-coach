#!/usr/bin/env bash
# Checks that duplicated skill files stay identical and that version numbers agree.
# Skills are self-contained (ADR 0006), so a few files exist in two skill folders on purpose.
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT"
P=plugins/gcp-cert-coach
fail=0
same() { if ! cmp -s "$1" "$2"; then echo "check-consistency: $1 and $2 differ: edit the template in init and copy it to rebuild"; fail=1; fi; }
same $P/skills/init/assets/tracker.html $P/skills/rebuild/assets/tracker.html
# The browser check is shared by init and progress; only the cross-reference line differs.
if ! diff <(sed 3d $P/skills/init/references/browser-progress-check.md) <(sed 3d $P/skills/progress/references/browser-progress-check.md) >/dev/null; then
  echo "check-consistency: browser-progress-check.md differs between init and progress"; fail=1
fi
v_manifest=$(python3 -c "import json;print(json.load(open('$P/.claude-plugin/plugin.json'))['version'])")
v_market=$(python3 -c "import json;print([p for p in json.load(open('.claude-plugin/marketplace.json'))['plugins'] if p['name']=='gcp-cert-coach'][0].get('version',''))")
v_seed=$(sed -n 's/^PLUGIN_VERSION = "\([^"]*\)".*/\1/p' $P/skills/init/scripts/build_seed.py)
v_page=$(sed -n 's/^const PLUGIN_VERSION = "\([^"]*\)".*/\1/p' $P/skills/init/assets/tracker.html)
for v in "$v_market" "$v_seed" "$v_page"; do
  if [ "$v" != "$v_manifest" ]; then echo "check-consistency: version mismatch (plugin.json $v_manifest, marketplace $v_market, build_seed $v_seed, tracker $v_page)"; fail=1; break; fi
done
[ "$fail" = 0 ] && echo "check-consistency: ok (version $v_manifest)"
exit "$fail"
