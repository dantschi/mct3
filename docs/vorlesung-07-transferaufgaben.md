# Vorlesung 7: Transferaufgaben und Quiz

Überarbeitung vom 11. November 2026 auf Grundlage des bereitgestellten Entwurfs
„Klausuraufgaben 07 · Moderne CPU-Architekturen“. Die sechs Aufgaben ersetzen
insbesondere die bisherigen Vier-Befehle-Fälle, die nur Register und Zahlen der
Folien variierten. Der Entwurf wurde für das vorhandene Übungsformat gekürzt;
die Musterlösungen bleiben im getrennten Lösungsprofil. Die Tabellen geben den
Stand nach der Kürzung vom 24. November 2026 wieder; deren Umfang und Prüfungen
stehen im [Nachtrag](#nachtrag-vom-24-november-2026-gekürzte-vorlesung).

## Lernziele und eigenständige Arbeit

| Aufgabe | Lernziel und Transfer gegenüber den Folien | Einordnung |
|---|---|---|
| 1 | Eine sechsstufige Pipeline selbst aufbauen und den zusätzlichen Stillstand ohne Forwarding herleiten; der WB-Takt ist nicht vorgegeben. | Kurzer Recheneinstieg, 4 P |
| 2 | Den Abhängigkeitsgraphen einer Reduktion umgestalten; Kette, Teilketten und Baum bei verschiedenen Start-/Retire-Breiten vergleichen sowie Fetch-Grenzen vom kurzen Ausführungsfenster unterscheiden. | Anwendung und Engpassanalyse, 10 P |
| 3 | Zwei Ladezugriffe bei blockierender beziehungsweise nicht blockierender LSU verfolgen; Quellversionen, Bestätigungsreihenfolge und ROB-Zustand zusammenführen. | Mehrstufige Ablaufanalyse, 14 P |
| 4 | Ein Gegenbeispiel zur Überlegenheit des 2-Bit-Prädiktors erklären und Takt, Fehlvorhersagestrafe, Leistung und Energie gemeinsam beurteilen. | Gegenbeispiel und Entwurfsvergleich, 10 P |
| 5 | Den Fehlerfall von Aufgabe 3 rekonstruieren und die sichere Freigabe einer alten Registerversion begründen. | Zustands- und Fehleranalyse, 5 P |
| 6 | Load-Use-Stillstände durch Scheduling vermeiden, Ausrollen von mehreren Akkumulatoren unterscheiden und die Zulässigkeit einer Umklammerung prüfen. | Codeumformung und Modellgrenzen, 10 P |

Die 53 Orientierungspunkte sind keine Vorgabe für die spätere Klausur. Für das
vollständige Blatt sind 95–115 Minuten einschließlich eigener Begründungen
geschätzt; die frühere Schätzung von 100–120 Minuten für 56 Punkte wurde
anteilig gekürzt. Grundlage sind die expliziten Modelle, mehrere Zeitpläne und der
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

`quizacademy/quiz_07_moderne_cpu_architekturen.csv` beruht auf der
bereitgestellten Datei `quiz_07_moderne_cpu_architekturen_v2.csv` mit dem
SHA-256 `8f8b06443b20012da1637ccc12405285ea3c12d8ccd3daa548256820e0f69486`.
Die Fragen 1–6, 8 und 9 sind daraus unverändert übernommen. Die Fragen 7 und
10 wurden am 24. November 2026 ersetzt, weil die Folien zur Store-Queue und
zur Wertkopplung eines Cache-Seitenkanals entfallen sind; die Datei ist daher
nicht mehr bytegleich mit dem Upload. Die vorhandene BOM bleibt erhalten; die
Quarto-Quellen sind UTF-8 ohne BOM. Jede der zehn Fragen enthält vier Antworten
und genau eine richtige.

| Frage | Lernziel und Denkschritt | Anspruch |
|---|---|---|
| 1 | Pipelinefenster einschließlich Füllen/Leeren berechnen und daraus CPI bestimmen. | Recheneinstieg |
| 2 | Zwei zunächst getrennte Abhängigkeitsketten im konkreten Programm anordnen und Start von Retire unterscheiden. | Ablaufanalyse |
| 3 | Fetch-Bytes in eine Befehlsrate umrechnen und mit drei weiteren Breiten vergleichen. | Engpassanalyse |
| 4 | Quellen an die beim Renaming gültige physische Version binden. | Zustandsverfolgung |
| 5 | Bei Latenz drei und Initiationsintervall eins die nötige Anzahl unabhängiger Ketten bestimmen. | Bedingungsanalyse |
| 6 | Aus blockiertem ältestem Eintrag und endlicher ROB-Kapazität die Grenze des Vorziehens ableiten. | Fehlerdiagnose einer Beschleunigungsbehauptung |
| 7 | Bei einer Exception eines jüngeren Befehls, während ein älterer Load noch wartet, Zeitpunkt des präzisen Traps und sichtbaren Zustand herleiten. Die Folien behandeln nur den Fehler am ältesten Befehl. | Transfer auf präzise Exceptions |
| 8 | Vorhersage und anschließendes Update über einen Richtungswechsel getrennt durchführen. | Zustandsverfolgung |
| 9 | Fehlrate pro Sprung in CPI umrechnen und Laufzeitzuwachs von Durchsatzverlust unterscheiden. | Mehrstufige Rechnung |
| 10 | Aus der Grenze des Rollbacks die Folge für einen späteren Zugriff des richtigen Pfads ableiten und von Register- bzw. Bestätigungswirkungen abgrenzen. | Kausalanalyse |

Alle markierten Antworten wurden fachlich unabhängig nachgerechnet. Die
Antwortoptionen haben vergleichbare Längen und einen ähnlichen Detailgrad;
die richtige Antwort lässt sich nicht systematisch an der längsten Option
erkennen. Die offenen Aufgaben verlangen zusätzlich eigene Herleitungen,
Zeitpläne und Begründungen.

## Prüfungen der Überarbeitung vom 11. November 2026

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

## Nachtrag vom 24. November 2026: gekürzte Vorlesung

Auf Wunsch entfallen in Vorlesung 7 acht Folien (Nummern der bisherigen
Fassung mit 70 Folien): 35 „Fetch-Bytes sind keine feste Befehlszahl“,
49 „Interrupt und Exception brauchen verschiedene Grenzen“, 50 „Ein Store hat
mehr als einen Abschlusszeitpunkt“, 62 „Ein Cache-Seitenkanal benötigt eine
Wertkopplung“, 63 „Unterschiedliche Mechanismen brauchen passende Maßnahmen“,
67 „Übersetzung und Funktion sind eigene Nachweise“, 68 „Abschlussquiz:
Fenster, Version und Vorhersage nennen“ und 70 „Was Sie jetzt erklären und
prüfen können“. Die Folie „Zurück zu den zwei Recheneinheiten“ bleibt als
Auflösung der Einstiegsfrage erhalten; die Einheit umfasst nun 62 Folien.
Der Zeitplan einschließlich 15 Minuten Quiz bleibt unverändert.

Folgeanpassungen in den Notizen:

- „Der engste Abschnitt begrenzt die dauerhafte Rate“ ordnet die Fetch-Breite
  in Bytes der Befehlszahl zu (32- und 16-Bit-Befehle). Aufgabe 2.4 und
  Quizfrage 3 bleiben damit durch die Vorlesung gedeckt.
- „Eine Exception bestätigt kein jüngeres Ergebnis“ enthält einen kurzen
  Absatz zur Annahmegrenze eines Interrupts und leitet zum Aliasfall über;
  „Register-Renaming löst keine Speicheraliase“ erklärt den Store-Puffer beim
  Weiterleiten.
- „Ein festes Modell für den Reihenfolgevergleich“ begründet die Ladelatenz
  von vier Takten als didaktische Wahl; „Out-of-Order: C und D nutzen die
  Wartezeit“ bezeichnet den Load nicht mehr als Miss. Nachgerechnet: Im
  M3-Vertrag benötigt In-Order für jede Ladelatenz $L\geq2$ genau $L+4$ und
  Out-of-Order $L+3$ Takte. Erst ab $L=3$ passen C und D in die Wartezeit;
  bei $L=4$ bleibt genau ein Takt ohne Start.
- „Rollback betrifft nicht jeden internen Zustand“ ordnet Seitenkanal und
  Spectre nur noch ein und leitet zum Compilerabschnitt über.
- „Ausrollen und mehrere Akkumulatoren unterscheiden“ verweist auf die
  optionale Übungsvertiefung mit `labs/src/lab07_ilp.c` und ordnet Compiler
  Explorer und Renode ein.
- Die Schlussfolie übernimmt Lernziele, Quizablauf, Quellen und den Übergang
  zu VL 8 aus der entfallenen Abschlussfolie; der KPTI-Beleg entfällt mit
  Folie 63.
- Ablauffolie und Abschnittsfolien 3 und 5 sind an Folienzahl,
  Vertiefungshinweise und Abschnittsinhalte angepasst.

Im Übungsblatt entfällt Teilaufgabe 5.3 zum Cache-Seitenkanal (3 P) mit den
Folien 62 und 63. Das Blatt umfasst 53 Orientierungspunkte; die Bearbeitungszeit
ist anteilig auf 95–115 Minuten geschätzt. Die optionale Vertiefung enthält den
bisher nur auf Folie 67 genannten Übersetzungsbefehl, jetzt mit `-std=c17`
passend zur Aufgabenstellung.

Im Quiz sind die Fragen 7 und 10 ersetzt (Zuordnung in der Tabelle oben).
Frage 7 verlangt den Transfer des präzisen Traps auf einen jüngeren
fehlerhaften Befehl, Frage 10 die Zeitfolge einer nach dem Rollback
verbliebenen Cachezeile samt Abgrenzung von Register- und Bestätigungswirkungen.
Beide sind nach Einschätzung von mittlerem Anspruch; studentische
Bearbeitungsdaten liegen nicht vor. Die richtigen Antworten stehen jetzt an den
Positionen 2, 3, 1, 4, 2, 3, 3, 4, 2, 1; das bisherige periodische Muster ist
damit aufgebrochen. In keiner Frage ist die richtige Option allein die längste.

Tatsächlich ausgeführte Prüfungen:

- UTF-8 ohne BOM und ohne Ersatzzeichen in den Quarto-Quellen; 62 Folien mit
  62 Notizblöcken. Die Quiz-CSV behält BOM und LF; der Formatvalidator meldet
  zehn Fragen ohne Befund. Die neuen Fragen wurden fachlich auf Eindeutigkeit
  geprüft.
- Toolchain gemäß `scripts/toolchain.env`. Das gepinnte rsvg-Paket
  `2.60.0+dfsg-1` liefert deb.debian.org nicht mehr (HTTP 404), daher bricht
  `scripts/setup.sh` vor der TeX-Prüfung ab. Die deutschen TeX-Pakete wurden
  mit `scripts/setup-tex.sh` installiert und geprüft.
- `python3 scripts/build-materials.py labs` und `website` erfolgreich. Übungsblatt 7
  hat elf Studierenden- und vierzehn Lösungsseiten; die Seiten mit Aufgabe 5
  und der optionalen Vertiefung wurden angesehen. Lösungen erscheinen nur in
  der Musterlösung, die Studierendenfassung enthält sieben Arbeitsräume.
- Das VL7-Handout wurde gezielt mit `quarto render` im Profil `handout`
  erzeugt: 54 Seiten, Folienköpfe 1–62 lückenlos, 62 Notizblöcke; die Seiten
  der Folien 42 und 62 wurden angesehen. Ein vollständiger `handouts`-Lauf
  unterblieb, weil das VL1-Handout SVG-Grafiken enthält und rsvg fehlt.
- Reveal.js-Vortrag bei 1280 × 720 im Browser: 62 Folien, jede mit Notizen,
  kein vertikaler Überlauf; Abschnittsfolie 5 und Schlussfolie angesehen.
- `labs/src/lab07_ilp.c` mit GCC 13.3 und `-std=c17 -O3 -Wall -Wextra -Werror`
  übersetzt und ausgeführt; alle Prüffälle bestanden.
- `python3 -m unittest discover -s tests`: 58 Tests bestanden;
  `git diff --check` ohne Befund.
