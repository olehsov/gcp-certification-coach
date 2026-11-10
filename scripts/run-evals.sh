#!/usr/bin/env bash
# Run the eval suite in evals/ against the plugin with `claude plugin eval`.
#
# `claude plugin eval` only accepts an eval directory inside the plugin root, while this
# repository keeps evals/ outside the plugin folder (CLAUDE.md layout rule). This wrapper stages
# a temporary copy of the plugin with evals/ inside it, runs the eval there, and copies the
# results back to evals/results/<timestamp>/ (gitignored). Reports are never published.
#
# Usage:
#   scripts/run-evals.sh [--baseline] [claude plugin eval options...]
#     --baseline   run without the plugin's skills (empty plugin, skill-fired graders removed,
#                  --ablation none) to measure the no-plugin baseline
# Examples:
#   scripts/run-evals.sh --model sonnet --runs 1 -j 4
#   scripts/run-evals.sh --tag quiz --model haiku
#   scripts/run-evals.sh --baseline --model sonnet --runs 1 -j 4
#   scripts/run-evals.sh --cases quiz-pretest,mock-verdict-hard --model haiku
#     --cases     (after --baseline, before other options) run only these case folders
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel)"
STAGE="$(mktemp -d "${TMPDIR:-/tmp}/gcp-cert-coach-eval.XXXXXX")"
trap 'rm -rf "$STAGE"' EXIT

BASELINE=0
if [ "${1:-}" = "--baseline" ]; then BASELINE=1; shift; fi
CASES=""
if [ "${1:-}" = "--cases" ]; then CASES="$2"; shift 2; fi

PLUGIN="$STAGE/gcp-cert-coach"
mkdir -p "$PLUGIN"
if [ "$BASELINE" = 1 ]; then
  mkdir -p "$PLUGIN/.claude-plugin"
  cp "$ROOT/plugins/gcp-cert-coach/.claude-plugin/plugin.json" "$PLUGIN/.claude-plugin/"
else
  cp -R "$ROOT/plugins/gcp-cert-coach/." "$PLUGIN/"
fi
rsync -a --exclude results/ "$ROOT/evals/" "$PLUGIN/evals/"
if [ -n "$CASES" ]; then
  # Keep only the named case folders (comma-separated); --case takes a single glob only.
  for d in "$PLUGIN"/evals/*/; do
    n="$(basename "$d")"
    case ",$CASES," in *",$n,"*) ;; *) if [ -f "$d/prompt.md" ]; then rm -rf "$d"; fi ;; esac
  done
fi
EXTRA=()
if [ "$BASELINE" = 1 ]; then
  find "$PLUGIN/evals" -name skill-fired.md -delete
  EXTRA+=(--ablation none)
fi

STAMP="$(date -u +%Y-%m-%dT%H-%M-%SZ)$( [ "$BASELINE" = 1 ] && echo -baseline || true )"
OUT="$ROOT/evals/results/$STAMP"
mkdir -p "$OUT"

set +e
claude plugin eval "$PLUGIN" --trust-plugin --no-publish \
  --allow-tools WebFetch WebSearch \
  --output-dir "$OUT" --report "$OUT/report.html" --json "$OUT/result.json" \
  ${EXTRA[@]+"${EXTRA[@]}"} "$@"
status=$?
set -e
echo "run-evals: results in evals/results/$STAMP (exit $status)"
exit "$status"
