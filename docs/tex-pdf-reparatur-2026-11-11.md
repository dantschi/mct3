# Deutsche Vorlesungs-PDFs: Setup-Reparatur vom 11. November 2026

Das festgelegte TinyTeX-Basisarchiv enthält nicht alle Pakete für die von
Quarto erzeugten deutschen LuaLaTeX-Handouts. `lang: de` aktiviert Babel;
dessen LuaLaTeX-Konfiguration `bidi=basic` benötigt unter anderem
`luatexbase`. Der erste Abbruch erfolgt daher vor dem eigentlichen Inhalt.

Das gemeinsame Setup ergänzt `luatexbase`, `babel-german`, `hyphen-german`
und `selnolig` einschließlich Abhängigkeiten. Der erste Actions-Lauf mit
dieser Ergänzung zeigte eine weitere Voraussetzung: Der im Basisarchiv
enthaltene `tlmgr` war für das aktuelle Paketrepository zu alt und brach
mit Exitcode 255 ab.

Vor einer nötigen Paketinstallation führt `scripts/setup-tex.sh` nun
`tlmgr update --self` aus. Sowohl dieses Update als auch die anschließende
Installation verlangen verifizierte Repository-Signaturen. Es wird keine
allgemeine Aktualisierung der TeX-Distribution angefordert. Sind alle
benötigten Dateien bereits vorhanden, entfallen Update und Installation;
die echte deutsche PDF-Prüfung läuft trotzdem erneut.

## Tatsächlich geprüfter lokaler Stand

- Vollständiges gemeinsames Setup erfolgreich: Paketverwaltung aktualisiert,
  die vier Zusatzpakete sowie `ctablestack` installiert, Sprachdateien und
  TeX-Formate erzeugt. Repository-Signaturprüfung erfolgreich.
- `scripts/tex-smoke.tex` erfolgreich mit LuaLaTeX kompiliert. Die Vorlage
  prüft deutsche Sprachbehandlung, TeX-Gyre-Schriften, Formeln und die
  für die Handouts verwendeten Boxen. Auch ein zweiter vollständiger
  Setup-Aufruf war erfolgreich und benötigte keine erneute Installation.
- Alle 58 Python-Tests bestanden, darunter neun Setup-Tests. Self-Update-
  und Installationsfehler werden getrennt getestet; ein fehlgeschlagenes
  Self-Update darf weder Installation noch Kompilierung auslösen.
- `python3 scripts/build-materials.py all` erfolgreich: zehn Websitequellen,
  neun reguläre Vorlesungshandouts und alle zehn Übungs-/Prüfungsblätter
  in beiden PDF-Profilen frisch gebaut. Es liegen keine Programmierprojekt-
  Manifeste vor; daher sind keine Startcode-ZIPs Teil dieses Laufs.
- Alle neun Handouts enthalten ihre fortlaufenden 510 Foliennummern und
  510 Notizüberschriften. Alle 433 Handoutseiten wurden textuell auf
  Ersatzzeichen und außerhalb des Papiers liegenden Text geprüft.
  Zusätzlich wurden 26 repräsentative Handoutseiten tatsächlich angesehen:
  Schaltungen, Timing, Formeln, neue Grundlagenabbildungen und Skriptnotizen
  sind in diesen Stichproben lesbar. Dies ist keine visuelle Einzelabnahme
  sämtlicher Seiten und kein erneuter fachlicher Gesamtdurchgang.
- Die zwanzig Lab-PDFs wurden auf vorhandene Aufgaben, getrennte Lösungen
  und Ersatzzeichen kontrolliert. Die Studierendenfassungen enthalten keine
  Musterlösungen, die Lösungsfassungen enthalten die zusätzlichen Lösungen.
- Shellsyntax und `git diff --check` ohne Fehler.

GitHub Actions verwendet dieselben Setup- und Buildbefehle. Die Freigabe des
Deploy-Jobs bleibt an einen erfolgreichen vollständigen Build gebunden.
Der lokale Prüfnachweis ersetzt keine separate Kontrolle des Actions-Laufs.
Die Basiswerkzeuge bleiben durch Versionen und Archivprüfsummen festgelegt;
Manager- und Ergänzungspaketrevisionen stammen aus dem signierten Repository.
