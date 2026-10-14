#!/usr/bin/env python3
"""Eigene MCT3-Datenflussabbildung, CC BY 4.0 (siehe Repository-LICENSE).

Keine Fremdbildteile; kursinternes Dense-Beispiel, keine Leistungsmessung.
Aufruf: python3 build_chip_comparison.py --png
SVG: Python-Standardbibliothek. PNG: Playwright und Chromium.
"""
import argparse
from build_figures import OUT, INK, MUTED, LIGHT, BG, RED, text, line, rect, path, save

NAME = 'cpu-gpu-npu'
WEIGHTS = (1, 2, 3)
INPUTS = (2, 1, 3)
BIAS = 1


def arrow_path(points):
    return path(points, MUTED, 2).replace('/>', ' marker-end="url(#arrow)"/>')


def label_box(x, y, width, height, label, size=26, accent=False):
    return [rect(x, y, width, height, '#FFFFFF', RED if accent else LIGHT),
            text(x+width/2, y+height/2+size*.32, label, size, anchor='middle')]


def comparison():
    products = tuple(w*x for w, x in zip(WEIGHTS, INPUTS))
    sums = [BIAS]
    for product in products:
        sums.append(sums[-1]+product)
    assert products == (2, 2, 9) and sums == [1, 3, 5, 14]
    p = [
        '<desc>Eine Ausgabesumme der Dense-Schicht: Gewichte 1, 2, 3, Eingaben 2, 1, 3 und Bias 1. '
        'Der skalare CPU-Lehrpfad nutzt eine MAC wiederholt. Der GPU-Lehrpfad bildet drei Produkte '
        'parallel und reduziert sie. Ein NPU-Prinzipbeispiel hält ladbare Gewichte lokal und '
        'reicht Teilsummen durch drei MAC-Zellen. Alle ergeben 14. Keine Zeit- oder Energiewerte.</desc>',
        '<metadata><rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:cc="http://creativecommons.org/ns#">'
        '<cc:Work rdf:about=""><dc:title>Dieselbe Ausgabesumme auf CPU, GPU und NPU</dc:title>'
        '<dc:creator>Projekt Mikrocomputertechnik 3 (MCT3)</dc:creator>'
        '<dc:description>Eigene Zeichnung zum kursinternen Zahlenbeispiel; keine übernommenen Bildbestandteile.</dc:description>'
        '<cc:license rdf:resource="https://creativecommons.org/licenses/by/4.0/"/>'
        '</cc:Work></rdf:RDF></metadata>',
    ]
    for x, name, subtitle in [(20, 'CPU', 'Skalarer Lehrpfad'),
                             (350, 'GPU', 'Produkte parallel bilden'),
                             (680, 'NPU', 'Ein lokaler Datenfluss')]:
        p += [text(x+150, 35, name, 30, anchor='middle'),
              text(x+150, 72, subtitle, 23, anchor='middle'),
              rect(x, 95, 300, 310)]

    # CPU: the first operand pair is drawn; the loop reuses the same MAC.
    p += label_box(45, 135, 115, 55, 'Eingang 2', 23)
    p += label_box(180, 135, 115, 55, 'Gewicht 1', 23)
    p += [arrow_path([(102, 190), (102, 205), (145, 205), (145, 225)]),
          arrow_path([(237, 190), (237, 205), (195, 205), (195, 225)])]
    p += label_box(115, 225, 110, 55, 'MAC')
    p += [rect(50, 305, 240, 60, '#FFFFFF', LIGHT),
          text(170, 326, 'Akkumulator', 22, anchor='middle'),
          text(170, 358, ' → '.join(map(str, sums)), 26, anchor='middle')]
    p += [line(170, 280, 170, 305, MUTED, arrow=True),
          arrow_path([(50, 335), (35, 335), (35, 252), (115, 252)]),
          text(170, 395, 'Rechenwerk erneut nutzen', 22, anchor='middle')]

    # GPU: three independent products, followed by reduction and one bias.
    p += [text(500, 125, 'Drei Produkte', 23, anchor='middle')]
    for x, product in zip((365, 465, 565), products):
        p += label_box(x, 145, 70, 55, str(product))
        p += [line(x+35, 200, x+35, 225, MUTED)]
    p += [line(400, 225, 600, 225, MUTED),
          line(500, 225, 500, 255, MUTED, arrow=True)]
    p += [rect(380, 255, 240, 85, '#FFFFFF', LIGHT),
          text(500, 289, 'Reduktion + Bias', 25, anchor='middle'),
          text(500, 326, 'Ergebnis 14', 25, RED, anchor='middle'),
          text(500, 395, 'Produkte dann summieren', 22, anchor='middle')]

    # NPU: a possible weight-stationary sum chain, not a universal architecture.
    p += [text(830, 125, 'Ladbare Gewichte', 23, anchor='middle')]
    for i, (weight, value) in enumerate(zip(WEIGHTS, INPUTS)):
        x = 728+i*80
        p += label_box(x, 140, 60, 40, str(weight), 26, accent=True)
        # Weight and activation enter at different top ports.
        p += [arrow_path([(x+30, 180), (x+30, 195), (x+15, 195), (x+15, 250)]),
              text(x+47, 228, str(value), 25, anchor='middle'),
              line(x+47, 234, x+47, 250, MUTED, arrow=True)]
        p += label_box(x, 250, 60, 55, 'MAC', 23)
        p += [text(x+30, 335, str(sums[i+1]), 26, RED if i==2 else INK, anchor='middle')]
        if i < 2:
            p += [line(x+60, 277, x+80, 277, MUTED, arrow=True)]
    p += [text(701, 264, str(BIAS), 25, anchor='middle'),
          line(691, 277, 728, 277, MUTED, arrow=True),
          text(830, 365, 'Startsumme: Bias 1', 22, anchor='middle'),
          text(830, 395, 'Gewichte bleiben lokal', 22, anchor='middle')]
    save(NAME, 'Dieselbe Ausgabesumme: drei beispielhafte Datenwege', 415, p)


def rasterize(chromium):
    from playwright.sync_api import sync_playwright
    source = OUT/(NAME+'.svg')
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=chromium, args=['--no-sandbox'])
        page = browser.new_page(viewport={'width': 1000, 'height': 415}, device_scale_factor=2)
        page.set_content('<html><body style="margin:0;background:white">'+source.read_text(encoding='utf-8')+'</body></html>')
        page.evaluate('document.fonts.ready')
        page.locator('svg').screenshot(path=str(source.with_suffix('.png')))
        browser.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--png', action='store_true')
    parser.add_argument('--chromium', default='/usr/bin/chromium')
    args = parser.parse_args()
    comparison()
    if args.png:
        rasterize(args.chromium)
    print('CPU/GPU/NPU-Vergleich: SVG'+(' und PNG' if args.png else ''))
