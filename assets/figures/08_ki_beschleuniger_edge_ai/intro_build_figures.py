#!/usr/bin/env python3
"""Eigene KI-Grundlagenbilder; Zahlen sind didaktische Annahmen, keine Messdaten.

SVG: Python-Standardbibliothek. Optional PNG: --png mit vorhandenem Chromium.
"""
from html import escape
from pathlib import Path
import argparse

OUT = Path(__file__).resolve().parent
INK, MUTED, RED, BG = '#1D1D1F', '#656D76', '#E2001A', '#F5F5F7'

def txt(x,y,s,size=25,color=INK,anchor='middle'):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}">{escape(str(s))}</text>'

def line(x1,y1,x2,y2,arrow=False,color=MUTED,width=2.5):
    marker=' marker-end="url(#arrow)"' if arrow else ''
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"{marker}/>'

def circle(x,y,r=37,label='',red=False):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="#FFFFFF" stroke="{RED if red else MUTED}" stroke-width="2.5"/>'+txt(x,y+8,label)

def save(name,title,items,height=420):
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="{height}" viewBox="0 0 1000 {height}" role="img" aria-labelledby="title">
<title id="title">{escape(title)}</title>
<style>text{{font-family:Inter,Arial,Helvetica,sans-serif}}</style>
<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0 0 L7 3 L0 6" fill="{MUTED}"/></marker></defs>
<rect width="1000" height="{height}" fill="#FFFFFF"/>
'''+''.join(items)+'</svg>\n'
    (OUT/f'{name}.svg').write_text(svg,encoding='utf-8')

def neuron():
    p=[txt(500,32,'Eine Recheneinheit: gewichten, summieren, aktivieren',27)]
    p += [line(172,131,398,194,True),line(172,269,398,206,True),
          line(435,113,435,157,True),line(473,200,580,200,True),line(763,200,845,200,True)]
    p += [circle(135,120,label='2'),circle(135,280,label='−1'),circle(435,82,30,'−1'),
          circle(435,200,43,'Σ'),circle(890,200,43,'1',True)]
    p += [txt(135,62,'x₀',23),txt(135,342,'x₁',23),txt(270,122,'Gewicht 3',24),txt(268,289,'Gewicht 4',24),
          txt(540,90,'Bias',24,anchor='start'),txt(527,177,'z = 1',24),txt(889,270,'a = 1',24)]
    p += [f'<rect x="594" y="135" width="154" height="130" rx="10" fill="{BG}" stroke="{MUTED}" stroke-width="2.5"/>',
          txt(672,167,'ReLU',25),line(614,240,730,240),line(658,248,658,183),
          txt(735,251,'z',19),txt(645,186,'a',19),
          line(620,240,658,240,color=RED,width=4),line(658,240,714,188,color=RED,width=4),
          txt(500,392,'z = 3 · 2 + 4 · (−1) − 1 = 1;   a = max(0, z)',25)]
    save('intro_neuron','Gewichtete Summe mit Bias und ReLU',p)

def matrix(x,y,values,highlight_row=None,highlight_col=None,highlight_cell=None):
    p=[];cellw=62;cellh=55
    for i,row in enumerate(values):
        for j,v in enumerate(row):
            highlighted=i==highlight_row or j==highlight_col or (i,j)==highlight_cell
            if highlighted:
                p.append(f'<rect x="{x+j*cellw}" y="{y+i*cellh}" width="{cellw}" height="{cellh}" rx="5" fill="{BG}"/>')
            p.append(txt(x+j*cellw+cellw/2,y+i*cellh+36,v,27,RED if highlighted else INK))
    h=len(values)*cellh;w=len(values[0])*cellw
    for xx,s in ((x-9,1),(x+w+9,-1)):
        p += [line(xx,y,xx,y+h),line(xx,y,xx+s*8,y),line(xx,y+h,xx+s*8,y+h)]
    return p

def batch():
    p=[txt(500,32,'Eine Zeile trifft eine Eingabespalte',27)]
    p += [txt(132,95,'W: 2 × 2'),txt(355,95,'X: 2 × 2'),txt(582,95,'Bias je Spalte'),txt(820,95,'Z: 2 × 2')]
    p += matrix(70,126,[[3,4],[-2,1]],highlight_row=0)
    p += matrix(292,126,[[2,0],[-1,3]],highlight_col=1)
    p += matrix(520,126,[[-1,-1],[2,2]])
    p += matrix(758,126,[[1,11],[-3,5]],highlight_cell=(0,1))
    p += [txt(238,194,'×',36),txt(476,194,'+',36),txt(700,194,'=',36),
          txt(582,275,'2 Parameter',22,MUTED),
          txt(355,275,'Eingabe 1 | Eingabe 2',22,MUTED),
          txt(500,335,'Z₀₁ = 3 · 0 + 4 · 3 − 1 = 11',27),
          txt(500,383,'ReLU wirkt anschließend auf jeden Eintrag: [[1, 11], [0, 5]]',24)]
    save('intro_batch','Matrixprodukt mit zwei Eingabespalten und Bias',p)

def layers():
    p=[txt(500,32,'Mehrere Schichten bilden eine neue Rechenfolge',27)]
    for yi in (135,285):
        for yh in (135,285):
            p.append(line(160,yi,427,yh,True))
    p += [line(506,135,810,210,True),line(506,285,810,210,True)]
    p += [circle(120,135,label='2'),circle(120,285,label='−1'),
          circle(468,135,40,'1',True),circle(468,285,40,'0',True),circle(852,210,42,'2',True)]
    p += [txt(120,83,'Eingabe x'),txt(470,83,'h = ReLU(W₁x + b₁)'),txt(850,135,'Ausgabe'),
          txt(663,135,'Gewicht 2',24),txt(661,310,'Gewicht −1',24),
          txt(500,365,'h = [1, 0]ᵀ;   y = [2, −1] · h = 2',26),
          txt(500,406,'Ohne Nichtlinearität bleiben mehrere affine Schichten insgesamt affin.',23,MUTED)]
    save('intro_layers','Zwei Eingaben, zwei nichtlineare Zwischenwerte und eine Ausgabesumme',p,height=440)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--png',action='store_true');args=parser.parse_args()
    neuron();batch();layers()
    if args.png:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
            for name in ('intro_neuron','intro_batch','intro_layers'):
                page=browser.new_page(viewport={'width':1000,'height':500})
                page.set_content('<style>body{margin:0}</style>'+(OUT/f'{name}.svg').read_text(encoding='utf-8'))
                page.locator('svg').screenshot(path=str(OUT/f'{name}.png'))
                page.close()
            browser.close()

if __name__=='__main__':main()
