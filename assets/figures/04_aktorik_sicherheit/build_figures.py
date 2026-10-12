#!/usr/bin/env python3
"""Reproduzierbare Lehrdiagramme für VL04; keine Messdaten oder Schaltpläne.

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
    p = box(20, 95, 180, 75, ["Software", "Sollwert"])
    p += box(270, 95, 180, 75, ["PWM-Timer", "Steuersignal"])
    p += box(520, 95, 190, 75, ["Treiberstufe", "schaltet Strom"])
    p += box(790, 95, 190, 75, ["Aktor", "z. B. Motor"])
    p += [line(200, 132, 265, 132, arrow=True), line(450, 132, 515, 132, arrow=True),
          line(710, 132, 785, 132, arrow=True), text(615, 30, "Externe Versorgung, z. B. 12 V", anchor="middle"),
          line(615, 42, 615, 90, RED, 3, arrow=True),
          text(365, 235, "GPIO: Steuerpegel", anchor="middle"),
          text(755, 235, "Leistungsweg: externe Energie", anchor="middle")]
    save("paths", "Steuerpfad und Leistungsweg sind getrennt", 265, p)

    p = box(20, 50, 180, 85, ["Timereingang", "100 MHz"])
    p += box(265, 50, 190, 85, ["PSC = 99", "Teiler = 100"])
    p += box(520, 50, 210, 85, ["CNT: Zählwerk", "1 MHz → 1 µs"])
    p += box(790, 50, 190, 85, ["Vergleich", "CNT < CCR"])
    p += [line(200, 93, 260, 93, arrow=True), line(455, 93, 515, 93, arrow=True),
          line(730, 93, 785, 93, arrow=True),
          text(625, 192, "ARR = 999: 0 … 999", anchor="middle"),
          line(625, 163, 625, 140, MUTED, arrow=True),
          text(885, 242, "CCR = 250", anchor="middle"),
          line(885, 213, 885, 140, MUTED, arrow=True),
          text(30, 244, "PSC + 1 teilt den Eingangstakt")]
    save("prescaler", "Vorteiler, Zählwerk und Vergleich des PWM-Timers", 270, p)

    p = [text(20, 30, "CNT"), text(150, 30, "ARR = 4 · ein Intervall pro Tick")]
    for top, values, label in [
        (60, [0, 1, 2, 3, 4], "Up: 5 Intervalle"),
        (220, [0, 1, 2, 3, 4, 3, 2, 1], "Auf/ab: 8 Intervalle"),
    ]:
        p += [text(20, top+70, label, 22)]
        points = []
        for i, value in enumerate(values+[0]):
            x = 275+i*78
            y = top+85-value*18
            if points:
                points.append((x, points[-1][1]))
            points.append((x, y))
            if i<len(values):
                points.append((x+78, y))
                p.append(text(x+39, top+117, value, 23, anchor="middle"))
        p += [path(points), line(275, top+85, 930, top+85, MUTED, dash=True),
              text(958, top+117, "→ 0", 22, anchor="end")]
    p.append(text(950, 380, "Zeit →", 22, anchor="end"))
    save("count-modes", "Diskrete Zählfolgen für Up und Auf-ab, ARR vier", 405, p)

    p = [text(20, 28, "Gleiche Pegel 0 / 3,3 V · gleiche Periode T = 1 ms")]
    for i, duty in enumerate([.25, .5, .75]):
        top = 60+i*90
        p += [text(20, top+28, f"D = {int(duty*100)} %"),
              digital([(0, duty, True), (duty, 1, False)], 200, 720, top, top+48),
              line(200+720*duty, top, 200+720*duty, 330, MUTED, 1, dash=True)]
    p += axis(200, 920, 330, [(200, "0"), (380, "250"), (560, "500"),
                             (740, "750"), (920, "1000")], "Zeit / µs")
    save("pwm-power", "Rechtecksignale mit 25, 50 und 75 Prozent HIGH", 398, p)

    p = [text(20, 30, "CNT"), text(170, 30, "ARR = 999 · CCR = 250 · ein Tick = 1 µs"),
         text(135, 68, "999", 22, anchor="end"), text(135, 205, "0", 22, anchor="end")]
    points = []
    for tick in range(1251):
        x = 170+tick*.62
        y = 200-(tick%1000)/999*140
        if points:
            points.append((x, points[-1][1]))
        points.append((x, y))
    p += [path(points, INK, 2), line(170, 200-250/999*140, 945, 200-250/999*140,
                                   MUTED, 1, dash=True),
          text(965, 157, "250", 22, anchor="end"),
          text(20, 277, "Pin", 24),
          digital([(0, 250, True), (250, 1000, False), (1000, 1250, True)],
                  170, .62, 235, 285)]
    p += axis(170, 945, 310, [(170, "0"), (325, "250"), (790, "1000")], "Zeit / µs")
    save("edge-pwm", "Zähler und Active-High-Ausgang bei CNT kleiner CCR", 380, p)

    p = [text(20, 30, "Ein Zähltakt = 1 µs · gleiche Breite je Tick")]
    for y, n, frequency, delta in [(65, 1000, "1 kHz", "0,1"), (180, 50, "20 kHz", "2")]:
        p += [text(20, y+27, f"{frequency}: N = {n}"),
              rect(280, y, n*.62, 44)]
        for tick in range(n+1):
            p.append(line(280+tick*.62, y, 280+tick*.62, y+44, LIGHT, .6))
        p += [text(280, y+80, f"Ein CCR-Schritt: {delta} Prozentpunkte")]
    p += [text(925, 295, "Periodenlänge →", 22, anchor="end")]
    save("resolution", "Kürzere Perioden enthalten weniger Zählintervalle", 320, p)

    p = [text(20, 30, "Aktiver Anteil = 25 % · gleiche Vergleichsbedingung")]
    for y, label, high_first in [(65, "Active-High", True), (175, "Active-Low", False)]:
        p += [text(20, y+25, label),
              digital([(0, .25, high_first), (.25, 1, not high_first)], 230, 690, y, y+48),
              text(316, y-12, "aktive Zeit", 22, anchor="middle")]
    p += axis(230, 920, 270, [(230, "0"), (402.5, "250"), (920, "1000")], "Zeit / µs")
    p += [text(500, 370, "HIGH-Anteil: oben 25 %, unten 75 %", anchor="middle")]
    save("polarity", "Active-High und Active-Low bei gleichem aktiven Zeitanteil", 395, p)

    vh, duty, period, tau = 3.3, .25, .001, .01
    a, b = math.exp(-duty*period/tau), math.exp(-(1-duty)*period/tau)
    vmax = vh*(1-a)/(1-a*b)
    vmin = b*vmax
    p = [text(20, 28, "Stationäres, unbelastetes RC-Modell · R = 1 kΩ · C = 10 µF"),
         text(20, 86, "Eingang", 22), text(20, 265, "Ausgang", 22),
         text(20, 295, "(Zoom)", 22)]
    intervals = []
    for k in range(3):
        intervals += [(k, k+duty, True), (k+duty, k+1, False)]
    p += [digital(intervals, 190, 250, 55, 115),
          text(955, 43, "3,3 V", 22, anchor="end"), text(955, 144, "0 V", 22, anchor="end"),
          line(190, 210, 940, 210, MUTED, 1, dash=True),
          line(190, 305, 940, 305, MUTED, 1, dash=True)]
    points = []
    for step in range(1201):
        t = step*3*period/1200
        local = t%period
        v = vh-(vh-vmin)*math.exp(-local/tau) if local<duty*period else (
            vmax*math.exp(-(local-duty*period)/tau))
        points.append((190+250*t/period, 305-(v-vmin)/(vmax-vmin)*95))
    p += [path(points), text(955, 195, f"max. {vmax:.4f} V".replace(".", ","), 22, anchor="end"),
          text(955, 334, f"min. {vmin:.4f} V".replace(".", ","), 22, anchor="end")]
    p += axis(190, 940, 355, [(190, "0"), (440, "1"), (690, "2"), (940, "3")], "Zeit / ms")
    save("rc-filter", "PWM-Eingang und Restwelligkeit eines RC-Tiefpasses", 423, p)

    p = [text(20, 30, "LOW-Wartezeit bleibt 50 µs · fallende Flanke 20 µs später")]
    p += [text(20, 104, "geplant"), digital([(0, 50, True), (50, 100, False), (100, 120, True)],
                                           220, 5.8, 65, 115),
          text(20, 213, "verzögert"), digital([(0, 70, True), (70, 120, False)],
                                             220, 5.8, 175, 225),
          line(510, 50, 510, 265, MUTED, 1, dash=True),
          line(626, 165, 626, 265, MUTED, 1, dash=True)]
    p += axis(220, 916, 265, [(220, "0"), (510, "50"), (626, "70"),
                             (800, "100"), (916, "120")], "Zeit / µs")
    p.append(text(500, 365, "HIGH: 70 µs · LOW: 50 µs · neue Periode: 120 µs", anchor="middle"))
    save("sw-vs-hw", "Verspätete Softwareflanke im gewählten Wartezeitmodell", 395, p)

    p = [text(20, 30, "Schreiben bei 500 µs: CCR 250 → 750 · Periode 1000 µs")]
    p += [text(20, 92, "sofort"),
          digital([(0, 250, True), (250, 500, False), (500, 750, True),
                   (750, 1000, False), (1000, 1750, True), (1750, 2000, False)],
                  200, .37, 60, 115),
          text(20, 213, "gepuffert"),
          digital([(0, 250, True), (250, 1000, False), (1000, 1750, True),
                   (1750, 2000, False)], 200, .37, 180, 235),
          line(385, 45, 385, 260, RED, 1, dash=True),
          line(570, 45, 570, 260, MUTED, 1, dash=True)]
    p += axis(200, 940, 265, [(200, "0"), (385, "500"), (570, "1000"),
                             (755, "1500"), (940, "2000")], "Zeit / µs")
    p.append(text(500, 362, "Pufferübernahme am Periodenanfang bei 1000 µs", anchor="middle"))
    save("preload", "Compare-Änderung sofort oder erst am nächsten Periodenanfang", 390, p)

    p = box(25, 105, 285, 105, ["Ein CNT, ein ARR", "N = 1000 · f = 1 kHz"])
    for y, channel, ccr, colour in [(30, 1, 250, "Rot"), (145, 2, 500, "Grün"), (260, 3, 0, "Blau")]:
        p += box(490, y, 235, 70, [f"CCR{channel} = {ccr}"])
        p += [line(365, y+35, 485, y+35, arrow=True),
              line(725, y+35, 810, y+35, arrow=True),
              text(830, y+43, colour)]
    p += [line(310, 157, 365, 157), line(365, 65, 365, 295),
          text(25, 345, "Je Kanal eigener Compare-Wert, aber gleiche Periode")]
    save("rgb-gamma", "Drei Compare-Kanäle teilen ein Zählwerk und eine Periode", 375, p)

    p = [text(20, 30, "Gewähltes Servoformat · drei alternative Pulse · T = 20 ms")]
    for y, pulse in [(65, 1), (155, 1.5), (245, 2)]:
        p += [text(20, y+26, f"{str(pulse).replace('.', ',')} ms"),
              digital([(0, pulse, True), (pulse, 20, False)], 210, 35, y, y+48),
              text(430, y+25, f"CCR = {int(pulse*1000)}", 22)]
    p += axis(210, 910, 330, [(210, "0"), (560, "10"), (910, "20")], "Zeit / ms")
    save("applications", "Servo-Kommandoimpulse bei 50 Hertz und einem MHz Zähltakt", 397, p)

    p = [text(20, 30, "Ideales Timeout: 2 s · jeder Feed startet die Frist neu")]
    x = lambda t: 100+250*t
    p += [line(x(1), 155, x(3), 155, INK, arrow=True),
          text((x(1)+x(3))/2, 138, "2 s ab letztem Feed", anchor="middle"),
          line(x(1.2), 95, x(1.2), 238, MUTED, dash=True),
          text(x(1.2)+12, 88, "Hänger ab 1,2 s", 22),
          line(x(3), 60, x(3), 238, RED, 3),
          text(x(3), 48, "Reset", anchor="middle")]
    for t in [0, .5, 1]:
        p += [line(x(t), 180, x(t), 230, RED, 3), text(x(t), 176, "Feed", 22, anchor="middle")]
    p += axis(100, 900, 238, [(x(0), "0"), (x(.5), "0,5"), (x(1), "1"),
                             (x(2), "2"), (x(3), "3")], "Zeit seit Start / s")
    save("watchdog", "Feed-Zeitpunkte und Watchdogfrist bis zum idealen Reset", 308, p)

    x = lambda age: 120+350*age
    p = [text(20, 30, "Modell: 0,5 s < Alter seit letztem Feed < 2 s"),
         rect(x(.5), 90, x(2)-x(.5), 115),
         text((x(.5)+x(2))/2, 123, "zulässiges Fenster", anchor="middle")]
    for age, label, y in [(.2, "zu früh", 166), (1, "zeitlich gültig", 166), (2.1, "abgelaufen", 76)]:
        p += [line(x(age), y+10, x(age), 225, RED, 3),
              text(x(age), y, label, 22, anchor="middle")]
    p += axis(120, 925, 230, [(x(0), "0"), (x(.5), "0,5"), (x(1), "1"),
                             (x(2), "2")], "Alter / s")
    p.append(text(500, 335, "Zeitlich gültig reicht nur mit frischem Fortschritt", anchor="middle"))
    save("window", "Frühes, gültiges und abgelaufenes Watchdog-Zeitfenster", 365, p)

    x = lambda t: 260+190*t
    p = [text(20, 30, "Letzter Feed: 1 s · Hänger: 1,2 s · idealer Reset: 3 s")]
    p += [text(20, 106, "Hauptprogramm"),
          rect(x(0), 75, x(1.2)-x(0), 45),
          text(x(0)+10, 106, "Fortschritt", 22),
          text(x(1.2)+15, 106, "hängt", 22),
          text(20, 206, "Hardware-PWM"),
          rect(x(0), 175, x(3)-x(0), 45),
          text(x(0)+10, 206, "letztes Signalmuster kann weiterlaufen", 22),
          rect(x(3), 75, 140, 145),
          text(x(3)+70, 105, "Zustand", 22, anchor="middle"),
          text(x(3)+70, 135, "prüfen", 22, anchor="middle"),
          line(x(1.2), 57, x(1.2), 238, MUTED, dash=True),
          line(x(3), 57, x(3), 238, RED, 3)]
    p += axis(x(0), 970, 245, [(x(0), "0"), (x(1.2), "1,2"), (x(3), "3")], "Zeit seit Start / s")
    p += [text(500, 350, "Resetdomänen und externe Versorgung bestimmen den Ausgang", 23, anchor="middle")]
    save("safe-state", "Programmstillstand, weiterlaufendes PWM-Muster und Resetdomänen", 380, p)


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
    print("15 Lehrdiagramme geschrieben" + (" (SVG und PNG)." if args.png else " (SVG)."))
