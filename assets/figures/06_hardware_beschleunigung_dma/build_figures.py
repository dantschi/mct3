#!/usr/bin/env python3
"""Reproduzierbare Lehrdiagramme für VL06; keine Messdaten oder Schaltpläne.

Python-Standardbibliothek für SVG. Optional: Playwright und Chromium für PNG.
Aufruf: python3 build_figures.py --png [--chromium /usr/bin/chromium]
"""
import argparse
import math
from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parent
INK, MUTED, LIGHT, BG, RED = (
    "#1D1D1F", "#86868B", "#E5E5EA", "#F5F5F7", "#E2001A"
)
W = 1000


def text(x, y, label, size=24, color=INK, anchor="start"):
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" '
            f'text-anchor="{anchor}">{escape(str(label))}</text>')


def line(x1, y1, x2, y2, color=INK, width=2, dash=False, arrow=False):
    extra = ' stroke-dasharray="6 5"' if dash else ""
    extra += ' marker-end="url(#arrow)"' if arrow else ""
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="{color}" stroke-width="{width}"{extra}/>')


def path(points, color=RED, width=3):
    coords = " ".join(f"{x:.3f},{y:.3f}" for x, y in points)
    return f'<polyline points="{coords}" fill="none" stroke="{color}" stroke-width="{width}"/>'


def rect(x, y, w, h, fill=BG, stroke=LIGHT, radius=8):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" '
            f'rx="{radius}" fill="{fill}" stroke="{stroke}"/>')


def box(x, y, w, h, labels):
    result = [rect(x, y, w, h)]
    for i, label in enumerate(labels):
        result.append(text(x+w/2, y+h/2+(i-(len(labels)-1)/2)*30+8,
                           label, 24, anchor="middle"))
    return result


def save(name, title, height, elements):
    start = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{height}" '
        f'viewBox="0 0 {W} {height}" role="img" aria-labelledby="title">',
        f'<title id="title">{escape(title)}</title>',
        '<style>text{font-family:Inter,Arial,Helvetica,sans-serif;font-weight:400}</style>',
        '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" '
        'orient="auto" markerUnits="strokeWidth"><path d="M0,0 L8,3 L0,6" '
        f'fill="{INK}"/></marker></defs>',
        f'<rect width="{W}" height="{height}" fill="#FFFFFF"/>',
    ]
    (OUT/f"{name}.svg").write_text(
        "\n".join(start+elements+["</svg>"])+"\n", encoding="utf-8"
    )


def axis(x0, x1, y, marks, label):
    result = [line(x0, y, x1, y, MUTED), text(x1, y+60, label, 22, anchor="end")]
    for x, value in marks:
        result += [line(x, y-5, x, y+5, MUTED), text(x, y+29, value, 22, anchor="middle")]
    return result


def digital(intervals, x0, scale, high, low, color=RED):
    """(start, end, is_high), contiguous half-open intervals."""
    points = []
    last_y = None
    for start, end, active in intervals:
        y = high if active else low
        x = x0+scale*start
        if last_y is not None and y != last_y:
            points.append((x, last_y))
        points.extend([(x, y), (x0+scale*end, y)])
        last_y = y
    return path(points, color)


def figures():
    p = [rect(35, 65, 380, 190), text(225, 160, "320 × 240 Pixel", 30, anchor="middle"),
         text(225, 210, "2 Bytes je Pixel", anchor="middle"),
         line(435, 160, 510, 160, arrow=True)]
    p += box(530, 80, 440, 80, ["153600 Bytes je Vollbild"])
    p += box(530, 200, 440, 80, ["60 Bilder/s → 9,216 MB/s"])
    p += [text(20, 35, "RGB565: 16 Bit je Pixel · MB = 10⁶ Bytes"),
          line(750, 160, 750, 195, arrow=True)]
    save("budget", "Bildspeicher und erforderliche Nutzdatenrate", 315, p)

    p = [text(20, 30, "Schematisch: gleicher Datenblock · Zeiten nicht maßstäblich")]
    for y, label in [(70, "Polling"), (155, "Interrupts"), (240, "DMA")]:
        p += [text(20, y+29, label), line(210, y+45, 945, y+45, MUTED)]
    p += [rect(210, 70, 705, 42, BG, RED), text(560, 99, "blockierender Aufruf wartet und bedient", 23, anchor="middle")]
    for x in [210, 355, 500, 645, 790]:
        p += [rect(x, 155, 42, 42, BG, RED)]
    p += [text(920, 219, "dazwischen: andere Arbeit", 22, anchor="end"),
          rect(210, 240, 130, 42, BG, RED), text(275, 270, "Start", 22, anchor="middle"),
          rect(340, 240, 450, 42), text(565, 270, "andere CPU-Arbeit", 23, anchor="middle"),
          rect(790, 240, 125, 42, BG, RED), text(852, 270, "Prüfung", 22, anchor="middle"),
          text(945, 331, "Zeit →", 22, anchor="end")]
    save("timelines", "Blockierendes Polling, Interruptbedienung und DMA", 355, p)

    p = [text(20, 30, "CPU-Kopieren")]
    p += box(20, 55, 235, 75, ["Speicher"])
    p += box(385, 55, 235, 75, ["CPU-Register"])
    p += box(750, 55, 230, 75, ["Peripherie"])
    p += [line(255, 92, 380, 92, arrow=True), line(620, 92, 745, 92, arrow=True),
          text(20, 183, "DMA-Kopieren")]
    p += box(20, 210, 235, 75, ["Speicher"])
    p += box(385, 210, 235, 75, ["DMA-Initiator"])
    p += box(750, 210, 230, 75, ["Peripherie"])
    p += [line(255, 247, 380, 247, RED, 3, arrow=True),
          line(620, 247, 745, 247, RED, 3, arrow=True),
          text(500, 340, "Beide Wege beanspruchen Speicher- und Busressourcen", 23, anchor="middle")]
    save("paths", "Daten durch CPU-Register oder einen DMA-Initiator", 365, p)

    p = box(20, 55, 235, 80, ["CPU", "Zugriff mit Cache-Miss"])
    p += box(20, 235, 235, 80, ["DMA", "Speicherzugriff"])
    p += box(385, 145, 210, 80, ["Arbiter", "teilt Zugriffe zu"])
    p += box(750, 145, 230, 80, ["Gemeinsamer", "Speicherpfad"])
    p += [line(255, 95, 380, 174, arrow=True), line(255, 275, 380, 196, arrow=True),
          line(595, 185, 745, 185, RED, 3, arrow=True),
          text(340, 35, "Lokaler Cache-Hit: nicht zwangsläufig dieser Pfad", 23),
          text(500, 365, "Konkurrenz nur an gemeinsam benutzten Ressourcen", 23, anchor="middle")]
    save("arbiter", "CPU und DMA konkurrieren am gemeinsamen Speicherpfad", 392, p)

    p = box(20, 115, 260, 100, ["Peripherie", "Register/FIFO bereit"])
    p += box(410, 115, 255, 100, ["DMA-Controller", "bewegt ein Element"])
    p += box(780, 115, 200, 100, ["Speicher"])
    p += [line(280, 140, 405, 140, RED, 3, arrow=True), text(340, 116, "Request", 22, anchor="middle"),
          line(410, 193, 285, 193, arrow=True), text(340, 242, "Datenzugriff", 22, anchor="middle"),
          line(780, 165, 670, 165, arrow=True),
          text(20, 35, "Lokale Bereitschaft ist kein externes Protokoll-ACK"),
          text(500, 313, "FIFO: First In, First Out · ACK: Acknowledge", 23, anchor="middle")]
    save("handshake", "Lokaler DMA-Request und Datenzugriff sind getrennte Vorgänge", 340, p)

    p = [text(20, 30, "Senden · Breite 1 Byte · Modelladressen mit 0x-Präfix"),
         text(190, 76, "Quelle im Speicher", anchor="middle"),
         text(760, 76, "UART-TX-Register fest", anchor="middle")]
    p += box(600, 155, 340, 95, ["0x40010004", "jedes Element hierhin"])
    for i in range(4):
        y = 100+55*i
        p += [rect(30, y, 320, 44), text(190, y+30, f"0x2000100{i}", anchor="middle"),
              line(350, y+22, 595, 175+17*i, RED, 2, arrow=True)]
    p += [text(500, 364, "Quelladresse +1 je Element · Zieladresse +0", 23, anchor="middle")]
    save("addrs", "Byteweises Senden mit inkrementierender Quelle und festem Ziel", 390, p)

    p = [text(20, 30, "Empfangen · Breite 2 Bytes · vier Messwerte"),
         text(225, 77, "ADC-Datenregister fest", anchor="middle"),
         text(770, 77, "Ziel im Speicher", anchor="middle")]
    p += box(40, 155, 370, 95, ["0x40011000", "jedes Element von hier"])
    for i in range(4):
        y = 100+55*i
        p += [rect(620, y, 320, 44), text(780, y+30, f"0x2000200{2*i}", anchor="middle"),
              line(410, 175+17*i, 615, y+22, RED, 2, arrow=True)]
    p += [text(500, 364, "Quelladresse +0 je Element · Zieladresse +2", 23, anchor="middle")]
    save("rx-addrs", "Sechzehn-Bit-Empfang mit festem Register und wachsendem Array", 390, p)

    p = box(20, 70, 270, 85, ["CPU-Zeiger", "virtuelle Adresse"])
    p += box(20, 245, 270, 85, ["DMA-Geräteadresse", "für diesen Initiator"])
    p += box(430, 155, 210, 85, ["Plattform", "übersetzt/ordnet zu"])
    p += box(770, 155, 210, 85, ["Derselbe", "Speicherbereich"])
    p += [line(290, 113, 425, 183, arrow=True), line(290, 287, 425, 211, arrow=True),
          line(640, 197, 765, 197, RED, 3, arrow=True),
          text(20, 35, "Gleicher Speicher bedeutet nicht automatisch gleiche Zahl"),
          text(500, 385, "Ein C-Cast erzeugt keine Geräteabbildung", 24, anchor="middle")]
    save("address-space", "CPU-Zeiger und DMA-Geräteadresse können unterschiedliche Zahlen haben", 410, p)

    p = []
    for x, labels in [(20, ["CPU", "füllt Puffer"]), (275, ["Übergabe", "sichtbar machen"]),
                      (530, ["DMA", "greift zu"]), (785, ["CPU", "prüft Ergebnis"])]:
        p += box(x, 95, 195, 100, labels)
    for x in [215, 470, 725]:
        p += [line(x, 145, x+55, 145, RED, 3, arrow=True)]
    p += [text(500, 35, "Endlicher Auftrag: logischer Besitzwechsel", 26, anchor="middle"),
          line(882, 210, 882, 265), line(882, 265, 117, 265),
          line(117, 265, 117, 200, arrow=True),
          text(500, 303, "Rückgabe erst nach bestätigtem Ende aller Pufferzugriffe", 23, anchor="middle")]
    save("lifecycle", "Vorbereiten, übergeben, schützen und geprüft zurücknehmen", 333, p)

    x = lambda t: 310+350*t
    p = [text(20, 30, "UART-Modell · T = Rahmendauer · letztes Byte B steht an")]
    p += [text(20, 115, "DMA-Auftrag"), line(180, 115, x(0), 115, RED, 3),
          text(x(0), 77, "TC", 24, anchor="middle"), line(x(0), 85, x(0), 282, MUTED, dash=True),
          text(20, 186, "FIFO: Byte B"), rect(x(0), 155, 175, 42),
          text(x(.25), 184, "wartet", 23, anchor="middle"),
          text(20, 257, "Schieberegister"), rect(x(-.3), 225, 280, 42, BG, RED),
          text(x(.1), 254, "Rest A", 23, anchor="middle"),
          rect(x(.5), 225, 350, 42, BG, RED), text(x(1), 254, "Byte B", 23, anchor="middle"),
          line(x(1.5), 85, x(1.5), 282, RED, 3),
          text(x(1.5), 77, "Leitungsende", 23, anchor="middle")]
    p += axis(x(0), 940, 287, [(x(0), "0"), (x(.5), "0,5 T"), (x(1.5), "1,5 T")], "Zeit nach DMA-TC →")
    save("wire-complete", "DMA-Abschluss vor FIFO-Leerung und Ende des letzten UART-Rahmens", 360, p)

    p = [text(20, 35, "Nicht kohärentes Write-Back-Modell · Werte als Hexbytes")]
    for x, title in [(20, "CPU-Cache"), (365, "Speicher"), (710, "DMA liest")]:
        p += box(x, 90, 270, 75, [title])
    p += [text(155, 210, "22 · Dirty", 30, RED, "middle"), text(500, 210, "11 · alt", 30, INK, "middle"),
          text(845, 210, "11 · alt", 30, INK, "middle"), line(635, 199, 705, 199, arrow=True),
          line(290, 245, 360, 245, RED, 3, dash=True, arrow=True),
          text(500, 303, "Erst Clean veröffentlicht 22 in den Speicher", 24, anchor="middle")]
    save("cache", "Neue CPU-Cachewerte sind ohne Veröffentlichung nicht DMA-sichtbar", 333, p)

    p = [text(20, 35, "Fehlerfall: alte Dirty-Zeile bleibt während DMA-Empfang")]
    p += box(20, 110, 270, 90, ["CPU-Cache", "AA · alt und Dirty"])
    p += box(365, 110, 270, 90, ["Speicher", "55 · neu"])
    p += box(710, 110, 270, 90, ["DMA", "schreibt 55"])
    p += [line(705, 155, 640, 155, RED, 3, arrow=True),
          line(290, 248, 360, 248, arrow=True), text(325, 285, "späteres Write-Back: AA überschreibt 55", 23, anchor="middle"),
          text(500, 346, "Vorbereiten und nach Empfang synchronisieren: Plattformregel", 23, anchor="middle")]
    save("rx-cache", "Eine alte Dirty-Cachekopie kann neu empfangene Daten überschreiben", 373, p)

    p = [text(20, 30, "32 Bytes pro Zeile · Ausschnitt ab 0x20001000")]
    for i in range(4):
        x0 = 90+i*210
        p += [rect(x0, 105, 210, 65), text(x0+105, 93, f"+0x{32*i:02X}", 23, anchor="middle")]
    p += [rect(90+3*840/128, 111, 100*840/128, 53, BG, RED, 0),
          text(450, 144, "Puffer: 100 Bytes", 24, anchor="middle"),
          line(90+3*840/128, 180, 90+3*840/128, 235, RED, 2),
          text(110, 263, "Start +0x03", 23),
          line(90+103*840/128, 180, 90+103*840/128, 235, RED, 2),
          text(760, 263, "Ende +0x67", 23, anchor="middle"),
          text(500, 333, "Wartungsbereich: +0x00 bis ausschließlich +0x80 = 128 Bytes", 23, anchor="middle")]
    save("cache-lines", "Hundert Bytes berühren vier ganze Cachezeilen mit gemeinsamem Rand", 363, p)

    p = []
    for x, labels in [(20, ["Sichtbarkeit", "Kohärenz / Cachepflege"]),
                      (360, ["Erreichbarkeit", "DMA kann adressieren"]),
                      (700, ["Besitz", "keine fremden Zugriffe"])]:
        p += box(x, 90, 280, 120, labels)
    p += [text(500, 35, "Alle drei Bedingungen müssen gleichzeitig gelten", 26, anchor="middle"),
          line(160, 215, 160, 267), line(500, 215, 500, 267), line(840, 215, 840, 267),
          line(160, 267, 840, 267, RED, 3),
          text(500, 315, "RAM_UNCACHED ist nur ein Name, keine Hardwarekonfiguration", 23, anchor="middle")]
    save("uncached", "Sichtbarkeit, DMA-Erreichbarkeit und Besitz getrennt prüfen", 342, p)

    p = box(20, 110, 220, 100, ["Speicher", "Burst liefert Daten"])
    p += box(395, 110, 260, 100, ["DMA-FIFO", "endliche Kapazität"])
    p += box(790, 110, 190, 100, ["Peripherie", "entnimmt"])
    p += [line(240, 160, 390, 160, RED, 4, arrow=True), text(317, 132, "gebündelt", 23, anchor="middle"),
          line(655, 160, 785, 160, arrow=True), text(720, 132, "einzeln", 23, anchor="middle"),
          line(790, 240, 660, 240, arrow=True), text(725, 271, "Request", 23, anchor="middle"),
          text(20, 35, "Speicherzugriff und Peripherieverbrauch haben andere Zeitmuster"),
          text(500, 327, "FIFO puffert kurzzeitig; voller oder leerer FIFO begrenzt den Weg", 23, anchor="middle")]
    save("burst", "Ein endlicher FIFO entkoppelt Speicherburst und einzelne Requests", 355, p)

    p = [text(20, 35, "Deskriptormodell: SRC · DST · COUNT · NEXT")]
    for i, x0 in enumerate([20, 370, 720]):
        p += box(x0, 100, 260, 140, [f"Auftrag {i+1}", "Quelle / Ziel / Anzahl", "NEXT → Folge" if i < 2 else "NEXT → Ende"])
        if i<2:
            p += [line(x0+260, 170, x0+345, 170, RED, 3, arrow=True)]
    p += [text(500, 307, "DMA muss diese Struktur und das definierte Kettenende unterstützen", 23, anchor="middle")]
    save("descriptors", "Eine unterstützte Deskriptorkette verbindet mehrere Transferaufträge", 335, p)

    p = [text(20, 30, "RGB565 · 2 Bytes/Pixel · Bildbreite 320 Pixel · Quell-Pitch 640 B"),
         text(310, 73, "Zoom: x = 8 … 15, y = 19 … 23", 23, anchor="middle")]
    for col in range(8):
        p += [text(118+col*55, 107, col+8, 22, anchor="middle")]
    for row in range(5):
        p += [text(67, 147+row*42, row+19, 22, anchor="end")]
        for col in range(8):
            selected = 1<=row<=3 and 2<=col<=5
            p += [rect(91+col*55, 120+row*42, 54, 40, BG, RED if selected else LIGHT, 0)]
    p += [text(670, 88, "Gepacktes Ziel", anchor="middle"),
          text(670, 116, "Pitch = 8 B", 22, anchor="middle"),
          line(545, 205, 620, 205, RED, 3, arrow=True)]
    for i in range(3):
        p += [rect(630, 145+i*52, 300, 42, BG, RED),
              text(780, 174+i*52, f"4 Pixel · 0x200080{8*i:02X}", 23, anchor="middle")]
    p += [text(500, 375, "Markiert: x = 10 … 13, y = 20 … 22 · drei Zeilen, insgesamt 24 B", 23, anchor="middle")]
    save("twod", "Drei Rechteckzeilen aus einem großen Bild werden ins Ziel gepackt", 403, p)

    p = [text(20, 30, "N = 8 · P = 14 geschrieben · C = 5 verarbeitet"),
         text(20, 90, "Platz"), text(20, 157, "Sample")]
    values = [8, 9, 10, 11, 12, 13, 6, 7]
    for i, value in enumerate(values):
        x0 = 180+i*95
        p += [text(x0+42, 90, i, 24, anchor="middle"), rect(x0, 115, 84, 62, BG, RED if i==5 else LIGHT),
              text(x0+42, 156, value, 30, anchor="middle")]
    p += [text(702, 221, "C mod 8 = 5", 23, anchor="middle"),
          text(850, 274, "P mod 8 = 6", 23, anchor="middle"),
          line(702, 198, 702, 181, arrow=True), line(798, 251, 798, 181, arrow=True),
          text(500, 343, "Rückstand P − C = 9 > 8: Sample 5 wurde durch 13 überschrieben", 23, anchor="middle")]
    save("ring", "Gesamtrückstand neun trotz Positionsdifferenz eins im Ring", 372, p)

    p = [text(20, 30, "Audio-TX-Modell · Rollenwechsel nach einer Halbzeit")]
    for top, dmahalf, cpuhalf, start, end in [(75, "A", "B", "1.", "Halbzeit"), (200, "B", "A", "2.", "Halbzeit")]:
        p += [text(20, top+28, f"{start} {end}", 23),
              rect(210, top, 320, 85, BG, RED),
              text(370, top+35, f"DMA liest {dmahalf}", 26, anchor="middle"),
              text(370, top+65, "CPU verändert nicht", 22, anchor="middle"),
              rect(630, top, 320, 85),
              text(790, top+35, f"CPU füllt {cpuhalf}", 26, anchor="middle"),
              text(790, top+65, "danach synchronisieren", 22, anchor="middle")]
    p += [text(500, 348, "Vor Wiedereintritt des DMA müssen Inhalt und Sichtbarkeit fertig sein", 23, anchor="middle")]
    save("pingpong", "DMA liest und CPU füllt abwechselnd unterschiedliche Pufferhälften", 377, p)

    x = lambda t: 180+10*t
    th = 2048/88200*1000
    p = [text(20, 30, "Halbzeit ≈ 23,22 ms · HT markiert Verlassen von A, nicht heutige Phase")]
    for start, end, label in [(0, th, "DMA liest A"), (th, 2*th, "DMA liest B"), (2*th, 3*th, "DMA liest A")]:
        p += [rect(x(start), 105, x(end)-x(start), 70, BG, RED),
              text((x(start)+x(end))/2, 149, label, 24, anchor="middle")]
    p += [line(x(th), 85, x(th), 239, MUTED, dash=True), text(x(th), 76, "HT gesetzt", 23, anchor="middle"),
          line(x(2*th+1), 85, x(2*th+1), 239, RED, 3),
          text(x(2*th+1), 219, "HT erst jetzt bearbeitet", 23, anchor="middle")]
    p += axis(x(0), 935, 245, [(x(0), "0"), (x(th), "23,22"), (x(2*th), "46,44"), (x(3*th), "69,66")], "Zeit / ms")
    p += [text(500, 342, "Bei 47,44 ms ist A bereits wieder belegt", 24, anchor="middle")]
    save("flag-late", "Ein verspätetes Half-Transfer-Flag gibt keine gerade aktive Hälfte frei", 371, p)

    p = [text(20, 30, "Timeout oder Fehler ist kein Beweis für ruhende Speicherzugriffe")]
    p += box(20, 100, 220, 85, ["Stopp anfordern"])
    p += box(360, 100, 260, 85, ["Begrenzt warten", "Status prüfen"])
    p += box(760, 100, 220, 85, ["Ruhe bestätigt", "Puffer zurück"])
    p += [line(240, 142, 355, 142, arrow=True), line(620, 142, 755, 142, RED, 3, arrow=True),
          text(695, 116, "ja", 22, anchor="middle"), line(490, 185, 490, 245, arrow=True)]
    p += box(330, 255, 320, 75, ["Nicht bestätigt:", "Puffer bleibt gesperrt"])
    p += [text(670, 231, "Frist abgelaufen", 23, anchor="middle")]
    save("lab", "Abbruch mit bestätigtem Stillstand oder weiterhin gesperrtem Puffer", 365, p)

def rasterize(chromium):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=chromium, headless=True,
                                   args=["--no-sandbox"])
        page = browser.new_page(viewport={"width":W, "height":450}, device_scale_factor=2)
        for source in sorted(OUT.glob("*.svg")):
            page.set_content('<html><body style="margin:0;background:white">'
                             +source.read_text(encoding="utf-8")+'</body></html>')
            page.locator("svg").screenshot(path=str(source.with_suffix(".png")))
        browser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--png", action="store_true")
    parser.add_argument("--chromium", default="/usr/bin/chromium")
    args = parser.parse_args()
    figures()
    if args.png:
        rasterize(args.chromium)
    print("21 Lehrdiagramme geschrieben" + (" (SVG und PNG)." if args.png else " (SVG)."))
