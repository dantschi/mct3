# Fachlicher Gesamtdurchgang MCT3

Stand: 20. Oktober 2026. Geprüft wurden die neun Vorlesungen mit insgesamt
450 Folien und 450 Notizblöcken, ihre eingebundenen Abbildungen,
neun Übungsblätter mit 54 Pflichtaufgaben, 96 QuizAcademy-Fragen,
die Probeklausur sowie die begleitenden Host-C-Beispiele.

## Fachlicher Abgleich

| Einheit | Geprüfte Zusammenhänge |
|---|---|
| 1 | Flash-Bitänderungen, 6T-SRAM-Topologie und Zugriffsphasen, DRAM-Ladungsteilung, DDR-Datenrate, Adressgrenzen und Startup |
| 2 | Kalter und warmer Cache, AMAT einschließlich bedingter L2-Missrate, Adressfelder, Ersetzung, Writeback und Arrayspuren |
| 3 | Trap-Zustand, Kategorie und Geräte-ID, Vektorslots, 64-Bit-Timerzugriffe auf RV32, Sollraster, PLIC-Claim und Threshold |
| 4 | Inklusive Zählgrenzen, Polarität, Mittel- und Effektivwert, RC-Restwelligkeit, Compare-Übernahme und Watchdog-Fristen |
| 5 | UART-Bitfolge und Pufferfristen, SPI-Flanken und Schiebeablauf, I²C-Elektrik und Quittungen, Zweierkomplement und Gleichtakt |
| 6 | Leitungs- und CPU-Budget, Elementbreite, Adressinkrement, Cachewartung, Besitzwechsel, Ringüberlauf und Ping-Pong-Fristen |
| 7 | Pipelinefenster, IPC/CPI, RAW/WAR/WAW, Registerversionen, Issue/Retire, präziser Zustand und Sprungprädiktoren |
| 8 | Dense- und Matrixrechnung, Roofline-Zählgrenze, RVV-Längenregeln, systolische Welle, Quantisierung und Speicherbudgets |
| 9 | MESI-Zustände und Datenwerte, False Sharing, LR/SC, C11-Atomics, Release/Acquire, Deadlock und Amdahl |

Der Aufbau führt von Speicherzellen und Adressen über Ereignisse und
Datenbewegung zur internen und zur Mehrkernparallelität. Neue Spezialbegriffe
werden in den jeweiligen Notizen erläutert. Die Arbeitsphasen ergeben jeweils
180 Unterrichtsminuten; die längeren Zeitangaben der Übungsblätter beziehen sich
auf vollständige selbstständige Bearbeitung.

## Korrigierte Befunde

- **Probeklausur B4:** Die ungültigen RISC-V-Namen `t7` und `t8` wurden durch
  `a0` und `a1` ersetzt. Die abgefragten WAW-, RAW- und WAR-Beziehungen bleiben
  fachlich erhalten.
- **I²C, Vorlesung und Übung 5:** Der Sinkstrom der Pull-up-Untergrenzenformel
  ist jetzt als Referenz der garantierten LOW-Treiberfähigkeit bei vorgegebenem
  Ausgangspegel definiert. Eine absolute Stromgrenze ist eine separate
  Anforderung. Die Parallelwiderstandsaufgabe nennt den Pegel ihrer Stromrechnung.
- **Übung 7:** Retire ist ausdrücklich frühestens im Folgetakt der Fertigstellung
  erlaubt. Der CPI-Vergleich hält die bestätigte Befehlszahl und die Frequenz fest.
- **Multicore-Quiz:** Die Zählerfrage nennt Anfangswert null und den erfolgreichen
  Join beider Worker als Voraussetzungen für den Endwert `2N`.
- **Timerfrage A5:** Ein neuer Vergleichstermin liegt ausdrücklich strikt in der
  Zukunft. Die mehrdeutige Formulierung „hinter der aktuellen Zeit“ entfällt.
- **Begriffe:** Die DRAM-Überschrift bezeichnet die etwa 55 mV als Abweichung vom
  Vorladepegel. Die Deadlock-Erklärung umfasst auch blockierende Abhängigkeiten
  zum unterbrochenen eigenen Kontext.
- **Quizqualität:** Eingebettete Semikolons in vier Antwortfeldern des Cache-Quiz
  wurden gemäß Importregel entfernt. Die regelmäßige Lösungspositionsfolge
  `1,2,3,4,…` in den Quizdateien 1, 6 und 7 wurde aufgelöst; Antworttexte und
  zugehörige Wahrheitswerte bleiben jeweils zusammen.
- **Kursübersicht:** Die Probeklausur ist mit 60 Minuten und 60 Punkten ausgewiesen.
- **Skripte:** Zu breite Codezeilen wurden in den Vorlesungen 2, 3, 4, 5 und 9
  umgebrochen, damit Befehle und Funktionssignaturen vollständig lesbar sind.

## Durchgeführte Prüfungen

- Unabhängige Rechen- und Zustandsmodelle für Cache-Spuren, Timertermine,
  PWM, Buszeiten, DMA-Bereiche, Befehlspläne, Prädiktoren, RVV-Restlängen,
  systolische Arrays und MESI. Lösungen und Einheiten wurden damit abgeglichen.
- Vier SRAM-Schaltbilder anhand der tatsächlichen SVG-Leitungen geprüft:
  jeweils sechs Transistoren, sieben getrennte Netze und passende Zustandsfarben.
- Vier ausführbare Hostprogramme mit strengen GCC-Warnungen, einmal mit
  AddressSanitizer/UndefinedBehaviorSanitizer und einmal mit `-O3` geprüft.
  Das Abschnittsbeispiel wurde als Objekt übersetzt und per Symboltabelle geprüft.
- Zwölf eingebettete C-Funktionen separat geprüft, darunter alle 65.536
  Zweierkomplement-Bytepaare und Grenzfälle der Prozent-/Compare-Rechnung.
  Die beiden timerartigen Registerfunktionen wurden an Host-Arrays geprüft.
- Alle CSV-Dateien: elf Spalten, vier Antworten, genau eine richtige Antwort,
  unveränderte Fragenzahl und kein Semikolon in einem Feld. Antwortlängen wurden
  kontrolliert. Die Probeklausur enthält zwanzig Fragen mit je vier Optionen,
  darunter Fragen mit mehreren und mit vier richtigen Antworten, sowie fünf
  Papieraufgaben; die Bewertung ergibt 20 + 40 = 60 Punkte.
- Website und neun Skript-PDFs erzeugt; je Vorlesung fünfzig korrekt zugeordnete
  Notizblöcke kontrolliert. Alle zwanzig Aufgaben-PDFs wurden auf Profiltrennung,
  enthaltene Aufgaben und Seitenränder geprüft. UTF-8 und Git-Diff wurden geprüft.

Die Prüfung belegt die Konsistenz der angegebenen Lehrmodelle und die getesteten
Hostfunktionen. Tatsächliche RISC-V-Firmware, Renode-Gerätemodelle, elektrische
Grenzwerte konkreter Bausteine und reale Laufzeit- oder Energiemessungen erfordern
einen gesonderten Plattformversuch. Nach den aufgeführten Korrekturen wurden im
Durchgang keine weiteren fachlichen Widersprüche in den geprüften Materialien
festgestellt.
