#!/usr/bin/env python3
"""Lehrfiguren VL06. Adressen sind fiktiv. Cachezeile 64 B ist nur ein Beispiel."""
from pathlib import Path

OUT = Path(__file__).resolve().parent
INK, MUTED = "#1D1D1F", "#5F6368"
CPU, DMA, IRQ, OK, ERR = "#1565C0", "#E65100", "#6A1B9A", "#1B5E20", "#B71C1C"


def svg(w, h):
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">',
        f'<rect width="{w}" height="{h}" fill="#fff"/>',
        "<style>text{font-family:Arial,Helvetica,sans-serif;fill:#1D1D1F}</style>",
    ]


def T(x, y, s, size=16, fill=INK, w="600", anchor="start"):
    s = str(s).replace("&", "&amp;").replace("<", "&lt;")
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


def rect(x, y, w, h, stroke=INK, fill="#fff", sw=1.6):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2" fill="{fill}" '
        f'stroke="{stroke}" stroke-width="{sw}"/>'
    )


def save(name, parts):
    (OUT / name).write_text("\n".join(parts) + "\n</svg>\n", encoding="utf-8")
    print(name)


def box(p, x, y, w, h, title, sub, stroke):
    p.append(rect(x, y, w, h, stroke))
    p.append(T(x + 8, y + 20, title, 14, stroke))
    if sub:
        p.append(T(x + 8, y + 38, sub, 12, MUTED, "400"))


def arrow(x1, y, x2, stroke=INK):
    return line(x1, y, x2, y, stroke, 2)


# 1 Bandbreite
def fig_budget():
    p = svg(1200, 430)
    p.append(T(16, 24, "Engpass liegt auf der SPI-Leitung, nicht nur in der CPU.", 18))
    p.append(T(16, 46, "Ein Frame RGB565: 320 x 240 x 2 = 153600 Byte. 60 FPS: 9,216 MB/s = 73,728 Mbit/s.", 14, MUTED, "400"))
    nodes = [
        (16, "Bildpuffer", "153600 B"),
        (210, "Speicherbus", "geteilt"),
        (400, "DMA oder CPU", "Nachfuellen"),
        (610, "SPI-TX", "Register/FIFO"),
        (820, "Leitung", "1 Bit/SCK"),
        (1010, "Display", "Geraet"),
    ]
    for x, a, b in nodes:
        box(p, x, 64, 170, 52, a, b, DMA if a == "Leitung" else CPU)
    for x in (186, 376, 586, 796, 990):
        p.append(arrow(x, 90, x + 22, INK))
    rows = [
        ("Anforderung 60 FPS", "9,216 MB/s", ERR),
        ("SPI 10 MHz ideal", "1,25 MB/s, etwa 8,14 FPS", DMA),
        ("SPI 50 MHz ideal", "6,25 MB/s, etwa 40,69 FPS", OK),
        ("60 FPS, 1 Bit/SCK", "mindestens 73,728 MHz", ERR),
    ]
    y = 150
    for name, val, col in rows:
        p.append(rect(16, y, 560, 36, col))
        p.append(T(28, y + 24, name, 15, col))
        p.append(T(300, y + 24, val, 15))
        y += 44
    p.append(rect(610, 150, 560, 168, MUTED))
    p.append(T(624, 176, "Wenn die Leitung nicht reicht:", 15))
    p.append(T(624, 204, "geringere Bildrate", 16, DMA))
    p.append(T(624, 232, "Teilupdates statt Vollbild", 16, DMA))
    p.append(T(624, 260, "oder eine breitere Schnittstelle", 16, DMA))
    p.append(T(624, 296, "Kommandos und Pausen senken den Durchsatz weiter.", 13, MUTED, "400"))
    p.append(T(16, 400, "Audio getrennt: 44100 Samples/s mono, 16 Bit = 88200 Byte/s. Samples allein sind keine Byte-Rate.", 14, MUTED, "400"))
    p.append(T(16, 422, "DMA kuerzt Nachfuellpausen. Es hebt das SCK-Limit nicht auf. MB hier dezimal.", 14, IRQ))
    save("budget.svg", p)


# 2 Zeitspuren
def fig_time():
    p = svg(1200, 460)
    p.append(T(16, 24, "Dieselbe Leitung, vier CPU-Spuren. 10 MHz SPI: ein Byte ideal 0,8 us.", 17))
    p.append(T(16, 46, "1 000 000 Byte mindestens 0,8 s reine Leitungszeit. Ausschnitt, nicht massstaeblich.", 14, MUTED, "400"))
    lanes = ["Polling", "IRQ/Byte", "IRQ/16 B", "DMA"]
    # segments: (start, width, color, label) in a 0..100 scale
    patterns = [
        [(0, 100, ERR, "Hauptschleife wartet")],
        [(0, 8, IRQ, "ISR"), (12, 18, CPU, "Nutz"), (34, 8, IRQ, "ISR"), (46, 18, CPU, "Nutz"), (68, 8, IRQ, "ISR"), (80, 16, CPU, "Nutz")],
        [(0, 10, IRQ, "ISR"), (14, 70, CPU, "Nutzarbeit"), (88, 10, IRQ, "ISR")],
        [(0, 12, DMA, "Setup"), (14, 74, CPU, "Main rechnet"), (90, 8, IRQ, "TC")],
    ]
    y0 = 70
    for i, (name, segs) in enumerate(zip(lanes, patterns)):
        y = y0 + i * 62
        p.append(T(16, y + 22, name, 14, INK))
        p.append(rect(130, y, 900, 28, MUTED, "#fff", 1))
        for a, w, col, lab in segs:
            p.append(rect(130 + a * 9, y + 2, w * 9 - 2, 24, col, col, 0))
            if w > 12:
                p.append(T(134 + a * 9, y + 19, lab, 12, "#fff", "400"))
    p.append(T(130, 330, "Leitung: Bytes ohne Pause    | Luecke = Software-Nachfuellpause, nur bei IRQ/Polling moeglich", 14, DMA))
    p.append(line(130, 348, 980, 348, DMA, 3))
    p.append(line(430, 340, 520, 340, ERR, 6))
    p.append(T(430, 372, "Pause", 13, ERR))
    p.append(T(16, 404, "Modell: 100-MHz-CPU, 100 Zyklen je Byte-IRQ. 1,25 Mio IRQ/s waeren 125 Prozent. Nicht erreichbar.", 14, ERR))
    p.append(T(16, 430, "16 Byte je IRQ: derselbe feste Aufwand etwa 7,81 Prozent. Kopieren kommt dazu. Keine Messung.", 14, MUTED, "400"))
    p.append(T(16, 452, "Polling beschaeftigt die aufrufende Schleife. Aktivierte Interrupts koennen weiterlaufen.", 14, MUTED, "400"))
    save("timelines.svg", p)


# 3 Pfade
def fig_paths():
    p = svg(1200, 420)
    p.append(T(16, 24, "CPU und DMAC sind Initiatoren. RAM und Peripherieregister sind Ziele.", 17))
    box(p, 20, 56, 150, 50, "CPU", "Initiator", CPU)
    box(p, 200, 56, 150, 50, "D-Cache", "optional", IRQ)
    box(p, 390, 56, 160, 50, "Interconnect", "CPU gegen DMA", ERR)
    box(p, 590, 56, 140, 50, "RAM", "Ziel", OK)
    box(p, 20, 140, 150, 50, "DMAC", "Initiator", DMA)
    box(p, 200, 140, 160, 50, "Kanal-Arbiter", "im DMAC", DMA)
    box(p, 390, 140, 160, 50, "SPI / UART", "MMIO-Ziel", MUTED)
    p.append(arrow(170, 80, 198, CPU))
    p.append(arrow(350, 80, 388, CPU))
    p.append(arrow(550, 80, 588, CPU))
    p.append(arrow(170, 164, 198, DMA))
    p.append(line(360, 164, 470, 90, DMA, 2))
    p.append(T(16, 220, "DMAMUX routet Requests. Kanaele sind Kontexte, nicht automatisch eigene Datenpfade.", 15))
    p.append(rect(16, 240, 560, 70, CPU))
    p.append(T(28, 266, "CPU-Arbeit mit Cache-Hits", 15, CPU))
    p.append(T(28, 290, "DMA stoert den Speicherbus seltener.", 14, MUTED, "400"))
    p.append(rect(600, 240, 560, 70, ERR))
    p.append(T(612, 266, "CPU-Arbeit mit vielen RAM-Zugriffen", 15, ERR))
    p.append(T(612, 290, "Dieselbe DMA-Last verzoegert deutlich staerker.", 14, MUTED, "400"))
    p.append(T(16, 340, "Round-Robin, angenommen: CPU, DMA, CPU, DMA. Feste Prioritaet: DMA, DMA, CPU.", 15, IRQ))
    p.append(T(16, 368, "Nicht: DMA gewinnt immer. Nicht: Stalls sind immer kurz.", 15, ERR))
    p.append(T(16, 400, "Setup, Cache-Wartung und Abschluss kosten Zeit. Bei kleinen Kopien kann die CPU guenstiger sein.", 14, MUTED, "400"))
    save("paths.svg", p)


# 4 Handshake
def fig_hand():
    p = svg(1200, 400)
    p.append(T(16, 24, "Speicher-Burst und Peripherie-Transfer sind zwei Breiten. DREQ/DACK sind Lehrnamen.", 16))
    steps = [
        (16, "RAM-Burst", "mehrere Bytes", CPU),
        (230, "DMAC-FIFO", "wenn vorhanden", DMA),
        (450, "ein Zugriff", "nur wenn bereit", IRQ),
        (680, "UART/SPI-FIFO", "wenn vorhanden", OK),
        (920, "Schiebereg.", "Leitung", ERR),
    ]
    for x, a, b, c in steps:
        box(p, x, 50, 190, 52, a, b, c)
    for x in (206, 426, 656, 896):
        p.append(arrow(x, 76, x + 22))
    p.append(T(16, 140, "Request", 14, IRQ))
    p.append(T(16, 180, "Zugriff", 14, DMA))
    p.append(T(16, 220, "FIFO", 14, OK))
    # request pulses
    xs = [120, 280, 440, 600, 760]
    for i, x in enumerate(xs):
        p.append(line(x, 150, x + 40, 150, IRQ, 3))
        p.append(line(x + 20, 128, x + 20, 150, IRQ, 2))
        if i < 4:
            p.append(rect(x + 8, 164, 24, 16, DMA, DMA, 0))
    p.append(T(120, 250, "Ein Request erlaubt nicht 16 Words in ein Ein-Byte-TX-Register.", 15, ERR))
    p.append(T(16, 290, "M2P: RAM -> Peripherie.   P2M: Peripherie -> RAM.   M2M: RAM -> RAM.", 16))
    p.append(T(16, 322, "P2M verhindert einen Overrun nicht, wenn der Pfad langsamer ist als die Quelle.", 15, ERR))
    p.append(T(16, 354, "M2M ist kein allgemeines memmove fuer Ueberlappung. DACK ist kein I2C-ACK.", 15, MUTED, "400"))
    p.append(T(16, 386, "Die zwei FIFOs nur zeichnen, wenn das konkrete Modell sie hat.", 14, MUTED, "400"))
    save("handshake.svg", p)


# 5 Adressen
def fig_addr():
    p = svg(1200, 460)
    p.append(T(16, 22, "M2P, fiktiv: 8 Bit, COUNT 16, SRC ab 0x20001000, DST fest 0x4003000C.", 16))
    headers = ["n", "SRC", "DST", "Rest"]
    xs = [16, 80, 280, 520]
    for x, h in zip(xs, headers):
        p.append(T(x, 52, h, 14, MUTED, "400"))
    rows = [
        ("1", "0x20001000", "0x4003000C", "15"),
        ("2", "0x20001001", "0x4003000C", "14"),
        ("3", "0x20001002", "0x4003000C", "13"),
        ("4", "0x20001003", "0x4003000C", "12"),
    ]
    for i, row in enumerate(rows):
        y = 78 + i * 28
        for x, val in zip(xs, row):
            col = ERR if x == 280 else INK
            p.append(T(x, y, val, 16, col))
    p.append(T(620, 78, "P2M, halfwordfaehig angenommen", 15, OK))
    p.append(T(620, 106, "ADC 0x40031000, fest", 15))
    p.append(T(620, 134, "RAM ab 0x20002000, +2", 15))
    p.append(T(620, 162, "COUNT 8 = 16 Byte", 15, DMA))
    p.append(T(16, 210, "Ein 16-Bit-I2C-Wert kann zwei Byte-Transfers sein. C-Typ und erlaubte Breite sind verschieden.", 15, ERR))
    p.append(T(16, 242, "1 000 000 Byte, 8 Bit, COUNT max. 65535: 15 x 65535 + 16975 = 16 Bloecke.", 16, CPU))
    p.append(T(16, 274, "Adressregister in Bytes zaehlen. uint16_t* p; p += width skaliert doppelt.", 15, IRQ))
    p.append(T(16, 310, "Getrennt: Bus-Alignment, Cacheline-Alignment, DMA-Erreichbarkeit.", 15))
    p.append(T(16, 342, "Ziel-Increment auf MMIO kann Nachbarregister beschreiben.", 15, ERR))
    p.append(T(16, 380, "uint32_t-Cast ist nur eine Adressannahme. uintptr_t macht aus einer CPU-Adresse keine DMA-Adresse.", 14, MUTED, "400"))
    p.append(T(16, 420, "Alle Adressen in dieser Abbildung sind fiktives Lehrmodell.", 14, MUTED, "400"))
    p.append(T(16, 446, "Packing nur, wenn Quelle, Ziel und Controller es dokumentieren.", 14, MUTED, "400"))
    save("addrs.svg", p)


# 6 Lebenszyklus
def fig_life():
    p = svg(1200, 420)
    p.append(T(16, 24, "Besitz des Puffers und Abschluss der Leitung sind zwei Zeitachsen.", 17))
    states = [
        (16, "CPU fuellt", OK),
        (210, "veroeffentlicht", CPU),
        (420, "DMA besitzt", DMA),
        (630, "DMA-TC", IRQ),
        (820, "CPU darf wieder", OK),
    ]
    for x, name, col in states:
        box(p, x, 48, 180, 40, name, "", col)
    for x in (196, 406, 616, 806):
        p.append(arrow(x, 68, x + 12))
    p.append(T(16, 120, "Waehrend DMA besitzt: CPU aendert den aktiven Quellbereich nicht.", 15, ERR))
    p.append(T(16, 146, "Ein lokales Array darf nach Rueckkehr der Startfunktion nicht verschwinden.", 15, ERR))
    p.append(T(16, 190, "DMA schreibt letztes Element", 14, DMA))
    p.append(T(16, 230, "DMA-TC", 14, IRQ))
    p.append(T(16, 270, "UART/SPI sendet", 14, CPU))
    p.append(T(16, 310, "Leitung fertig", 14, OK))
    marks = [(200, 178, DMA), (360, 218, IRQ), (560, 258, CPU), (760, 298, OK)]
    p.append(line(180, 330, 1000, 330, MUTED, 1))
    for x, y, col in marks:
        p.append(line(x, y, x, 330, col, 2))
        p.append(rect(x - 6, y - 6, 12, 12, col, col, 0))
    p.append(T(180, 360, "Abstand nicht festgelegt. Ohne Controllerdokument keine feste Differenz.", 14, MUTED, "400"))
    p.append(T(16, 390, "Pufferfreigabe, naechster DMA-Start und SPI-CS sind getrennte Entscheidungen.", 15, ERR))
    p.append(T(16, 414, "Vor Start: Kanal stoppen, Altstatus, Route, Breite, Count, Cache, IRQ. Kein blindes |=.", 14, MUTED, "400"))
    save("lifecycle.svg", p)


# 7 Cache
def fig_cache():
    p = svg(1200, 460)
    p.append(T(16, 24, "Nicht kohaerenter Write-Back-D-Cache. Werte beispielhaft. Linie hier 64 Byte, nur illustrativ.", 15))
    p.append(T(16, 70, "TX", 16, DMA))
    tx = [("Cache 0x22, RAM 0x11", ERR), ("Clean: RAM wird 0x22", CPU), ("DMA liest 0x22", OK)]
    for i, (t, c) in enumerate(tx):
        box(p, 70 + i * 300, 48, 270, 40, t, "", c)
    p.append(T(16, 150, "RX", 16, CPU))
    rx = [("Cache alt, RAM neu", ERR), ("schmutzige Line kann zurueckschreiben", ERR), ("danach CPU liest neu", OK)]
    for i, (t, c) in enumerate(rx):
        box(p, 70 + i * 300, 128, 270, 44, t, "", c)
    p.append(rect(16, 200, 560, 90, OK))
    p.append(T(28, 224, "Puffer auf ganzen Linien isoliert", 15, OK))
    p.append(T(28, 250, "[ DMA-Daten | DMA-Daten ]", 16))
    p.append(T(28, 274, "CPU-Metadaten liegen daneben, nicht in derselben Linie.", 13, MUTED, "400"))
    p.append(rect(600, 200, 560, 90, ERR))
    p.append(T(612, 224, "Fehler: Metadaten in der DMA-Linie", 15, ERR))
    p.append(T(612, 250, "[ Laenge | DMA-Byte | Flags ]", 16))
    p.append(T(612, 274, "Clean oder Invalidate trifft dann fremde Bytes.", 13, MUTED, "400"))
    p.append(T(16, 320, "prepare_tx_for_device: neu veroeffentlichen, bevor DMA liest.", 15, DMA))
    p.append(T(16, 346, "prepare_rx_for_device: schmutzige Kopie entfernen, bevor das Geraet schreibt.", 15, CPU))
    p.append(T(16, 372, "finish_rx_for_cpu: veraltete Kopie verwerfen, bevor die CPU liest.", 15, OK))
    p.append(T(16, 404, "Clean schreibt zurueck. Invalidate verwirft. Flush = Clean plus Invalidate. FENCE ersetzt das nicht.", 14, MUTED, "400"))
    p.append(T(16, 432, "Auch andere nicht kohaerente Modi koennen beim Empfang alte Kopien liefern. Zicbom nur wenn vorhanden.", 14, MUTED, "400"))
    save("cache.svg", p)


# 8 Uncached
def fig_uncached():
    p = svg(1200, 400)
    p.append(T(16, 24, "Drei Ebenen. Ein Linkername macht Speicher nicht uncached.", 18))
    layers = [
        (16, "1 Plattform", "Attribute setzen", "PMA, nicht PMP", CPU),
        (310, "2 Linker", "Puffer platzieren", ".dma_buffer", DMA),
        (610, "3 Anwendung", "Adresse uebergeben", "DMA-erreichbar", OK),
    ]
    for x, a, b, c, col in layers:
        box(p, x, 56, 270, 78, a, b + " / " + c, col)
    p.append(T(16, 170, "Fiktive Karte: 246 KiB ab 0x20000000, 10 KiB ab 0x2003D800, Ende exklusiv 0x20040000.", 15))
    p.append(rect(16, 190, 760, 28, MUTED, "#E8EEF2"))
    p.append(rect(16, 190, 620, 28, CPU, "#D6E6F5", 1))
    p.append(rect(636, 190, 140, 28, DMA, "#F8E0CC", 1))
    p.append(T(24, 210, "0x20000000  gewoehnlich", 13, CPU))
    p.append(T(646, 210, "DMA-Zone", 13, DMA))
    p.append(T(16, 250, "Uncached nur, wenn die Plattform das fuer 0x2003D800 wirklich konfiguriert.", 15, ERR))
    rows = [("PMP", "Zugriffsrechte", CPU), ("PMA / Plattform", "unter anderem Cacheability", DMA), ("Linker", "nur Platzierung", MUTED)]
    y = 280
    for a, b, c in rows:
        p.append(T(16, y, a, 16, c))
        p.append(T(220, y, b, 16))
        y += 28
    p.append(T(16, 376, "Uncached heisst weder automatisch DMA-erreichbar noch automatisch geordnet.", 14, MUTED, "400"))
    save("uncached.svg", p)


# 9 Burst DRAM
def fig_burst():
    p = svg(1200, 440)
    p.append(T(16, 24, "SoC-Transaktionen und DRAM-Kommandos sind zwei Ebenen.", 17))
    p.append(T(16, 52, "Bus, angenommen: Einzelbeats brauchen je eine Anfrage. Burst buendelt Beats.", 14, MUTED, "400"))
    p.append(T(16, 90, "einzeln", 14, CPU))
    for i in range(6):
        p.append(rect(120 + i * 70, 70, 28, 22, CPU, CPU, 0))
        p.append(rect(150 + i * 70, 70, 28, 22, MUTED, "#fff"))
    p.append(T(16, 140, "Burst", 14, DMA))
    p.append(rect(120, 120, 40, 22, IRQ, IRQ, 0))
    for i in range(6):
        p.append(rect(170 + i * 36, 120, 30, 22, DMA, DMA, 0))
    p.append(T(560, 110, "dunkle Kaestchen: Adressphase. Helle: Warten der CPU.", 13, MUTED, "400"))
    p.append(T(16, 180, "DRAM, Open-Page, dieselbe zunaechst geschlossene Zeile:", 15))
    p.append(T(16, 210, "ACT", 16, ERR))
    p.append(rect(80, 192, 50, 24, ERR, ERR, 0))
    for i, name in enumerate(("RD", "RD", "RD", "RD")):
        p.append(rect(150 + i * 60, 192, 48, 24, OK, OK, 0))
        p.append(T(158 + i * 60, 210, name, 13, "#fff"))
    p.append(T(400, 210, "Row-Hits auch bei getrennten SoC-Zugriffen", 14, OK))
    p.append(T(16, 260, "Zeilenwechsel: RD, PRE, ACT, RD. Offene passende Zeile: kein neues ACT.", 15, IRQ))
    p.append(T(16, 300, "Nicht: 16 Einzeltransfers bedeuten 16 Row-Aktivierungen.", 16, ERR))
    p.append(T(16, 334, "Vergleichen: Protokollaufwand, raeumliche Lokalitaet, CPU-Wartezeit. Keine feste Beschleunigung.", 15))
    p.append(T(16, 368, "Laengere Busbelegung ist der Preis des Bursts. Arbitration je Beat ist nur eine angenommene Politik.", 14, MUTED, "400"))
    p.append(T(16, 400, "On-Chip-SRAM hat keine DRAM-Zeile. Der Bezug auf Vorlesung 1 gilt nur fuer DRAM.", 14, MUTED, "400"))
    p.append(T(16, 428, "Eine DMA-Laenge ist nicht automatisch die DRAM-Burstlaenge.", 14, MUTED, "400"))
    save("burst.svg", p)


# 10 Ping-pong
def fig_ping():
    p = svg(1200, 430)
    p.append(T(16, 22, "44100 Hz, mono, 16 Bit: 88200 Byte/s. Puffer 4096 B, Haelften 2048 B = 1024 Samples.", 15))
    p.append(T(16, 46, "16-Bit-COUNT 2048. HT nach 1024 Elementen. Eine Haelfte ideal etwa 23,22 ms, Runde 46,44 ms.", 14, MUTED, "400"))
    p.append(T(16, 78, "DMA", 14, DMA))
    p.append(rect(120, 58, 300, 26, DMA, DMA, 0))
    p.append(T(230, 76, "A", 14, "#fff", "700", "middle"))
    p.append(rect(420, 58, 300, 26, IRQ, IRQ, 0))
    p.append(T(540, 76, "B", 14, "#fff", "700", "middle"))
    p.append(rect(720, 58, 300, 26, DMA, DMA, 0))
    p.append(T(860, 76, "A", 14, "#fff", "700", "middle"))
    p.append(T(16, 130, "CPU", 14, CPU))
    p.append(rect(420, 110, 300, 26, OK, "#E5F2E6"))
    p.append(T(500, 128, "bearbeitet A", 14, OK))
    p.append(rect(720, 110, 300, 26, OK, "#E5F2E6"))
    p.append(T(800, 128, "bearbeitet B", 14, OK))
    p.append(T(250, 168, "HT", 13, IRQ, "700", "middle"))
    p.append(T(560, 168, "TC", 13, IRQ, "700", "middle"))
    p.append(line(420, 58, 420, 150, IRQ, 1, "4 3"))
    p.append(line(720, 58, 720, 150, IRQ, 1, "4 3"))
    p.append(T(16, 210, "Beide Haelften vor dem Start vorbereiten. Danach nur die freigegebene Haelfte anfassen.", 15))
    p.append(T(16, 240, "IRQ-Verzoegerung + Nachfuellen + Veroeffentlichen + Reserve < Fenster vor der naechsten Nutzung.", 14, ERR))
    p.append(T(16, 270, "30 ms Nachfuellzeit ueberschreitet die idealen 23,22 ms. TX: Underrun. RX: Overrun.", 15, ERR))
    p.append(T(16, 304, "ISR: Status lesen, Quelle quittieren, Arbeit signalisieren. Nachfuellen ausserhalb, wenn das Budget traegt.", 14))
    p.append(T(16, 336, "Zwei boolesche Flags zaehlen keine beliebig vielen Runden. Bei unklarem Besitz neu synchronisieren.", 14, MUTED, "400"))
    p.append(T(16, 368, "Etwa 43,07 HT-/TC-Ereignisse je Sekunde. Wrap nur, wenn der Controller ihn neu laedt.", 14, MUTED, "400"))
    p.append(T(16, 400, "Linearer Ring mit HT/TC und Hardware-Doppelpuffer sind verschiedene Implementierungen.", 14, MUTED, "400"))
    save("pingpong.svg", p)


# 11 2D
def fig_2d():
    p = svg(1200, 400)
    p.append(T(16, 24, "RGB565, 320 Pixel, Pitch 640 Byte. Rechteck 4 x 3 bei x=10, y=20.", 16))
    p.append(rect(16, 48, 420, 200, MUTED))
    p.append(rect(16 + 80, 48 + 70, 70, 52, DMA, "#F8E0CC"))
    p.append(T(24, 68, "Framebuffer", 14, MUTED, "400"))
    p.append(T(100, 100, "4 x 3", 14, DMA))
    p.append(T(460, 80, "Basis 0x20001000, fiktiv", 16))
    p.append(T(460, 112, "Erste Zeile: 0x20004214", 18, DMA))
    p.append(T(460, 144, "8 Byte kopieren, Skip 632 Byte", 16))
    p.append(T(460, 176, "Naechster Zeilenstart +640 Byte", 16, CPU))
    p.append(T(460, 214, "Dichtes Ziel: Startabstand 8 Byte", 16, OK))
    p.append(T(16, 280, "Offsetregister koennen Pixel statt Bytes zaehlen. Datenblatt umrechnen.", 15, IRQ))
    p.append(T(16, 314, "Scatter-Gather: drei Puffer, Deskriptor mit SRC, DST, Count, Next.", 15))
    p.append(T(16, 346, "Deskriptoren brauchen Erreichbarkeit, Alignment, Lebensdauer und ggf. Cache-Pflege.", 14, MUTED, "400"))
    p.append(T(16, 376, "Next = 0 ist kein universeller Stopp. DMA ersetzt kein I2C-START/STOP.", 14, ERR))
    save("twod.svg", p)


# 12 Labor
def fig_lab():
    p = svg(1200, 400)
    p.append(T(16, 24, "Rechenmodell, keine Renode-Messung. 4096 Byte, 115200 Baud, 8N1.", 17))
    p.append(T(16, 50, "Ideale Leitungszeit: 4096 x 10 / 115200 = 355,56 ms.", 16, DMA))
    nodes = [
        (16, "TX-Puffer", OK),
        (220, "DMAC", DMA),
        (420, "UART", DMA),
        (640, "Pruefer", OK),
        (860, "main", CPU),
    ]
    subs = ["lebt weiter", "Request", "FIFO/Shift", "Bytestrom", "Heartbeat"]
    for (x, a, col), sub in zip(nodes, subs):
        box(p, x, 76, 180, 52, a, sub, col)
    p.append(T(16, 170, "Heartbeat schaltet die LED in main(), etwa alle 10 ms nach Zeitvergleich.", 15, CPU))
    p.append(T(16, 198, "Ein Timer darf die Zeitbasis sein. Der Wechsel darf nicht autonom in Hardware oder Timer-ISR liegen.", 14, ERR))
    p.append(T(16, 236, "Vergleich nur bei identischen Daten und UART-Einstellungen.", 15))
    p.append(T(16, 264, "Getrennt protokollieren: korrekter Bytestrom, Main-Fortschritt, Heartbeat-Luecken, DMA-TC, Leitung fertig.", 14))
    p.append(T(16, 300, "PerformanceInMips ist keine MCU-Taktfrequenz. Hostlaufzeit ist keine Transferzeit.", 15, IRQ))
    p.append(T(16, 334, "Ohne Baud- und Handshake-Modell bleibt der Lauf ein Funktionstest, keine Entlastungsmessung.", 15, ERR))
    p.append(T(16, 370, "Im Repository kein DMA-Modell und keine .repl. Diese Adressen bleiben fiktiv.", 14, MUTED, "400"))
    save("lab.svg", p)


if __name__ == "__main__":
    for fn in (
        fig_budget, fig_time, fig_paths, fig_hand, fig_addr, fig_life,
        fig_cache, fig_uncached, fig_burst, fig_ping, fig_2d, fig_lab,
    ):
        fn()
