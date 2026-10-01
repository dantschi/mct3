#!/usr/bin/env python3
"""Lehrfiguren VL05. Zeitdiagramme sind Modelle, keine Messungen.

Registeradressen und Renode-Aufrufe sind kein geprueftes Labor.
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent
INK, MUTED = "#1D1D1F", "#5F6368"
CLK, DATA, SAMP, ERR, GND, OK = (
    "#E65100",
    "#1565C0",
    "#6A1B9A",
    "#B71C1C",
    "#546E7A",
    "#1B5E20",
)


def svg(w, h):
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">',
        f'<rect width="{w}" height="{h}" fill="#fff"/>',
        "<style>text{font-family:Arial,Helvetica,sans-serif;fill:#1D1D1F}</style>",
    ]


def T(x, y, s, size=16, fill=INK, w="600", anchor="start"):
    s = (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
    return (
        f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{w}" '
        f'fill="{fill}" text-anchor="{anchor}">{s}</text>'
    )


def line(x1, y1, x2, y2, stroke=INK, sw=2, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" '
        f'stroke-width="{sw}"{d}/>'
    )


def rect(x, y, w, h, stroke=INK, fill="none", sw=1.6):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" '
        f'stroke="{stroke}" stroke-width="{sw}"/>'
    )


def circ(x, y, r, fill, stroke=None, sw=1.5):
    return (
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" '
        f'stroke="{stroke or fill}" stroke-width="{sw}"/>'
    )


def poly(pts, stroke, sw=2.4, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return (
        f'<polyline points="{p}" fill="none" stroke="{stroke}" stroke-width="{sw}" '
        f'stroke-linejoin="miter" stroke-linecap="square"{d}/>'
    )


def wave(levels, x0, y_low, y_high, bw):
    """levels: Folge von 0/1, jede Stufe dauert bw. y_low ist unten."""
    pts = []
    x = x0
    for lv in levels:
        y = y_high if lv else y_low
        pts.append((x, y))
        x += bw
        pts.append((x, y))
    return pts


def save(name, parts):
    (OUT / name).write_text("\n".join(parts) + "\n</svg>\n", encoding="utf-8")
    print(name)


def box(p, x, y, w, h, title, sub, stroke):
    p.append(rect(x, y, w, h, stroke, "#fff"))
    p.append(T(x + 8, y + 22, title, 15, stroke))
    if sub:
        p.append(T(x + 8, y + 42, sub, 13, MUTED, "400"))


def arrow(x1, y, x2):
    return line(x1, y, x2, y, INK, 2) + circ(x2, y, 3.2, INK)


# ---------------------------------------------------------------------------
# 1 Weg und drei Verdrahtungen
# ---------------------------------------------------------------------------
def fig_path():
    p = svg(1200, 430)
    p.append(T(16, 26, "Vom Sensorregister zur CPU. Drei Adressarten, drei Verdrahtungen.", 18))
    p.append(T(16, 48, "Lehrschema. GND gehoert dazu, zaehlt aber nicht als Signalleitung.", 14, MUTED, "400"))
    labels = [
        (16, "Sensorregister", "ACCEL ab 0x3B", DATA),
        (250, "Bitstrom", "Protokollrahmen", CLK),
        (470, "Bus-Controller", "FIFO / Datenreg.", SAMP),
        (700, "MMIO-Load", "z. B. 0x4001....", ERR),
        (930, "CPU-Register", "uint8_t / int16_t", OK),
    ]
    for x, a, b, c in labels:
        box(p, x, 64, 210, 58, a, b, c)
    for x in (226, 446, 680, 910):
        p.append(arrow(x, 93, x + 22))
    p.append(T(16, 154, "Getrennte Symbole: Quadrat = SoC-MMIO, Sechseck nur als Text: I2C-Adresse 0x68, gestrichelt = internes Register.", 14, MUTED, "400"))
    # three wirings
    cols = [
        (20, "UART 0/3,3 V, nicht isoliert", [
            "TX1 ----- RX2",
            "RX1 ----- TX2",
            "GND ----- GND",
            "Frame ist nicht RS-232.",
        ]),
        (410, "SPI Mode-0-Grundmodell", [
            "SCK  ----- SCK",
            "MOSI ----- MOSI/SDI",
            "MISO ----- MISO/SDO",
            "CS   ----- CS, plus GND",
        ]),
        (800, "I2C Open-Drain", [
            "SDA -- Pull-up -- SDA",
            "SCL -- Pull-up -- SCL",
            "GND ----------- GND",
            "HIGH = loslassen",
        ]),
    ]
    for x, title, rows in cols:
        p.append(rect(x, 176, 370, 210, INK))
        p.append(T(x + 12, 202, title, 16))
        yy = 232
        for i, row in enumerate(rows):
            col = ERR if i == 3 and "RS-232" in row else INK
            p.append(T(x + 16, yy, row, 16, col, "400"))
            yy += 32
        p.append(line(x + 16, 360, x + 340, 360, GND, 3))
        p.append(T(x + 16, 378, "gemeinsamer Bezug", 13, GND, "400"))
    p.append(T(16, 414, "MPU6050-Beispiel: Beschleunigungsrohwerte. Neigung ist daraus nur unter Annahmen abgeleitet.", 15, ERR))
    save("path.svg", p)


# ---------------------------------------------------------------------------
# 2 Parallel, Schieberegister, 0x53
# ---------------------------------------------------------------------------
def fig_shift():
    p = svg(1200, 420)
    p.append(T(16, 26, "0x53 = 0101 0011 in MSB-Schreibweise. UART sendet d0 zuerst.", 18))
    bits = [0, 1, 0, 1, 0, 0, 1, 1]  # b7..b0
    p.append(T(16, 58, "Parallel, b7 links bis b0 rechts. Ankunft versetzt, ein gemeinsames Fenster.", 15, MUTED, "400"))
    base = 150
    for i, b in enumerate(bits):
        y = 78 + i * 18
        p.append(line(70, y, 70 + 28 * 8, y, MUTED, 1, "3 3"))
        # skew: each line arrives later
        x_arr = 90 + i * 22
        p.append(line(x_arr, y - 6, x_arr, y + 6, DATA, 3))
        p.append(T(40, y + 4, f"b{7-i}={b}", 13, INK, "400"))
    p.append(rect(250, 70, 36, 150, OK, "none", 1.5))
    p.append(T(292, 150, "gueltiges Fenster", 14, OK))
    p.append(T(620, 78, "Serielle Folge, LSB zuerst:", 15))
    seq = [1, 1, 0, 0, 1, 0, 1, 0]
    x0, bw, y_lo, y_hi = 620, 52, 150, 100
    p.append(poly(wave(seq, x0, y_lo, y_hi, bw), DATA, 2.6))
    for i, b in enumerate(seq):
        p.append(T(x0 + i * bw + 16, 176, str(b), 16, DATA, "700", "middle"))
        p.append(T(x0 + i * bw + 16, 196, f"d{i}", 13, MUTED, "400", "middle"))
    p.append(T(16, 250, "Schieberegister, vereinfachtes Links-Modell nur fuer die sichtbaren Bits. UART schiebt faktisch LSB hinaus.", 14, MUTED, "400"))
    rows = [
        ("Start", "0101 0011", "Leitung leer", "........"),
        ("nach d0,d1", "0101 00..", "1 dann 1", "..000011"),
        ("nach 8 Bit", "........", "Frame fertig", "0101 0011"),
    ]
    p.append(T(16, 278, "Sender", 14, CLK))
    p.append(T(280, 278, "Leitung", 14, DATA))
    p.append(T(560, 278, "Empfaenger", 14, OK))
    for i, (name, a, b, c) in enumerate(rows):
        y = 300 + i * 32
        p.append(T(16, y, name, 14, MUTED, "400"))
        p.append(T(120, y, a, 16))
        p.append(T(280, y, b, 16, DATA))
        p.append(T(560, y, c, 16, OK))
    p.append(T(16, 408, "Seriell beseitigt Laufzeit nicht. USB/PCIe sind andere Kodierungen, kein On-Board-UART.", 14, MUTED, "400"))
    save("shift.svg", p)


# ---------------------------------------------------------------------------
# 3 UART-Frame
# ---------------------------------------------------------------------------
def fig_uart():
    p = svg(1280, 520)
    p.append(T(16, 24, "UART 8N1, 115200 Baud, Byte 0x53, LSB first. Ideales Modell.", 18))
    p.append(T(16, 46, "Tbit = 1/115200 = 8,681 us. Tframe = 10 Tbit = 86,806 us. Even Parity von 0x53 ist 0.", 15, MUTED, "400"))
    data = [1, 1, 0, 0, 1, 0, 1, 0]
    # idle, start, 8 data, stop, idle
    levels = [1, 1] + [0, 0] + [b for b in data for _ in (0, 1)] + [1, 1, 1]
    # use 0.5 bit cells so labels sit in the middle: each bit is two half-steps of bw
    bw = 46
    x0 = 70
    y_lo, y_hi = 150, 78
    p.append(poly(wave(levels, x0, y_lo, y_hi, bw), DATA, 2.8))
    # start edge after two idle half-bits? levels: 2 idle halves = 1 idle bit, then 2 start halves
    # Let's recount: [1,1] idle one bit, [0,0] start, then 8*2 data, [1,1] stop, [1] trailing idle
    names = ["Idle", "Start"] + [f"d{i}" for i in range(8)] + ["Stop"]
    for i, name in enumerate(names):
        x = x0 + (i + 0.5) * 2 * bw
        p.append(T(x, 176, name, 13, INK, "400", "middle"))
    # start edge x
    x_edge = x0 + 2 * bw  # after one idle bit (two halves)
    p.append(T(16, 196, "Abtastung Daten 1,5 .. 8,5 Tbit nach der Startflanke, Stop bei 9,5. Punkte = Sample.", 14, SAMP))
    for k in range(8):
        xs = x_edge + (1.5 + k) * 2 * bw
        ys = y_hi if data[k] else y_lo
        p.append(circ(xs, ys, 5, SAMP))
    xs = x_edge + 9.5 * 2 * bw
    p.append(circ(xs, y_hi, 5, SAMP))
    p.append(T(x_edge, 214, "Startflanke", 13, ERR))
    p.append(line(x_edge, 70, x_edge, 160, ERR, 1, "4 3"))

    # oversampling inset
    p.append(T(16, 250, "Ein Datenbit, 16-fach, Beispiel mit drei Samples um die Mitte. Controller werten unterschiedlich viele.", 15))
    ix0, ibw = 40, 28
    bit_levels = []
    # show a high bit divided in 16
    p.append(poly(wave([1] * 16, ix0, 340, 270, ibw), DATA, 2.4))
    for n in range(16):
        p.append(line(ix0 + n * ibw, 334, ix0 + n * ibw, 346, MUTED, 1))
        if n in (7, 8, 9):
            p.append(circ(ix0 + (n + 0.5) * ibw, 270, 4.5, SAMP))
        else:
            p.append(circ(ix0 + (n + 0.5) * ibw, 270, 2.2, MUTED))
    p.append(T(ix0 + 8 * ibw, 368, "Mehrheit der markierten Samples, hier HIGH", 14, SAMP, "400", "middle"))

    # drift
    p.append(T(560, 250, "Zwei Bitzeitraster laufen ueber den Frame auseinander.", 15))
    p.append(T(560, 272, "Naechster gueltiger Start synchronisiert neu. Kein festes Toleranzlimit.", 14, MUTED, "400"))
    for row, color, label in ((0, DATA, "Soll"), (1, ERR, "etwas kuerzer")):
        y = 300 + row * 28
        p.append(T(560, y + 4, label, 13, color, "400"))
        x = 700
        step = 36 if row == 0 else 33
        for k in range(9):
            p.append(circ(x + k * step, y, 4, color))
    p.append(T(16, 410, "0x53 hat vier Einsen. Even-Parity-Bit = 0. Ein einzelner Kipper faellt auf, zwei Kipper koennen bleiben.", 15, ERR))
    p.append(T(16, 438, "Stop falsch = Framing-Fehler. Parity falsch = eigener Status. Beides ist noch kein Paketprotokoll.", 15))
    p.append(T(16, 468, "Optional 8E1: 11 Symbole, Datenanteil 8/11 etwa 72,7 Prozent. Leitungsrate bleibt 115200 Baud.", 14, MUTED, "400"))
    p.append(T(16, 500, "Direkt 0/3,3 V nur bei gemeinsamem Bezug. Ein UART-Pin vertraegt deshalb noch keine RS-232-Pegel.", 14, MUTED, "400"))
    save("uart-frame.svg", p)


# ---------------------------------------------------------------------------
# 4 FIFO
# ---------------------------------------------------------------------------
def fig_fifo():
    p = svg(1200, 400)
    p.append(T(16, 24, "Getrennte TX- und RX-Pfade. FIFO und Schieberegister sind zwei Stufen.", 18))
    rows = [
        (70, "TX", ["CPU / MMIO", "TX-FIFO", "TX-Schiebereg.", "Leitung"]),
        (180, "RX", ["Leitung", "Sampling / Frame", "RX-Schiebereg.", "RX-FIFO", "CPU / MMIO"]),
    ]
    for y, name, boxes in rows:
        p.append(T(16, y + 28, name, 16, CLK))
        x = 70
        for i, b in enumerate(boxes):
            box(p, x, y, 150, 48, b, "", DATA if "FIFO" in b else INK)
            if i < len(boxes) - 1:
                p.append(arrow(x + 150, y + 24, x + 168))
            x += 176
    p.append(T(16, 268, "115200 Baud, 8N1: hoechstens 11520 Byte/s, Datenanteil 80 Prozent.", 16, DATA))
    p.append(T(16, 296, "RX-FIFO 16 Plaetze, Watermark 8. Acht Bytes etwa 694 us Spielraum, keine IRQ-Latenz.", 16, SAMP))
    p.append(T(16, 324, "Kommen weniger als acht Bytes, braucht es Timeout oder Idle. Overflow ist ein eigener Fehler.", 16, ERR))
    p.append(T(16, 352, "Platz im TX-Puffer heisst nicht: letztes Stop-Bit ist schon auf der Leitung.", 16))
    p.append(T(16, 384, "Fuer RS-485-Richtung zaehlt das gesendete Stop-Bit, nicht nur das leere FIFO.", 15, MUTED, "400"))
    save("uart-fifo.svg", p)


# ---------------------------------------------------------------------------
# 5 SPI ring
# ---------------------------------------------------------------------------
def spi_segments(cpol, cpha, bits):
    """Halbperioden-Segmente (sck, mosi) plus Sample-Indizes in Halbperioden ab t=0."""
    segs = []
    samples = []
    changes = []
    # 2 Halbperioden Vorlauf
    pre = bits[0] if cpha == 0 else None
    segs.append((2, cpol, pre))
    t = 2
    clk = cpol
    for i, b in enumerate(bits):
        clk = 1 - clk  # leading
        prev = segs[-1][2]
        if cpha == 0:
            segs.append((1, clk, b))
            samples.append(t)
        else:
            segs.append((1, clk, b))
            if prev != b:
                changes.append(t)
        t += 1
        clk = 1 - clk  # trailing
        if cpha == 0:
            nxt = bits[i + 1] if i + 1 < len(bits) else b
            segs.append((1, clk, nxt))
            if b != nxt:
                changes.append(t)
        else:
            segs.append((1, clk, b))
            samples.append(t)
        t += 1
    segs.append((2, cpol, segs[-1][2]))
    return segs, samples, changes


def expand(segs):
    sck, mos = [], []
    for n, c, m in segs:
        for _ in range(n):
            sck.append(c)
            mos.append(0 if m is None else m)
    return sck, mos


def fig_spi():
    p = svg(1280, 520)
    p.append(T(16, 24, "SPI Mode 0, MSB first. Controller 0x96, Target 0x3C. Aktives CS ist LOW.", 18))
    p.append(T(16, 46, "Sample an der steigenden Flanke, Datenwechsel an der fallenden. Gemeinsamer Bezug gehoert dazu.", 14, MUTED, "400"))
    bits_o = [1, 0, 0, 1, 0, 1, 1, 0]  # 0x96
    bits_i = [0, 0, 1, 1, 1, 1, 0, 0]  # 0x3C
    segs, samples, changes = spi_segments(0, 0, bits_o)
    sck, mosi = expand(segs)
    _, miso = expand(spi_segments(0, 0, bits_i)[0])
    # CS: high 1 half, low during, high at end. segs length in halves:
    n = len(sck)
    bw = 28
    x0 = 90
    traces = [
        (70, "CS", [1] + [0] * (n - 2) + [1], ERR),
        (150, "SCK", sck, CLK),
        (230, "MOSI", mosi, DATA),
        (310, "MISO", miso, OK),
    ]
    # CS length must match. [1] + lows + [1] may differ by 1. Force length n.
    cs = [1, 1] + [0] * (n - 4) + [1, 1]
    traces[0] = (70, "CS", cs, ERR)
    for y, name, levels, col in traces:
        p.append(T(16, y + 18, name, 15, col))
        p.append(poly(wave(levels, x0, y + 28, y, bw), col, 2.4))
    # sample numbers 1..8 on SCK rising: samples are half-period indices
    for i, t in enumerate(samples):
        x = x0 + t * bw
        p.append(circ(x, 150, 4.5, SAMP))
        p.append(T(x, 138, str(i + 1), 12, SAMP, "700", "middle"))
    p.append(T(16, 370, "Gefuellter Punkt = Sample. Datenwechsel liegt auf der anderen Flanke.", 14, SAMP))
    p.append(T(16, 398, "Register, Linksverschieben und Einschieben: Start 0x96 / 0x3C", 16))
    p.append(T(16, 426, "nach 4 Takten 0x63 / 0xC9, nach 8 Takten 0x3C / 0x96.", 16, DATA))
    p.append(T(16, 456, "Lesen braucht oft ein Dummy-Byte. Volle FIFO beweist kein fertiges CS-Hold.", 15, MUTED, "400"))
    p.append(T(16, 484, "Full-Duplex gilt fuer dieses 4-Signal-Modell. 3-Draht, Dual und Quad sind Erweiterungen.", 15, MUTED, "400"))
    p.append(T(16, 508, "CS-Setup vor der ersten Sample-Flanke, CS-Hold nach dem letzten Bit.", 14, ERR))
    save("spi-ring.svg", p)


def fig_modes():
    p = svg(1280, 560)
    p.append(T(16, 22, "Vier Modi, gleiche MOSI-Folge 0x96. Leading geht vom Idle weg, Trailing kehrt zurueck.", 17))
    bits = [1, 0, 0, 1, 0, 1, 1, 0]
    modes = [(0, 0, "Mode 0  Idle LOW, Sample steigend"),
             (0, 1, "Mode 1  Idle LOW, Sample fallend"),
             (1, 0, "Mode 2  Idle HIGH, Sample fallend"),
             (1, 1, "Mode 3  Idle HIGH, Sample steigend")]
    y = 40
    bw = 18
    for cpol, cpha, title in modes:
        p.append(T(16, y + 14, title, 14))
        segs, samples, changes = spi_segments(cpol, cpha, bits)
        sck, mos = expand(segs)
        x0 = 360
        p.append(poly(wave(sck, x0, y + 36, y + 8, bw), CLK, 2.2))
        p.append(poly(wave(mos, x0, y + 78, y + 50, bw), DATA, 2.2))
        p.append(T(300, y + 28, "SCK", 13, CLK, "400"))
        p.append(T(300, y + 70, "MOSI", 13, DATA, "400"))
        for t in samples:
            p.append(circ(x0 + t * bw, y + 8 if sck[min(t, len(sck) - 1)] else y + 36, 3.5, SAMP))
        for t in changes:
            yy = y + 50 if mos[min(t, len(mos) - 1)] else y + 78
            p.append(rect(x0 + t * bw - 3, yy - 3, 6, 6, ERR, "#fff", 1.4))
        y += 100
    p.append(T(16, 460, "Punkt = Sample. Quadrat = Datenwechsel. Bei CPHA = 0 steht Bit 0 schon vor der ersten Sample-Flanke.", 15))
    p.append(T(16, 486, "Bei CPHA = 1 bereitet die erste Flanke das Bit fuer die folgende Sample-Flanke.", 15))
    p.append(T(16, 514, "Gleicher SCK verhindert Bauddrift, nicht beliebig hohe Frequenz. Setup, Hold, Clock-to-Output und Leitung begrenzen das Auge.", 14, MUTED, "400"))
    p.append(T(16, 542, "Maximale SCK-Frequenz aus beiden Datenblaettern und dem Layout, nicht aus dem Modus allein.", 14, MUTED, "400"))
    save("spi-modes.svg", p)


# ---------------------------------------------------------------------------
# 7 Topologie
# ---------------------------------------------------------------------------
def fig_topo():
    p = svg(1200, 460)
    p.append(T(16, 24, "Stern: SCK, MOSI, MISO gemeinsam, drei CS, zusaetzlich GND. Nur ein MISO-Treiber aktiv.", 16))
    box(p, 20, 48, 140, 50, "Controller", "CS0 CS1 CS2", CLK)
    for i, name in enumerate(("T0 selektiert", "T1 hochohmig", "T2 hochohmig")):
        y = 120 + i * 70
        col = OK if i == 0 else MUTED
        box(p, 280, y, 200, 52, name, "MISO" if i == 0 else "MISO Hi-Z", col)
        p.append(line(160, 73, 280, y + 26, INK, 1.4))
    p.append(T(520, 80, "Gemeinsame Netze: SCK, MOSI, MISO", 15, DATA))
    p.append(T(520, 108, "Getrennt: CS0, CS1, CS2", 15, CLK))
    p.append(T(520, 136, "GND zwischen allen Bausteinen", 15, GND))
    p.append(rect(520, 160, 640, 70, ERR, "#fff"))
    p.append(T(532, 188, "Fehler: zwei Push-Pull-MISO-Treiber,", 15, ERR))
    p.append(T(532, 212, "unterschiedliche Pegel, ein Netz.", 15, ERR))
    p.append(T(16, 350, "Daisy-Chain nur wenn das Geraet sie vorsieht. Start 00/00/00, Controller sendet 0x33, 0x22, 0x11.", 15))
    p.append(T(16, 378, "Nach 8 Takten 33/00/00, nach 16: 22/33/00, nach 24: 11/22/33. Latch ist ein extra Ereignis.", 16, DATA))
    p.append(T(16, 410, "Controller-SDO gehoert an Target-SDI. Gleicher Name heisst nicht gleiche Leitung.", 15, MUTED, "400"))
    p.append(T(16, 440, "Ein Sensor mit Kommando/Antwort ist keine Daisy-Chain und hat im Grundmodell kein ACK.", 15, MUTED, "400"))
    save("spi-topo.svg", p)


# ---------------------------------------------------------------------------
# 8 Open-Drain
# ---------------------------------------------------------------------------
def fig_od():
    p = svg(1200, 480)
    p.append(T(16, 24, "Open-Drain-Lehrrechnung. Vio = 3,3 V, Cb = 100 pF, IOL = 3 mA bei VOL,max = 0,4 V.", 16))
    p.append(T(16, 46, "Annahme, keine Messung. tr = 0,8473 * Rp * Cb fuer 30 bis 70 Prozent.", 14, MUTED, "400"))
    # circuit
    p.append(T(40, 78, "Vio", 14, CLK))
    p.append(line(70, 86, 70, 120, CLK, 2))
    p.append(rect(55, 120, 30, 46, CLK, "#fff"))
    p.append(T(60, 148, "Rp", 14, CLK))
    p.append(line(70, 166, 70, 200, INK, 2))
    p.append(line(70, 200, 260, 200, DATA, 2.4))
    p.append(T(140, 192, "SDA oder SCL", 13, DATA, "400"))
    p.append(line(260, 200, 260, 250, MUTED, 2))
    p.append(T(268, 230, "Cb", 14, MUTED, "400"))
    p.append(line(240, 250, 280, 250, GND, 2))
    # two switches
    p.append(line(120, 200, 120, 250, OK, 2))
    p.append(line(180, 200, 180, 250, ERR, 2))
    p.append(T(100, 270, "A", 14, OK))
    p.append(T(168, 270, "B", 14, ERR))
    p.append(line(90, 290, 210, 290, GND, 2))
    p.append(T(230, 288, "GND", 14, GND, "400"))
    p.append(T(340, 100, "beide los: HIGH", 15, OK))
    p.append(T(340, 128, "nur A oder nur B: LOW", 15, DATA))
    p.append(T(340, 156, "beide ziehen: LOW", 15, DATA))
    p.append(T(340, 184, "HIGH heisst freigegeben, nicht aktiv getrieben.", 14, MUTED, "400"))
    p.append(T(340, 214, "Push-Pull HIGH gegen LOW ist ein Konflikt.", 15, ERR))
    p.append(T(340, 242, "Open-Drain begrenzt diesen einen Fall, nicht jede Fehlverdrahtung.", 14, ERR))
    # exponential polyline
    p.append(T(16, 330, "Anstieg nach dem Loslassen, RC-Modell ab 0 V.", 15))
    pts = []
    x0, y0 = 40, 450
    for i in range(81):
        t = i / 80.0
        v = 1 - pow(2.718281828, -t * 3.2)
        pts.append((x0 + i * 6, y0 - v * 90))
    p.append(poly(pts, DATA, 2.4))
    # 30% and 70% markers: v=0.3 and 0.7 of the drawn curve
    # curve uses v = 1-exp(-t*3.2), t=i/80
    import math
    for frac, name in ((0.3, "30%"), (0.7, "70%")):
        # 1-exp(-3.2 i/80) = frac => i = -80/3.2*ln(1-frac)
        i = -80 / 3.2 * math.log(1 - frac)
        x = x0 + i * 6
        y = y0 - frac * 90
        p.append(line(x, y, x, y0, MUTED, 1, "3 3"))
        p.append(T(x + 4, y - 4, name, 13, SAMP))
    p.append(T(560, 360, "4,7 kOhm: etwa 398 ns", 16, CLK))
    p.append(T(560, 388, "2,2 kOhm: etwa 186 ns", 16, OK))
    p.append(T(560, 416, "Fast-Mode 300 ns: Rp,max etwa 3,54 kOhm", 16, SAMP))
    p.append(T(560, 444, "Rp,min etwa 967 Ohm. 2,2 kOhm liegt dazwischen.", 16, ERR))
    p.append(T(16, 472, "Zwei 4,7-kOhm-Modul-Pull-ups parallel: 2,35 kOhm. Standard-Mode-Grenze 1000 ns. Datenblattgrenzen extra pruefen.", 14, MUTED, "400"))
    save("open-drain.svg", p)


# ---------------------------------------------------------------------------
# 9 I2C write waveform
# ---------------------------------------------------------------------------
def i2c_write_levels():
    """Viertelbit-Pegel. SDA wechselt in der Mitte von SCL LOW, ausser START/STOP."""
    bytes_ = [
        [1, 1, 0, 1, 0, 0, 0, 0, 0],  # 0xD0 + ACK
        [0, 1, 1, 0, 1, 0, 1, 1, 0],  # 0x6B + ACK
        [0, 0, 0, 0, 0, 0, 0, 0, 0],  # 0x00 + ACK
    ]
    scl, sda = [], []

    def ext(sc, sd, n=1):
        scl.extend([sc] * n)
        sda.extend([sd] * n)

    ext(1, 1, 4)  # Idle
    ext(1, 1, 2)  # START, SCL bleibt HIGH
    ext(1, 0, 2)  # SDA faellt bei SCL HIGH
    prev = 0
    for bits in bytes_:
        for bit in bits:
            ext(0, prev, 2)  # SCL LOW, SDA noch alt
            ext(0, bit, 2)  # SDA wechselt bei SCL LOW
            ext(1, bit, 4)  # SCL HIGH, SDA stabil
            prev = bit
    ext(0, 0, 4)  # vor STOP: SCL LOW, SDA LOW
    ext(1, 0, 2)  # SCL HIGH
    ext(1, 1, 2)  # SDA steigt = STOP
    return scl, sda


def fig_i2c():
    p = svg(1280, 460)
    p.append(T(16, 22, "I2C-Write, ein Controller. 7-Bit-Adresse 0x68, Write-Byte 0xD0, Register 0x6B, Daten 0x00.", 16))
    p.append(T(16, 44, "SDA wechselt bei Daten nur waehrend SCL LOW. Fallende SDA bei SCL HIGH = START, steigende = STOP.", 14, MUTED, "400"))
    scl, sda = i2c_write_levels()
    bw = 5
    x0 = 36
    p.append(T(16, 100, "SCL", 15, CLK))
    p.append(T(16, 170, "SDA", 15, DATA))
    p.append(poly(wave(scl, x0, 110, 70, bw), CLK, 2.2))
    p.append(poly(wave(sda, x0, 190, 150, bw), DATA, 2.2))
    # label phases. START occupies halves index 2..3, then 9 bits * 2, three times, then stop
    # index of first data half after start: 4
    names = ["S", "0xD0 + ACK", "0x6B + ACK", "0x00 + ACK", "P"]
    # widths in half steps: S=2 (plus we won't include idle), each byte 18, P=3
    spans = [4, 36, 36, 36, 8]
    cursor = 4  # Idle ueberspringen
    for name, n in zip(names, spans):
        x = x0 + (cursor + n / 2) * bw
        p.append(T(x, 220, name, 14, INK, "600", "middle"))
        cursor += n
    p.append(T(16, 258, "Neunte Clock: Sender gibt SDA frei, Target zieht fuer ACK auf LOW.", 16, OK))
    p.append(T(16, 286, "Address-NACK: niemand zieht. Data-NACK: unerwartete Ablehnung.", 16, ERR))
    p.append(T(16, 314, "Controller-NACK nach dem letzten gelesenen Byte ist der normale Abschluss, kein fehlendes Geraet.", 16, SAMP))
    p.append(T(16, 348, "0x68 << 1 | 0 = 0xD0, 0x68 << 1 | 1 = 0xD1. Eine API mit 7-Bit-Adresse schiebt intern. Nicht doppelt schieben.", 15))
    p.append(T(16, 378, "Zwei Targets mit derselben Adresse trennt das Basisprotokoll nicht. AD0, Multiplexer oder getrennte Busse pruefen.", 15))
    p.append(T(16, 408, "128 Bitmuster sind nicht 128 freie Geraete. Reservierte Adressen und optionale 10-Bit-Adressierung bleiben.", 15, MUTED, "400"))
    p.append(T(16, 440, "Ein ACK bestaetigt den Empfang des Bytes, nicht den physikalischen Messwert.", 15, MUTED, "400"))
    save("i2c-byte.svg", p)


def fig_burst():
    p = svg(1200, 460)
    p.append(T(16, 24, "Burst-Read 0x3B bis 0x40. Kein STOP zwischen Zeiger und Read. Repeated Start haelt die Transaktion.", 16))
    phases = [
        ("S", "Start"),
        ("D0", "Write ACK"),
        ("3B", "Reg ACK"),
        ("Sr", "kein STOP"),
        ("D1", "Read ACK"),
        ("10", "ACK"),
        ("00", "ACK"),
        ("E0", "ACK"),
        ("00", "ACK"),
        ("40", "ACK"),
        ("00", "NACK"),
        ("P", "Stop"),
    ]
    x = 16
    for i, (a, b) in enumerate(phases):
        col = ERR if a == "00" and b == "NACK" else (SAMP if a == "Sr" else INK)
        box(p, x, 46, 90, 58, a, b, col)
        if i < len(phases) - 1:
            p.append(arrow(x + 90, 74, x + 104))
        x += 98
    p.append(T(16, 140, "Controller bestaetigt Byte 1 bis 5 mit ACK und beendet Byte 6 mit NACK.", 16, ERR))
    p.append(T(16, 176, "Bytes: 10 00 | E0 00 | 40 00", 18, DATA))
    p.append(T(16, 208, "X = 0x1000 = 4096, Y = 0xE000 = -8192, Z = 0x4000 = 16384", 16))
    p.append(T(16, 240, "+/-2 g und 16384 LSB/g: +0,25 g, -0,5 g, +1 g. Rohwert, Einheit und Bereich getrennt halten.", 16, OK))
    p.append(T(16, 276, "Tests: 0x0000 -> 0, 0x7FFF -> 32767, 0x8000 -> -32768, 0xFFFF -> -1", 16, SAMP))
    p.append(T(16, 312, "Unsigned zusammensetzen, dann als int16_t lesen. Kein Cast eines Bytepuffers auf int16_t*.", 15))
    p.append(T(16, 348, "9 Bytes * 9 SCL = 81 Pulse. 810 us bei 100 kHz, 202,5 us bei 400 kHz, ohne Stretching.", 16, CLK))
    p.append(T(16, 380, "Nutzdaten 48/81, etwa 59 Prozent. Ein einzelnes Byte ab 0x3B ist nur X-High.", 16, ERR))
    p.append(T(16, 420, "Auto-Increment und ein gemeinsamer Snapshot sind Eigenschaften des Sensors, nicht von I2C allgemein.", 14, MUTED, "400"))
    p.append(T(16, 446, "Getrennte Transaktionen koennen drei Achsen aus verschiedenen Abtastungen mischen.", 14, MUTED, "400"))
    save("i2c-burst.svg", p)


def fig_stretch():
    p = svg(1200, 460)
    p.append(T(16, 24, "Stretching: der Controller gibt SCL frei, das Target haelt LOW, die Leitung bleibt LOW.", 16))
    # planned vs wire
    p.append(T(16, 70, "geplant", 14, CLK))
    p.append(T(16, 120, "Target", 14, ERR))
    p.append(T(16, 170, "Leitung", 14, DATA))
    plan = [0, 0, 1, 1, 1, 1, 1, 1, 0, 0]
    hold = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1]
    wire = [0, 0, 0, 0, 0, 0, 1, 1, 0, 0]
    bw = 36
    x0 = 120
    p.append(poly(wave(plan, x0, 80, 48, bw), CLK, 2.4))
    p.append(poly(wave(hold, x0, 130, 98, bw), ERR, 2.4))
    p.append(poly(wave(wire, x0, 180, 148, bw), DATA, 2.6))
    p.append(T(16, 220, "Abtastung erst in der wirklichen HIGH-Phase, nicht beim Softwarebefehl HIGH.", 15, SAMP))
    p.append(T(16, 248, "Ob Stretching existiert und wie lange gewartet werden darf, steht im Controller, im Target und im Modell.", 14, MUTED, "400"))
    p.append(T(16, 284, "Arbitration, beide Write. A: 0x50 -> 0xA0. B: 0x68 -> 0xD0.", 16))
    p.append(T(16, 312, "MSB beide 1. Danach sendet A eine 0, B eine 1. Die Leitung wird 0, B verliert und treibt nicht weiter.", 15, ERR))
    p.append(T(16, 348, "A setzt 1 0 1 0 0 0 0 fort. B darf den Gewinn von A nicht mit einem STOP abbrechen.", 16, DATA))
    p.append(T(16, 384, "Zustaende: frei, START, Adresse, Daten, Ende. Ausgaenge: NACK, Timeout, Arbitration Lost, Bus Error.", 15))
    p.append(T(16, 416, "0x00 und 0xFF sind gueltige Bytes. Neun Clocks loesen nur festgehaltenes SDA bei steuerbarem SCL.", 14, MUTED, "400"))
    p.append(T(16, 444, "Ein Watchdog-Reset der CPU setzt einen extern versorgten Sensor nicht automatisch zurueck.", 14, MUTED, "400"))
    save("stretch.svg", p)


def fig_diff():
    p = svg(1200, 480)
    p.append(T(16, 24, "Single-Ended gegen Bezug, differentiell als Differenz. Common Mode bleibt begrenzt.", 17))
    box(p, 16, 46, 250, 70, "Single-Ended", "Pegel gegen GND", DATA)
    box(p, 290, 46, 280, 70, "Differentiell", "Vdiff = VA - VB", OK)
    p.append(T(600, 74, "Vcm = (VA + VB) / 2", 16, SAMP))
    p.append(T(16, 150, "Beispiel: VA = 2,5 V, VB = 0,5 V -> Vdiff = 2,0 V, Vcm = 1,5 V", 16))
    p.append(T(16, 178, "Dieselbe Stoerung +0,8 V: Vdiff bleibt 2,0 V, Vcm wird 2,3 V", 16, DATA))
    p.append(T(16, 210, "Liegt 2,3 V noch im erlaubten Bereich des gewaehlten Transceivers? Das Datenblatt entscheidet.", 15, ERR))
    p.append(rect(16, 230, 560, 90, INK))
    p.append(T(28, 254, "RS-485, Halbduplex", 15))
    p.append(T(28, 278, "UART -> Transceiver -> A/B, Stubs kurz", 14, MUTED, "400"))
    p.append(T(28, 302, "Terminierung an beiden physikalischen Enden, Driver Enable steuert die Richtung", 14, MUTED, "400"))
    p.append(rect(600, 230, 560, 90, INK))
    p.append(T(612, 254, "CAN separat", 15))
    p.append(T(612, 278, "CAN-Controller plus CAN-Transceiver", 14, MUTED, "400"))
    p.append(T(612, 302, "Dominant/rezessiv. Rezessiv ist nicht zwingend invertiert.", 14, MUTED, "400"))
    p.append(T(16, 360, "Twisted Pair naehert gleiche Einkopplung an. Unsymmetrie und reale Empfaenger bleiben.", 15))
    p.append(T(16, 390, "Schichten: UART-Frame, dann RS-485-Transceiver, dann Leitung. Modbus liegt darueber.", 15, CLK))
    p.append(T(16, 420, "RS-485 liefert keine CAN-Arbitration. Masse, Schutz und Isolation bleiben Systemfragen.", 15, ERR))
    p.append(T(16, 454, "Mehrere hundert Meter sind keine beliebige Bitrate. Reichweite und Geschwindigkeit zusammen nennen.", 15, MUTED, "400"))
    save("diff.svg", p)


if __name__ == "__main__":
    for fn in (
        fig_path,
        fig_shift,
        fig_uart,
        fig_fifo,
        fig_spi,
        fig_modes,
        fig_topo,
        fig_od,
        fig_i2c,
        fig_burst,
        fig_stretch,
        fig_diff,
    ):
        fn()
