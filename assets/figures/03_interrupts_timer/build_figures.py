#!/usr/bin/env python3
"""Lehrfiguren VL03. Adressen und IDs sind das RV32-Referenzmodell, kein SoC-Datenblatt."""
from pathlib import Path
OUT = Path(__file__).resolve().parent
INK, MUTED = "#1D1D1F", "#5F6368"
LOCAL, EXT, HW, SW = "#E65100", "#1565C0", "#6A1B9A", "#1B5E20"

def svg(w, h):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">',
            f'<rect width="{w}" height="{h}" fill="#fff"/>',
            '<style>text{font-family:Arial,Helvetica,sans-serif;fill:#1D1D1F}</style>']

def T(x, y, s, size=16, fill=INK, anchor="start", w="600"):
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{w}" fill="{fill}" text-anchor="{anchor}">{s}</text>'

def box(x, y, w, h, stroke=INK, fill="#fff"):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{stroke}"/>'

def save(name, p):
    (OUT / name).write_text("\n".join(p) + "\n</svg>\n", encoding="utf-8")
    print(name)

def fig_poll():
    p = svg(1100, 320)
    p += [T(16, 22, "Modell. Ereignis bei 1,2 ms. Wartezeit bis dahin 0,8 ms.", 15, MUTED, w="400")]
    lanes = [
        (40, "Busy-Wait", "#FFEBEE", "CPU belegt bis 1,2 ms"),
        (110, "Periodisch", "#FFF3E0", "Fragen 0 / 1 / 2 ms"),
        (180, "Interrupt", "#E8F5E9", "Latenz, ISR, weiter Main"),
    ]
    for y, name, fill, cap in lanes:
        p += [box(16, y, 160, 52, INK, fill), T(28, y + 32, name, 16)]
        p += [box(200, y, 860, 52, INK, "#fff"), T(220, y + 32, cap, 16)]
    p += [T(200, 268, "Markierung Ereignis", 14, "#B71C1C")]
    p += [f'<line x1="520" y1="40" x2="520" y2="232" stroke="#B71C1C" stroke-width="2"/>']
    p += [T(16, 300, "0,8 ms ist die angenommene Zeit bis zum Ereignis, nicht die Interruptlatenz.", 15, MUTED, w="400")]
    save("poll-vs-irq.svg", p)

def fig_mtvec():
    p = svg(1100, 280)
    p += [T(16, 20, "BASE 0x80000100. Vectored-Registerwert 0x80000101.", 15)]
    labels = ["Exc", "d", "d", "MSI", "d", "d", "d", "MTI", "d", "d", "d", "MEI"]
    for i, lab in enumerate(labels):
        col = "#E8F5E9" if lab != "d" else "#F5F5F7"
        p += [box(16 + i * 88, 40, 80, 44, INK, col), T(24 + i * 88, 68, f"{i} {lab}", 13)]
    p += [T(16, 120, "Cause 3 -> +12 = 0x8000010C", 16)]
    p += [T(16, 150, "Cause 7 -> +28 = 0x8000011C", 16)]
    p += [T(16, 180, "Cause 11 -> +44 = 0x8000012C", 16)]
    p += [T(16, 220, "Abstand 4 Byte bleibt auch bei komprimierten Befehlen fest.", 16)]
    p += [T(16, 252, "Exceptionen gehen an BASE, nicht in einen Cause-Slot.", 16)]
    save("mtvec.svg", p)

def fig_levels():
    p = svg(1100, 300)
    p += [T(16, 22, "Lehr-Modell, ein Hart. Cause-Code und PLIC-ID sind verschiedene Zahlen.", 15, MUTED, w="400")]
    p += [box(16, 40, 320, 110, LOCAL, "#FFF3E0"), T(28, 68, "Lokal: mtime, mtimecmp, msip", 15, LOCAL)]
    p += [T(28, 96, "MSI Cause 3, MTI Cause 7", 16, LOCAL), T(28, 124, "CSRs im Hart: mip, mie, MIE", 15)]
    p += [box(360, 40, 360, 110, EXT, "#E3F2FD"), T(372, 68, "UART ID1, I2C ID2, GPIO ID3", 15, EXT)]
    p += [T(372, 96, "alle nach MEI, Cause 11", 16, EXT), T(372, 124, "Claim liefert die Geraete-ID", 15)]
    p += [box(750, 40, 320, 110, HW), T(762, 78, "ID 7 ist nicht Cause 7", 16, HW)]
    p += [T(762, 110, "Timer bleibt Cause 7", 15)]
    p += [T(16, 190, "Prioritaet der Kategorien im klassischen M-Mode: MEI vor MSI vor MTI.", 16)]
    p += [T(16, 220, "Der Timer ist nicht automatisch der hoechstpriore VIP.", 16)]
    p += [T(16, 250, "O(1) waehlt nur die Kategorie. Die ISR-Laufzeit bleibt workloadabhaengig.", 15, MUTED, w="400")]
    p += [T(16, 280, "Lokal heisst dem Hart zugeordnet, nicht automatisch kuerzere Leitung.", 15, MUTED, w="400")]
    save("two-levels.svg", p)

def fig_trap():
    p = svg(1100, 240)
    p += [T(16, 22, "Einfacher M-Mode-Trap. Hardware rettet nicht alle Register.", 15, MUTED, w="400")]
    p += [T(16, 58, "Vorher: Main-PC, MIE=1", 16)]
    p += [T(16, 90, "Hardware: mepc=Ruecksprung-PC, mcause=Ursache, MPIE=altes MIE, MIE=0, MPP=alter Modus", 15)]
    p += [T(16, 124, "Software: Prolog auf dem Stack, Handler, Epilog", 16, SW)]
    p += [T(16, 158, "mret: PC aus mepc, MIE aus MPIE, Privileg aus MPP", 16, HW)]
    p += [T(16, 198, "MIE=0 sperrt die betrachteten maskierbaren M-Interrupts, keine synchronen Exceptions.", 15)]
    p += [T(16, 226, "Ein BUTTON-Vergleich ohne Interrupt-Bit und ohne Claim-ID trifft weder Cause noch Geraet.", 14, MUTED, w="400")]
    save("trap-state.svg", p)

def fig_timer():
    p = svg(1100, 250)
    p += [T(16, 20, "mtime steigt, mtimecmp ist die Deadline. MTIP, sobald mtime >= mtimecmp.", 16)]
    p += [T(16, 56, "Pending allein reicht nicht. Zusaetzlich MTIE und, im M-Mode, MIE.", 16, LOCAL)]
    p += [T(16, 96, "Deadline offen | erreicht, MTIE=0 | erreicht, MIE=0 | beide an | Compare in der Zukunft", 15)]
    p += [T(16, 136, "mret quittiert den Timer nicht. Ein ueberfaelliger Vergleich kann erneut trappen.", 16)]
    p += [T(16, 176, "MTIP faellt nach dem Schreiben nicht garantiert sofort. Kein Busy-Wait auf MTIP.", 15)]
    p += [T(16, 216, "Reihenfolge: Stack und mtvec, Zeit lesen, Compare setzen, MTIE, dann MIE.", 16, SW)]
    save("timer-gates.svg", p)

def fig_hilo():
    p = svg(1100, 250)
    p += [T(16, 20, "RV32, zwei 32-Bit-Haelften. Kein einzelner atomarer 64-Bit-Load.", 15, MUTED, w="400")]
    p += [T(16, 56, "Vorher 0x00000001_FFFFFFFF, nachher 0x00000002_00000000", 16)]
    p += [T(16, 90, "HI=1 vor dem Uebergang und LO=0 danach ergibt faelschlich 0x00000001_00000000", 16, "#B71C1C")]
    p += [T(16, 130, "Lesen: HI, LO, HI noch einmal. Nur gleiche HI-Werte akzeptieren.", 16, SW)]
    p += [T(16, 170, "Compare schreiben, Little Endian: LO=0xFFFFFFFF, dann HI, dann neues LO.", 16, LOCAL)]
    p += [T(16, 210, "32-Bit-Ticks bei 1 MHz: ca. 71,6 min. 32-Bit-Millisekunden: ca. 49,7 Tage.", 15, MUTED, w="400")]
    save("hi-lo.svg", p)

def fig_drift():
    p = svg(1100, 250)
    p += [T(16, 20, "Timer 10 MHz: 10000 Ticks/ms. CPU 100 MHz: 100000 Zyklen/ms.", 16)]
    p += [T(16, 58, "Soll 10,0 ms, ISR bei 10,2 ms. now+1 ms ergibt 11,2 ms statt Phase 11,0 ms.", 16, LOCAL)]
    p += [T(16, 100, "Ueberlast: naechste Sollzeit 10 ms, Service bei 15,3 ms, Periode 1 ms.", 16)]
    p += [T(16, 136, "k = floor((15,3-10)/1)+1 = 6 faellige Deadlines. Naechste Zukunft: 16 ms.", 16, SW)]
    p += [T(16, 176, "Ein Pending-Bit zaehlt nicht alle vergangenen Perioden.", 16)]
    p += [T(16, 210, "Optional: 500 Zyklen bei 100 MHz = 5 us, bei 1 kHz = 0,5 Prozent. Nur Modell.", 15, MUTED, w="400")]
    save("tick-drift.svg", p)

def fig_plic():
    p = svg(1100, 240)
    p += [T(16, 20, "Kontext 0, Threshold 5. Benachrichtigung nur bei Prioritaet strikt groesser 5.", 15, MUTED, w="400")]
    p += [T(16, 56, "ID1 Prio 3 pending enabled: keine Meldung", 16, MUTED)]
    p += [T(16, 90, "ID2 Prio 7 und ID3 Prio 7: ID2 gewinnt, kleinere ID", 16, EXT)]
    p += [T(16, 130, "Claim liest ID2 und loescht ihr PLIC-Pending. Threshold filtert Claim nicht.", 16)]
    p += [T(16, 170, "Kontext ist Hart plus Privileg, nicht einfach der Kern. Nummern sind Lehrwerte.", 15)]
    p += [T(16, 210, "Ein Pending-Bit ist keine unbegrenzte Ereigniswarteschlange.", 16, HW)]
    save("plic-table.svg", p)

def fig_claim():
    p = svg(1100, 250)
    p += [T(16, 20, "Geraet, PLIC, Hart. Claim ist nicht die Quittung im UART.", 15, MUTED, w="400")]
    p += [T(16, 56, "1 Quelle aktiv  2 Pending  3 MEI Cause 11  4 Claim liest ID", 16, EXT)]
    p += [T(16, 96, "5 Geraetursache loeschen  6 dieselbe ID als Complete schreiben", 16, SW)]
    p += [T(16, 136, "ID 0: kein Tabellenzugriff und kein Complete.", 16, "#B71C1C")]
    p += [T(16, 176, "Level bleibt aktiv: nach Complete erneut Pending. Sonst bleibt es aus.", 16)]
    p += [T(16, 214, "Zwei Harts: eine Quelle wird einmal geclaimt. Der andere Hart liest 0, wenn nichts bleibt.", 15)]
    save("claim.svg", p)

def fig_nest():
    p = svg(1100, 250)
    p += [T(16, 20, "Konzeptionell, keine gepruefte sichere ISR-Vorlage.", 15, "#B71C1C")]
    p += [T(16, 56, "Main, aeussere ISR, innere ISR, zurueck, Main. Je ein Frame und ein Ruecksprung-PC.", 16)]
    p += [T(16, 100, "Fehler: einziges mepc ueberschrieben. t0/t1 im alten Prolog verloren.", 16, "#B71C1C")]
    p += [T(16, 140, "Ein Frame rettet benutzte GPRs, noetige CSRs und geaenderte Masken.", 16, SW)]
    p += [T(16, 176, "ILP32: Stack 16-Byte-ausgerichtet, sobald C aufgerufen wird. 8 Byte genuegen nicht.", 16)]
    p += [T(16, 214, "MIE=1 erlaubt nicht nur hoeherpriore Quellen. Externe Quellen extra maskieren.", 15, MUTED, w="400")]
    save("nesting.svg", p)

def fig_ipi():
    p = svg(1100, 200)
    p += [T(16, 22, "Zwei Harts. msip ist ein Pending-Bit, keine Nachrichtenwarteschlange.", 15, MUTED, w="400")]
    p += [box(16, 50, 220, 60, LOCAL), T(28, 86, "Hart A schreibt", 16, LOCAL)]
    p += [box(280, 50, 260, 60, HW), T(292, 86, "msip von Hart B = 1", 16, HW)]
    p += [box(580, 50, 480, 60, SW), T(592, 86, "Hart B: MSI Cause 3, dann msip=0", 16, SW)]
    p += [T(16, 150, "Die Nutzdaten liegen in einer eigenen Shared-Memory-Struktur mit passender Ordnung.", 16)]
    p += [T(16, 182, "MSI ist nicht automatisch niedriger als der Timer. Kategorien: MEI, MSI, MTI.", 15)]
    save("ipi.svg", p)

def fig_fg():
    p = svg(1100, 220)
    p += [T(16, 22, "Timer-ISR aktualisiert kurz. Main liest einen Snapshot und prueft die LED-Deadline.", 16)]
    p += [T(16, 64, "last=0xFFFFFFF0, now=0x00000020, uint32_t(now-last)=48", 18, SW)]
    p += [T(16, 104, "Nur gueltig, wenn kein voller Zaehlerumlauf zwischen den Vergleichen liegt.", 15)]
    p += [T(16, 144, "volatile erzwingt im Modell die Zugriffe. Es ist kein atomares RMW und kein SMP-Schloss.", 16)]
    p += [T(16, 184, "Renode-Zeit ist virtuell. PerformanceInMips ist keine Zyklen- oder Latenzgarantie.", 15, MUTED, w="400")]
    save("foreground.svg", p)

if __name__ == "__main__":
    fig_poll(); fig_levels(); fig_mtvec(); fig_trap(); fig_timer()
    fig_hilo(); fig_drift(); fig_plic(); fig_claim(); fig_nest(); fig_ipi(); fig_fg()
