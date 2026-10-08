#!/usr/bin/env python3
"""Lehrfiguren VL08. Roofline, TOPS und Arraytakte sind ein Modell, keine Messung."""
from pathlib import Path

OUT = Path(__file__).resolve().parent
INK, MUTED = "#1D1D1F", "#5F6368"
W, ACT, ACC, MEM = "#E65100", "#1565C0", "#1B5E20", "#6A1B9A"
ERR = "#B71C1C"

A = [[1, 2], [3, 4]]
B = [[5, 6], [7, 8]]
# C = A @ B
C = [[19, 22], [43, 50]]


def svg(w, h):
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">',
        f'<rect width="{w}" height="{h}" fill="#fff"/>',
        "<style>text{font-family:Arial,Helvetica,sans-serif;fill:#1D1D1F}</style>",
    ]


def T(x, y, s, size=15, fill=INK, weight="600", anchor="start"):
    s = str(s).replace("&", "&amp;").replace("<", "&lt;")
    return (
        f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" '
        f'fill="{fill}" text-anchor="{anchor}">{s}</text>'
    )


def R(x, y, w, h, stroke=INK, fill="#fff"):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" '
        f'stroke="{stroke}" stroke-width="1.4"/>'
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


def fig_a():
    p = svg(1200, 360)
    p.append(T(16, 22, "Lokale und Cloud-Inferenz. Keine Aussage, Funk sei immer teurer.", 16))
    for x, title, lines, col in (
        (16, "Lokal", ["Sensor", "Vorverarbeitung", "Inferenz", "Ergebnis"], ACT),
        (620, "Cloud", ["Sensor", "Funk", "Server-Inferenz", "Antwort"], W),
    ):
        p.append(R(x, 48, 520, 150, col))
        p.append(T(x + 16, 74, title, 16, col))
        for i, line in enumerate(lines):
            p.append(T(x + 16 + i * 120, 120, line, 14))
    p.append(T(16, 230, "Anforderungen: Latenz, Energie, Datenschutz, Verfuegbarkeit. Jede kann ausfallen.", 15))
    p.append(T(16, 258, "Edge umfasst auch Gateways. Nicht jede lokale Inferenz braucht eine NPU.", 15))
    p.append(T(16, 286, "Lokal bleiben heisst nicht automatisch datenschutzkonform oder sicher.", 15, ERR))
    p.append(T(16, 320, "OoO kann Load-Latenzen und mehrere Akkumulatoren nutzen. Eine einzelne Kette bleibt RAW.", 14, MUTED, "400"))
    p.append(T(16, 346, "-O3 garantiert weder Unrolling noch kuerzere Laufzeit.", 14, MUTED, "400"))
    save("edge.svg", p)


def fig_b():
    p = svg(1200, 420)
    p.append(T(16, 22, "Dense y = Wx+b. W ist 2x3, x hat 3, b und y haben 2. Integer-Analogie, kein Float-mul.", 15))
    p.append(T(16, 48, "W = [[1,2,3],[0,-1,4]], x = [2,1,3], b = [1,-2]", 16, W))
    p.append(T(16, 78, "y0 = 1*2 + 2*1 + 3*3 + 1 = 14", 16, ACT))
    p.append(T(16, 104, "y1 = 0*2 + (-1)*1 + 4*3 + (-2) = 9", 16, ACT))
    p.append(T(16, 140, "Parameter 6+2 = 8. MACs nur die Produkte: 6. Nicht allgemein Parameter = MACs.", 15, ERR))
    p.append(T(16, 168, "1 MAC = 2 arithmetische Ops in dieser TOPS-Konvention. Bias-Add ist extra.", 15))
    rows = [("Parameter", "8"), ("MACs", "6"), ("Arithmetik", "14"), ("Int8-Bytes Daten", "11")]
    for i, (a, b) in enumerate(rows):
        p.append(R(16 + i * 280, 190, 250, 50, MEM))
        p.append(T(28 + i * 280, 212, a, 13, MEM))
        p.append(T(28 + i * 280, 230, b, 16))
    p.append(T(16, 270, "14 = 6*2 + 2 Bias-Additionen. Schleife und Pointer zaehlen hier nicht mit.", 14))
    p.append(T(16, 298, "RV32IM mul/add sind Ganzzahl. Eine Float32-MAC waere eine andere ISA.", 15, ERR))
    p.append(T(16, 326, "FMA rundet einmal. Getrennte Mul und Add runden zweimal.", 14))
    p.append(T(16, 354, "Convolution: ein Gewicht wird mehrfach benutzt. Dann sind MACs groesser als die Parameterzahl.", 14, MUTED, "400"))
    p.append(T(16, 386, "10^6 Gewichte sind nur unter der Annahme ein Gewicht pro MAC auch 10^6 MACs.", 14, MUTED, "400"))
    save("dense.svg", p)


def fig_c():
    p = svg(1200, 400)
    p.append(T(16, 20, "Lehr-Roofline, keine Chipmessung. Grenze: DRAM zu On-Chip. Peak 8 Ops/Takt, Band 8 Byte/Takt.", 14))
    p.append(T(16, 44, "Knick bei Peak/Bandbreite = 1 Op/Byte.", 16, MEM))
    # axes
    p.append(T(80, 250, "0,25", 13, ACT))
    p.append(R(140, 200, 80, 40, ACT, "#E3F2FD"))
    p.append(T(150, 224, "naiv", 13, ACT))
    p.append(T(280, 180, "0,5", 13, ACC))
    p.append(R(330, 160, 80, 40, ACC, "#E8F5E9"))
    p.append(T(338, 184, "Reuse", 13, ACC))
    p.append(L(80, 250, 520, 80, ACT, 3))
    p.append(L(520, 80, 1100, 80, ERR, 3))
    p.append(T(80, 270, "Bandbreite", 12, ACT))
    p.append(T(700, 72, "Peak 8 Ops/Takt", 12, ERR))
    p.append(T(16, 280, "Naiv: 2 Ops / 8 Byte = 0,25. Erreichbar min(8, 8*0,25) = 2 Ops/Takt.", 15))
    p.append(T(16, 308, "2x2 ohne Wiederverwendung: 64 Byte, untere Schranke 8 Takte bei 8 Byte/Takt.", 15))
    p.append(T(16, 336, "Mit lokalem Tile: 32 Byte, Schranke 4 Takte. Rechnung min(Peak, Band*AI).", 15, ACC))
    p.append(T(16, 368, "Nicht jeder Zugriff ist ein DRAM-Miss. SRAM, Cache-Hit und Prefetch sind andere Faelle.", 14, MUTED, "400"))
    save("roofline.svg", p)


def fig_d():
    p = svg(1200, 360)
    p.append(T(16, 22, "Dieselbe 2x2-Matmul. Lokaler Speicher fasst A und B, 8 Elemente.", 16))
    p.append(R(16, 48, 520, 140, ACT))
    p.append(T(28, 74, "Naiv, kein Halten", 15, ACT))
    p.append(T(28, 102, "8 Produkte, jedes A und B neu", 14))
    p.append(T(28, 128, "16 Float32-Loads = 64 Byte", 14))
    p.append(R(580, 48, 560, 140, ACC))
    p.append(T(592, 74, "Ein Tile, alles lokal", 15, ACC))
    p.append(T(592, 102, "A und B einmal laden: 8 Floats", 14))
    p.append(T(592, 128, "32 Byte extern, Produkte aus dem Tile", 14))
    p.append(T(16, 220, "Gewichte, Aktivierungen und Teilsummen getrennt zaehlen.", 15))
    p.append(T(16, 248, "Zwischenaktivierungen koennen mehr Speicher brauchen als die Gewichte.", 15, ERR))
    p.append(T(16, 276, "Systolische Weitergabe hilft lokal. Den externen Verkehr beseitigt sie nicht.", 15))
    p.append(T(16, 310, "Annahme: Element bleibt im Tile, kein Write-Allocate, Output-Bytes zunaechst getrennt.", 13, MUTED, "400"))
    p.append(T(16, 338, "CPU und GPU koennen dasselbe Blocking. Das Array ist eine Hardwareform davon.", 13, MUTED, "400"))
    save("tile.svg", p)


def fig_e():
    p = svg(1200, 360)
    p.append(T(16, 22, "Packed Add ist kein Int8-Dot-Product. Lanes haben getrennte Uebertraege.", 16))
    lanes = [("0x01", "0x02", "0x03"), ("0x7F", "0x01", "sat?")]
    p.append(T(16, 60, "Lane", 14, MUTED, "400"))
    for i, (a, b, s) in enumerate([("01", "02", "03"), ("10", "20", "30"), ("7F", "01", "80/sat"), ("FF", "01", "00/sat")]):
        p.append(R(80 + i * 250, 44, 220, 70, ACT))
        p.append(T(92 + i * 250, 70, f"{a} + {b}", 16, ACT))
        p.append(T(92 + i * 250, 96, f"Ergebnis {s}", 14))
    p.append(T(16, 150, "Int8-MAC: Produkt, dann breiter Akkumulator. Signed/Unsigned und Saettigung festlegen.", 15, W))
    p.append(T(16, 178, "Beispiel: 20 * 20 passt nicht in int8. Akkumulator hier int32.", 15))
    p.append(T(16, 214, "Ein neuer MAC je Takt ist ein Initiationsintervall, nicht die Ergebnis-Latenz.", 15, ERR))
    p.append(T(16, 246, "Zwei Speicherbusse helfen nur ohne Bankkonflikt.", 15))
    p.append(T(16, 274, "Zero-Overhead-Loop entfernt den Schleifenzweig, nicht jeden Daten-Stall.", 15))
    p.append(T(16, 310, "SIMD, RVV und NPU sind kombinierbar, keine Pflicht-Reihenfolge.", 14, MUTED, "400"))
    p.append(T(16, 338, "Die letzten beiden Lanes zeigen Wrap ohne Saettigung beziehungsweise den Saettigungsfall als Alternative.", 13, MUTED, "400"))
    save("simd.svg", p)


def fig_f():
    p = svg(1200, 420)
    p.append(T(16, 20, "LMUL=1, e32. VLMAX = VLEN/SEW. VLEN ist nicht die Lane-Zahl.", 16))
    p.append(R(16, 48, 540, 90, ACT))
    p.append(T(28, 74, "VLEN 128 Bit, VLMAX 4", 16, ACT))
    p.append(T(28, 100, "1000 Elemente: 250 mal VL=4, Rest 0", 14))
    p.append(R(600, 48, 560, 90, W))
    p.append(T(612, 74, "VLEN 1024 Bit, VLMAX 32", 16, W))
    p.append(T(612, 100, "Eine Policy: 30 mal 32, dann 32+8", 14))
    p.append(T(16, 170, "31*32+8 = 1000. Zusammen 32 Schleifen, nicht 31.", 16, ERR))
    p.append(T(16, 202, "vsetvli liefert nicht immer min(AVL, VLMAX), wenn AVL zwischen VLMAX und 2*VLMAX liegt.", 15))
    p.append(T(16, 234, "Ist der Rest 8 und VLMAX 32, ist VL genau 8, nicht frei gewaehlt.", 14))
    p.append(T(16, 270, "Eine physische Lane-Gruppe kann VLMAX Elemente ueber mehrere Takte rechnen.", 15, MEM))
    p.append(T(16, 302, "Ein Binary braucht passende ISA, Erweiterung, ABI und einen RVV-Kern.", 15))
    p.append(T(16, 334, "Pointer += VL * 4 Byte. Zaehler -= VL. Ende bei AVL 0.", 15, ACC))
    p.append(T(16, 370, "Policy im Beispiel: ta, ma, m1. Spezifikation RVV 1.0.", 14, MUTED, "400"))
    p.append(T(16, 398, "Keine Toolchain in diesem Repository hat die Schleife assembliert.", 13, MUTED, "400"))
    save("rvv.svg", p)


def fig_g():
    p = svg(1200, 430)
    x0, cw = 230, 100
    p.append(T(16, 22, "Gleiche Achse Takte 1-9. Mul-Latenz 2, Add-Latenz 1, II 1. Keine RVV-Messung.", 14))
    for c in range(1, 10):
        x = x0 + (c - 1) * cw
        p.append(T(x + cw / 2, 52, str(c), 13, MUTED, "600", "middle"))
        p.append(L(x, 60, x, 330, MUTED, 0.6, "3 4"))
    p.append(L(x0 + 9 * cw, 60, x0 + 9 * cw, 330, MUTED, 0.6, "3 4"))

    def bar(row_y, start, span, label, color):
        x = x0 + (start - 1) * cw + 6
        p.append(R(x, row_y, span * cw - 12, 28, color))
        p.append(T(x + 8, row_y + 19, label, 12))

    p.append(T(16, 92, "Ohne, Mul", 13, ACT))
    p.append(T(16, 142, "Ohne, Add", 13, ACC))
    for i in range(4):
        bar(74, i + 1, 2, f"e{i}", ACT)
        bar(124, i + 6, 1, f"e{i}", ACC)
    p.append(T(16, 214, "Mit, Mul", 13, ACT))
    p.append(T(16, 264, "Mit, Add", 13, W))
    for i in range(4):
        bar(196, i + 1, 2, f"e{i}", ACT)
        bar(246, i + 3, 1, f"e{i}", W)
    # e0: Mul endet Ende Takt 2, Add mit Chaining startet Takt 3
    xfwd = x0 + 2 * cw
    p.append(L(xfwd, 102, xfwd, 246, ERR, 1.8))
    p.append(T(xfwd + 6, 180, "e0 weiter", 12, ERR))
    p.append(T(16, 370, "Ohne Chaining letztes Ergebnis Ende Takt 9. Mit Chaining erstes Ende Takt 3, letztes Ende Takt 6.", 14))
    p.append(T(16, 398, "Vier Mul und vier Add bleiben. RVV garantiert das nicht. Zwei Instruktionen sind keine FMA.", 14, ERR))
    save("chain.svg", p)


def systolic():
    """Return per clock list of (i,j,k,prod,acc). clocks 1..4."""
    acc = [[0, 0], [0, 0]]
    out = []
    for t in range(4):
        step = []
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    if k + i + j == t:
                        prod = A[i][k] * B[k][j]
                        acc[i][j] += prod
                        step.append((i, j, k, prod, acc[i][j]))
        out.append(step)
    return out


def fig_h():
    p = svg(1200, 460)
    p.append(T(16, 18, "Output-Stationary. A nach rechts, B nach unten, C bleibt. Takt = ein gueltiger MAC.", 14))
    p.append(T(16, 40, "C00=19, C01=22, C10=43, C11=50. Fertig in den Takten 2, 3, 3 und 4.", 16, ACC))
    steps = systolic()
    for t, step in enumerate(steps, start=1):
        y = 58 + (t - 1) * 70
        p.append(T(16, y + 22, f"T{t}", 14, MEM))
        for n, (i, j, k, prod, acc) in enumerate(step):
            p.append(R(70 + n * 280, y, 260, 52, W if acc in (19, 22, 43, 50) else ACT))
            p.append(T(80 + n * 280, y + 22, f"C{i}{j} k={k} +{prod}", 13))
            p.append(T(80 + n * 280, y + 42, f"Summe {acc}", 14, ACC))
    p.append(T(16, 360, "Nicht: ab Takt 3 ein fertiger Output je Takt. C11 endet erst in Takt 4.", 15, ERR))
    p.append(T(16, 388, "Staffelung: gleiche k treffen sich, weil Zeile und Spalte verzoegert eingespeist werden.", 14))
    p.append(T(16, 416, "Fill Takt 1, Compute bis Takt 4, Readout der lokalen C danach. Drain ist kein Automatismus.", 14, MUTED, "400"))
    p.append(T(16, 444, "Leere Zellen in einem Takt sind ungueltige Begegnungen, keine extra MACs.", 13, MUTED, "400"))
    save("array.svg", p)


def fig_i():
    p = svg(1200, 340)
    p.append(T(16, 22, "Zwei Dataflows. Der Rand-Speicherzugriff gilt fuer dieses vereinfachte Array.", 15))
    p.append(R(16, 50, 560, 150, ACT))
    p.append(T(28, 76, "Output-Stationary", 16, ACT))
    p.append(T(28, 104, "C bleibt. A horizontal, B vertikal.", 14))
    p.append(T(28, 130, "Teilsumme lokal. Readout am Ende.", 14))
    p.append(T(28, 156, "Gewichte fliessen, sie stehen nicht fest.", 14, ERR))
    p.append(R(620, 50, 540, 150, W))
    p.append(T(632, 76, "Weight-Stationary", 16, W))
    p.append(T(632, 104, "Gewicht steht. Aktivierung fliesst.", 14))
    p.append(T(632, 130, "Teilsumme kann weiterwandern.", 14))
    p.append(T(632, 156, "Weights brauchen trotzdem Load und Wechsel.", 14, ERR))
    p.append(T(16, 230, "Nicht jede NPU ist systolisch und nicht jede rechnet nur Matrizen.", 15))
    p.append(T(16, 258, "Vergleich CPU/GPU/NPU braucht Datentyp, Batch, Auslastung und Transfer.", 15))
    p.append(T(16, 292, "TPU v1: 256*256*2*700e6 = 91,75e12 Ops/s, oft 92 TOPS genannt. Datacenter, kein mW-Edge.", 14, MUTED, "400"))
    p.append(T(16, 320, "Peak ist nicht die End-to-End-Inferenzleistung.", 14, MUTED, "400"))
    save("stationary.svg", p)


def fig_j():
    p = svg(1200, 360)
    p.append(T(16, 22, "Peak-Rechnung und illustrative Auslastung. Keine gemessenen TOPS/W.", 16))
    p.append(T(16, 52, "65536 MACs * 700 MHz = 45,8752 TMAC/s. Mal 2 Ops = 91,7504 TOPS.", 15, W))
    p.append(T(16, 88, "2x2-Rechnung auf einem gedachten 4x4-Array: 4 von 16 Zellen aktiv = 25 Prozent.", 15, ACT))
    for r in range(4):
        for c in range(4):
            on = r < 2 and c < 2
            p.append(R(16 + c * 36, 110 + r * 36, 32, 32, ACC if on else MUTED, "#E8F5E9" if on else "#f5f5f5"))
    p.append(T(200, 150, "Gruen = aktive Zelle des 2x2-Beispiels.", 14, ACC))
    p.append(T(16, 280, "Pruefliste: Praezision, Ops je MAC, Sparse oder Dense, Batch, Messgrenze, End-to-End-Latenz.", 14))
    p.append(T(16, 308, "Nullen in einer Dense-Matrix sparen keine Zeit, solange der Kernel sie rechnet.", 15, ERR))
    p.append(T(16, 338, "Tile, Fill, Drain und nicht beschleunigte Operatoren senken die Auslastung.", 14, MUTED, "400"))
    save("tops.svg", p)


def fig_k():
    p = svg(1200, 400)
    p.append(T(16, 20, "real = scale * (q - zero_point). scale=0,1 zero_point=0. Rundung zur naechsten Zahl.", 14))
    p.append(T(16, 50, "1,24 -> q=12 -> zurueck 1,2. Fehler 0,04.", 16, ACT))
    p.append(T(16, 78, "20,0 -> Rohwert 200 -> Clamp 127 -> zurueck 12,7.", 16, ERR))
    p.append(T(16, 114, "Int8-Gewichte: 4 Byte auf 1 Byte, 75 Prozent weniger reine Gewichtsbytes.", 15))
    p.append(T(16, 142, "Bias, Metadaten, Aktivierungen, Scratch und Arena bleiben extra.", 15, W))
    p.append(R(16, 170, 340, 80, MEM))
    p.append(T(28, 196, "Flash: Gewichte", 14, MEM))
    p.append(T(28, 220, "nur der konstante Block", 13))
    p.append(R(400, 170, 740, 80, ACT))
    p.append(T(412, 196, "SRAM: Input, Output, Aktivierungen, Scratch", 14, ACT))
    p.append(T(412, 220, "Arena ist dieser Puffer, kein zweiter Heap", 13))
    p.append(T(16, 280, "Int32-Akkumulator fuer geeignete Int8-MACs. Per-Tensor und Per-Channel sind verschiedene Scales.", 14))
    p.append(T(16, 308, "Integer ist nicht auf jeder CPU schneller. Accuracy gehoert auf Testdaten gemessen.", 15, ERR))
    p.append(T(16, 340, "Pruning aendert die Darstellung. Weniger MACs nur, wenn der Kernel Sparse versteht.", 14))
    p.append(T(16, 372, "Kein 10-KiB- oder 20-KB-Wert ohne Messung.", 14, MUTED, "400"))
    save("quant.svg", p)


def fig_l():
    p = svg(1200, 360)
    p.append(T(16, 20, "Workflow. Das Byte-Array ist Modelldaten, kein ausfuehrbarer Maschinencode.", 15))
    steps = ["Trainieren", "Quantisieren", "Operator pruefen", "C-Array", "Vorverarbeitung", "Invoke", "Pruefen"]
    for i, name in enumerate(steps):
        p.append(R(16 + (i % 4) * 290, 48 + (i // 4) * 70, 270, 52, ACT if i < 4 else ACC))
        p.append(T(28 + (i % 4) * 290, 80 + (i // 4) * 70, name, 14))
    p.append(T(16, 210, "CPU-Kernel ist der Default. Eine NPU braucht Backend, Operator und Toolchain.", 15, ERR))
    p.append(T(16, 240, "AllocateTensors und Invoke haben Rueckgaben. Arena-Groesse wird gemessen, nicht geraten.", 15))
    p.append(T(16, 270, "Int8-Input folgt scale und zero_point der Trainingsvorverarbeitung.", 15))
    p.append(T(16, 300, "Ein Logit ist keine kalibrierte Wahrscheinlichkeit. 0,8 ist keine allgemeine Schwelle.", 15, W))
    p.append(T(16, 334, "Renode-Funktion ist kein Beweis fuer Memory Wall, CPI oder NPU-Beschleunigung.", 14, MUTED, "400"))
    save("flow.svg", p)


if __name__ == "__main__":
    assert A[0][0] * B[0][0] + A[0][1] * B[1][0] == 19
    assert A[0][0] * B[0][1] + A[0][1] * B[1][1] == 22
    assert A[1][0] * B[0][0] + A[1][1] * B[1][0] == 43
    assert A[1][0] * B[0][1] + A[1][1] * B[1][1] == 50
    y0 = 1 * 2 + 2 * 1 + 3 * 3 + 1
    y1 = 0 * 2 + (-1) * 1 + 4 * 3 + (-2)
    assert (y0, y1) == (14, 9)
    macs = 65536 * 700_000_000
    assert macs == 45_875_200_000_000
    assert macs * 2 == 91_750_400_000_000
    assert 31 * 32 + 8 == 1000
    q = max(-128, min(127, int(round(1.24 / 0.1))))
    assert q == 12
    q2 = max(-128, min(127, int(round(20.0 / 0.1))))
    assert q2 == 127
    for fn in (fig_a, fig_b, fig_c, fig_d, fig_e, fig_f, fig_g, fig_h, fig_i, fig_j, fig_k, fig_l):
        fn()
    # systolic final
    acc = [[0, 0], [0, 0]]
    done = {}
    for t, step in enumerate(systolic(), start=1):
        for i, j, k, prod, total in step:
            acc[i][j] = total
            if (i, j) == (0, 0) and total == 19:
                done.setdefault((i, j), t)
            if total in (22, 43, 50) and (i, j) not in done:
                if (i, j) != (0, 0):
                    done[(i, j)] = t
    assert acc == C
    assert done[(0, 0)] == 2 and done[(0, 1)] == 3 and done[(1, 0)] == 3 and done[(1, 1)] == 4
    print("checks ok", done)
