# Vorlesung 8: überarbeitete Übung und Quiz

Stand: 17. November 2026. Grundlage sind das bereitgestellte zehnseitige
„Übungsblatt 8 (überarbeitet) KI-Beschleuniger & Edge AI.pdf“ und
`quiz_08_ki_beschleuniger_edge_ai_v2.csv`. Umfang, Lernziele, Papierphasen und
Quizzuordnung geben den Stand nach der Kürzung vom 26. November 2026 wieder;
Einzelheiten stehen im [Nachtrag](#nachtrag-vom-26-november-2026-npu-gpu-programmierung-statt-array-und-firmware).

## Umfang und Verwendung

Das Übungsblatt enthält Teil A mit fünf Aufgaben und 32 Orientierungspunkten
sowie Teil B mit zwei längeren Aufgaben, 28 Punkten und den geschätzten Zeiten
30 + 20 = 50 Minuten.
Alle Teilaufgaben des Entwurfs sind mit vollständigen, profilgebundenen
Musterlösungen übernommen. Das Blatt beginnt direkt mit Aufgabe 1.
Die optionalen Rechneraufgaben bleiben zusätzliche Funktionsprüfungen.

Die 180 Minuten Präsenz umfassen 105 Minuten Erklärung und Besprechung,
50 Minuten angeleitete Papierarbeit, 15 Minuten Quiz und zehn Minuten Puffer.
Die Papierphasen verwenden folgende Auswahl:

| Folie | Präsenzaufgaben aus Teil A | Zeit | Nachbereitung |
|---|---|---|---|
| 21 | 1.1, 1.2, 2.1 | 10 min | 1.3–1.4, 2.2–2.4 |
| 33 | 3.1, 3.2, 3.4 | 15 min | 3.3 |
| 40 | 4.1–4.3 | 15 min | – |
| 45 | 5.1, 5.2 | 10 min | – |

Teil B gehört zur zusätzlichen selbstständigen Prüfungsvorbereitung. Die
Punkte und Zeiten stammen aus dem Entwurf und sind keine verbindliche
Klausurvorgabe. Empirische Bearbeitungsdaten liegen nicht vor. Die Notizen
und Verweise der vier Papierphasen sind angeglichen. Die anschließende
Folienrevision führt von 70 auf 55 Folien; ihre Daten, neuen Beispiele und
Prüfungen stehen im Bericht `vorlesung-08-ki-einstieg.md`. Das Abschlussquiz
hat zwölf Fragen.

## Lernziele und eigenständige Denkschritte

| Aufgabe | Lernziel und Transfer |
|---|---|
| A1 | Zwei Schichten mit ReLU verfolgen und eine vermeintlich gleichwertige affine Zusammenfassung widerlegen; Parameter, MACs und gleichzeitig lebende Aktivierungen unterscheiden. |
| A2 | Die erforderliche Tilegröße aus der Roofline herleiten und gegen ein Pufferbudget prüfen; mehr Peak mit besserer Wiederverwendung vergleichen. |
| A3 | Zulässige RVV-Längen von einer konkreten Implementierungswahl unterscheiden, einen Zeigerfehler diagnostizieren und Chaining bei geändertem Initiationsintervall beurteilen. |
| A4 | Die NPU-Werkzeugkette auf zwei Plattformen übertragen: portable von herstellergebundenen Ergebnissen trennen, aus Compilerberichten NPU-Abschnitte und Zeiten herleiten und einen herstellereigenen Kernel gegen die Bindung abwägen. |
| A5 | Eingabevertrag eines Sensorfensters bemessen; Teilbeschleunigung einschließlich Kopie bis zu ihrer Grenze bilanzieren. |
| K1 | Ein Sensorgerät über Formen, Modellbytes, Aktivierungslebensdauer, Batching-Wartezeit und Gesamtpfad beurteilen; personenbezogene Datentrennung begründen. |
| K2 | Eine RVV-Schleife vervollständigen und Lane-Rundung, Speicherbandbreite sowie Datenbreite als unterschiedliche Grenzen bewerten. |

Die geänderten Bedingungen verlangen über das Wiederfinden eines
Folienergebnisses hinaus eigene Modellentscheidungen. Rechenroutinen bleiben
als Einstieg enthalten; die längeren Aufgaben verknüpfen mehrere Konzepte.

## Präzisierte Annahmen

- ReLU arbeitet im selben Puffer; Dense-Eingabe und -Ausgabe leben während
  der Schicht getrennt. Damit sind die Aktivierungsspitzen von fünf Byte in
  A1 und 112 Byte in K1 eindeutig. Float32-Quellfenster werden separat gezählt.
- RVV-Fehler werden als Indexsimulation ausgewertet. Außerhalb echter Arrays
  liegende Zugriffe und vorzeichenbehafteter C-Überlauf werden nicht als
  vermeintliche Tests ausgeführt. K2 hat ein nicht überlappendes Ausgabearray.
- Der Zeitvertrag ist Ende von Takt `Start + Latenz − 1`. In A4 kostet jeder
  zusammenhängende NPU-Abschnitt 0,10 ms plus 0,02 ms je enthaltenem Teil;
  die CPU-Zeiten sind vorgegeben.
- Roofline-Zeiten sind untere Schranken. In K1 scheiden Batches ab drei
  Fenstern schon wegen Wartezeit plus positiver Rechenzeit aus; zwei Fenster
  sind erst mit einer passenden oberen Restzeitschranke fristgerecht.

## Quizprüfung

Die Fragen 1–7, 9 und 12 stammen unverändert aus der bereitgestellten CSV
(SHA-256 `1a1bee2450a2a5bf8a02c2483f1e515ff68ae77e306922e86bdd9e81fefab310`).
Die Fragen 8, 10 und 11 wurden am 26. November 2026 ersetzt; die Datei ist
daher nicht mehr bytegleich mit dem Upload.
Die BOM des Uploads bleibt erhalten. Der Formatvalidator bestätigt elf Spalten,
vier Optionen und genau eine richtige Antwort pro Frage.

| Frage | Lernziel und erforderlicher Schritt | Anspruch, eingeschätzt |
|---|---|---|
| 1 | Batching: 25 Parameter von 60 MACs unterscheiden. | Recheneinstieg |
| 2 | Zwei affine Schichten algebraisch zusammenfassen. | Grundlagenverständnis |
| 3 | Leckage bei zufälliger Aufteilung überlappender Fenster erkennen. | Anwendung |
| 4 | Zwei Intensitäten gegen denselben Roofline-Knick prüfen. | Engpassanalyse |
| 5 | Letzten Ergebnistakt aus Latenz und Startabstand herleiten. | Routine |
| 6 | Zulässigen RVV-Spielraum für einen Rest von 50 bestimmen. | Bedingungsanalyse |
| 7 | Int8-Produktgrenzen auf die Akkumulatorbreite übertragen. | Grenzfallanalyse |
| 8 | Startkonfiguration eines GPU-Kernels für 300 Ausgänge bestimmen und die Schutzbedingung für überzählige Threads begründen. | Anwendung, als schwer markiert |
| 9 | MAC-Peak in TOPS und eine minimale Taktzahl umrechnen. | Mehrstufige Rechnung |
| 10 | Folge eines nicht unterstützten Operators für Abschnitte und Übergaben ableiten. | Transfer auf die Werkzeugkette |
| 11 | Beim Herstellerwechsel portable von gebundenen Ergebnissen unterscheiden. | Bewertung der Herstellerbindung |
| 12 | Gesamtzeit einschließlich Übergabe statt nur Dense-Zeit vergleichen. | Systemvergleich |

Alle markierten Antworten sind richtig; die Antwortlängen liefern keinen
systematischen Lösungshinweis. Die Erläuterung zu Frage 2 beschreibt die
allgemeine Wirkung einer Nichtlinearität; Sonderfälle identischer ReLU sind
in A1 ausdrücklich behandelt. Soll auf neue Personen generalisiert werden,
ist wie in K1 eine personenbezogene Trennung nötig; eine aufnahmeweise
Trennung verhindert zunächst Überlappungsleckage.

## Ausgeführte Prüfungen der ersten Übungsrevision

- Alle sechs A-Aufgaben, K1–K3 und ihre vollständigen Musterlösungen wurden
  unabhängig gelesen und numerisch nachgerechnet. Beispiele: A1 ergibt
  $z=[7,-15,-1]^T$, ReLU-Ausgabe 10 statt der affinen Ausgabe $-19$;
  A4 ergibt zwölf gültige MACs und $C=[[-5,12],[13,10]]$. K2 endet mit
  Code 24, Rückwert 0,74 und absolutem Fehler 0,0181; 22 Akkumulatorbits
  genügen für den dort angegebenen Zeilenumfang. K3 hat bei der benannten
  Speichergrenze mindestens 187 Takte, unabhängig von den kürzeren reinen
  Arithmetikfenstern.
- Die bereitgestellte Quizdatei besteht den vorhandenen CSV-Validator mit
  zwölf Fragen; Bytevergleich und SHA-256 bestätigen die unveränderte
  Übernahme. Alle markierten Antworten wurden separat geprüft.
- Das bestehende `labs/src/lab08_dense.c` wurde mit
  `gcc -std=c17 -O2 -Wall -Wextra -Werror -pedantic -fsanitize=address,undefined`
  und `-lm` übersetzt und erfolgreich ausgeführt. Das bestätigt seine
  vorhandenen Hostprüfungen. Die zusätzlich vorgeschlagenen studentischen
  Erweiterungen, eine reale RVV-Ausführung und ein TFLM-Gerätelauf werden
  damit nicht als ausgeführt behauptet.
- Nach `source scripts/activate.sh` lief
  `python3 scripts/build-materials.py all` erfolgreich: zehn Websitequellen,
  neun reguläre PDF-Handouts und zehn Übungs-/Klausurquellen in jeweils
  beiden PDF-Profilen. Keine Codeprojekt-Manifeste vorhanden, daher keine
  neuen Startcode-ZIPs.
- Alle 16 Seiten des Aufgabenblatts und alle 23 Lösungsseiten wurden visuell
  geprüft. Ein fehlendes Mikrosekundenpräfix, eine alleinstehende
  Lösungsüberschrift, zusammengezogene nummerierte Lösungsabschnitte und
  die Trennung von Zeittabelle und Unterfragen wurden korrigiert.
  Betroffene Seiten wurden erneut angesehen. Ein Vergleich der gerenderten
  Seitenbilder bestätigt, dass beide endgültigen Gesamtbuild-PDFs vollständig
  mit den so sichtgeprüften Fassungen übereinstimmen.
- Lösungstrennung zusätzlich am PDF-Text kontrolliert: alle neun Aufgaben in
  beiden Profilen; neun Arbeitsräume und keine Musterlösung im Aufgabenblatt.
  Die zehn Lösungsmarkierungen, mehrere eindeutige Lösungspassagen und die
  optionalen Lösungshinweise erscheinen ausschließlich im Lösungsprofil.
- Die fünf angeglichenen Folien wurden im frischen Reveal.js-Vortrag bei
  1280 × 720 im Browser angesehen und auf Überlauf sowie Notizzuordnung
  geprüft. Im 63-seitigen Handout wurden die zugehörigen PDF-Seiten 3–4,
  26–27, 40–41, 52–53 und 62–63 visuell geprüft. Die übrigen Handoutseiten
  wurden für diesen Auftrag nicht erneut vollständig angesehen.
- Beide Quarto-Quellen sind UTF-8 ohne BOM und Ersatzzeichen; weiterhin
  70 Folien mit 70 Notizblöcken im damaligen Ausgangsstand.
  Die nachfolgende 55-Folien-Fassung wird im separaten Bericht geprüft. Die 27 übrigen Kursquellen sind per SHA-256
  unverändert. `git diff --check` ohne Befund.

## Nachtrag vom 26. November 2026: NPU-/GPU-Programmierung statt Array und Firmware

Die Vorlesung wurde ab der Folie „Eine Zelle rechnet und reicht weiter“ stark
gekürzt. Entfallen sind die Detailfolien zum systolischen Array, die
TPU-Peak-Folie, Papierphase 3 zum Array und der Firmwareabschnitt mit
Speicherplanung, Quantisierungsformeln und TFLM-Initialisierung. Neu ist der
Abschnitt „Beschleuniger programmieren“: ein CUDA-Lehrkernel für eine
Dense-Schicht, die NPU-Werkzeugkette mit Modellcompiler am Beispiel Vela,
Ursachen des Vendor-Lock-in und Maßnahmen zu seiner Begrenzung. Der Abschnitt
zur Gesamtbilanz mit Amdahl bleibt als fünfter Abschnitt erhalten. Die
Vorlesung hat jetzt 49 Folien in fünf Abschnitten; die Requantisierungsformel
steht kompakt auf der Folie „Schmal speichern, breit rechnen“. Das
Mermaid-Diagramm der NPU-Folie begrenzt wie in Vorlesung 9 eine
foliensatzlokale Regel in `assets/styles/ki-beschleuniger.css` auf die Breite
der Textspalte. Ohne diese Regel skaliert `mermaid-fit` breite Diagramme über
die 920 px breite Spalte hinaus, und der rechte Teil wird abgeschnitten.

Im Übungsblatt entfallen die Array-Aufgabe, die Quantisierungsaufgabe, die
Teile zu Speicherbudget und TFLM-Lebensdauer, die Array-Teilaufgabe von K1
und die quantisierte Dense-Zeile K2. Neu ist A4 „Ein Modell, zwei
NPU-Plattformen“; die frühere K3 heißt jetzt K2. Die Optionalaufgaben zum
Matrixprodukt aus der Array-Aufgabe und zu den Quantisierungsfällen entfallen.

Prüfnotiz zu den neuen Quizfragen: Frage 8 verlangt die Übertragung der
Startrechnung von der Folie auf 300 Ausgänge und die Begründung der
Schutzbedingung. Frage 10 überträgt das Verhalten nicht unterstützter
Operatoren auf einen Operator in der Mitte des Graphen. Frage 11 verlangt die
Unterscheidung portabler und herstellergebundener Ergebnisse. Der Anspruch ist
eingeschätzt; studentische Bearbeitungsdaten liegen nicht vor. Die richtigen
Antworten stehen an den Positionen 2, 3, 1, 4, 2, 1, 3, 4, 4, 1, 3, 2.

Belege: Die Vela-Beschreibung auf PyPI wurde in dieser Sitzung gelesen; sie
bestätigt, dass Vela beschleunigbare Teile durch einen Ethos-U-Operator
ersetzt und nicht beschleunigbare Teile unverändert lässt. Die Seiten zu CUDA,
HIP, OpenCL und ONNX waren aus der Prüfumgebung nicht erreichbar; die
zugehörigen Aussagen sind allgemein gehalten und auf der Quellenfolie
verlinkt. Der CUDA-Ausschnitt ist eigener Lehrcode und wurde nicht auf einer
GPU ausgeführt.
