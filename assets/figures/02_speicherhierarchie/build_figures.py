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
    p += [T(16, 258, "i, sum, limit der C-Schleife müssen keine Data-Cache-Zugriffe sein.", 16, MUTED, w="400")]
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

def fig_datapath():
    p = svg(1100, 300)
    p += [T(16, 22, "Direct Mapped: ein Way. 4-Way: vier Vergleiche, gleicher Datenumfang.", 16)]
    p += [box(16, 40, 200, 50, "#FFF3E0", IDX), T(28, 70, "Index → Decoder", 15, IDX)]
    p += [box(240, 40, 200, 50, "#F3E5F5", TAG), T(252, 70, "Tag-Speicher", 15, TAG)]
    p += [box(460, 40, 180, 50), T(476, 70, "Valid", 15)]
    p += [box(660, 40, 200, 50, "#E3F2FD", OFF), T(676, 70, "Datenarray", 15, OFF)]
    p += [box(240, 120, 220, 44, "#fff", HIT), T(252, 148, "Tag gleich und Valid", 15, HIT)]
    p += [box(500, 120, 220, 44, "#E3F2FD", OFF), T(512, 148, "Offset wählt Wort", 15, OFF)]
    p += [box(760, 120, 140, 44), T(790, 148, "zur CPU", 15)]
    p += [T(16, 200, "4-Way: vier Ways des Sets, vier Komparatoren, ein Daten-MUX.", 16)]
    p += [T(16, 232, "Tag-Vergleiche können parallel sein. Der Gesamtzugriff hat trotzdem Laufzeit.", 16)]
    p += [T(16, 270, "Kein Dividierer für den Index. Decoder, SRAM, Vergleich und MUX brauchen Zeit.", 16, MUTED, w="400")]
    save("datapath.svg", p)

def fig_thrash():
    p = svg(1100, 280)
    p += [T(16, 22, "0x1000 und 0x9000, kalter Cache. Beide: Set 64.", 16)]
    p += [T(16, 52, "Direct Mapped: Tags 0 und 1. Acht Misses (2 compulsory, 6 conflict).", 17, MISS)]
    p += [T(16, 88, "4-Way, LRU: Tags 0 und 4. Zwei Misses, danach sechs Hits.", 17, HIT)]
    p += [T(16, 130, "Miss-Arten: compulsory (erster Bezug), capacity (Working Set > Cache), conflict (Mapping).", 16)]
    p += [T(16, 168, "Fully associative vermeidet diesen Mapping-Konflikt, nicht jeden Capacity Miss.", 16)]
    p += [T(16, 210, "C-Arrays kollidieren nur bei passenden Basisadressen. Der Quelltext allein beweist das nicht.", 16, MUTED, w="400")]
    p += [T(16, 250, "W+1 Blöcke im selben Set überfordern auch einen W-Way-Cache.", 16)]
    save("thrashing.svg", p)

def fig_repl():
    p = svg(1100, 260)
    p += [T(16, 22, "Ein 4-Way-Set, Folge A B C D A E. Kalt. LRU und FIFO starten gleich.", 16)]
    p += [T(16, 60, "Nach A B C D A:", 18)]
    p += [T(16, 96, "FIFO-Ladereihenfolge: A ältester Geladener (Hit auf A ändert FIFO nicht) → E verdrängt A", 16, MISS)]
    p += [T(16, 136, "LRU-Nutzung: A wurde zuletzt genutzt → ältester ist B → E verdrängt B", 16, HIT)]
    p += [T(16, 180, "LRU ist eine Heuristik für zeitliche Lokalität, nicht die immer beste Policy.", 16)]
    p += [T(16, 214, "Zeitstempel sind eine mögliche Umsetzung. Pseudo-LRU nähert LRU mit weniger Zustand an.", 16, MUTED, w="400")]
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
    p = svg(1100, 280)
    p += [T(16, 20, "Miniaturmodell, nicht die 1000×1000-Matrix: uint32_t m[16][16], Basis 0x1000", 16, TAG)]
    p += [T(16, 48, "Zeile = 64 Byte = eine Line. Cache 512 Byte, direct mapped, 8 Sets, kalt, nur diese Loads.", 15)]
    p += [T(16, 84, "Adresse(m[r][c]) = 0x1000 + 4*(16*r + c)", 18)]
    p += [T(16, 124, "Zeilenweise: 16 Misses, 240 Hits.", 18, HIT)]
    p += [T(16, 156, "Spaltenweise: 256 Misses, 0 Hits.", 18, MISS)]
    p += [T(16, 196, "1000×1000, 4 Byte: Zeilenabstand 4000 Byte. 4000 ist kein Vielfaches von 64.", 16)]
    p += [T(16, 228, "Die erste Line einer Zeile beginnt dann nicht generell bei Spalte 0.", 16)]
    p += [T(16, 262, "Stores nur unter genannter Write-Allocate-Policy. Compiler kann Schleifen verändern.", 15, MUTED, w="400")]
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
