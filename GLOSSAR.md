# Kursglossar: Mikrocomputertechnik 3

Dieses Glossar dokumentiert bevorzugte Bezeichnungen bereits eingeführter
MCT3-Konzepte. Es ergänzt die [Terminologieregeln](AGENTS.md#präzise-terminologie)
und die lokalen Erklärungen in den Lernnotizen. Die Fundstellen nennen die
zugehörige Vorlesung und den vorhandenen Folientitel; sie sind keine Behauptung
einer unabhängig geprüften Buchseite oder eines Hardwareversuchs.

## Pflege und Verwendung

- Verwenden Sie die bevorzugte Bezeichnung durchgängig in Folien, Notizen,
  Aufgaben, Musterlösungen, Quiz und Codeerläuterungen. Ordnen Sie Synonyme bei
  ihrer Einführung ausdrücklich zu.
- Ergänzen Sie Einträge anhand der tatsächlichen Einführung und der zentralen
  Literatur aus [README.md](README.md). Dokumentieren Sie bei externen Quellen
  nur geprüfte Ausgaben, Abschnitte und Seitenzahlen.
- Erhalten Sie reale Register-, API- und Codebezeichner. Ähnlich benannte
  Operationen oder technische Ebenen sind nicht automatisch gleichbedeutend.
- Ein Glossareintrag ersetzt weder die benötigte lokale Erklärung noch die
  Modellannahmen eines Rechenbeispiels. Er begründet keinen zusätzlichen
  Pflichtstoff.

## Speicher und Caches

| Bevorzugte Bezeichnung | Bedeutung und Abgrenzung | Synonyme bzw. englische Bezeichnung | Einführung / Fundstelle |
|---|---|---|---|
| SRAM | Flüchtiger statischer Speicher: Daten bleiben bei anliegender Versorgung ohne regelmäßiges Auffrischen erhalten. Zellprinzip und Zahl der Zugriffsports sind verschiedene Eigenschaften. | Static Random-Access Memory | [VL 1](vorlesungen/01_speicherphysik.qmd), „Im SoC müssen Datenwege zusammenpassen“ und die SRAM-Zellfolien |
| DRAM | Flüchtiger dynamischer Speicher: Der gespeicherte Ladungszustand muss aufgefrischt werden. Nicht mit SRAM oder einer Cache-Organisation gleichsetzen. | Dynamic Random-Access Memory | [VL 1](vorlesungen/01_speicherphysik.qmd), „Im SoC müssen Datenwege zusammenpassen“ und die DRAM-Zellfolien |
| Memory Map | Zuordnung von Adressbereichen zu Speicher und Geräten; legt nicht den aktuellen Cache-Inhalt fest. | Adressraumzuordnung | [VL 1](vorlesungen/01_speicherphysik.qmd), „Vier Schulstunden: Lernweg und Arbeitsphasen“; [VL 2](vorlesungen/02_speicherhierarchie.qmd), „Gleiche Adresse, anderer Lieferweg“ |
| FIFO | Reihenfolge, bei der zuerst eingefügte Elemente zuerst entnommen werden. Ein Ringpuffer ist eine mögliche Implementierung; bei Cache-Verdrängung bezeichnet FIFO die Ladereihenfolge. | First In, First Out | [VL 1](vorlesungen/01_speicherphysik.qmd), „FIFO: Ringposition allein verrät nicht voll oder leer“; [VL 2](vorlesungen/02_speicherhierarchie.qmd), „Verdrängen: FIFO und LRU“ |
| Cache-Zeile | Cache-Platz für die Kopie eines ausgerichteten Speicherblocks einschließlich zugehöriger Verwaltungsinformation. Blockadresse und Speicheradresse bleiben vom Lieferweg unabhängig. | Cache-Line, Cacheline; im Kontext auch Line | [VL 2](vorlesungen/02_speicherhierarchie.qmd), „Gleiche Adresse, anderer Lieferweg“ |
| Treffer / Fehlschlag | Ein Treffer benötigt eine gültige passende Cache-Kopie. Bei einem Fehlschlag kann die angefragte Information dort nicht geliefert werden. | Hit / Miss | [VL 2](vorlesungen/02_speicherhierarchie.qmd), „Zeitliche Lokalität: bald wieder dieselbe Adresse“ |
| AMAT | Mittlere Speicherzugriffszeit im jeweils angegebenen Modell. Eine zusätzliche Miss Penalty ist nicht die gesamte Miss-Zugriffszeit. | Average Memory Access Time; Hit Time; zusätzliche Miss Penalty | [VL 2](vorlesungen/02_speicherhierarchie.qmd), „Mittlere Zugriffszeit: AMAT“ |
| LRU | Verdrängt unter den zulässigen gültigen Plätzen den am längsten nicht genutzten Block. Anders als FIFO berücksichtigt die Regel auch Treffer. | Least Recently Used | [VL 2](vorlesungen/02_speicherhierarchie.qmd), „Verdrängen: FIFO und LRU“ |
| Write-Back / Dirty | Write-Back verändert zunächst die Cache-Kopie; Dirty kennzeichnet eine gegenüber der nächsten Ebene geänderte Zeile. Dirty bedeutet weder ungültig noch beschädigt. | Zurückschreiben; Änderungsbit | [VL 2](vorlesungen/02_speicherhierarchie.qmd), „Write-Back und Dirty“ |

## Ereignisse, Interrupts und Zeit

| Bevorzugte Bezeichnung | Bedeutung und Abgrenzung | Synonyme bzw. Registerzuordnung | Einführung / Fundstelle |
|---|---|---|---|
| Hart | Hardware-Ausführungskontext für einen Befehlsstrom. Das Grundmodell der Vorlesung verwendet genau einen Hart im Machine Mode. | Hardware Thread | [VL 3](vorlesungen/03_interrupts_timer.qmd), „Vorkenntnisse und Lehrmodell“ |
| Polling | Software fragt einen Gerätezustand selbst ab. Periodisches Polling und beschäftigtes Warten unterscheiden sich durch Abfragelücken und anderweitig verfügbare Rechenzeit. | Abfragen; Busy Waiting als besonderer Entwurf | [VL 3](vorlesungen/03_interrupts_timer.qmd), „Reaktionswege auf einer Zeitachse“ |
| Interrupt | Asynchrone Anforderung unabhängig vom gerade ausgeführten Befehl. Ein gespeichertes Ereignis, die Freigabe und die Bearbeitung sind getrennte Schritte. | Unterbrechung | [VL 3](vorlesungen/03_interrupts_timer.qmd), „Interrupt, Exception und Trap“ |
| Exception | Synchron aus der Ausführung eines Befehls entstandene Ausnahme. Vor einer Fortsetzung kann eine Korrektur oder andere Behandlung erforderlich sein. | Ausnahme | [VL 3](vorlesungen/03_interrupts_timer.qmd), „Interrupt, Exception und Trap“ |
| Trap | Gemeinsamer Übergang in die Behandlung eines Interrupts oder einer Exception. Der gleiche Eintrittsmechanismus macht die Ursachen nicht gleich. | Trap-Eintritt | [VL 3](vorlesungen/03_interrupts_timer.qmd), „Interrupt, Exception und Trap“ |
| PLIC / Claim / Complete | Der externe Interruptcontroller bündelt Quellen. Claim übernimmt eine wartende Geräte-ID; Complete schließt die übernommene Anforderung ab. Die Geräteursache ist gesondert nach Gerätevertrag zu behandeln. | Platform-Level Interrupt Controller | [VL 3](vorlesungen/03_interrupts_timer.qmd), „Kategorie ist nicht Geräte-ID“ und „Claim, Gerät bearbeiten, Complete“ |
| Eintrittslatenz / Behandlungsdauer / Reaktionszeit | Zeit bis zum Behandlungsbeginn, Dauer der Behandlung und gesamte Zeit bis zum benannten Reaktionsendpunkt sind verschiedene Größen. Blockierung und spätere Arbeit sind je nach Endpunkt zusätzlich zu berücksichtigen. | Interrupt-Latenz; ISR: Interrupt Service Routine | [VL 3](vorlesungen/03_interrupts_timer.qmd), „Reaktionswege auf einer Zeitachse“ und „Wann ist die Reaktion fertig?“ |
| Timer-Tick / Prozessorzyklus | Fortschritt der Timerzeitquelle und des Prozessortakts. Die Frequenzen dürfen bei Umrechnungen nicht stillschweigend gleichgesetzt werden. | `mtime` als Hardwarezeit; `mtimecmp` als Vergleichstermin | [VL 3](vorlesungen/03_interrupts_timer.qmd), „Timer-Ticks sind keine Prozessorzyklen“ |
| PWM / Tastverhältnis | Pulsweitenmodulation verändert die aktive Dauer innerhalb einer Periode. Tastverhältnis, HIGH-Pegel und Lastwirkung sind verschiedene Größen. | Pulse Width Modulation; Duty Cycle | [VL 4](vorlesungen/04_aktorik_sicherheit.qmd), „PWM: gleiche Periode, andere Pulsbreite“ |
| Watchdog | Überwachung eines vereinbarten Auffrischens bzw. Fortschrittsnachweises. Ein Reset allein belegt weder vollständige Fehlererkennung noch einen sicheren Aktorzustand. | Feed: Auffrischen | [VL 4](vorlesungen/04_aktorik_sicherheit.qmd), „Von Ereignissen zu Ausgaben“ und „Was ein Watchdog nicht nachweist“ |

## Datenbewegung, Parallelität und Beschleuniger

| Bevorzugte Bezeichnung | Bedeutung und Abgrenzung | Synonyme bzw. englische Bezeichnung | Einführung / Fundstelle |
|---|---|---|---|
| Open-Drain | Ein Ausgang treibt LOW aktiv und gibt die Leitung für HIGH frei. Ein Pull-up und die elektrischen Randbedingungen bestimmen das Ansteigen. | offener Drain-Ausgang | [VL 5](vorlesungen/05_serielle_bussysteme.qmd), „Open-Drain: LOW treiben, HIGH freigeben“ |
| DMA | Datenbewegung durch einen eigenständigen Controller. Die CPU muss nicht jedes Wort selbst kopieren; Konfiguration, Abschluss, Pufferzuständigkeit und Sichtbarkeit bleiben eigene Aufgaben. | Direct Memory Access | [VL 6](vorlesungen/06_hardware_beschleunigung_dma.qmd), „Voraussetzungen und Lehrmodell“ |
| Clean / Invalidate | Clean schreibt geänderte Cache-Daten zurück; Invalidate entzieht einer lokalen Kopie die Gültigkeit. Reihenfolge und notwendige Kombination richten sich nach Plattform und Übertragungsrichtung. | Cache-Maintenance | [VL 6](vorlesungen/06_hardware_beschleunigung_dma.qmd), „Empfang: Dirty-Daten können zurückschlagen“; [VL 9](vorlesungen/09_paralleles_rechnen_multicore.qmd), „Welche Teilnehmer gehören zur Kohärenzdomäne?“ |
| ILP | Verfügbare Parallelität zwischen Befehlen eines Programms. Die tatsächlich nutzbare Rate hängt zusätzlich von Ressourcen und Ausführungsmodell ab. | Instruction-Level Parallelism | [VL 7](vorlesungen/07_moderne_cpu_architekturen.qmd), „ILP ist verfügbare Unabhängigkeit“ |
| IPC / CPI | Bestätigte ISA-Befehle pro Kerntakt bzw. Kerntakte pro bestätigtem ISA-Befehl. Der Kehrwertbezug gilt nur bei derselben Zählbasis und demselben nichtleeren Fenster. | Instructions Per Cycle / Cycles Per Instruction | [VL 7](vorlesungen/07_moderne_cpu_architekturen.qmd), „IPC und CPI brauchen dieselbe Zählbasis“ |
| MAC | Multiplikation und Akkumulation. Die Konvention, eine MAC als zwei arithmetische Operationen zu zählen, ist keine Aussage über Takte oder Maschinenbefehle. | Multiply-Accumulate | [VL 8](vorlesungen/08_ki_beschleuniger_edge_ai.qmd), „MACs, Parameter und Operationen zählen“ |
| NPU / Edge AI | Eine NPU ist ein Beschleuniger für neuronale Verarbeitung. Edge AI bezeichnet den Verarbeitungsort am Rand eines vernetzten Systems und setzt keine NPU voraus. | Neural Processing Unit; künstliche Intelligenz am Edge | [VL 8](vorlesungen/08_ki_beschleuniger_edge_ai.qmd), „Edge ist ein Ort, keine Prozessorpflicht“ |
| Kohärenzdomäne | Teilnehmer und Speicherbereiche, deren gültige Kopien ein gemeinsames Protokoll koordiniert. CPU-Kohärenz umfasst nicht automatisch Geräte oder garantiert die Synchronisation eines Programms. | Coherence Domain | [VL 9](vorlesungen/09_paralleles_rechnen_multicore.qmd), „Welche Teilnehmer gehören zur Kohärenzdomäne?“ |
