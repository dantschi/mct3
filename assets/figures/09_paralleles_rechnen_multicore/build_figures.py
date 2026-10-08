#!/usr/bin/env python3
"""Lehrfiguren VL09. MESI ist snoopbasiert, Write-Back, Write-Allocate. 64 B nur Beispiel."""
from pathlib import Path

OUT = Path(__file__).resolve().parent
INK, MUTED = "#1D1D1F", "#5F6368"
C0, C1, MEM, BUS = "#1565C0", "#E65100", "#1B5E20", "#6A1B9A"
ERR = "#B71C1C"


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


def L(x1, y1, x2, y2, stroke=INK, sw=1.6):
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" '
        f'stroke-width="{sw}"/>'
    )


def save(name, p):
    (OUT / name).write_text("\n".join(p) + "\n</svg>\n", encoding="utf-8")
    print(name)


def fig_a():
    p = svg(1200, 380)
    p.append(T(16, 22, "SMP-Lehrmodell: gleiche Kerne, ein OS, gemeinsamer Speicher. L2 ist Beispiel, keine Definition.", 14))
    p.append(R(16, 50, 250, 70, C0))
    p.append(T(28, 78, "Core0 + privates L1", 15, C0))
    p.append(T(28, 100, "Task UI", 13, MUTED, "400"))
    p.append(R(300, 50, 250, 70, C1))
    p.append(T(312, 78, "Core1 + privates L1", 15, C1))
    p.append(T(312, 100, "Task Arbeit", 13, MUTED, "400"))
    p.append(R(620, 50, 250, 70, BUS))
    p.append(T(632, 78, "Interconnect", 15, BUS))
    p.append(T(632, 100, "Kohaerenzdomaene", 13, MUTED, "400"))
    p.append(R(900, 50, 260, 70, MEM))
    p.append(T(912, 78, "L2 beispielhaft", 15, MEM))
    p.append(T(912, 100, "dann DRAM", 13, MUTED, "400"))
    p.append(T(16, 160, "Migration nur, wenn Scheduler, Port und Affinity es erlauben.", 15))
    p.append(T(16, 188, "Engpaesse: Interconnect, L2, DRAM, Locks. Mehr Kerne beschleunigen einen Thread nicht automatisch.", 14))
    p.append(T(16, 220, "SMP: ein OS, gleicher Zugriff. AMP: getrennte Software, oft ohne diese Kohaerenz.", 15, ERR))
    p.append(T(16, 252, "FreeRTOS-SMP gilt nur fuer passende Ports und Konfigurationen.", 14))
    p.append(T(16, 284, "Heterogene Kerne sind hier ausgeblendet.", 14, MUTED, "400"))
    p.append(T(16, 320, "TLP kann Aufgaben und Datenarbeit betreffen. DLP bleibt zusaetzlich moeglich.", 14, MUTED, "400"))
    p.append(T(16, 352, "Block 8 hat keine gemessene Memory Wall aus Renode geliefert.", 14, MUTED, "400"))
    save("smp.svg", p)


def fig_b():
    p = svg(1200, 400)
    p.append(T(16, 20, "Kohaerenz, Konsistenz und Atomizitaet sind drei Fragen.", 16))
    p.append(R(16, 44, 560, 90, ERR))
    p.append(T(28, 70, "Write-Through ohne Invalidation", 15, ERR))
    p.append(T(28, 96, "RAM wird 5. Core1-L1 kann weiter 0 halten.", 14))
    p.append(R(620, 44, 540, 90, MEM))
    p.append(T(632, 70, "Koordinierte Kohaerenz", 15, MEM))
    p.append(T(632, 96, "Fremde Kopie wird ungueltig oder mit 5 versorgt.", 14))
    rows = [
        ("MESI", "Writes einer Adresse", "kein i++ und kein Flag"),
        ("Atomic-RMW", "ein RMW unteilbar", "keine Publikationsordnung"),
        ("Acquire/Release", "Ordnung um ein Datum", "keine Kohaerenz allein"),
    ]
    for i, (a, b, c) in enumerate(rows):
        y = 160 + i * 48
        p.append(T(16, y, a, 15, C0))
        p.append(T(220, y, b, 15, MEM))
        p.append(T(620, y, c, 15, ERR))
    p.append(T(16, 330, "Ohne Hardware-Kohaerenz bleiben non-cacheable Speicher und Ownership moeglich, oft in AMP.", 14))
    p.append(T(16, 358, "Fuer cachebares SMP-Sharing ist das aufwendig. DMA-Maintenance ist nicht selten per Definition.", 14, MUTED, "400"))
    p.append(T(16, 386, "Nicht jede RAM-Kopie muss in jedem Takt den neuesten Wert halten.", 14, MUTED, "400"))
    save("three.svg", p)


def fig_c():
    p = svg(1200, 460)
    p.append(T(16, 20, "Vereinfachtes Write-Back-MESI. Transiente Zustaende ausgeblendet. 64 B nur Beispiel.", 14))
    states = [(40, "I", ERR), (300, "E", C0), (560, "S", MEM), (860, "M", C1)]
    for x, name, col in states:
        p.append(R(x, 48, 140, 44, col))
        p.append(T(x + 70, 76, name, 18, col, "700", "middle"))
    lines = [
        "I + lokaler Read, keine Kopie -> E, Speicher liefert",
        "I + lokaler Read, andere saubere Kopie -> S",
        "I + lokaler Read, Owner M -> Daten  vom Owner, dann S",
        "E + lokaler Write -> M, still",
        "E + Fremdread -> S, Daten teilen",
        "S + eigener Write -> erst Ownership, Invalidates, dann M",
        "S + Fremdwrite -> I",
        "M + Fremdread -> aktuelle Daten liefern, dann S",
        "M + Fremdwrite -> Daten liefern, dann I",
        "Eviction von M schreibt zurueck. Eviction von S kann S woanders lassen.",
    ]
    for i, line in enumerate(lines):
        p.append(T(16, 130 + i * 26, line, 14))
    p.append(T(16, 410, "S heisst sauber und teilbar, nicht nachweislich mehrere Kopien.", 15, ERR))
    p.append(T(16, 438, "I heisst lokal ungueltig, nicht zwingend geloeschte Bits. M und E sind exklusiv.", 14, MUTED, "400"))
    save("mesi.svg", p)


def fig_d():
    p = svg(1200, 360)
    p.append(T(16, 20, "x startet 0, beide I, RAM 0. Klassischer MESI-Pfad, Write-Back.", 15))
    headers = ["Schritt", "Core0", "Core1", "RAM", "Aktion"]
    xs = [16, 180, 360, 540, 700]
    for x, h in zip(xs, headers):
        p.append(T(x, 52, h, 13, MUTED, "400"))
    rows = [
        ("0 Read", "E:0", "I", "0", "Speicher liefert"),
        ("1 Read", "S:0", "S:0", "0", "E wird S"),
        ("0 Write 5", "M:5", "I", "0", "Invalidate, RAM noch 0"),
        ("1 Read", "S:5", "S:5", "5", "Owner liefert 5"),
    ]
    for i, row in enumerate(rows):
        y = 86 + i * 36
        for x, val in zip(xs, row):
            p.append(T(x, y, val, 15, C0 if i % 2 == 0 else C1))
    p.append(T(16, 250, "Bei M darf der untere Speicher noch 0 sein. Der folgende Read muss 5 sehen.", 15, ERR))
    p.append(T(16, 280, "Invariante: hoechstens ein M oder E. S-Kopien stimmen ueberein. I ist kein Hit.", 15))
    p.append(T(16, 310, "Gleichzeitige Schreiber: der Interconnect serialisiert Ownership.", 14))
    p.append(T(16, 338, "Snooping ist nicht an einen einzelnen Draht gebunden. Directory nur als Abgrenzung.", 13, MUTED, "400"))
    save("trace.svg", p)


def fig_e():
    p = svg(1200, 340)
    p.append(T(16, 22, "S nach M ist mehr als ein Broadcast. Erst Ownership und Bestaetigung, dann der Write.", 15))
    steps = ["Request", "Invalidate", "Ack", "Write M"]
    for i, name in enumerate(steps):
        p.append(R(16 + i * 220, 56, 190, 40, C1 if i == 3 else BUS))
        p.append(T(28 + i * 220, 82, name, 15))
    p.append(T(16, 130, "Fremdread einer M-Line: Owner liefert 5, wird S, Empfaenger wird S, RAM wird 5.", 15, MEM))
    p.append(T(16, 164, "Dirty-Shared oder Owned gehoeren nicht zu diesem MESI.", 15, ERR))
    p.append(T(16, 198, "Ein Broadcast ohne abgeschlossene Invalidates ist noch kein Write.", 15))
    p.append(T(16, 232, "Studierende pruefen die Tabelle: nach Schritt 3 ist RAM noch 0, nach Schritt 4 ist er 5.", 14))
    p.append(T(16, 270, "Mehrstufige Hierarchien sind hier auf L1 plus unteren Stand vereinfacht.", 14, MUTED, "400"))
    p.append(T(16, 304, "Sauber heisst: Uebereinstimmung mit dem kohaerenten unteren Stand, nicht magisch mit jedem RAM-Takt.", 13, MUTED, "400"))
    save("own.svg", p)


def fig_f():
    p = svg(1200, 360)
    p.append(T(16, 20, "Line beispielhaft 64 B, Basis 0x20001000. Keine Zeitmessung.", 15))
    p.append(R(16, 48, 520, 80, ERR))
    p.append(T(28, 74, "False Sharing", 15, ERR))
    p.append(T(28, 100, "temp1 bei +0, temp2 bei +4, gleiche Line", 14))
    p.append(R(580, 48, 580, 80, MEM))
    p.append(T(592, 74, "Getrennt", 15, MEM))
    p.append(T(592, 100, "temp2 bei +64 = 0x20001040", 14))
    p.append(T(16, 160, "Jeder Write holt die Ownership der ganzen Line. Der andere Kern verliert sie.", 15))
    p.append(T(16, 190, "True Sharing waere ein gemeinsamer Zaehler, nicht zwei eigene Variablen.", 15, C0))
    p.append(T(16, 220, "Padding hilft nur mit Basis, Groesse und echter Line. Array-Alignment allein reicht nicht.", 14, ERR))
    p.append(T(16, 250, "Preis: mehr Speicher und manchmal schlechtere Lokalitaet.", 14))
    p.append(T(16, 284, "Messung: Threads pinnen, Arbeit gleich, mehrfach, Optimierung nicht wegwerfen.", 14))
    p.append(T(16, 318, "Ein Simulator ohne Kohaerenzzeit belegt keine Verlangsamung.", 14, MUTED, "400"))
    save("false.svg", p)


def fig_g():
    p = svg(1200, 340)
    p.append(T(16, 20, "Start 0. Gewoehnliche Writes bleiben kohaerent und verlieren trotzdem ein Update.", 15))
    p.append(T(16, 56, "Core0", 14, C0))
    p.append(T(120, 56, "Read 0    Add 1    Write 1", 16, C0))
    p.append(T(16, 96, "Core1", 14, C1))
    p.append(T(120, 96, "Read 0    Add 1    Write 1", 16, C1))
    p.append(T(16, 140, "Speicher endet bei 1. MESI hat beide Writes geordnet, die Rechnung nicht.", 15, ERR))
    p.append(T(16, 176, "Zwei atomare Fetch-Adds: alte Werte 0 und 1, Ende 2. Reihenfolge der Alten offen.", 15, MEM))
    p.append(T(16, 214, "Ungeschuetztes C-int ist ein Data Race und in C11 undefiniert. Das Bild ist nur Motivation.", 14))
    p.append(T(16, 248, "i++ ist eine Quelltextoperation, keine garantierte Atomic-RMW.", 15))
    p.append(T(16, 282, "AMO kann das RMW in einer Instruktion ausdruecken. Intern bleibt ein Datenpfad.", 14, MUTED, "400"))
    p.append(T(16, 316, "volatile erzwingt Compilerzugriffe und schafft weder Atomizitaet noch Ordnung.", 14, MUTED, "400"))
    save("race.svg", p)


def fig_h():
    p = svg(1200, 480)
    p.append(T(16, 20, "LR setzt eine Reservation auf eine Granule, kein gehaltenes Mutex. SC-Erfolg liefert 0.", 14))
    headers = ["Hart", "Gelesen", "Reservation", "SC", "Speicher"]
    xs = [16, 160, 360, 620, 860]
    for x, h in zip(xs, headers):
        p.append(T(x, 52, h, 13, MUTED, "400"))
    rows = [
        ("0 LR", "0", "gesetzt", "-", "0"),
        ("1 LR", "0", "gesetzt", "-", "0"),
        ("0 SC", "0", "endet", "Status 0", "1"),
        ("1 SC", "0", "endet", "Status ungleich 0", "1"),
        ("1 LR neu", "1", "gesetzt", "kein SC", "1"),
        ("0 Release", "-", "keine", "-", "0"),
        ("1 LR/SC", "0", "endet", "Status 0", "1"),
    ]
    for i, row in enumerate(rows):
        y = 84 + i * 32
        for x, val in zip(xs, row):
            p.append(T(x, y, val, 15, C0 if "0" in row[0] else C1))
    p.append(T(16, 340, "Schlosswerte nur 0 oder 1. Status 0 ist Erfolg, ungleich 0 ist Fehlschlag ohne Store.", 15, ERR))
    p.append(T(16, 372, "Liest der neue LR 1, gibt es keinen SC. Nach Release 0 kann Hart 1 erneut erwerben.", 14))
    p.append(T(16, 404, "Ein SC darf auch ohne fremden Write scheitern. Keine Fairness je Hart.", 14))
    p.append(T(16, 436, "Beobachtete Geraetewrites auf die gelesenen Bytes duerfen nicht ignoriert werden.", 13, MUTED, "400"))
    p.append(T(16, 464, "Granule ist nicht automatisch eine 64-Byte-Line. Kritischer Abschnitt erst nach Status 0.", 13, MUTED, "400"))
    save("lrsc.svg", p)


def fig_i():
    p = svg(1200, 360)
    p.append(T(16, 20, "Lehrschloss fuer gewoehnlichen Shared Memory. Kein Cache-Flush als Ersatz.", 15))
    p.append(T(16, 52, "lr.w.aq  pruefen  sc.w  bei Erfolg 0", 16, C0))
    p.append(T(16, 84, "kritische Daten liegen zwischen Acquire und Release", 16, MEM))
    p.append(T(16, 116, "fence rw,w    dann sw zero auf das Schloss", 16, C1))
    p.append(T(16, 156, "Acquire begrenzt spaetere Zugriffe. Release begrenzt fruehere Schreibzugriffe.", 15))
    p.append(T(16, 188, "Daten plus Flag: der atomare Flag-Store allein publiziert die Daten nicht.", 15, ERR))
    p.append(T(16, 220, "Spinlock: nicht schlafen, nicht blockierend warten, nicht lang rechnen.", 15))
    p.append(T(16, 252, "ISR auf ein Schloss des unterbrochenen Kontexts: Selbstdeadlock.", 15, ERR))
    p.append(T(16, 284, "Timeout bricht das Schloss nicht sicher, solange der Besitzer noch schreibt.", 14))
    p.append(T(16, 316, "MMIO und Compiler-Barrieren sind andere Domaenen. Annahme: RVWMO, A-Extension.", 13, MUTED, "400"))
    p.append(T(16, 344, "Diese Sequenz ist hier nicht mit einer RISC-V-Toolchain assembliert.", 13, MUTED, "400"))
    save("lock.svg", p)


def fig_j():
    p = svg(1200, 380)
    p.append(T(16, 20, "Ohne explizites memory_order-Argument gilt seq_cst. Das serialisiert nicht das ganze Programm.", 14))
    p.append(T(16, 52, "Ziel kann AMO, LR/SC oder ein Library-Fallback sein. ABI und Typ entscheiden.", 15))
    p.append(T(16, 88, "amoadd.w: Speicher 10, Addend 3. Rd bekommt 10, Speicher wird 13.", 16, C0))
    p.append(T(16, 124, "Zwei Fetch-Adds um 1 ab 0: alte Werte 0 und 1, Ende 2.", 16, MEM))
    p.append(T(16, 160, "Relaxed genuegt fuer einen reinen Zaehler ohne weiteres publiziertes Datum.", 15))
    p.append(T(16, 192, "Ein ISR darf keinen blockierenden Lock-Fallback rufen. Das ist eine eigene Pruefung.", 15, ERR))
    p.append(T(16, 224, "Testidee: zwei Harts, je N Inkremente, Ende 2N. Breite ohne Ueberlauf.", 15))
    p.append(T(16, 256, "Der normale C-Zaehler ist ein Data Race, keine Messreferenz.", 15, ERR))
    p.append(T(16, 290, "AMO schuetzt eine Adresse in ihrer Domaene, nicht den Bus und nicht alle Daten.", 14))
    p.append(T(16, 322, "DMA nimmt nicht automatisch am C11-Happens-Before teil.", 14))
    p.append(T(16, 354, "Host-GCC ist kein Nachweis der RISC-V-Codegenerierung.", 13, MUTED, "400"))
    save("atomic.svg", p)


def fig_k():
    p = svg(1200, 320)
    p.append(T(16, 22, "Deadlock ist ein Wartezyklus. Starvation ist Warten ohne Zyklus. Livelock ist Betrieb ohne Fortschritt.", 14))
    p.append(R(16, 52, 520, 110, ERR))
    p.append(T(28, 78, "Zyklus", 15, ERR))
    p.append(T(28, 106, "Core0 haelt A, will B", 14))
    p.append(T(28, 132, "Core1 haelt B, will A", 14))
    p.append(R(580, 52, 560, 110, MEM))
    p.append(T(592, 78, "Ordnung A vor B", 15, MEM))
    p.append(T(592, 106, "beide erwerben A, dann B", 14))
    p.append(T(592, 132, "kein Zyklus", 14))
    p.append(T(16, 200, "Timeout allein stellt keinen gueltigen Datenzustand her.", 15, ERR))
    p.append(T(16, 232, "Frage: Die ISR spinnt auf ein Schloss, das der unterbrochene Kern haelt. Was folgt?", 15))
    p.append(T(16, 264, "Antwort in den Notizen: Selbstdeadlock. Atomics ersetzen keine Prioritaetsvererbung.", 14, MUTED, "400"))
    p.append(T(16, 296, "Das Schloss nicht blind freigeben, waehrend der Besitzer noch schreibt.", 14, MUTED, "400"))
    save("dead.svg", p)


def fig_l():
    p = svg(1200, 420)
    p.append(T(16, 22, "Analytisch, s=0,2, p=0,8, h=0. Keine Messung. Grenze 5.", 15))
    ns = [1, 2, 4, 8, 16, 100]
    ss = [1 / (0.2 + 0.8 / n) for n in ns]
    xs = [80, 200, 320, 460, 620, 980]
    def y_of(s):
        return 300 - (s / 5.5) * 240
    p.append(L(60, 300, 1100, 300, MUTED, 1))
    p.append(L(60, 40, 60, 300, MUTED, 1))
    p.append(L(60, y_of(5), 1100, y_of(5), ERR, 1.2))
    p.append(T(1110, y_of(5) + 4, "5", 12, ERR))
    pts = []
    for x, n, s in zip(xs, ns, ss):
        y = y_of(s)
        pts.append((x, y))
        p.append(R(x - 5, y - 5, 10, 10, C0, C0))
        p.append(T(x, 322, str(n), 12, MUTED, "400", "middle"))
        p.append(T(x, y - 12, f"{s:.2f}", 12, C0, "600", "middle"))
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        p.append(L(x1, y1, x2, y2, C0, 2))
    p.append(T(16, 360, "N auf der Achse ist nicht linear: 100 steht rechts, damit die Grenze sichtbar bleibt.", 14))
    p.append(T(16, 388, "T1=100 Zeiteinheiten: 20 seriell plus 80/N. T4=40, T100=20,8. Effizienz bei 100 etwa 4,81 Prozent.", 14, ERR))
    save("amdahl.svg", p)


def fig_v1():
    p = svg(1200, 360)
    p.append(T(16, 22, "Kohaerente Harts links. DMA nur mit Plattformvertrag in der Domaene.", 15))
    p.append(R(40, 70, 200, 70, C0))
    p.append(T(52, 100, "Hart 0", 16, C0))
    p.append(T(52, 124, "L1-D privat", 13, MUTED, "400"))
    p.append(R(40, 180, 200, 70, C1))
    p.append(T(52, 210, "Hart 1", 16, C1))
    p.append(T(52, 234, "L1-D privat", 13, MUTED, "400"))
    p.append(R(360, 120, 220, 80, BUS))
    p.append(T(372, 154, "Koordinator", 16, BUS))
    p.append(T(372, 178, "Snoop oder Directory", 13, MUTED, "400"))
    p.append(L(240, 105, 360, 150, C0, 2))
    p.append(L(240, 215, 360, 170, C1, 2))
    p.append(R(700, 120, 180, 80, MEM))
    p.append(T(712, 154, "Memory", 16, MEM))
    p.append(T(712, 178, "unterer Stand", 13, MUTED, "400"))
    p.append(L(580, 160, 700, 160, MEM, 2))
    p.append(R(960, 70, 200, 70, ERR))
    p.append(T(972, 100, "DMA", 16, ERR))
    p.append(T(972, 124, "Vertrag offen", 13, MUTED, "400"))
    p.append(L(1060, 140, 880, 160, ERR, 1.4))
    p.append(T(16, 290, "CPU-Kohaerenz, DMA-Maintenance, atomare RMW und MMIO-Ordnung sind verschiedene Pflichten.", 14))
    p.append(T(16, 322, "Gemeinsames L2 allein beweist die Domaene nicht. L1-I ist hier nicht der Datenpfad.", 14, MUTED, "400"))
    save("v_domain.svg", p)


def fig_v2():
    p = svg(1200, 400)
    p.append(T(16, 22, "data und ready sind _Atomic int, Start 0. Ein Schreiber, kein spaeterer Payloadwrite.", 14))
    p.append(R(16, 50, 560, 140, C0))
    p.append(T(28, 78, "Producer", 16, C0))
    p.append(T(28, 108, "data = 42 relaxed", 15))
    p.append(T(28, 136, "ready = 1 relaxed", 15))
    p.append(T(28, 168, "Programmreihenfolge, keine Sync-Kante", 13, ERR))
    p.append(R(620, 50, 540, 140, C1))
    p.append(T(632, 78, "Consumer relaxed", 16, C1))
    p.append(T(632, 108, "liest ready, dann data", 15))
    p.append(T(632, 136, "ready 1 und data 0 moeglich", 15, ERR))
    p.append(T(632, 168, "racefrei, aber nicht publiziert", 13, MUTED, "400"))
    p.append(R(16, 220, 1140, 100, MEM))
    p.append(T(28, 250, "Mit Ordnung: ready-Store release, ready-Load acquire liest genau diese 1.", 15, MEM))
    p.append(T(28, 282, "Dann ist data 42 sichtbar. Bei ready 0 die Daten nicht verwenden.", 15))
    p.append(T(16, 360, "Gewoehnliches non-atomic data plus relaxed Flag waere wieder ein Data Race.", 14, ERR))
    p.append(T(16, 388, "Kein gemessener RISC-V-Lauf. Schwache Ordnung erlaubt das Lehr-Outcome, erzwingt es nicht.", 13, MUTED, "400"))
    save("v_flag.svg", p)


def fig_v3():
    p = svg(1200, 280)
    p.append(T(16, 22, "Lehrline 64 B. int hier 4 B. Basis 0x20001000 ist ausgerichtet.", 14))
    p.append(R(16, 50, 520, 48, ERR))
    p.append(R(16, 50, 32, 48, C0))
    p.append(R(48, 50, 32, 48, C1))
    p.append(T(16, 130, "a[0] und a[1] liegen beide in 0x20001000-3F.", 14, ERR))
    p.append(R(620, 50, 250, 48, C0))
    p.append(R(900, 50, 250, 48, C1))
    p.append(T(620, 130, "Records bei +0 und +64: Lines 0x20001000 und 0x20001040.", 14, MEM))
    p.append(T(16, 180, "Sprachlich getrennte Variablen koennen trotzdem dieselbe Ownership teilen.", 15))
    p.append(T(16, 212, "Padding trennt Layout. Es ersetzt keine Atomizitaet eines gemeinsamen Zaehlers.", 15, ERR))
    p.append(T(16, 248, "Keine gemessene Verlangsamung. 64 Byte sind keine universelle Line.", 14, MUTED, "400"))
    save("v_stride.svg", p)


def fig_v4():
    p = svg(1200, 320)
    p.append(T(16, 22, "Hardwaremotiv, keine C11-Ergebnisliste. volatile aendert die Teilung nicht.", 14))
    p.append(T(16, 60, "Hart 0", 14, C0))
    p.append(T(120, 60, "liest 0", 15, C0))
    p.append(T(280, 60, "schreibt 1", 15, C0))
    p.append(T(480, 60, "Abschnitt", 15, ERR))
    p.append(T(16, 100, "Hart 1", 14, C1))
    p.append(T(120, 100, "liest 0", 15, C1))
    p.append(T(280, 100, "schreibt 1", 15, C1))
    p.append(T(480, 100, "Abschnitt", 15, ERR))
    p.append(T(16, 150, "Beide sind gleichzeitig im Abschnitt, weil Check und Set getrennt sind.", 15, ERR))
    p.append(R(16, 180, 1140, 70, MEM))
    p.append(T(28, 210, "Atomare Uebernahme: nur ein SC mit Status 0 betritt den Abschnitt.", 15, MEM))
    p.append(T(28, 236, "Der andere liest 1 und wartet bis zum Release auf 0.", 15, MEM))
    p.append(T(16, 290, "Das ist kein Zaehler-RMW. Der Schlosswert bleibt 0 oder 1.", 14, MUTED, "400"))
    save("v_check.svg", p)


def fig_v5():
    p = svg(1200, 260)
    p.append(T(16, 22, "Ein Hart. Die ISR unterbricht den Halter desselben Schlosses.", 15))
    steps = ["Haelt L", "IRQ", "ISR spinnt", "kein Resume", "kein Release"]
    for i, name in enumerate(steps):
        p.append(R(16 + i * 230, 60, 200, 44, ERR if i >= 2 else C0))
        p.append(T(28 + i * 230, 88, name, 14))
        if i < 4:
            p.append(L(216 + i * 230, 82, 246 + i * 230, 82, INK, 1.6))
    p.append(T(16, 150, "IRQ-Sperre auf diesem Hart haelt andere Harts nicht fern.", 15))
    p.append(T(16, 182, "Konzept: kurze Meldung, Arbeit spaeter. Keine konkrete RTOS-Funktion.", 15, MEM))
    p.append(T(16, 220, "Zusaetzliche Atomizitaet loest den Selbstdeadlock nicht. Timeout gibt L nicht frei.", 14, ERR))
    save("v_isr.svg", p)


def fig_v6():
    p = svg(1200, 360)
    p.append(T(16, 22, "Konzept-SoC. Behandelt, optional oder im Target nicht belegt.", 15))
    boxes = [
        (16, 50, "Harts", "behandelt als Idee", C0),
        (230, 50, "Cache/MESI", "Lehrmodell", BUS),
        (460, 50, "Memory", "behandelt", MEM),
        (690, 50, "DMA", "behandelt", C1),
        (920, 50, "UART SPI I2C", "behandelt", INK),
        (16, 160, "CLINT/PLIC", "Beispiel, nicht jeder SoC", MUTED),
        (360, 160, "Timer/PWM", "Lehrrechnung", C0),
        (680, 160, "RVV/NPU", "optional, nicht belegt", ERR),
    ]
    for x, y, a, b, col in boxes:
        p.append(R(x, y, 200, 70, col))
        p.append(T(x + 10, y + 30, a, 14, col))
        p.append(T(x + 10, y + 54, b, 12, MUTED, "400"))
    p.append(T(16, 270, "Ein Sample: Bus, Puffer, CPU-Rechnung, Completion. Interrupt meldet, DMA bewegt.", 15))
    p.append(T(16, 304, "OoO, kohaerentes SMP, RVV und NPU sind hier keine vorhandene Laborplattform.", 14, ERR))
    p.append(T(16, 338, "AMAT und PWM stehen auf den Wiederholungsfolien, nicht als Boardmessung.", 14, MUTED, "400"))
    save("v_soc.svg", p)


if __name__ == "__main__":
    s4 = 1 / (0.2 + 0.8 / 4)
    s100 = 1 / (0.2 + 0.8 / 100)
    assert abs(s4 - 2.5) < 1e-12
    assert abs(s100 - 4.807692307692) < 1e-9
    assert abs(s100 / 100 - 0.048076923) < 1e-9
    for fn in (fig_a, fig_b, fig_c, fig_d, fig_e, fig_f, fig_g, fig_h, fig_i, fig_j, fig_k, fig_l, fig_v1, fig_v2, fig_v3, fig_v4, fig_v5, fig_v6):
        fn()
    print("checks", round(s100, 4), round(100 * s100 / 100, 2))
