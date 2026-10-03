#!/usr/bin/env python3
"""Lehrfiguren VL07. Zeiten und IPC gelten nur fuer das jeweils genannte Modell."""
from pathlib import Path

OUT = Path(__file__).resolve().parent
INK, MUTED = "#1D1D1F", "#5F6368"
C = ["#1565C0", "#E65100", "#1B5E20", "#6A1B9A", "#00838F"]
ERR, WAIT = "#B71C1C", "#F3E5D8"


def svg(w, h):
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">',
        f'<rect width="{w}" height="{h}" fill="#fff"/>',
        "<style>text{font-family:Arial,Helvetica,sans-serif;fill:#1D1D1F}</style>",
    ]


def T(x, y, s, size=15, fill=INK, w="600", anchor="start"):
    s = str(s).replace("&", "&amp;").replace("<", "&lt;")
    return (
        f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{w}" '
        f'fill="{fill}" text-anchor="{anchor}">{s}</text>'
    )


def R(x, y, w, h, stroke=INK, fill="#fff", sw=1.4):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" '
        f'stroke="{stroke}" stroke-width="{sw}"/>'
    )


def L(x1, y1, x2, y2, stroke=INK, sw=1.6, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" '
        f'stroke-width="{sw}"{d}/>'
    )


def save(name, p):
    (OUT / name).write_text("\n".join(p) + "\n</svg>\n", encoding="utf-8")
    print(name)


def cell(p, x, y, w, h, txt, fill, size=12):
    p.append(R(x, y, w, h, fill, fill, 0.4))
    p.append(T(x + w / 2, y + h * 0.68, txt, size, "#fff", "700", "middle"))


# A: 5-stage, color = instruction
def fig_a():
    p = svg(1200, 420)
    p.append(T(16, 22, "Skalares 5-Stufen-Modell. Farbe = Instruktion, nicht Stufe.", 16))
    p.append(T(16, 44, "Fuenf unabhaengige ALU-Befehle. Ohne Stall: 5+5-1 = 9 Takte, CPI = 9/5 = 1,8.", 14, MUTED, "400"))
    stages = ["IF", "ID", "EX", "MEM", "WB"]
    # grid cycles 1..9, rows I1..I5
    bw, bh = 78, 28
    x0, y0 = 150, 70
    for c in range(9):
        p.append(T(x0 + c * bw + bw / 2, y0 - 8, str(c + 1), 12, MUTED, "400", "middle"))
    for i in range(5):
        p.append(T(16, y0 + i * bh + 20, f"I{i+1}", 14, C[i]))
        for s, name in enumerate(stages):
            cyc = i + s  # 0-based cycle
            if cyc < 9:
                cell(p, x0 + cyc * bw + 2, y0 + i * bh + 2, bw - 6, bh - 6, name, C[i], 11)
    p.append(T(16, 250, "Stationaer ab Takt 5: ein WB je Takt. Davor Fuellung, danach Leerung.", 15))
    p.append(T(16, 278, "Ein RAW-Stall ohne Forwarding zwischen I1 und I2: +1 Takt, 10 Takte, CPI = 2,0.", 15, ERR))
    p.append(T(16, 310, "IPC = retired ISA-Befehle / Takte des Fensters = 5/9. Nicht aus einem einzelnen WB schliessen.", 14))
    p.append(T(16, 342, "CPI = 1/IPC nur fuer denselben Zeitraum und dieselbe Zaehlbasis.", 14, MUTED, "400"))
    p.append(T(16, 374, "T = N * CPI / f gilt bei konstanter Frequenz. Ein Compiler kann N aendern.", 14, MUTED, "400"))
    p.append(T(16, 406, "Micro-Ops zaehlen hier nicht als ISA-IPC.", 14, MUTED, "400"))
    save("pipe.svg", p)


def fig_b():
    p = svg(1200, 400)
    p.append(T(16, 22, "Vier unabhaengige ALU-Befehle. ALU-Latenz 1. Fuellung gehoert zum Fenster.", 15))
    p.append(T(16, 46, "Skalar: Issue und Retire hoechstens 1. Fenster 5 Takte, IPC = 4/5 = 0,8.", 15, C[0]))
    # scalar retire marks
    labels = ["I1 iss", "I2 iss / I1 ret", "I3 iss / I2 ret", "I4 iss / I3 ret", "I4 ret"]
    for i, lab in enumerate(labels):
        cell(p, 16 + i * 230, 64, 210, 32, lab, C[0], 12)
    p.append(T(16, 130, "Zweifach: Issue und Retire hoechstens 2. Fenster 3 Takte, IPC = 4/3 ca. 1,33.", 15, C[1]))
    dual = ["I1 I2 iss", "I3 I4 iss / I1 I2 ret", "I3 I4 ret"]
    for i, lab in enumerate(dual):
        cell(p, 16 + i * 300, 148, 280, 32, lab, C[1], 13)
    p.append(T(16, 220, "Takt 2 retiriert zwei Befehle. Das mittlere IPC des Fensters ist nicht 2.", 16, ERR))
    p.append(T(16, 252, "Nachhaltig mehrere Retires sind etwas anderes als ein einzelner Abschlussburst.", 15))
    p.append(T(16, 290, "Superskalar heisst Multiple Issue, nicht automatisch Out-of-Order.", 15))
    p.append(T(16, 322, "Drei Units garantieren weder drei passende Befehle noch IPC 3.", 15))
    p.append(T(16, 360, "Annahme: keine Abhaengigkeit, keine Cache-Misses, Retire im Takt nach dem Issue.", 13, MUTED, "400"))
    p.append(T(16, 386, "P_dyn ungefaehr alpha * C * V^2 * f. Leckleistung ist ein eigener Term. Breite ist nicht kostenlos.", 13, MUTED, "400"))
    save("width.svg", p)


def fig_c():
    p = svg(1200, 430)
    p.append(T(16, 22, "Vereinfachtes Front-End/Back-End. Breiten sind Annahmen, kein konkreter Kern.", 16))
    boxes = [
        (16, "Fetch 16 Byte", "C-ISA: keine feste Zahl"),
        (230, "Decode 3", "Dispatch 3"),
        (430, "Issue 3", "wenn bereit"),
        (640, "ALU0  ALU1", "Latenz 1"),
        (860, "LSU", "Load/Store"),
        (1020, "Retire 2", "Engpass hier"),
    ]
    for x, a, b in boxes:
        p.append(R(x, 48, 160 if x < 1000 else 160, 58, C[3] if "Retire" in a else C[0]))
        p.append(T(x + 8, 70, a, 14, C[3] if "Retire" in a else C[0]))
        p.append(T(x + 8, 92, b, 12, MUTED, "400"))
    p.append(T(16, 140, "MUL pipelined: Latenz 3 Takte, Initiationsintervall 1. Durchsatz ist nicht 1/Latenz-Wartezeit als Einzelstueck.", 14))
    p.append(T(16, 168, "Ein MUL alle Takte startbar, Ergebnis erst nach 3 Takten. Latenz und Durchsatz getrennt.", 15, C[1]))
    p.append(T(16, 210, "Belegung, ein Takt, drei unabhaengige Befehle add/add/lw:", 15))
    p.append(T(40, 240, "ALU0: add    ALU1: add    LSU: lw    Retire-Slots: 2", 16))
    p.append(T(16, 278, "Ausfuehrung koennte 3 schaffen, Retire nur 2. Der ROB fuellt sich. Engpass: Retire-Breite.", 15, ERR))
    p.append(T(16, 316, "Ein zweites lw im selben Takt passt nicht: nur eine LSU. Operationstyp begrenzt die Auslastung.", 15))
    p.append(T(16, 354, "Zusaetzliche Ports, Scheduler und Bypassnetze kosten Flaeche und Energie.", 14, MUTED, "400"))
    p.append(T(16, 386, "16 Fetch-Bytes sind bei komprimierten RISC-V-Befehlen keine feste Instruktionszahl.", 14, MUTED, "400"))
    p.append(T(16, 416, "Aktivitaet alpha, Kapazitaet C, Spannung V, Frequenz f. Keine feste GHz-Mauer aus diesem Modell.", 13, MUTED, "400"))
    save("frontend.svg", p)


def edge(p, x1, y1, x2, y2, label, col):
    p.append(L(x1, y1, x2, y2, col, 2))
    p.append(T((x1 + x2) / 2, (y1 + y2) / 2 - 6, label, 12, col, "700", "middle"))


def fig_d():
    p = svg(1200, 360)
    p.append(T(16, 22, "Dieselben IDs. RAW bleibt echt. WAR und WAW sind Namenskonflikte.", 16))
    # RAW
    p.append(T(40, 58, "RAW", 16, C[0]))
    p.append(R(20, 80, 200, 40, C[0]))
    p.append(T(28, 106, "I1 lw t0", 14, C[0]))
    p.append(R(20, 180, 220, 40, C[1]))
    p.append(T(28, 206, "I2 add t1,t0,t2", 14, C[1]))
    edge(p, 120, 120, 120, 180, "RAW t0", ERR)
    # WAR
    p.append(T(420, 58, "WAR", 16, C[1]))
    p.append(R(360, 80, 230, 40, C[1]))
    p.append(T(368, 106, "I2 liest t0", 14, C[1]))
    p.append(R(360, 180, 250, 40, C[2]))
    p.append(T(368, 206, "I3 sub t0,t4,t5", 14, C[2]))
    edge(p, 470, 120, 470, 180, "WAR t0", C[3])
    # WAW
    p.append(T(820, 58, "WAW", 16, C[2]))
    p.append(R(740, 80, 180, 40, C[0]))
    p.append(T(748, 106, "I1 schreibt t0", 14, C[0]))
    p.append(R(740, 180, 250, 40, C[2]))
    p.append(T(748, 206, "I3 schreibt t0 neu", 14, C[2]))
    edge(p, 860, 120, 860, 180, "WAW t0", C[4])
    p.append(T(16, 260, "Forwarding kuerzt RAW-Wartezeit, hebt die Abhaengigkeit nicht auf.", 15))
    p.append(T(16, 288, "Ein RAW-Paar hat ILP 1. Das ist nicht das ILP des ganzen Programms.", 15, ERR))
    p.append(T(16, 320, "RV32I/RV64I: 32 Integer-Architekturregister, x0 fest 0. RV32E ist ein anderes Profil.", 14, MUTED, "400"))
    p.append(T(16, 346, "Architekturregister sind Namen. Die physische Datei kann groesser sein. >100 ist keine Mindestzahl.", 14, MUTED, "400"))
    save("deps.svg", p)


def fig_e():
    p = svg(1280, 520)
    p.append(T(16, 20, "Gleiches Programm, gleiche Latenzen. In-Order stoppt hier global hinter dem Load.", 15))
    p.append(T(16, 42, "I1 lw Miss, Daten in Takt 4 bereit, Nutzer fruehestens Takt 5. ALU-Latenz 1. Retire-Breite OoO: 2.", 13, MUTED, "400"))
    p.append(T(16, 70, "In-Order, Issue 1. 7 Takte, 4 Retires, IPC = 4/7 ca. 0,57.", 15, C[0]))
    rows = [
        ("I1 lw", ["iss", "", "", "ret", "", "", ""]),
        ("I2 add", ["", "", "", "", "iss/ret", "", ""]),
        ("I3 sub", ["", "", "", "", "", "iss/ret", ""]),
        ("I4 and", ["", "", "", "", "", "", "iss/ret"]),
    ]
    draw_grid(p, rows, 96, C[0])
    p.append(T(16, 250, "OoO, Issue 2, zwei ALU, eine LSU. 6 Takte, IPC = 4/6 ca. 0,67.", 15, C[1]))
    rows2 = [
        ("I1 lw", ["iss", "wait", "wait", "cpl/ret", "", ""]),
        ("I2 add", ["raw", "raw", "raw", "raw", "iss/ret", ""]),
        ("I3 sub", ["iss/cpl", "fertig", "fertig", "wartet", "ret", ""]),
        ("I4 and", ["", "iss/cpl", "fertig", "wartet", "wartet", "ret"]),
    ]
    draw_grid(p, rows2, 276, C[1], cycles=6)
    p.append(T(16, 430, "I3 und I4 sind frueh fertig, duerfen vor I1 nicht retiren. Der Miss wird ueberlappt, nicht geloescht.", 14, ERR))
    p.append(T(16, 456, "Takt 3: beide ALU ungenutzt. Ein voller ROB wuerde spaeter auch unabhaengige Arbeit stoppen.", 14))
    p.append(T(16, 484, "Werte: mem=10, t2=1, t4=8, t5=3, t7=15, t8=3. Ergebnisse t0=10, t1=11, t3=5, t6=3.", 13, MUTED, "400"))
    p.append(T(16, 508, "Dieses In-Order-Stauverhalten ist die Lehrannahme, nicht jeder reale In-Order-Kern.", 13, MUTED, "400"))
    save("ooo.svg", p)


def draw_grid(p, rows, y, col, cycles=7):
    bw = 108
    x0 = 110
    for c in range(cycles):
        p.append(T(x0 + c * bw + bw / 2, y - 4, str(c + 1), 11, MUTED, "400", "middle"))
    for i, (name, cells) in enumerate(rows):
        p.append(T(16, y + i * 32 + 18, name, 13, C[i]))
        for c, txt in enumerate(cells):
            if not txt:
                p.append(R(x0 + c * bw, y + i * 32, bw - 4, 26, MUTED, "#fafafa", 0.6))
            else:
                fill = ERR if txt in ("wait", "raw", "wartet") else (WAIT if txt == "fertig" else col)
                ink = INK if txt == "fertig" else "#fff"
                p.append(R(x0 + c * bw, y + i * 32, bw - 4, 26, fill, fill, 0.4))
                p.append(T(x0 + c * bw + (bw - 4) / 2, y + i * 32 + 17, txt, 11, ink, "700", "middle"))


def fig_f():
    p = svg(1200, 460)
    p.append(T(16, 20, "PRF-Modell. Map-Update beim Rename ist nicht der Commit. x0 bekommt kein Ziel.", 15))
    p.append(T(16, 42, "Startmap: t0=P0 t1=P1=4 t2=P2=1 t3=P3 t4=P4=2 t5=P5=9 t6=P6=1. Frei: P10, P11, P13.", 13, MUTED, "400"))
    headers = ["Instr", "log. Q", "phys. Q", "neues Ziel", "Map danach", "Wert"]
    xs = [16, 200, 340, 500, 680, 900]
    for x, h in zip(xs, headers):
        p.append(T(x, 78, h, 13, MUTED, "400"))
    rows = [
        ("A add t0,t1,t2", "t1,t2", "P1,P2", "P10", "t0->P10", "P10=5"),
        ("B add t3,t0,t4", "t0,t4", "P10,P4", "P13", "t3->P13", "P13=7"),
        ("C sub t0,t5,t6", "t5,t6", "P5,P6", "P11", "t0->P11", "P11=8"),
        ("E add t1,t0,t2", "t0,t2", "P11,P2", "P14", "t1->P14", "liest P11"),
        ("F sub t0,t4,t5", "t4,t5", "P4,P5", "P12", "t0->P12", "WAR weg"),
    ]
    for i, row in enumerate(rows):
        y = 108 + i * 36
        for x, val in zip(xs, row):
            p.append(T(x, y, val, 14, C[min(i, 4)]))
    p.append(T(16, 300, "B liest die alte Version P10=5. C schreibt die neue Version P11=8. B sieht P11 nicht.", 15, C[1]))
    p.append(T(16, 330, "E liest t0 als P11. F erhaelt ein neues t0=P12. Das ist WAR, kein gemeinsames Ziel.", 15, C[3]))
    p.append(T(16, 362, "Freigabe des alten physischen Registers erst nach Commit, wenn kein aelterer Leser bleibt.", 14))
    p.append(T(16, 392, "Recovery stellt die gueltige Map wieder her. Nicht alle physischen Werte werden geloescht.", 14, ERR))
    p.append(T(16, 424, "Zwei freie ALUs sind zusaetzlich noetig. Renaming allein erzwingt kein gemeinsames Issue.", 14, MUTED, "400"))
    p.append(T(16, 448, "P10/P11 bleiben die Versionsnamen in den folgenden Folien.", 13, MUTED, "400"))
    save("rename.svg", p)


def fig_g():
    p = svg(1200, 480)
    p.append(T(16, 20, "PRF haelt Werte. ROB haelt Reihenfolge, Ready, Exception und Zielmetadaten. Kein Ergebniszylinder.", 14))
    snaps = [
        (16, "1 juenger fertig", "I3 ready, I1 nicht. Head zeigt auf I1."),
        (310, "2 aeltester fertig", "I1 ready. I3/I4 bleiben dahinter."),
        (610, "3 Retire", "Nur der Head retiriert, dann der naechste."),
        (900, "4 Exception", "I2 fault: kein Commit, juengere verworfen."),
    ]
    for x, a, b in snaps:
        p.append(R(x, 40, 280, 70, C[0]))
        p.append(T(x + 8, 64, a, 14, C[0]))
        p.append(T(x + 8, 88, b, 12, MUTED, "400"))
    p.append(T(16, 140, "Architektur vor dem Fault, nach Retire von I1: t0=10. t1, t3, t6 noch alt.", 15))
    p.append(T(16, 168, "Nach Squash bleiben diese Architekturwerte. P13/P11 im PRF sind nicht committed.", 15, ERR))
    p.append(T(16, 206, "Synchrone Exception: aeltere duerfen committen, der fehlerhafte Befehl nicht, juengere werden verworfen.", 14))
    p.append(T(16, 236, "Ein Interrupt ist kein fehlerhafter Befehl. Er wird an einer zulaessigen praezisen Grenze angenommen.", 14, C[1]))
    p.append(T(16, 270, "In-order-Retire ordnet die Architektursicht dieses Kerns. Andere Kerne sehen Speicher nicht automatisch so.", 14))
    p.append(T(16, 300, "RVWMO ist das Speichermodell. Store-Commit, Puffer-Drain und Register-Retire sind verschiedene Schritte.", 14, C[3]))
    p.append(T(16, 334, "Issue Queue: Operand bereit reicht nicht. Port, Unit und Auswahl muessen passen.", 14))
    p.append(T(16, 364, "Ein Common Data Bus ist das klassische Lehrbild. Reale Netze koennen verteilt sein.", 14, MUTED, "400"))
    p.append(T(16, 396, "OoO heisst datenabhaengige Reihenfolge, nicht eine taktlose CPU.", 15, ERR))
    p.append(T(16, 428, "ROB ist eine verbreitete Loesung fuer praezise Zustaende, nicht die einzige moegliche Struktur.", 13, MUTED, "400"))
    p.append(T(16, 456, "Head/Tail, ready und exception stehen im ROB. Der Zahlenwert steht in der PRF.", 13, MUTED, "400"))
    save("rob.svg", p)


def fig_h():
    p = svg(1200, 360)
    p.append(T(16, 20, "Aelterer Store, juengerer Load. Adressalias zuerst unbekannt. Eine Zusatzfolie.", 16))
    p.append(R(16, 48, 360, 120, C[0]))
    p.append(T(28, 74, "Adressen verschieden", 15, C[0]))
    p.append(T(28, 102, "Load darf unabhaengig laufen", 14))
    p.append(T(28, 128, "kein Replay", 14, C[2]))
    p.append(R(400, 48, 360, 120, ERR))
    p.append(T(412, 74, "Dieselbe Adresse", 15, ERR))
    p.append(T(412, 102, "Store-to-Load oder Replay", 14))
    p.append(T(412, 128, "Renaming loest das nicht", 14, ERR))
    p.append(R(790, 48, 380, 120, C[3]))
    p.append(T(802, 74, "Drei Schritte", 15, C[3]))
    p.append(T(802, 102, "1 Store-Queue", 14))
    p.append(T(802, 126, "2 Commit-Freigabe", 14))
    p.append(T(802, 150, "3 Memory-Drain", 14))
    p.append(T(16, 200, "Spekulative Stores duerfen nicht beliebig MMIO ausloesen.", 15, ERR))
    p.append(T(16, 230, "Kein Commit heisst nicht: der Cache bleibt ohne Seiteneffekt. Seitenkanaele sind ein anderes Thema.", 14))
    p.append(T(16, 262, "Unbekannte Aliasbeziehung: der Load wartet oder wird bei Konflikt wiederholt.", 14, MUTED, "400"))
    p.append(T(16, 294, "Register-Retire und sichtbarer Speicher sind nicht dasselbe Ereignis.", 14, MUTED, "400"))
    p.append(T(16, 330, "Modellannahme: eine LSU, eine Store-Queue, keine konkrete BOOM-Konfiguration.", 13, MUTED, "400"))
    save("lsu.svg", p)


def fig_i():
    p = svg(1200, 420)
    p.append(T(16, 20, "Annahmen: 20 Prozent Branches, 10 Prozent davon falsch, Penalty 15, Basis-CPI 1. Keine Ueberlappung.", 14))
    p.append(T(16, 44, "Aufschlag 0,20 * 0,10 * 15 = 0,30. CPI = 1,30.", 16, C[0]))
    p.append(R(16, 64, 360, 70, C[1]))
    p.append(T(28, 90, "Laufzeit * 1,30", 16, C[1]))
    p.append(T(28, 116, "30 Prozent laenger, gleiches N und f", 13))
    p.append(R(400, 64, 420, 70, C[2]))
    p.append(T(412, 90, "Durchsatz * 0,769", 16, C[2]))
    p.append(T(412, 116, "etwa 23,1 Prozent weniger Durchsatz", 13))
    p.append(T(16, 160, "Richtig vorhergesagt", 14, C[2]))
    p.append(T(16, 190, "Falsch", 14, ERR))
    for i, name in enumerate(["Br", "S1", "S2", "S3", "ok"]):
        cell(p, 120 + i * 70, 142, 60, 24, name, C[2], 12)
    for i, name in enumerate(["Br", "S1", "S2", "aufl.", "neu"]):
        col = ERR if name in ("S1", "S2", "aufl.") else C[0]
        cell(p, 120 + i * 70, 176, 60, 24, name, col, 12)
    p.append(T(16, 230, "Ein Treffer ist nicht automatisch kostenlos: Target und Fetch-Bandbreite bleiben.", 15))
    p.append(T(16, 258, "Die Penalty haengt von Aufloesung und Front-End ab, nicht nur von der Stufenzahl.", 15))
    p.append(T(16, 290, "Renaming entfernt WAR/WAW, nicht jede Datenabhaengigkeit und nicht den Branch.", 15, ERR))
    p.append(T(16, 322, "Die Kurve CPI = 1 + 0,20 * m * 15 ist ein Modell ueber die Fehlrate m, keine Messung.", 14, MUTED, "400"))
    p.append(T(16, 354, "1/1,30 = 0,76923. Nicht 23 Prozent laenger.", 16, ERR))
    p.append(T(16, 390, "Spekulative Kaestchen sind der falsche Pfad und werden verworfen, nicht retired.", 13, MUTED, "400"))
    save("cpi.svg", p)


def predictor_rows():
    """2-bit start 11, sequence TT TTN twice. Returns list of tuples."""
    seq = ["T", "T", "T", "T", "N", "T", "T", "T", "T", "N"]
    state = 3
    out = []
    for outcome in seq:
        pred = "T" if state >= 2 else "N"
        hit = pred == outcome
        nxt = min(3, state + 1) if outcome == "T" else max(0, state - 1)
        out.append((state, pred, outcome, hit, nxt))
        state = nxt
    return out


def fig_j():
    p = svg(1200, 520)
    p.append(T(16, 20, "2-Bit-Automat mit Saettigung. Vorhersage steht im Zustand, Update danach.", 16))
    # four states
    states = [(40, 70, "00 NT", False), (300, 70, "01 NT", False), (560, 70, "10 T", True), (820, 70, "11 T", True)]
    for x, y, name, taken in states:
        p.append(R(x, y, 140, 44, C[2] if taken else ERR))
        p.append(T(x + 70, y + 28, name, 16, C[2] if taken else ERR, "700", "middle"))
    p.append(L(180, 92, 300, 92, C[2], 2))
    p.append(L(440, 92, 560, 92, C[2], 2))
    p.append(L(700, 92, 820, 92, C[2], 2))
    p.append(T(210, 84, "T", 12, C[2]))
    p.append(T(470, 84, "T", 12, C[2]))
    p.append(T(730, 84, "T", 12, C[2]))
    p.append(L(820, 110, 700, 110, ERR, 2))
    p.append(L(560, 110, 440, 110, ERR, 2))
    p.append(L(300, 110, 180, 110, ERR, 2))
    p.append(T(730, 128, "NT", 12, ERR))
    p.append(T(470, 128, "NT", 12, ERR))
    p.append(T(210, 128, "NT", 12, ERR))
    p.append(L(40, 48, 40, 70, ERR, 2))
    p.append(L(180, 48, 40, 48, ERR, 2))
    p.append(T(70, 44, "NT", 12, ERR))
    p.append(L(860, 48, 1000, 48, C[2], 2))
    p.append(L(1000, 48, 1000, 70, C[2], 2))
    p.append(T(900, 44, "T", 12, C[2]))
    p.append(T(16, 150, "T: 00->01, 01->10, 10->11, 11->11. NT: 11->10, 10->01, 01->00, 00->00.", 15))
    p.append(T(16, 176, "Aus 11 aendert ein NT nur nach 10, Vorhersage bleibt T. Aus 10 reicht ein NT fuer NT.", 14, C[1]))
    rows = predictor_rows()
    p.append(T(16, 210, "Folge T T T T N | T T T T N, Start 11. Prediction vor dem Update.", 14, MUTED, "400"))
    labels = ["alt", "vorh", "ist", "treffer", "neu"]
    names = ["00", "01", "10", "11"]
    for i, h in enumerate(labels):
        p.append(T(16 + i * 90, 236, h, 12, MUTED, "400"))
    misses = 0
    for n, (st, pred, outcome, hit, nxt) in enumerate(rows):
        y = 256 + (n % 5) * 22
        xbase = 16 if n < 5 else 520
        vals = [names[st], pred, outcome, "ja" if hit else "nein", names[nxt]]
        if not hit:
            misses += 1
        for i, val in enumerate(vals):
            p.append(T(xbase + i * 90, y, val, 13, C[2] if hit else ERR))
    p.append(T(16, 390, "Warm, Start stark T: ein Miss je fuenf Ergebnisse, der Schleifenausgang N.", 15, C[2]))
    p.append(T(16, 416, "1-Bit, warm auf T: der Ausgang kippt auf N, der naechste Einstieg ist der zweite Miss.", 15, ERR))
    p.append(T(16, 444, "Kaltstart und sehr kurze Schleifen koennen andere Trefferzahlen liefern.", 14, MUTED, "400"))
    p.append(T(16, 472, "Aufgabe: Start 01, erstes Ergebnis T. Vorhersage ist N, Folgezustand 10. Loesung in den Notizen.", 14))
    p.append(T(16, 500, f"Nachgerechnete Misses in den zehn Schritten ab 11: {misses}.", 13, MUTED, "400"))
    save("pred.svg", p)


def fig_k():
    p = svg(1200, 400)
    p.append(T(16, 20, "Richtung und Ziel sind getrennt. Index nicht blind die niedrigsten Bits, Ausrichtung beachten.", 14))
    p.append(R(16, 48, 200, 50, C[0]))
    p.append(T(28, 78, "Fetch-PC", 16, C[0]))
    p.append(R(280, 48, 280, 50, C[1]))
    p.append(T(292, 78, "BHT: taken / not taken", 15, C[1]))
    p.append(R(620, 48, 280, 50, C[2]))
    p.append(T(632, 78, "BTB: Zieladresse", 15, C[2]))
    p.append(L(216, 73, 280, 73, INK, 2))
    p.append(L(560, 73, 620, 73, INK, 2))
    p.append(T(16, 130, "Aliasing, Index PC[4:2]: 0x04 und 0x24 liefern beide 001.", 16, ERR))
    p.append(T(16, 158, "Zwei verschiedene Branches koennen denselben Eintrag teilen und sich stoeren.", 14))
    p.append(T(16, 196, "gshare-Lehrbeispiel, 4 Bit: PC-Index 0101 XOR GHR 0011 = 0110.", 16, C[0]))
    p.append(T(16, 226, "Globale Historie ist nicht automatisch lokale plus globale Historie.", 15))
    p.append(T(16, 258, "Lokal, global und Hybrid-Auswahl sind verschiedene Modelle.", 15))
    p.append(T(16, 290, "TAGE und Perceptron sind veroeffentlichte Beispiele, nicht die Implementierung jedes Kerns.", 14, MUTED, "400"))
    p.append(T(16, 322, "Lernen heisst hier ein festes Hardware-Modell, keine allgemeine KI.", 14, MUTED, "400"))
    p.append(T(16, 360, "BHT/PHT: in diesem Bild ist BHT die Richtungstabelle. Das Ziel liegt nur im BTB.", 13, MUTED, "400"))
    save("bpred.svg", p)


def fig_l():
    p = svg(1200, 460)
    p.append(T(16, 18, "Spectre-v1, schematisch. Die Bounds-Pruefung bleibt architektonisch korrekt.", 15))
    steps = ["Bounds-Branch", "transienter Wert", "Probe-Zugriff", "Squash", "Timing"]
    for i, name in enumerate(steps):
        col = ERR if i in (1, 2, 4) else C[2]
        p.append(R(16 + i * 230, 40, 210, 36, col))
        p.append(T(24 + i * 230, 64, name, 14, col))
    p.append(T(16, 100, "Architektur", 14, C[2]))
    p.append(T(160, 100, "Pruefung gilt, falscher Pfad wird verworfen, Register/Map zurueck.", 14, C[2]))
    p.append(T(16, 130, "Cache", 14, ERR))
    p.append(T(160, 130, "Der abhaengige Probe-Zugriff kann eine Zeile zuruecklassen.", 14, ERR))
    p.append(T(16, 170, "Ein schneller Hit ist ein Indiz mit Rauschen, kein Beweis und keine Messung aus diesem Kurs.", 14))
    p.append(T(16, 210, "Spectre: falscher vorhergesagter Pfad. Meltdown: andere Privilege-Grenze, vor allem aeltere Designs.", 14))
    p.append(T(16, 240, "KPTI zielt auf den urspruenglichen Meltdown-Mechanismus, nicht auf jede Spectre-Variante.", 14, C[0]))
    p.append(T(16, 268, "Bounds-Masking oder eine passende Barriere kann bestimmte Spectre-v1-Faelle mildern.", 14, C[1]))
    p.append(T(16, 296, "Nicht jede Fence ist auf jeder ISA eine Spekulationsbarriere.", 15, ERR))
    p.append(T(16, 328, "Neuere Hardware mindert einzelne Wege. Sie macht nicht jeden Cache-Effekt unsichtbar.", 14))
    p.append(T(16, 360, "Auch In-Order-Kerne koennen spekulativ fetchen. OoO ist hier zusaetzlich, nicht die einzige Voraussetzung.", 13, MUTED, "400"))
    p.append(T(16, 388, "Rollback loescht nicht jeden mikroarchitektonischen Zustand und nicht die ganze PRF blind.", 13, MUTED, "400"))
    p.append(T(16, 420, "Keine Aussage: Spectre ist vollstaendig geloest.", 15, ERR))
    p.append(T(16, 446, "Quellen: spectreattack.com/spectre.pdf und meltdownattack.com/meltdown.pdf.", 12, MUTED, "400"))
    save("spectre.svg", p)


if __name__ == "__main__":
    for fn in (fig_a, fig_b, fig_c, fig_d, fig_e, fig_f, fig_g, fig_h, fig_i, fig_j, fig_k, fig_l):
        fn()
    misses = sum(1 for row in predictor_rows() if not row[3])
    assert misses == 2, misses
    assert abs(1 / 1.3 - 0.7692307) < 1e-5
    assert 0x04 >> 2 & 0x7 == 0x24 >> 2 & 0x7
    assert (0b0101 ^ 0b0011) == 0b0110
    print("checks ok", misses)
