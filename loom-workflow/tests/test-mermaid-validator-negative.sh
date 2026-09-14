#!/usr/bin/env bash
# test-mermaid-validator-negative.sh
#
# A5 negative (known-bad-arrow-block-rejected): the Mermaid validator at
# loom-workflow/tests/mermaid/validate_mermaid.mjs must exit 1 on a
# markdown file whose mermaid block uses the invalid `A -> B` arrow, and
# name that block in a FAIL line. A validator that exits 0 here parses
# nothing, so the positive run over the real templates would prove nothing.
#
# Skips only when the validator's node_modules is absent AND CI is unset
# (a local checkout that never ran `npm ci`); under CI the same absence
# fails instead.
#
# Usage:
#   bash loom-workflow/tests/test-mermaid-validator-negative.sh

set -u

WORKFLOW_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PROJECT="$WORKFLOW_DIR/tests/mermaid"
VALIDATOR="$PROJECT/validate_mermaid.mjs"

if [ ! -d "$PROJECT/node_modules" ]; then
  if [ -z "${CI:-}" ]; then
    echo "SKIP — $PROJECT/node_modules absent; run: npm ci --prefix loom-workflow/tests/mermaid"
    exit 0
  fi
  echo "FAIL — $PROJECT/node_modules absent under CI"
  exit 1
fi

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
BAD="$TMP/bad.md"
printf '# bad\n\n```mermaid\nflowchart TD\n    A -> B\n```\n' > "$BAD"

OUT="$(node "$VALIDATOR" "$BAD" 2>&1)"
CODE=$?

FAILS=0
if [ "$CODE" -eq 1 ]; then
  echo "PASS — validator exits 1 on the A -> B block"
else
  echo "FAIL — validator exit code $CODE, expected 1"; FAILS=$((FAILS + 1))
fi
if printf '%s\n' "$OUT" | grep -q "^FAIL $BAD:3 "; then
  echo "PASS — FAIL line names $BAD:3"
else
  echo "FAIL — no 'FAIL $BAD:3' line in output:"; printf '%s\n' "$OUT"; FAILS=$((FAILS + 1))
fi

[ "$FAILS" -eq 0 ]
