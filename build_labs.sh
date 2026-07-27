#!/bin/bash
set -eu

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

OUT_DIR="labs/_output"
mkdir -p "$OUT_DIR"

# Alte Doppel-Suffix-Artefakte und veraltete Kopien entfernen
rm -f "$OUT_DIR"/*-musterloesung-musterloesung.pdf \
      "$OUT_DIR"/*-musterloesung-studierende.pdf \
      "$OUT_DIR"/*-studierende-studierende.pdf 2>/dev/null || true

# Veraltete Musterlösungs-PDFs in labs/ (Labs 1–3) entfernen —
# sonst werden sie beim Kopieren mit doppeltem Suffix erfasst.
rm -f labs/lab_*-musterloesung.pdf labs/probeklausur-musterloesung.pdf 2>/dev/null || true

echo "Baue Studierenden-Versionen (ohne Lösungen)..."
quarto render labs/ --to pdf

for pdf in labs/lab_[0-9][0-9]_*.pdf labs/probeklausur.pdf; do
  [ -f "$pdf" ] || continue
  case "$pdf" in
    *-musterloesung.pdf|*-studierende.pdf) continue ;;
  esac
  base="$(basename "$pdf" .pdf)"
  cp "$pdf" "$OUT_DIR/${base}-studierende.pdf"
  # Für die Website/README: Studierenden-PDF auch unter dem Basisnamen belassen
done

echo "Baue Dozenten-Versionen (mit Lösungen)..."
quarto render labs/ --to pdf --profile solution

for pdf in labs/lab_[0-9][0-9]_*.pdf labs/probeklausur.pdf; do
  [ -f "$pdf" ] || continue
  case "$pdf" in
    *-musterloesung.pdf|*-studierende.pdf) continue ;;
  esac
  base="$(basename "$pdf" .pdf)"
  cp "$pdf" "$OUT_DIR/${base}-musterloesung.pdf"
done

# Studierenden-Versionen zurück nach labs/ (CI/README erwartet Basisnamen ohne Lösung)
echo "Stelle Studierenden-PDFs in labs/ wieder her..."
for stud in "$OUT_DIR"/*-studierende.pdf; do
  [ -f "$stud" ] || continue
  base="$(basename "$stud" -studierende.pdf)"
  cp "$stud" "labs/${base}.pdf"
done

# Veraltete ungesuffixed Kopien in _output entfernen (nur -studierende/-musterloesung behalten)
for pdf in "$OUT_DIR"/lab_*.pdf "$OUT_DIR"/probeklausur.pdf; do
  [ -f "$pdf" ] || continue
  case "$(basename "$pdf")" in
    *-studierende.pdf|*-musterloesung.pdf) ;;
    *) rm -f "$pdf" ;;
  esac
done

echo "Fertig. PDFs unter $OUT_DIR:"
ls -la "$OUT_DIR"
