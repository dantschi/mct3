#!/usr/bin/env python3
"""Schematische Vektorfiguren für VL01. Keine Messdaten, keine Die-Fotos."""
from pathlib import Path

OUT = Path(__file__).resolve().parent
DATA = "#1565C0"
CTRL = "#E65100"
STATE = "#6A1B9A"
INK = "#1D1D1F"
MUTED = "#5F6368"
HAIR = "#E5E5EA"
VDD = "#B71C1C"
PANEL = "#FAFAFB"

def svg_open(w, h):
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">',
        f'<rect width="{w}" height="{h}" fill="#FFFFFF"/>',
        '<style>text{font-family:Arial,Helvetica,sans-serif;fill:#1D1D1F}</style>',
    ]

def save(name, parts):
    p = OUT / name
    p.write_text("\n".join(parts) + "\n</svg>\n", encoding="utf-8")
    print(name)

def txt(x, y, s, size=22, fill=INK, anchor="start", weight="600"):
    return (
        f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" '
        f'fill="{fill}" text-anchor="{anchor}">{s}</text>'
    )

def legend(x, y):
    return "\n".join([
        f'<rect x="{x}" y="{y}" width="16" height="8" fill="{DATA}"/>',
        txt(x + 22, y + 9, "Daten", 16, DATA, weight="500"),
        f'<rect x="{x+90}" y="{y}" width="16" height="8" fill="{CTRL}"/>',
        txt(x + 112, y + 9, "Steuerung", 16, CTRL, weight="500"),
        f'<rect x="{x+230}" y="{y}" width="16" height="8" fill="{STATE}"/>',
        txt(x + 252, y + 9, "Zustand/Ladung", 16, STATE, weight="500"),
        txt(x + 430, y + 9, "schematisch, nicht maßstabsgetreu", 16, MUTED, weight="400"),
    ])

def nmos(x, y, gate="left"):
    """NMOS, Kanal vertikal, Drain oben (y), Source unten (y+44)."""
    g = x - 14 if gate == "left" else x + 14
    gx1, gx2 = (g, x - 4) if gate == "left" else (x + 4, g)
    return "\n".join([
        f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y+10}" stroke="{DATA}" stroke-width="2.5"/>',
        f'<line x1="{x}" y1="{y+34}" x2="{x}" y2="{y+44}" stroke="{DATA}" stroke-width="2.5"/>',
        f'<line x1="{x-8}" y1="{y+14}" x2="{x+8}" y2="{y+14}" stroke="{INK}" stroke-width="2"/>',
        f'<line x1="{x-8}" y1="{y+22}" x2="{x+8}" y2="{y+22}" stroke="{INK}" stroke-width="2"/>',
        f'<line x1="{x-8}" y1="{y+30}" x2="{x+8}" y2="{y+30}" stroke="{INK}" stroke-width="2"/>',
        f'<line x1="{gx1}" y1="{y+12}" x2="{gx1}" y2="{y+32}" stroke="{CTRL}" stroke-width="2.5"/>',
        f'<line x1="{gx1}" y1="{y+22}" x2="{gx2}" y2="{y+22}" stroke="{CTRL}" stroke-width="2"/>',
        # Pfeil Source (unten) nach innen = NMOS
        f'<polygon points="{x-5},{y+38} {x+5},{y+38} {x},{y+30}" fill="{INK}"/>',
    ])

def pmos(x, y, gate="left"):
    g = x - 14 if gate == "left" else x + 14
    gx1 = g
    return "\n".join([
        f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y+10}" stroke="{DATA}" stroke-width="2.5"/>',
        f'<line x1="{x}" y1="{y+34}" x2="{x}" y2="{y+44}" stroke="{DATA}" stroke-width="2.5"/>',
        f'<line x1="{x-8}" y1="{y+14}" x2="{x+8}" y2="{y+14}" stroke="{INK}" stroke-width="2"/>',
        f'<line x1="{x-8}" y1="{y+22}" x2="{x+8}" y2="{y+22}" stroke="{INK}" stroke-width="2"/>',
        f'<line x1="{x-8}" y1="{y+30}" x2="{x+8}" y2="{y+30}" stroke="{INK}" stroke-width="2"/>',
        f'<line x1="{gx1}" y1="{y+12}" x2="{gx1}" y2="{y+32}" stroke="{CTRL}" stroke-width="2.5"/>',
        f'<circle cx="{x}" cy="{y+8}" r="3.2" fill="#FFFFFF" stroke="{INK}" stroke-width="1.6"/>',
    ])

def cap(x, y):
    return "\n".join([
        f'<line x1="{x}" y1="{y-16}" x2="{x}" y2="{y-4}" stroke="{DATA}" stroke-width="2.5"/>',
        f'<line x1="{x-14}" y1="{y}" x2="{x+14}" y2="{y}" stroke="{STATE}" stroke-width="3"/>',
        f'<line x1="{x-14}" y1="{y+8}" x2="{x+14}" y2="{y+8}" stroke="{INK}" stroke-width="3"/>',
        f'<line x1="{x}" y1="{y+12}" x2="{x}" y2="{y+26}" stroke="{INK}" stroke-width="2.5"/>',
    ])

def panel(x, y, w, h, title):
    return "\n".join([
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{PANEL}" stroke="{HAIR}"/>',
        txt(x + 12, y + 26, title, 18, CTRL),
    ])

def dot(x, y, c=INK):
    return f'<circle cx="{x}" cy="{y}" r="3.2" fill="{c}"/>'

# --- 6T geometry used by overview / hold / read / write ---
def cell_6t(ox, oy, mode):
    """mode: hold | read | write. Q stored 0 in read; write 0->1."""
    # local coords
    # VDD y=oy+18, left inv x=ox+70, right x=ox+150
    L, R = ox + 78, ox + 168
    parts = []
    parts.append(f'<line x1="{ox+40}" y1="{oy+36}" x2="{ox+206}" y2="{oy+36}" stroke="{VDD}" stroke-width="2"/>')
    parts.append(txt(ox + 8, oy + 40, "VDD", 14, VDD))
    parts.append(pmos(L, oy + 36, "right"))
    parts.append(pmos(R, oy + 36, "left"))
    parts.append(nmos(L, oy + 90, "right"))
    parts.append(nmos(R, oy + 90, "left"))
    parts.append(f'<line x1="{ox+40}" y1="{oy+134}" x2="{ox+206}" y2="{oy+134}" stroke="{INK}" stroke-width="2"/>')
    parts.append(txt(ox + 8, oy + 138, "GND", 14))
    # storage nodes
    qy = oy + 86
    parts.append(f'<line x1="{L}" y1="{oy+80}" x2="{L}" y2="{qy}" stroke="{DATA}" stroke-width="2"/>')
    parts.append(f'<line x1="{R}" y1="{oy+80}" x2="{R}" y2="{qy}" stroke="{DATA}" stroke-width="2"/>')
    # cross couple: Q (left) to right gates, Qb to left gates
    parts.append(f'<path d="M {L} {qy} H {ox+118} V {oy+58} H {R-16}" fill="none" stroke="{STATE}" stroke-width="1.8"/>')
    parts.append(f'<path d="M {R} {qy} H {ox+128} V {oy+112} H {L+16}" fill="none" stroke="{STATE}" stroke-width="1.8"/>')
    parts.append(dot(L, qy, STATE))
    parts.append(dot(R, qy, STATE))
    parts.append(txt(L - 28, qy + 4, "Q", 16, STATE))
    parts.append(txt(R + 8, qy + 4, "Qb", 16, STATE))
    # access
    parts.append(nmos(ox + 36, oy + 150, "left"))
    parts.append(nmos(ox + 210, oy + 150, "right"))
    parts.append(f'<line x1="{L}" y1="{qy}" x2="{L}" y2="{oy+150}" stroke="{DATA}" stroke-width="2"/>')
    parts.append(f'<line x1="{ox+36}" y1="{oy+150}" x2="{L}" y2="{oy+150}" stroke="{DATA}" stroke-width="2"/>')
    parts.append(f'<line x1="{R}" y1="{qy}" x2="{R}" y2="{oy+150}" stroke="{DATA}" stroke-width="2"/>')
    parts.append(f'<line x1="{ox+210}" y1="{oy+150}" x2="{R}" y2="{oy+150}" stroke="{DATA}" stroke-width="2"/>')
    # BL
    parts.append(f'<line x1="{ox+16}" y1="{oy+194}" x2="{ox+36}" y2="{oy+194}" stroke="{DATA}" stroke-width="2.5"/>')
    parts.append(f'<line x1="{ox+210}" y1="{oy+194}" x2="{ox+230}" y2="{oy+194}" stroke="{DATA}" stroke-width="2.5"/>')
    parts.append(txt(ox + 4, oy + 214, "BL", 15, DATA))
    parts.append(txt(ox + 198, oy + 214, "BLb", 15, DATA))
    # WL through gates
    wl_y = oy + 172
    parts.append(f'<line x1="{ox+8}" y1="{wl_y}" x2="{ox+22}" y2="{wl_y}" stroke="{CTRL}" stroke-width="2.5"/>')
    parts.append(f'<line x1="{ox+224}" y1="{wl_y}" x2="{ox+236}" y2="{wl_y}" stroke="{CTRL}" stroke-width="2.5"/>')
    parts.append(txt(ox + 4, oy + 168, "WL", 15, CTRL))
    if mode == "hold":
        parts.append(txt(ox + 70, oy + 236, "WL = 0, Zugänge sperren", 15, CTRL))
        parts.append(txt(ox + 70, oy + 254, "Q = 1 bleibt im Ring", 15, STATE))
    elif mode == "read":
        parts.append(txt(ox + 48, oy + 236, "BL/BL vorgeladen, WL = 1", 15, CTRL))
        parts.append(txt(ox + 48, oy + 254, "kleine Differenz, Q bleibt", 15, STATE))
    else:
        parts.append(txt(ox + 40, oy + 236, "Treiber: BL=1, BL=0", 15, DATA))
        parts.append(txt(ox + 40, oy + 254, "Q kippt 0 nach 1", 15, STATE))
    return "\n".join(parts)

def fig_6t_states():
    w, h = 1180, 430
    p = svg_open(w, h)
    p.append(legend(16, 12))
    p.append(panel(12, 40, 370, 370, "Hold: WL = 0"))
    p.append(cell_6t(30, 70, "hold"))
    p.append(panel(398, 40, 370, 370, "Lesen: gleiche Zelle"))
    p.append(cell_6t(416, 70, "read"))
    p.append(panel(784, 40, 380, 370, "Schreiben: gleiche Zelle"))
    p.append(cell_6t(800, 70, "write"))
    save("sram-6t-states.svg", p)

def fig_sram_read():
    w, h = 1200, 340
    p = svg_open(w, h)
    p.append(legend(16, 10))
    titles = [
        "1  BL und BL vorladen",
        "2  WL an, kleine Differenz",
        "3  Sense Amplifier wertet aus",
    ]
    notes = [
        "beide Leitungen hoch, Zelle isoliert",
        "Q=0 zieht BL nur leicht herunter",
        "Differenz wird 0/1, Zelle bleibt",
    ]
    for i, (t, n) in enumerate(zip(titles, notes)):
        x = 16 + i * 392
        p.append(panel(x, 40, 376, 280, t))
        p.append(txt(x + 16, y := 90, "BL", 16, DATA))
        p.append(txt(x + 16, 118, "BL", 16, DATA))
        p.append(f'<line x1="{x+70}" y1="{78}" x2="{x+250}" y2="{78}" stroke="{DATA}" stroke-width="3"/>')
        p.append(f'<line x1="{x+86}" y1="{64}" x2="{x+110}" y2="{64}" stroke="{DATA}"/>')
        p.append(f'<line x1="{x+70}" y1="{108}" x2="{x+250}" y2="{108}" stroke="{DATA}" stroke-width="3"/>')
        if i == 0:
            p.append(txt(x + 150, 74, "VDD", 16, DATA, "middle"))
            p.append(txt(x + 150, 104, "VDD", 16, DATA, "middle"))
        elif i == 1:
            p.append(f'<path d="M {x+90} 78 Q {x+160} 92 {x+230} 86" fill="none" stroke="{STATE}" stroke-width="2.5"/>')
            p.append(txt(x + 150, 150, "delta V klein", 16, STATE, "middle"))
            p.append(txt(x + 20, 180, "WL = 1", 16, CTRL))
        else:
            p.append(f'<rect x="{x+250}" y="60" width="90" height="70" rx="6" fill="#FFF" stroke="{CTRL}" stroke-width="2"/>')
            p.append(txt(x + 258, 100, "SA", 18, CTRL))
            p.append(txt(x + 20, 180, "Ausgang: gespeichertes Bit", 16))
        p.append(txt(x + 16, 250, n, 16, MUTED, weight="400"))
    save("sram-read.svg", p)

def fig_sram_write():
    w, h = 1100, 320
    p = svg_open(w, h)
    p.append(legend(16, 10))
    steps = [
        ("1  Treiber setzen", "BL = 1, BL = 0", "Schreibtreiber staerker als Zell-Pull"),
        ("2  WL = 1", "Zugriff offen", "Q kippt von 0 auf 1"),
        ("3  WL = 0", "Zelle isoliert", "neuer Zustand bleibt im Ring"),
    ]
    for i, (a, b, c) in enumerate(steps):
        x = 16 + i * 360
        p.append(panel(x, 40, 344, 260, a))
        p.append(txt(x + 20, 100, b, 20, DATA))
        p.append(txt(x + 20, 140, c, 16))
        p.append(txt(x + 20, 190, "Beispiel Q: 0 → 1", 18, STATE))
        p.append(txt(x + 20, 230, "keine universelle Groessenregel", 14, MUTED, weight="400"))
    save("sram-write.svg", p)

def fig_dram_read():
    w, h = 1200, 360
    p = svg_open(w, h)
    p.append(legend(16, 8))
    labels = [
        "1  BL = VDD/2",
        "2  WL an, Charge Sharing",
        "3  ±ΔV verstärken",
        "4  Restore, WL noch an",
    ]
    for i, lab in enumerate(labels):
        x = 12 + i * 296
        p.append(panel(x, 36, 284, 300, lab))
        # 1T1C
        p.append(txt(x + 16, 80, "WL", 15, CTRL))
        p.append(nmos(x + 70, 90, "left"))
        p.append(f'<line x1="{x+70}" y1="{134}" x2="{x+70}" y2="{160}" stroke="{DATA}" stroke-width="2"/>')
        p.append(cap(x + 70, 176))
        p.append(txt(x + 90, 190, "Cs", 15, STATE))
        p.append(txt(x + 16, 230, "BL", 15, DATA))
        p.append(f'<line x1="{x+16}" y1="{100}" x2="{x+70}" y2="{100}" stroke="{DATA}" stroke-width="2"/>')
        if i == 0:
            p.append(txt(x + 16, 270, "vorladen, Zelle zu", 15))
        elif i == 1:
            p.append(txt(x + 16, 270, "Ladung teilt sich, nicht leer", 15))
        elif i == 2:
            p.append(txt(x + 150, 120, "SA", 16, CTRL))
            p.append(txt(x + 16, 270, "SA kippt auf vollen Pegel", 15))
        else:
            p.append(txt(x + 16, 270, "voller Pegel zurück in Cs", 15))
    save("dram-read-restore.svg", p)

def fig_1t1c():
    w, h = 720, 300
    p = svg_open(w, h)
    p.append(legend(12, 10))
    # NMOS: Drain y=78, Gate-Mitte y=100, Source y=122
    p.append(nmos(220, 78, "left"))
    p.append(f'<line x1="70" y1="78" x2="220" y2="78" stroke="{DATA}" stroke-width="2.5"/>')
    p.append(txt(24, 84, "BL", 18, DATA))
    p.append(f'<line x1="70" y1="100" x2="206" y2="100" stroke="{CTRL}" stroke-width="2.5"/>')
    p.append(txt(24, 106, "WL", 18, CTRL))
    p.append(f'<line x1="220" y1="122" x2="220" y2="150" stroke="{DATA}" stroke-width="2.5"/>')
    p.append(cap(220, 166))
    p.append(txt(250, 174, "Cs", 16, STATE))
    p.append(txt(250, 210, "Plate / GND-Modell", 16, MUTED, weight="400"))
    p.append(txt(24, 270, "WL am Gate, BL am Drain, Speicherknoten am Source.", 16))
    save("dram-1t1c.svg", p)

def fig_refresh():
    w, h = 860, 280
    p = svg_open(w, h)
    p.append(txt(20, 28, "Zellspannung einer gespeicherten 1  (schematisch)", 18))
    p.append(f'<line x1="60" y1="40" x2="60" y2="220" stroke="{INK}"/>')
    p.append(f'<line x1="60" y1="220" x2="820" y2="220" stroke="{INK}"/>')
    p.append(txt(20, 50, "V", 16))
    p.append(txt(780, 246, "t", 16))
    p.append(f'<polyline points="70,70 160,78 250,110 340,168 390,178 430,90 500,74 600,100 700,155 760,188" fill="none" stroke="{STATE}" stroke-width="3"/>')
    p.append(txt(300, 200, "Leck", 15, STATE))
    p.append(txt(430, 60, "Refresh", 15, CTRL))
    p.append(txt(20, 268, "64 ms nur als geräte- und temperaturabhängiges Beispiel-Fenster, keine feste Bit-Lebensdauer.", 15, MUTED, weight="400"))
    save("dram-refresh.svg", p)

def fig_ddr():
    w, h = 1000, 320
    p = svg_open(w, h)
    p.append(txt(16, 24, "Gleicher Schnittstellentakt — SDR vs. DDR (schematisch)", 18))
    # clock
    p.append(txt(16, 70, "CLK", 16, CTRL))
    d = "M 80 80"
    x = 80
    high = True
    for _ in range(8):
        y1, y2 = (50, 90) if high else (90, 50)
        d += f" V {y1} H {x+50} V {y2} H {x+100}"
        x += 100
        high = not high
    p.append(f'<path d="{d}" fill="none" stroke="{CTRL}" stroke-width="2.5"/>')
    p.append(txt(16, 150, "SDR", 16, DATA))
    p.append(txt(16, 210, "DDR", 16, DATA))
    for i, cx in enumerate(range(130, 830, 100)):
        p.append(f'<circle cx="{cx}" cy="140" r="6" fill="{DATA}"/>')
        p.append(f'<circle cx="{cx}" cy="200" r="6" fill="{DATA}"/>')
        p.append(f'<circle cx="{cx+50}" cy="200" r="6" fill="{STATE}"/>')
    p.append(txt(16, 260, "Punkte: gültige Datenübernahme. DDR nutzt beide Flanken.", 16))
    p.append(txt(16, 288, "Bandbreite etwa doppelt — die Zeilen-Latenz halbiert sich dadurch nicht.", 16, MUTED, weight="400"))
    save("sdram-ddr.svg", p)

def fig_memory_wall():
    w, h = 980, 360
    p = svg_open(w, h)
    p.append(txt(16, 24, "Relative Entwicklung (schematisch, keine Messreihe)", 18))
    p.append(f'<line x1="70" y1="40" x2="70" y2="250" stroke="{INK}"/>')
    p.append(f'<line x1="70" y1="250" x2="900" y2="250" stroke="{INK}"/>')
    p.append(txt(16, 40, "rel.", 14))
    p.append(txt(820, 272, "Generation", 14))
    pts_cpu = [(80, 230), (160, 220), (260, 190), (380, 145), (520, 100), (680, 68), (860, 48)]
    pts_mem = [(80, 230), (200, 224), (360, 210), (520, 198), (700, 184), (860, 172)]
    def poly(pts, color):
        d = "M " + " L ".join(f"{x} {y}" for x, y in pts)
        return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="3"/>'
    p.append(poly(pts_cpu, CTRL))
    p.append(poly(pts_mem, DATA))
    p.append(txt(620, 46, "CPU-Durchsatz", 16, CTRL))
    p.append(txt(560, 150, "Speicher-Durchsatz", 16, DATA))
    p.append(txt(16, 310, "Kenngröße: Durchsatz, nicht Latenz gemischt mit Bandbreite.", 16))
    p.append(txt(16, 338, "Beispiel ohne Überlappung: 4 GHz × 100 ns = 400 Takte Wartezeit.", 16, STATE))
    save("memory-wall.svg", p)

def fig_hierarchy():
    w, h = 1000, 420
    p = svg_open(w, h)
    levels = [
        (360, 40, 280, "Register", "klein, schnell"),
        (280, 100, 440, "L1/L2 SRAM", "Cache"),
        (180, 170, 640, "DRAM", "großer SoC"),
        (80, 240, 840, "Flash / Massenspeicher", "MCU: oft statt DRAM nur SRAM"),
    ]
    colors = ["#FDECEA", "#FFF3E0", "#E3F2FD", "#E8F5E9"]
    for (x, y, wi, name, sub), c in zip(levels, colors):
        p.append(f'<polygon points="{x},{y} {x+wi},{y} {x+wi-40},{y+52} {x+40},{y+52}" fill="{c}" stroke="{INK}"/>')
        p.append(txt(x + wi / 2, y + 24, name, 18, anchor="middle"))
        p.append(txt(x + wi / 2, y + 44, sub, 14, MUTED, "middle", "400"))
    p.append(txt(20, 330, "↑ Zugriffszeit, Kosten/Bit nach oben kleiner werdende Kapazität", 16))
    p.append(txt(20, 360, "MCU-Beispiel: Flash + SRAM. Großer SoC: Cache, DRAM, Massenspeicher.", 16))
    p.append(txt(20, 392, "Zeiten in der Vorlesung nur als Größenordnung, nicht austauschbare Ebenen.", 15, MUTED, weight="400"))
    save("hierarchy.svg", p)

def fig_von_harvard():
    w, h = 1100, 340
    p = svg_open(w, h)
    p.append(panel(10, 10, 520, 310, "Von-Neumann: ein physischer Pfad"))
    p.append(f'<rect x="40" y="80" width="120" height="60" rx="6" fill="#FFF" stroke="{INK}"/>')
    p.append(txt(70, 116, "CPU", 18))
    p.append(f'<rect x="300" y="80" width="180" height="70" rx="6" fill="#FFF" stroke="{DATA}" stroke-width="2"/>')
    p.append(txt(330, 122, "Code+Daten", 16, DATA))
    p.append(f'<line x1="160" y1="110" x2="300" y2="110" stroke="{DATA}" stroke-width="4"/>')
    p.append(txt(170, 100, "ein Bus", 14, CTRL))
    p.append(txt(30, 200, "Gemeinsamer Adressraum und", 16))
    p.append(txt(30, 224, "ein Port: Fetch und Load streiten.", 16))
    p.append(panel(550, 10, 530, 310, "Modified Harvard"))
    p.append(f'<rect x="580" y="70" width="100" height="50" fill="#FFF" stroke="{INK}"/>')
    p.append(txt(600, 100, "CPU", 16))
    p.append(f'<rect x="720" y="50" width="120" height="36" fill="#FFF" stroke="{CTRL}"/>')
    p.append(txt(740, 74, "L1-I", 15, CTRL))
    p.append(f'<rect x="720" y="110" width="120" height="36" fill="#FFF" stroke="{DATA}"/>')
    p.append(txt(740, 134, "L1-D", 15, DATA))
    p.append(f'<rect x="880" y="78" width="160" height="50" fill="#FFF" stroke="{INK}"/>')
    p.append(txt(900, 108, "gemeinsamer RAM", 14))
    p.append(f'<line x1="680" y1="80" x2="720" y2="68" stroke="{CTRL}" stroke-width="2"/>')
    p.append(f'<line x1="680" y1="110" x2="720" y2="128" stroke="{DATA}" stroke-width="2"/>')
    p.append(f'<line x1="840" y1="68" x2="880" y2="90" stroke="{INK}"/>')
    p.append(f'<line x1="840" y1="128" x2="880" y2="110" stroke="{INK}"/>')
    p.append(txt(570, 200, "Getrennte L1-Pfade, darunter", 16))
    p.append(txt(570, 224, "ein Speicher. Adressraum kann", 16))
    p.append(txt(570, 248, "trotzdem gemeinsam sein.", 16))
    save("von-harvard.svg", p)

def fig_soc():
    w, h = 1000, 340
    p = svg_open(w, h)
    p.append(txt(16, 24, "Schematischer MCU-SoC — DRAM nicht zwingend auf demselben Die", 16))
    p.append(f'<rect x="40" y="50" width="640" height="250" rx="10" fill="none" stroke="{INK}" stroke-dasharray="6 4"/>')
    p.append(txt(52, 72, "Silizium-Die", 14, MUTED, weight="400"))
    boxes = [(70, 110, "CPU"), (220, 90, "L1-I/D"), (220, 160, "SRAM"), (400, 90, "NOR-Flash"), (400, 160, "MMIO")]
    for x, y, name in boxes:
        p.append(f'<rect x="{x}" y="{y}" width="130" height="48" rx="6" fill="#FFF" stroke="{DATA if "L1" in name or name=="SRAM" or "Flash" in name else INK}"/>')
        p.append(txt(x + 12, y + 30, name, 16))
    p.append(f'<line x1="200" y1="134" x2="220" y2="114" stroke="{CTRL}" stroke-width="2"/>')
    p.append(f'<line x1="200" y1="134" x2="220" y2="184" stroke="{DATA}" stroke-width="2"/>')
    p.append(f'<line x1="350" y1="114" x2="400" y2="114" stroke="{INK}"/>')
    p.append(f'<line x1="350" y1="184" x2="400" y2="184" stroke="{INK}"/>')
    p.append(txt(70, 230, "Interconnect on-chip", 15, CTRL))
    p.append(f'<rect x="740" y="120" width="200" height="60" rx="6" fill="#FFF" stroke="{STATE}"/>')
    p.append(txt(760, 155, "DRAM off-chip", 16, STATE))
    p.append(f'<line x1="680" y1="150" x2="740" y2="150" stroke="{STATE}" stroke-dasharray="5 3"/>')
    p.append(txt(740, 210, "nur wenn das System", 14, MUTED, weight="400"))
    p.append(txt(740, 230, "Hauptspeicher braucht", 14, MUTED, weight="400"))
    save("soc-interconnect.svg", p)

def fig_floating_gate():
    w, h = 980, 320
    p = svg_open(w, h)
    for i, title in enumerate(("ohne Elektronen, Vth niedrig", "Elektronen im FG, Vth höher")):
        x = 20 + i * 480
        p.append(panel(x, 10, 450, 290, title))
        p.append(f'<rect x="{x+40}" y="180" width="360" height="50" fill="#ECEFF1" stroke="{INK}"/>')
        p.append(txt(x + 160, 210, "Substrat / Kanal", 15))
        p.append(f'<rect x="{x+80}" y="150" width="80" height="30" fill="#FFF" stroke="{INK}"/>')
        p.append(txt(x + 92, 170, "S", 14))
        p.append(f'<rect x="{x+280}" y="150" width="80" height="30" fill="#FFF" stroke="{INK}"/>')
        p.append(txt(x + 300, 170, "D", 14))
        p.append(f'<rect x="{x+150}" y="120" width="140" height="22" fill="#FFF8E1" stroke="{STATE}"/>')
        p.append(txt(x + 175, 136, "Floating Gate", 13, STATE))
        if i == 1:
            p.append(txt(x + 190, 112, "e− e−", 14, STATE))
        p.append(f'<rect x="{x+150}" y="70" width="140" height="28" fill="#FFF" stroke="{CTRL}"/>')
        p.append(txt(x + 168, 90, "Control Gate", 14, CTRL))
        p.append(txt(x + 40, 250, "Oxid isoliert das Floating Gate.", 15))
    p.append(txt(20, 312, "Floating-Gate-Modell. Nicht jede moderne Flash-Zelle nutzt ein Floating Gate.", 14, MUTED, weight="400"))
    save("floating-gate.svg", p)

def fig_nand_nor():
    w, h = 1100, 360
    p = svg_open(w, h)
    p.append(panel(10, 8, 530, 250, "NOR: parallele Pfade"))
    p.append(panel(560, 8, 520, 250, "NAND: serieller String"))
    p.append(txt(30, 50, "BL", 16, DATA))
    for i, xx in enumerate((120, 220, 320)):
        p.append(nmos(xx, 70, "left"))
        p.append(f'<line x1="50" y1="80" x2="{xx}" y2="80" stroke="{DATA}"/>')
        p.append(txt(xx - 20, 60, f"WL{i}", 13, CTRL))
    p.append(txt(30, 180, "ausgewählter Pfad direkt zur BL", 15))
    p.append(txt(30, 210, "Schnittstelle: Wortadresse, XIP möglich", 15, DATA))
    p.append(txt(580, 50, "BL", 16, DATA))
    p.append(nmos(680, 60, "left"))
    p.append(nmos(680, 110, "left"))
    p.append(nmos(780, 110, "left"))
    p.append(txt(640, 55, "SGD", 13, CTRL))
    p.append(txt(640, 105, "WL", 13, CTRL))
    p.append(txt(740, 105, "SGS", 13, CTRL))
    p.append(txt(580, 200, "nur der String leitet, Page-Lesen", 15))
    p.append(txt(580, 230, "Schnittstelle: Page, Buffer, Controller", 15, DATA))
    p.append(txt(16, 300, "Elektrische Vereinfachung. NOR: parallele Zellen. NAND: Serie plus Auswahltransistoren.", 16))
    p.append(txt(16, 330, "Deshalb XIP typisch bei NOR, block-/pageorientiert bei NAND — NAND ist kein Magnetband.", 16))
    save("nand-nor.svg", p)

def fig_flash_bits():
    w, h = 1000, 260
    p = svg_open(w, h)
    states = [
        ("gelöscht", "1 1 1 1", "Block auf 1 (Modell)"),
        ("programmieren", "1 0 1 0", "nur 1→0, feiner"),
        ("erneut löschen", "1 1 1 1", "nur blockweise zurück"),
    ]
    for i, (t, bits, note) in enumerate(states):
        x = 16 + i * 326
        p.append(panel(x, 10, 310, 220, t))
        p.append(txt(x + 30, 100, bits, 32, STATE, weight="700"))
        p.append(txt(x + 20, 160, note, 16))
    p.append(txt(16, 250, "SLC-Modellkonvention: Programmieren 1→0, Erase zurück auf 1. Keine universelle Page-/Blockgröße.", 15, MUTED, weight="400"))
    save("flash-program-erase.svg", p)

def fig_rom_strip():
    w, h = 1100, 160
    p = svg_open(w, h)
    items = [
        ("Mask-ROM", "Maske, Fabrik"),
        ("PROM", "einmal, Sicherung"),
        ("EPROM", "UV-Löschen"),
        ("EEPROM", "elektrisch, Byte"),
        ("Flash", "elektrisch, Block"),
    ]
    for i, (a, b) in enumerate(items):
        x = 10 + i * 216
        p.append(f'<rect x="{x}" y="20" width="200" height="110" rx="8" fill="#FFF" stroke="{INK}"/>')
        p.append(txt(x + 12, 60, a, 18))
        p.append(txt(x + 12, 96, b, 15, MUTED, weight="400"))
        if i < 4:
            p.append(f'<line x1="{x+200}" y1="70" x2="{x+216}" y2="70" stroke="{CTRL}" stroke-width="2"/>')
    save("rom-evolution.svg", p)

def fig_wear():
    w, h = 980, 300
    p = svg_open(w, h)
    p.append(txt(16, 24, "Logischer Sektor 0 — drei Updates (schematisch)", 18))
    blocks = [(80, "Block 4", "gültig", STATE), (280, "Block 12", "alt/ungültig", MUTED), (480, "Block 27", "aktuell", DATA), (700, "Block 40", "frei", INK)]
    for x, name, st, col in blocks:
        p.append(f'<rect x="{x}" y="70" width="150" height="80" rx="6" fill="#FFF" stroke="{col}" stroke-width="2"/>')
        p.append(txt(x + 12, 105, name, 16))
        p.append(txt(x + 12, 130, st, 14, col, weight="400"))
    p.append(txt(16, 190, "FTL: logische Adresse → physischer Block. P/E-Zähler je Block steigen ungleich.", 16))
    p.append(txt(16, 220, "Wear Leveling wählt einen wenig genutzten Block. Garbage Collection ist optional und getrennt.", 16))
    p.append(txt(16, 260, "Update 1→4, Update 2→12 (4 ungültig), Update 3→27 (12 ungültig).", 16, MUTED, weight="400"))
    save("wear-leveling.svg", p)

def fig_matrix():
    w, h = 1000, 340
    p = svg_open(w, h)
    p.append(txt(16, 24, "Illustrative Adresse, nicht zwei gleiche Hälften einer 32-Bit-Adresse", 16))
    p.append(txt(16, 52, "Bank | Row | Column | Byte-Offset   (Breiten geräteabhängig)", 18, DATA))
    # grid
    for r in range(4):
        for c in range(6):
            x, y = 80 + c * 36, 80 + r * 36
            fill = "#FFF3E0" if r == 1 else "#FFF"
            p.append(f'<rect x="{x}" y="{y}" width="32" height="32" fill="{fill}" stroke="{HAIR}"/>')
    p.append(txt(16, 110, "Row", 14, CTRL))
    p.append(txt(80, 250, "Column-Mux", 14, DATA))
    p.append(f'<rect x="340" y="90" width="90" height="120" fill="#FFF" stroke="{CTRL}"/>')
    p.append(txt(352, 150, "SA /", 14, CTRL))
    p.append(txt(348, 172, "Row buf", 14, CTRL))
    p.append(txt(460, 120, "Historisch: RAS dann CAS als Strobes.", 16))
    p.append(txt(460, 150, "SDRAM: Kommandos (ACT, READ, …),", 16))
    p.append(txt(460, 176, "nicht zwingend dieselben Pins-Strobes.", 16))
    p.append(txt(16, 310, "Zeile wird aktiviert, Spalte wählt aus dem Row Buffer. Orange: ausgewählte Zeile.", 15, MUTED, weight="400"))
    save("dram-matrix.svg", p)

def fig_dpram():
    w, h = 1000, 300
    p = svg_open(w, h)
    p.append(f'<rect x="360" y="70" width="280" height="140" rx="8" fill="#FFF" stroke="{INK}" stroke-width="2"/>')
    p.append(txt(430, 150, "DPRAM", 22))
    p.append(txt(40, 90, "Port A", 18, CTRL))
    p.append(txt(40, 120, "Adresse A", 16, DATA))
    p.append(txt(40, 146, "Daten A", 16, DATA))
    p.append(txt(40, 172, "Steuerung A", 16, CTRL))
    p.append(txt(760, 90, "Port B", 18, CTRL))
    p.append(txt(760, 120, "Adresse B", 16, DATA))
    p.append(txt(760, 146, "Daten B", 16, DATA))
    p.append(txt(760, 172, "Steuerung B", 16, CTRL))
    p.append(f'<line x1="180" y1="120" x2="360" y2="120" stroke="{DATA}" stroke-width="2"/>')
    p.append(f'<line x1="640" y1="120" x2="750" y2="120" stroke="{DATA}" stroke-width="2"/>')
    p.append(txt(16, 240, "Verschiedene Adressen: konfliktfrei. Dieselbe Adresse: Verhalten implementierungsabhängig.", 16))
    p.append(txt(16, 270, "Keine feste „8T“-Zelle. Arbitration nur, wenn der Baustein sie vorsieht.", 16, MUTED, weight="400"))
    save("dpram.svg", p)

def fig_fifo():
    w, h = 980, 280
    p = svg_open(w, h)
    p.append(txt(16, 24, "Ringpuffer, ein Taktbereich. Async-FIFO braucht extra Synchronisation.", 16))
    for i in range(8):
        x = 40 + i * 90
        fill = "#E3F2FD" if i in (1, 2, 3) else "#FFF"
        p.append(f'<rect x="{x}" y="70" width="70" height="50" fill="{fill}" stroke="{INK}"/>')
        p.append(txt(x + 28, 102, str(i), 16, anchor="middle"))
    p.append(txt(120, 150, "R", 16, CTRL))
    p.append(txt(300, 150, "W", 16, DATA))
    p.append(txt(16, 200, "Push erhöht W, Pop erhöht R, beide mit Wraparound.", 16))
    p.append(txt(16, 228, "Empty: R=W. Full: nächster W würde R treffen (Konvention des Zählers).", 16))
    p.append(txt(16, 260, "UART: Watermark löst einen Interrupt aus, nicht ein Interrupt pro Bit.", 16, STATE))
    save("fifo-ring.svg", p)

def fig_floorplan():
    w, h = 860, 280
    p = svg_open(w, h)
    p.append(f'<rect x="40" y="30" width="780" height="200" rx="8" fill="#FFF" stroke="{INK}"/>')
    p.append(f'<rect x="60" y="50" width="300" height="160" fill="#E3F2FD" stroke="{DATA}"/>')
    p.append(txt(80, 130, "regelmäßiges SRAM", 16, DATA))
    p.append(txt(80, 154, "(Cache, schematisch)", 14, DATA, weight="400"))
    p.append(f'<rect x="380" y="50" width="200" height="160" fill="#FFF3E0" stroke="{CTRL}"/>')
    p.append(txt(400, 130, "Logik / ALU", 16, CTRL))
    p.append(f'<rect x="600" y="50" width="190" height="70" fill="#F3E5F5" stroke="{STATE}"/>')
    p.append(txt(616, 92, "I/O-Ring", 15, STATE))
    p.append(txt(40, 260, "Schematischer Floorplan, keine Mikroskopaufnahme.", 16, MUTED, weight="400"))
    save("floorplan.svg", p)

def fig_memmap():
    w, h = 1100, 460
    p = svg_open(w, h)
    p.append(txt(16, 22, "Schematische MCU-Map — keine STM32-/SiFive-Adressen", 16, MUTED, weight="400"))
    p.append(f'<rect x="30" y="40" width="280" height="360" fill="#FFF8E1" stroke="{CTRL}"/>')
    p.append(txt(40, 64, "FLASH (LMA)", 16, CTRL))
    p.append(txt(40, 110, ".text   Code", 16))
    p.append(txt(40, 150, ".rodata  table[]", 16))
    p.append(txt(40, 190, ".data-Image  counter=3", 16, STATE))
    p.append(txt(40, 250, "kein .bss-Array", 15, MUTED, weight="400"))
    p.append(f'<rect x="400" y="40" width="300" height="360" fill="#E3F2FD" stroke="{DATA}"/>')
    p.append(txt(410, 64, "RAM (VMA)", 16, DATA))
    p.append(txt(410, 120, ".data  counter", 16, STATE))
    p.append(txt(410, 170, ".bss   buffer[16]", 16))
    p.append(txt(410, 230, "Heap  ↑ Beispiel", 16))
    p.append(txt(410, 300, "Stack ↓ Beispiel", 16))
    p.append(f'<rect x="760" y="40" width="310" height="300" fill="#FFF" stroke="{INK}"/>')
    p.append(txt(776, 70, "Startup", 16, CTRL))
    for i, line in enumerate(["1 Stack-Pointer setzen", "2 .data Flash→RAM kopieren", "3 .bss auf 0 setzen", "4 main() aufrufen"]):
        p.append(txt(776, 110 + i * 40, line, 16))
    p.append(txt(16, 430, "static const uint32_t table[]={1,2};  uint32_t counter=3;  uint32_t buffer[16];", 16))
    save("memory-map.svg", p)

def fig_ff():
    p = svg_open(1100, 280)
    p.append(txt(16, 24, "Positiv flankengesteuert. Master bei CLK=0 offen, Slave bei CLK=1.", 16))
    labels = ["CLK", "Master", "Slave", "D", "Q"]
    waves = [
        [0,0,1,1,0,0,1,1],
        [1,1,0,0,1,1,0,0],
        [0,0,1,1,0,0,1,1],
        [0,1,1,0,0,1,1,0],
        [0,0,1,1,1,1,0,0],
    ]
    for i, (name, bits) in enumerate(zip(labels, waves)):
        y = 50 + i * 42
        p.append(txt(16, y + 16, name, 14, CTRL if i < 3 else DATA))
        x = 120
        for b in bits:
            yy = y if b else y + 18
            p.append(f'<line x1="{x}" y1="{yy}" x2="{x+70}" y2="{yy}" stroke="{INK}" stroke-width="2"/>')
            x += 70
    p.append(txt(16, 268, "Schematisch. Q uebernimmt D an der steigenden Flanke, nicht waehrend beide offen sind.", 14, MUTED, weight="400"))
    save("ff-timing.svg", p)

def fig_hold():
    p = svg_open(900, 320)
    p.append(txt(16, 24, "Hold: WL = 0. Zugriffstransistoren sperren. Q = 1, Qb = 0.", 16))
    p.append(txt(16, 70, "Zwei CMOS-Inverter: vier Transistoren. Zwei Access-Transistoren. Zusammen 6T.", 16))
    p.append(txt(16, 110, "Kreuzkopplung haelt die Spannungen. Kein dauerhafter VDD-GND-Pfad im Idealmodell.", 16))
    p.append(txt(16, 150, "Reale Leckstroeme bleiben. Der Zustand ist ohne Refresh stabil, solange VDD anliegt.", 16))
    p.append(txt(16, 200, "BL und BLb sind getrennt. WL steuert beide Access-Transistoren gemeinsam.", 16, CTRL))
    p.append(txt(16, 260, "Gleiche Geometrie wie Lesen und Schreiben. Nur die Steuersignale aendern sich.", 14, MUTED, weight="400"))
    save("sram-hold.svg", p)

def fig_cells():
    p = svg_open(1000, 220)
    p.append(txt(16, 24, "1 MiB = 8388608 Bit. Nur Zellbauelemente, keine Flaeche und keine Kosten.", 16))
    p.append(txt(16, 70, "20T-Vergleich: 167772160 Transistoren", 18, CTRL))
    p.append(txt(16, 110, "6T-SRAM: 50331648 Transistoren", 18, DATA))
    p.append(txt(16, 150, "1T1C: 8388608 Transistoren und 8388608 Kondensatoren", 18, STATE))
    p.append(txt(16, 200, "Peripherie, Leitungen und ECC fehlen. 20T ist eine Lehrannahme.", 14, MUTED, weight="400"))
    save("cell-count.svg", p)

if __name__ == "__main__":
    fig_6t_states()
    fig_sram_read()
    fig_sram_write()
    fig_dram_read()
    fig_1t1c()
    fig_refresh()
    fig_ddr()
    fig_memory_wall()
    fig_hierarchy()
    fig_von_harvard()
    fig_soc()
    fig_floating_gate()
    fig_nand_nor()
    fig_flash_bits()
    fig_rom_strip()
    fig_wear()
    fig_matrix()
    fig_dpram()
    fig_fifo()
    fig_floorplan()
    fig_memmap()
    fig_ff()
    fig_hold()
    fig_cells()
