#!/bin/bash
set -eu
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
failed=0
for qmd in vorlesungen/*.qmd; do
  echo "=== HANDOUT: $qmd ==="
  if ! quarto render "$qmd" --profile handout --to pdf; then
    echo "FAILED: $qmd"
    failed=1
  fi
done
echo "HAND_OUT_DONE failed=$failed"
exit "$failed"
