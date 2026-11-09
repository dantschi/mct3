# Mikrocomputertechnik 3 (MCT3)

Herzlich willkommen zur Vorlesung **Mikrocomputertechnik 3 (MCT3)** an der Dualen Hochschule Baden-Württemberg Stuttgart, Studiengang Elektro- und Informationstechnik.

**Dozent:** Prof. Dr.-Ing. Daniel Klünder  
**Kurswebsite:** [dantschi.github.io/mct3](https://dantschi.github.io/mct3/)  
*Hinweis: Quellen im Repo unter [`vorlesungen/`](vorlesungen/) und [`labs/`](labs/).*  
**Repository:** [github.com/dantschi/mct3](https://github.com/dantschi/mct3)

Das Modul vertieft digitale Rechnerarchitektur und die Hardware/Software-Schnittstelle am Beispiel der **RISC-V**-Architektur. Aufbauend auf MCT1 zoomen wir vom isolierten CPU-Kern hinaus zum **System-on-Chip (SoC)**: Speicherphysik und -hierarchie, Interrupts und Timer, Aktorik, serielle Busse, DMA, moderne CPU-Features, Edge-AI-Beschleuniger und Multicore — bis hin zu hardwarenaher C-Programmierung am Gesamtsystem.

## Kursrahmen und Lernziele

Die folgenden Angaben beschreiben die Planung dieser Materialien; ein
Modulhandbuch mit Fassung und verbindlichen Prüfungsregeln liegt hier nicht vor.

| Rahmen | Angaben zur Veranstaltung |
|--------|---------------------------|
| Modul und Zielgruppe | Mikrocomputertechnik 3, Bachelor Elektro- und Informationstechnik, fünftes Semester |
| Voraussetzungen | MCT1/2, binäre und hexadezimale Zahlen, C-Zeiger und Arrays, Bitoperationen und Schleifen; bekannte STM32-Timer mit Prescaler und ARR |
| Zeitplanung | Je Einheit vier Schulstunden (180 Minuten) einschließlich Übung und Quiz; zusätzliche selbstständige Bearbeitungszeiten stehen auf den Übungsblättern |
| Prüfungsvorbereitung | Probeklausur mit 60 Minuten und 60 Punkten, Multiple Choice und offenen Papieraufgaben; verbindliche Prüfungsform und Hilfsmittel sind gesondert festzulegen |
| Technischer Rahmen | RISC-V-Lehrmodelle, RV32 soweit angegeben; C-Lehrcode und Hostversuche mit jeweils ausdrücklich genannten Voraussetzungen; konkrete Registeradressen und Zeitwerte sind plattformabhängig |

Nach Abschluss der Veranstaltung können Sie:

- Speicherarten und Cacheorganisationen erklären, Zugriffe zerlegen und deren Folgen berechnen.
- Interrupt-, Timer- und Peripherieabläufe herleiten und Reaktionsfristen unter benannten Annahmen prüfen.
- Datenübertragung, DMA und gemeinsame Datenzugriffe einschließlich Fehlerfällen begründet entwerfen.
- Prozessorparallelität, KI-Beschleuniger und Multicore im Hinblick auf Durchsatz, Speicher und Synchronisation beurteilen.

## Kursübersicht

Der rote Faden der Veranstaltung:

**Speicherzelle → Caches → Interrupts → Aktorik → Busse → DMA → OoO/Branch → Edge AI → Multicore**

Pro Einheit: Folien (Reveal.js), Handout-PDF sowie Übungsblatt (Studierende / Musterlösung). Links verweisen auf die Kurswebsite.

| Einheit | Thema | Schwerpunkt | Folien | Handout | Übungsblatt | Musterlösung |
|--------:|-------|-------------|:------:|:-------:|:-----------:|:------------:|
| 1 | Speicherphysik & RAM-Typen | SRAM/DRAM, Flash/XIP, Memory Map, Linker | [HTML](https://dantschi.github.io/mct3/vorlesungen/01_speicherphysik.html) | [PDF](https://dantschi.github.io/mct3/vorlesungen/01_speicherphysik-handout.pdf) | [PDF](https://dantschi.github.io/mct3/labs/lab_01_speicherphysik.pdf) | [PDF](https://dantschi.github.io/mct3/labs/lab_01_speicherphysik-musterloesung.pdf) |
| 2 | Speicherhierarchie & Caches | Lokalität, AMAT, Mapping, cache-freundlicher C-Code | [HTML](https://dantschi.github.io/mct3/vorlesungen/02_speicherhierarchie.html) | [PDF](https://dantschi.github.io/mct3/vorlesungen/02_speicherhierarchie-handout.pdf) | [PDF](https://dantschi.github.io/mct3/labs/lab_02_speicherhierarchie.pdf) | [PDF](https://dantschi.github.io/mct3/labs/lab_02_speicherhierarchie-musterloesung.pdf) |
| 3 | Interrupts & Timer | Ereignis- und Trap-Pfad, PLIC, Timer-Raster, Reaktionszeit, ISR/Hauptprogramm | [HTML](https://dantschi.github.io/mct3/vorlesungen/03_interrupts_timer.html) | [PDF](https://dantschi.github.io/mct3/vorlesungen/03_interrupts_timer-handout.pdf) | [PDF](https://dantschi.github.io/mct3/labs/lab_03_interrupts_timer.pdf) | [PDF](https://dantschi.github.io/mct3/labs/lab_03_interrupts_timer-musterloesung.pdf) |
| 4 | Aktorik & Sicherheit | Hardware-Timer, PWM, Bit-Banging vs. Hardware, Watchdog | [HTML](https://dantschi.github.io/mct3/vorlesungen/04_aktorik_sicherheit.html) | [PDF](https://dantschi.github.io/mct3/vorlesungen/04_aktorik_sicherheit-handout.pdf) | [PDF](https://dantschi.github.io/mct3/labs/lab_04_aktorik_sicherheit.pdf) | [PDF](https://dantschi.github.io/mct3/labs/lab_04_aktorik_sicherheit-musterloesung.pdf) |
| 5 | Serielle Bussysteme | UART/SPI/I2C, Open-Drain, differentielle Übertragung, EMI | [HTML](https://dantschi.github.io/mct3/vorlesungen/05_serielle_bussysteme.html) | [PDF](https://dantschi.github.io/mct3/vorlesungen/05_serielle_bussysteme-handout.pdf) | [PDF](https://dantschi.github.io/mct3/labs/lab_05_serielle_bussysteme.pdf) | [PDF](https://dantschi.github.io/mct3/labs/lab_05_serielle_bussysteme-musterloesung.pdf) |
| 6 | Hardware-Beschleunigung (DMA) | Interrupt Storm, Bus-Mastering, Cache-Kohärenz, Ringpuffer | [HTML](https://dantschi.github.io/mct3/vorlesungen/06_hardware_beschleunigung_dma.html) | [PDF](https://dantschi.github.io/mct3/vorlesungen/06_hardware_beschleunigung_dma-handout.pdf) | [PDF](https://dantschi.github.io/mct3/labs/lab_06_hardware_beschleunigung_dma.pdf) | [PDF](https://dantschi.github.io/mct3/labs/lab_06_hardware_beschleunigung_dma-musterloesung.pdf) |
| 7 | Moderne CPU-Architekturen | ILP-Limits, Out-of-Order, Branch Prediction, Spectre-Idee | [HTML](https://dantschi.github.io/mct3/vorlesungen/07_moderne_cpu_architekturen.html) | [PDF](https://dantschi.github.io/mct3/vorlesungen/07_moderne_cpu_architekturen-handout.pdf) | [PDF](https://dantschi.github.io/mct3/labs/lab_07_moderne_cpu_architekturen.pdf) | [PDF](https://dantschi.github.io/mct3/labs/lab_07_moderne_cpu_architekturen-musterloesung.pdf) |
| 8 | KI-Beschleuniger & Edge AI | Memory Wall, Systolic Arrays, RVV, TensorFlow Lite Micro | [HTML](https://dantschi.github.io/mct3/vorlesungen/08_ki_beschleuniger_edge_ai.html) | [PDF](https://dantschi.github.io/mct3/vorlesungen/08_ki_beschleuniger_edge_ai-handout.pdf) | [PDF](https://dantschi.github.io/mct3/labs/lab_08_ki_beschleuniger_edge_ai.pdf) | [PDF](https://dantschi.github.io/mct3/labs/lab_08_ki_beschleuniger_edge_ai-musterloesung.pdf) |
| 9 | Paralleles Rechnen & Multicore | SMP, MESI, Atomics, Wrap-Up / Klausurvorbereitung | [HTML](https://dantschi.github.io/mct3/vorlesungen/09_paralleles_rechnen_multicore.html) | [PDF](https://dantschi.github.io/mct3/vorlesungen/09_paralleles_rechnen_multicore-handout.pdf) | [PDF](https://dantschi.github.io/mct3/labs/lab_09_paralleles_rechnen_multicore.pdf) | [PDF](https://dantschi.github.io/mct3/labs/lab_09_paralleles_rechnen_multicore-musterloesung.pdf) |

**Hinweise:** Folien im Browser öffnen (Speaker View: Taste **S**). Handout-PDF = Folieninhalt mit Skriptnotizen. Quelltexte unter [`vorlesungen/`](vorlesungen/) und [`labs/`](labs/).

### Probeklausur

| Dokument | Studierende | Musterlösung |
|----------|:-----------:|:------------:|
| Probeklausur (60 Min., 60 Punkte) | [PDF](https://dantschi.github.io/mct3/labs/probeklausur.pdf) | [PDF](https://dantschi.github.io/mct3/labs/probeklausur-musterloesung.pdf) |

## Literatur

Zentrale Referenz dieses Moduls:

> **Sarah L. Harris, David Money Harris**  
> *Digital Design and Computer Architecture — RISC-V Edition*  
> Morgan Kaufmann

Definitionen, Terminologie und didaktischer Aufbau orientieren sich an diesem Standardwerk.

Zur Vertiefung empfohlen:

> **David A. Patterson, John L. Hennessy**  
> *Computer Organization and Design: The Hardware/Software Interface — RISC-V Edition*  
> Morgan Kaufmann

## Tools und Ressourcen

| Tool | Einsatz | Link |
|------|---------|------|
| **RISC-V GCC** | Bare-Metal-C nach RISC-V-Maschinencode (Cross-Toolchain) | [gcc.gnu.org](https://gcc.gnu.org/) |
| **Renode** | SoC-Simulator (CPU, Busse, Speicher, Peripherie) für Labor und Treiber | [renode.io](https://renode.io/) |
| **Compiler Explorer** | C live als RISC-V-Assembler betrachten (Optimierung, Scheduling) | [godbolt.org](https://godbolt.org/) |
| **Ripes** | Visueller RISC-V-Simulator (u. a. Data-Cache-Ansicht) | [github.com/mortbopet/Ripes](https://github.com/mortbopet/Ripes) |

### Kursglossar

Das [Kursglossar](GLOSSAR.md) hält die eingeführten Fachbegriffe und ihre
Zuordnung zu englischen Bezeichnungen und Registern fest.

## Materialien weiterentwickeln

Die [Build- und Autorenanleitung](TEMPLATE.md) beschreibt Einrichtung,
Ausgabeformate, sechs Autoren-Skills und geprüfte Startcode-Pakete. Die
Projektregeln stehen in [AGENTS.md](AGENTS.md) und [FACHREGELN.md](FACHREGELN.md).

Nach Einrichtung der gemeinsamen Toolchain:

```bash
source scripts/activate.sh
python3 scripts/build-materials.py all
```

Dieser Aufruf baut Website, alle Handouts sowie Übungsblätter und Probeklausur
jeweils für Studierende und mit Musterlösungen. Vorhandene Programmierprojekte
werden zusätzlich geprüft und als Startcode-ZIP paketiert. Ein Paket enthält
Anleitung, Startcode und freigegebene Tests; Referenzlösungen bleiben außerhalb
des ZIPs, sind in diesem öffentlichen Repository aber weiterhin einsehbar.
Das [Template-Beispiel](examples/template/README.md) erläutert die Paketstruktur
außerhalb des MCT3-Stoffplans.

GitHub Actions verwendet denselben vollständigen Build bei Pull Requests und
Pushes auf `main`. Der Deploy-Schritt veröffentlicht nur nach erfolgreicher
Prüfung die bereits gebauten Dateien aus `_site/`.

## OER und Lizenz

Dieses Vorlesungsmaterial ist eine **Open Educational Resource (OER)**. Die Vorlesungsinhalte – Texte, Code und Diagramme – stehen unter der Lizenz **[Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)**.

Sie dürfen diese Inhalte teilen und bearbeiten, sofern Sie die Urheberschaft angemessen nennen. Der vollständige Lizenztext liegt in der Datei [`LICENSE`](LICENSE) im Repository.

**Ausnahme:** Hochschullogos und andere geschützte Markenzeichen (einschließlich des DHBW-Logos) sind von dieser Lizenz **ausdrücklich ausgenommen**. Sie unterliegen dem Markenrecht der jeweiligen Rechteinhaber und dürfen ohne deren Genehmigung nicht übernommen oder weiterverwendet werden.
