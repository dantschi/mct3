# Kompakte Schaltungsbilder für Vorlesung 1

Die Folien verwenden rohe SVGs für das Web und reproduzierbare PNG-Versionen
für das PDF-Skript. Beide entstehen mit:

```bash
python3 assets/figures/01_speicherphysik/build_figures.py --png
python3 assets/images/01_speicherphysik/check_topology.py
```

Der PNG-Schritt benötigt Playwright und Chromium. Die SVG-Erzeugung und der
Topologiecheck verwenden nur die Python-Standardbibliothek.

Die 6T-Bilder enthalten zwei pMOS, vier nMOS, implizite Substratanschlüsse
und sieben getrennte Netze. Kreise am pMOS-Gate kennzeichnen dessen
Steuerwirkung; Leitungssprünge bedeuten **keine Verbindung**. Punkte markieren
Verbindungen. Vorladung, Leseverstärker und Schreibtreiber sind außerhalb der
sechs Zelltransistoren und als Randbedingungen angegeben.

`check_topology.py` liest die tatsächlich gezeichneten äußeren Leitungen und
Komponentenanschlüsse, vergleicht deren Verbindungen mit der unabhängigen
Referenz `../../figures/01_speicherphysik/6t/topologie.json` und prüft beide
stabilen digitalen Zustände. Der Bericht steht in `pruefprotokoll.json`.
Die vorhandenen ausführlichen 6T-Zeichnungen im Referenzordner bleiben erhalten.

Das sind qualitative Schaltungs- und Zeitmodelle. Sie berechnen weder Ströme,
Lesestörabstände, Schreibfähigkeit noch physikalische Verzögerungen. Die
Timingbilder besitzen deshalb keine Nanosekundenachse. Die 1T1C-DRAM-Zelle
verwendet ausdrücklich eine vereinfachte Plattenspannung von null Volt.
