# Vorlesung 7: Transferaufgaben und Quiz

Überarbeitung vom 11. November 2026 auf Grundlage des bereitgestellten Entwurfs
„Klausuraufgaben 07 · Moderne CPU-Architekturen“. Die sechs Aufgaben ersetzen
insbesondere die bisherigen Vier-Befehle-Fälle, die nur Register und Zahlen der
Folien variierten. Der Entwurf wurde für das vorhandene Übungsformat gekürzt;
die Musterlösungen bleiben im getrennten Lösungsprofil.

## Lernziele und eigenständige Arbeit

| Aufgabe | Lernziel und Transfer gegenüber den Folien | Einordnung |
|---|---|---|
| 1 | Eine sechsstufige Pipeline selbst aufbauen und den zusätzlichen Stillstand ohne Forwarding herleiten; der WB-Takt ist nicht vorgegeben. | Kurzer Recheneinstieg, 4 P |
| 2 | Den Abhängigkeitsgraphen einer Reduktion umgestalten; Kette, Teilketten und Baum bei verschiedenen Start-/Retire-Breiten vergleichen sowie Fetch-Grenzen vom kurzen Ausführungsfenster unterscheiden. | Anwendung und Engpassanalyse, 10 P |
| 3 | Zwei Ladezugriffe bei blockierender beziehungsweise nicht blockierender LSU verfolgen; Quellversionen, Bestätigungsreihenfolge und ROB-Zustand zusammenführen. | Mehrstufige Ablaufanalyse, 14 P |
| 4 | Ein Gegenbeispiel zur Überlegenheit des 2-Bit-Prädiktors erklären und Takt, Fehlvorhersagestrafe, Leistung und Energie gemeinsam beurteilen. | Gegenbeispiel und Entwurfsvergleich, 10 P |
| 5 | Den Fehlerfall von Aufgabe 3 rekonstruieren, die sichere Freigabe einer alten Registerversion begründen und die notwendige Wertkopplung eines Cache-Seitenkanals erklären. | Zustands- und Fehleranalyse, 8 P |
| 6 | Load-Use-Stillstände durch Scheduling vermeiden, Ausrollen von mehreren Akkumulatoren unterscheiden und die Zulässigkeit einer Umklammerung prüfen. | Codeumformung und Modellgrenzen, 10 P |

Die 56 Orientierungspunkte sind keine Vorgabe für die spätere Klausur. Für das
vollständige Blatt sind 100–120 Minuten einschließlich eigener Begründungen
geschätzt. Grundlage sind die expliziten Modelle, mehrere Zeitpläne und der
Vergleich geänderter Randbedingungen; studentische Bearbeitungsdaten liegen
noch nicht vor. Im 180-Minuten-Plan der Vorlesung bleiben 55 Minuten für eine
angeleitete Auswahl: Aufgabe 1, 2.1–2.2, Auswahl aus 3.2–3.3/4.1 sowie
5.1–5.2/6.1. Die übrigen Teilaufgaben dienen der selbstständigen Vertiefung.

Die Taktverträge stehen jeweils bei den Aufgaben. Insbesondere gilt im
Fehlerfall: Retire und Trap-Entscheidung erfolgen am Taktanfang vor Issue.
Damit hängt die Lösung nicht von einer unausgesprochenen Reihenfolge dieser
Aktionen ab. Die kurzen Modelle sind keine Messwerte eines realen Kerns.
Die Folienbeispiele und die vorhandene Host-C-Datei bleiben erhalten.

## Übernommenes Quiz

`quizacademy/quiz_07_moderne_cpu_architekturen.csv` enthält die bereitgestellte
Datei `quiz_07_moderne_cpu_architekturen_v2.csv` bytegenau. Ihr SHA-256 ist
`8f8b06443b20012da1637ccc12405285ea3c12d8ccd3daa548256820e0f69486`.
Die vorhandene BOM des Uploads bleibt erhalten; die Quarto-Quellen sind UTF-8
ohne BOM. Jede der zehn Fragen enthält vier Antworten und genau eine richtige.

| Frage | Lernziel und Denkschritt | Anspruch |
|---|---|---|
| 1 | Pipelinefenster einschließlich Füllen/Leeren berechnen und daraus CPI bestimmen. | Recheneinstieg |
| 2 | Zwei zunächst getrennte Abhängigkeitsketten im konkreten Programm anordnen und Start von Retire unterscheiden. | Ablaufanalyse |
| 3 | Fetch-Bytes in eine Befehlsrate umrechnen und mit drei weiteren Breiten vergleichen. | Engpassanalyse |
| 4 | Quellen an die beim Renaming gültige physische Version binden. | Zustandsverfolgung |
| 5 | Bei Latenz drei und Initiationsintervall eins die nötige Anzahl unabhängiger Ketten bestimmen. | Bedingungsanalyse |
| 6 | Aus blockiertem ältestem Eintrag und endlicher ROB-Kapazität die Grenze des Vorziehens ableiten. | Fehlerdiagnose einer Beschleunigungsbehauptung |
| 7 | Bei einer älteren Exception die Wirkung eines jüngeren, noch ungeordneten Stores beurteilen. | Transfer auf präzise Exceptions |
| 8 | Vorhersage und anschließendes Update über einen Richtungswechsel getrennt durchführen. | Zustandsverfolgung |
| 9 | Fehlrate pro Sprung in CPI umrechnen und Laufzeitzuwachs von Durchsatzverlust unterscheiden. | Mehrstufige Rechnung |
| 10 | Die Kopplung zwischen spekulativem Wert und Cacheadresse erkennen und die Grenze von Rollback begründen. | Kausalanalyse |

Alle markierten Antworten wurden fachlich unabhängig nachgerechnet. Die
Antwortoptionen haben vergleichbare Längen und einen ähnlichen Detailgrad;
die richtige Antwort lässt sich nicht systematisch an der längsten Option
erkennen. Die offenen Aufgaben verlangen zusätzlich eigene Herleitungen,
Zeitpläne und Begründungen.

## Prüfungen

Die zentralen Zeitpläne wurden mit einem unabhängig formulierten Scheduler
nachgerechnet: Kette/Teilketten 8/5 Takte, Teilketten bei Retire-Breite eins
8 Takte, Vierfach-Baum 4 Takte; die drei Load-Modelle ergeben 15/14/9 Takte.
Bei einem Fehler von C erfolgt der Trap in Takt 7 nach Bestätigung von A und B
und vor einem weiteren Issue. Die Prädiktor-Gegenfolge ergibt drei Fehler
mit einem Bit und fünf mit zwei Bits. Takt-/Spannungsvergleich und die
Scheduling-/Akkumulatorgrenzen wurden separat nachgerechnet.

Weitere tatsächlich ausgeführte Prüfungen:

- CSV-Validator: zehn Fragen ohne Formatfehler; Upload und Zieldatei per
  Bytevergleich und SHA-256 identisch. Fachprüfung aller zehn richtigen
  Antworten einschließlich M2-Retire-Fenster, Prädiktor-Update und CPI-Bilanz.
- Vorhandenes `labs/src/lab07_ilp.c` mit C11, `-O3 -Wall -Wextra -Werror` und
  Address-/UndefinedBehaviorSanitizer übersetzt und erfolgreich ausgeführt.
  Die optionale `sum3`-Musterlösung separat als C17 mit denselben Warnungen
  und Sanitizern geprüft: vorgegebene Beispiele, Null-Länge/Nullzeiger sowie
  alle Präfixlängen 0–25 eines Feldes mit großen vorzeichenlosen Werten.
  Dies sind Funktionsprüfungen, keine Prozessor-Zeitmessungen.
- Binary32-Beispiel unabhängig mit Rundung nach jedem Additionsschritt
  nachgerechnet: linke Summe 1, aufgeteilte Summe 0. Der dafür nötige
  Werteabstand bei $10^8$ ist in der Aufgabe angegeben.
- `source scripts/activate.sh` und `python3 scripts/build-materials.py all`
  erfolgreich: zehn Websitequellen, neun reguläre PDF-Handouts und zehn
  Übungs-/Klausurquellen in beiden PDF-Profilen. Keine Codeprojekt-Manifeste
  vorhanden, daher keine neuen Startcode-ZIPs.
- Die geänderte Ablauffolie im frischen Reveal.js-Vortrag bei 1280 × 720 im
  Browser angesehen; Tabelle lesbar, keine abgeschnittenen Inhalte. Das
  60-seitige VL7-Handout an der geänderten Folie und ihren Notizen auf
  PDF-Seiten 3–4 angesehen. Die übrigen Handoutseiten wurden bei diesem
  Auftrag nicht erneut vollständig visuell geprüft.
- Alle Seiten des Aufgabenblatts und der Musterlösung visuell kontrolliert.
  Gefundene Umbrüche korrigiert: ROB-Tabelle zusammenhalten, nummerierte
  Lösungsabschnitte trennen, Teilaufgabe 6.4 zusammenhalten und mehr Schreibraum
  für Aufgabe 4. Endfassung: elf Studierenden- und vierzehn Lösungsseiten.
  Nach Änderungen betroffene Seiten erneut angesehen; Gleichheit der
  unveränderten Seiten durch Vergleich der gerenderten Seitenbilder belegt.
- Lösungstrennung zusätzlich am PDF-Text geprüft: alle sechs Aufgaben und
  die optionale Vertiefung in beiden Profilen, sieben Arbeitsräume in der
  Studierendenfassung; Lösungskennzeichnungen, mehrere eindeutige
  Lösungspassagen und der ausgearbeitete `sum3`-Code ausschließlich in der
  Musterlösung.
- UTF-8 ohne BOM und Ersatzzeichen für beide Quarto-Quellen; weiterhin
  siebzig Folien mit siebzig Notizblöcken. Die 27 übrigen Kursquellen aus
  Vorlesungen, Übungen und Quiz bleiben per SHA-256 unverändert.
  `git diff --check` ohne Befund.
