# Vorlesung 8: überarbeitete Übung und Quiz

Stand: 17. November 2026. Grundlage sind das bereitgestellte zehnseitige
„Übungsblatt 8 (überarbeitet) KI-Beschleuniger & Edge AI.pdf“ und
`quiz_08_ki_beschleuniger_edge_ai_v2.csv`.

## Umfang und Verwendung

Die kanonische Übungsquelle enthält Teil A mit sechs Aufgaben und
44 Orientierungspunkten sowie Teil B mit drei verketteten Aufgaben,
44 Punkten und den geschätzten Zeiten 35 + 20 + 20 = 75 Minuten.
Alle Teilaufgaben des Entwurfs sind mit vollständigen, profilgebundenen
Musterlösungen übernommen. Das Blatt beginnt direkt mit Aufgabe 1.
Die optionalen Rechneraufgaben bleiben zusätzliche Funktionsprüfungen.

Die 180 Minuten Präsenz umfassen weiterhin 110 Minuten Erklärung und
Besprechung, 55 Minuten angeleitete Papierarbeit und 15 Minuten Quiz.
Die Papierphasen verwenden die Auswahl des Uploads:

| Folie | Präsenzaufgaben aus Teil A | Zeit | Nachbereitung |
|---|---|---|---|
| 21 | 1.1, 1.2, 2.1 | 10 min | 1.3–1.4, 2.2–2.4 |
| 31 | 3.1, 3.2, 3.4 | 15 min | 3.3 |
| 40 | 4.1–4.3 | 15 min | 4.4–4.5 |
| 51 | 5.1, 5.3, 6.3 | 15 min | übrige Teile von 5 und 6 |

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
| A4 | Die Welle eines längeren Matrixprodukts vollständig verfolgen und zur allgemeinen Auslastungsformel übertragen; Nullprodukt, leerer Platz und räumliche Belegung unterscheiden. |
| A5 | Negative Zahlen, Nullpunkt, Requantisierung und Akkumulatorgrenzen gemeinsam behandeln; Gewichtsersparnis von Arena-Bedarf trennen. |
| A6 | Speicherbudget mit Objektlebensdauer, Fehlerstatus und Zeigergröße verbinden; Teilbeschleunigung einschließlich Kopie bis zu ihrer Grenze bilanzieren. |
| K1 | Ein Sensorgerät über Formen, Modellbytes, Batching-Wartezeit, Array-Abbildung und Gesamtpfad beurteilen; personenbezogene Datentrennung begründen. |
| K2 | Einen vollständigen Zahlenfall von Realwerten über Integercodes und Bias bis zum Ausgang verfolgen und die Fehlerbeiträge sowie nötige Akkumulatorbreite erklären. |
| K3 | Eine RVV-Schleife vervollständigen und Lane-Rundung, Speicherbandbreite sowie Datenbreite als unterschiedliche Grenzen bewerten. |

Die geänderten Bedingungen verlangen über das Wiederfinden eines
Folienergebnisses hinaus eigene Modellentscheidungen. Rechenroutinen bleiben
als Einstieg enthalten; die längeren Aufgaben verknüpfen mehrere Konzepte.

## Präzisierte Annahmen

- ReLU arbeitet im selben Puffer; Dense-Eingabe und -Ausgabe leben während
  der Schicht getrennt. Damit sind die Aktivierungsspitzen von fünf Byte in
  A1 und 112 Byte in K1 eindeutig. Float32-Quellfenster werden separat gezählt.
- RVV-Fehler werden als Indexsimulation ausgewertet. Außerhalb echter Arrays
  liegende Zugriffe und vorzeichenbehafteter C-Überlauf werden nicht als
  vermeintliche Tests ausgeführt. K3 hat ein nicht überlappendes Ausgabearray.
- Der Zeitvertrag ist Ende von Takt `Start + Latenz − 1`. Array-Auslastung
  nennt ausdrücklich ihre Bezugsmenge: aktive Zellen oder alle physischen Zellen.
- Roofline-Zeiten sind untere Schranken. In K1 scheiden Batches ab drei
  Fenstern schon wegen Wartezeit plus positiver Rechenzeit aus; zwei Fenster
  sind erst mit einer passenden oberen Restzeitschranke fristgerecht.
- Der TFLM-ähnliche Code ist Pseudocode mit ausdrücklich vereinbartem
  Elementanzahl-Parameter. Vier Zeigerbytes sind keine 400 Eingabeelemente.
  Die Stackreserve ist ein Planungsbudget, keine gemessene Hardwaregrenze.

## Quizprüfung

Die zwölf Fragen sind bytegenau übernommen. SHA-256 der kanonischen CSV:
`1a1bee2450a2a5bf8a02c2483f1e515ff68ae77e306922e86bdd9e81fefab310`.
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
| 8 | Systolischen Zeitplan auf 160 MACs und 256 Zell-Takte verallgemeinern. | Anspruchsvolle Herleitung |
| 9 | MAC-Peak in TOPS und eine minimale Taktzahl umrechnen. | Mehrstufige Rechnung |
| 10 | Nullpunkt und Sättigung gemeinsam berücksichtigen. | Fehleranalyse |
| 11 | Einen Fehlerstatus von einer neuen Inferenzentscheidung unterscheiden. | Firmwareentscheidung |
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
