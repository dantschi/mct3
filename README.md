# Mikrocomputertechnik 3 (MCT3)

Herzlich willkommen zur Vorlesung **Mikrocomputertechnik 3 (MCT3)** an der Dualen Hochschule Baden-Württemberg Stuttgart.

Das Modul vertieft digitale Rechnerarchitektur und die Hardware/Software-Schnittstelle am Beispiel der **RISC-V**-Architektur — von Speicherkonzepten und Organisation bis zu Entwurf und Verständnis moderner Mikrocomputer.

## Materialien

| Format | Link |
|--------|------|
| Folien (Reveal.js) | [01 · Speicherphysik & RAM-Typen](vorlesungen/01_speicherphysik.html) · [02 · Speicherhierarchie & Caches](vorlesungen/02_speicherhierarchie.html) · [03 · Interrupts & Timer](vorlesungen/03_interrupts_timer.html) · [04 · Aktorik & Sicherheit](vorlesungen/04_aktorik_sicherheit.html) |
| PDF-Handout (Skript) | [01 · Speicherphysik (PDF)](vorlesungen/01_speicherphysik-handout.pdf) · [02 · Caches (PDF)](vorlesungen/02_speicherhierarchie-handout.pdf) · [03 · Interrupts (PDF)](vorlesungen/03_interrupts_timer-handout.pdf) · [04 · Aktorik (PDF)](vorlesungen/04_aktorik_sicherheit-handout.pdf) |
| Übungsblatt | [Beispielblatt (PDF)](labs/lab_01_beispiel.pdf) |
| Musterlösung | [Beispielblatt Musterlösung (PDF)](labs/lab_01_beispiel-musterloesung.pdf) |

Das PDF-Handout enthält die Folien inklusive Dozentennotizen. Übungsblätter und Musterlösungen werden bei jedem Publish über GitHub Actions aktualisiert.

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
