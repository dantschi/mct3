#!/usr/bin/env python3
"""Didaktische Vektorfiguren für VL02. Zahlen aus dem Referenzmodell, keine Messdaten."""
from pathlib import Path

OUT = Path(__file__).resolve().parent
TAG, IDX, OFF = "#6A1B9A", "#E65100", "#1565C0"
INK, MUTED, HAIR = "#1D1D1F", "#5F6368", "#E5E5EA"
HIT, MISS = "#1B5E20", "#B71C1C"

def svg(w, h):
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">',
        f'<rect width="{w}" height="{h}" fill="#fff"/>',
        '<style>text{font-family:Arial,Helvetica,sans-serif;fill:#1D1D1F}</style>',
    ]

def T(x, y, s, size=18, fill=INK, anchor="start", w="600"):
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{w}" fill="{fill}" text-anchor="{anchor}">{s}</text>'

def save(name, parts):
    (OUT / name).write_text("\n".join(parts) + "\n</svg>\n", encoding="utf-8")
    print(name)

def box(x, y, w, h, fill="#fff", stroke=INK):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{stroke}"/>'

def fig_locality():
    p = svg(1100, 280)
    p += [T(16, 24, "Modell: kalter Cache, 64-B-Lines, keine Verdrängung in dieser Folge", 16, MUTED, w="400")]
    p += [T(16, 58, "Zeitlich: 0x1000, 0x1000, 0x1000", 18)]
    for i, lab in enumerate(["Miss", "Hit", "Hit"]):
        c = MISS if lab == "Miss" else HIT
        p += [box(16 + i * 140, 72, 120, 36, "#fff", c), T(28 + i * 140, 96, lab, 16, c)]
    p += [T(16, 150, "Räumlich (Daten): 0x1000, 0x1004, 0x1008 — dieselbe Line 0x1000–0x103F", 18)]
    for i, lab in enumerate(["Miss", "Hit", "Hit"]):
        c = MISS if lab == "Miss" else HIT
        p += [box(16 + i * 140, 164, 120, 36, "#fff", c), T(28 + i * 140, 188, lab, 16, c)]
    p += [T(16, 230, "Befehlsfolge PC, PC+4 liegt im L1-I. Daten-Loads liegen im L1-D.", 16)]
    p += [T(16, 258, "Assemblerfolge ist gemischt. Die Kaesten sind zwei getrennte Vergleichsspuren.", 15, MUTED, w="400")]
    save("locality.svg", p)

def fig_layout():
    p = svg(1100, 260)
    p += [T(16, 24, "Array: aufeinanderfolgende uint32_t in einer 64-Byte-Line", 18)]
    for i in range(8):
        p += [box(16 + i * 70, 40, 66, 40, "#E3F2FD", OFF), T(28 + i * 70, 66, f"+{4*i}", 14, OFF)]
    p += [T(16, 110, "Line 0x1000–0x103F nutzt hier 32 von 64 Byte (8 Wörter gezeichnet).", 15, MUTED, w="400")]
    p += [T(16, 150, "Liste: ein mögliches verstreutes Layout, nicht jedes Listenlayout", 18)]
    xs = [16, 220, 480, 760]
    addrs = ["0x2000", "0x8040", "0x4010", "0x9000"]
    for x, a in zip(xs, addrs):
        p += [box(x, 168, 140, 40, "#FFF3E0", IDX), T(x + 12, 194, a, 16, IDX)]
    p += [T(16, 240, "Jede Adresse kann eine eigene Line füllen. Nachbarn der Liste liegen dann nicht in der Line.", 16)]
    save("array-list.svg", p)

def fig_amat():
    p = svg(1100, 300)
    p += [T(16, 24, "100 Zugriffe, Hit Time 1, zusätzliche Miss Penalty 100 (berechnetes Modell)", 16)]
    p += [box(16, 40, 760, 28, "#E8F5E9", HIT), T(24, 60, "100 × 1 Takt Hit Time", 16, HIT)]
    p += [box(16, 78, 38, 28, "#FFEBEE", MISS), T(64, 98, "5 × 100 Takte extra", 16, MISS)]
    p += [T(16, 140, "95×1 + 5×(1+100) = 600 Takte;  600/100 = 6 Takte/Zugriff", 20)]
    p += [T(16, 176, "AMAT = 1 + MissRate×100", 18, TAG)]
    pts = [(0, 1), (0.05, 6), (0.1, 11), (0.2, 21), (0.5, 51)]
    p += [T(16, 210, "Kurve (Modell): Miss Rate 0 → 1;  5 % → 6;  10 % → 11;  50 % → 51", 16)]
    p += [T(16, 246, "6 Takte sind mittlere Zugriffszeit. 100/6 ist kein gemessener Programm-Speedup.", 16, MUTED, w="400")]
    p += [T(16, 278, "Ohne Cache im selben Modell: jeder Zugriff 100 Takte, nicht 1+100.", 16, MUTED, w="400")]
    save("amat.svg", p)

def fig_line():
    p = svg(1100, 240)
    p += [T(16, 22, "64-Byte-Grenzen. Dezimaladresse 1000 liegt in Line 960–1023, Offset 40.", 17)]
    p += [box(40, 40, 900, 36, "#E3F2FD", OFF)]
    p += [T(48, 64, "960", 16, OFF), T(860, 64, "1023", 16, OFF, "end")]
    p += [f'<line x1="640" y1="40" x2="640" y2="76" stroke="{MISS}" stroke-width="3"/>']
    p += [T(620, 100, "1000", 16, MISS, "middle")]
    p += [T(16, 140, "Ausgerichtetes uint32_t-Array, Basis mod 64 = 0: eine Line = 16 Elemente.", 17)]
    p += [T(16, 176, "Weitere Elemente derselben gültigen Line sind Hits, solange sie nicht verdrängt oder invalidiert wird.", 16)]
    p += [T(16, 214, "Ein Miss lädt 960–1023, nicht 1000–1063.", 18, MISS)]
    save("line-bounds.svg", p)

def band(p, y, title, segs):
    p.append(T(16, y, title, 16))
    x = 16
    for w, label, col in segs:
        p.append(box(x, y + 8, w, 36, "#fff", col))
        p.append(T(x + 8, y + 32, label, 14, col))
        x += w

def fig_bits():
    p = svg(1100, 220)
    p += [T(16, 22, "0x12345678, 32-Bit-Byteadresse, Zweierpotenzen. Metadaten zählen nicht zur Datenkapazität.", 15, MUTED, w="400")]
    band(p, 40, "Direct Mapped 32 KiB, 512 Sets, 64 B: Tag 0x2468, Index 345, Offset 56", [(420, "Tag 17 Bit", TAG), (220, "Index 9", IDX), (160, "Off 6", OFF)])
    band(p, 120, "4-Way, gleiche Datenkapazität, 128 Sets: Tag 0x91A2, Set 89, Offset 56", [(480, "Tag 19 Bit", TAG), (180, "Index 7", IDX), (160, "Off 6", OFF)])
    save("bitfields.svg", p)

def arrow(x1, y1, x2, y2):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{INK}" stroke-width="2" marker-end="url(#arr)"/>'

def fig_datapath():
    p = svg(1100, 340)
    p += ['<defs><marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#1D1D1F"/></marker></defs>']
    p += [T(16, 24, "Direct-Mapped-Leseweg. Ein Miss geht zur naechsten Ebene, nicht immer zum DRAM.", 16)]
    steps = [
        (16, "Adresse"),
        (190, "Index"),
        (360, "Tag + Valid"),
        (560, "Vergleich"),
        (760, "Offset-MUX"),
        (940, "CPU"),
    ]
    for x, lab in steps:
        p += [box(x, 48, 140, 44, "#fff", INK), T(x + 10, 76, lab, 15)]
    for x in (156, 330, 500, 700, 900):
        p += [arrow(x, 70, x + 30, 70)]
    p += [box(190, 130, 310, 70, "#F3E5F5", TAG), T(204, 158, "gespeichertes Tag", 16, TAG), T(204, 184, "Valid = 1 und Tag gleich", 15, TAG)]
    p += [box(560, 130, 300, 70, "#E3F2FD", OFF), T(574, 158, "Datenarray, ein Way", 16, OFF), T(574, 184, "Offset waehlt das Wort", 15, OFF)]
    p += [arrow(345, 130, 345, 96)]
    p += [arrow(700, 130, 830, 96)]
    p += [box(16, 230, 500, 80, "#FFEBEE", MISS), T(28, 260, "Miss: Fill von der naechsten Ebene", 16, MISS), T(28, 288, "alte Dirty-Line zuerst sichern", 15, MISS)]
    p += [box(540, 230, 530, 80, "#E8F5E9", HIT), T(552, 260, "4-Way: vier Kandidaten, ein Hit-Way", 16, HIT), T(552, 288, "Decoder, SRAM, Vergleich brauchen Zeit", 15, HIT)]
    save("datapath.svg", p)

def fig_thrash():
    p = svg(1100, 420)
    p += [T(16, 24, "Acht Loads: 0x1000 / 0x9000 im Wechsel. Kalt, keine Prefetches.", 16)]
    p += [T(16, 52, "DM  Index 64   Tags 0 und 1", 16, MISS)]
    p += [T(560, 52, "4-Way  Set 64   Tags 0 und 4", 16, HIT)]
    seq = ["1000", "9000", "1000", "9000", "1000", "9000", "1000", "9000"]
    dm = ["M", "M", "M", "M", "M", "M", "M", "M"]
    way = ["M", "M", "H", "H", "H", "H", "H", "H"]
    p += [T(24, 80, "Zugriff", 14), T(258, 80, "DM", 14, MISS), T(328, 80, "4W", 14, HIT)]
    for i, (a, d, w) in enumerate(zip(seq, dm, way)):
        y = 96 + i * 36
        p += [box(16, y, 220, 30), T(24, y + 21, f"{i+1}  0x{a}", 15)]
        p += [box(250, y, 50, 30, "#FFEBEE", MISS), T(264, y + 21, d, 15, MISS)]
        c = "#FFEBEE" if w == "M" else "#E8F5E9"
        col = MISS if w == "M" else HIT
        p += [box(320, y, 50, 30, c, col), T(334, y + 21, w, 15, col)]
    p += [box(420, 96, 640, 250), T(436, 128, "DM: beide Bloecke brauchen denselben Platz.", 16, MISS)]
    p += [T(436, 164, "Erste zwei Misses: compulsory.", 16)]
    p += [T(436, 200, "Sechs weitere: conflict, Cache sonst leer.", 16)]
    p += [T(436, 248, "4-Way: zwei Ways, danach Hits.", 16, HIT)]
    p += [T(436, 292, "Capacity-Miss ist das nicht.", 16)]
    save("thrashing.svg", p)

def fig_repl():
    p = svg(1100, 360)
    p += [T(16, 24, "Ein kaltes 4-Way-Set. Alt links, neu rechts. Nur Loads.", 16)]
    p += [T(16, 56, "FIFO nach A B C D A", 16, MISS), T(560, 56, "LRU nach A B C D A", 16, HIT)]
    fifo = ["A alt", "B", "C", "D neu"]
    lru = ["B alt", "C", "D", "A neu"]
    for i, lab in enumerate(fifo):
        p += [box(16 + i * 120, 72, 110, 44, "#FFEBEE", MISS), T(28 + i * 120, 100, lab, 16, MISS)]
    for i, lab in enumerate(lru):
        p += [box(560 + i * 120, 72, 110, 44, "#E8F5E9", HIT), T(572 + i * 120, 100, lab, 16, HIT)]
    p += [box(16, 150, 500, 80, "#FFEBEE", MISS), T(28, 182, "E verdrängt FIFO-A", 18, MISS), T(28, 210, "Hit auf A aendert FIFO nicht", 15, MISS)]
    p += [box(560, 150, 500, 80, "#E8F5E9", HIT), T(572, 182, "E verdrängt LRU-B", 18, HIT), T(572, 210, "A wurde zuletzt benutzt", 15, HIT)]
    p += [T(16, 270, "Danach: FIFO B C D E,  LRU C D A E.", 16)]
    p += [T(16, 310, "LRU kennt die Zukunft nicht. Pseudo-LRU naehert die Reihenfolge an.", 16, MUTED, w="400")]
    save("fifo-lru.svg", p)

def fig_writes():
    p = svg(1100, 300)
    p += [T(16, 20, "Ein Wort, Start Cache=0, nächste Ebene=0. Stores 5, dann 7. Ein-Level-Modell.", 15, MUTED, w="400")]
    rows = [
        ("Write-Through ohne Puffer", "Cache 5 dann 7, Ebene sofort 5 dann 7"),
        ("Write-Through mit Puffer", "Cache schon 5/7; Puffer hält Updates; voller Puffer → Stall"),
        ("Write-Back", "Cache 5/7, Dirty=1; nächste Ebene bleibt 0 bis Writeback"),
    ]
    for i, (a, b) in enumerate(rows):
        y = 40 + i * 70
        p += [box(16, y, 1060, 60), T(28, y + 26, a, 16, TAG), T(28, y + 50, b, 16)]
    p += [T(16, 270, "Dirty=0: Line verwerfen. Dirty=1: im einfachen Modell erst Writeback, dann Refill.", 16)]
    p += [T(16, 294, "Die Penalty verdoppelt sich nicht universell; Puffer und Überlappung ändern das.", 15, MUTED, w="400")]
    save("write-states.svg", p)

def fig_alloc():
    p = svg(1100, 240)
    p += [T(16, 22, "Zwei getrennte Entscheidungen, nicht fest gekoppelt.", 16)]
    p += [box(16, 48, 500, 80, "#fff", TAG), T(28, 78, "Weitergabe: Write-Through oder Write-Back", 16, TAG)]
    p += [box(540, 48, 530, 80, "#fff", IDX), T(552, 78, "Store-Miss: Allocate oder No-Allocate", 16, IDX)]
    p += [T(16, 160, "Allocate: Block laden, Store ausführen, Zustand setzen.", 17)]
    p += [T(16, 192, "No-Allocate: Store an die nächste Ebene, keinen neuen Eintrag anlegen.", 17)]
    p += [T(16, 224, "Matrix-Nullsetzen unten nur eindeutig, wenn die Store-Miss-Policy genannt ist.", 16, MUTED, w="400")]
    save("write-allocate.svg", p)

def fig_matrix():
    p = svg(1100, 420)
    p += [T(16, 22, "Miniatur: 16 Zeilen, je eine 64-Byte-Line. 8 DM-Plaetze. Nicht 1000x1000.", 16)]
    for r in range(16):
        y = 40 + r * 18
        col = "#E8F5E9" if r < 8 else "#FFEBEE"
        p += [box(16, y, 28, 16, col, INK), T(48, y + 13, f"Zeile {r:02d}  Set {r % 8}", 13)]
    p += [box(280, 40, 360, 140, "#E8F5E9", HIT)]
    p += [T(296, 70, "Zeilenweise", 18, HIT)]
    p += [T(296, 100, "1 Miss, dann 15 Hits", 16, HIT)]
    p += [T(296, 130, "gesamt 16 M / 240 H", 16, HIT)]
    p += [T(296, 160, "Line bleibt bis Zeilenende", 15, HIT)]
    p += [box(280, 200, 360, 160, "#FFEBEE", MISS)]
    p += [T(296, 230, "Spaltenweise", 18, MISS)]
    p += [T(296, 260, "Schritt = eine Zeile = 64 B", 16, MISS)]
    p += [T(296, 290, "Zeile r und r+8: Set r%8", 16, MISS)]
    p += [T(296, 320, "gesamt 256 M / 0 H", 16, MISS)]
    p += [box(680, 40, 390, 320)]
    p += [T(696, 70, "Grosses C-Beispiel getrennt", 16, TAG)]
    p += [T(696, 110, "1000 Spalten x 4 Byte", 16)]
    p += [T(696, 146, "Zeilenabstand 4000 Byte", 16)]
    p += [T(696, 182, "4000 mod 64 = 32", 16)]
    p += [T(696, 230, "Keine exakte Miss-Quote", 16, MISS)]
    p += [T(696, 266, "ohne festgelegte Spur.", 16, MISS)]
    p += [T(16, 360, "Nur die 256 Daten-Loads. Basis 0x1000 ist eine Annahme.", 15, MUTED, w="400")]
    p += [T(16, 390, "Store-Zaehlung nur mit genannter Write-Allocate-Policy.", 15, MUTED, w="400")]
    save("matrix.svg", p)

def fig_visible():
    p = svg(1100, 240)
    p += [box(16, 16, 320, 90, "#F3E5F5", TAG), T(28, 48, "Kern, Dirty-Kopie 5", 16, TAG), T(28, 76, "regulärer Write-Back", 15, TAG)]
    p += [box(360, 16, 320, 90, "#E3F2FD", OFF), T(372, 48, "Untere Ebene noch 0", 16, OFF), T(372, 76, "kein Kohärenzfehler", 15, OFF)]
    p += [box(16, 130, 500, 80), T(28, 162, "Kohärenter zweiter Kern: aktueller Wert über das Protokoll,", 15), T(28, 188, "DRAM muss nicht jederzeit 5 enthalten. Details: Block 9.", 15)]
    p += [box(540, 130, 530, 80, "#FFF3E0", IDX), T(552, 162, "Nicht kohärentes DMA: Maintenance am", 15, IDX), T(552, 188, "gemeinsamen Punkt. Kein Zicbom für jedes RV32I.", 15, IDX)]
    save("visibility.svg", p)

def fig_hierarchy():
    p = svg(1000, 220)
    p += [box(16, 40, 120, 50), T(48, 70, "CPU", 16)]
    p += [box(180, 16, 140, 44, "#FFF3E0", IDX), T(200, 44, "L1-I", 16, IDX)]
    p += [box(180, 76, 140, 44, "#E3F2FD", OFF), T(200, 104, "L1-D", 16, OFF)]
    p += [box(380, 40, 160, 50), T(420, 70, "L2", 16)]
    p += [box(600, 40, 200, 50, "#F3E5F5", TAG), T(640, 70, "nächste Ebene", 16, TAG)]
    p += [f'<line x1="136" y1="50" x2="180" y2="38" stroke="{IDX}" stroke-width="2"/>']
    p += [f'<line x1="136" y1="70" x2="180" y2="98" stroke="{OFF}" stroke-width="2"/>']
    p += [f'<line x1="320" y1="38" x2="380" y2="60" stroke="{INK}"/>']
    p += [f'<line x1="320" y1="98" x2="380" y2="70" stroke="{INK}"/>']
    p += [f'<line x1="540" y1="65" x2="600" y2="65" stroke="{TAG}" stroke-width="2"/>']
    p += [T(16, 160, "L1-Miss geht zur nächsten Ebene, nicht zwingend bis DRAM.", 17)]
    p += [T(16, 196, "Größen und Takte der Folie sind Größenordnungen, keine Messreihe.", 16, MUTED, w="400")]
    save("hierarchy.svg", p)

if __name__ == "__main__":
    fig_locality(); fig_layout(); fig_amat(); fig_line(); fig_bits()
    fig_datapath(); fig_thrash(); fig_repl(); fig_writes(); fig_alloc()
    fig_matrix(); fig_visible(); fig_hierarchy()
