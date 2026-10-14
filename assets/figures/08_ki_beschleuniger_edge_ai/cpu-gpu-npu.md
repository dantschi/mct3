# Dieselbe Ausgabesumme auf CPU, GPU und NPU

Eigene MCT3-Abbildung zum bereits eingeführten Dense-Lehrbeispiel:
Gewichte `(1, 2, 3)`, Eingaben `(2, 1, 3)`, Bias `1`, Ausgang `14`.
Sie enthält keine Bildbestandteile, Logos oder Messwerte der externen Vorlage.
Gestaltung und Rechenbeispiel entstehen aus dem eigenen Diagrammquellcode.

Die Zeichnung vergleicht drei **beispielhafte** Datenwege:

- CPU: wiederverwendete skalare MAC mit Akkumulator;
- GPU: unabhängige Produkte mit anschließender Reduktion und Bias;
- NPU: mögliche Kette mit lokal geladenen Gewichten und bewegten Teilsummen.

CPUs können auch SIMD und andere Parallelität nutzen. Eine GPU berechnet nicht
beliebig viele Produkte gleichzeitig. NPU-Gewichte sind in diesem Beispiel
ladbare Parameter. Zeit und Energie sind nicht quantifiziert.
Der nachfolgende systolische Zeitplan der Vorlesung gilt für ein anderes,
Output-Stationary genanntes Modell und darf nicht auf diese Kette übertragen werden.

Reproduzieren vom Repository-Hauptordner:

```bash
python3 assets/figures/08_ki_beschleuniger_edge_ai/build_chip_comparison.py --png
```

SVG-Erzeugung: Python-Standardbibliothek und lokale Diagrammhelfer.
PNG-Erzeugung: Playwright und Chromium, alternativ `--chromium /pfad/zu/chromium`.
`cpu-gpu-npu.svg` ist die bearbeitbare Vektorquelle,
`cpu-gpu-npu.png` die Version für Folien und PDF.

Die Abbildung steht wie die übrigen eigenen Kursdiagramme unter
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), siehe die
[Repository-Lizenz](../../../LICENSE). Als Urheberangabe verwenden Sie
„Mikrocomputertechnik 3 (MCT3), dantschi/mct3“ mit einem Link zum Repository.
Die SVG-Datei enthält ebenfalls Lizenz- und Herkunftsmetadaten.
