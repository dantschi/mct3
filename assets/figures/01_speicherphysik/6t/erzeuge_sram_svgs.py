#!/usr/bin/env python3
"""Eigenständige Lehrzeichnungen: 6T-CMOS-SRAM, keine analoge Simulation.

Nur Python-Standardbibliothek erforderlich. Ausgabe im Verzeichnis dieses Skripts.
Geometrische Leitungsnetze werden unabhängig gegen eine Solltopologie geprüft.
"""
from pathlib import Path
from xml.sax.saxutils import escape
import json
import textwrap
import re
import math
import xml.etree.ElementTree as ET

OUT = Path(__file__).resolve().parent
COL = {'ink':'#172b46', 'muted':'#586a80', 'wire':'#334155',
       'bl':'#1769bf', 'wl':'#b85d09', 'feedback':'#7544a5',
       'on':'#16734e', 'off':'#8391a2', 'panel':'#f4f7fb', 'border':'#ced8e4'}
EXPECTED = {
    'P_Q': {'type':'pMOS', 'G':'Q_B', 'S':'VDD', 'D':'Q'},
    'N_Q': {'type':'nMOS', 'G':'Q_B', 'D':'Q', 'S':'GND'},
    'P_QB': {'type':'pMOS', 'G':'Q', 'S':'VDD', 'D':'Q_B'},
    'N_QB': {'type':'nMOS', 'G':'Q', 'D':'Q_B', 'S':'GND'},
    'A_Q': {'type':'nMOS', 'G':'WL', 'T1':'BL', 'T2':'Q'},
    'A_QB': {'type':'nMOS', 'G':'WL', 'T1':'Q_B', 'T2':'BL_B'},
}

class Drawing:
    def __init__(self, title, subtitle, width=1680, height=1120):
        self.width, self.height = width, height
        self.parts = []
        self.nets = []
        self.components = []
        self.bridges = [(430,330), (570,330)]
        self.title, self.subtitle = title, subtitle
        self.rect(0, 0, width, height, fill='white', stroke='none')
        self.text(48, 60, title, 40, weight='700')
        self.text(48, 101, subtitle, 24, color=COL['muted'])
        self.path(f'M 48 126 H {width-48}', COL['border'], 2)

    def text(self, x, y, s, size=24, color=None, anchor='start', weight='400'):
        self.parts.append(f'<text x="{x}" y="{y}" font-family="DejaVu Sans,Arial,sans-serif" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="{color or COL["ink"]}">{escape(str(s))}</text>')

    def lines(self, x, y, lines, size=24, color=None, step=34, width=None):
        for line in lines:
            wrapped = textwrap.wrap(line, width=width, break_long_words=False, break_on_hyphens=False) if width else [line]
            for row in wrapped or ['']:
                self.text(x, y, row, size, color)
                y += step
        return y

    def rect(self, x, y, w, h, fill=None, stroke=None, rx=12, dash=None):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill or COL["panel"]}" stroke="{stroke or COL["border"]}" stroke-width="2"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')

    def path(self, d, color=None, width=4, dash=None, arrow=False):
        self.parts.append(f'<path d="{d}" fill="none" stroke="{color or COL["wire"]}" stroke-width="{width}" stroke-linejoin="round" stroke-linecap="round"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
        if arrow:
            # Explicit triangles also render in SVG-to-PDF converters without
            # support for SVG marker-end. Arrow paths here use absolute M/H/V.
            tokens=re.findall(r'[MHV]|-?\d+(?:\.\d+)?',d)
            x=y=0.;prev=(0.,0.);i=0
            while i<len(tokens):
                cmd=tokens[i];i+=1;prev=(x,y)
                if cmd=='M':x=float(tokens[i]);y=float(tokens[i+1]);i+=2
                elif cmd=='H':x=float(tokens[i]);i+=1
                elif cmd=='V':y=float(tokens[i]);i+=1
                else:raise ValueError('Unsupported arrow path')
            dx,dy=x-prev[0],y-prev[1];length=math.hypot(dx,dy)
            ux,uy=dx/length,dy/length;head=width*3.2;wing=width*1.45
            ax,ay=x-head*ux,y-head*uy
            points=f'{x},{y} {ax-wing*uy},{ay+wing*ux} {ax+wing*uy},{ay-wing*ux}'
            self.parts.append(f'<polygon points="{points}" fill="{color or COL["wire"]}"/>')

    def circle(self, x, y, r=6, fill=None, stroke=None, width=2):
        self.parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill or COL["wire"]}" stroke="{stroke or fill or COL["wire"]}" stroke-width="{width}"/>')

    def net(self, name, pts, color=None, d=None):
        # pts sind die tatsächlichen elektrischen Knoten. Ein Brückenbogen
        # kreuzt einen anderen Leiter ausdrücklich ohne gemeinsame Verbindung.
        self.nets.append({'net':name, 'points':pts})
        data = json.dumps(pts, separators=(',',':'))
        d = d or 'M '+' L '.join(f'{x} {y}' for x,y in pts)
        self.parts.append(f'<path data-net="{name}" data-points="{escape(data)}" d="{d}" fill="none" stroke="{color or COL["wire"]}" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"/>')

    def card(self, y, title, lines, height, width=41):
        self.rect(1070, y, 562, height)
        self.text(1094, y+39, title, 26, weight='700')
        end=self.lines(1094, y+78, lines, 23, step=33, width=width)
        assert end-33+6 <= y+height-12, f'Text exceeds card: {title}'
        return end

    def footer(self):
        self.text(48, 1049, 'Vereinfachte 3-polige MOS-Symbole: Kreis am Gate = pMOS; Bulkanschlüsse sind ausgeblendet.', 20, COL['muted'])
        self.text(48, 1081, 'Bulk-Annahme: pMOS an VDD, nMOS an GND. Lehrschema; kein Größen-, Strom- oder Zeitmaßstab.', 20, COL['muted'])

    def write(self, filename, metadata=None):
        definitions=[]
        for c in COL.values():
            definitions.append(f'<marker id="arrow-{c[1:]}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 Z" fill="{c}"/></marker>')
        meta={'purpose':'didactic 6T SRAM schematic; not a simulation', 'components':self.components,
              'wires':self.nets, 'nonconnecting_crossings':self.bridges, **(metadata or {})}
        svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}" viewBox="0 0 {self.width} {self.height}" role="img" aria-labelledby="title desc">\n'
        svg+=f'<title id="title">{escape(self.title)}</title><desc id="desc">{escape(self.subtitle)}</desc>\n'
        svg+='<metadata id="electrical-topology">'+escape(json.dumps(meta,ensure_ascii=False))+'</metadata>\n'
        svg+='<defs>'+''.join(definitions)+'</defs>\n'+'\n'.join(self.parts)+'\n</svg>\n'
        path=OUT/filename
        path.write_text(svg,encoding='utf-8')
        return path

def vertical_mos(d, name, x, y, typ, direction, state, gates, source, drain):
    sign=1 if direction=='right' else -1
    gate_x=x+sign*30
    port_x=x+sign*60
    color=COL['on'] if state=='an' else COL['off'] if state=='aus' else COL['ink']
    d.parts.append(f'<g id="device-{name}" data-device="{name}" data-type="{typ}">')
    # Source/Drain-Leads end at the symbol channel; no bypass wire exists.
    d.path(f'M {x} {y-55} V {y-25}', COL['wire'])
    d.path(f'M {x} {y+25} V {y+55}', COL['wire'])
    d.path(f'M {x} {y-25} V {y+25}', color, 5)
    d.path(f'M {gate_x} {y-25} V {y+25}', COL['wire'], 3)
    if typ=='pMOS':
        center=gate_x+sign*9
        d.path(f'M {port_x} {y} H {center+sign*7}', COL['wire'], 3)
        d.path(f'M {gate_x} {y} H {center-sign*7}', COL['wire'], 3)
        d.circle(center,y,7,fill='white',stroke=COL['wire'],width=3)
    else:
        d.path(f'M {port_x} {y} H {gate_x}', COL['wire'], 3)
    label_x=x-sign*54
    anchor='end' if sign==1 else 'start'
    d.text(label_x, y+3, name, 23, anchor=anchor, weight='700')
    info=typ+(f' · {state}' if state else '')
    d.text(label_x, y+30, info, 19, color=COL['on'] if state=='an' else COL['muted'], anchor=anchor)
    d.parts.append('</g>')
    spt=(x,y-55) if typ=='pMOS' else (x,y+55)
    dpt=(x,y+55) if typ=='pMOS' else (x,y-55)
    d.components.append({'name':name,'type':typ,'ports':{'G':{'xy':(port_x,y),'net':gates},'S':{'xy':spt,'net':source},'D':{'xy':dpt,'net':drain}}})

def access_mos(d,name,x,y,state,left,right):
    color=COL['on'] if state=='an' else COL['off'] if state=='aus' else COL['ink']
    d.parts.append(f'<g id="device-{name}" data-device="{name}" data-type="nMOS">')
    d.path(f'M {x-55} {y} H {x-25}', COL['wire'])
    d.path(f'M {x+25} {y} H {x+55}', COL['wire'])
    d.path(f'M {x-25} {y} H {x+25}',color,5)
    d.path(f'M {x-25} {y-30} H {x+25}',COL['wire'],3)
    d.path(f'M {x} {y-55} V {y-30}',COL['wire'],3)
    d.text(x,y+54,name,23,anchor='middle',weight='700')
    access_state={'an':'aktiviert','aus':'gesperrt'}.get(state)
    d.text(x,y+82,'nMOS'+(f' · {access_state}' if access_state else ''),19,color=COL['on'] if state=='an' else COL['muted'],anchor='middle')
    d.parts.append('</g>')
    d.components.append({'name':name,'type':'nMOS','ports':{'G':{'xy':(x,y-55),'net':'WL'},'T1':{'xy':(x-55,y),'net':left},'T2':{'xy':(x+55,y),'net':right}}})

def states(q, wl):
    return {'P_Q':'an' if q else 'aus','N_Q':'aus' if q else 'an',
            'P_QB':'aus' if q else 'an','N_QB':'an' if q else 'aus',
            'A_Q':'an' if wl else 'aus','A_QB':'an' if wl else 'aus'}

def circuit(d, q=None, wl=None, mode='base'):
    st=states(q,wl) if q is not None else {name:None for name in EXPECTED}
    d.parts.append('<g id="cell-and-periphery" transform="translate(48 190)">')
    d.rect(110,85,780,535,fill='white',stroke=COL['border'],dash='8 7')
    d.text(128,600,'6T-Zelle',20,COL['muted'])
    # Bitlines and common wordline are separate nets.
    d.net('BL',[(80,45),(80,330),(80,650)],COL['bl'])
    d.net('BL_B',[(920,45),(920,330),(920,650)],COL['bl'])
    d.net('WL',[(125,60),(180,60),(820,60)],COL['wl'])
    d.net('WL',[(180,60),(180,275)],COL['wl'])
    d.net('WL',[(820,60),(820,275)],COL['wl'])
    for x in (180,820):d.circle(x,60,5,COL['wl'])
    d.text(500,44,'WL'+(f' = {wl}' if wl is not None else ''),26,COL['wl'],anchor='middle',weight='700')
    d.text(80,0,'BL',26,COL['bl'],anchor='middle',weight='700')
    d.text(920,0,'BL_B',26,COL['bl'],anchor='middle',weight='700')
    if mode=='read':
        d.text(80,30,'VDD − ΔV',20,COL['bl'],anchor='middle')
        d.text(920,30,'≈ VDD',20,COL['bl'],anchor='middle')
    elif mode=='write':
        d.text(80,30,'1 ≈ VDD',20,COL['bl'],anchor='middle')
        d.text(920,30,'0 ≈ GND',20,COL['bl'],anchor='middle')
    elif mode in ('hold','end'):
        d.text(80,30,'Zelle isoliert',18,COL['muted'],anchor='middle')
        d.text(920,30,'Zelle isoliert',18,COL['muted'],anchor='middle')

    d.net('VDD',[(350,110),(500,110),(650,110)])
    d.net('VDD',[(350,110),(350,145)])
    d.net('VDD',[(650,110),(650,145)])
    d.text(500,98,'VDD',25,anchor='middle',weight='700')
    d.net('GND',[(350,570),(500,570),(650,570)])
    d.net('GND',[(350,515),(350,570)])
    d.net('GND',[(650,515),(650,570)])
    d.path('M 500 570 V 582 M 481 582 H 519 M 486 590 H 514 M 492 598 H 508',COL['wire'],3)
    d.text(700,579,'GND',24)

    d.net('Q',[(350,255),(350,330),(350,405)],COL['feedback'])
    d.net('Q_B',[(650,255),(650,330),(650,405)],COL['feedback'])
    d.net('Q',[(235,330),(350,330)],COL['feedback'])
    d.net('Q_B',[(650,330),(765,330)],COL['feedback'])
    d.net('BL',[(80,330),(125,330)],COL['bl'])
    d.net('BL_B',[(875,330),(920,330)],COL['bl'])

    # Common inverter inputs; the two bridges explicitly do not connect.
    d.net('Q_B',[(430,200),(430,390),(430,460)],COL['feedback'])
    d.net('Q_B',[(410,200),(430,200)],COL['feedback'])
    d.net('Q_B',[(410,460),(430,460)],COL['feedback'])
    d.net('Q',[(570,200),(570,270),(570,460)],COL['feedback'])
    d.net('Q',[(590,200),(570,200)],COL['feedback'])
    d.net('Q',[(590,460),(570,460)],COL['feedback'])
    # White clearance below each jump makes the crossing unambiguous
    # even when both independent nets use the same colour.
    d.path('M 419 330 Q 430 314 441 330','white',11)
    d.path('M 581 330 Q 570 346 559 330','white',11)
    d.net('Q',[(350,330),(480,330),(480,270),(570,270)],COL['feedback'],
          'M 350 330 H 419 Q 430 314 441 330 H 480 V 270 H 570')
    d.net('Q_B',[(650,330),(520,330),(520,390),(430,390)],COL['feedback'],
          'M 650 330 H 581 Q 570 346 559 330 H 520 V 390 H 430')

    vertical_mos(d,'P_Q',350,200,'pMOS','right',st['P_Q'],'Q_B','VDD','Q')
    vertical_mos(d,'N_Q',350,460,'nMOS','right',st['N_Q'],'Q_B','GND','Q')
    vertical_mos(d,'P_QB',650,200,'pMOS','left',st['P_QB'],'Q','VDD','Q_B')
    vertical_mos(d,'N_QB',650,460,'nMOS','left',st['N_QB'],'Q','GND','Q_B')
    access_mos(d,'A_Q',180,330,st['A_Q'],'BL','Q')
    access_mos(d,'A_QB',820,330,st['A_QB'],'Q_B','BL_B')
    for x,y in [(350,110),(650,110),(350,570),(650,570)]:d.circle(x,y,5)
    for x,y in [(350,330),(650,330),(430,390),(570,270)]:d.circle(x,y,6,COL['feedback'])
    for x in (80,920):d.circle(x,330,5,COL['bl'])
    d.text(350,307,'Q'+(f' = {q}' if q is not None else ''),26,COL['feedback'],anchor='middle',weight='700')
    d.text(650,307,'Q_B'+(f' = {1-q}' if q is not None else ''),26,COL['feedback'],anchor='middle',weight='700')
    if mode=='read':
        # Arrows are overlays on existing conductor segments, not new wires.
        d.path('M 80 220 V 300',COL['on'],5,arrow=True)
        d.path('M 250 330 H 325',COL['on'],5,arrow=True)
        d.path('M 350 350 V 392',COL['on'],5,arrow=True)
        d.path('M 350 526 V 558',COL['on'],5,arrow=True)
        d.text(95,477,'I_Lesen',24,COL['on'],weight='700')
        d.net('BL',[(80,650),(80,725),(350,725)],COL['bl'])
        d.net('BL_B',[(920,650),(920,725),(650,725)],COL['bl'])
        d.rect(350,680,300,95,fill='#edf4fc',stroke=COL['bl'])
        d.text(500,716,'SA',26,COL['bl'],anchor='middle',weight='700')
        d.text(500,749,'Leseverstärker · extern',20,COL['bl'],anchor='middle')
        d.path('M 500 775 V 820',COL['bl'],4,arrow=True)
        d.text(540,815,'D_OUT = 0',25,COL['bl'],weight='700')
        d.text(500,655,'Auswertung: Vorladung ist deaktiviert',22,COL['muted'],anchor='middle')
    elif mode=='write':
        d.path('M 650 119 V 139',COL['on'],5,arrow=True)
        d.path('M 650 265 V 312',COL['on'],5,arrow=True)
        d.path('M 675 330 H 748',COL['on'],5,arrow=True)
        d.path('M 920 460 V 535',COL['on'],5,arrow=True)
        for x,label in [(80,'BL = 1'),(920,'BL_B = 0')]:
            d.net('BL' if x==80 else 'BL_B',[(x,650),(x,675)],COL['bl'])
            d.rect(x-76,675,152,91,fill='#edf4fc',stroke=COL['bl'])
            d.text(x,710,'Treiber',22,COL['bl'],anchor='middle',weight='700')
            d.text(x,744,label,21,COL['bl'],anchor='middle')
        d.text(500,715,'Externe Schreibtreiber',24,COL['muted'],anchor='middle')
        d.text(500,756,'Startpegel gezeigt; Q_B wird zuerst abgesenkt.',22,COL['muted'],anchor='middle')
    else:
        d.text(500,682,'BL und BL_B: externe Bitleitungen',23,COL['bl'],anchor='middle')
        d.text(500,720,'Punkt = Verbindung · Brücke = keine Verbindung',23,COL['muted'],anchor='middle')
    d.parts.append('</g>')
    return st

def state_table(d,y,st,title='Transistorzustände'):
    d.rect(1070,y,562,337)
    d.text(1094,y+39,title,26,weight='700')
    for i,name in enumerate(EXPECTED):
        yy=y+83+i*40
        d.text(1094,yy,name,23,weight='700')
        d.text(1262,yy,EXPECTED[name]['type'],22,COL['muted'])
        label=({'an':'aktiviert','aus':'gesperrt'}[st[name]] if name.startswith('A_') else st[name])
        d.text(1490,yy,label,23,COL['on'] if st[name]=='an' else COL['muted'],weight='700')

def make_schematics():
    d=Drawing('6T-SRAM · Grundschaltung','Zwei kreuzgekoppelte CMOS-Inverter und zwei nMOS-Zugriffstransistoren')
    circuit(d)
    d.card(174,'Ein Bit · sechs Transistoren',[
        'P_Q und N_Q bilden den Inverter mit Ausgang Q.',
        'P_QB und N_QB bilden den Inverter mit Ausgang Q_B.',
        'A_Q und A_QB verbinden die Zelle mit den Bitleitungen.'],290)
    d.card(491,'Rückkopplung und Zugriff',[
        'Q_B steuert beide Gates links.',
        'Q steuert beide Gates rechts.',
        'WL steuert beide Access-Gates.',
        'Q und Q_B sind nicht direkt verbunden.'],260)
    d.card(778,'Leseschlüssel',[
        'Violett: Zell- und Rückkopplungsnetze.',
        'Blau: Bitleitungen; orange: Wortleitung.',
        'pMOS: Kreis am Gate, nicht an der Versorgung.'],220)
    d.footer()
    paths=[d.write('01_6t_sram_grundschaltung.svg')]

    d=Drawing('6T-SRAM · Halten','Beispiel Q = 0, Q_B = 1 · WL = 0 trennt die Zelle von den Bitleitungen')
    st=circuit(d,0,0,'hold')
    state_table(d,174,st)
    d.card(538,'Spannungszustand erhalten',[
        'N_Q hält Q nahe GND.',
        'P_QB hält Q_B nahe VDD.',
        'Die Rückkopplung stabilisiert beide Pegel; es kreist kein Haltestrom.'],244)
    d.card(809,'Versorgung bleibt nötig',[
        'Ideal: kein dauerhafter VDD-GND-Pfad.',
        'Real: Leckströme bleiben.',
        'Kein Refresh; dennoch flüchtig.'],188)
    d.footer()
    paths.append(d.write('02_6t_sram_halten_q0.svg',{'logic_state':{'Q':0,'Q_B':1,'WL':0},'device_states':st}))

    d=Drawing('6T-SRAM · Lesen einer 0','Auswertephase nach dem Vorladen · Q bleibt logisch 0, BL sinkt etwas ab')
    st=circuit(d,0,1,'read')
    d.card(174,'1 · Vorladen',[
        'WL zunächst 0: BL und BL_B werden auf VDD vorgeladen.',
        'Dann Vorladung deaktivieren und WL auf 1 setzen.'],225)
    d.card(426,'2 · Entladen und auswerten',[
        'Entladepfad: BL → A_Q → Q → N_Q → GND.',
        'BL_B bleibt zunächst nahe VDD.',
        'ΔV = V(BL_B) − V(BL) > 0.',
        'SA wertet die kleine Differenz aus.'],269)
    d.card(722,'3 · Lesestabilität',[
        'Q kann analog etwas ansteigen, muss jedoch logisch 0 bleiben.',
        'Die Zelle darf nicht umkippen.',
        'Nach dem Lesen WL deaktivieren.',
        'Grüne Pfeile: konventioneller Entladestrom.'],277)
    d.footer()
    paths.append(d.write('03_6t_sram_lesen_q0.svg',{'logic_state':{'Q':0,'Q_B':1,'WL':1},'device_states':st,'phase':'early read evaluation; analog Q slightly above GND'}))

    d=Drawing('6T-SRAM · Schreiben einer 1','Beginn des Umschaltens aus Q = 0, Q_B = 1 · initiale Inverterzustände gezeigt')
    st=circuit(d,0,1,'write')
    d.card(174,'1 · Schreibdaten anlegen',[
        'Zunächst WL = 0.',
        'Treiber setzen BL = 1 und BL_B = 0.',
        'Danach WL = 1: beide Access-Pfade sind aktiviert.'],237)
    d.card(438,'2 · Q_B zuerst absenken',[
        'BL_B zieht Q_B über A_QB nach unten.',
        'P_QB ist zunächst noch leitend und wirkt dem Absenken entgegen.',
        'Grüne Pfeile: anfänglicher Strom über P_QB zum Low-Schreibtreiber.'],285)
    d.card(750,'3 · Rückkopplung kippt',[
        'Q_B sinkt: P_Q schaltet ein, N_Q aus; Q steigt.',
        'Q steigt: P_QB schaltet aus, N_QB ein; Q_B sinkt weiter.',
        'Die grünen Kanäle zeigen den Anfangszustand, nicht den Endzustand.'],265)
    d.footer()
    paths.append(d.write('04_6t_sram_schreiben_beginn.svg',{'logic_state':{'Q':0,'Q_B':1,'WL':1},'device_states':st,'phase':'start of write; transistor states will change during regeneration'}))

    d=Drawing('6T-SRAM · Nach dem Schreiben','Neuer Haltezustand Q = 1, Q_B = 0 · WL wurde wieder deaktiviert')
    st=circuit(d,1,0,'end')
    state_table(d,174,st,'Zustände nach dem Umschalten')
    d.card(538,'Neuer Zustand stabil',[
        'P_Q hält Q nahe VDD.',
        'N_QB hält Q_B nahe GND.',
        'Beide Zugriffstransistoren sind gesperrt.'],218)
    d.card(783,'Schreibzyklus abschließen',[
        'WL deaktivieren, während die Schreibdaten noch gültig sind.',
        'Erst danach Schreibtreiber freigeben.',
        'Das Schreiben einer 0 erfolgt spiegelbildlich.'],230)
    d.footer()
    paths.append(d.write('05_6t_sram_schreiben_endzustand.svg',{'logic_state':{'Q':1,'Q_B':0,'WL':0},'device_states':st}))
    return paths

def axis(d,y,label,low,high):
    d.text(52,y+46,label,26,weight='700')
    d.path(f'M 225 {y-8} V {y+143} H 1480',COL['muted'],2,arrow=True)
    d.text(211,y+8,high,19,COL['muted'],anchor='end')
    d.text(211,y+138,low,19,COL['muted'],anchor='end')
    d.text(1486,y+150,'t',23,COL['muted'])
    d.path(f'M 226 {y} H 1460 M 226 {y+130} H 1460',COL['border'],1,dash='5 6')

def make_timing():
    d=Drawing('6T-SRAM · Qualitativer Lesezyklus','Spannungen über der Zeit · keine simulierten Kurven, keine Zahlenwerte',1680,980)
    for x,label in [(375,'Vorladen'),(800,'Auswerten'),(1300,'neu vorladen')]:
        d.text(x,190,label,24,anchor='middle',weight='700')
    for x in (550,1000,1160):d.path(f'M {x} 215 V 825',COL['border'],2,dash='5 7')
    axis(d,240,'WL','0','1')
    d.path('M 250 370 H 550 V 240 H 1000 V 370 H 1450',COL['wl'],5)
    axis(d,445,'BL / BL_B','0','VDD')
    d.path('M 250 445 H 1450',COL['feedback'],5)
    d.text(1480,448,'BL_B',23,COL['feedback'])
    d.path('M 250 445 H 550 C 640 450 830 479 960 484 H 1160 C 1200 447 1240 445 1280 445 H 1450',COL['bl'],5)
    d.text(1035,514,'BL',23,COL['bl'])
    d.path('M 930 448 V 480',COL['ink'],2)
    d.text(950,470,'ΔV',21)
    d.path('M 930 215 V 595',COL['on'],2,dash='4 6')
    d.text(952,418,'SA auswerten',21,COL['on'])
    axis(d,650,'Q','0','VDD')
    d.path('M 250 780 H 550 C 575 780 590 752 640 753 H 1000 C 1020 771 1060 780 1100 780 H 1450',COL['feedback'],5)
    d.text(665,720,'kleine analoge Anhebung; logisch weiterhin 0',23,COL['feedback'])
    d.text(48,890,'Vorladung aus → WL an → kleine Differenz auswerten → WL aus → erst dann erneut vorladen.',24)
    d.text(48,934,'Nicht maßstäblich. ΔV und Q-Anhebung hängen von Zell- und Peripherieauslegung ab; Q_B bleibt hier logisch 1.',20,COL['muted'])
    a=d.write('06_6t_sram_lesen_zeitverlauf.svg',{'illustration':'qualitative timing only','nonconnecting_crossings':[]})
    d=Drawing('6T-SRAM · Qualitativer Schreibzyklus','Q: 0 → 1 · Daten vor WL↑ anlegen und erst nach WL↓ freigeben',1680,980)
    for x,label in [(355,'Daten setzen'),(845,'Zelle umschalten'),(1310,'Halten')]:d.text(x,190,label,24,anchor='middle',weight='700')
    for x in (480,620,1050,1160):d.path(f'M {x} 215 V 825',COL['border'],2,dash='5 7')
    axis(d,240,'WL','0','1')
    d.path('M 250 370 H 620 V 240 H 1050 V 370 H 1450',COL['wl'],5)
    axis(d,445,'BL / BL_B','0','VDD')
    d.path('M 250 445 H 1160',COL['bl'],5)
    d.path('M 250 445 H 480 V 575 H 1160',COL['feedback'],5)
    d.text(1130,430,'BL',22,COL['bl'],anchor='end')
    d.text(1130,608,'BL_B',22,COL['feedback'],anchor='end')
    d.lines(1190,485,['Treiber frei;', 'Spannungen ab hier', 'nicht dargestellt.'],21,COL['muted'],step=30)
    axis(d,650,'Q / Q_B','0','VDD')
    d.path('M 250 780 H 730 C 780 780 790 650 910 650 H 1450',COL['bl'],5)
    d.path('M 250 650 H 670 C 735 650 760 780 860 780 H 1450',COL['feedback'],5)
    d.text(1480,659,'Q',23,COL['bl'])
    d.text(1480,785,'Q_B',23,COL['feedback'])
    d.text(48,890,'Q_B wird zuerst abgesenkt; die positive Rückkopplung hebt Q an und stabilisiert den neuen Zustand.',24)
    d.text(48,934,'Qualitative Phasenfolge, keine gemessenen Zeiten. Bitleitungen nach Treiberfreigabe sind nicht als definierte Pegel gezeichnet.',20,COL['muted'])
    b=d.write('07_6t_sram_schreiben_zeitverlauf.svg',{'illustration':'qualitative timing only','nonconnecting_crossings':[]})
    return [a,b]

def check_svg(path):
    root=ET.parse(path).getroot()
    ns={'s':'http://www.w3.org/2000/svg'}
    meta=json.loads(root.find('s:metadata',ns).text)
    if not meta['components']:
        return {'file':path.name,'xml':'ok','type':'qualitative timing, no simulation'}
    comps={x['name']:x for x in meta['components']}
    assert len(comps)==6 and set(comps)==set(EXPECTED)
    assert sum(c['type']=='pMOS' for c in comps.values())==2
    assert sum(c['type']=='nMOS' for c in comps.values())==4
    # Extract what is present in the SVG, not merely the expected circuit table.
    rendered={x.attrib['data-device']:x.attrib['data-type'] for x in root.findall('.//s:g',ns) if 'data-device' in x.attrib}
    assert rendered=={n:c['type'] for n,c in comps.items()}
    wire_nodes={}
    graphs={}
    for el in root.findall('.//s:path',ns):
        if 'data-net' not in el.attrib:continue
        net=el.attrib['data-net']
        pts=[tuple(p) for p in json.loads(el.attrib['data-points'])]
        for pt in pts:
            wire_nodes.setdefault(pt,set()).add(net)
            graphs.setdefault(net,{}).setdefault(pt,set())
        for a,b in zip(pts,pts[1:]):
            graphs[net][a].add(b); graphs[net][b].add(a)
    assert all(len(nets)==1 for nets in wire_nodes.values()),'different nets share an electrical point'
    endpoints={}
    for name,c in comps.items():
        assert c['type']==EXPECTED[name]['type']
        for pin,port in c['ports'].items():
            net=EXPECTED[name][pin]
            assert port['net']==net
            pt=tuple(port['xy'])
            assert net in wire_nodes.get(pt,set()),f'{name}.{pin} lacks its wire'
            endpoints.setdefault(net,[]).append(pt)
    for net,pts in endpoints.items():
        visited=set();todo=[pts[0]]
        while todo:
            pt=todo.pop()
            if pt in visited:continue
            visited.add(pt);todo.extend(graphs[net].get(pt,set())-visited)
        assert set(pts)<=visited,f'disconnected transistor terminals on {net}'
    if 'device_states' in meta:
        st=meta['logic_state'];q=st['Q'];qb=st['Q_B'];wl=st['WL']
        assert qb==1-q
        # Independent switch checks from gate logic (pMOS active at low gate).
        for name,c in comps.items():
            gate={'Q':q,'Q_B':qb,'WL':wl}[c['ports']['G']['net']]
            expected_on=(gate==0) if c['type']=='pMOS' else (gate==1)
            assert (meta['device_states'][name]=='an')==expected_on
    return {'file':path.name,'xml':'ok','device_count':'2 pMOS + 4 nMOS',
            'terminal_net_graph':'all six device terminals connected according to independent reference',
            'crossings':'2 nonconnecting bridges; visual verification additionally required',
            'simulation':'not performed'}

def main():
    paths=make_schematics()+make_timing()
    qa=[check_svg(p) for p in paths]
    (OUT/'topologie.json').write_text(json.dumps(EXPECTED,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (OUT/'pruefprotokoll.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'svg_count':len(paths),'results':qa},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
