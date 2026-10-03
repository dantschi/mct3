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
    p = svg(1200, 380)
    p.append(T(16, 20, "LR setzt eine Reservation auf eine Granule, kein gehaltenes Mutex. SC-Erfolg liefert 0.", 14))
    headers = ["Hart", "Gelesen", "Reservation", "SC", "Speicher"]
    xs = [16, 160, 360, 620, 860]
    for x, h in zip(xs, headers):
        p.append(T(x, 52, h, 13, MUTED, "400"))
    rows = [
        ("0 LR", "0", "gesetzt", "-", "0"),
        ("1 LR", "0", "gesetzt", "-", "0"),
        ("0 SC", "0", "endet", "0", "1"),
        ("1 SC", "0", "ungueltig", "nicht 0", "1"),
        ("1 Retry", "1", "neu", "0", "2"),
    ]
    for i, row in enumerate(rows):
        y = 84 + i * 32
        for x, val in zip(xs, row):
            p.append(T(x, y, val, 15, C0 if "0" in row[0] else C1))
    p.append(T(16, 270, "Ein SC darf auch scheitern, wenn kein anderer Hart geschrieben hat.", 15, ERR))
    p.append(T(16, 300, "Interrupt, Kontextwechsel und fremder Store koennen die Reservation loeschen.", 14))
    p.append(T(16, 330, "DMA gehoert nur dazu, wenn die Plattform dieselbe Reservationsdomaene definiert.", 14))
    p.append(T(16, 360, "Constrained Loops haben Fortschritt unter Spec-Bedingungen, keine unbegrenzte Fairness.", 13, MUTED, "400"))
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
    p.append(T(16, 20, "atomic_fetch_add ist ohne Ordnung sequentially consistent. Das serialisiert nicht das ganze Programm.", 14))
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
    p = svg(1200, 360)
    p.append(T(16, 20, "Analytisch, fester Workload, kein Overhead. s=0,2 p=0,8.", 16))
    p.append(T(16, 52, "S(4) = 1/0,4 = 2,5", 18, C0))
    p.append(T(16, 84, "S(100) = 1/0,208 = 4,8077", 18, C1))
    p.append(T(16, 116, "Grenze 1/s = 5. Effizienz S(100)/100 = 4,81 Prozent.", 16, MEM))
    p.append(T(16, 156, "4,8 liegt nahe an 5. Die Parallel-Effizienz ist trotzdem sehr klein.", 15, ERR))
    p.append(T(16, 190, "Ideal ohne seriellen Anteil waere S(N)=N. Die Kurve ist keine Messung.", 15))
    p.append(T(16, 224, "Optional T(N)/T(1)=s+p/N+o(N). Ohne genannte o(N) bleibt der Overhead draussen.", 14))
    p.append(T(16, 258, "Eine groessere Aufgabe ist eine andere Frage und widerlegt Amdahl nicht.", 14))
    p.append(T(16, 292, "Annahmen: feste Arbeit, serieller Anteil der Ein-Kern-Zeit, ideale Balance.", 13, MUTED, "400"))
    p.append(T(16, 324, "Mehr DLP loest die Memory Wall nicht allein. Lokalitaet und Transfers bleiben.", 13, MUTED, "400"))
    save("amdahl.svg", p)


if __name__ == "__main__":
    s4 = 1 / (0.2 + 0.8 / 4)
    s100 = 1 / (0.2 + 0.8 / 100)
    assert abs(s4 - 2.5) < 1e-12
    assert abs(s100 - 4.807692307692) < 1e-9
    assert abs(s100 / 100 - 0.048076923) < 1e-9
    for fn in (fig_a, fig_b, fig_c, fig_d, fig_e, fig_f, fig_g, fig_h, fig_i, fig_j, fig_k, fig_l):
        fn()
    print("checks", round(s100, 4), round(100 * s100 / 100, 2))
