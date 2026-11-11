# Review der Vorlesungen 4 bis 9

Stand: 11. November 2026. Geprüfter Ausgangsstand: `4f24a76`.

Der Review folgt dem vorhandenen Skill
[material-review](../.agents/skills/material-review/SKILL.md) und den Projekt-,
Fach-, Folien- und Quizregeln. Die Prüfung erfolgt in der Reihenfolge 4–9.
Sie verändert keine Lehrinhalte. P1 bezeichnet einen Fehler mit unmittelbarer
Folge für die fachliche Korrektheit oder Lösbarkeit; P2 eine relevante
Präzisierung oder didaktische Verbesserung; P3 eine kleinere Ergänzung.
Sichere Fehler, Verbesserungen und offene Nachweise werden unterschieden.

Zielgruppe und Rahmen: fünftes Bachelorsemester EIT, vorhergehende MCT-Inhalte,
je Einheit 180 Minuten einschließlich angeleiteter Übung und Quiz.
Ein offizielles Modulhandbuch und empirische Bearbeitungsdaten liegen nicht vor.
Prüfungsnähe wird deshalb nur gegenüber der vorhandenen Probeklausur und den
dokumentierten Lernzielen beurteilt, nicht als gesicherte Klausurprognose.

## 1. Vorlesung 4: Aktorik und Sicherheit

**Umfang und Urteil.** 50 Folien mit 50 zugeordneten Notizblöcken, sechs
Pflichtaufgaben mit Musterlösungen, zehn Quizfragen und die zugehörigen
Diagrammquellen. Der fachliche Lernweg trägt: Zähltakt → Periode und Compare →
Signalwirkung → Aktualisierung → Überwachung und Aktorzustand. Das explizite
Lehrmodell verhindert eine falsche Gleichsetzung der Peripherieregister mit
einem RISC-V-Standard. Besonders gelungen sind Active-Low, Effektivwert,
Preload, zeitliche Watchdoggrenzen und die Abgrenzung von Reset und Sicherheit.

### Befunde

- **P2, sichere begriffliche Unschärfe:**
  [Notizen zur Leistung, Zeile 404](../vorlesungen/04_aktorik_sicherheit.qmd#L404)
  nennen die „volle Pulsleistung“ viermal so groß wie die Leistung einer
  konstanten Mittelwertspannung. Die vorausgehenden Formeln sind korrekt:
  mittlere PWM-Leistung 2,7225 mW, konstante 0,825 V an 1 kΩ 0,680625 mW.
  Deren Quotient ist vier. Die momentane HIGH-Leistung bei 3,3 V ist dagegen
  10,89 mW, also sechzehnmal so groß. **Vorschlag:** „mittlere Leistung des
  ungefilterten PWM-Signals“ schreiben und die momentane Leistung ausdrücklich
  davon abgrenzen. Sonst wird die gerade eingeführte Unterscheidung von
  Mittelwert und Momentanwert wieder verwischt.
- **P2, didaktische Verbesserung:**
  [Erste inhaltliche Folie, Zeile 13](../vorlesungen/04_aktorik_sicherheit.qmd#L13)
  erklärt den Anschluss an VL3, stellt aber keine aktivierende Frage; danach
  folgen bereits Voraussetzungen und Ablauf. Die erste Rechenfrage steht erst
  bei [Zeile 265](../vorlesungen/04_aktorik_sicherheit.qmd#L265).
  **Vorschlag:** den vorhandenen Einstieg um „Die Software hängt, der Motor
  läuft weiter – ist der Timer defekt?“ als begründete Vorhersage ergänzen,
  Antworten zwei Minuten sammeln und bei „Was passiert, wenn das Hauptprogramm
  hängt?“ sowie „Reset und Aktorzustand“ ausdrücklich wieder aufnehmen.
- **P2, didaktische Verbesserung:**
  [Quiz, Zeilen 2–5, 7 und 9](../quizacademy/quiz_04_aktorik_sicherheit.csv#L2)
  verwendet dieselben Zahlen bzw. Fälle wie die gelösten Folien: 100 MHz/99/999,
  3,3 V/25 %, Active-Low mit 1000/250, Auf/ab-Zyklus mit ARR 4, gleich um 5 µs
  verschobene Flanken und Feeds 0/0,5/1 s bis Reset bei 3 s. Als kurze Einstiegsdiagnose
  ist das brauchbar; für die genannten Anwendungsziele prüft der Satz zu häufig
  Wiedererkennen. **Vorschlag:** wenige Routinefragen behalten, übrige Fragen als
  Entscheidung aus Anforderungen oder Fehlerdiagnose gestalten, beispielsweise
  zwei Timerkonfigurationen bei geforderter Pulsbreite vergleichen oder einen
  trotz gültigem Fenster unzureichenden Fortschrittsnachweis beurteilen.
- **P2, Darstellungsverbesserung:**
  [Generator, Zeile 165](../assets/figures/04_aktorik_sicherheit/build_figures.py#L165)
  zeichnet das Raster von `resolution.png` mit 0,6 SVG-Einheiten breiten Linien
  im Abstand 0,62 und Farbe `#E5E5EA`. Die Grafik zeigt dadurch bereits als PNG
  überwiegend eine helle Fläche; einzelne Compare-Schritte sind kaum erkennbar.
  Gegen Weiß beträgt der Kontrast etwa 1,26:1. **Vorschlag:** die maßstäbliche
  Übersicht behalten, daneben einige Ticks vergrößert und mit dunkleren,
  ausreichend dicken inhaltstragenden Linien zeigen.

### Aufgaben, Niveau und Prüfungsvorbereitung

| Aufgabe | Lernziel und eigener Denkschritt | Einschätzung |
|---|---|---|
| 1 | Zähltakt, Puls und Periodengrenze herleiten; geändertes ARR und getrennte Auf/ab-Konvention auswerten | Routine mit sinnvollen Grenzfällen; etwa 10–12 min |
| 2 | Mittelwert, Effektivwert und Lastleistung trennen; Polarität übertragen | Anwendung bekannter Formeln; etwa 10–12 min |
| 3 | verspätete Flanken und ungepufferten Registerwechsel auf einer Zeitachse rekonstruieren | eigenständige Ablaufanalyse; etwa 10–15 min |
| 4 | Kommandoformat dimensionieren, Rundung und Hüllkurve auswerten | Anwendung und Codeverständnis; etwa 10–12 min |
| 5 | Timeout vom letzten Feed und Taktgrenzen herleiten; Fenster prüfen | zeitliche Analyse; etwa 10–12 min |
| 6 | neue Fortschrittsrunde und Resetfolgen begründen | Entwurfsentscheidung; etwa 8–12 min |

Damit sind die 60–75 Minuten des Blatts als Schätzung plausibel. Die im
Unterricht vorgesehenen 55 Minuten erfordern Auswahl und gemeinsame Besprechung,
wie die Notizen bereits erklären. Der Lab-Satz enthält gegenüber den Folien neue
Zahlen und bei Aufgaben 3/5/6 zusätzliche Ablauf- bzw. Entwurfsentscheidungen.
Die Quizfragen 1–4 sind überwiegend Rechen-/Begriffsroutine, 5–10 unterscheiden
bereits erklärte Ursachen und Zustände. Ein Punkt allein liefert keine
allgemeine selbstständige Entwurfsleistung. Antwortlängen und Positionen zeigen
im Satz keinen durchgehenden verlässlichen Lösungshinweis.

**Nachgerechnet:** 48 MHz/24/1200 = 1666,667 Hz; ARR 1200 → 1665,279 Hz und
39,9667 %; Widerstandslast 1,8 V/3 V/4,5 mW; verzögerter Puls 115 µs mit
39,1304 %; Stellformat ARR 49999/CCR3600; Watchdoggrenzen 2,60870–3,52941 s.
Das RC-Modell ergibt 0,794325–0,856190 V, also 61,865 mV Restwelligkeit.
Die sechs Musterlösungen und zehn richtigen Quizoptionen passen zu den
vorgegebenen Lehrannahmen. Keine simulierte Hardware- oder elektrische Messung.

**Terminologie und Grenzen.** Die Begriffe PWM, Tastverhältnis und Watchdog
passen zum Glossar; Registerwert, tatsächlicher Teiler und Timer-Tick bleiben
sauber getrennt. Herstellerlinks sind vorhanden, aber keine festgehaltenen
Dokumentrevisionen/Abschnitte. Konkretes Pin-/Resetverhalten bleibt zu Recht
plattformabhängig. Sichtgeprüft wurde hier insbesondere das vorhandene
`resolution.png`; es wird keine frische HTML-/PDF-Freigabe behauptet.

## 2. Vorlesung 5: Serielle Bussysteme

**Umfang und Urteil.** 50 Folien und Notizblöcke, sechs Pflichtaufgaben mit
Musterlösungen, zehn Quizfragen und 20 SVG-Diagrammquellen. Der Aufbau von
Bitfolge über UART/SPI/I²C zum gültigen Sensorwert ist nachvollziehbar.
Besonders sorgfältig sind die Trennung von Rahmen und elektrischen Pegeln,
FIFO-voll gegenüber Overrun, ACK-Rollen, Arbitration-Bereinigung und die
portable Zweierkomplement-Decodierung. Der Gerätevertrag und die Grenzen
idealer Zeitdiagramme sind ausdrücklich benannt.

### Befunde und Verbesserungen

- **P2, didaktische Verbesserung:**
  [Einstieg, Zeile 13](../vorlesungen/05_serielle_bussysteme.qmd#L13)
  enthält eine erklärende Brücke; nach ihr folgen Voraussetzungen und Agenda.
  Eine Vorhersagefrage vor der Erklärung fehlt. **Vorschlag:** „Auf der Leitung
  kommen sechs fehlerfreie Bytes an – haben wir damit bereits einen neuen
  gültigen Messwert?“ Zunächst Gegenbeispiele sammeln, später bei „Erfolg
  prüfen, dann Daten übernehmen“ und im Abschluss mit Konfiguration,
  Datensatzkonsistenz, Status und Interpretation beantworten.
- **P2, Foliennähe und Lernzielabdeckung:**
  [Quiz 1–3 und 9](../quizacademy/quiz_05_serielle_bussysteme.csv#L2)
  wiederholen 115200 Baud/8N1, dieselben SPI-Startregister 0x96/0x3C mit genau
  dem bereits angegebenen Vier-Takt-Zustand, Adresse 0x68→D0 sowie den gleichen
  Gleichtaktversatz +0,8 V. Quellen: [Zeile 179](../vorlesungen/05_serielle_bussysteme.qmd#L179),
  [Zeile 353](../vorlesungen/05_serielle_bussysteme.qmd#L353),
  [Zeile 599](../vorlesungen/05_serielle_bussysteme.qmd#L599) und
  [Zeile 789](../vorlesungen/05_serielle_bussysteme.qmd#L789).
  Die übrigen Fragen sind überwiegend unmittelbare Zuordnungen der erklärten
  Rollen und Definitionen. Pull-up-Auslegung, FIFO-Servicefrist und
  fehlerhafte Verarbeitung des Sensors werden im Quiz nicht selbstständig
  angewandt. **Vorschlag:** einen gelösten Zahlenfall als Einstieg behalten,
  zwei weitere durch einen ausgewählten fehlerhaften Transferverlauf und
  eine Entscheidung über zwei Pull-up-/Pufferkonfigurationen ersetzen.
- **P3, Terminologie vereinheitlichen:**
  [Musterlösung 5, Zeile 177](../labs/lab_05_serielle_bussysteme.qmd#L177)
  wechselt ohne lokalen Hinweis von „Controller“ zu „Master“. Die Vorlesung
  ordnet die historischen Bezeichnungen zwar bei Einführung zu
  ([Zeile 126](../vorlesungen/05_serielle_bussysteme.qmd#L126)), aber gerade die
  ACK-Rollen sollen ohne neue Benennung zugeordnet werden. **Vorschlag:**
  in dieser Lösung ebenfalls „Controller“ verwenden; reale Pinbezeichnungen
  MOSI/MISO unverändert belassen.

### Aufgaben und Nachweise

| Aufgabe | Eigenständiger Denkschritt | Anspruch / Zeit, geschätzt |
|---|---|---|
| 1 | zeitliche Bitfolge in Stellengewichte übersetzen und vollständigen Rahmen rekonstruieren | Routine mit Darstellungstransfer, 8–10 min |
| 2 | frühe Samples und verfügbare FIFO-Plätze zeitlich einordnen | Randfall-/Zustandsanalyse, 8–12 min |
| 3 | simultane Registerupdates, Modus 3 und Timingbudget auswerten; Protokollaufwand zählen | mehrschrittige Anwendung, 12–15 min |
| 4 | zulässigen Widerstandsbereich statt einzelner Faustzahl bestimmen | Dimensionierung und Ausschlussfall, 10–12 min |
| 5 | vollständigen Read/Write mit Rollen und Fehlerpfaden aufschreiben | Protokollanalyse, 10–12 min |
| 6 | neue physikalische Einheit, Gleichtakt und Durchsatzentscheidung verbinden | Anwendung/Entwurfsentscheidung, 10–15 min |

Der Lab-Satz ist deutlich selbstständiger als das Quiz und deckt die zentralen
Lernziele ab. Die Richtzeit 60–75 Minuten ist bei bereitliegenden Formeln
plausibel, setzt aber die geübten Byte- und Bruchrechnungen voraus. Die Fälle
sind neu: 0xB6 statt 0x53, kleinere Empfangsrate, andere FIFO-Belegung, Modus 3,
1,8-V-Pull-ups und ein erfundener Zweikanalsensor. Ein Aufgabenabschluss auf
Papier ist mit der vorhandenen Probeklausurform vereinbar; ein verbindlicher
Prüfungsanspruch wird daraus nicht abgeleitet.

**Unabhängige Gegenrechnungen:** SPI nach 2/5/8 Takten ergibt 9D/76,
EB/B4 und 5D/A7; UART-Bitzeit 17,3611 µs, Bytezeit 173,6111 µs;
FIFO-voll 1,21528 ms, erster Overrun 1,38889 ms. Pull-up-Bereich 750–3147,25 Ω,
Anstiegszeiten 190,6425 ns bzw. 495,6705 ns; bei 700p F ist die obere Grenze 674,41 Ω
und der Bereich leer. Vier-Byte-Read: 63 Takte / 252 µs; SPI-Auftrag: 56 Takte / 7 µs.
Die vorgegebenen Lösungen und richtigen Quizoptionen sind unter den
benannten Modellen konsistent. `decode_s16_be` vermeidet im C11-Modell einen
außerhalb des Zielbereichs liegenden Cast nach `int16_t`; exklusiver Zugriff
und ausreichende Puffer werden korrekt als Vorbedingungen genannt.

**Bilder und Begriffe:** Alle SVG-Textbeschriftungen wurden mit den
Folienfolgen abgeglichen; `i2c-burst.png` und `spi-modes.png` tatsächlich
angesehen. Rollen, Taktzahlen und Abtastpunkte stimmen mit den Notizen überein.
Open-Drain entspricht dem Glossar. Eine neue vollständige HTML-/PDF- oder
reale elektrische Timingprüfung gehört nicht zu diesem Quellenreview.

## 3. Vorlesung 6: Hardware-Beschleunigung und DMA

**Umfang und Urteil.** 50 Folien mit Notizen, sechs Pflichtaufgaben,
zehn Quizfragen und 21 SVG-Diagramme. Die drei getrennten Budgets – Leitung,
CPU und gemeinsamer Speicherpfad – führen sinnvoll zu einem Transferauftrag
und anschließend zu Besitz-, Cache- und Streamregeln. Die Einheit macht
keine unzulässige „DMA macht alles schneller“-Zusage. Besonders wertvoll
sind der RX-Dirty-Gegenfall, die Unterscheidung DMA-TC/Leitungsende und das
zu spät behandelte Half-Transfer-Flag.

### Befunde und Verbesserungen

- **P2, didaktische Verbesserung:**
  [Erster Inhalt, Zeile 14](../vorlesungen/06_hardware_beschleunigung_dma.qmd#L14)
  nennt bereits die Antwort „DMA übernimmt Kopierarbeit“, bevor eine offene
  Entscheidung aus demVorwissen gestellt wird. **Vorschlag:** mit dem
  vorhandenen Displayfall fragen „Die CPU verbringt ihre gesamte Zeit mit
  Senden – erreicht DMA damit 60 Bilder/s über dieselbe Leitung?“ Erst Vermutungen
  sammeln und beim Bandbreitenvergleich und der Abschlussauswahl beantworten.
- **P2, eigenständige Anwendung im Quiz ausbauen:**
  [Quiz 1/2/3/4/10](../quizacademy/quiz_06_hardware_beschleunigung_dma.csv#L2)
  übernimmt das Vollbild 320×240/50 MHz, die Million-Byte-Zerlegung mit 65535,
  den festen UART-TX-Pfad, die Werte 11/22 sowie den 16-Bit-ADC-Pfad direkt aus
  [Zeile 82](../vorlesungen/06_hardware_beschleunigung_dma.qmd#L82),
  [Zeile 324](../vorlesungen/06_hardware_beschleunigung_dma.qmd#L324),
  [Zeile 252](../vorlesungen/06_hardware_beschleunigung_dma.qmd#L252),
  [Zeile 522](../vorlesungen/06_hardware_beschleunigung_dma.qmd#L522) und
  [Zeile 269](../vorlesungen/06_hardware_beschleunigung_dma.qmd#L269).
  Die Fehlerfälle 6–8 sind fachlich sinnvoll, ihre richtige Entscheidung wurde
  aber ebenfalls bereits wörtlich erklärt. **Vorschlag:** einen neuen
  kombinierten Zustand bewerten lassen, etwa TC nach Abbruch bei noch aktivem
  Kanal oder ausreichende Leitungsrate bei zu spät freier Pufferhälfte.
  Die richtige Option sollte die tatsächlich fehlende Voraussetzung nennen,
  statt eine bekannte Regel isoliert zu wiederholen.

Es wurde kein sicherer fachlicher Fehler in den angegebenen Rechenmodellen,
Musterlösungen oder richtigen Quizoptionen gefunden. Diese Aussage bezieht
sich auf die benannten Modelle, nicht auf eine beliebige reale DMA-Plattform.

### Aufgaben, Niveau und Gegenrechnungen

| Aufgabe | Lernziel und eigener Denkschritt | Anspruch / Zeit, geschätzt |
|---|---|---|
| 1 | Bildbedarf, Leitung und angebotenen Interruptbedarf getrennt rechnen | Routine mit Budgetentscheidung, 10–12 min |
| 2 | Adressfolgen und Elementbreite übertragen; Null-Limit und Ausrichtung prüfen | mehrschrittige Anwendung, 10–12 min |
| 3 | zwei Abschlusszeiten und einen nicht bestätigten Abbruch auswerten | Zustands-/Fehleranalyse, 8–10 min |
| 4 | nicht kohärente TX-/RX-Fälle und ganze 64-Byte-Zeilen beurteilen | anspruchsvollere Übertragung, 12–15 min |
| 5 | Stereo-Speicherformat, Half-Transfer-Phase und verlorene Samples rekonstruieren | mehrschrittige Zeit-/Ringanalyse, 12–15 min |
| 6 | vier nicht zusammenhängende Quellzeilen herleiten und DMA-Wahl begründen | Anwendung/Entscheidung, 8–10 min |

Damit liegt die vollständige Bearbeitung eher im oberen Bereich der
60–75 Minuten; die ersten beiden Aufgaben bauen nötige Routine auf, 3–6
fordern nachvollziehbare Ablauf- und Entwurfsentscheidungen. Die geänderten
Randbedingungen sind substanziell:64-Byte-Zeilen statt 32, Stereo 24 Bit in
32-Bit-Speicherplätzen, ein überlaufener 16er-Ring und vier Rechteckzeilen.
Die Begriffe DMA, Clean/Invalidate und Cache-Sichtbarkeit stimmen mit dem
Glossar überein; Cycle Stealing wird in der Vorlesung tatsächlich eingeführt
([Zeile 221](../vorlesungen/06_hardware_beschleunigung_dma.qmd#L221)).

**Nachgerechnet:** Bild 64800 Byte, Bedarf 2,916 MB/s; ideale 23,1481/69,4444 Bilder/s;
angebotener CPU-Bedarf 120 % bzw. 3,75 %. 25000 Byte = 6×4095+430;
1 MiB/12 Mbit/s = 0,6990507 s. Cacheende 0x210030CB, letzte Adresse CA,
umschließender Bereich [0x21003000, 0x21003100) mit 256 Byte und je 53 Randbytes.
Stereo-Datenrate 384000 Byte/s, Halbzeit 8 ms, Reserve 1,1 ms. Bei P=39 / C=21
sind die Elemente 21/22 verloren. Rechteckquellen 44AE/468E/486E/4A4E bestätigen die Lösung.
Die beiden reinen C-Helfer haben passende Breiten- und Bereichsannahmen;
positive Länge/positives Limit und gültige Gerätebereiche bleiben Pflichten
des Aufrufers.

**Abbildungen und Grenzen.** Alle SVG-Beschriftungen wurden gegen die
beschriebenen Modelle geprüft; `rx-cache.png` und `flag-late.png` wurden
angesehen. Neue und alte Daten, Richtungen und Zeitgrenzen sind konsistent
beschriftet. Keine neue HTML-/PDF-Gesamtsichtprüfung, keine Firmwareausführung,
Cachemessung oder reale Buslatenzanalyse.

## 4. Vorlesung 7: Moderne CPU-Architekturen

**Umfang und Urteil.** 50 Folien und Notizblöcke, sechs Pflichtaufgaben,
zehn Quizfragen, 28 SVG-Diagramme sowie `labs/src/lab07_ilp.c`.
Die Trennung der Modelle M1/M2/M3 ist fachlich und didaktisch entscheidend und
hier ausdrücklich geleistet. RAW/WAR/WAW, gespeicherte Quelltags, geordnetes
Retire und präzise Fehlerzustände werden über dieselbe kleine Folge aufgebaut.
Auch die Abgrenzungen ISA/Mikroarchitektur, Latenz/Initiationsintervall,
Bestätigung/Speichersichtbarkeit und Spectre/Meltdown sind sorgfältig formuliert.

### Befunde und Verbesserungen

- **P2, didaktische Verbesserung:**
  [Erste Folie, Zeile 14](../vorlesungen/07_moderne_cpu_architekturen.qmd#L14)
  erläutert das Thema, statt vor den Voraussetzungen und der Agenda eine
  offene Vorhersage zu verlangen. **Vorschlag:** „Ein Load wartet auf den
  Speicher. Darf der Prozessor die danach stehende unabhängige Subtraktion
  schon rechnen – und darf ihr Ergebnis bereits sichtbar werden?“ Zunächst
  die zwei Entscheidungen trennen lassen und bei M3/ROB wieder aufnehmen.
- **P2, Quiz zu nahe an vollständig gelösten Beispielen:**
  [Quiz 1,3,4,5,7](../quizacademy/quiz_07_moderne_cpu_architekturen.csv#L2)
  fragt genau 5/9, P10/P12, den M3-Vergleich 8/7, die beschriebene ROB/PRF-Verteilung
  und den CPI-Schritt 1→1,30 erneut ab. Das sind die Resultate von
  [Zeile 161](../vorlesungen/07_moderne_cpu_architekturen.qmd#L161),
  [Zeile 374](../vorlesungen/07_moderne_cpu_architekturen.qmd#L374),
  [Zeile 464](../vorlesungen/07_moderne_cpu_architekturen.qmd#L464) und
  [Zeile 599](../vorlesungen/07_moderne_cpu_architekturen.qmd#L599).
  Die Fragen diagnostizieren durchaus typische Verwechslungen, aber die
  Antworten können großenteils wiedergefunden werden. **Vorschlag:** einige
  vorgegebene Ablaufpläne oder Renamingtabellen mit genau einem Fehler prüfen
  lassen; daneben einen Fall mit geändertem Ressourcenlimit oder einer
  zusätzlichen echten Abhängigkeit beurteilen. Dafür die vollständigen
  Modellparameter in der Frage belassen.

Es wurde kein sicherer Widerspruch zwischen den angegebenen Modellen,
Zeitdiagrammen, Musterlösungen und richtigen Quizantworten gefunden. Der
Hostcode zeigt funktionale Gleichheit der ausgeführten Fälle und wird
zutreffend nicht als Nachweis eines Laufzeitgewinns ausgegeben.

### Aufgaben und Niveau

| Aufgabe | Eigenständiger Denkschritt | Anspruch / Zeit, geschätzt |
|---|---|---|
| 1 | sechste Stufe und Readzeitpunkt statt bloßer Fünf-Stufen-Formel berücksichtigen | mehrschrittige Routine/Übertragung, 10–12 min |
| 2 | Wert- und Namenskanten sowie physische Versionen für andere Befehle verfolgen | Anwendung, 10–12 min |
| 3 | Start/Fertig/Retire unter festgelegten Ressourcen komplett planen | Analyse, 12–15 min |
| 4 | Prädiktor aus altem Zustand verfolgen und additive Strafe interpretieren | Zustandsanalyse/Rechnung, 10–12 min |
| 5 | erfolgreichen Prefix von intern fertigen Werten trennen | Begründung/Fehleranalyse, 8–12 min |
| 6 | drei Summenketten, Rest und Null-Eingabe auswerten | Code-/Randfallanalyse, 8–12 min |

Die Änderungen gegenüber den Folien sind nachvollziehbar: sechs Stufen,
anderer RAW-Lesezeitpunkt, längerer Load, andere Rechenoperationen, neuer
Prädiktorverlauf und drei statt zwei Akkumulatoren. Mit den bereitgestellten
Konventionen liegt die vollständige Bearbeitung geschätzt bei 60–75 Minuten.
Die offenen Ablauf- und Begründungsaufgaben ergänzen die Multiple-Choice-Fragen
für die im Kurs gezeigte Prüfungsform sinnvoll.

**Nachgerechnet:** Pipeline 12 Takte, mit Stall 14; 192/216 Takte bei 160 MHz ergeben
1,2/1,35 µs. 14 XOR 9 = 7, Endzustände 7/24/5. Der M3-Labvergleich endet in 10/9 Takten;
Retirefolgen 7,8,9,10 gegenüber 7,8,8,9 sind bei Breite 2 konsistent.
Der achtstufige Prädiktorverlauf hat Treffer in 1/4/7, Endzustand 01.
CPI 0,9 + 0,15 × 0,12 × 10 = 1,08, Zeit +20 %, Rate −16,667 %.
Die drei Akkumulatoren ergeben vor dem Rest 11/8/11, anschließend 17/8/11 und 36.

**Ausgeführt:** Das vorhandene `lab07_ilp.c` mit
`gcc -std=c11 -O1 -Wall -Wextra -Werror -fsanitize=address,undefined`
übersetzt und auf dem Host ausgeführt; alle eingebauten Prüffälle bestanden.
Dies ist keine OoO-Zeitmessung. Alle SVG-Textinhalte wurden abgeglichen;
`pred.png` und `ooo.png` wurden angesehen. IPC/CPI/ILP stimmen mit dem Glossar
überein. Keine neue Gesamtansicht gerenderter Folien/PDFs und keine unabhängige
Revisionprüfung der verlinkten Architekturquellen.

## 5. Vorlesung 8: KI-Beschleuniger und Edge AI

**Umfang und Urteil.** 50 Folien mit Notizen, sechs Pflichtaufgaben,
zehn Quizfragen, 28 SVG-Diagramme und `labs/src/lab08_dense.c`.
Der Aufbau Dense → Speichergrenze → Vektor-/Arraydatenfluss → Quantisierung
und Firmware ist für das fünfte Semester anspruchsvoll, aber mit den
vorausgehenden Cache-, DMA- und Abhängigkeitskonzepten begründbar.
Die CPU/GPU/NPU-Abbildung vermeidet unzulässige allgemeine Geschwindigkeits-
oder Energievergleiche. Besonders gelungen sind die explizite Speichergrenze,
die vollständige systolische Einspeisung und die korrekten RVV-1.0-Regeln
für den mittleren AVL-Bereich.

### Befunde und Verbesserungen

- **P2, aktivierender Einstieg fehlt:**
  [Zeile 14](../vorlesungen/08_ki_beschleuniger_edge_ai.qmd#L14)
  erklärt bereits Rechnung und Datenversorgung. Die erste eigenständige
  Rechenfrage folgt erst bei
  [Zeile 120](../vorlesungen/08_ki_beschleuniger_edge_ai.qmd#L120), nach
  Voraussetzungen, Lernzielen und Begriffen. **Vorschlag:** als erste Frage
  „Ein Beschleuniger hat zehnmal mehr Rechenwerke – wird dieselbe kleine
  Sensorauswertung zehnmal schneller?“ verwenden. Die begründeten Vermutungen
  bei Roofline, Arrayauslastung und Gesamtzeit gezielt wieder aufnehmen.
- **P2, Foliennähe und Schwierigkeitsmarkierung:**
  [Quiz 2, Zeile 3](../quizacademy/quiz_08_ki_beschleuniger_edge_ai.csv#L3)
  ist mit „Schwer“ markiert, verlangt aber genau dieselbe Einsetzung
  min(8,8×0,5)=4 wie die ausgearbeitete
  [Roofline-Folie, Zeile 188](../vorlesungen/08_ki_beschleuniger_edge_ai.qmd#L188).
  [Quiz 10, Zeile 11](../quizacademy/quiz_08_ki_beschleuniger_edge_ai.csv#L11)
  wiederholt ebenfalls die schon gelösten Verhältnisse 16/8 und 10/1 aus
  [Zeile 614](../vorlesungen/08_ki_beschleuniger_edge_ai.qmd#L614).
  Auch Parameterzahl, Tilebytes, AVL 40, Chaining und Quantisierungsfälle
  stammen unmittelbar aus den Folien. **Vorschlag:** wenige dieser Routinen
  behalten; für als anspruchsvoll gekennzeichnete Fragen beispielsweise zwei
  scheinbar widersprüchliche Intensitätsangaben mit verschiedenen
  Transfergrenzen oder einen gemischten Speicher-/Zeitengpass beurteilen
  lassen. „Schwer“ erst mit diesem Denkschritt begründen; ohne studentische
  Bearbeitungsdaten bleibt die Schwierigkeit eine Schätzung.

Ein sicherer numerischer Fehler wurde im Modell-, Labor- und Quizabgleich
nicht gefunden. Die Kennzeichnung aller Zahlen als Lehrmodelle und die
Abgrenzung des Hostversuchs von einem trainierten TFLM-Modell sind korrekt.

### Aufgaben und Nachweise

| Aufgabe | Eigenständiger Denkschritt | Anspruch / Zeit, geschätzt |
|---|---|---|
| 1 | neue Dense-Form, Parameter/MACs und Speicherbytes je Datentyp trennen | Routine/Anwendung, 8–10 min |
| 2 | Intensität für geänderte innere Dimension und erweiterte Transfergrenze berechnen | mehrschrittige Analyse, 10–12 min |
| 3 | erlaubte VL-Folgen und Zeitplan aus neuen Latenzen herleiten | Regel-/Ablaufanalyse, 12–15 min |
| 4 | gültige Paare und alle Teilsummen im fünf-Takte-Array verfolgen | anspruchsvollere Ablaufanalyse, 12–15 min |
| 5 | negative Quantisierung und Requantisierung mit Bias-/Nullpunktkorrektur | mehrschrittige Anwendung, 12–15 min |
| 6 | getrennte Budgets und Fehler-/Lebensdauerfall beurteilen | Systemanalyse, 10–12 min |

Das Blatt enthält echte neue Situationen: 3×2-Dense, 2×3-mal-3×2-Tile,
negative Werte und Nullprodukte, geänderte Skalen sowie ein anderes
Sensorfenster. Der Richtwert 60–75 Minuten liegt bei vollständigen
Begründungen eher am unteren Rand; Aufgabe 4 und die zusätzliche
Requantisierung sollten bei der Präsenzplanung gezielt ausgewählt werden.
Die Vorlesungsnotizen enthalten bereits vollständige Lösungen der
Papierphasen. Für selbstständige Bearbeitung zuerst nur die Aufgabenfassung
bereitstellen und die Lösungen anschließend zur Besprechung verwenden.
Das ist eine Einsatzempfehlung, kein Fehler des Lösungsprofils.

**Nachgerechnet:** Dense [7,−15,−1], neun Parameter/sechs MACs,
20 Byte ohne bzw. 23 Byte mit Ausgaben. Tile 24 Ops: 96/48 Eingangsbytes,
mit Ausgaben 112/64 Byte. Beim Array entstehen
[[2,0],[0,0]], [[0,8],[3,0]], [[−5,11],[3,12]],
[[−5,12],[13,12]], [[−5,12],[13,10]];
gültige MACs 1/3/4/3/1 und Auslastung 60 % bzw. 15 % im 4×4-Fenster.
Die VL-Regeln ergeben für 250 Elemente 16 Iterationen; Chaining endet in 10
statt 15. Quantisierung ergibt −7/−1,4 und −128/−25,6;
Akkumulation −20, Realwert −0,5, Ausgangscode −3 mit Rückwert −0,48.
SRAM-Rest 16,4375 KiB; Gesamtfaktor 16,5 / 7,25 = 2,275862.

**Ausgeführt:** `lab08_dense.c` mit C11, `-O1 -Wall -Wextra -Werror`
und Address-/Undefined Behavior Sanitizer sowie `-lm` auf dem Host übersetzt
und ausgeführt. Alle eingebauten Dense-, Matrix-, Sättigungs- und Fehlerfälle
bestanden. Alle SVG-Beschriftungen wurden abgeglichen;
`cpu-gpu-npu.png` und `wave.png` wurden angesehen. MAC, NPU/Edge AI und
Speicherbegriffe passen zum Glossar. Keine RVV-Assemblerausführung,
TFLM-Integration oder Hardwarezeit-/Energiemessung; keine neue vollständige
HTML-/PDF-Sichtprüfung.

## 6. Vorlesung 9: Paralleles Rechnen und Multicore

**Umfang und Urteil.** 50 Folien und zugeordnete Notizblöcke, sechs
Pflichtaufgaben mit Lösungen, zehn Quizfragen, 29 SVG-Diagramme und
`labs/src/lab09_atomics.c`. Die Trennung von Kohärenz, atomarem Update und
Datenordnung ist der richtige Schwerpunkt zum Kursabschluss. Das explizite
MESI-Lehrmodell vermeidet Aussagen über beliebige reale Speicherhierarchien.
Besonders sorgfältig sind C-Data-Race gegenüber logischem Lost Update,
SC-Rückgabewert gegenüber gespeichertemWert, gewöhnlicher Speicher gegenüber
MMIO sowie der fehlende Fortschritt eines ISR-Spinlocks erklärt.

### Befunde und Verbesserungen

- **P2, aktivierender Einstieg:**
  [Die erste Folie, Zeile 14](../vorlesungen/09_paralleles_rechnen_multicore.qmd#L14)
  erklärt bereits, warum mehrere Kerne gemeinsame Werte richtig nutzen
  müssen. Die nachfolgenden Leitfragen strukturieren, verlangen aber noch
  keine konkrete Vorhersage. **Vorschlag:** zuerst „Zwei Kerne erhöhen einen
  Zähler je einmal. Muss das Ergebnis zwei sein, wenn ihre Caches kohärent
  sind?“ beantworten lassen. Die fehlenden Annahmen erst sammeln und später
  beim Unterschied zwischen Kohärenz, C-Sprachregel und atomarer RMW auflösen.
- **P2, Quiz prüft häufig schon gelöste Fälle:**
  [Quizfragen 1–4, 7, 8 und 10](../quizacademy/quiz_09_paralleles_rechnen_multicore.csv#L2)
  wiederholen M:5 mit unterem Stand null, den Write auf S:0, den sauberen
  S-Auswurf, Offsets null/vier/64, den Zähler mit zwei Workern, die Publikation
  von 42 sowie Amdahl mit 0,2 und hundert Kernen. Diese Ergebnisse stehen
  bereits in den Folien, beispielsweise
  [Zeile 248](../vorlesungen/09_paralleles_rechnen_multicore.qmd#L248),
  [Zeile 262](../vorlesungen/09_paralleles_rechnen_multicore.qmd#L262),
  [Zeile 290](../vorlesungen/09_paralleles_rechnen_multicore.qmd#L290),
  [Zeile 543](../vorlesungen/09_paralleles_rechnen_multicore.qmd#L543),
  [Zeile 589](../vorlesungen/09_paralleles_rechnen_multicore.qmd#L589) und
  [Zeile 664](../vorlesungen/09_paralleles_rechnen_multicore.qmd#L664).
  Die falschen Optionen adressieren sinnvolle Fehlvorstellungen. Für den
  Transfer sind jedoch neue Zustandsfolgen oder Fehlerdiagnosen stärker.
  **Vorschlag:** zwei kurze Abläufe gegenüberstellen, von denen genau einer
  eine MESI-Invariante verletzt; bei der Publikation einen späteren Rewrite
  ergänzen und nach der entfallenen Garantie fragen. Die als „Schwer“
  markierte Amdahl-Frage durch einen Vergleich mit Zusatzzeit oder ungleicher
  Last ersetzen, statt die bereits vorgerechneten Kennwerte erneut abzufragen.

Es wurde kein sicherer Widerspruch zwischen dem benannten Lehrmodell,
Musterlösungen und richtigen Quizoptionen gefunden. Die Antwortpositionen
sind verteilt; ein durchgehender Längenhinweis auf richtige Optionen ergibt
sich nicht. Einzelne richtige Antworten sind länger, etwa bei Frage 10.
Beim Überarbeiten die nötigen Voraussetzungen möglichst in den Fragetext
verlagern, damit die Antwortoptionen vergleichbar knapp bleiben.

### Aufgaben, Niveau und Nachweise

| Aufgabe | Lernziel und eigener Denkschritt | Anspruch / Zeit, geschätzt |
|---|---|---|
| 1 | drei Kopien, Rechte und Werte verfolgen; S nach Fremdauswurf begründen | Zustandsanalyse, 12–15 min |
| 2 | Objekt- und Zeilengrenzen sowie Besitzerwechsel aus einer Folge herleiten | Anwendung und Abgrenzung, 8–10 min |
| 3 | neues Update-Interleaving und getrennte LR-/SC-Ergebnisse auswerten | Ablauf- und Sprachanalyse, 12–15 min |
| 4 | passende Übergabe, dreiteiligen Wartekreis und ISR-Fortschritt begründen | anspruchsvollere Analyse, 15–20 min |
| 5 | ideale Teilung, Zusatzaufwand und maximale Teilzeit auseinanderhalten | mehrschrittige Rechnung, 10–12 min |
| 6 | neues Cachemapping, AMAT, PWM und Geräteübergabe zusammenführen | Transfer und Wiederholung, 12–15 min |

Der Richtwert von 75–90 Minuten ist bei vollständigen Begründungen plausibel,
aber eine Schätzung. Die vier Papierphasen im Ablauf umfassen zusammen
60 Minuten; vollständige Bearbeitung und Diskussion des ganzen Blatts passen
nur bei Auswahl oder anschließender Eigenarbeit in diese Zeit. Der neue
Dreikernfall, 128-Byte-Zeilen, Addition um zwei, dreiteilige Wartekreis und die
geänderten Systemparameter verlangen eigene Arbeit. Das Blatt ist gegenüber
dem Quiz deutlich besser für die Vorbereitung offener Papieraufgaben geeignet.

**Unabhängig nachvollzogen:** Die MESI-Folge endet nach dem M-Auswurf bei
`L=13`, der nächste alleinige Leser erhält E:13. Die Schreiberfolge hat vier
Besitzerwechsel. LR/SC endet bei 14, während die vorgegebene getrennte
Load/Store-Folge nur zwölf erzeugt. Drei Kerne ergeben Zeit 80, Speedup 1,875
und Effizienz 62,5 %; sechzig Kerne ergeben 46,75, 3,208556 und 5,347594 %.
Zusatzzeit sechs ergibt 86 und 1,744186; ungleiche Teilpakete ergeben 110 und
1,363636. Das Cachemapping ergibt sieben Offset-, sechs Index- und neunzehn
Tagbits, Offset 24, Index fünf, Tag `0x18002`, Basis `0x30004280`.
AMAT ist sieben Takte bzw. 56 ns. PWM ergibt 200 Hz, fünf ms Periode und
zwei ms HIGH, also 40 %. Die numerischen Ergebnisse stimmen mit den Lösungen
überein.

**Ausgeführt:** `lab09_atomics.c` mit C11, `-O1 -Wall -Wextra -Werror
-pedantic -pthread` und Address-/Undefined Behavior Sanitizer übersetzt und auf
dem Host ausgeführt. Teilsummen 10/26/36, seriell nachgebildetes Lost Update
mit Endwert eins, atomarer und gesperrter Zähler jeweils 40000 sowie
veröffentlichte Payload 42 wurden bestätigt. Das Programm führt keinen
gewöhnlichen ungeschützten C-Race aus. Die Behandlung von Threadfehlern ist
quellseitig nachvollziehbar; Fehlerpfade wurden nicht durch Injektion erzwungen.

**Abbildungen und Grenzen.** Alle SVG-Beschriftungen wurden mit den
beschriebenen Modellen verglichen; `lrsc.png` und `v_flag.png` wurden angesehen.
M/E-Exklusivität, aktueller Datenlieferant, SC-Status und passende
Release-/Acquire-Verbindung sind konsistent. Kohärenz, False Sharing,
Atomizität und Hart stimmen mit dem Glossar überein. Keine RISC-V-Ausführung,
keine Messung von MESI-Verkehr, Fairness oder Speedup und keine neue
vollständige HTML-/PDF-Sichtprüfung. Der verlinkte Spezifikationsstand ist
benannt, wurde aber nicht nochmals unabhängig gegen die gesamte Spezifikation
validiert.
## 7. Folgerungen und offene Nachweise

Die Einheiten wurden nacheinander geprüft. Das größte gemeinsame
Verbesserungspotenzial liegt in zwei konkreten Punkten: Vor den erklärenden
Einstiegen fehlt jeweils eine aktivierende Vorhersage aus dem Vorwissen; die
Quizsätze übernehmen häufig bereits vollständig gelöste Beispiele. Für jede
Einheit sind oben eine passende Einstiegsfrage und konkrete Transferfälle
vorgeschlagen. Die Übungen leisten den Transfer bereits deutlich besser.

Zuerst sollte die Leistungsbenennung in VL4 korrigiert werden. Anschließend
bieten sich die Einstiege, die Auswahl neuer Quizfälle und die lesbarere
Auflösungsgrafik an. Eine breite fachliche Neuausrichtung wird durch die
geprüften Inhalte nicht begründet. Die späteren Einheiten gewinnen gerade
durch ihre ausdrücklich begrenzten Lehrmodelle und die getrennten Fragen
nach Datenweg, Abschluss, Zuständigkeit und Sichtbarkeit.

**Tatsächlich geprüft:** 300 inhaltliche Folien und 300 Notizblöcke,
36 Pflichtaufgaben einschließlich Lösungen, 60 Quizfragen sowie die
zugehörigen Diagrammquellen. Ein Strukturcheck bestätigte pro Quiz zehn
Datensätze mit je vier Optionen, gültige Markierungen und jeweils genau eine
richtige Antwort. Alle 141 referenzierten Bilddateien sind vorhanden; die
141 SVGs lassen sich als XML lesen. Die Textbeschriftungen wurden mit den
Modellen abgeglichen und elf vorhandene PNGs gezielt angesehen. Die
Rechengegenproben und tatsächlich ausgeführten Hostprogramme stehen jeweils
bei der Einheit. An Lehrmaterialien wurden im Rahmen dieses Reviews keine
Änderungen vorgenommen.

**Offene Nachweise:** Eine frische vollständige HTML-/PDF-Ausgabe mit Prüfung
jeder gerenderten Folie und jeder Lösungsprofil-Seite wurde hier nicht erzeugt.
Eine visuelle Gesamtfreigabe, ein Hardwareversuch oder ein CI-Ergebnis wird
folglich nicht behauptet. Für die konkreten elektrischen und zeitlichen
Plattformeigenschaften bleiben Datenblattrevision und Zielhardware maßgebend;
die Lehrmodelle ersetzen diese Nachweise nicht. Bearbeitungszeiten und
Schwierigkeitsangaben sollten anhand tatsächlicher Rückmeldungen aus der
Veranstaltung kalibriert werden. Die vorhandene Probeklausur belegt das
Aufgabenformat, ersetzt aber kein offizielles Prüfungs- oder Modulhandbuch.
