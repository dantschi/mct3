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
| Hart | Hardware-Ausführungskontext für einen Befehlsstrom. Das Grundmodell in VL 3 verwendet genau einen Hart im Machine Mode; VL 9 betrachtet mehrere Harts und trennt sie von Softwarethreads und physischen Kernen. | Hardware Thread | [VL 3](vorlesungen/03_interrupts_timer.qmd), „Vorkenntnisse und Lehrmodell“; [VL 9](vorlesungen/09_paralleles_rechnen_multicore.qmd), „Thread, Hart und Kern auseinanderhalten“ |
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


## Grundlagen der CPU-Architektur

Die folgenden Begriffe verbinden die überarbeitete [Vorlesung 7](vorlesungen/07_moderne_cpu_architekturen.qmd)
mit dem vorhandenen ILP- und IPC-Modell. Breiten und Zeitpunkte gelten immer
für die jeweils ausdrücklich benannte Stufe des Lehrmodells.

| Bevorzugte Bezeichnung | Bedeutung und Abgrenzung | Synonyme bzw. englische Bezeichnung | Einführung |
|---|---|---|---|
| Befehlssatzarchitektur / Mikroarchitektur | Die Befehlssatzarchitektur legt die für Software beschriebene Wirkung fest; die Mikroarchitektur setzt sie mit konkreten Stufen, Puffern und Rechenwerken um. | ISA: Instruction Set Architecture; Microarchitecture | VL 7, „Befehlssatz und Mikroarchitektur trennen“ |
| Pipeline | Verschiedene Schritte mehrerer Befehle überlappen. Ein einzelner Befehl benötigt weiterhin seine gesamte Verarbeitung; Überlappung allein ist keine Mehrfachstartbreite. | Fließbandverarbeitung | VL 7, Pipeline-Grundlagen |
| Superskalarität | Eine Mikroarchitektur kann mehrere gewöhnliche Befehle pro Takt starten. Breite ist eine Kapazität und weder eine zugesagte mittlere Rate noch automatisch Out-of-Order-Ausführung. | Superscalar execution | VL 7, Grundlagen und „Superskalarität beschreibt Breite“ |
| Ausführungseinheit | Hardware, die eine bestimmte Operation ausführen kann. Verfügbare Einheiten und Ports begrenzen gleichzeitig mögliche Starts auch bei unabhängigen Befehlen. | Functional unit; ALU: Arithmetic Logic Unit | VL 7, Ressourcen und Startbreite |
| Issue / Start | Auswahl und Start einer bereiten Operation in einer Ausführungseinheit nach der Konvention des jeweiligen Modells. Nicht mit Holen, Dekodieren oder Bestätigen gleichsetzen. | Instruction issue | VL 7, Start- und Abschlussmodell |
| Retire / Commit | Architektonische Bestätigung eines Befehls in der festgelegten Programmreihenfolge. Eine intern bereits fertige Operation kann vorher noch auf Bestätigung warten. | Retirement; Commit | VL 7, Start- und Abschlussmodell |
| Out-of-Order | Bereite jüngere Operationen dürfen unter den Modellregeln vor wartenden älteren starten. Die sichtbare Befehlswirkung muss trotzdem den Architekturvertrag erfüllen. | OoO | VL 7, „Out-of-Order ändert die Startreihenfolge“ |
| Latenz / Initiationsintervall | Latenz ist die Dauer bis zum Ergebnis einer gestarteten Operation; das Initiationsintervall ist der kleinste Abstand zwischen Starts auf der betreffenden Ressource. Beides sind keine universellen ISA-Eigenschaften. | Latency; initiation interval | VL 7, „Latenz und Initiationsintervall sind verschieden“ |

## Grundlagen der neuronalen Rechnung

Diese Begriffe werden in der erweiterten [Vorlesung 8](vorlesungen/08_ki_beschleuniger_edge_ai.qmd)
vor der Beschleunigerarchitektur eingeführt. Die kleinen Zahlenbeispiele sind
Lehrrechnungen mit vorgegebenen Parametern, keine behaupteten Trainingsergebnisse.

| Bevorzugte Bezeichnung | Bedeutung und Abgrenzung | Synonyme bzw. mathematische Zuordnung | Einführung |
|---|---|---|---|
| Modell | Festgelegte Rechenstruktur mit Parametern und einem Eingabe-/Ausgabevertrag. In der hier betrachteten Inferenz wird damit eine konkrete Beobachtung ausgewertet; die Eignung für die Anwendung ist gesondert zu prüfen. | Model; $\widehat y=f_\theta(x)$ | VL 8, „Ein Modell verbindet Eingabe und Ausgabe“ |
| Eingabemerkmal | Numerischer Bestandteil der beschriebenen Modelleingabe, etwa ein aufbereitetes Sensorsignal. Ein Rohdatenfenster und seine Vorverarbeitung gehören zum Eingabevertrag; Merkmale können in anderen Modellen auch gelernt werden. | Feature | VL 8, KI-Grundlagen |
| Vorverarbeitung / Sensorfenster | Ein Sensorfenster ist ein zeitlich begrenzter Ausschnitt von Messwerten; Vorverarbeitung ordnet oder transformiert ihn nach einer festgelegten Regel zur Modelleingabe. Reihenfolge, Skalierung und Zeitbezug müssen zur späteren Auswertung passen. | Preprocessing; input window | VL 8, „Vom Sensorfenster zur Eingabe“ |
| Modellparameter | Beim Training angepasste Zahlen wie Gewichte und Bias. Während der betrachteten Inferenz bleiben sie fest; neue Eingaben sind keine Parameteränderung. | Parameters; weights; bias | VL 8, KI-Grundlagen und „Welche Zahlen speichert ein Netz?“ |
| Zielwert / Label | Zur überwachten Lernaufgabe gehörende Sollausgabe eines Beispiels, etwa eine bekannte Klasse. Die Modellvorhersage wird damit verglichen; das Label ist kein zusätzlicher Eingang, der bei jeder späteren Inferenz bekannt wäre. | Target; class label | VL 8, Training und Beispieldaten |
| Training | Parameter anhand von Beispielen und einem festgelegten Fehlermaß anpassen. Gute Ergebnisse auf den Trainingsdaten allein belegen kein zuverlässiges Verhalten auf neuen Eingaben. | Model training; Verlustfunktion: loss function | VL 8, KI-Grundlagen und „Training und Inferenz sind verschiedene Arbeit“ |
| Inferenz | Neue Eingaben mit den festgelegten Parametern auswerten. Eingabeaufbereitung und die Interpretation der Ausgabe bleiben eigene Anwendungsschritte. | Inference | VL 8, KI-Grundlagen und „Training und Inferenz sind verschiedene Arbeit“ |
| Validierungsdaten | Von den zur Parameteranpassung verwendeten Beispielen getrennte Daten zur Auswahl von Varianten und Einstellungen. Der anschließend unabhängige Test wird davon unterschieden. | Validation set | VL 8, „Beispiele zum Lernen und zum Prüfen“ |
| Testdaten | Getrennte Beispiele zur Bewertung eines festgelegten Modells; sie dürfen nicht zugleich als gewöhnliche Trainingsbeispiele die hier geprüften Parameter bestimmen. Eine endliche Prüfung ist keine Garantie für jede reale Eingabe. | Test set | VL 8, Training und Bewertung |
| Bias | Eingabeunabhängiger Summand je Ausgang. Eine gewichtete Summe mit Bias ist allgemein affin; ohne Nichtlinearität werden mehrere affine Schichten wieder zu einer affinen Abbildung. | Verschiebung; bias vector | VL 8, gewichtete Summe und Schichten |
| Voraktivierung | Gewichtete Summe einschließlich Bias vor der Aktivierungsfunktion. Im Grundlagenbeispiel heißt sie $z=Wx+b$; im bewusst ohne Aktivierungsfunktion betrachteten älteren Dense-Beispiel wird die Ausgabe $y$ genannt. | Preactivation; affine Abbildung | VL 8, „Eine gewichtete Summe vollständig verfolgen“ |
| Aktivierungsfunktion | Nachgeschaltete Abbildung auf den berechneten Zahlen; beispielsweise ReLU als Maximum aus null und dem Eingang. Nicht mit den gespeicherten Aktivierungswerten gleichsetzen. | ReLU: Rectified Linear Unit | VL 8, KI-Grundlagen |
| Aktivierungen | Eingabe-, Zwischen- und Ausgabewerte einer konkreten Auswertung. Sie benötigen neben den Modellparametern eigenen Speicher; sie sind nicht die Aktivierungsfunktion selbst. | Activations | VL 8, „Welche Zahlen speichert ein Netz?“ |
| Dense-Schicht | Jeder Ausgang verwendet jeden Eingang mit einem eigenen Gewicht. Zeilen der Gewichtsmatrix gehören zu Ausgängen, Spalten zu Eingängen; ein Bias wird je Ausgang ergänzt. | Fully connected layer | VL 8, KI-Grundlagen und „Dense-Schicht: zwei gewichtete Summen“ |
| Batch | Mehrere Eingabebeispiele werden gemeinsam betrachtet. In der hier eingeführten Matrixdarstellung stehen die Beispiele als Spalten; die Orientierung ist eine explizite Konvention. | Eingabestapel; batch | VL 8, mehrere Eingaben als Matrix |
| Matrixprodukt / elementweise Operation | Ein Matrixprodukt bildet gewichtete Summen über eine gemeinsame innere Dimension. Eine elementweise Operation verknüpft die jeweils bezeichneten Elemente und ist eine andere Rechenregel. | Matrix multiplication; elementwise operation | VL 8, Matrix-Grundlagen |

## Gemeinsame Daten und Multicore

Die Begriffe der [Vorlesung 9](vorlesungen/09_paralleles_rechnen_multicore.qmd)
trennen die Koordination von Cache-Kopien, die Unteilbarkeit einer Operation,
die Ordnung verschiedener Speicherzugriffe und den Fortschritt eines Programms.
Das MESI-Lehrmodell K ist dabei ausdrücklich keine universelle Beschreibung
jedes realen Cache-Protokolls.

| Bevorzugte Bezeichnung | Bedeutung und Abgrenzung | Synonyme bzw. API-Zuordnung | Einführung / Fundstelle |
|---|---|---|---|
| Ausführungsfaden / Thread | Softwareseitige Folge von Programmschritten. Ein Thread kann auf einem Hart ausgeführt werden; mehrere Threads bedeuten noch keine gleichzeitige Ausführung auf mehreren Kernen. | Software thread; TLP: Thread-Level Parallelism | VL 9, „Thread, Hart und Kern auseinanderhalten“ und „TLP ergänzt ILP und DLP“ |
| Cache-Kohärenz | Koordination gültiger Kopien und der Reihenfolge von Änderungen desselben Speicherorts innerhalb der festgelegten Domäne. Macht weder eine Folge von Load/Änderung/Store unteilbar noch veröffentlicht sie allein andere Datenobjekte. | Cache coherence | VL 9, „Drei Mechanismen beantworten drei Fragen“ |
| MESI | Zustände Modified, Exclusive, Shared und Invalid beschreiben Gültigkeit und Rechte je Zeile. Shared bedeutet sauber und teilbar; die letzte verbliebene S-Kopie muss nicht automatisch E werden. | MESI-Protokoll; Lehrmodell K | VL 9, „MESI: Gültigkeit und Schreibrecht je Zeile“ |
| False Sharing | Verschiedene, unabhängig beschriebene Objekte teilen eine Kohärenzzeile. Das kann zusätzliche Übernahmen des Zeilenschreibrechts verursachen, ohne dass ein logischer Konflikt auf demselben Objekt vorliegt. | falsches Teilen; Padding als mögliche Layoutmaßnahme | VL 9, „False Sharing: verschiedene Variablen, eine Zeile“ |
| Atomare RMW | Lesen, Ändern und Schreiben bilden gegenüber konkurrierenden Zugriffen eine unteilbare Operation auf dem betreffenden Objekt. Getrennte atomare Loads und Stores ergeben keine atomare RMW. | Read-modify-write; etwa `atomic_fetch_add_explicit` | VL 9, „Die atomare RMW entscheidet die Übernahme“ |
| LR/SC | LR liest und reserviert; SC versucht einen bedingten Store. Erfolgsstatus null und geschriebener Datenwert sind getrennt. Bei Fehlschlag muss die Berechnung vom neu gelesenen Wert ausgehen; ein Fehler beweist nicht zwingend einen fremden Store. | Load-Reserved / Store-Conditional; `lr.w`, `sc.w` | VL 9, „LR liest; SC versucht den bedingten Store“ |
| Acquire / Release | Ordnungssemantik für eine passende Synchronisation. In der einmaligen Veröffentlichung ordnet ein Acquire, das den Release-Wert desselben Flags liest, die vorangehenden Nutzdatenschreibzugriffe vor nachfolgenden Nutzdatenlesezugriffen. | `memory_order_acquire`, `memory_order_release`; Happens-before | VL 9, „Acquire und Release ordnen die Nutzdaten“ und „Einmalige Veröffentlichung: bereit heißt Daten bereit“ |
| C-Data-Race | Konfligierende Zugriffe verschiedener Threads auf denselben Speicherort, mindestens einer schreibend und mindestens einer nicht atomar, ohne passende Happens-before-Ordnung. In C11 ist das Verhalten undefiniert; daraus folgt keine gültige Liste möglicher Endwerte. | data race; nicht mit jedem logischen Race gleichsetzen | VL 9, „Race Condition und C-Data-Race unterscheiden“ |
| Deadlock | Beteiligte können wegen einer zyklischen Warteabhängigkeit nicht fortfahren. Atomare Lockoperationen allein verhindern weder einen solchen Kreis noch garantieren sie Fairness oder eine beschränkte Wartezeit. | Verklemmung; Fortschritt: liveness | VL 9, „Deadlock: korrekte Atomics, falsche Wartebeziehung“ |
| Speedup / Effizienz | Speedup ist die Ein-Kern-Zeit geteilt durch die Zeit mit N Kernen; Effizienz ist Speedup geteilt durch N. Amdahls Grundmodell betrachtet feste Arbeit, einen festen seriellen Anteil und zunächst keinen Zusatzaufwand. | Beschleunigungsfaktor; Amdahl's law | VL 9, „Amdahl: feste Arbeit enthält serielle Zeit“ |
