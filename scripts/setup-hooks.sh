#!/usr/bin/env bash
# One-time setup for a clone: enable the repository's native git hooks. Safe to run again.
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"
chmod +x .githooks/* scripts/*.sh
if [ "$(git config --get core.hooksPath || true)" = ".githooks" ]; then
  echo "setup-hooks: core.hooksPath already set to .githooks"
else
  git config core.hooksPath .githooks
  echo "setup-hooks: core.hooksPath set to .githooks"
fi
command -v gitleaks >/dev/null 2>&1 \
  && echo "setup-hooks: gitleaks found ($(gitleaks version 2>/dev/null))" \
  || echo "setup-hooks: gitleaks not installed; hooks will skip it (install: brew install gitleaks)"
DENY="${GCP_CERT_COACH_DENYLIST:-$HOME/.config/gcp-cert-coach/denylist.txt}"
[ -f "$DENY" ] \
  && echo "setup-hooks: personal denylist found (contents not shown)" \
  || echo "setup-hooks: optional personal denylist not found at $DENY (one term per line; never commit it)"
