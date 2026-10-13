#!/usr/bin/env python3
"""Reproduzierbare Lehrdiagramme für VL07; keine Messdaten oder Schaltpläne.

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


def figures():
    p = [text(20, 30, "M1 · ein Takt je Stufe · nur Funktionen, kein Schaltplan")]
    for i, labels in enumerate([["IF", "Befehl", "holen"], ["ID", "Decode", "Register lesen"],
                                ["EX", "ALU", "rechnet"], ["MEM", "Daten", "zugreifen"],
                                ["WB", "Register", "schreiben"]]):
        p += box(20+i*200, 95, 160, 100, labels)
        if i<4:p += [line(180+i*200, 145, 215+i*200, 145, RED if i==3 else INK, arrow=True)]
    p += [text(500, 254, "Ein Befehl braucht fünf Schritte · mehrere Befehle nutzen verschiedene Stufen", 22, anchor="middle")]
    save("stages", "Fünf Funktionen der skalaren Lehrpipeline", 283, p)

    stages=["IF","ID","EX","MEM","WB"]
    events=[(i,i+j+1,s,j==4) for i in range(5) for j,s in enumerate(stages)]
    cycle_grid("pipe","M1 · fünf unabhängige Befehle · keine Stalls",
               [f"I{i}" for i in range(1,6)],9,events,
               "Fünf Befehle in neun Takten · rot: letzte Stufe")

    p=[text(20,30,"M1 · Produzent: EX Ende 3, WB in 5 · Registerlesen nach WB erlaubt")]
    x=lambda c:230+(c-3)*175
    for c in range(3,7):p += [text(x(c)+77,75,c,23,anchor="middle")]
    for y,label in [(100,"Produzent"),(190,"mit Forwarding"),(280,"ohne Forwarding")]:
        p += [text(20,y+29,label,22)]
        for c in range(3,7):p += [rect(x(c),y,154,50,"#FFFFFF",LIGHT)]
    p += [rect(x(3),100,154,50),text(x(3)+77,134,"EX",24,anchor="middle"),
          rect(x(5),100,154,50),text(x(5)+77,134,"WB",24,anchor="middle"),
          rect(x(4),190,154,50,BG,RED),text(x(4)+77,224,"EX",24,anchor="middle"),
          line(x(3)+150,153,x(4)+20,185,RED,3,arrow=True)]
    for c in [4,5]:
        p += [rect(x(c),280,154,50),text(x(c)+77,314,"wartet",23,anchor="middle")]
    p += [rect(x(6),280,154,50),text(x(6)+77,314,"EX",24,anchor="middle"),
          text(980,372,"Takt →",22,anchor="end")]
    save("forwarding","Ergebnisweiterleitung verkürzt den Weg zum Verbraucher",400,p)

    p=box(20,65,235,70,["bereite Operanden"])
    p+=box(20,215,235,70,["andere Operanden"])
    p+=box(370,65,240,70,["Summe 1"])
    p+=box(370,215,240,70,["Summe 2"])
    p+=box(765,140,215,70,["Gesamtsumme"])
    p += [line(255,100,365,100,arrow=True),line(255,250,365,250,arrow=True),
          line(610,100,760,160,RED,3,arrow=True),line(610,250,760,190,RED,3,arrow=True),
          text(20,30,"Unabhängige Summen · gemeinsamer Verbraucher wartet auf beide"),
          text(500,343,"Wertabhängigkeiten bestimmen, welche Arbeit zusammen möglich ist",23,anchor="middle")]
    save("ilp","Zwei unabhängige Summen vor einem gemeinsamen Verbraucher",371,p)

    p=box(40,90,330,70,["A: Load → t0"])
    p+=box(40,265,330,70,["B: t1 ← t0 + t2"])
    p+=box(620,90,330,70,["C: t0 ← t4 − t5"])
    p+=box(620,265,330,70,["D: t6 ← t0 AND t3"])
    p += [line(205,160,205,260,RED,3,arrow=True),text(215,214,"RAW",22,RED),
          line(785,160,785,260,RED,3,arrow=True),text(795,214,"RAW",22,RED),
          line(370,125,615,125,INK,2,dash=True,arrow=True),text(493,106,"WAW t0",22,anchor="middle"),
          line(370,300,615,145,INK,2,dash=True,arrow=True),text(498,252,"WAR t0",22,anchor="middle"),
          text(20,30,"Programmfolge A, B, C, D · Wertfluss und Namenskonflikte"),
          text(500,389,"Rot: echte Werte · gestrichelt: gleiche Namen",23,anchor="middle")]
    save("deps","Echte Abhängigkeiten und zwei Konflikte auf dem Namen t0",418,p)

    p=box(20,145,230,90,["Auswahl", "maximal 3 Starts"])
    for y,labels in [(60,["ALU0"]), (160,["ALU1"]), (260,["LSU"])]:
        p+=box(420,y,200,60,labels)
        p += [line(250,190,330,190),line(330,90,330,290),
              line(330,y+30,415,y+30,arrow=True),
              line(620,y+30,755,190,arrow=True)]
    p+=marked_box(760,145,220,90,["Retire", "maximal 2"])
    p += [
          text(20,30,"Eigenes Ressourcenmodell · zwei ALUs und eine LSU"),
          text(500,373,"Drei passende Starts sind möglich · dauerhaft höchstens zwei Retires",23,anchor="middle")]
    save("frontend","Verschiedene Ausführungseinheiten und begrenzte Bestätigungsbreite",401,p)

    p=[text(20,30,"M2 · vier unabhängige Operationen · Retire frühestens im Folgetakt")]
    x0,bw=235,145
    for c in range(1,6):p += [text(x0+(c-.5)*bw,72,c,22,anchor="middle")]
    lanes=[(90,"einfach: Start",["I1","I2","I3","I4",""],False),
           (150,"Retire",["","I1","I2","I3","I4"],True),
           (250,"zweifach: Start",["I1 I2","I3 I4","","",""],False),
           (310,"Retire",["","I1 I2","I3 I4","",""],True)]
    for y,label,values,final in lanes:
        p += [text(20,y+32,label,23)]
        for i,v in enumerate(values):
            p += [rect(x0+i*bw,y,bw-8,48,BG if v else "#FFFFFF",RED if final and v else LIGHT),
                  text(x0+i*bw+(bw-8)/2,y+32,v,23,anchor="middle")]
    p += [text(500,415,"Einfach: 4/5 IPC · zweifach: 4/3 IPC",24,anchor="middle")]
    save("width","Breiter Start und breitere Bestätigung im kurzen Modell",443,p)

    stages=["1","2","3"]
    events=[(i,i+j+1,s,j==2) for i in range(4) for j,s in enumerate(stages)]
    cycle_grid("latency","Rechenblock · Latenz 3 · Initiationsintervall 1",
               [f"Operation {i}" for i in range(1,5)],6,events,
               "Vier Ergebnisse Ende 3 bis Ende 6 · keine abhängigen Starts")

    p=[]
    for x,labels in [(20,["Fetch / Decode","geordnet"]), (275,["Vorbereitung","Quellen / Ziele"]),
                     (530,["Auswahl / Execute","nach Bereitschaft"]), (785,["Retire","geordnet"])]:
        p+=box(x,110,195,100,labels)
    for x in [215,470,725]:p += [line(x,160,x+55,160,RED if x==470 else INK,3,arrow=True)]
    p += [text(20,30,"Drei Rollen · Vorbereitung, dynamische Ausführung, Bestätigung"),
          text(500,285,"Startreihenfolge darf sich ändern · sichtbare Wirkungen bleiben korrekt",23,anchor="middle")]
    save("flow","Geordnete Vorbereitung, dynamischer Start und geordnete Bestätigung",313,p)

    p=[text(20,30,"Quellen aus alter Abbildung lesen · neues Ziel anschließend eintragen")]
    headers=[(50,"Befehl"),(290,"Quellen"),(660,"neues Ziel")]
    for x,label in headers:p += [text(x,77,label,23)]
    rows=[("A: Load t0","s1 → P9","t0 → P10"),
          ("B: Add t1","t0 → P10, t2 → P2","t1 → P11"),
          ("C: Sub t0","t4 → P4, t5 → P5","t0 → P12"),
          ("D: AND t6","t0 → P12, t3 → P3","t6 → P13")]
    for i,(ins,src,dst) in enumerate(rows):
        y=95+i*52
        p += [rect(30,y,930,46),text(50,y+31,ins,23),text(290,y+31,src,23),text(660,y+31,dst,23)]
    p += [text(20,345,"Aktuelle t0-Abbildung:",23)]
    for x,label in [(390,"P7"),(590,"P10"),(790,"P12")]:
        p+=box(x,313,120,50,[label])
    p += [line(510,338,585,338,RED,3,arrow=True),line(710,338,785,338,RED,3,arrow=True),
          text(552,393,"A",22,anchor="middle"),text(752,393,"C",22,anchor="middle")]
    save("rename","Vier gespeicherte Quellversionen und vier getrennte neue Ziele",420,p)

    p=box(20,90,270,85,["P10 = 10","alte t0-Version"])
    p+=box(20,245,270,85,["P12 = 5","neue t0-Version"])
    p+=box(690,90,290,85,["B behält P10","10 + 1 = 11"])
    p+=box(690,245,290,85,["D nutzt P12","5 AND 7 = 5"])
    p += [line(290,132,685,132,arrow=True),line(290,287,685,287,RED,3,arrow=True),
          text(20,30,"Aktuelle Abbildung t0 → P12 · alter Leser wird nicht umgebogen"),
          text(500,385,"P10 bleibt geschützt, solange ein alter Nutzer oder Rückweg es benötigt",23,anchor="middle")]
    save("version","Gespeicherter Quelltag statt späterem Blick auf die neueste Abbildung",413,p)

    p=[text(20,30,"Vor A-Abschluss · ein freier ALU-Start · B und D warten")]
    for y,labels in [(75,["B: P10 fehlt"]), (170,["C: Quellen bereit"]), (265,["D: P12 fehlt"])]:
        p+=box(30,y,370,65,labels)
    p+=box(700,170,270,65,["freie ALU"])
    p += [line(400,202,695,202,RED,3,arrow=True),text(550,173,"C auswählen",23,anchor="middle"),
          text(500,379,"Nach C-Ende wird P12 bereit · D ist dann ein Kandidat",23,anchor="middle")]
    save("issue","Auswahl eines bereiten Kandidaten mit passender freier Einheit",407,p)

    rows=["A: Load","B: Add","C: Sub","D: AND"]
    events=[(0,1,"Start",False),(0,4,"fertig",False),(0,5,"Retire",True),
            (1,5,"Start",False),(1,6,"Retire",True),
            (2,6,"Start",False),(2,7,"Retire",True),
            (3,7,"Start",False),(3,8,"Retire",True)]
    cycle_grid("inorder","M3 · In-Order · B blockiert die Startwahl bis Takt 5",
               rows,8,events,"Erster Start 1 · letzter Retire 8 · ALU fertig am Starttaktende")
    events=[(0,1,"Start",False),(0,4,"fertig",False),(0,5,"Retire",True),
            (1,5,"Start",False),(1,6,"Retire",True),
            (2,2,"Start",False),(2,6,"Retire",True),
            (3,3,"Start",False),(3,7,"Retire",True)]
    cycle_grid("ooo","M3 · Out-of-Order · C und D starten vor dem wartenden B",
               rows,7,events,"Erster Start 1 · letzter Retire 7 · Retire bleibt A, B, C, D")

    p=[text(20,30,"Momentaufnahme Ende Takt 3 · Einträge bestehen schon vor Execute"),
       text(30,82,"ROB: Programmordnung und Status",24),
       text(750,82,"PRF: Werte",24)]
    for i,(ins,dst,ready) in enumerate([("A","P10",False),("B","P11",False),("C","P12",True),("D","P13",True)]):
        y=105+i*55
        p += [rect(30,y,625,48,BG,RED if ready else LIGHT),
              text(65,y+32,ins,24),text(210,y+32,dst,24),
              text(370,y+32,"fertig" if ready else "wartet",24)]
    p+=box(745,160,230,60,["P12 = 5"])
    p+=box(745,245,230,60,["P13 = 5"])
    p += [text(80,367,"Kopf A blockiert die Bestätigung",23),
          line(15,355,15,129,INK,2), line(15,129,25,129,INK,2,arrow=True),
          text(755,367,"P10 noch nicht bereit",22)]
    save("rob","Reihenfolge und Status getrennt von den physischen Zahlenwerten",398,p)

    p=box(20,105,200,85,["Vorgänger", "bestätigt"])
    p+=marked_box(290,105,200,85,["A: Loadfehler", "kein Retire"])
    p+=box(560,105,210,85,["B, C, D", "nicht bestätigen"])
    p+=box(835,105,145,85,["Trap", "bei A"])
    p += [
          line(220,147,285,147,arrow=True),line(490,147,555,147,RED,3,arrow=True),
          line(770,147,830,147,arrow=True),
          text(20,30,"Fehlervariante · A erreicht den Kopf mit einem Zugriffsfehler"),
          text(500,270,"Architektur: t0 = 42, t1 = 9, t6 = 12 bleiben erhalten",24,anchor="middle"),
          text(500,325,"Fertige jüngere Werte dürfen intern existieren, ohne sichtbar zu werden",23,anchor="middle")]
    save("trap","Präziser Ausnahmezustand ohne normale jüngere Bestätigung",354,p)

    p=[]
    for x,labels in [(20,["Adresse und Daten","vorbereiten"]), (275,["Store-Queue","noch vorläufig"]),
                     (530,["Commit","geordnet freigeben"]), (785,["Cache / Speicher","später weitergeben"])]:
        p+=box(x,105,195,100,labels)
    for x in [215,470,725]:p += [line(x,155,x+55,155,RED if x==470 else INK,3,arrow=True)]
    p += [text(20,30,"Store: Fertigstellung, Bestätigung und Speicherweg unterscheiden"),
          text(500,277,"Externe Sichtbarkeit hängt zusätzlich von Cache und Speichervertrag ab",23,anchor="middle")]
    save("lsu","Vorläufiger Store, Freigabe durch Commit und spätere Weitergabe",307,p)

    p=[text(20,30,"Verschiedene Basisregisternamen garantieren keine verschiedenen Orte"),
       text(20,70,"a0 ≠ a1: verschiedene Speicherstellen",23)]
    for x,w,labels in [(20,180,["Store via a0"]), (285,160,["Ort A"]),
                       (540,160,["Ort B"]), (790,190,["Load via a1"])]:
        p+=box(x,95,w,60,labels)
    p += [line(200,125,280,125,arrow=True),line(700,125,785,125,arrow=True),
          text(20,225,"a0 = a1: gleiche Speicherstelle",23)]
    p+=box(20,255,180,60,["Store via a0"])
    p+=marked_box(395,255,210,60,["gemeinsamer Ort"])
    p+=box(790,255,190,60,["Load via a1"])
    p += [
          line(200,285,390,285,RED,3,arrow=True),line(605,285,785,285,RED,3,arrow=True),
          text(500,380,"Bei gleicher Adresse muss der jüngere Load den richtigen Storewert erhalten",22,anchor="middle")]
    save("alias","Speicheralias und Wertfolge trotz verschiedener Registernamen",408,p)

    p=box(20,135,200,80,["Fetch-PC"])
    p+=box(370,65,260,75,["BHT", "Richtung T / NT"])
    p+=box(370,235,260,75,["BTB", "Zieladresse"])
    p+=box(775,135,205,80,["nächster PC"])
    p += [line(220,175,365,102,arrow=True),line(220,175,365,272,arrow=True),
          line(630,102,770,155,arrow=True),line(630,272,770,197,RED,3,arrow=True),
          text(690,97,"Richtung",22,anchor="middle"),
          text(704,298,"Ziel bei Taken",22,anchor="middle"),
          text(20,30,"Richtung und Ziel sind getrennte Vorhersageinformationen"),
          text(500,378,"Fehlt ein passendes Ziel, ist richtiges Taken noch kein kompletter Fetch",23,anchor="middle")]
    save("bpred","Zwei Informationsquellen für die Wahl des nächsten Program Counters",408,p)

    p=[text(20,30,"Schematische Zeit · keine gemessene Taktzahl"),
       text(20,109,"Branch geholt",23),text(640,109,"Entscheidung",23)]
    for x,label in [(210,"falscher Pfad 1"),(370,"Pfad 2"),(500,"Pfad 3")]:
        w=150 if x==210 else 115
        p += [rect(x,145,w,70,BG,RED),text(x+w/2,185,label,22,anchor="middle")]
    p += [line(630,125,630,283,RED,3),
          rect(670,235,300,55),text(820,271,"richtiger Pfad wird gefüllt",23,anchor="middle"),
          line(210,320,970,320,MUTED,2,arrow=True),
          text(970,356,"Zeit →",22,anchor="end"),
          text(20,268,"jüngere Arbeit verwerfen",23)]
    save("flush","Falscher Pfad, Verwerfen und erneute Lieferung des richtigen Pfads",385,p)

    p=[text(20,30,"CPI: mittlere Takte je bestätigtem Befehl · additives Lehrmodell")]
    p += [rect(150,105,520,85),text(410,155,"Basis 1,00",28,anchor="middle"),
          rect(670,105,156,85,BG,RED),text(748,155,"+ 0,30",26,anchor="middle")]
    p += axis(150,870,218,[(150,"0"),(410,"0,5"),(670,"1,0"),(826,"1,3")],"CPI")
    p += [text(500,325,"Zeitfaktor 1,30 · Durchsatzfaktor 1 / 1,30 ≈ 0,769",24,anchor="middle")]
    save("cpi","Zusätzliche mittlere Takte und deren Kehrwert für den Durchsatz",355,p)

    outcomes=[True,True,True,True,False]*2
    state=False
    p=[text(20,30,"1 Bit · Start N nach einem vorherigen Schleifenende")]
    for y,label in [(100,"Ergebnis"),(175,"Vorhersage")]:p += [text(20,y+32,label,24)]
    for i,actual in enumerate(outcomes):
        x=235+i*73
        p += [text(x+32,79,i+1,22,anchor="middle"),
              rect(x,100,64,50),text(x+32,134,"T" if actual else "N",26,anchor="middle"),
              rect(x,175,64,50,BG,RED if state!=actual else LIGHT),
              text(x+32,209,"T" if state else "N",26,anchor="middle")]
        state=actual
    p += [text(500,290,"TTTTN zweimal · vier Misses: Eintritt und Ende jedes Durchlaufs",23,anchor="middle")]
    save("onebit","Ein-Bit-Vorhersage aus alter Historie bei zwei wiederholten Schleifen",320,p)

    p=[text(20,30,"2 Bit · Vorhersage aus altem Zustand · T erhöht, NT vermindert")]
    for i,state in enumerate(["00","01","10","11"]):
        x=40+i*240
        p+=box(x,100,200,85,[state,"Vorhersage NT" if i<2 else "Vorhersage T"])
        if i<3:
            p += [line(x+200,135,x+235,135,RED if i==1 else INK,2,arrow=True),
                  text(x+218,116,"T",22,anchor="middle"),
                  line(x+240,170,x+205,170,RED if i==1 else INK,2,arrow=True),
                  text(x+218,218,"NT",22,anchor="middle")]
    p += [path([(40,145),(16,145),(16,292),(140,292),(140,189)],INK,2),
          text(73,286,"NT",22), line(140,270,140,190,INK,2,arrow=True),
          path([(960,145),(984,145),(984,68),(860,68),(860,95)],INK,2),
          text(938,61,"T",22), line(860,70,860,95,INK,2,arrow=True),
          text(500,351,"00 und 11 sättigen · nur 01 ↔ 10 wechselt die Vorhersagerichtung",23,anchor="middle")]
    save("pred","Vollständiger Automat eines saturierenden Zwei-Bit-Prädiktors",380,p)

    state=3;outcomes=[True,True,False,False,True];rows=[]
    for actual in outcomes:
        pred=state>=2;nxt=min(3,state+1) if actual else max(0,state-1)
        rows.append((state,pred,actual,pred==actual,nxt));state=nxt
    xs=[70,235,390,545,710,875]
    p=[text(20,30,"Start 11 · Folge T, T, NT, NT, T · zuerst vorhersagen")]
    for x,label in zip(xs,["Schritt","alt","Vorhersage","Ist","neu","Treffer"]):
        p += [text(x,76,label,22,anchor="middle")]
    for i,(st,pr,ac,hit,nxt) in enumerate(rows):
        y=92+i*47
        p += [rect(25,y,950,42)]
        vals=[str(i+1),f"{st:02b}","T" if pr else "NT","T" if ac else "NT",f"{nxt:02b}","ja" if hit else "nein"]
        for x,label in zip(xs,vals):p += [text(x,y+29,label,24,RED if label=="nein" else INK,"middle")]
    p += [text(500,380,"Zwei Treffer · drei Misses · Endzustand 10",24,anchor="middle")]
    save("predict-table","Vorhersagen und anschließende Zustandsupdates für fünf Ergebnisse",408,p)

    p=[text(20,30,"Oberes Modell: 8 Einträge, Index aus PC[4:2]")]
    p+=box(20,75,260,65,["PC 0x04 → 001"])
    p+=box(20,170,260,65,["PC 0x24 → 001"])
    p+=marked_box(525,120,330,75,["BHT-Eintrag 1"])
    p += [
          line(280,107,520,140,RED,3,arrow=True),line(280,202,520,176,RED,3,arrow=True),
          text(20,285,"Anderes Modell: gshare mit vier Bits",24)]
    p+=box(20,320,210,55,["PC-Index 0101"])
    p+=box(340,320,270,55,["XOR GHR 0011"])
    p+=box(780,320,200,55,["Index 0110"])
    p += [line(230,347,335,347,arrow=True),line(610,347,775,347,RED,3,arrow=True)]
    save("history","Indexalias und getrenntes Vier-Bit-gshare-Beispiel",410,p)

    p=[text(20,30,"Fehlvorhersage · Architekturzustand und interne Spur unterscheiden")]
    for y,label in [(95,"Architektur"),(240,"Cache")]:p += [text(20,y+44,label,24)]
    for x,y,labels in [(225,95,["vorläufige Werte"]),(495,95,["Squash"]),(765,95,["gültige Abbildung"]),
                       (225,240,["Zugriff ausgelöst"]),(495,240,["Zeile ggf. geladen"]),(765,240,["Zeit ggf. verändert"])]:
        p+=box(x,y,215,80,labels)
    for y,col in [(135,INK),(280,RED)]:
        p += [line(440,y,490,y,col,3,arrow=True),line(710,y,760,y,col,3,arrow=True)]
    p += [text(500,378,"Rücknahme normaler Wirkungen löscht nicht pauschal jede Cacheänderung",23,anchor="middle")]
    save("speculation","Zwei Beobachtungsebenen bei einer falschen spekulativen Ausführung",408,p)

    p=[text(20,30,"Spectre-v1-Prinzip · schematisch, ohne Angriffsausführung")]
    for x,labels in [(20,["Bereichsprüfung","Pfad vorhergesagt"]), (275,["Wert transient","vorläufig gelesen"]),
                     (530,["Probeadresse","vom Wert abhängig"]), (785,["Cachezeile","ggf. geladen"])]:
        p+=box(x,110,195,100,labels)
    for x in [215,470,725]:p += [line(x,160,x+55,160,RED if x>=470 else INK,3,arrow=True)]
    p += [line(882,210,882,280,RED,3,arrow=True),
          text(500,270,"Squash: keine normale Bestätigung des falschen Pfads",23,anchor="middle"),
          text(720,319,"spätere Zeitbeobachtung kann Information tragen",22,anchor="middle")]
    save("spectre","Wertabhängiger Probezugriff als mögliche Cache-Seitenkanalspur",348,p)

    p=[text(20,30,"Vier Werte 1, 2, 3, 4 · gleiche Summe, andere Abhängigkeiten")]
    p += [text(20,102,"eine Summe",23)]
    for i,val in enumerate([0,1,3,6,10]):
        x=230+i*145
        p+=box(x,68,105,60,[str(val)])
        if i<4:
            p += [line(x+105,98,x+140,98,arrow=True),text(x+123,60,f"+{i+1}",21,anchor="middle")]
    for y,label,vals,adds in [(220,"Teilsumme A",[0,1,4],[1,3]),(315,"Teilsumme B",[0,2,6],[2,4])]:
        p += [text(20,y+37,label,23)]
        for i,val in enumerate(vals):
            x=230+i*195
            p+=box(x,y,115,60,[str(val)])
            if i<2:
                p += [line(x+115,y+30,x+190,y+30,arrow=True),text(x+153,y+15,f"+{adds[i]}",21,anchor="middle")]
    p+=box(840,260,135,75,["Summe 10"])
    p += [line(735,250,835,280,RED,3,arrow=True),line(735,345,835,315,RED,3,arrow=True),
          text(500,428,"Zwei kürzere Ketten brauchen eine Schlussaddition und passende Ressourcen",23,anchor="middle")]
    save("reduction","Eine durchgehende Summe oder zwei Teilakkumulatoren mit Zusammenführung",456,p)

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
    print("28 Lehrdiagramme geschrieben" + (" (SVG und PNG)." if args.png else " (SVG)."))
