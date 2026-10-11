6T-SRAM: SVG-Schaltungen und Cursor-Prompt

INHALT UND FOLIENZUORDNUNG
01_6t_sram_grundschaltung.svg: Folie 44; vollständige Schaltung.
02_6t_sram_halten_q0.svg: Folie 47; Halten bei Q=0 und Q_B=1.
03_6t_sram_lesen_q0.svg: Folie 48; Auswertung nach Vorladung.
04_6t_sram_schreiben_beginn.svg: Folie 49; Anfang des Schreibens Q:0->1.
05_6t_sram_schreiben_endzustand.svg: Folie 49 oder ergänzende Folie; neuer Haltezustand.
06_6t_sram_lesen_zeitverlauf.svg: Ergänzung zu Folie 48.
07_6t_sram_schreiben_zeitverlauf.svg: Ergänzung zu Folie 49.
cursor_prompt_mct3_6t_sram_mit_svg.txt: vollständiger Verbesserungsauftrag im Hauptverzeichnis des ZIP-Pakets.

Alle SVGs sind eigenständige Vektordateien mit bearbeitbaren Textelementen und ohne externe Ressourcen. Das Paket enthält außerdem den Python-Generator erzeuge_sram_svgs.py, topologie.json und pruefprotokoll.json. Der Generator benötigt nur die Python-Standardbibliothek und schreibt die SVGs in sein eigenes Verzeichnis.

VERWENDUNG
Entpacke das ZIP-Paket im Arbeitsbereich von Cursor. Übernimm die SVGs in das tatsächliche Abbildungsverzeichnis des Vorlesungsprojekts. Gib Cursor den beigefügten Prompt. Passe Dateiverweise an die tatsächlich vorhandene Projektstruktur an; die Paketstruktur ist keine Behauptung über bestehende Repository-Pfade.

SVGs 01–05 enthalten die Schaltung als Gruppe mit id="cell-and-periphery". Titel, Erläuterungskarten und Fußnoten sind separate SVG-Elemente. Sie können bei der Integration in ein bestehendes Foliendesign passend angeordnet werden. Die Hinweise zum vereinfachten Modell und zu den Bulkanschlüssen dürfen bei einem Zuschnitt nicht verloren gehen: übernimm sie gegebenenfalls in Bildunterschrift und Notizen.

Die Zeichnungen verwenden vereinfachte dreipolige MOS-Symbole. Der Kreis am Gate kennzeichnet pMOS. Ausgeblendete Bulkanschlüsse werden konventionell an VDD (pMOS) beziehungsweise GND (nMOS) angenommen. Punkte markieren echte Verbindungen; die beiden Brücken im Rückkopplungsnetz markieren Kreuzungen ohne Verbindung.

WICHTIGE MODELLGRENZEN
- Q und Q_B bezeichnen im stabilen Zustand komplementäre interne Speicherknoten.
- BL und BL_B sind zwei Bitleitungen; beim Vorladen dürfen beide high sein.
- „an/aus“ bei den Invertern ist eine qualitative Schalterbetrachtung.
- „aktiviert“ an Access-Transistoren bedeutet: WL gibt den Zugriff frei. Es ist keine Aussage, dass beide Transistoren in jedem Moment gleich stark leiten oder Strom führen. Die tatsächliche Leitfähigkeit hängt von Gateübersteuerung und Knotenspannungen ab.
- SVG 03 zeigt die Auswertephase nach dem Vorladen. Die Vorladeperipherie ist deaktiviert und wird nicht transistorweise dargestellt. Der Leseverstärker ist ein externer Funktionsblock; er zählt nicht zur 6T-Zelle.
- SVG 04 zeigt den anfänglichen Inverterzustand beim Beginn des Umschaltens. Während der Rückkopplung wechseln die Zustände. Das Ergebnis zeigt SVG 05.
- Die Schreibtreiber in SVG 04 sind externe Funktionsblöcke, keine zusätzlichen Zelltransistoren.
- Die Zeitdiagramme zeigen eine qualitative Reihenfolge. Abstände und Amplituden sind keine Simulations- oder Messwerte.
- Im Schreibzeitbild starten beide Bitleitungen als didaktische Annahme high. Schreibdaten werden vor WL-Aktivierung gesetzt. Nach Treiberfreigabe werden die Bitleitungsspannungen nicht weiter gezeichnet.
- Betriebsspannung, Transistordimensionen, Prozessparameter, Rauschabstände, genaue Verzögerungen und Leckströme werden nicht numerisch bestimmt.

PRÜFUNG
Die sieben SVGs wurden als XML geparst und gerendert. Für die fünf Schaltbilder wurden die Transistoranzahl (2 pMOS, 4 nMOS), die Anschlüsse und der zusammenhängende Terminalnetzgraph gegen eine separate Solltopologie geprüft. Die logischen Gatezustände wurden geprüft. Die gerenderten Zeichnungen wurden auf Verbindungspunkte, isolierte Gates, die beiden nicht verbundenen Kreuzungen, Beschriftungen, Stromrichtungen und Textüberläufe kontrolliert.

Diese Prüfungen sind keine SPICE-Simulation und kein Nachweis realer Schreib- oder Lesestabilität in einem konkreten Halbleiterprozess. Der reguläre Export der Vorlesung muss nach der Integration erneut visuell geprüft werden.

FACHLICHE REFERENZEN
David Harris, Harvey Mudd College, Lecture 15: SRAM, insbesondere PDF-Seiten 6–9:
https://pages.hmc.edu/harris/class/e158/lect15-sram.pdf

MIT OpenCourseWare, 6.111, Memory Basics and Timing, PDF-Seite 5:
https://ocw.mit.edu/courses/6-111-introductory-digital-systems-laboratory-spring-2006/499fae5e27b58a4b28605923aebe210e_lec7.pdf

Die SVGs sind neu gezeichnete Lehrschemata; es wurden keine fremden Grafiken übernommen.
