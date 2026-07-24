# Mikrocomputertechnik 3 (MCT3)

Herzlich willkommen zur Vorlesung **Mikrocomputertechnik 3 (MCT3)** an der Dualen Hochschule Baden-Württemberg Stuttgart, Studiengang Elektro- und Informationstechnik.

**Dozent:** Prof. Dr.-Ing. Daniel Klünder  
**Kurswebsite:** [dantschi.github.io/mct3](https://dantschi.github.io/mct3/)  
**Repository:** [github.com/dantschi/mct3](https://github.com/dantschi/mct3)

Das Modul vertieft digitale Rechnerarchitektur und die Hardware/Software-Schnittstelle am Beispiel der **RISC-V**-Architektur. Aufbauend auf MCT1 zoomen wir vom isolierten CPU-Kern hinaus zum **System-on-Chip (SoC)**: Speicherphysik und -hierarchie, Interrupts und Timer, Aktorik, serielle Busse, DMA, moderne CPU-Features, Edge-AI-Beschleuniger und Multicore — bis hin zu hardwarenaher C-Programmierung am Gesamtsystem.

## Kursübersicht

Der rote Faden der Veranstaltung:

> Speicherzelle → Caches → Interrupts → Aktorik → Busse → DMA → OoO/Branch → Edge AI → Multicore

Pro Einheit: Folien (Reveal.js), Handout-PDF sowie Übungsblatt (Studierende / Musterlösung). Links verweisen auf die Kurswebsite.

| Einheit | Thema | Schwerpunkt | Folien | Handout | Übungsblatt | Musterlösung |
|---------|-------|-------------|--------|---------|-------------|--------------|
| 1 | Speicherphysik & RAM-Typen | SRAM/DRAM, Flash/XIP, Memory Map, Linker | [HTML](vorlesungen/01_speicherphysik.html) | [PDF](vorlesungen/01_speicherphysik-handout.pdf) | [PDF](labs/lab_01_speicherphysik.pdf) | [PDF](labs/lab_01_speicherphysik-musterloesung.pdf) |
| 2 | Speicherhierarchie & Caches | Lokalität, AMAT, Mapping, cache-freundlicher C-Code | [HTML](vorlesungen/02_speicherhierarchie.html) | [PDF](vorlesungen/02_speicherhierarchie-handout.pdf) | [PDF](labs/lab_02_speicherhierarchie.pdf) | [PDF](labs/lab_02_speicherhierarchie-musterloesung.pdf) |
| 3 | Interrupts & Timer | Direct/Vectored, CLINT/PLIC, Nested Interrupts, System-Tick | [HTML](vorlesungen/03_interrupts_timer.html) | [PDF](vorlesungen/03_interrupts_timer-handout.pdf) | [PDF](labs/lab_03_interrupts_timer.pdf) | [PDF](labs/lab_03_interrupts_timer-musterloesung.pdf) |
| 4 | Aktorik & Sicherheit | Hardware-Timer, PWM, Bit-Banging vs. Hardware, Watchdog | [HTML](vorlesungen/04_aktorik_sicherheit.html) | [PDF](vorlesungen/04_aktorik_sicherheit-handout.pdf) | [PDF](labs/lab_04_aktorik_sicherheit.pdf) | [PDF](labs/lab_04_aktorik_sicherheit-musterloesung.pdf) |
| 5 | Serielle Bussysteme | UART/SPI/I2C, Open-Drain, differentielle Übertragung, EMI | [HTML](vorlesungen/05_serielle_bussysteme.html) | [PDF](vorlesungen/05_serielle_bussysteme-handout.pdf) | [PDF](labs/lab_05_serielle_bussysteme.pdf) | [PDF](labs/lab_05_serielle_bussysteme-musterloesung.pdf) |
| 6 | Hardware-Beschleunigung (DMA) | Interrupt Storm, Bus-Mastering, Cache-Kohärenz, Ringpuffer | [HTML](vorlesungen/06_hardware_beschleunigung_dma.html) | [PDF](vorlesungen/06_hardware_beschleunigung_dma-handout.pdf) | [PDF](labs/lab_06_hardware_beschleunigung_dma.pdf) | [PDF](labs/lab_06_hardware_beschleunigung_dma-musterloesung.pdf) |
| 7 | Moderne CPU-Architekturen | ILP-Limits, Out-of-Order, Branch Prediction, Spectre-Idee | [HTML](vorlesungen/07_moderne_cpu_architekturen.html) | [PDF](vorlesungen/07_moderne_cpu_architekturen-handout.pdf) | [PDF](labs/lab_07_moderne_cpu_architekturen.pdf) | [PDF](labs/lab_07_moderne_cpu_architekturen-musterloesung.pdf) |
| 8 | KI-Beschleuniger & Edge AI | Memory Wall, Systolic Arrays, RVV, TensorFlow Lite Micro | [HTML](vorlesungen/08_ki_beschleuniger_edge_ai.html) | [PDF](vorlesungen/08_ki_beschleuniger_edge_ai-handout.pdf) | [PDF](labs/lab_08_ki_beschleuniger_edge_ai.pdf) | [PDF](labs/lab_08_ki_beschleuniger_edge_ai-musterloesung.pdf) |
| 9 | Paralleles Rechnen & Multicore | SMP, MESI, Atomics, Wrap-Up / Klausurvorbereitung | [HTML](vorlesungen/09_paralleles_rechnen_multicore.html) | [PDF](vorlesungen/09_paralleles_rechnen_multicore-handout.pdf) | [PDF](labs/lab_09_paralleles_rechnen_multicore.pdf) | [PDF](labs/lab_09_paralleles_rechnen_multicore-musterloesung.pdf) |

**Hinweise:** Folien im Browser öffnen (Speaker View: Taste `S`). Handout-PDF = Folieninhalt mit Skriptnotizen. Quelltexte unter `vorlesungen/` und `labs/`. Übungsblätter und Musterlösungen werden bei jedem Publish über GitHub Actions als PDF gebaut.

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

## OER und Lizenz

Dieses Vorlesungsmaterial ist eine **Open Educational Resource (OER)**. Die Vorlesungsinhalte – Texte, Code und Diagramme – stehen unter der Lizenz **[Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)**.

Sie dürfen diese Inhalte teilen und bearbeiten, sofern Sie die Urheberschaft angemessen nennen. Der vollständige Lizenztext liegt in der Datei [`LICENSE`](LICENSE) im Repository.

**Ausnahme:** Hochschullogos und andere geschützte Markenzeichen (einschließlich des DHBW-Logos) sind von dieser Lizenz **ausdrücklich ausgenommen**. Sie unterliegen dem Markenrecht der jeweiligen Rechteinhaber und dürfen ohne deren Genehmigung nicht übernommen oder weiterverwendet werden.
