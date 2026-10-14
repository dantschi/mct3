#!/usr/bin/env python3
"""Reproduzierbare Lehrdiagramme für VL01; keine Messdaten oder Transistorsimulationen.

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


def marked_box(x, y, w, h, labels):
    result = box(x, y, w, h, labels)
    result[0] = rect(x, y, w, h, BG, RED)
    return result


def cycle_grid(name, title, rows, cycles, events, caption):
    x0, bw, bh, top = 175, 800/cycles, 44, 92
    p = [text(20, 30, title)]
    for c in range(1, cycles+1):
        p += [text(x0+(c-.5)*bw, 72, c, 22, anchor="middle")]
    for r, label in enumerate(rows):
        y = top+r*bh
        p += [text(20, y+29, label, 23)]
        for c in range(1, cycles+1):
            p += [rect(x0+(c-1)*bw, y, bw-3, bh-4, "#FFFFFF", LIGHT, 0)]
    for row, cycle, label, final in events:
        x=x0+(cycle-1)*bw; y=top+row*bh
        p += [rect(x+2, y+2, bw-7, bh-8, BG, RED if final else LIGHT, 5),
              text(x+(bw-3)/2, y+28, label, 22, anchor="middle")]
    bottom=top+len(rows)*bh
    p += [text(980, bottom+35, "Takt →", 22, anchor="end"),
          text(500, bottom+76, caption, 23, anchor="middle")]
    save(name, title, bottom+105, p)




IMAGES = OUT.parents[1]/"images"/"01_speicherphysik"


def save_circuit(name, title, height, elements):
    global OUT
    old = OUT
    OUT = IMAGES
    OUT.mkdir(parents=True, exist_ok=True)
    save(name, title, height, elements)
    OUT = old


def dot(x, y):
    return f'<circle cx="{x}" cy="{y}" r="4" fill="{MUTED}"/>'


def gate(x, y, name="1"):
    return [rect(x, y, 100, 70, "#FFFFFF", LIGHT, 0),
            text(x+50, y+45, name, 28, anchor="middle"),
            f'<circle cx="{x+106}" cy="{y+35}" r="6" fill="#FFFFFF" stroke="{MUTED}" stroke-width="2"/>']


def table_rows(rows, xs, top=100, step=50):
    p = []
    for i, row in enumerate(rows):
        for x, s in zip(xs, row):
            p.append(text(x, top+i*step, s, 24))
    return p


def figures():
    save("tools-flow", "Werkzeugfolge und getrennte Ausführungsebenen", 285,
         box(20,65,185,90,["C-Quelltext"])+box(265,65,190,90,["Compiler", "Objektdateien"])+
         box(515,65,190,90,["Linker", "ELF-Abbild"])+box(765,65,215,90,["Zielplattform", "oder Renode"])+
         [line(205,110,260,110,MUTED,arrow=True),line(455,110,510,110,MUTED,arrow=True),line(705,110,760,110,MUTED,arrow=True),
          text(500,225,"Ausführen benötigt Plattform und Startcode; Zellphysik ist eine eigene Ebene.",22,anchor="middle")])
    p=box(30,120,170,85,["CPU"])+box(285,90,220,145,["Interconnect"])
    p += [line(200,162,285,162,MUTED),line(505,162,585,162,MUTED),line(585,60,585,355,MUTED)]
    for y,labels in [(20,["internes Flash"]),(125,["internes SRAM"]),(230,["Peripherie"])]:
        p+=box(650,y,290,80,labels)+[line(585,y+40,650,y+40,RED if y==125 else MUTED)]
    p+=box(650,335,290,80,["DRAM-Controller"])+[path([(585,355),(585,375),(650,375)],MUTED),text(500,458,"Optionaler Controller → externes DRAM",24,anchor="middle")]
    save("soc-interconnect","Ein SoC mit optionalem externem DRAM-Pfad",490,p)
    save("cell-count","Kapazität und Zellbauteile für ein MiB",280,
         [text(500,38,"1 MiB = 1 048 576 Byte = 8 388 608 Bit",28,anchor="middle")]+
         box(30,80,445,115,["6T-SRAM", "50 331 648 Zelltransistoren"])+box(525,80,445,115,["1T1C-DRAM", "8 388 608 Transistoren", "8 388 608 Kondensatoren"])+
         [text(500,247,"Nur Zellbauteile; Decoder, Verstärker und weitere Peripherie fehlen.",22,anchor="middle")])
    p=[text(250,35,"Ein-Port-Lehrmodell",27,anchor="middle"),text(750,35,"Getrennte I-/D-Wege",27,anchor="middle")]
    p+=box(35,90,130,110,["CPU"])+box(285,90,180,110,["Code + Daten"])+[line(165,145,285,145,MUTED),text(225,235,"ein Port",23,anchor="middle")]
    p+=box(535,90,130,110,["CPU"])+box(800,70,175,75,["Befehle"])+box(800,175,175,75,["Daten"])
    p+=[path([(665,120),(730,120),(730,107),(800,107)],MUTED),path([(665,170),(730,170),(730,212),(800,212)],MUTED),
        text(500,310,"Adressraum, Portzahl und physische Speicher sind getrennte Eigenschaften.",22,anchor="middle")]
    save("von-harvard","Gemeinsamer Port gegenüber getrennten Befehls- und Datenwegen",345,p)
    cycle_grid("memory-wall","Latenz 3 Takte; unabhängige Starts jedes Taktes möglich",["Anfrage A","Anfrage B","Anfrage C","Anfrage D"],6,
               [(0,1,"Start",False),(0,3,"fertig",True),(1,2,"Start",False),(1,4,"fertig",True),(2,3,"Start",False),(2,5,"fertig",True),(3,4,"Start",False),(3,6,"fertig",True)],
               "Vier unabhängige Anfragen: letzte Antwort in Takt 6; seriell in Takt 12.")
    p=[]
    for i,(w,label) in enumerate([(320,"Register"),(500,"Caches: oft SRAM"),(680,"Arbeitsspeicher: oft DRAM"),(880,"Dauerhafte Ablage: z. B. Flash")]):
        p+=box(500-w/2,20+i*78,w,65,[label])
    p += [text(20,390,"Typisch nach unten: mehr Kapazität, längere Zugriffswege",24),text(20,429,"Keine universellen Geschwindigkeitswerte aus dem Zellnamen ableiten.",22)]
    save("hierarchy","Speicherhierarchie als Zuordnung typischer Aufgaben",460,p)
    save("rom-evolution","Lesen und Ändern der ROM-Familie",350,
         table_rows([("Bauart","Inhalt ändern","Beispielverfahren"),("Masken-ROM","nicht im Betrieb","Fertigung"),("PROM","einmalig","Programmierung"),("EPROM","löschen / programmieren","UV-Licht zum Löschen"),("EEPROM / Flash","elektrisch ändern","Granularität beachten")],[30,300,665],55,58))
    p=[rect(135,35,420,50,LIGHT,LIGHT,0),text(345,69,"Control Gate",25,anchor="middle"),
       rect(135,90,420,25,"#FFFFFF",LIGHT,0),text(580,110,"Oxid",22),
       rect(135,120,420,60,BG,LIGHT,0),text(345,158,"Floating Gate: − − −",24,anchor="middle"),
       rect(135,185,420,25,"#FFFFFF",LIGHT,0),text(580,205,"Oxid",22),
       rect(90,235,125,65,LIGHT,LIGHT,0),text(152,275,"Source",24,anchor="middle"),
       rect(475,235,125,65,LIGHT,LIGHT,0),text(537,275,"Drain",24,anchor="middle"),
       line(215,285,475,285,RED,3),text(345,265,"n-Kanal",24,anchor="middle"),
       text(660,80,"Mehr negative Ladung",24),text(660,130,"→ höhere",24,RED),text(660,165,"Schwellspannung",24,RED),
       text(500,360,"Prinzipbild: Geometrie und Spannungen sind nicht maßstäblich.",23,anchor="middle")]
    save("floating-gate","Isoliertes Gate und auslesbarer Kanal im Flash-Modell",395,p)
    p=[text(500,35,"Logisches Flash-Lehrmodell: gelöscht = FF",27,anchor="middle")]
    for i,(a,b,label) in enumerate([("FF · 11111111","A5 · 10100101","nur 1 → 0"),("A5 · 10100101","81 · 10000001","nur weitere 1 → 0"),("A5 · 10100101","AF · 10101111","0 → 1: vorher löschen")]):
        y=70+i*95;p+=box(30,y,310,65,[a])+box(460,y,310,65,[b])+[line(345,y+32,450,y+32,MUTED,arrow=True),text(795,y+38,label,21,RED if i==2 else INK)]
    p += [text(500,390,"Löschen betrifft den ganzen Modellblock; benötigte Nachbarbytes sichern.",23,anchor="middle")]
    save("flash-program-erase","Erlaubte Bitänderungen und Löschbedarf",425,p)
    p=[text(250,35,"NOR: parallele Zellpfade",26,anchor="middle"),text(750,35,"NAND: serieller Zellstrang",26,anchor="middle")]
    for x in [90,225,360]:
        p += [line(x,80,x,130,MUTED),rect(x-25,130,50,60,"#FFFFFF",LIGHT,0),text(x,170,"Z",24,anchor="middle"),line(x,190,x,245,MUTED)]
    p+=[line(90,80,360,80,MUTED),line(90,245,360,245,MUTED)]
    for y in [70,155,240]:p+=[rect(720,y,60,50,"#FFFFFF",LIGHT,0),text(750,y+34,"Z",24,anchor="middle")]
    p += [line(750,120,750,155,MUTED),line(750,205,750,240,MUTED),text(500,345,"Z = Speicherzelle; Zellverschaltung ist nicht die äußere Busbreite.",23,anchor="middle")]
    save("nand-nor","Parallele NOR-Zellpfade und serieller NAND-Zellstrang",380,p)
    p=box(25,60,150,90,["CPU Fetch"])+box(235,60,230,90,["Adressabbildung", "und Controller"])+box(525,60,200,90,["Flash-Leseweg"])+box(790,60,185,90,["Codebytes"])
    p += [line(175,105,230,105,MUTED,arrow=True),line(465,105,520,105,MUTED,arrow=True),line(725,105,785,105,MUTED,arrow=True),
          text(500,215,"XIP: Codeadresse ist über einen ausführbaren Leseweg erreichbar.",24,anchor="middle"),text(500,260,"Cachetreffer können Zugriffe bedienen, ohne erneut Flash zu lesen.",23,anchor="middle")]
    save("flash-fetch","Execute-in-Place als Eigenschaft des System-Lesewegs",295,p)
    p=[text(500,35,"Sechs physische Löschzyklen auf drei Blöcken",27,anchor="middle")]
    for i,(label,vals) in enumerate([("einseitig",[6,0,0]),("verteilt",[2,2,2])]):
        y=100+i*115;p.append(text(30,y+42,label,24))
        for j,v in enumerate(vals):p+=box(225+j*245,y,210,80,[f"Block {j}",f"{v} Löschzyklen"])
    p += [text(500,355,"Gleiche Summe, geringerer Maximalwert; Mapping und Aufwand bleiben nötig.",23,anchor="middle")]
    save("wear-leveling","Verschleißverteilung als Modell physischer Löschzyklen",390,p)
    p=[line(90,290,940,290,MUTED),line(90,290,90,45,MUTED),text(90,30,"Zellpegel",24)]
    pts=[(100,75),(245,145),(245,75),(390,145),(390,75),(535,145),(535,75),(680,145),(680,75),(825,145)]
    p+=[path(pts,RED),line(90,220,940,220,MUTED,dash=True),text(930,210,"schematische Grenze",22,anchor="end"),text(940,335,"qualitative Zeit →",23,anchor="end"),
        text(500,389,"Leckage senkt Abstand; rechtzeitiger Refresh stellt den Zustand wieder her.",23,anchor="middle")]
    save("dram-refresh","Qualitative Leckage und Auffrischung einer DRAM-Zelle",420,p)
    p=box(35,90,250,130,["Zelle isoliert", "0 V oder 1,2 V"])+box(635,90,310,130,["BL vorladen", "Vpre = 0,6 V"])
    p += [line(285,155,430,155,MUTED),line(430,155,475,120,MUTED),line(500,155,635,155,MUTED),text(470,85,"WL = 0",24,anchor="middle"),
          text(500,295,"Vorladung beenden → WL aktivieren → Ladung teilen",26,anchor="middle"),text(500,345,"Lehrmodell: Versorgung 1,2 V; Platte 0 V",23,anchor="middle")]
    save("dram-precharge","Getrennte DRAM-Zelle und vorgeladene Bitleitung",380,p)
    p=[text(500,32,"BL: hoher und niedriger Zellfall als Alternativen",25,anchor="middle")]
    x=[110,280,430,600,745,900]
    p += [line(100,160,920,160,MUTED,dash=True),text(30,167,"½ VDD",20)]
    p += [path([(110,160),(280,160),(430,140),(600,65),(745,65),(900,160)],RED),path([(110,160),(280,160),(430,180),(600,255),(745,255),(900,160)],MUTED)]
    for a,s in zip(x,["vorladen","WL ↑","teilen","Sense / Restore","WL ↓","Precharge"]):p.append(text(a,315,s,21,anchor="middle"))
    p += [text(500,372,"Restore: Zelle verbunden; Precharge: Zelle bereits getrennt.",24,anchor="middle")]
    save("dram-read-restore","Ladungsteilung, Verstärken und Wiederherstellen",410,p)
    p=[text(500,35,"4 Banken × 128 Zeilen × 64 Spalten × 2 Byte = 64 KiB",26,anchor="middle")]
    for i,(label,w) in enumerate([("Bank [15:14]",160),("Zeile [13:7]",360),("Spalte [6:1]",300),("Byte [0]",140)]):
        start=[20,180,540,840][i];p+=box(start,85,w,90,[label,["2 Bit","7 Bit","6 Bit","1 Bit"][i]])
    p+=box(35,235,425,100,["aktivierte Zeile", "64 Spalten mit je 2 Byte"])+box(580,235,370,100,["Spalte auswählen", "Byte 0 oder 1"])+[line(460,285,575,285,MUTED,arrow=True),text(500,405,"Frei gewählte Feldreihenfolge; kein universelles Controller-Mapping.",23,anchor="middle")]
    save("dram-matrix","Bank-, Zeilen-, Spalten- und Bytefelder im Lehrmodell",440,p)
    p=[]
    for i,(lab,cmds) in enumerate([("passende Zeile offen",["READ"]),("Bank geschlossen",["ACTIVATE","READ"]),("andere Zeile offen",["PRECHARGE","ACTIVATE","READ"])]):
        y=30+i*100;p.append(text(20,y+50,lab,24))
        for j,c in enumerate(cmds):
            p+=box(345+j*210,y,185,80,[c])
            if j:p.append(line(325+j*210,y+40,340+j*210,y+40,MUTED,arrow=True))
    p.append(text(500,370,"Reihenfolge ohne konkrete Befehlsabstände oder Latenzwerte",23,anchor="middle"))
    save("dram-commands","Drei DRAM-Ausgangszustände und ihre Lesevorbereitung",405,p)
    p=[text(20,34,"200 MHz · 64 Bit = 8 Byte je Transfer",26),text(25,125,"Takt",24),text(25,240,"SDR",24),text(25,330,"DDR",24)]
    p+=[digital([(0,.5,False),(.5,1,True),(1,1.5,False),(1.5,2,True),(2,2.5,False),(2.5,3,True),(3,3.5,False),(3.5,4,True),(4,4.2,False)],150,190,75,125,MUTED)]
    for t in [.5,1.5,2.5,3.5]:p += [line(150+190*t,200,150+190*t,245,MUTED),text(150+190*t,278,"8 B",22,anchor="middle")]
    for t in [.5,1,1.5,2,2.5,3,3.5,4]:p += [line(150+190*t,295,150+190*t,340,RED),text(150+190*t,372,"8 B",22,anchor="middle")]
    p += [text(500,430,"SDR: 200 MT/s, 1,6 GB/s · DDR: 400 MT/s, 3,2 GB/s",25,anchor="middle")]
    save("sdram-ddr","Ein oder zwei Transfers pro Taktperiode",465,p)
    p=box(25,100,230,100,["Port A", "Adresse / Daten"])+box(370,75,260,150,["gemeinsamer", "Speicherinhalt"])+box(745,100,230,100,["Port B", "Adresse / Daten"])
    p += [line(255,150,370,150,MUTED),line(630,150,745,150,MUTED),text(500,300,"Gleiche Adresse / Schreiben: Ergebnis laut Spezifikation.",25,anchor="middle"),text(500,350,"Ports, Zellbauart und Synchronisation getrennt prüfen.",24,anchor="middle")]
    save("dpram","Zwei Zugriffsports zu gemeinsamen Speicherinhalten",385,p)
    p=[text(500,35,"Nach A, B, C einlegen · A entnehmen · D, E einlegen",26,anchor="middle")]
    for j,s in enumerate(["E","B","C","D"]):
        p+=box(30+j*245,100,215,110,[f"Platz {j}",s])
    p += [text(382,255,"r = w = 1",27,RED,anchor="middle"),text(500,320,"count = 4 → voll; Entnahmereihenfolge B, C, D, E",25,anchor="middle"),text(500,370,"Anfangs r = w = 0, count = 0 → leer",24,anchor="middle")]
    save("fifo-ring","Vier-Plätze-Ringpuffer mit expliziter Belegung",405,p)
    p=[]
    for y,lab,start,end,last,size in [(30,"Flash","0x00000000","0x00040000","0x0003FFFF","256 KiB"),(205,"SRAM","0x10000000","0x10010000","0x1000FFFF","64 KiB")]:
        p+=box(260,y,475,100,[lab,size])+[text(20,y+35,"Start",23),text(20,y+73,start,23),text(770,y+35,"Ende exklusiv",23),text(770,y+73,end,23),text(500,y+137,f"Letztes Byte: {last}",24,anchor="middle")]
    save("memory-map","Lehr-Memory-Map mit expliziten Grenzen",380,p)
    p=[text(260,35,"Flash: Ladebild",27,anchor="middle"),text(760,35,"RAM: Laufzeitobjekte",27,anchor="middle")]
    p+=box(65,80,365,90,[".text + .rodata"])+box(65,205,365,80,[".data-Anfangswerte"])+box(580,205,350,80,[".data: veränderbar"])+box(580,315,350,80,[".bss: nullsetzen"])+box(580,425,350,65,["Stack: reservieren"])
    p += [line(430,245,575,245,RED,arrow=True),text(503,219,"kopieren",22,anchor="middle"),text(60,365,"Keine .bss-Nullbytes",25),text(60,403,"im Ladebild nötig",25)]
    save("sections-startup","Ladebild und Laufzeitbereiche im typischen Firmwaremodell",515,p)
    p=[]
    labels=["Reset-Einstieg", "Prozessor / Stack vorbereiten", ".data kopieren", ".bss nullsetzen", "main aufrufen"]
    for i,s in enumerate(labels):
        p+=box(205,20+i*80,590,60,[s])
        if i<4:p.append(line(500,80+i*80,500,95+i*80,MUTED,arrow=True))
    p += [text(500,465,"Vereinfachte Folge; zusätzliche Zielinitialisierung ist plattformabhängig.",23,anchor="middle")]
    save("startup-flow","Verantwortung des Startcodes vor der C-Anwendung",500,p)


def mos_vertical(x,y,side,p_type,label,state=None):
    """Three visible terminals; bulk connection is implicit. No ideal bypass."""
    col=INK if state is None else RED if state else MUTED
    gx=x-30 if side=="left" else x+30
    port=x-80 if side=="left" else x+80
    p=[line(x,y-55,x,y-20,MUTED),line(x,y+20,x,y+55,MUTED),line(x,y-20,x,y+20,col,4),line(gx,y-20,gx,y+20,MUTED)]
    if p_type:
        cx=gx-10 if side=="left" else gx+10
        p+=[f'<circle cx="{cx}" cy="{y}" r="6" fill="#FFFFFF" stroke="{MUTED}" stroke-width="2"/>',line(port,y,cx-6 if side=="left" else cx+6,y,MUTED)]
        p+=[line(cx+6 if side=="left" else cx-6,y,gx,y,MUTED)]
    else:p.append(line(port,y,gx,y,MUTED))
    tx=x+36 if side=="left" else x-36
    p.append(text(tx,y+6,label,24,anchor="start" if side=="left" else "end"))
    import json
    terminals={"G":[port,y],"S":[x,y-55],"D":[x,y+55]} if p_type else {"G":[port,y],"D":[x,y-55],"S":[x,y+55]}
    kind = "pMOS" if p_type else "nMOS"
    attrs = escape(json.dumps(terminals), quote=True)
    return [f'<g data-component="{label}" data-type="{kind}" data-terminals="{attrs}">',*p,"</g>"]


def mos_access(x,y,label,state):
    col=INK if state is None else RED if state else MUTED
    import json
    terminals={"G":[x,y-55],"T1":[x-55,y],"T2":[x+55,y]}
    attrs = escape(json.dumps(terminals), quote=True)
    return [f'<g data-component="{label}" data-type="nMOS" data-terminals="{attrs}">',line(x-55,y,x-20,y,MUTED),line(x+20,y,x+55,y,MUTED),line(x-20,y,x+20,y,col,4),
            line(x-20,y-30,x+20,y-30,MUTED),line(x,y-55,x,y-30,MUTED),text(x,y+60,label,24,anchor="middle"),"</g>"]


def sram(name, phase, q=None, wl=None):
    import json
    topo={"P_Q":{"type":"pMOS","G":"Q_B","S":"VDD","D":"Q"},"N_Q":{"type":"nMOS","G":"Q_B","D":"Q","S":"GND"},
          "P_QB":{"type":"pMOS","G":"Q","S":"VDD","D":"Q_B"},"N_QB":{"type":"nMOS","G":"Q","D":"Q_B","S":"GND"},
          "A_Q":{"type":"nMOS","G":"WL","T1":"BL","T2":"Q"},"A_QB":{"type":"nMOS","G":"WL","T1":"Q_B","T2":"BL_B"}}
    p=[f'<metadata id="cell-topology">{escape(json.dumps(topo,sort_keys=True))}</metadata>',text(500,28,phase,25,anchor="middle"),
       line(150,65,850,65,RED if wl==1 else MUTED),text(500,57,"WL"+(" = "+str(wl) if wl is not None else ""),24,anchor="middle"),
       line(150,65,150,195,MUTED),line(850,65,850,195,MUTED),line(330,110,670,110,MUTED),text(500,103,"VDD",24,anchor="middle"),
       line(330,110,330,115,MUTED),line(670,110,670,115,MUTED),line(330,385,330,410,MUTED),line(670,385,670,410,MUTED),
       line(330,410,670,410,MUTED),text(500,438,"GND",24,anchor="middle"),line(40,115,40,385,MUTED),line(960,115,960,385,MUTED),
       text(40,105,"BL",24,anchor="middle"),text(960,105,"BLB",24,anchor="middle"),line(40,250,95,250,MUTED),line(905,250,960,250,MUTED)]
    if name=="sram-read": bl="hoch → leicht sinkend"; blb="zunächst hoch"
    elif name=="sram-write": bl="Treiber: 1";blb="Treiber: 0"
    else:bl=blb="nicht festgelegt"
    p += [text(25,470,bl,22),text(975,470,blb,24,anchor="end")]
    states=[None]*4 if q is None else [q==1,q==0,q==0,q==1]
    for args in [(330,170,"left",True,"P_Q",states[0]),(330,330,"left",False,"N_Q",states[1]),(670,170,"right",True,"P_QB",states[2]),(670,330,"right",False,"N_QB",states[3])]:p+=mos_vertical(*args)
    p+=mos_access(150,250,"A_Q",None if wl is None else wl==1)+mos_access(850,250,"A_QB",None if wl is None else wl==1)
    # Four bridges: crossing wires remain electrically separate.
    p += [f'<path data-net="Q" d="M205,250 H238 Q250,235 262,250 H330" fill="none" stroke="{MUTED}" stroke-width="2"/>',
          f'<path data-net="Q_B" d="M670,250 H738 Q750,235 762,250 H795" fill="none" stroke="{MUTED}" stroke-width="2"/>',
          line(330,225,330,275,MUTED),line(670,225,670,275,MUTED),line(250,170,250,330,MUTED),line(750,170,750,330,MUTED),
          f'<path data-net="Q_B" d="M670,250 H590 V210 H345 Q330,195 315,210 H250" fill="none" stroke="{MUTED}" stroke-width="2"/>',
          f'<path data-net="Q" d="M330,250 H410 V290 H655 Q670,305 685,290 H750" fill="none" stroke="{MUTED}" stroke-width="2"/>',
          dot(330,250),dot(670,250),dot(250,210),dot(750,290),dot(150,65),dot(850,65),
          text(330,242,"Q"+(" = "+str(q) if q is not None else ""),24,anchor="middle"),
          text(670,242,"QB"+(" = "+str(1-q) if q is not None else ""),24,anchor="middle")]
    if name=="sram-read":p += [path([(40,250),(95,250)],RED,4),line(330,250,330,275,RED,3),line(330,385,330,410,RED,3)]
    if name=="sram-write":p += [line(905,250,960,250,RED,4)]
    save_circuit(name,phase,490,p)


def circuits():
    p=gate(230,90)+[line(80,125,230,125,MUTED),line(342,125,490,125,MUTED),text(80,105,"A",25),text(490,105,"Y",25),text(750,55,"A      Y",26,anchor="middle"),text(750,120,"0      1",28,anchor="middle"),text(750,180,"1      0",28,anchor="middle"),text(500,260,"Y = logische Negation von A",25,anchor="middle")]
    save_circuit("inverter","IEC-Inverter und Wahrheitstabelle",295,p)
    p=gate(200,110)+gate(640,110)
    p += [line(312,145,640,145,MUTED),line(752,145,815,145,MUTED),path([(815,145),(815,65),(150,65),(150,145),(200,145)],MUTED),

          text(410,130,"Q",26),text(810,130,"QB",26),text(500,315,"Stabil: Q / QB = 0 / 1 oder 1 / 0",27,anchor="middle")]
    save_circuit("inverter-pair","Zwei kreuzgekoppelte Inverter mit getrennten Knoten",350,p)
    p=mos_vertical(400,130,"left",True,"pMOS")+mos_vertical(400,290,"left",False,"nMOS")
    p += [line(400,30,400,75,MUTED),text(400,23,"VDD",24,anchor="middle"),line(400,185,400,235,MUTED),line(400,345,400,380,MUTED),text(400,415,"GND",24,anchor="middle"),line(320,130,320,290,MUTED),line(150,210,320,210,MUTED),dot(320,210),text(150,195,"A",25),line(400,210,540,210,MUTED),dot(400,210),text(550,217,"Y",25),text(680,140,"A = 0 → Y = 1",25),text(680,235,"A = 1 → Y = 0",25),text(680,330,"Bulkanschlüsse implizit",22)]
    save_circuit("cmos-inverter","Qualitativer CMOS-Inverter",440,p)
    for args in [("sram-6t","6T-Zelle: Topologie ohne Betriebszustand",None,None),("sram-hold","Halten: Q = 0 / QB = 1",0,0),("sram-read","Lesen: Vorladung aus, früher Auswertezeitpunkt",0,1),("sram-write","Schreiben 0 → 1: Beginn vor dem Kippen",0,1)]:sram(*args)
    for mode in ["read","write"]:
        labels=["Vorladung","WL","BL","BLB","Q","QB"] if mode=="read" else ["Treiber","WL","BL","BLB","Q","QB"]
        p=[text(500,28,"Qualitativ: "+("Lesen von Q = 0" if mode=="read" else "Schreiben Q: 0 → 1"),26,anchor="middle")]
        x0,scale=170,150
        intervals=[[(0,1,True),(1,4,False),(4,5,True)],[(0,1.5,False),(1.5,3.5,True),(3.5,5,False)]] if mode=="read" else [[(0,.5,False),(.5,4,True),(4,5,False)],[(0,1.5,False),(1.5,3.5,True),(3.5,5,False)]]
        for i,label in enumerate(labels):
            hi=65+i*60;lo=hi+30;p.append(text(25,hi+22,label,24))
            if i<2:p.append(digital(intervals[i],x0,scale,hi,lo,MUTED if i==0 else RED))
            elif mode=="read":
                pts=([(0,hi),(1.5,hi),(2.8,hi+10),(3.5,hi+10),(4,hi),(5,hi)] if i==2 else [(0,hi),(5,hi)] if i in [3,5] else [(0,lo),(1.5,lo),(2,lo-5),(3.5,lo),(5,lo)])
                p.append(path([(x0+scale*t,y) for t,y in pts],RED if i==2 else MUTED))
            else:
                if i in [2,3]:
                    p += [digital([(.5,4,i==2)],x0,scale,hi,lo,MUTED),rect(x0+4*scale,hi-5,scale,42,BG,LIGHT,0),text(x0+4.5*scale,hi+21,"frei",20,anchor="middle")]
                else:p.append(digital([(0,2,i==5),(2,5,i==4)],x0,scale,hi,lo,RED))
        p += [text(920,510,"Phasen → (keine absolute Zeit)",23,anchor="end")]
        save_circuit("sram-"+mode+"-timing","Qualitative SRAM-"+("Lese" if mode=="read" else "Schreib")+"folge",535,p)
    p=mos_access(380,165,"nMOS",None)
    p += [text(120,155,"BL",26),line(170,165,325,165,MUTED),line(380,50,380,110,MUTED),text(380,35,"WL",26,anchor="middle"),line(435,165,650,165,MUTED),line(650,165,650,245,MUTED),dot(650,165),text(685,174,"Zellknoten",25),
          line(600,245,700,245,MUTED,3),line(600,270,700,270,MUTED,3),line(650,270,650,355,MUTED),text(650,395,"Platte: 0 V im Modell",24,anchor="middle"),text(745,264,"Ccell",25)]
    save_circuit("dram-1t1c","Ein Zugriffstransistor und ein Zellkondensator",430,p)


def png(chromium):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        browser=pw.chromium.launch(executable_path=chromium,args=["--no-sandbox"])
        page=browser.new_page(device_scale_factor=2)
        for folder in (OUT,IMAGES):
            for f in sorted(folder.glob("*.svg")):
                # Old unused archive figures stay untouched; regenerate only generated names.
                if f.name not in GENERATED[folder]:continue
                page.set_content(f.read_text(encoding="utf-8"));page.evaluate("document.fonts.ready")
                svg=page.locator("svg");size=svg.bounding_box()
                page.set_viewport_size({"width":math.ceil(size["width"]),"height":math.ceil(size["height"])})
                svg.screenshot(path=str(f.with_suffix(".png")))
        browser.close()


GENERATED={OUT:set(),IMAGES:set()}
_original_save=save

def save(name,title,height,elements):
    GENERATED[OUT].add(name+".svg")
    _original_save(name,title,height,elements)


if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--png",action="store_true")
    ap.add_argument("--chromium",default="/usr/bin/chromium")
    args=ap.parse_args()
    figures();circuits()
    if args.png:png(args.chromium)
    print(f"VL01: {sum(map(len,GENERATED.values()))} SVG"+(" und PNG" if args.png else ""))
