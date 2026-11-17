# Berechnete Abbildungen für Vorlesung 8

Erzeugung aus dem Repository-Stamm:

```bash
python3 code/vl08_activity_demo.py
```

Benötigt werden Python 3, NumPy und Matplotlib. Es werden keine Daten aus dem
Netz geladen. Der kuratierte Ausschnitt, Herkunft, Einheitenbeleg und originale
MIT-Lizenz liegen unter `assets/data/08_motion_sense/`.

Die PNGs dienen dem Vortrag, die gleichnamigen SVGs bleiben als skalierbare
Exporte erhalten. Die Diagramme sind selbst erstellt; dargestellte Messwerte
stammen aus MotionSense, nicht aus einer eigenen Messung mit Studierenden.

| Datei | Daten, Modell und Aussage |
|---|---|
| `traces` | Drei vorab gewählte Ausschnitte von Person 1, jeweils 512 Messpunkte. Gezeigt wird der Betrag der rohen Beschleunigung einschließlich Gravitation in g. Die Zeit folgt der angegebenen nominellen Abtastrate 50 Hz. „Laufen“ bezeichnet hier die Datensatzaktivität `jogging`. |
| `features` | Alle 1152 nicht überlappenden Fenster mit je 32 XYZ-Messpunkten. Zwei erklärende Merkmale sind Mittelwert und Populationsstandardabweichung (`ddof=0`) des Beschleunigungsbetrags. Die drei Klassen haben verschiedene Farben und Markerformen. Diese Merkmale sind nicht der 96-Eingang des Netzes. |
| `boundary` | Dieselbe zweidimensionale Merkmalsdarstellung, mit nur aus Trainingspersonen berechneter Standardisierung. Die Linien sind didaktisch festgelegt und nicht trainiert. Für normierte Gewichte gilt `w=(cos(phi),sin(phi))`: links Drehung von 135° nach 110° bei Bias null, rechts Bias 0 bzw. −0,75 bei gleichem Winkel 135°. Jede Linie ist die Nullmenge eines einzelnen Neurons, keine vollständige Dreiklassenentscheidung. |
| `gradient` | Analytisches Ein-Parameter-Beispiel `L(w)=(2w−4)^2`: Ableitung −8 bei `w=1`, ein Gradientenabstiegsschritt mit Lernrate 0,1 nach `w=1,8`. Der Verlust sinkt von 4 auf 0,16. Diese Funktion ist nicht die Kreuzentropie des Aktivitätsmodells. |
| `relu_regions` | Links `ReLU(z)=max(0,z)`. Rechts ein separates mathematisches Beispiel: Vier verborgene Ausgaben `ReLU(x1), ReLU(−x1), ReLU(x2), ReLU(−x2)` ergeben mit Ausgang `s=sum(h)−1` die stückweise lineare Grenze `abs(x1)+abs(x2)=1`. Das ist keine gemessene Klassengrenze und behauptet nicht, dass drei Klassen zwingend eine verborgene Schicht benötigen. |
| `training` | Tatsächlich ausgeführtes Training: 600 im Voraus festgelegte Epochen mit Adam, Lernrate 0,003, Batchgröße 64, Seed 20261117. Gezeigt werden Training und Validierung; der zunehmende Validierungsverlust macht Überanpassung sichtbar. Es wurde kein Checkpoint nach diesen Kurven oder dem Test gewählt. |

Das Netz besitzt 96 Eingänge, 16 ReLU-Neuronen und drei unnormierte
Ausgangsscores in der Reihenfolge `standing`, `walking`, `jogging`. Ein Eingang
besteht aus 32 Zeitpunkten mit jeweils XYZ, zeitpunktweise zu 96 Werten
angeordnet. Seine Standardisierung wird ausschließlich auf Personen 1–16
angepasst. Personen 17–20 dienen der Validierung, 21–24 dem getrennten Test.

`model-activity.json` enthält Float32-Gewichte und Float32-Standardisierung.
`model-summary.json` enthält Versionsangaben, Splits, Kurven, Konfusionsmatrizen
und ein vorab festgelegtes Testfenster (Person 21, `walking`, Fenster 0). Die
berichteten Scores und Kennzahlen stammen aus einem Float32-Vorwärtslauf der
exportierten Werte. Der JSON-Text selbst ist keine kompakte Firmwaredatei.

Die 1603 Netzparameter würden als rohe Float32-Werte 6412 Byte beanspruchen.
Die zusätzliche Standardisierung enthält 96 Mittelwerte und 96 Streuungen,
also weitere 768 Byte. Runtime, Aktivierungen und Arbeitsbereiche sind damit
noch nicht bilanziert. Es handelt sich um ein reproduzierbares Lehrmodell
auf einem kleinen Datenausschnitt, keine validierte Aktivitätserkennung für
beliebige Personen und keine Aussage über eingebettete Laufzeit oder Energie.
