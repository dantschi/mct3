# CPU-Architekturen und KI-Beschleuniger: Erweiterung vom 11. November 2026

## Aktuelle Auswahl und Voraussetzungen

Die README zeigt die Einheiten 1, 2, 3, 7, 8 und 9. Die Folien, Übungen und
Quizdateien der Einheiten 4–6 bleiben vollständig im Repository erhalten.
Die Nummerierung und vorhandenen Downloadpfade werden beibehalten.
Beschreibung, Lernziele und roter Faden der sichtbaren Übersicht sind angepasst.

Die Einheiten 7 und 8 setzen keine Inhalte der ausgeblendeten Einheiten voraus.
Sie knüpfen an Speicher, Caches, Register, Interrupts und Exceptions aus den
Einheiten 1–3 an. Auch der ausdrückliche DMA-Vorwissensverweis in Einheit 9
ist durch eine lokale Erklärung der Datenzuständigkeit ersetzt. Die Regeln in
AGENTS und die neuen Grundbegriffe im Glossar passen zu dieser Auswahl.

## Vorlesung 7: vom einzelnen Befehl zur superskalaren Ausführung

Die Einheit enthält jetzt 70 Folien mit 70 ausgearbeiteten Notizblöcken,
also 20 zusätzliche Folien einschließlich fünf Abschnittstrennern,
Einstiegsfrage, späterer Rückbindung und 13 Grundlagenfolien.

Die fünf Abschnitte führen durch Befehlsweg/Pipeline, Breite/Abhängigkeiten,
Reihenfolge/Bestätigung, Sprungvorhersage und Compilerwirkung. Eine kurze
Abschnittsmarkierung unterstützt die Orientierung zwischen den Trennern.
Alle bestehenden Fachthemen und die ausdrücklich getrennten Modelle M1,
M2 und M3 bleiben erhalten. Der frühere Einstieg ist auf Speicher und
Unterbrechungen bezogen; DMA wird nicht vorausgesetzt.

Die zusätzliche Einführung erklärt:

- C-Ausdrücke, Maschinenbefehle, Operanden und benötigte Datenwege;
- Durchlaufdauer eines Befehls gegenüber Ergebnisrate einer gefüllten Pipeline;
- skalare Pipeline gegenüber mehreren Starts pro Takt;
- unabhängige Summen, echte Werteabhängigkeiten und begrenzte Rechenressourcen;
- Start, Fertigstellung und geordnete Bestätigung mit festgelegten Zeitpunkten;
- die getrennten Entscheidungen Superskalarität, Out-of-Order, SIMD und Multicore.

Drei neue eigene Abbildungen zeigen Wertefluss, 20 gegenüber acht Takten
für vier Befehle mit je fünf Schritten sowie einen zweifachen Start mit
abhängigem Verbraucher. Ihre Generatoren und SVG-/PNG-Dateien liegen mit
Präfix `intro_` im Abbildungsordner der Einheit. Es handelt sich um berechnete
Lehrabläufe, nicht um Messungen an einem realen Prozessor.

## Vorlesung 8: von KI-Software zur Matrixrechnung

Auch diese Einheit enthält 70 Folien mit 70 Notizblöcken. Die 20 zusätzlichen
Folien umfassen sechs Abschnittstrenner, Einstiegsfrage, Rückbindung und
zwölf grundlegende Erklärungen. Die bisherigen Fachinhalte und Codebeispiele
bleiben erhalten.

Die sechs Abschnitte verbinden Modell/Matrix, Rechenarbeit/Daten,
Vektorverarbeitung, systolische Arrays, Firmware und die Gesamtanwendung.
Für den Einstieg sind keine KI-Softwarekenntnisse erforderlich. Er erklärt
Sensorfenster und Vorverarbeitung, Modelleingaben und gelernte Parameter,
Training, Validierung, Test und Inferenz.

Von einer einzelnen gewichteten Summe führt der Lernweg über Bias und ReLU
zu mehreren Neuronen, Matrixformen und mehreren Eingabespalten. Voraktivierung
und Aktivierung werden getrennt; bei mehreren Eingaben wird der Bias je
Spalte angewandt, ohne neue Parameter zu erzeugen. Mehrere affine Schichten
ohne Nichtlinearität bleiben insgesamt affin. So wird begründet, weshalb
Matrixprodukte und Wiederverwendung für viele neuronale Netze zentral sind,
ohne jede KI auf Matrixrechnung zu reduzieren.

Drei neue eigene Abbildungen zeigen ein Neuron mit ReLU, die Auswahl von
Gewichtszeile und Eingabespalte sowie die Verkettung mehrerer Schichten.
Die Zahlen sind von Hand gesetzte Lehrwerte und keine Trainingsergebnisse.
Beim Übergang zum bestehenden Dense-Beispiel wird die geänderte Form und
die dort bewusst fehlende Aktivierungsfunktion erklärt.

## Lernnotizen, Übungen und Zeitplanung

Alle bisherigen und neuen Notizen sind als zusammenhängende Buchprosa mit
Übergängen überarbeitet. Regieanweisungen und instabile Foliennummerverweise
sind durch fachliche Erklärungen ersetzt. Bestehende Beispiele, Quellen,
Modellgrenzen und Codeblöcke bleiben erhalten. Die Begriffe sind mit dem
ergänzten Kursglossar abgeglichen.

Die vorhandenen Übungen und Quizdateien zu 7 und 8 bleiben bestehen und
werden durch die erhaltenen Fachinhalte weiterhin abgedeckt. Die neuen
Grundlagenfolien enthalten zusätzliche Denkfragen und vollständig erläuterte
Rechenbeispiele. Eine Überarbeitung aller Quizfragen war nicht Teil dieses
Auftrags; die entsprechenden früheren Reviewbefunde bleiben separat dokumentiert.

Der Plan bleibt bei je 180 Minuten einschließlich Übungen und Quiz. Die
zusätzlichen Folien teilen Grundideen in kleinere Schritte; der Lerntext
ist kein Wort-für-Wort-Vortragsskript. Einzelne Implementierungsdetails der
CPU-Einheit sind als Vertiefung zur Lektüre gekennzeichnet. Tatsächliche
Bearbeitungs- und Vortragszeiten sind weiterhin empirisch zu kalibrieren.

## Ausgeführte Prüfungen

- Quellenstruktur, UTF-8 ohne BOM, passende Notizzuordnung und vorhandene
  Bildpfade: je 70 Folien, je 70 Notizen und je drei neue eigene Abbildungen.
- Unabhängiger fachlicher Vergleich beider vollständiger Quellen mit den
  ursprünglichen 50-Folien-Fassungen. Die alten Codeblöcke sind erhalten.
  Ein uneinheitliches „Initiierungsintervall“ wurde zu „Initiationsintervall“
  vereinheitlicht. Keine fachliche Regression wurde festgestellt.
- Neue Zahlenfälle unabhängig nachgerechnet: vier Befehle/fünf Schritte
  benötigen ohne Überlappung 20 und in M1 acht Takte. Der neue M2-Fall
  startet in 1/1/2/2 und bestätigt in 2/2/3/3; die abhängige Viererkette
  erreicht ihre letzte Bestätigung erst in Takt fünf.
- Für das neue KI-Beispiel ergeben sich Voraktivierung `[1, -3]`, ReLU
  `[1, 0]` und bei zwei Eingaben `[[1, 11], [-3, 5]]` vor der Aktivierung.
  Formen, Bias-Wiederholung und die Schichtausgabe zwei wurden geprüft.
- Alle sechs neuen PNGs tatsächlich angesehen und ihre SVG-Quellen geprüft.
- Frische Reveal.js-Fassungen mit Quarto 1.11.9 erzeugt und alle 140 Folien
  in Chromium mit gesetzten Formeln auf Überlauf, Bildfehler und Notizzuordnung
  geprüft. Die gefundenen Platzprobleme wurden behoben; anschließend waren
  diese Prüfungen fehlerfrei. Neue Grundlagen- und Abschnittsfolien wurden
  zusätzlich anhand von Screenshots angesehen.
- Beide HTML-Lesefassungen erzeugt und im Browser kontrolliert: je 70 sichtbare
  Notizabschnitte, keine fehlenden Bilder. Sie liegen unter
  `_handout/vorlesungen/07_moderne_cpu_architekturen.html` und
  `_handout/vorlesungen/08_ki_beschleuniger_edge_ai.html`.
- Die gerenderte Startseite verlinkt die aktuelle Auswahl; Materialdateien
  der Einheiten 4–6 sind per SHA-256 als unverändert bestätigt.
- Die beiden Quizdateien bestehen den vorhandenen CSV-Validator. Die
  vorhandenen Hostprogramme `lab07_ilp.c` und `lab08_dense.c` wurden mit
  C11, strengen Warnungen, Address-/UndefinedBehaviorSanitizer und beim
  Dense-Programm `-lm` übersetzt und erfolgreich ausgeführt.
- `git diff --check` ohne Fehler.

## Grenze des vollständigen Builds

Der gemeinsame vollständige Build wurde ausgeführt. Alle zehn Websitequellen
wurden gerendert; der anschließende reguläre Handoutlauf scheiterte bereits
bei Einheit 1 am fehlenden `luatexbase.sty` in der installierten TeX-Umgebung.
Eine aktuelle Freigabe der regulären PDF-Handouts und Lab-PDF-Profile liegt
deshalb nicht vor. Alte PDFs werden nicht als Nachweis verwendet. Die
HTML-Lesefassungen benötigen kein LaTeX und wurden unabhängig davon geprüft.
Der gezielte gemeinsame Website-Build (`python3 scripts/build-materials.py website`)
war anschließend erfolgreich und hat die aktuelle Startseite und die Vorträge
unter `_site/` bereitgestellt. Dieser Teilerfolg ersetzt nicht den vollständigen
Build einschließlich PDF-Ausgaben.
Es wird keine RISC-V-Firmwareausführung oder Messung realer Laufzeit behauptet.
