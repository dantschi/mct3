#!/usr/bin/env python3
"""Berechnete Einführungsdiagramme für VL7; reine Lehrmodelle, keine Messwerte.

SVG aus der Standardbibliothek; optional --png mit vorhandenem Playwright/Chromium.
Es werden ausschließlich intro_*.svg und die zugehörigen PNGs erzeugt.
"""
from pathlib import Path
from html import escape
import argparse

OUT = Path(__file__).resolve().parent
INK, MUTED, BG, RED = '#1D1D1F', '#656D76', '#F5F5F7', '#E2001A'

def text(x, y, label, size=25, anchor='start', color=INK):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" fill="{color}">{escape(str(label))}</text>'

def rect(x, y, w, h, color=MUTED, fill=BG):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{fill}" stroke="{color}" stroke-width="2"/>'

def path(points, color=INK, arrow=True):
    d=' '.join(f'{x},{y}' for x,y in points)
    end=' marker-end="url(#arrow)"' if arrow else ''
    return f'<polyline points="{d}" fill="none" stroke="{color}" stroke-width="3"{end}/>'

def save(name, title, height, content):
    lines=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1160" height="{height}" viewBox="0 0 1160 {height}" role="img" aria-labelledby="title">',
           f'<title id="title">{escape(title)}</title>',
           '<style>text{font-family:Inter,Arial,Helvetica,sans-serif;font-weight:400}</style>',
           '<defs><marker id="arrow" markerWidth="9" markerHeight="9" refX="8" refY="3" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L8,3 L0,6" fill="#1D1D1F"/></marker></defs>',
           f'<rect width="1160" height="{height}" fill="#FFFFFF"/>',*content,'</svg>']
    (OUT/f'{name}.svg').write_text('\n'.join(lines)+'\n',encoding='utf-8')

def figures():
    # M1: vier unabhängige Befehle, fünf Ein-Takt-Stufen.
    stages=['F','D','X','M','W']
    serial={i:[5*i+j+1 for j in range(5)] for i in range(4)}
    pipeline={i:[i+j+1 for j in range(5)] for i in range(4)}
    assert max(max(v) for v in serial.values())==20
    assert max(max(v) for v in pipeline.values())==8
    p=[text(25,35,'Gleiche vier Befehle · gleiche fünf Schritte je Befehl',29)]
    x0, cw, rh = 210, 44, 38
    for top, label, schedule, end in [(95,'Ohne Überlappung',serial,20),(345,'M1: Pipeline',pipeline,8)]:
        p.append(text(25,top-22,label,27))
        for c in range(1,21):
            p.append(text(x0+(c-.5)*cw,top+10,c,21,'middle',MUTED))
        for i in range(4):
            y=top+25+i*rh
            p.append(text(25,y+26,f'I{i+1}',25))
            for j,c in enumerate(schedule[i]):
                x=x0+(c-1)*cw
                p.extend([rect(x,y,cw-3,rh-4,RED if j==4 else MUTED),text(x+(cw-3)/2,y+25,stages[j],22,'middle')])
        p.append(text(1115,top+25+4*rh+30,f'Ende nach {end} Takten',25,'end',RED))
    p.extend([text(25,598,'F: Holen · D: Dekodieren · X: Rechnen · M: Speicherphase · W: Rückschreiben',24),
              text(25,638,'Ein Takt je Zelle; keine Abhängigkeiten, Cache-Misses oder Ressourcenkonflikte.',23,color=MUTED)])
    save('intro_overlap','Vier Befehle benötigen ohne Überlappung zwanzig, in M1 acht Takte',665,p)

    # Wertfluss ist eine gerichtete Berechnung, kein Ablaufplan in Takten.
    p=[text(25,35,'Zwei Summen können unabhängig entstehen; ihre Weiterverarbeitung wartet.',27)]
    for x,y,label in [(35,95,'2'),(35,205,'3'),(35,345,'4'),(35,455,'1')]:
        p.extend([rect(x,y,110,65),text(x+55,y+43,label,31,'middle')])
    for y,out in [(165,5),(415,5)]:
        p.extend([rect(325,y-30,170,80),text(410,y+19,'Addition',27,'middle'),rect(640,y-30,110,80),text(695,y+22,out,31,'middle'),path([(495,y+10),(630,y+10)])])
    p.extend([path([(145,127),(235,127),(235,155),(315,155)]),path([(145,237),(235,237),(235,195),(315,195)]),
              path([(145,377),(235,377),(235,405),(315,405)]),path([(145,487),(235,487),(235,445),(315,445)]),
              path([(750,175),(810,175),(810,300),(855,300)],RED),
              path([(750,425),(810,425),(810,335),(855,335)],RED),
              rect(865,280,170,80,RED),text(950,330,'5 + 5 = 10',27,'middle'),
              text(25,575,'Pfeile tragen Werte: gleiche Zahlen bedeuten nicht dieselbe Abhängigkeit.',24,color=MUTED)])
    save('intro_value_flow','Zwei unabhängige Additionen und ihr gemeinsamer Verbraucher',605,p)

    # M2-Variante: Issue in Programmfolge, zwei ALUs, Ergebnisse am Starttaktende.
    starts=[1,1,2,2]; finishes=starts[:]; retires=[2,2,3,3]
    assert starts[2]>finishes[0] and starts[2]>finishes[1]
    assert all(r>f for r,f in zip(retires,finishes))
    assert all(starts.count(c)<=2 and retires.count(c)<=2 for c in range(1,4))
    p=[text(25,35,'M2-Variante · zwei passende ALUs und höchstens zwei Starts / Retires je Takt',26)]
    labels=['I1: 2 + 3 → t0','I2: 4 + 1 → t1','I3: t0 + t1 → t2','I4: 6 XOR 3 → t3']
    x0,cw,top,rh=430,220,110,75
    for c in range(1,4):p.append(text(x0+(c-.5)*cw,82,f'Takt {c}',27,'middle'))
    for i,label in enumerate(labels):
        y=top+i*rh
        p.append(text(25,y+43,label,27))
        for c in range(1,4):p.append(rect(x0+(c-1)*cw,y,cw-10,rh-12,fill='#FFFFFF'))
        x=x0+(starts[i]-1)*cw
        p.extend([rect(x+4,y+4,cw-18,rh-20),text(x+(cw-10)/2,y+42,'Start → Ende',25,'middle')])
        x=x0+(retires[i]-1)*cw
        p.extend([rect(x+4,y+4,cw-18,rh-20,RED),text(x+(cw-10)/2,y+42,'Retire',25,'middle',RED)])
    p.extend([text(25,465,'I3 startet erst, wenn beide Werte 5 seit Ende Takt 1 bereitliegen.',26),
              text(25,513,'Ergebnisse: t0 = 5, t1 = 5, t2 = 10, t3 = 5; letzter Retire in Takt 3.',25),
              text(25,560,'Start am Taktbeginn · Fertigstellung am Taktende · Retire frühestens im Folgetakt',23,color=MUTED)])
    save('intro_dual_issue','Zweifachstart mit einem gemeinsamen abhängigen Verbraucher',590,p)

def rasterize(chromium):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path=chromium,headless=True,args=['--no-sandbox'])
        page=browser.new_page(viewport={'width':1160,'height':700},device_scale_factor=2)
        for source in OUT.glob('intro_*.svg'):
            page.set_content('<html><body style="margin:0;background:white">'+source.read_text(encoding='utf-8')+'</body></html>')
            page.locator('svg').screenshot(path=str(source.with_suffix('.png')))
        browser.close()

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--png',action='store_true')
    parser.add_argument('--chromium',default='/usr/bin/chromium')
    args=parser.parse_args()
    figures()
    if args.png:rasterize(args.chromium)
    print('Drei Einführungsdiagramme mit geprüften Lehrwerten erzeugt.')
