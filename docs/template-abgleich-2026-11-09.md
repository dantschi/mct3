# Template-Abgleich vom 9. November 2026

## Herkunft und Umfang

Quelle: [dantschi/dhbw-quarto-template](https://github.com/dantschi/dhbw-quarto-template).
MCT3 wurde mit Initial-Commit `a86c1323f52162bf5c451d64f89158112d554e41`
vom 24. Juli 2026 abgeleitet. Dessen Git-Tree ist exakt identisch mit dem
Template-Stand `efd484e` (Tree `a9db2c1ea636a01d1321eadb409125c92e5bc90e`).
Die Basis wurde damit über den Dateiinhalt und nicht allein über das Datum bestimmt.

Übernommen wurde der Netto-Änderungsstand bis einschließlich
`578e3da2f55d82325007576e2a3043f4070dc85d` vom 7. November 2026.
Der untersuchte Bereich enthält 13 Commits einschließlich eines Merge-Commits:

| Commit | Änderung im Template |
|--------|----------------------|
| [9170284](https://github.com/dantschi/dhbw-quarto-template/commit/9170284) | Adopt MCT1-style Pages layout and port EZS template tooling. |
| [e589324](https://github.com/dantschi/dhbw-quarto-template/commit/e589324) | Keep handout slide boxes on one page. |
| [a1654f3](https://github.com/dantschi/dhbw-quarto-template/commit/a1654f3) | Require complete speaker notes for every lecture slide. |
| [9f73831](https://github.com/dantschi/dhbw-quarto-template/commit/9f73831) | Add quizacademy CSV conventions as a Cursor rule. |
| [4398e10](https://github.com/dantschi/dhbw-quarto-template/commit/4398e10) | Migrate AI teaching rules to AGENTS.md and add subject guidance |
| [413275d](https://github.com/dantschi/dhbw-quarto-template/commit/413275d) | Merge pull request #1 from dantschi/work |
| [ddc8350](https://github.com/dantschi/dhbw-quarto-template/commit/ddc8350) | Unify cloud and CI toolchains and require complete material builds |
| [8eec6c3](https://github.com/dantschi/dhbw-quarto-template/commit/8eec6c3) | Add teaching workflow skills and document their usage |
| [be1a8f6](https://github.com/dantschi/dhbw-quarto-template/commit/be1a8f6) | Add verified starter-code packages for programming labs |
| [6a4bf0c](https://github.com/dantschi/dhbw-quarto-template/commit/6a4bf0c) | Keep terminology consistent across teaching materials |
| [ed1aad3](https://github.com/dantschi/dhbw-quarto-template/commit/ed1aad3) | Strengthen understanding and exam preparation in task design |
| [144b88c](https://github.com/dantschi/dhbw-quarto-template/commit/144b88c) | Start each lecture with an activating prior-knowledge question |
| [578e3da](https://github.com/dantschi/dhbw-quarto-template/commit/578e3da) | Separate template guide from course homepage in README |

## Übernahme in MCT3

- Gemeinsame versionsgebundene Toolchain, Aktivierung, vollständiger Materialbuild,
  Programmierpaketprüfung und die zugehörigen Tests übernommen.
- CI auf denselben Build umgestellt: Pull Requests prüfen alle Ausgaben;
  Veröffentlichung auf `gh-pages` erst nach erfolgreichem Build, ohne erneutes Rendern.
- `build_slides.sh`, `build_handouts.sh` und `build_labs.sh` an die gemeinsame
  Pipeline angebunden. Die neun Vorlesungen, neun Übungsblätter und Probeklausur
  bleiben in der Quellenauswahl enthalten.
- Livefigures einschließlich Schriften und Renderer übernommen und in Quarto
  sowie im PDF-Handout aktiviert. Website- und Handout-Änderungen abgeglichen.
  Unteilbare Folienkarten waren in MCT3 bereits vorhanden.
- Autorenregeln von Cursor nach `AGENTS.md` und Bereichsregeln migriert;
  Fachregeln, sechs Autoren-Skills, Quizvalidator und Kursglossar ergänzt.
  Literatur, Zielgruppe und Werkzeugbezüge an MCT3 angepasst.
- README mit Kursrahmen, Lernzielen, Glossar und Autoren-/Build-Verweisen ergänzt;
  Homepage auf die aktuelle Template-Konfiguration umgestellt. Die technische
  Anleitung steht separat in `TEMPLATE.md`.
- `labs/lab_template.qmd` übernommen. Die generischen Kickoff- und Python-Beispiele
  samt Startcode, Referenzlösung, Tests und Manifest liegen unverändert unter
  `examples/template/`. Sie werden nicht als neue MCT3-Einheit veröffentlicht.

Erhalten bleiben alle fachlichen Vorlesungs-, Übungs- und Quizdateien,
MCT3-Titel, URLs, Literatur und Code-Highlighting sowie die größeren
MCT3-Handoutgrafiken. Die Template-Regeln für aktivierende Einstiegsfragen,
Begriffsgebrauch und Transferaufgaben sind übernommen; eine erneute fachliche
Gesamtüberarbeitung der neun Einheiten war nicht Gegenstand dieses Abgleichs.
Die fremde generische Kickoff-Frage ersetzt daher keine vorhandene Kursfolie.

## Tatsächlich ausgeführte Prüfungen

- `python3 -m unittest discover -s tests -v`: 49 Tests bestanden, keine übersprungen.
- Alle neun bestehenden Quiz-CSV-Dateien mit je zehn Fragen strukturell validiert;
  ihre Inhalte bleiben unverändert.
- Das ausgelagerte Python-Beispiel mit Python 3.12.14 geprüft: erwarteter
  Starterzustand, vollständige Referenzlösung und erneut entpacktes Startcode-ZIP.
  Das ZIP enthält genau die drei freigegebenen Dateien, keine Referenzlösung.
- Shellsyntax, YAML-Konfiguration, acht JavaScriptmodule der Extension,
  Bytegleichheit der übernommenen Extension-Dateien und lokale Dokumentverweise geprüft.
- `git diff --check` für die angepassten Dateien ohne Fehler. Leerzeichen am
  Zeilenende im unverändert übernommenen Renderer-Bundle und im originalen
  Kickoff-Beispiel bleiben zur Bytegleichheit mit Upstream erhalten.
  Untersuchte Upstream-Dateien sind übernommen,
  kursbezogen angepasst, bereits vorhanden oder ausdrücklich als Beispiele ausgelagert.

## Offene Build-Prüfung

`bash scripts/setup.sh` scheiterte beim Download mit HTTP 403. Der angeforderte
Wiederholungsversuch außerhalb der Sandbox wurde abgebrochen. Die neue gepinnte
Toolchain ist deshalb in dieser Cloud-Umgebung nicht vollständig eingerichtet;
`python3 scripts/build-materials.py all` wurde nicht ausgeführt. Es wird kein
Erfolg für HTML-/PDF-Rendering, eine Sichtprüfung frischer Ausgaben oder einen
GitHub-Actions-Lauf behauptet. Vorhandene ältere Builddateien sind kein Nachweis.

Der Commit und Push erfolgen auf ausdrücklichen Nutzerauftrag. Die CI gibt
fertige Kursmaterialien weiterhin erst nach erfolgreichem vollständigem Build
zur Veröffentlichung frei. Für den nächsten Template-Abgleich ist
`578e3da2f55d82325007576e2a3043f4070dc85d` der hier berücksichtigte Ausgangsstand.
