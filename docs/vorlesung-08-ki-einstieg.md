# Vorlesung 8: vom Messsignal zum Beschleuniger

Stand: 17. November 2026. Grundlage sind die bereitgestellten Hinweise zum
KI-Einstieg und die unmittelbar zuvor überarbeiteten Übungen und Quizfragen.
Der zugehörige Übungsbericht steht in
[vorlesung-08-transferaufgaben.md](vorlesung-08-transferaufgaben.md).

## Ziel und Aufbau

Die Einheit führt Studierende ohne vorausgesetzte KI-Softwarekenntnisse von
Beschleunigungsmessungen zu einem kleinen Modell und dessen Rechen-, Daten-
und Speicherbedarf. Am Ende sollen sie eine lokale Hardware- und Firmwarewahl
anhand des gesamten Auswertungspfads begründen können. Vorwissen aus den
sichtbaren Vorlesungen 1–3 und 7 genügt; die ausgeblendeten Einheiten 4–6
werden nicht vorausgesetzt.

Die Fassung hat 55 Folien statt 70, jeweils mit einem vollständigen
Notizblock. Der Notizumfang sinkt von 13.896 auf 7.491 Wörter, bei
vollständiger Erklärung der wesentlichen Rechenwege. Sechs Abschnittsfolien und Abschnittsangaben halten den aktuellen
Gedankengang sichtbar. Die Notizen erläutern Zusammenhänge als fortlaufenden
Lerntext, mit einer Kernaussage am Anfang und ausgearbeiteten Rechenwegen.
Annahmen der Hardwaremodelle sind an den Abschnittseinstiegen gebündelt;
relevante lokale Grenzen bleiben bei der jeweiligen Rechnung erhalten.

| Folien | Funktion im Gedankengang |
|---|---|
| 1–4 | Eigene Entscheidungsregel vorschlagen, Vorwissen und Ablauf einordnen. |
| 5–15 | Echte Verläufe und Punktwolken lesen; Trenngerade, Bias, ReLU, Scores und einen Gradientenschritt erklären; danach Training, Datentrennung, FIR-Brücke und Matrixformen einführen. |
| 16–21 | Parameter von Arbeit trennen, Roofline und Wiederverwendung bilanzieren. |
| 22–31 | SIMD, Latenz, Initiationsintervall, RVV und Chaining unterscheiden. |
| 32–40 | Lokale Produktsummen, systolische Welle und Auslastung herleiten. |
| 41–46 | Flash, Arena, Quantisierung, Produktskalen und Initialisierung verbinden. |
| 47–52 | Mit Amdahl den Gesamtpfad beurteilen, Einstiegsfrage beantworten, Papierphase und Abschlussquiz. |
| 53–55 | Glossar, Quellen und eigener Messversuch als Hintergrund. |

Kurze Vorhersagefragen stehen vor der Auflösung, unter anderem bei den
Messverläufen, der Biasänderung, mehr Peak, der Arraywelle und dem
Gesamtgewinn. Die zwölf bereitgestellten Quizfragen bleiben unverändert als
Abschlusskontrolle erhalten. Für die Zwischenfragen werden keine vollständigen
Quizlösungen vorweggenommen.

## Reale Messdaten und ausführbares Lehrmodell

Die mitgelieferten MotionSense-Daten stammen aus dem gepinnten öffentlichen
Datensatzstand, einschließlich Original-MIT-Lizenz, Herkunft und
Einheitenbelegen. Es werden 36.864 unveränderte XYZ-Messzeilen von 24 Personen
verwendet: Stehen, Gehen und Joggen, nominell 50 Hz und Einheit g einschließlich
Gravitation. Daraus entstehen 1.152 nicht überlappende Fenster mit je
32 Zeitpunkten und drei Achsen. Der Datenumfang wird unabhängig vom späteren
Modellergebnis durch eine feste Auswahlregel bestimmt.

Das Hauptmodell besitzt 96 Eingänge, 16 ReLU-Neuronen und drei Scores.
Personen 1–16 liefern 768 Trainingsfenster, 17–20 liefern 192
Validierungsfenster und 21–24 liefern 192 Testfenster. Mittelwerte und
Standardabweichungen werden ausschließlich auf Trainingspersonen bestimmt.
Das Skript optimiert in Float64 und exportiert Gewichte sowie Normalisierung
nach Float32; die angegebenen Kennzahlen werden mit diesem Export erneut
berechnet. Architektur, 600 Epochen, Lernrate 0,003, Batchgröße 64 und Seed
20261117 sind vor dem Test festgelegt. Es wird kein Checkpoint anhand der
Validierungs- oder Testwerte ausgewählt.

| Rolle | Richtige Vorhersagen | Anteil |
|---|---:|---:|
| Training | 768 / 768 | 100 % |
| Validierung | 157 / 192 | 81,77 % |
| Test | 159 / 192 | 82,81 % |

Das vorab bestimmte Beispiel Person 21, Gehen, Fenster 0 ergibt die Scores
−6,243 / 0,901 / −1,240 und damit Index 1, Gehen. Das Modell ist ein
nachvollziehbarer Lehrversuch; das Gefälle zwischen Trainings- und Testgüte
gehört zur Diskussion und belegt keine allgemeine Aktivitätserkennung.
Die 1.603 Netzwerkparameter benötigen als rohe Float32-Werte 6.412 Byte;
die 192 Normalisierungswerte zusätzlich 768 Byte. JSON-Dateigröße,
Laufzeitspeicher und gemessene eingebettete Ausführungszeit werden damit
nicht gleichgesetzt.

Das Skript `code/vl08_activity_demo.py` und das kurze aufrufende Notebook
wurden tatsächlich ausgeführt. Geprüfte Umgebung: Python 3.12.14,
NumPy 2.3.5, Matplotlib 3.10.8. Aus dem Repository-Stamm:

```bash
python3 code/vl08_activity_demo.py
```

Die sechs selbst erzeugten Diagramme bleiben als PNG und SVG mit
Erzeugungscode erhalten. Zwei Merkmale dienen allein der anschaulichen
Geometrie; sie sind kein stiller Ersatz für die 96 Rohwerte des Netzes.
Trenngeraden, Raute aus vier ReLUs und Ein-Parameter-Gradient sind ausdrücklich
separate mathematische Lehrbeispiele. Insbesondere erzwingen drei Klassen
allein keine verborgene Schicht. Die tatsächliche Optimierung mit Adam wird
nicht als der einzelne gezeigte Gradientenschritt ausgegeben.

## Umsetzung der fachlichen Hinweise

- Conv1D wird als bekannte lokale FIR-Rechnung mit gelernten Koeffizienten
  erschlossen; Kreuzkorrelation, mehrere Kanäle und nachfolgende Aktivierung
  sind ausdrücklich eingeordnet.
- Amdahls Gesetz erhält seinen Namen und berücksichtigt zusätzliche
  Übergabekosten. Ein schneller Dense-Kern ist damit noch kein gleicher
  Gewinn für die vollständige Entscheidung.
- Das kleine Hauptmodell passt als Float32-Gewichtssatz in das gezeigte
  Flashbudget. Eine gegenteilige Behauptung wird nicht zur Motivation der
  Quantisierung verwendet. Das größere fiktive Budget bleibt separat.
- Die LSM6DSOX-Alternative wird am ST-Beispiel eines Entscheidungsbaums
  belegt. Eine ungeprüfte Zahl parallel arbeitender Bäume wird nicht übernommen.
- LiteRT wird als Fortsetzung der TensorFlow-Lite-Werkzeugfamilie eingeordnet.
  Die gepflegte Mikrocontroller-Laufzeit heißt im gelesenen Repository
  weiterhin TensorFlow Lite for Microcontrollers, TFLM. Vorhandene API-Namen
  werden erhalten. Herstellerwerkzeuge werden als weitere Wege genannt.
- Roofline wird mit Williams, Waterman und Patterson (2009), der systolische
  Ansatz mit Kung (1982) referenziert. Abbildungen aus diesen Artikeln werden
  nicht übernommen.
- Das Glossar erhält die aktuellen Einführungsstellen und weitere Begriffe
  zur Geometrie, Datenversorgung und Firmware. Abkürzungen werden bei ihrer
  Einführung erklärt und anschließend gezielt wiederverwendet.

## Übungsphasen und zeitlicher Rahmen

Das 180-Minuten-Budget umfasst 110 Minuten Erklärung, kurze Vorhersagen und
Besprechung, 55 Minuten Papieraufgaben sowie 15 Minuten Abschlussquiz. Die
vier Themenblöcke dauern einschließlich Papierarbeit 40, 40, 40 und
60 Minuten; sie werden nicht mit vier einzelnen Schulstunden verwechselt.
Die Hintergrundfolien 53–55 verlängern den geplanten Pflichtvortrag nicht.

| Nach Folie | Teil A des Übungsblatts | Papierzeit |
|---|---|---:|
| 21 | 1.1, 1.2, 2.1 | 10 min |
| 31 | 3.1, 3.2, 3.4 | 15 min |
| 40 | 4.1–4.3 | 15 min |
| 51 | 5.1, 5.3, 6.3 | 15 min |

Die verbleibenden Teilaufgaben und Teil B sind Nachbereitung. Die
Bearbeitungszeiten sind Planungsannahmen und keine empirisch kalibrierten
Zusagen. Weder daraus noch aus einer Folienmarkierung wird eine offizielle
Klausurrelevanz abgeleitet. Folienverweise im Übungsblatt wurden von 63 auf
42, von 42 auf 28 und zweimal von 54 auf 38 umgestellt.

## Prüfung und Grenzen

Alle 55 Folien mit ihren Notizen wurden fachlich gegengelesen. Eine davon
unabhängige Rechnung mit exportierten Gewichten reproduziert die drei
Konfusionsmatrizen und die Beispielentscheidung. Die ausschließlich auf
Trainingspersonen bestimmte Normalisierung und die Speicherzahlen wurden
neu berechnet. Die Gradienten des ausführbaren Trainings wurden zusätzlich
mit zentralen Differenzen geprüft; der größte Fehler lag bei
$1{,}92\cdot10^{-10}$. Datenauswahl und Dateihashes sind reproduzierbar.

Ein TFLM-Export, ein Mikrocontrollerlauf und eigene phyphox-Messungen sind
weiterführende Schritte und wurden nicht als ausgeführt behauptet.

Die Browserprüfung bei 1280 × 720 umfasst alle 55 Folien: vollständige
Notizzuordnung, keine fehlenden Bilder, keine MathJax-Fehler und keine
abgeschnittenen Elemente. Alle Folien wurden zusätzlich visuell angesehen.
Die Messkurven und Punktwolken wurden anschließend vergrößert und erneut
geprüft; die vereinfachte argmax-Schreibweise vermeidet mehrdeutige
Dezimalkommas. Externe Google-Webfonts waren in dieser Umgebung nicht
erreichbar, daher erfolgte die Sichtprüfung mit der vorgesehenen
Ersatzschrift. MathJax selbst wurde erfolgreich geladen und gesetzt.

Nach `source scripts/activate.sh` war der vollständige Lauf
`python3 scripts/build-materials.py all` erfolgreich: zehn Websitequellen,
neun PDF-Handouts und zehn Übungs-/Klausurquellen in beiden PDF-Profilen.
Codeprojekt-Manifeste sind nicht vorhanden, daher entstehen keine neuen
Startcode-ZIPs. Zwei bei der PDF-Sichtprüfung gefundene Stellen wurden vor
Abschluss des Laufs gezielt neu gerendert: ein zu langer Codekommentar und
ein nicht zur Abbildung passender Hinweis auf einen roten Rand. Zusätzlich
wurde der Tabellenkopf der Ablaufplanung gekürzt.

Das endgültige 44-seitige Skript wurde vollständig visuell geprüft. Es
enthält alle 55 Folien in Reihenfolge und 55 zugehörige Notizüberschriften.
Nach den letzten Korrekturen unterscheiden sich nur die Seiten 2, 14 und 37;
diese wurden erneut angesehen, die übrigen 41 Seiten sind pixelidentisch.
Die veröffentlichbaren Dateien in `_site/` und `_handout/` entsprechen
bytegenau den geprüften Endfassungen. Auch der erneute Browserdurchgang über
alle 55 Folien meldet keine Überläufe, fehlenden Bilder oder MathJax-Fehler.
Alle 31 lokalen Bild-, Skript-, Stylesheet- und Downloadverweise sind
vorhanden. Glossar, Trainingscode, Notebook, CSV und Lizenz werden als
geprüfte Website-Ressourcen mit ausgeliefert.

Die Übung hat weiterhin 16 Aufgabenseiten und 23 Lösungsseiten. Der Vergleich
mit der zuvor vollständig sichtgeprüften Fassung bestätigt ausschließlich
die vier erwarteten Foliennummernänderungen im PDF-Text. Nur drei
Aufgabenseiten und vier Lösungsseiten ändern ihr Seitenbild; diese sieben
Seiten wurden erneut vollständig visuell geprüft. Alle anderen Seiten
sind pixelidentisch. Die Lösungstrennung bleibt erhalten. Der
Quizvalidator bestätigt zwölf Fragen; SHA-256 und Bytevergleich bestätigen
die unveränderte Übernahme des Uploads. 28 unbeteiligte Kursquellen bleiben
per SHA-256 unverändert. UTF-8-Prüfung und `git diff --check` sind ohne Befund.

Beim abschließenden Git-Check wurden ausschließlich automatisch erzeugte
Leerzeichen an SVG-Zeilenenden entfernt. Der Generator normalisiert diese
Ausgabe nun selbst. Sein erneuter vollständiger Lauf erzeugt byteidentische
PNGs und Modelldaten; die im Vortrag und Skript verwendeten Bilder ändern
sich dadurch nicht. Auch dieser Stand besteht `git diff --cached --check`.
