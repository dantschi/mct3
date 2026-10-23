# Vorlesung 3: Lernziele und Stofftiefe

Überarbeitung vom 23. Oktober 2026 für das fünfte Bachelorsemester.

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
| Ereignisse erfassen und Benachrichtigung wählen | Speicherung, Polling-Lücke, Aufwand | Aufgabe 1: Drehgeber und Impulse | 1 |
| Trap und Gerätepfad korrekt erklären | Freigaben, Kontext, Kategorie/ID, Claim–Gerät–Complete | Aufgaben 2–3: Zustände, Adresse, Gerätefehler | 2–6 |
| Zeit aus einer Zeitquelle ableiten und Termine planen | Tickeinheiten, Vergleich, absolutes Raster, versäumte Termine | Aufgabe 4: andere Frequenz und anderes Sollraster | 7–8 |
| Reaktionsfrist und Datenübergabe begründen | mittlere Last gegenüber Zeitgrenze, kurze ISR, kritische Übergabe | Aufgaben 5–6: zwei Endpunkte und verlorenes Zählerereignis | 9–10 |

Die Vorlesung erklärt und begründet. Die Übung verlangt eigene Skizzen,
Rechnungen und korrigierte Abläufe mit gegenüber den Folien geänderten
Situationen. Das Quiz dient der schnellen Diagnose typischer Fehlvorstellungen;
es ersetzt keine offene Entwurfs- oder Rechenaufgabe. Seine zehn Fragen besitzen
je vier Antworten und genau eine richtige Antwort. Bei drei Fragen ist die
richtige Option allein am längsten; ihre Position folgt keinem einfachen Zyklus.

## Was bleibt, was entfällt aus dem Hauptteil?

- Direct/Vectored bleibt als kompakter Vergleich mit einer Adressrechnung.
  Modusbitkodierung, vollständiger Tabellenaufbau und Assemblerdirektiven entfallen.
- Trap-Kontext und die Aufgaben von Hardware und Software bleiben zentral.
  Ausführlicher GCC-Attributvertrag und eigene Prologimplementierung entfallen.
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
- Das zusätzliche 32-Bit-Umlaufbeispiel entfällt. Die Grenzen der verwendeten
  Terminrechnung bleiben ausdrücklich genannt: positive Periode, kein Umlauf
  oder arithmetischer Überlauf im betrachteten Zeitraum.

Die gewonnene Erklärzeit fließt in Ereignisspeicherung, ungünstigste Polling-Lücke,
Anwendungspolitik bei versäumten Terminen, zwei unterschiedliche Reaktionsendpunkte
und eine konkret geschützte Übergabe. Drei neue eigene Abbildungen zeigen diese
Zusammenhänge und die vereinfachte Kategorie-/Geräteauswahl.

## Umfang und Einbettung

Der Foliensatz enthält 46 Hauptfolien mit vollständigen Skriptnotizen und vier
optionale Vertiefungen. Die Planung umfasst weiterhin vier Schulstunden mit
110 Minuten gemeinsamer Erarbeitung, 55 Minuten angeleiteter Aufgabenarbeit
und 15 Minuten Quiz. Das vollständige Übungsblatt umfasst sechs Pflichtaufgaben
mit 32 Orientierungspunkten und etwa 60–75 Minuten selbstständiger Bearbeitung;
in den Präsenzphasen werden ausgewählte Teilaufgaben bearbeitet und verglichen.

Vorausgesetzt werden Geräteadressen und Speichergrundlagen aus den Vorlesungen
1–2 sowie C-Zeiger, Bits und Schleifen. Neue Architekturbegriffe werden lokal
erklärt. Vorlesung 4 kann auf Zeitquelle, Vergleich, ISR und Reaktionsfristen
aufbauen. Die Interrupt- und Timerfragen der bestehenden Probeklausur bleiben
durch den Hauptteil abgedeckt. Übung und Quiz verlangen keine optionale Vertiefung.

## Prüfung der überarbeiteten Fassung

Die 50 Folien wurden im Browser mit gesetzten Formeln auf überlaufende Inhalte
geprüft. Alle Folien besitzen genau einen zugeordneten Notizblock. Das Skript-PDF
und beide Übungsblattprofile wurden erzeugt und auf Aufgaben, Lösungstrennung
und Seitenränder kontrolliert. Die drei neuen Diagramme wurden visuell geprüft.
Die Zahlenbeispiele wurden unabhängig nachgerechnet und die reine C-Terminplanung
mit 1.170.000 Fällen gegen eine schrittweise Rasterberechnung geprüft, einschließlich
Compilerwarnungen und Address-/UndefinedBehaviorSanitizer. CSV-Struktur,
Antwortlängen und UTF-8-Prüfung waren ebenfalls erfolgreich.

Diese Prüfungen betreffen Lehrmodelle, reine Host-Rechnung und Darstellung.
Eine konkrete RISC-V-Firmware oder eine reale Reaktionszeit wurde damit nicht gemessen.
