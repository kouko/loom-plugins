#!/usr/bin/env bash
# mermaid-validator-negative.sh
#
# A5 negative (known-bad-arrow-block-rejected): the Mermaid validator at
# loom-workflow/tests/mermaid/validate_mermaid.mjs must exit 1 on a
# markdown file whose mermaid block uses the invalid `A -> B` arrow, and
# name that block in a FAIL line. A validator that exits 0 here parses
# nothing, so the positive run over the real templates would prove nothing.
#
# No skip path: the workflow-mermaid group of scripts/run_package_tests.py
# runs this after `npm ci`, so node_modules is present. The name does not
# match the workflow-shell group's test-*.sh glob, which runs without node.
#
# Usage:
#   bash loom-workflow/tests/mermaid-validator-negative.sh

set -u

WORKFLOW_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PROJECT="$WORKFLOW_DIR/tests/mermaid"
VALIDATOR="$PROJECT/validate_mermaid.mjs"

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
