#!/bin/bash
set -eu
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
failed=0
for qmd in vorlesungen/*.qmd; do
  echo "=== FOLIEN: $qmd ==="
  if ! quarto render "$qmd" --to revealjs; then
    echo "FAILED slides: $qmd"
    failed=1
  fi
done
echo "SLIDES_DONE failed=$failed"
exit "$failed"
