# Vorlesung 9: Multicore ohne kursweiten Wiederholungsteil

Überarbeitung vom 11. November 2026 auf Basis von Commit `57c93ea`.
Die Nummer 9 und die bisherigen Materialpfade bleiben erhalten.

## Lernweg und Umfang

Die [Vorlesung](../vorlesungen/09_paralleles_rechnen_multicore.qmd) enthält
64 Folien mit jeweils einem vollständig überarbeiteten Notizblock.
Die Notizen sind als zusammenhängender Lerntext mit begründeten Übergängen,
ausgearbeiteten Beispielen und Modellgrenzen lesbar. Sie enthalten insgesamt
etwa 11.200 Wörter; sie sind kein Wort-für-Wort-Vortragsskript.

Sechs Abschnittsfolien und laufende Abschnittsmarkierungen geben Orientierung:

1. Arbeit aufteilen: Thread, Hart, Kern, gemeinsame Eingabe, private Rechnung
   und Zusammenführen nach beiden Abschlüssen.
2. Cachekopien koordinieren: gültige Kopien, Schreibrecht, MESI und False Sharing.
3. Gemeinsame Aktionen schützen: verlorene Updates, geschützter Abschnitt,
   atomare RMW und LR/SC.
4. Daten übergeben und fertig werden: Acquire/Release, C11, Sperren,
   Veröffentlichung und Fortschritt.
5. Beschleunigung begrenzen: feste Arbeit, Amdahl, Zusatzaufwand und Verteilung.
6. Einen Multicore-Entwurf begründen: zwei unabhängig veröffentlichte
   Teilsummen, vollständige Ergebnisübernahme und Fehlerfälle.

Der Einstieg fragt, ob zwei Kerne automatisch die doppelte Geschwindigkeit
und einen richtigen gemeinsamen Zähler ergeben. Die spätere Auflösung
beantwortet beide Fragen und begründet getrennte Teilsummen als Entwurfswahl.
Für den Fall mit 20 seriellen und 80 parallelen Zeiteinheiten ergeben zwei
Kerne 60 Einheiten und den Faktor 1,6667, nicht zwei.

Die beiden bisherigen Rückblicke auf Cacheadresszerlegung/AMAT und PWM
entfallen. Der frühere Weg durch Sensor, DMA und Gesamtveranstaltung ist
durch den Multicore-Anwendungsfall ersetzt. Die ursprünglichen fachlichen
Kerne einschließlich MESI-Lehrmodell K, LR/SC, C11, Deadlock, ISR-Selbstdeadlock
und Amdahl bleiben erhalten. Alle sechs ursprünglichen Codeblöcke sind
unverändert übernommen; ein neuer C11-Lehrausschnitt ergänzt den Sammler.
Gegenüber den ursprünglich 50 Folien entfallen drei bisherige Rückblick- bzw.
Systemwegfolien; 17 zusätzliche Erklär- und Gliederungsschritte ergeben 64.
Der bisherige Auftakt ist zur aktivierenden Frage umgeschrieben.

Die Einheit setzt die sichtbaren Vorlesungen 1–3 und 7–8 voraus. Ein
Betriebssystemkurs und die ausgeblendeten Einheiten 4–6 sind nicht nötig.
DMA wird ausschließlich lokal als Beispiel für eine gesondert zu prüfende
Kohärenzdomäne erklärt. Drei eigene neue SVG-/PNG-Abbildungen samt Generator
zeigen Schreibzuständigkeiten, alternative Zeilenrechte und die beiden
Veröffentlichungen. Ihre Pfeile bedeuten Zuordnung oder logische Ordnung,
keine gemessenen Zeitdauern.

## Übung, Quiz und Zeitbudget

Im [Übungsblatt](../labs/lab_09_paralleles_rechnen_multicore.qmd) ersetzt ein
neuer Sechs-Punkte-Fall die bisherige fachübergreifende Wiederholungsaufgabe.
Zwei Worker bearbeiten `[3, 6, 9, 12]`; die beabsichtigten Teilsummen sind
9 und 21, das Gesamtergebnis 30. Dies ist nicht das ausgearbeitete
Folienbeispiel `[1, 3, 5, 7]` mit den Ergebnissen 4, 12 und 16.

Die Aufgabe verlangt zusätzlich die Diagnose einer fehlerhaften Veröffentlichung,
die vollständigen Happens-before-Beziehungen, eine Layoutentscheidung gegen
False Sharing und eine Fehlerpolitik bei einem ausbleibenden Worker. Der
Transfer besteht in der gemeinsamen Beurteilung dieser getrennten Anforderungen,
nicht allein im Austausch von Zahlen. Die 1 + 2 + 2 + 1 Punkte bewerten
Ergebnis, Synchronisation, Layout und Fortschritt.

| Lernziel | Papieraufgaben | Quizfragen |
|---|---|---|
| Cachezustände, Rechte und Zeilengrenzen herleiten | 1–2, 6 | 1–4 |
| Updatezerlegung und atomare Übernahme unterscheiden | 3 | 5–7 |
| Nutzdatenveröffentlichung begründen | 4, 6 | 8 |
| Warteabhängigkeiten und fehlenden Fortschritt erkennen | 4, 6 | 9 |
| Beschleunigung bei fester Arbeit beurteilen | 5 | 10 |

Die zehn vorhandenen Quizfragen bleiben unverändert und sind durch die
erhaltenen Inhalte abgedeckt. Die Notizen erklären ausdrücklich, dass
relaxed RMW allein keine weiteren Nutzdaten veröffentlicht, erfolgreiche
Joins aber unabhängig davon frühere Workerzugriffe vor spätere Zugriffe des
Joiners ordnen. Damit wird die Erläuterung „über den Zähler“ in Quizfrage 7
nicht als allgemeines Bestreiten der Join-Synchronisation missverstanden.

Der 180-Minuten-Plan enthält 110 Minuten Erklärung und Besprechung,
55 Minuten ausgewählte Papierarbeit und 15 Minuten Quiz. Die Auswahl wird
ausdrücklich von den 75–90 Minuten für das vollständige selbstständige Blatt
unterschieden. Der Hostversuch bleibt optional. Diese Zeitangaben sind eine
Autorenplanung und keine empirisch nachgewiesenen Unterrichtszeiten.

## Durchgeführte Prüfungen

- Unabhängiger vollständiger fachlicher und didaktischer Durchgang durch
  Folien, Notizen, neue Diagrammquellen, Übungen, Musterlösungen und alle
  zehn Quizfragen: keine fachlichen Blocker festgestellt.
- Sämtliche Summen, Zeilengrenzen, Besitzerwechsel sowie Amdahl-, Effizienz-,
  Zusatzaufwands- und Lastverteilungsrechnungen unabhängig nachgerechnet.
  Die neu eingeführten Glossar-Fundstellen sind im Vortrag vorhanden.
- Quellenstruktur: 64 Folien, 64 passende Notizblöcke, sechs Trenner,
  gültige Bildpfade, ausgeglichene Codefences und UTF-8 ohne BOM geprüft.
- Alle drei neuen PNGs tatsächlich angesehen; SVG-Quellen und Pfeilzuordnung
  mit dem beschriebenen Modell abgeglichen. Es sind eigene Lehrdiagramme.
- Frische Reveal.js-Fassung mit Quarto 1.11.9 erzeugt. Alle 64 Folien in
  Chromium bei 1440 × 900 mit gesetzten Formeln geprüft: keine Überläufe,
  fehlenden Bilder oder falsch zugeordneten Notizblöcke. Einstiegs-,
  Grundlagen- und Abschnittsfolien zusätzlich visuell kontrolliert.
- Frische HTML-Lesefassung unter
  `_handout/vorlesungen/09_paralleles_rechnen_multicore.html` erzeugt:
  alle 64 Notizabschnitte sichtbar, keine fehlenden Bilder; Skriptansicht
  im Browser kontrolliert.
- Beide Lab-Profile frisch als reguläres PDF erzeugt: sieben Seiten für
  Studierende, acht Seiten mit Musterlösungen. Text und gerasterte Seiten
  auf Aufgabeninhalt, Code, Formeln, Arbeitsraum und Lösungstrennung geprüft.
  Die Studierendenfassung enthält sechs Lösungsbereiche ohne Musterlösung;
  die Lösungsfassung enthält alle sechs ausgearbeiteten Lösungen.
  Auch beide HTML-Profile wurden auf diese Trennung geprüft.
- Der vorhandene Quiz-CSV-Validator bestätigt zehn Fragen. Der unabhängige
  Inhaltsreview hat sämtliche Optionen und Erläuterungen geprüft.
- GCC 14.2.0: das unveränderte `labs/src/lab09_atomics.c` mit C11,
  `-O1 -g -Wall -Wextra -Werror -pedantic -pthread` und
  Address-/UndefinedBehaviorSanitizer übersetzt und erfolgreich ausgeführt.
  Ergebnisse: Teilsummen 10/26 und 36; vorgegebener Verlustfall eins;
  atomarer und gesperrter Zähler je 40000; veröffentlichte Payload 42.
- Die reparierte neue Aufgabe 6 zusätzlich als temporäres Zwei-Worker-
  Programm mit denselben Optionen in 100 frischen einmaligen Durchläufen
  geprüft. Die gewöhnlichen Ergebnisplätze wurden nach beiden Acquire-
  Beobachtungen vor den Joins gelesen: stets 9, 21 und 30. Der Versuch
  ergänzt die C11-Begründung; er beweist keine allgemeine Wartezeitschranke
  oder Eigenschaft beliebiger Hardwareabläufe. Die fehlerhafte Fassung mit
  gewöhnlichem Data Race wurde nicht als Zahlenbeweis ausgeführt.
- SHA-256-Vergleich bestätigt unveränderte Quellen der Einheiten 3, 7 und 8,
  das Quiz 9 sowie Folien, Labs und Quizdateien der ausgeblendeten Einheiten
  4–6. Bestehender Hostcode und ältere Abbildungen bleiben erhalten.
- `git diff --check` ohne Fehler.

## Grenze des Gesamtbuilds

`python3 scripts/build-materials.py all` wurde mit der gemeinsamen Toolchain
ausgeführt. Alle zehn Websitequellen wurden gerendert. Der reguläre
Vorlesungshandoutlauf scheiterte anschließend bereits bei Einheit 1 am
fehlenden `luatexbase.sty` in der installierten TeX-Umgebung. Für die
Vorlesungshandouts liegt damit keine aktuelle PDF-Freigabe vor; alte PDFs
werden nicht als Prüfnachweis verwendet. Die eigenständigen Lab-PDFs
und die HTML-Lesefassung ließen sich dagegen frisch erzeugen und prüfen.
Ein zusätzlicher gezielter PDF-Handoutlauf für Vorlesung 9 scheiterte am
gleichen fehlenden Paket; eine automatische Paketinstallation war deaktiviert.

Der anschließende gemeinsame Website-Build
(`python3 scripts/build-materials.py website`) war erfolgreich und hat die
aktualisierte Startseite sowie alle Vorträge unter `_site/` bereitgestellt.
Die dortige Vorlesung 9 enthält ebenfalls 64 Folien und 64 Notizblöcke;
die Startseite erhält die bisherige Auswahl ohne Einheiten 4–6.
Auch `python3 scripts/build-materials.py labs` war anschließend erfolgreich:
alle zehn Blätter einschließlich Probeklausur wurden in beiden PDF-Profilen
gebaut und unter `_site/labs/` bereitgestellt. Für Programmierpakete lagen
keine `lab.json`-Manifeste vor; es wurden daher keine Startcode-ZIPs erzeugt.

Es wird weder eine RISC-V-Firmwareausführung noch eine reale Multicore-
Laufzeit-, Kohärenz- oder Energiemessung behauptet. Ein erfolgreicher
Teilbuild ersetzt den fehlgeschlagenen vollständigen Build nicht.
