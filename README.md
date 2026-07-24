# Mikrocomputertechnik 3 (MCT3)

Herzlich willkommen zur Vorlesung **Mikrocomputertechnik 3 (MCT3)** an der Dualen Hochschule Baden-Württemberg Stuttgart.

Das Modul vertieft digitale Rechnerarchitektur und die Hardware/Software-Schnittstelle am Beispiel der **RISC-V**-Architektur — von Speicherkonzepten und Organisation bis zu Entwurf und Verständnis moderner Mikrocomputer.

## Materialien

| Format | Link |
|--------|------|
| Folien (Reveal.js) | [01 · Speicherphysik & RAM-Typen](vorlesungen/01_speicherphysik.html) · [02 · Speicherhierarchie & Caches](vorlesungen/02_speicherhierarchie.html) · [03 · Interrupts & Timer](vorlesungen/03_interrupts_timer.html) · [04 · Aktorik & Sicherheit](vorlesungen/04_aktorik_sicherheit.html) · [05 · Serielle Bussysteme](vorlesungen/05_serielle_bussysteme.html) · [06 · Hardware-Beschleunigung (DMA)](vorlesungen/06_hardware_beschleunigung_dma.html) · [07 · Moderne CPU-Architekturen](vorlesungen/07_moderne_cpu_architekturen.html) · [08 · KI-Beschleuniger & Edge AI](vorlesungen/08_ki_beschleuniger_edge_ai.html) · [09 · Paralleles Rechnen & Multicore](vorlesungen/09_paralleles_rechnen_multicore.html) |
| PDF-Handout (Skript) | [01 · Speicherphysik](vorlesungen/01_speicherphysik-handout.pdf) · [02 · Caches](vorlesungen/02_speicherhierarchie-handout.pdf) · [03 · Interrupts](vorlesungen/03_interrupts_timer-handout.pdf) · [04 · Aktorik](vorlesungen/04_aktorik_sicherheit-handout.pdf) · [05 · Busse](vorlesungen/05_serielle_bussysteme-handout.pdf) · [06 · DMA](vorlesungen/06_hardware_beschleunigung_dma-handout.pdf) · [07 · CPU-Architekturen](vorlesungen/07_moderne_cpu_architekturen-handout.pdf) · [08 · Edge AI](vorlesungen/08_ki_beschleuniger_edge_ai-handout.pdf) · [09 · Multicore](vorlesungen/09_paralleles_rechnen_multicore-handout.pdf) |

Das PDF-Handout enthält die Folien inklusive Dozentennotizen.

### Übungsblätter

Zu den Vorlesungen 1–6 liegen PDF-Übungsblätter und zugehörige Musterlösungen vor (Build über GitHub Actions bei jedem Publish).

| Nr. | Thema | Übungsblatt | Musterlösung |
|-----|-------|-------------|--------------|
| 01 | Speicherphysik und Speicher-Mapping | [PDF](labs/lab_01_speicherphysik.pdf) | [PDF](labs/lab_01_speicherphysik-musterloesung.pdf) |
| 02 | Speicherhierarchie und Caches | [PDF](labs/lab_02_speicherhierarchie.pdf) | [PDF](labs/lab_02_speicherhierarchie-musterloesung.pdf) |
| 03 | Advanced Interrupts & Timer | [PDF](labs/lab_03_interrupts_timer.pdf) | [PDF](labs/lab_03_interrupts_timer-musterloesung.pdf) |
| 04 | Aktorik & Sicherheit | [PDF](labs/lab_04_aktorik_sicherheit.pdf) | [PDF](labs/lab_04_aktorik_sicherheit-musterloesung.pdf) |
| 05 | Serielle Bussysteme | [PDF](labs/lab_05_serielle_bussysteme.pdf) | [PDF](labs/lab_05_serielle_bussysteme-musterloesung.pdf) |
| 06 | Hardware-Beschleunigung (DMA) | [PDF](labs/lab_06_hardware_beschleunigung_dma.pdf) | [PDF](labs/lab_06_hardware_beschleunigung_dma-musterloesung.pdf) |

## Literatur

Die zentrale Referenz dieses Moduls ist:

> **Sarah L. Harris, David Money Harris**  
> *Digital Design and Computer Architecture — RISC-V Edition*  
> Morgan Kaufmann

Definitionen, Terminologie und didaktischer Aufbau orientieren sich an diesem Standardwerk.

Zur Vertiefung empfohlen:

> **David A. Patterson, John L. Hennessy**  
> *Computer Organization and Design: The Hardware/Software Interface — RISC-V Edition*  
> Morgan Kaufmann

## Tools & Ressourcen

| Tool | Einsatz | Link |
|------|---------|------|
| **RISC-V GCC** | C-Toolchain: Übersetzung von Bare-Metal-C nach RISC-V-Maschinencode | [GCC](https://gcc.gnu.org/) |
| **Renode** | SoC-Simulator (CPU, Busse, Speicher, Peripherie) für Labor und Treiberentwicklung | [Renode](https://renode.io/) |

## OER & Lizenz

Dieses Vorlesungsmaterial ist eine **Open Educational Resource (OER)**. Die Vorlesungsinhalte – Texte, Code und Diagramme – stehen unter der Lizenz **[Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)**.

Sie dürfen diese Inhalte teilen und bearbeiten, sofern Sie die Urheberschaft angemessen nennen. Der vollständige Lizenztext liegt in der Datei [`LICENSE`](LICENSE) im Repository.

**Ausnahme:** Hochschullogos und andere geschützte Markenzeichen (einschließlich des DHBW-Logos) sind von dieser Lizenz **ausdrücklich ausgenommen**. Sie unterliegen dem Markenrecht der jeweiligen Rechteinhaber und dürfen ohne deren Genehmigung nicht übernommen oder weiterverwendet werden.
