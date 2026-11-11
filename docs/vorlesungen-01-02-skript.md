# Vorlesungen 1 und 2: Gliederung und Skriptnotizen

Leichte Nachbearbeitung vom 11. November 2026. Die beiden Einheiten enthalten
jetzt jeweils 55 Folien: die bisher behandelten Inhalte und fünf zusätzliche
Abschnittsfolien. Es wurden keine zusätzlichen fachlichen Themen eingeführt.
Dateinamen, Reihenfolge der Fachthemen, Modelle, Zahlenbeispiele, Abbildungen,
vier Codeblöcke und ausgearbeitete Übungslösungen bleiben erhalten.

## Orientierung und Lerntext

| Abschnitt | Vorlesung 1 | Vorlesung 2 |
|---|---|---|
| 1 | Datenwege und Maßstäbe | Lokalität und Hierarchie |
| 2 | Nichtflüchtige Speicher | Treffer und Zugriffszeit |
| 3 | SRAM: Rückkopplung und Zugriff | Platzzuordnung und Verdrängung |
| 4 | DRAM: Ladung und Organisation | Schreibzugriffe |
| 5 | Speicherorganisation und Software | C-Zugriffsmuster |

Je 47 laufende Abschnittsmarkierungen verbinden die Fachfolien mit den
fünf Übersichten. Die gemeinsame Datei
`assets/styles/abschnittsorientierung.css` ist nur in diesen beiden Einheiten
eingebunden. Die 180-Minuten-Planung einschließlich Papierarbeit und Quiz
bleibt bestehen; die Übersichten ordnen die vorhandenen Inhalte.

Alle 110 Notizblöcke wurden als zusammenhängender Lerntext überarbeitet.
Definitionen stehen bei ihrer Einführung, spätere Absätze knüpfen daran an.
Übergänge erklären den fachlichen Zusammenhang. Rechenwege, Modellannahmen,
Grenzen und Lösungen sind weiterhin ausgearbeitet. Regieanweisungen und
instabile Foliennummerverweise sind durch fachliche Erläuterungen ersetzt.

Der Einstieg in Vorlesung 1 fragt nach erhaltenen Informationen beim
Ausschalten. Der Abschluss verbindet Flash, SRAM, `.data`, `.bss` und Startup
mit dieser Frage und unterscheidet Ausschalten von Reset. Vorlesung 2 beginnt
mit der Reihenfolge gleicher Arrayzugriffe. Der Abschluss erklärt deren
Wirkung unter den jeweils angegebenen Cache- und Zugriffsannahmen.

Drei bereits in der Ausgangsfassung überlaufende Abbildungsfolien der ersten
Einheit erhalten begrenzte Bildhöhen. Die Literatur am Schluss ist kompakter
gesetzt. Die Abbildungsdateien selbst bleiben unverändert.

## Kleine Konsistenzkorrekturen

Die Quizfolie der zweiten Einheit nennt die tatsächlich vorhandenen zehn
Fragen. Datenkapazität in Byte wird sprachlich von einem Line-Platz
unterschieden. Im Quiz 2 wurden genau zwei CSV-Zellen präzisiert:

- Frage 7: Bei 16 Vier-Byte-Stores entsprechen 64 Byte Write-Through-Verkehr
  genau einer zurückgeschriebenen 64-Byte-Line. Erst ab 17 Stores gibt
  Write-Back in diesem Modell weniger Nutzbytes weiter.
- Frage 9: Die Frage nennt nun die für die Zugriffsspur vorausgesetzten
  64-Byte-Lines. `0x2000` und `0x2004` gehören damit eindeutig zum selben Block.

Alle Fragezahlen, Antwortoptionen und Korrektmarker bleiben erhalten.
UTF-8-BOM und CRLF-Zeilenenden der hochgeladenen Quizdatei sind bewahrt.
Die bestehenden Übungsblätter benötigen keine Anpassung.

## Ausgeführte Prüfungen

- Beide vollständigen Quellen einschließlich aller 110 Notizen unabhängig
  mit den bisherigen 100 Folien und den zugehörigen Aufgaben verglichen.
  Zahlen, Modelle, Lösungen, ursprüngliche Bildverweise und Codeblöcke erhalten.
- Struktur und UTF-8 geprüft: je 55 Folien, 55 zugeordnete Notizblöcke,
  fünf Abschnittstrenner und 47 laufende Markierungen; alle Bildpfade vorhanden.
- Beide Quizdateien bestehen den CSV-Validator mit je zehn Fragen. Die zwei
  geänderten Zellen wurden unabhängig nachgerechnet und abgeglichen.
- Frische Reveal.js-Ausgaben mit der gemeinsamen Toolchain erzeugt und alle
  110 Folien in Chromium bei 1440 × 900 mit gesetzten Formeln geprüft:
  keine Überläufe, fehlenden Bilder oder falsch zugeordneten Notizen.
  Neue Übersichten, Rückbindungen und angepasste Bildfolien zusätzlich
  anhand aktueller Screenshots angesehen.
- 27 weitere geschützte QMD-/CSV-Quellen sind per SHA-256 als unverändert
  bestätigt. Die einzige Quiz-Ausnahme besteht aus den zwei genannten Zellen.
- Frische reguläre PDF-Handouts erzeugt: Vorlesung 1 umfasst 50, Vorlesung 2
  43 Seiten. Auf allen 93 Seiten sind die 110 Folien und Notizblöcke sowie
  die laufenden Abschnittsmarkierungen vollständig. Text und Notizanfänge/-enden
  wurden mit den Quellen abgeglichen; keine erkannten Glyphenfehler oder über
  die Seitenfläche laufenden Wörter. Zwölf repräsentative PDF-Seiten wurden
  tatsächlich rasterisiert und visuell geprüft, darunter neue Einstiege,
  Abschnittsfolien, Schaltungs-/Rechenbeispiele und Abschlussnotizen.
  Dies ist keine visuelle Einzelabnahme aller 93 Seiten.
- `git -c core.whitespace=cr-at-eol diff --check` ohne Fehler. Die Option
  berücksichtigt die unverändert beibehaltenen CRLF-Zeilenenden der Quizdatei.

Der gemeinsame vollständige Projektcheck
`source scripts/activate.sh && python3 scripts/build-materials.py all` war
erfolgreich. Er hat alle zehn Websitequellen, neun regulären Vorlesungshandouts
und zehn Übungs-/Prüfungsblätter in beiden PDF-Profilen frisch erzeugt und
unter `_site/` bereitgestellt. Für Programmierpakete liegen keine Manifeste vor.
Die in diesem Auftrag geänderten Inhalte wurden damit auch im regulären
Gesamtbuild verarbeitet; ein GitHub-Actions-Lauf wurde dafür nicht ausgelöst.
