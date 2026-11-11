# Vorlesung 3: Lernziele und Stofftiefe

Stand: 11. November 2026. Grundüberarbeitung vom 23. Oktober 2026,
anschließend Erläuterungen, STM32-Bezüge, Übung und Quiz überarbeitet.
Die aktuelle Fassung ergänzt Abschnittsfolien und durchgehende Lernnotizen.
Zielgruppe ist das fünfte Bachelorsemester.

## Kritische Einordnung

Die bisherige Fassung verband fachlich belastbare Modelle mit zu vielen gleich
gewichteten Implementierungsdetails. Vektortabellenaufbau, RV32-Halbzugriffe,
Softwareinterrupts, PLIC-Schwellenwertsonderfälle, Compilerattribute und
verschachtelte Interrupts erforderten jeweils neue Begriffe. Der Nutzen dieser
Details für einen eigenen Systementwurf war gegenüber ihrer Stoffmenge zu wenig
sichtbar. Der Einstieg setzte mit einer Themenübersicht ein und machte vorhandene
Vorstellungen der Studierenden noch nicht sichtbar.

Im fünften Semester ist die Verbindung von Architektur, C-Programmierung und
zeitlichen Anforderungen sinnvoll anspruchsvoll. Die Tiefe entsteht hier durch
begründete Entscheidungen, vollständige Zustandsfolgen, Zeitrechnungen und
Fehleranalysen. Eine vollständige Registerkarte oder ein selbst geschriebener
Trap-Prolog sind dafür keine notwendigen zusätzlichen Lernziele.

Die Neufassung beginnt mit der Diskussion: Ein Messgerät rechnet vier
Millisekunden, soll neue Daten aber binnen hundert Mikrosekunden sichern.
Hilft ein doppelt so schneller Prozessor, und welche Annahmen fehlen?
Am Ende wird dieser Fall mit dem erarbeiteten Modell erneut entschieden.

## Gemeinsames Ziel der drei Lernformen

Studierende können einen Ereignis- und Zeitpfad entwerfen und erklären, welche
Bedingungen für korrekte Datenübernahme, Fortsetzung und rechtzeitige Reaktion
erfüllt sein müssen.

| Kompetenz | Vorlesung | Papierübung | Quizfragen |
|-----------|-----------|-------------|------------|
| Ereignisse erfassen und Benachrichtigung wählen | Speicherung, Polling-Lücke, Aufwand | Aufgabe 1: begründete Auswahl und Hardware-Schrittzähler | 1 |
| Trap und Gerätepfad korrekt erklären | Freigaben, Kontext, Kategorie/ID, Claim–Gerät–Complete | Aufgaben 2–3: Exception, Vektorziel, Initialisierung und Gerätefehler | 2–6 |
| Zeit aus einer Zeitquelle ableiten und Termine planen | Tickeinheiten, Vergleich, absolutes Raster, versäumte Termine | Aufgabe 4: fehlerhafte Timer-Routine analysieren und korrigieren | 7–8 |
| Reaktionsfrist und Datenübergabe begründen | Blockierung, Prioritätsgrenzen, kurze ISR, kritische Übergabe | Aufgaben 5–6: Reaktionsentwurf, Dauerbetrieb und verlorenes Zählerereignis | 9–10 |

Die Vorlesung erklärt und begründet. Die Übung verlangt eigene Skizzen,
Rechnungen und korrigierte Abläufe mit gegenüber den Folien geänderten
Situationen. Das Quiz dient der schnellen Diagnose typischer Fehlvorstellungen;
es ersetzt keine offene Entwurfs- oder Rechenaufgabe. Seine zehn Fragen besitzen
je vier Antworten und genau eine richtige Antwort. Die am 1. November
bereitgestellte Ersatzdatei wurde unverändert übernommen. Darin ist bei einer
Frage die richtige Option allein am längsten; ihre Position folgt keinem
einfachen Zyklus.

## Was bleibt, was entfällt aus dem Hauptteil?

- Direct/Vectored bleibt als Vergleich mit Adressrechnungen, BASE/MODE-Erklärung
  und ausgewählten Einsprungplätzen. Ein vollständiger Tabellenaufbau und
  Assemblerdirektiven sind keine zusätzlichen Pflichtaufgaben.
- Trap-Kontext und die Aufgaben von Hardware und Software bleiben zentral.
  Einzelne CSR-Zugriffe machen Setzen und Löschen von Freigabebits greifbar.
  Ein ausführlicher GCC-Attributvertrag und eigene Prologimplementierung entfallen.
- Der lokale Timer und externe PLIC-Pfad bleiben. Ein separater Softwareinterrupt-
  und Mehrkernbenachrichtigungspfad entfällt an dieser Stelle.
- Die Pflichtbeispiele verwenden einen PLIC-Schwellenwert von null. Der Unterschied
  zwischen Threshold-gefilterter Benachrichtigung und explizitem Claim ist optional.
- Konsistentes Lesen und Schreiben wird im Hauptteil als Vertrag der
  Plattformfunktion benannt. HI–LO–HI und die Dreischritt-Schreibfolge stehen
  in zwei Vertiefungsfolien.
- Nicht verschachtelte ISR bleiben das Grundmodell. Warum Verschachtelung
  zusätzlichen Rückkehrzustand benötigt, steht in einer Vertiefungsfolie.
  Frame-Budgetrechnung und Verschachtelungsaufgabe sind keine Pflichtaufgaben mehr.
- Die Notizen vergleichen die Umlaufzeiten von 32- und 64-Bit-Zählern und erklären
  den möglichen Mischwert bei Halbzugriffen. Die Terminrechnung verlangt weiterhin
  eine positive Periode und keinen Umlauf oder arithmetischen Überlauf im
  betrachteten Zeitraum.

Die gewonnene Erklärzeit fließt in Ereignisspeicherung, ungünstigste Polling-Lücke,
Anwendungspolitik bei versäumten Terminen, zwei unterschiedliche Reaktionsendpunkte
und eine konkret geschützte Übergabe. Drei neue eigene Abbildungen zeigen diese
Zusammenhänge und die vereinfachte Kategorie-/Geräteauswahl.

## Umfang und Einbettung

Der Foliensatz enthält 56 Folien mit vollständigen Lernnotizen: 46 bisherige
Hauptfolien, fünf neue Abschnittsfolien, einen Orientierungstrenner vor der
Vertiefung und die vier vorhandenen Vertiefungsfolien. Die fünf Lernabschnitte
sind Ereignisse, Trap-Eintritt, Geräte/PLIC, Timer und Reaktionszeit/Datenübergabe.
Kurze Abschnittsmarkierungen machen die Position auch zwischen den Trennern sichtbar. Die Planung umfasst weiterhin vier Schulstunden mit
110 Minuten gemeinsamer Erarbeitung, 55 Minuten angeleiteter Aufgabenarbeit
und 15 Minuten Quiz. Das vollständige Übungsblatt umfasst sechs Pflichtaufgaben
mit 36 Orientierungspunkten und etwa 75–90 Minuten selbstständiger Bearbeitung;
in den Präsenzphasen werden ausgewählte Teilaufgaben bearbeitet und verglichen.

Vorausgesetzt werden Geräteadressen und Speichergrundlagen aus den Vorlesungen
1–2 sowie C-Zeiger, Bits und Schleifen. Die bekannte STM32-Timerkonfiguration mit
Prescaler und ARR dient als Anker; der frei laufende Output-Compare-Betrieb wird
erklärt. Update-Flag und Vergleichsereignis werden dabei unterschieden.
Neue Architekturbegriffe werden lokal erklärt. Vorlesung 4 kann auf Zeitquelle,
Vergleich, ISR und Reaktionsfristen aufbauen. Die Interrupt- und Timerfragen der bestehenden Probeklausur bleiben
durch den Hauptteil abgedeckt. Übung und Quiz verlangen keine optionale Vertiefung.

## Frühere Prüfungen vor der Gliederungsüberarbeitung

Die damaligen 50 Folien wurden im Browser mit gesetzten Formeln auf überlaufende Inhalte
geprüft. Alle Folien besitzen genau einen zugeordneten Notizblock. Das Skript-PDF
und beide Übungsblattprofile wurden erzeugt und auf Aufgaben, Lösungstrennung
und Seitenränder kontrolliert. Die drei neuen Diagramme wurden visuell geprüft.
Die Zahlenbeispiele wurden unabhängig nachgerechnet und die reine C-Terminplanung
mit 1.170.000 Fällen gegen eine schrittweise Rasterberechnung geprüft, einschließlich
Compilerwarnungen und Address-/UndefinedBehaviorSanitizer. CSV-Struktur,
Antwortlängen und UTF-8-Prüfung waren ebenfalls erfolgreich.

Die neue Übung ergänzt Entscheidungen zur Ereignisbehandlung, eine Exception
mit demselben Code wie ein externer Interrupt, Initialisierung und Fehleranalyse
einer Timer-Routine. Der integrierte Reaktionsfall setzt ausdrücklich voraus,
dass nach einer Sperre oder Behandlung der wartende höher priorisierte Sensor
vor weiterer Hauptprogrammarbeit bedient wird. Unter diesen Annahmen ist die
Blockierung das Maximum aus UART-Behandlung und Hauptprogrammsperre, nicht deren
Summe. Dauerbetrieb und endliche Puffer werden getrennt vom Einzelereignis geprüft.
Die fehlerhafte und die korrigierte C-Routine wurden mit Zeit-/Vergleichsstubs
auf dem Host übersetzt und mit Sanitizern an frühen und verspäteten Aufrufen
geprüft. Die übernommene Quizdatei wurde zusätzlich auf Bytegleichheit geprüft.

Diese Prüfungen betreffen Lehrmodelle, reine Host-Rechnung und Darstellung.
Eine konkrete RISC-V-Firmware oder eine reale Reaktionszeit wurde damit nicht gemessen.


## Gliederung und Lerntext vom 11. November 2026

Fünf zusätzliche Abschnittsfolien führen jeweils mit einer Leitfrage in
Ereignisspeicherung, Trap-Eintritt, Geräte/PLIC, Timer und Reaktionszeit mit
Datenübergabe ein. Ein eigener Trenner kennzeichnet die optionale Vertiefung.
Die bisherige Reihenfolge der 50 Sach- und Orientierungsfolien bleibt erhalten;
mit den sechs neuen Trennern enthält die Fassung 56 Folien.

Jede bestehende Folie trägt eine kurze Abschnittsmarkierung. Das dafür
verwendete Stylesheet ist nur in Vorlesung 3 eingebunden. Die Orientierungszeit
gehört zu den bereits vorgesehenen Erklär- und Besprechungsphasen; es entsteht
kein zusätzlicher Pflichtstoff. Die Übung verweist auf den beständigen Titel
„Nächsten Vergleichstermin planen“ statt auf die frühere Foliennummer.

Alle Notizen sind als fortlaufender Lerntext mit begründeten Übergängen
überarbeitet. Regieanweisungen und nummernabhängige Querverweise sind durch
inhaltliche Erklärungen ersetzt. Analogien, Rechenbeispiele, Plattformgrenzen
und die STM32-Brücke bleiben erhalten. Unabhängiger Originalvergleich:
Sämtliche ursprünglichen C-, Assembler- und Pseudocode-Blöcke bleiben unverändert;
die fachliche Reihenfolge und die vorhandenen Abbildungen ebenfalls.

**Aktuelle Prüfungen:** UTF-8 ohne BOM, 56 Überschriften mit genau 56 zugeordneten
Notizblöcken, reparierter Übungsverweis und Diff-Prüfung. Frische Reveal.js-Fassung
mit Quarto 1.11.9 erzeugt und in Chromium mit gesetzten Formeln über alle
56 Folien auf Überlauf, Bildfehler und Notizzuordnung geprüft. Nach Anpassung des
Abstands zwischen Titel und Abschnittsmarkierung waren diese Prüfungen fehlerfrei.
Die Abschnitte und mehrere dichte Folien wurden zusätzlich anhand von
Screenshots angesehen. Eine HTML-Lesefassung enthält alle 56 Notizabschnitte,
die im Browser sichtbar und mit vollständigen Bildpfaden geprüft wurden.
Sie lässt sich ohne LaTeX als zusammenhängender Lesetext erzeugen:

```bash
source scripts/activate.sh
quarto render vorlesungen/03_interrupts_timer.qmd --profile handout --to html
```

Ausgabe: `_handout/vorlesungen/03_interrupts_timer.html`.

**Prüfgrenze:** Der vollständige gemeinsame Build wurde ausgeführt. Alle zehn
Websitequellen wurden gerendert, danach scheiterte der reguläre Handoutlauf
bereits bei Vorlesung 1 am fehlenden `luatexbase.sty` in der installierten
TeX-Umgebung. Auch die gezielte PDF-Prüfung mit XeLaTeX gelang wegen fehlender
Sprachunterstützung (`ngerman`) nicht. Es gibt daher keine aktuelle Freigabe des
regulären Skript-PDFs oder beider Lab-PDF-Profile. Ältere PDF-Dateien werden nicht
als Nachweis dieser Fassung verwendet. Die Inhalts- und HTML-Prüfung ist davon
getrennt; eine Firmwareausführung oder reale Zeitmessung wurde nicht behauptet.
