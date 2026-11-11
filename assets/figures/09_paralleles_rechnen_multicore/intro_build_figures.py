#!/usr/bin/env python3
"""Eigene räumliche Lehrdiagramme zu Datenaufteilung und Zeilenrechten.

Keine Messdaten: Pfeile bezeichnen Datenzuordnung oder logische Ordnung.
SVG mit Python-Standardbibliothek; optional PNG mit vorhandenem Playwright:
    python3 intro_build_figures.py --png
"""
import argparse
from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parent
INK, MUTED, BG, RED = '#1D1D1F', '#656D76', '#F5F5F7', '#E2001A'


def text(x, y, label, size=25, color=INK, anchor='middle'):
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" '
            f'text-anchor="{anchor}">{escape(str(label))}</text>')


def rect(x, y, w, h, accent=False):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" '
            f'fill="{BG}" stroke="{RED if accent else MUTED}" stroke-width="2"/>')


def line(x1, y1, x2, y2, arrow=False, accent=False, dash=False):
    extra = ' marker-end="url(#arrow)"' if arrow else ''
    extra += ' stroke-dasharray="7 6"' if dash else ''
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="{RED if accent else MUTED}" stroke-width="2.5"{extra}/>')


def save(name, title, items, height=430):
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="{height}" '
           f'viewBox="0 0 1000 {height}" role="img" aria-labelledby="title">',
           f'<title id="title">{escape(title)}</title>',
           '<style>text{font-family:Inter,Arial,Helvetica,sans-serif}</style>',
           '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" '
           'refY="3" orient="auto"><path d="M0,0 L7,3 L0,6" '
           f'fill="{MUTED}"/></marker></defs>',
           f'<rect width="1000" height="{height}" fill="#FFFFFF"/>']
    (OUT / f'{name}.svg').write_text('\n'.join(svg + items + ['</svg>'])+'\n', encoding='utf-8')


def private_shared():
    p = [text(500, 32, 'Eine gemeinsame Eingabe, getrennte Schreibzuständigkeiten', 28)]
    # Gleiche Speicheradressen sind für beide Worker erreichbar. Die Klammern
    # darunter teilen den Eingabebereich auf; keine zeitliche Achse.
    for i, value in enumerate([1, 3, 5, 7]):
        x = 300+i*100
        p += [rect(x, 65, 100, 60), text(x+50, 105, value, 29), text(x+50, 150, f'x[{i}]', 22, MUTED)]
    p += [text(500, 190, 'x bleibt während beider Rechnungen unverändert', 23, MUTED),
          line(350, 207, 240, 238, True), line(650, 207, 760, 238, True),
          rect(80, 248, 320, 88), text(240, 279, 'Worker 0: x[0] + x[1]'),
          text(240, 315, 'lokaler Akkumulator → 4', 24, RED),
          rect(600, 248, 320, 88), text(760, 279, 'Worker 1: x[2] + x[3]'),
          text(760, 315, 'lokaler Akkumulator → 12', 24, RED),
          text(500, 391, 'Getrennte Ergebnisse: teil[0] nur von W0, teil[1] nur von W1 geschrieben.', 23)]
    save('intro_private_shared', 'Unveränderliche Eingabe und je Worker private Teilsumme', p)


def line_rights():
    p = [text(245, 35, 'Fall A: gemeinsam lesen', 27),
         text(745, 35, 'Fall B: Schreibrecht bei K0', 27),
         line(500, 58, 500, 330, dash=True)]
    # Zwei alternative Zustände; links gültige Leser, rechts K0 exklusiv.
    for x in (0, 500):
        for y, label in ((95, 'Kern 0'), (245, 'Kern 1')):
            p.append(text(x+65, y+41, label, 23))
            for j in range(4):
                p += [rect(x+130+j*85, y, 85, 66), text(x+172+j*85, y+43, 5 if j==0 else '…', 27)]
    p += [text(245, 204, 'beide Kopien gültig und sauber', 23, MUTED),
          text(745, 204, 'K0 darf die ganze Zeile ändern', 23, RED),
          f'<rect x="624" y="89" width="352" height="78" rx="10" fill="none" stroke="{RED}" stroke-width="3"/>',
          line(640, 305, 960, 251, accent=True), line(640, 251, 960, 305, accent=True),
          text(745, 346, 'K1 ungültig: kein Treffer', 23, RED),
          text(500, 392, 'Alternative Rechtefälle derselben Zeile; kein Zeitablauf und kein Software-Lock.', 23, MUTED)]
    save('intro_line_rights', 'Eine Zeile kann lesend geteilt oder zum Schreiben exklusiv übernommen werden', p)


def handover():
    p = [text(500, 32, 'Ergebnisse gehören erst nach ihrer Veröffentlichung dem Sammler', 27)]
    for x, worker, value in [(60, 'W0', 4), (540, 'W1', 12)]:
        p += [text(x+200, 81, f'{worker}: getrennt rechnen', 26),
              rect(x, 104, 195, 74), text(x+97, 136, 'teil schreiben', 24), text(x+97, 165, value, 25, RED),
              line(x+207, 140, x+255, 140, True),
              rect(x+270, 104, 150, 74, True), text(x+345, 135, 'fertig = 1', 24),
              text(x+345, 165, 'Release', 22, RED),
              text(x+335, 210, 'beobachtet', 20, MUTED, 'end')]
        target = 390 if worker == 'W0' else 610
        p += [line(x+345, 191, x+345, 234),
              line(x+345, 234, target, 234), line(target, 234, target, 253, True)]
    p += [rect(290, 256, 420, 79), text(500, 288, 'Sammler: beide 1 mit Acquire gelesen', 24),
          text(500, 319, 'danach teil[0] + teil[1] = 16', 26, RED),
          text(500, 382, 'Ein Durchlauf, kein erneutes Überschreiben; Pfeile geben logische Ordnung an.', 23, MUTED),
          text(500, 416, 'Eine frühe Fertigmeldung erlaubt kein Lesen des noch nicht freigegebenen Ergebnisses.', 21, MUTED)]
    save('intro_handover', 'Zwei unabhängig veröffentlichte Teilergebnisse und anschließende Zusammenführung', p, 440)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--png', action='store_true')
    args = parser.parse_args()
    private_shared()
    line_rights()
    handover()
    if args.png:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--no-sandbox'])
            for name in ('intro_private_shared', 'intro_line_rights', 'intro_handover'):
                page = browser.new_page(viewport={'width':1000, 'height':500}, device_scale_factor=2)
                page.set_content('<style>body{margin:0}</style>'+ (OUT/f'{name}.svg').read_text(encoding='utf-8'))
                page.locator('svg').screenshot(path=str(OUT/f'{name}.png'))
                page.close()
            browser.close()


if __name__ == '__main__':
    main()
