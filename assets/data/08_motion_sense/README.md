# Echte Aktivitätsmessungen für Vorlesung 8

Diese kleine Auswahl stammt aus **MotionSense**, nicht aus einer künstlichen
Signalerzeugung. Sie dient als nachvollziehbares Beispiel für Stehen, Gehen
und Joggen. Die Messungen stammen von einem iPhone in der vorderen Hosentasche.
Der vorgesehene Lernversuch ist keine validierte allgemeine Aktivitätserkennung.

## Quelle, Urheberschaft und Lizenz

- Datensatz: [MotionSense](https://github.com/mmalekzadeh/motion-sense),
  Mohammad Malekzadeh, Richard G. Clegg, Andrea Cavallaro und Hamed Haddadi.
- Gepinnter Repository-Stand:
  [`261cb0d60611a049ab38127738e42cc510ed50f4`](https://github.com/mmalekzadeh/motion-sense/tree/261cb0d60611a049ab38127738e42cc510ed50f4).
- Ausgangsarchiv:
  [`data/B_Accelerometer_data.zip`](https://github.com/mmalekzadeh/motion-sense/blob/261cb0d60611a049ab38127738e42cc510ed50f4/data/B_Accelerometer_data.zip).
- Die tatsächlich gelesene Repository-Lizenz ist **MIT**, Copyright (c) 2018
  Mohammad Malekzadeh. Ihr vollständiger Originaltext steht in [LICENSE](LICENSE).
  Die README stellt den Datensatz ausdrücklich in diesem Repository bereit;
  sie enthält keine abweichende Datenlizenz. Der ursprüngliche Lizenz- und
  Urheberhinweis bleibt bei Weitergabe dieser Messdatenauswahl erhalten.
- Gewünschte wissenschaftliche Quellenangabe aus der Original-README:
  Malekzadeh, M.; Clegg, R. G.; Cavallaro, A.; Haddadi, H. (2019):
  *Mobile Sensor Data Anonymization*. Proceedings of IoTDI '19, S. 49–58.
  DOI: [10.1145/3302505.3310068](https://doi.org/10.1145/3302505.3310068).

Die Originallizenz gilt für die übernommenen MotionSense-Daten. Sie ist keine
Änderung der Lizenz des gesamten Lehrmaterial-Repositories. Es werden keine
Fotos, Karten oder sonstigen Abbildungen des Datensatzes übernommen.

## Auswahl und Dateiformat

`motionsense-activities.csv` hat folgende Spalten:

| Spalte | Bedeutung |
|---|---|
| `subject` | ursprüngliche pseudonyme Personennummer 1–24 |
| `activity` | `standing`, `walking` oder `jogging` |
| `trial` | ursprünglicher Versuch: `std_6`, `wlk_7` oder `jog_9` |
| `sample` | ursprünglicher nullbasierter Zeilen-/Sampleindex im Versuch |
| `x`, `y`, `z` | unveränderte Beschleunigungswerte der drei Geräteachsen in g |

Pro Person und Aktivität werden die **mittleren 512 aufeinanderfolgenden
Samples** genau eines ursprünglichen Versuchs übernommen. Der Start ist
`floor((ursprüngliche Länge − 512) / 2)`. Es gibt keine nachträgliche Auswahl
anhand von Klassifikationsergebnissen und keine Normalisierung, Interpolation,
Glättung oder Resampling der CSV-Werte. Das Originalformat der drei
Zahlenstrings bleibt erhalten. Die Auswahl umfasst 72 Abschnitte und
36.864 Messzeilen.

Die Original-README nennt **50 Hz**. Daraus wird für Darstellungen die nominelle
relative Zeit `t = (sample − erster Sampleindex) / 50` in Sekunden abgeleitet.
Die CSV enthält keine unabhängig gemessenen Zeitstempel. Ein Fenster aus 32
aufeinanderfolgenden XYZ-Samples entspricht einer 96-dimensionalen Eingabe
und einer nominellen Fensterdauer von 0,64 s. Für den Lernversuch entstehen
16 nicht überlappende Fenster je Abschnitt, insgesamt 1.152 Fenster.

`provenance.json` enthält für jeden Abschnitt Quelldatei, ursprüngliche Länge,
ersten und letzten Originalindex sowie Hashwerte. Die Aktivitätslabels werden
aus den ursprünglichen Versuchslabels übernommen. Weitere personenbezogene
Metadaten werden nicht übernommen.

## Einheitenbeleg

MotionSense beschreibt die Aufzeichnung mit SensingKit auf Grundlage von Apple
Core Motion. Die Rohbeschleunigung enthält auch den Schwerkraftanteil; deshalb
liegt der Betrag beim ruhenden Gerät ungefähr bei 1 g statt bei null.

Die Einheitenzuordnung wurde über die tatsächlich gelesenen Quelltexte geprüft:

1. Die [MotionSense-README, Abschnitt Accelerometer_data](https://github.com/mmalekzadeh/motion-sense/blob/261cb0d60611a049ab38127738e42cc510ed50f4/README.md)
   ordnet die Daten dem Beschleunigungssensor und den Achsen x/y/z zu.
2. SensingKit übernimmt in
   [`SKAccelerometerData.m`](https://github.com/SensingKit/SensingKit-iOS/blob/2bffc5da83586ca746da5e025be2607f5abe1623/SensingKit/SKAccelerometerData.m)
   `accelerometerData.acceleration` direkt und schreibt dessen x/y/z unverändert
   in die CSV-Ausgabe.
3. Apple definiert `CMAcceleration` im SDK-Header `CMAccelerometer.h` ausdrücklich
   als Achsenbeschleunigungen „in G's“. Geprüft wurde der
   [iOS-18.0-SDK-Header in diesem gepinnten Spiegel](https://github.com/xybp888/iOS-SDKs/blob/4a48e5409f8ea6ac422c44d91b86fa0f8ae010ff/iPhoneOS18.0.sdk/System/Library/Frameworks/CoreMotion.framework/Headers/CMAccelerometer.h).
   Die [Apple-API-Dokumentation](https://developer.apple.com/documentation/coremotion/cmacceleration)
   ist der primäre Dokumentationseinstieg. Fremder SDK-Code wird hier nicht kopiert.

## Reproduktion und Trennung der Datenrollen

Aus dem Repository-Stamm:

```bash
python3 assets/data/08_motion_sense/extract_motionsense.py \
  --archive /tmp/motionsense/B_Accelerometer_data.zip
```

Fehlt das Archiv, lädt der Auswahlcode genau den gepinnten Stand herunter.
Das 20,7-MB-Originalarchiv bleibt außerhalb des Repositories. Der erwartete
Archiv-SHA-256 ist
`0bf7446dd2e6aca6f7a6ea55012c7e3d7a43887c34c6d05d480473f3216ee07b`.
Die geprüfte CSV hat SHA-256
`8c6c5718367ce7929b2e480ae236f322c1b16913213b204d399721e0e06578e1`.

Für das zugehörige Lehrtraining ist die Personentrennung festgelegt:

| Rolle | Personen | 32-Sample-Fenster |
|---|---|---:|
| Training | 1–16 | 768 |
| Validierung | 17–20 | 192 |
| Test | 21–24 | 192 |

Fenster derselben Person gelangen dadurch nicht über die Rollengrenzen.
Vorverarbeitungsparameter werden nur aus den Trainingsdaten bestimmt.
Eine kleine Testmenge ist ein begrenzter Nachweis für diesen Versuch und
keine Garantie für andere Personen, Smartphonepositionen oder Geräte.
