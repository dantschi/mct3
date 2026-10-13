#!/usr/bin/env python3
"""Reproduzierbare Lehrdiagramme für VL08; keine Messdaten oder Schaltpläne.

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



def matrix(x, y, values, label, cell=72):
    p = [text(x+cell, y-18, label, 24, anchor="middle")]
    for i,row in enumerate(values):
        for j,value in enumerate(row):
            p += [rect(x+j*cell,y+i*cell,cell-4,cell-4),
                  text(x+j*cell+(cell-4)/2,y+i*cell+43,value,27,anchor="middle")]
    return p


def figures():
    p = [text(20,30,"Edge: Verarbeitung am Gerät oder lokalen Gateway")]
    for x,labels in [(20,["Sensor"]),(210,["Endgerät","CPU / DSP"]),
                     (465,["Gateway","lokal"]),(750,["Server","entfernt"])]:
        p += box(x,100,150 if x==20 else 220,100,labels)
    for x1,x2,c in [(170,205,RED),(430,460,RED),(685,745,MUTED)]:
        p += [line(x1,150,x2,150,c,2,arrow=True)]
    p += [text(320,245,"kurzer lokaler Weg",23,anchor="middle"),
          text(825,245,"Netzübertragung",23,anchor="middle"),
          text(500,295,"Ort allein bestimmt weder Energie noch Modellgüte",24,anchor="middle")]
    save("edge","Lokale und entfernte Verarbeitungsorte",325,p)

    p=[text(20,30,"Tensorform: Elemente und Parameter getrennt betrachten")]
    for x,labels in [(20,["x: 3 Eingänge","[2, 1, 3]"]),(270,["W: 2 × 3 Gewichte","b: 2 Biaswerte"]),
                     (650,["y: 2 Ausgänge","[14, 9]"])]:
        p += box(x,100,210 if x==20 else 300,105,labels)
    p += [line(230,152,265,152,arrow=True),line(570,152,645,152,RED,3,arrow=True),
          text(500,265,"6 Gewichte + 2 Bias = 8 Parameter · x und y sind Aktivierungen",24,anchor="middle")]
    save("tensors","Formen des Dense-Lehrbeispiels",298,p)

    p=[text(20,30,"Dense · drei Produkte je Ausgang · Bias einmal hinzufügen")]
    for y,terms,result in [(100,["1 · 2 = 2","2 · 1 = 2","3 · 3 = 9"],14),
                           (225,["0 · 2 = 0","−1 · 1 = −1","4 · 3 = 12"],9)]:
        for i,label in enumerate(terms):p += box(20+i*210,y,190,60,[label])
        p += [line(640,y+30,690,y+30,arrow=True)]
        p += marked_box(700,y-10,275,80,["Bias +1" if result==14 else "Bias −2",f"Ausgang {result}"])
    p += [text(500,345,"6 produktbezogene MACs · 8 Parameter · Ausgabe [14, 9]",24,anchor="middle")]
    save("dense","Zwei vollständige Produktsummen mit Bias",375,p)

    p=[text(20,30,"Modell R · Peak 8 Operationen/Takt · Bandbreite 8 Byte/Takt")]
    x=lambda i:130+360*i
    y=lambda v:290-28*v
    p += [line(130,40,130,290,MUTED),line(130,290,910,290,MUTED),
          text(20,365,"Ops/Takt",22),text(900,365,"Intensität I [Ops/Byte]",22,anchor="end")]
    for v in [0,2,4,6,8]:p += [text(112,y(v)+8,v,21,anchor="end"),line(127,y(v),910,y(v),LIGHT)]
    for v in [0,.25,.5,1,2]:p += [text(x(v),320,str(v).replace('.',','),21,anchor="middle")]
    p += [path([(x(0),y(0)),(x(1),y(8)),(x(2),y(8))]),
          text(790,105,"Rechenlimit 8",23,anchor="middle")]
    for i,v in [(.25,2),(.5,4)]:
        p += [f'<circle cx="{x(i)}" cy="{y(v)}" r="6" fill="{INK}"/>',
              text(x(i)+15,y(v)+25,f"{i} → {v}".replace('.',','),22)]
    p += [text(x(1)+10,55,"Knick I = 1",22)]
    save("roofline","Ideale Obergrenze durch Versorgung und Rechenpeak",390,p)

    p=[text(20,30,"A und B werden wiederverwendet · jedes Element belegt hier 4 Byte")]
    p += matrix(70,90,[[1,2],[3,4]],"A")+matrix(390,90,[[5,6],[7,8]],"B")
    p += matrix(740,90,[[19,22],[43,50]],"C = AB")
    p += [text(305,177,"×",32,anchor="middle"),text(650,177,"=",32,anchor="middle"),
          text(500,290,"8 MACs = 16 Ops · Eingangsverkehr: naiv 64 B, lokal gehalten 32 B",24,anchor="middle"),
          text(500,332,"Ein A-Wert dient zwei Spalten · ein B-Wert dient zwei Zeilen",23,anchor="middle")]
    save("tile","Dieselbe Matrixmultiplikation mit lokaler Wiederverwendung",362,p)

    p=[text(20,30,"Wertabhängigkeit und gleiche Arbeit auf getrennten Daten")]
    p += [text(20,106,"eine Summe",23)]
    for i,v in enumerate([0,2,4,13]):
        x=260+i*180;p += box(x,65,125,65,[v])
        if i<3:p += [line(x+125,97,x+175,97,RED,3,arrow=True)]
    p += [text(20,210,"zwei Ausgänge",23)]
    p += box(270,160,300,70,["Summe y0: 14"])+box(635,160,300,70,["Summe y1: 9"])
    p += [text(20,314,"viele Produkte",23)]
    for i,label in enumerate(["1 · 2","2 · 1","3 · 3","0 · 2"]):p += box(260+i*180,265,150,65,[label])
    p += [text(500,380,"Getrennte Summen sind unabhängig · Produkte bieten Datenparallelität",23,anchor="middle")]
    save("ilp","Summenabhängigkeit und unabhängige Datenarbeit",410,p)

    p=[text(20,30,"Packed SIMD · unsigned 8-Bit-Addition modulo 256 · ohne Carry zwischen Lanes")]
    vals=[[1,16,127,255],[2,32,1,1],[3,48,128,0]]
    for r,label in enumerate(["A","B","A + B"]):
        p += [text(45,110+r*75,label,24)]
        for j,v in enumerate(vals[r]):
            p += [rect(230+j*170,70+r*75,164,60, BG,RED if r==2 else LIGHT),
                  text(312+j*170,109+r*75,f"{v:02X}",27,anchor="middle")]
    p += [text(500,335,"Hexwerte · FF + 01 wird 00 in dieser Lane · kein Übertrag zum Nachbarfeld",23,anchor="middle")]
    save("simd","Vier getrennte Byte-Additionen mit definiertem Überlauf",365,p)

    p=[text(20,30,"Int8-Eingaben bedeuten nicht Int8-Produkte oder Int8-Summen")]
    p += box(20,95,180,80,["20","8-Bit-Eingabe"])+box(260,95,180,80,["20","8-Bit-Gewicht"])
    p += [text(230,146,"×",28,anchor="middle"),line(440,135,505,135,arrow=True)]
    p += marked_box(520,90,180,90,["400","Produkt"])
    p += [line(700,135,775,135,arrow=True)]
    p += marked_box(790,90,190,90,["1200","3 Produkte"])
    p += [text(500,255,"Vor der Rechnung verbreitern · anschließend Ergebnisbereich prüfen",24,anchor="middle")]
    save("wide","Breite des Produkts und Akkumulators",285,p)

    p=[text(20,30,"DSP-Lehrbild · FIR: zwei Koeffizienten und ein Eingangsfenster")]
    p += box(30,75,260,85,["Koeffizienten","1, 2"])+box(30,210,260,85,["Fensterwerte","3, 4"])
    p += [line(290,117,445,117,arrow=True),line(290,252,445,252,arrow=True)]
    p += box(460,100,270,175,["MAC","1 · 3 + 2 · 4","Akkumulator 11"])
    p += [text(500,350,"Getrennte Pfade helfen nur bei passenden Speicherbänken und Ports",23,anchor="middle")]
    save("dsp","Zwei lokale Operandenpfade für eine gewichtete Summe",380,p)

    events=[(i,i+j+1,str(j+1),j==2) for i in range(4) for j in range(3)]
    cycle_grid("pipeline","Unabhängige Starts · Latenz 3 · Startabstand 1",
               ["Op 1","Op 2","Op 3","Op 4"],6,events,
               "Ergebnisse Ende 3, 4, 5, 6 · Taktzahl ist eine Lehrannahme")

    p=[text(20,30,"32 Vektorregister v0–v31 · ein Register hat hier VLEN = 128 Bit")]
    for i in range(4):
        p += [rect(80+i*215,100,210,90,BG,RED if i<3 else LIGHT),
              text(185+i*215,155,f"Element {i}" if i<3 else "Tail",25,anchor="middle"),
              text(185+i*215,224,"32 Bit",23,anchor="middle")]
    p += [text(500,280,"LMUL = 1 · SEW = 32 Bit · VLMAX = 4 Elemente · VL = 3 Elemente",24,anchor="middle")]
    save("rvv","Vektorkapazität und drei aktive Elementplätze",310,p)

    p=[text(20,30,"AVL = 40 · VLMAX = 32 · erste VL muss zwischen 20 und 32 liegen")]
    for y,lengths in [(95,[32,8]),(210,[20,20])]:
        x=120
        for length in lengths:
            p += [rect(x,y,length*20-5,65,BG,RED if x==120 else LIGHT),
                  text(x+length*10-2,y+42,length,28,anchor="middle")]
            x += length*20
    p += [text(500,325,"Zulässig: 32 + 8 oder 20 + 20 · unzulässig: zuerst 16",24,anchor="middle")]
    save("strip","Zwei gültige Aufteilungen desselben Vektorrestes",355,p)

    p=[text(20,30,"VL = 4 aktive Elemente · reine Modellrechnung ohne Load/Store")]
    p += [text(20,110,"1 Lane",24),text(20,245,"2 Lanes",24)]
    for i in range(4):
        p += box(220+i*185,75,150,60,[f"Element {i}"])
        p += [text(295+i*185,174,f"Schritt {i+1}",23,anchor="middle")]
    for i in range(4):
        x=260+(i//2)*350;y=200+(i%2)*70
        p += box(x,y,250,60,[f"Element {i}"])
    p += [text(385,377,"Schritt 1",23,anchor="middle"),text(735,377,"Schritt 2",23,anchor="middle")]
    save("lanes","Gleiche Vektorwirkung mit unterschiedlicher Rechenbreite",410,p)

    events=[]
    for i in range(4):
        events += [(0,i+2,f"p{i}",False),(1,i+3,f"y{i}",True),(2,i+6,f"y{i}",True)]
    cycle_grid("chain","Multiplikation: Latenz 2 · Addition: Latenz 1 · Startabstand jeweils 1",
               ["Produkt fertig","Add direkt","Add warten"],9,events,
               "Direkte Weitergabe endet in 6 · Warten auf alle Produkte endet in 9")

    p=[text(20,30,"Output-Stationary · lokale Summe bleibt während des Tiles")]
    p += marked_box(360,125,280,125,["C hält die Summe","C neu: C + A · B"])
    p += [text(70,198,"A von links",24),line(230,185,350,185,arrow=True),
          text(500,82,"B von oben",24,anchor="middle"),line(500,92,500,115,arrow=True),
          line(650,185,750,185,arrow=True),text(790,194,"A weiter",24),
          line(500,258,500,300,arrow=True),text(500,337,"B weiter",24,anchor="middle"),
          text(500,393,"Nur gültige Paare rechnen · unveränderte Operanden gehen zum Nachbarn",23,anchor="middle")]
    save("cell","Lokale Akkumulation und gerichtete Nachbarweitergabe",422,p)

    p=[text(20,30,"2 × 2 Output-Stationary · A rechts · B unten · C bleibt lokal")]
    for i in range(2):
        for j in range(2):p += box(330+j*300,95+i*150,180,100,[f"C{i}{j}","Startwert 0"])
    for i in range(2):p += [text(30,158+i*150,f"A{i}: " + ["1, 2", "3, 4"][i],24),line(200,145+i*150,320,145+i*150,arrow=True),line(515,145+i*150,620,145+i*150,arrow=True)]
    for j in range(2):p += [text(420+j*300,70,f"B{j}: " + ["5, 7", "6, 8"][j],24,anchor="middle"),line(420+j*300,77,420+j*300,87,arrow=True),line(420+j*300,200,420+j*300,235,arrow=True)]
    save("array","Vier Ausgabesummen in Nachbarzellen",380,p)

    rows=["A Zeile 0","A Zeile 1","B Spalte 0","B Spalte 1"]
    events=[]
    for row,vals,offset in [(0,[1,2],0),(1,[3,4],1),(2,[5,7],0),(3,[6,8],1)]:
        events += [(row,k+1+offset,str(v),bool(offset)) for k,v in enumerate(vals)]
    cycle_grid("skew","Zeitlich versetzte Randwerte · leer bedeutet ungültig",rows,4,events,
               "Gleicher Summenindex k trifft in derselben Zelle zusammen")

    p=[text(20,30,"Gültige MAC-Paare · unveränderte Operanden wandern je Takt eine Zelle")]
    for t in range(1,5):
        x0=20+(t-1)*245
        p += [text(x0+108,80,f"Takt {t}",25,anchor="middle")]
        count=0
        for i in range(2):
            for j in range(2):
                active=any(t==1+k+i+j for k in range(2));count+=active
                p += [rect(x0+j*110,110+i*85,100,75,BG,RED if active else LIGHT),
                      text(x0+j*110+50,155+i*85,f"C{i}{j}",25,anchor="middle")]
        p += [text(x0+108,325,f"{count} MAC"+("s" if count!=1 else ""),25,anchor="middle")]
    save("wave","Anlauf und Auslaufen der vier Zellen",365,p)

    p=[text(20,30,"Stationary bezeichnet den lokal bleibenden Wert, nicht das ganze Netz")]
    p += marked_box(110,110,270,110,["C bleibt lokal","Output-Stationary"])
    p += marked_box(620,110,270,110,["W bleibt lokal","Weight-Stationary"])
    for x,label in [(245,"A und B bewegen sich"),(755,"x und Teilsummen bewegen sich")]:
        p += [line(x,65,x,100,arrow=True),line(x,230,x,270,arrow=True),text(x,312,label,22,anchor="middle")]
    p += [text(500,375,"Vorladen und Tilewechsel bleiben nötig · verschiedene Ablaufmodelle",24,anchor="middle")]
    save("stationary","Zwei unterschiedliche lokal gehaltene Datenarten",405,p)

    p=[text(20,30,"Ein isoliertes 2 × 2-Tile · vier interne Takte · keine weitere Arbeit")]
    for x,n,label in [(90,2,"2 × 2-Array"),(550,4,"4 × 4-Array")]:
        p += [text(x+130,78,label,25,anchor="middle")]
        step=260/n
        for i in range(n):
            for j in range(n):p += [rect(x+j*step,100+i*step,step-5,step-5,BG,RED if i<2 and j<2 else LIGHT)]
    p += [text(220,395,"8 / 16 Zell-Takte = 50 %",23,anchor="middle"),
          text(680,395,"8 / 64 Zell-Takte = 12,5 %",23,anchor="middle"),
          text(680,430,"Räumlich belegt: 4 / 16 = 25 %",23,anchor="middle")]
    save("util","Zeitliche Auslastung und räumliche Belegung",458,p)

    p=[text(20,30,"TPU v1 · dokumentierter Rechenpeak · 2 Ops je Int8-MAC")]
    for x,labels in [(20,["256 × 256","65 536 MACs"]),(355,["700 MHz","45,8752 TMAC/s"]),(700,["× 2 Ops/MAC","91,7504 TOPS"])]:
        p += box(x,110,280,100,labels)
    p += [line(300,160,350,160,arrow=True),line(635,160,695,160,RED,3,arrow=True),
          text(500,280,"Gerundet 92 TOPS · keine Inferenzen/s · keine Wattangabe",24,anchor="middle")]
    save("tops","Von Einheiten und Taktfrequenz zum gezählten Peak",310,p)

    p=[text(20,30,"Serielle Lehrzeiten in ms · gleiche Eingabe und gleiche Ausgabe")]
    phases=[([2,10,3,1],["Vor","Dense","Rest","Nach"]),([2,1,1,3,1],["Vor","Kopie","Dense","Rest","Nach"])]
    for r,(lengths,labels) in enumerate(phases):
        y=110+r*135;x=180
        p += [text(20,y+40,"CPU" if r==0 else "NPU",24)]
        for v,label in zip(lengths,labels):
            w=v*47
            p += [rect(x,y,w-3,58,BG,RED if label=="Dense" else LIGHT),
                  text(x+w/2,y+38,str(v),25,anchor="middle"),
                  text(x+w/2,y+(119 if r==1 and label=="Dense" else 91),label,21,anchor="middle")]
            x+=w
        p += [text(x+8,y+38,"= 16" if r==0 else "= 8",24)]
    p += [text(500,420,"Dense: Faktor 10 · gesamte Anwendung: Faktor 2",24,anchor="middle")]
    save("speed","Teilbeschleunigung und vollständiges Zeitbudget",450,p)

    p=[text(20,30,"Modellvorbereitung und Firmwareausführung sind getrennte Phasen")]
    for x,labels in [(20,["Training","Parameter"]),(355,["Konvertierung",".tflite-Daten"]),(700,["Firmware","Daten + Kernel"])]:p += box(x,95,280,95,labels)
    p += [line(300,143,350,143,arrow=True),line(635,143,695,143,arrow=True)]
    for x,labels in [(20,["Sensorfenster","vorbereiten"]),(355,["Operatoren","ausführen"]),(700,["Ausgabe","interpretieren"])]:p += box(x,270,280,95,labels)
    p += [line(300,317,350,317,arrow=True),line(635,317,695,317,RED,3,arrow=True),line(840,198,840,260,arrow=True)]
    save("flow","Vom Modell zu wiederholter Inferenz",395,p)

    p=[text(20,30,"Int8-Lehrregel · Skala s = 0,1 · Nullpunkt z = 0")]
    for y,labels in [(100,["r = 1,24","r/s = 12,4","q = 12","Rückwert 1,2"]),
                     (240,["r = 20","r/s = 200","q = 127","Rückwert 12,7"])]:
        for i,label in enumerate(labels):
            p += box(20+i*245,y,225,60,[label])
            if i<3:p += [line(245+i*245,y+30,260+i*245,y+30,RED if y==240 and i==1 else INK,2,arrow=True)]
        p += [text(500,y+103,"Rundungsfehler 0,04" if y==100 else "Begrenzungsfehler 7,3",24,anchor="middle")]
    save("quant","Rundung und Sättigung sind verschiedene Fehlerarten",382,p)

    p=[text(20,30,"Fiktive Speicherbudgets · KiB = 1024 Byte · Eingabetensor bereits in Arena")]
    for y,total,vals,labels in [(110,128,[40,24,64],["Firmware 40","Modell 24","frei 64"]),
                               (285,32,[12,1.5,6,4,8.5],["Arena 12","Quelle 1,5","Stack 6","übrig 4","frei 8,5"])]:
        p += [text(20,y-25,"Flash 128 KiB" if total==128 else "SRAM 32 KiB",25)]
        x=20
        for i,(v,label) in enumerate(zip(vals,labels)):
            w=960*v/total
            p += [rect(x,y,w-3,65,BG,RED if (total==128 and i==1) or (total==32 and i==0) else LIGHT),
                  text(x+w/2,y+41,str(v).replace('.',','),24,anchor="middle")]
            x+=w
        # Labels below the short SRAM segments are placed on separate lines.
        p += [text(20,y+105," · ".join(labels),23)]
    save("arena","Getrennte Flash- und SRAM-Bilanz",430,p)

    p=[text(20,30,"Konzeptioneller TFLM-Ablauf · alle Objekte und Puffer bleiben gültig")]
    for x,labels in [(20,["Modell prüfen","Operatoren"]),(355,["Arena planen","Status prüfen"]),(700,["Tensorvertrag","bereit"])]:p += box(x,85,280,90,labels)
    p += [line(300,130,350,130,arrow=True),line(635,130,695,130,arrow=True)]
    for x,labels in [(20,["Eingabe","schreiben"]),(355,["Invoke","Status prüfen"]),(700,["bei Erfolg","Ausgabe lesen"])]:p += box(x,245,280,90,labels)
    p += [line(300,290,350,290,arrow=True),line(635,290,695,290,arrow=True),
          line(840,182,840,208,arrow=True),line(840,208,160,208),line(160,208,160,238,arrow=True),
          line(495,343,495,375,RED,3,arrow=True),text(495,410,"Fehler: keine neue Entscheidung aus alten Ausgangsbytes",23,anchor="middle")]
    save("runtime","Initialisierung und wiederholter Inferenzzyklus mit Fehlerpfad",440,p)

    p=[text(20,30,"Fiktiver Tensorvertrag: 128 Zeitpunkte · je drei Achsen · geordnete Elemente")]
    x0=100
    for i in range(4):
        p += [text(x0+i*210+80,83,f"Zeit {i}" if i<3 else "… 127",24,anchor="middle")]
        for j,label in enumerate(["x","y","z"]):p += [rect(x0+i*210+j*52,110,48,60),text(x0+i*210+j*52+24,149,label,24,anchor="middle")]
    p += [text(500,225,"128 × 3 = 384 Elemente",26,anchor="middle"),
          text(500,277,"Float32-Quelle: 1536 Byte · Int8-Ziel: 384 Byte",24,anchor="middle"),
          text(500,335,"Datentyp + Reihenfolge + Skala + Ausgabebedeutung vereinbaren",23,anchor="middle")]
    save("sensor","Elementzahl, Bytezahl und Sensorreihenfolge",365,p)


def rasterize(chromium):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path=chromium,headless=True,args=["--no-sandbox"])
        page=browser.new_page(viewport={"width":W,"height":600},device_scale_factor=2)
        for source in sorted(OUT.glob("*.svg")):
            page.set_content('<html><body style="margin:0;background:white">'+source.read_text(encoding="utf-8")+'</body></html>')
            page.locator("svg").screenshot(path=str(source.with_suffix(".png")))
        browser.close()


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--png",action="store_true")
    parser.add_argument("--chromium",default="/usr/bin/chromium")
    args=parser.parse_args()
    figures()
    if args.png:rasterize(args.chromium)
    print("27 Lehrdiagramme geschrieben"+(" (SVG und PNG)." if args.png else " (SVG)."))
