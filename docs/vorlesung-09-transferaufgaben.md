# Vorlesung 9: fünf Fragen für den Multicore-Entwurf

Überarbeitung vom 17. November 2026 auf Grundlage des bereitgestellten
achtseitigen Übungsentwurfs und des Quiz-Uploads mit zwölf Fragen.
Die vorangehende 64-Folien-Fassung ist im historischen Bericht
[vorlesung-09-neufassung.md](vorlesung-09-neufassung.md) beschrieben.

## Lernweg und Prüfrahmen

Die neue Fassung hat 59 Folien mit 59 vollständigen Notizblöcken. Davon
bilden zwei MESI-Tabellen und die optionale Snooping-/Directory-Folie den
Nachschlage- und Hintergrundanhang. Der Notizumfang sinkt von rund 11.100
auf rund 7.500 Wörter. Die Texte beginnen mit der Kernaussage und erklären
Beispiele zusammenhängend; Zahlen und Threadnummern werden als Ziffern
geführt. Gemeinsame Bildkonventionen stehen einmal bei der Ablaufplanung.

Fünf Fragen stehen wörtlich auf den Folien 2, 13, 52 und 56:

1. Ist die Kopie gültig?
2. Ist das Update unteilbar?
3. Sind die Daten nach der Meldung sichtbar?
4. Wird jeder Beteiligte fertig?
5. Wird es schneller?

Die Abschnittsangaben orientieren weiterhin im Lernweg. Die Fragen bilden
den durchgehenden Prüfrahmen für Kopien, Atomizität, Veröffentlichung,
Fortschritt und Laufzeit, einschließlich Aufgabe 6 des neuen Blatts.

## Inhaltliche Änderungen

- ILP/DLP/TLP und SMP/AMP sind zusammengeführt. Kopien und Write-Back
  werden direkt an den passenden MESI-Fällen erklärt. Der rote Rahmen um
  den Beginn des zweiten Arbeitsbereichs wird in den Notizen erläutert.
- Modell K gilt für beliebig viele beteiligte Datencaches. Beim Fremdread
  auf M aktualisiert der Besitzer den unteren Stand L; die beteiligten
  Leser werden S. Beim Fremdwrite auf M liefert der Besitzer dagegen die
  aktuelle ganze Zeile an den neuen Schreiber und wird I; L bleibt alt.
  Beide Vorgänge sind ausdrücklich getrennt. Die zwei Referenztabellen
  decken lokale Reads/Writes, Fremdreads/-writes und Auswurf ab.
- False Sharing und Padding eröffnen den zweiten Themenblock. Der C11-Code
  verwendet `alignas(64)` aus `stdalign.h`; echte Zeilengröße, unterstützte
  Ausrichtung, Strukturgröße und Elementabstand bleiben Zielbedingungen.
- AMO und der C11-Zähler stehen direkt hinter LR/SC im Atomizitätsabschnitt.
- Die Veröffentlichung zeigt sequenced-before, synchronizes-with und die
  daraus folgende happens-before-Beziehung. Die gleichen Kanten werden
  bei beiden Workern wiederverwendet. Gewöhnliche Nutzdaten mit fehlender
  Synchronisation werden vom vollständig atomaren relaxed-Fall getrennt.
- Der nachgestellte Release-Fence wird eindeutig als fehlerhaft erklärt.
  Ein Wartegraph benennt Threads und die Wartebeziehungen; eine globale
  Erwerbsreihenfolge schließt den gezeigten Kreis aus. Lock-free,
  wait-free und Fairness bleiben verschiedene Fortschrittsaussagen.
- Die neue berechnete Kurve setzt den bestehenden Vorlesungsfall mit
  Referenz 100 und seriellem Anteil 0,2 fort: Für mindestens zwei Kerne
  gilt $h(N)=0{,}02N$. Das ganzzahlige Minimum liegt bei sechs Kernen.
  Dieser Vorwärtsfall übernimmt nicht die Rückwärtsrechnung der Übung.
  Strong/Weak Scaling und Gustafsons Sicht werden kurz eingeordnet.
- Der Hostversuch steht jetzt im optionalen Laborteil. Alle Befehle werden
  aus dem Repository-Stamm mit `labs/src/lab09_atomics.c` beschrieben.
- „Sperre“ bezeichnet den Mechanismus, „Schlosswort“ dessen Speicherobjekt.
  Betroffene Abbildungen und Generatoren sind entsprechend angepasst.
  N1570 mit 5.1.2.4 und 7.17 sowie die RISC-V-Atomics-Fassung 20240411
  haben auf der Abschlussfolie ausgeschriebene, im PDF lesbare URLs.

## Präsenz und Nachbereitung

| Themenblock | Erklärung und Besprechung | Papierphase | Kernteile |
|---|---:|---:|---|
| 1, bis Folie 21 | 30 min | 15 min | Aufgabe 1, 6 Punkte |
| 2, bis Folie 36 | 25 min | 15 min | Aufgabe 3 a–c, 8 Punkte |
| 3, bis Folie 45 | 25 min | 15 min | Aufgabe 4 a–b, 7 Punkte |
| 4, bis Folie 55 | 25 min | 15 min | Aufgabe 5 a–b und 6 c, 10 Punkte |

Das sind 105 Minuten Erklärung und Besprechung plus 60 Minuten Papierarbeit.
Mit 15 Minuten Abschlussquiz entstehen 180 Minuten. Die vier Themenblöcke
sind mit 45, 40, 40 und 55 Minuten einschließlich Aktivitäten nicht jeweils
eine einzelne Schulstunde. Die angeglichene Erklärzeit entlastet den Beginn
und gibt der Schlussanwendung mehr Raum. Die beiden MESI-Tabellen dienen
beim Bearbeiten als Referenz; Snooping/Directory ist optionaler Hintergrund.

Die vollständige Übung enthält sechs Aufgaben mit 76 Orientierungspunkten;
31 davon gehören zu den Kernphasen, der Rest zur Nachbereitung. Ihre
Musterlösungen stehen ausschließlich im Lösungsprofil. Auf ausdrücklichen
Wunsch enthalten die Foliennotizen der Papierphasen nur Arbeitsaufträge.
Punkte und geschätzte Zeiten sind keine neu erfundenen offiziellen
Klausurvorgaben; empirische Bearbeitungszeiten liegen nicht vor.

## Eigenständige Denkschritte und fachliche Prüfung

| Aufgabe | Lernziel und Transfer |
|---|---|
| 1 | MESI-Invarianten auf drei Caches übertragen und Koordination mitzählen. |
| 2 | Zeilenrechte von Variablenrechten trennen, einen falschen Datenlieferanten und ungültige Zustandsfolgen diagnostizieren. |
| 3 | Eine LR/SC-Erhöhung selbst schreiben, den SC-Ausgang herleiten und Korrektheit von Fortschritt unterscheiden; AMO und C11 vergleichen. |
| 4 | Speicherordnung als benannte Kette begründen, zwei Ordnungsfehler korrigieren, einen Dreier-Wartegraphen ableiten und den ISR-Fall lösen. |
| 5 | Unbekannte Anteile aus zwei Laufzeiten bestimmen, die diskrete optimale Kernzahl und eine nachweislich beste Paketverteilung finden. |
| 6 | Layout, lokale Akkumulation, drei Veröffentlichungen, Ausfall, Timeout und geregelte Wiederverwendung gemeinsam entwerfen. |

Die Lösungen wurden unabhängig gegengelesen und nachgerechnet. Beispiele:
Aufgabe 1 erzeugt zwei Invalidierungen und zwei Rückschreibungen. Aufgabe 2
benötigt in Schritt 4 den aktuellen Besitzertransfer; die letzte S-Kopie
bleibt nach dem Auswurf S. Die korrekte LR/SC-Folge endet nach beiden
Erhöhungen bei 14, V1 verliert einen Beitrag und V2 hat nach Fehlschlag
keine neue Reservation.

Aufgabe 5 ergibt $s=0{,}2$, $c=0{,}005$ und für $N\geq2$
$T(N)=40+160/N+N$. Das ganzzahlige Minimum liegt bei 13 Kernen mit
$T(13)=849/13$. Der Vergleich aller 729 Zuteilungen der sechs Pakete
bestätigt die bestmögliche maximale Last 60 und Gesamtzeit 100.
Die Vorlesungskurve mit anderem c hat dagegen ihr Minimum bei sechs Kernen.

Die unveränderte vorhandene Hostdatei wurde mit GCC 14.2.0, C11,
`-O2 -Wall -Wextra -Werror -pedantic -pthread -fsanitize=address,undefined`
übersetzt und erfolgreich ausgeführt. Eine separate temporäre Referenzprüfung
bestätigt drei Worker, 21.000 relaxed-RMW-Beiträge, die einmalige Übergabe
von 73, die Drei-Slot-Summe 78 und 64-Byte-Padding mit 192 Byte Gesamtgröße.
Kein gewöhnlicher C-Data-Race wurde als Zahlenbeweis ausgeführt.
Die studentischen Erweiterungen und optionalen Laufzeitmessungen werden
damit nicht als vollständig implementiert oder auf RISC-V ausgeführt behauptet.

Das bereitgestellte Quiz ist bytegenau übernommen, alle zwölf markierten
Antworten sind fachlich geprüft und der CSV-Validator bestätigt das Format.
Richtige Antwortpositionen sind gleichmäßig verteilt; die Antwortlängen
liefern keinen systematischen Lösungshinweis. SHA-256:
`24f954a9de05a2473aea5e008df2b126e9072703ff301c8771cdb15c87f50225`.

## Ausgaben und abschließende Kontrolle

Nach `source scripts/activate.sh` lief
`python3 scripts/build-materials.py all` erfolgreich: zehn Websitequellen,
neun reguläre PDF-Handouts und zehn Übungs-/Klausurquellen in beiden
PDF-Profilen. Codeprojekt-Manifeste sind nicht vorhanden. Die anschließend
noch korrigierten Umbrüche des Übungsblatts wurden gezielt in beiden
Profilen neu gerendert und in `_site/labs/` sowie `labs/_output/` übernommen.

Alle 59 Vortragsfolien wurden bei 1280 × 720 visuell geprüft. Der
Browserdurchgang bestätigt 59 passende Notizblöcke, keine fehlenden Bilder,
keine MathJax-Fehler und keine Überläufe. Drei neue Mermaid-Diagramme wurden
an die lokale Textbreite angepasst; die Kantenbeschriftungen sind lesbar.
Alle 30 lokalen Ressourcenverweise sind vorhanden. Externe Google-Webfonts
waren in der Umgebung nicht erreichbar; die Prüfung erfolgte mit der
vorgesehenen Ersatzschrift. Mathematik wurde erfolgreich geladen und gesetzt.

Das 46-seitige Skript ist vollständig visuell geprüft. Es enthält alle
59 Folien in Reihenfolge und 59 Notizüberschriften. Nach dem letzten Umbruch
zweier Codezeilen ändern sich nur die Seiten 20 und 23; sie wurden erneut
angesehen. Die übrigen 44 Seiten sind pixelidentisch. Die veröffentlichbare
Website und beide Handout-Pfade entsprechen bytegenau den geprüften Fassungen.
Eine abschließende reine Markdown-Leerzeichenkorrektur erhält nachweislich
den vollständigen Pandoc-AST und damit dieselben Inhalte und Umbrüche.

Aufgabenfassung und Lösungsfassung wurden vollständig angesehen und die
geänderten Seiten erneut kontrolliert. Das endgültige Aufgabenblatt hat
9 Seiten, die Musterlösung 18. Der V2-Codeblock, die MESI- und die
SC-Ablauftabelle stehen zusammenhängend; der optionale C11-Aufruf ist als
kurzer Codeblock umbrochen. Weitere Seiten wurden über pixelidentische
Inhalte zugeordnet, wenn sich allein die Seitenzahl verschob. Eine zusätzliche
Textgeometrieprüfung findet keine Überläufe in beiden Endfassungen. Alle
sechs Aufgaben bleiben in beiden Fassungen vorhanden; sechs Arbeitsräume
stehen nur im Aufgabenblatt, sämtliche Lösungspassagen nur im Lösungsprofil.

Der Quizvalidator bestätigt zwölf Fragen; Bytevergleich mit dem Upload und
SHA-256 stimmen. 26 weitere Kursquellen bleiben unverändert. UTF-8 ohne BOM
für die QMD-Quellen, unveränderte Quiz-BOM und `git diff --cached --check`
sind geprüft. Nicht durchgeführt wurden ein RISC-V-Hardwarelauf, die
optionalen Zeitbenchmarks und eine empirische Kalibrierung der Aufgabenzeiten.
