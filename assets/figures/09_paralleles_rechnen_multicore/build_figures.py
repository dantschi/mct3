#!/usr/bin/env python3
"""Reproduzierbare Lehrdiagramme für VL09; keine Messdaten oder Schaltpläne.

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




def table(name, title, columns, rows, widths, highlight=None):
    p=[text(20,30,title)]
    x=20
    for label,w in zip(columns,widths):
        p += [text(x+8,82,label,23)];x+=w
    for i,row in enumerate(rows):
        y=100+i*62;x=20
        for v,w in zip(row,widths):
            p += [rect(x,y,w-4,56,BG,RED if i==highlight else LIGHT),text(x+8,y+36,v,23)]
            x+=w
    save(name,title,125+len(rows)*62,p)


def figures():
    p=[text(20,30,"Lehrmodell: ein Hart je Kern · Thread ist Software, Hart ist Hardware")]
    for x,n in [(100,0),(650,1)]:
        p += box(x,90,250,70,[f"Softwarethread {n}"])
        p += [line(x+125,165,x+125,220,RED,3,arrow=True)]
        p += box(x,230,250,90,[f"Kern {n}",f"Hart {n}"])
    p += [text(500,200,"Zuordnung durch Scheduler",23,anchor="middle"),
          text(500,380,"Mehr Threads bedeuten nicht automatisch mehr gleichzeitig arbeitende Harts",23,anchor="middle")]
    save("thread","Softwareablauf und Hardware-Ausführungsinstanz",410,p)

    p=[text(20,30,"Unveränderte Eingaben lesen · getrennte Ergebnisobjekte schreiben")]
    for i in range(8):p += [rect(100+i*100,80,94,60,BG,RED if i==4 else LIGHT),text(147+i*100,119,i+1,27,anchor="middle")]
    p += [line(295,145,295,205,arrow=True),line(695,145,695,205,arrow=True)]
    p += box(150,215,290,85,["Thread 0: Index 0–3","1 + 2 + 3 + 4 = 10"])
    p += box(550,215,290,85,["Thread 1: Index 4–7","5 + 6 + 7 + 8 = 26"])
    p += [line(295,310,295,345),line(695,310,695,345),line(295,345,695,345),
          line(500,345,500,375,RED,3,arrow=True),text(500,415,"Nach beiden Abschlüssen: 10 + 26 = 36",25,anchor="middle")]
    save("partition","Aufteilung und anschließende Reduktion",446,p)

    p=[text(20,30,"Organisation der Software · Cacheebenen sind keine SMP-Definition")]
    p += box(70,85,365,75,["SMP: gemeinsame Verwaltung"])
    p += box(560,85,365,75,["AMP: getrennte Zuständigkeiten"])
    for x,labels in [(70,["Kern 0"]),(290,["Kern 1"]),(560,["Kern 0", "Software A"]),(790,["Kern 1", "Software B"])]:
        p += box(x,245,170,85,labels)
    p += [line(250,165,250,205),line(155,205,375,205),line(155,205,155,235,RED,3,arrow=True),line(375,205,375,235,RED,3,arrow=True),
          line(740,165,740,205),line(645,205,875,205),line(645,205,645,235,arrow=True),line(875,205,875,235,arrow=True)]
    # Narrow right-hand labels use a smaller type only inside their own boxes.
    p=[e.replace('font-size="24"','font-size="20"') if 'Software A' in e or 'Software B' in e else e for e in p]
    p += [text(500,389,"Migration und Speichervertrag zusätzlich festlegen",24,anchor="middle")]
    save("smp","Symmetrische und getrennte Softwareorganisation",420,p)

    p=[text(20,30,"Beispiel einer Kohärenzdomäne · Gerätepfad separat prüfen"),rect(35,65,610,270,"#FFFFFF",RED)]
    for x,n in [(70,0),(370,1)]:p += box(x,85,240,80,[f"CPU {n}","privater Datencache"])
    p += box(100,225,470,70,["kohärenter Interconnect"])
    p += [line(190,173,190,215,arrow=True),line(490,173,490,215,arrow=True)]
    p += box(750,95,200,75,["DMA-Gerät"])+box(750,255,200,85,["untere Ebene","Speicher"])
    p += [line(580,260,740,290,arrow=True),line(850,180,850,245,MUTED,2,dash=True,arrow=True),
          text(500,399,"CPU-Kohärenz ist kein automatischer DMA-Maintenance-Vertrag",23,anchor="middle")]
    save("v_domain","Teilnehmergrenze der Kopienkoordination",430,p)

    p=[text(20,30,"Absichtliches Gegenmodell: Write-Through ohne fremde Kopienkoordination")]
    p += marked_box(80,100,240,95,["Kern 0 Cache","neuer Wert 5"])
    p += box(680,100,240,95,["Kern 1 Cache","alte Kopie 0"])
    p += marked_box(370,265,260,80,["unterer Stand 5"])
    p += [line(200,205,200,305),line(200,305,360,305,RED,3,arrow=True),
          text(800,275,"weiter als gültig gelesen",23,anchor="middle"),
          text(500,400,"Ein Schreibweg nach unten aktualisiert nicht jede schon gecachte Fremdkopie",23,anchor="middle")]
    save("stale","Veraltete Fremdkopie ohne Kohärenz",431,p)

    p=[text(20,30,"Kopien · Update · Veröffentlichung: unterschiedliche Anforderungen")]
    for x,labels in [(20,["Kohärenz","eine Adresse","gültige Kopien"]),
                     (355,["atomare RMW","ein Update","unteilbar"]),
                     (700,["Acquire / Release","weitere Nutzdaten","geordnet übergeben"])]:p += box(x,100,280,160,labels)
    p += [text(500,325,"MESI macht i++ nicht atomar · ein atomarer Flagstore publiziert nicht allein",23,anchor="middle")]
    save("three","Drei Fragen korrekter gemeinsamer Daten",356,p)

    p=[text(20,30,"Snooping: Anfrage verteilen · Directory: relevante Teilnehmer gezielt fragen")]
    p += box(20,90,420,65,["Broadcast / gemeinsame Anfrage"])
    for i in range(3):
        p += box(20+i*150,260,130,65,[f"Cache {i}"])
        p += [line(230,165,230,210),line(80+i*150,210,230,210),line(80+i*150,210,80+i*150,250,arrow=True)]
    p += box(590,90,330,65,["Directory: Besitzerinformation"])+box(655,260,200,65,["angefragter Owner"])
    p += [line(755,165,755,250,RED,3,arrow=True),text(500,390,"Fremdread teilt Daten · fremdes Schreibrecht entzieht Gültigkeit",23,anchor="middle")]
    save("snoop","Verteilte und gezielte Kohärenzanfragen",420,p)

    p=[text(20,30,"MESI: stabile Rechte einer ganzen Cachezeile · Modell K")]
    for x,labels,red in [(20,["M: Modified","gültig, geändert","exklusiv"],True),
                         (270,["E: Exclusive","gültig, sauber","exklusiv"],True),
                         (520,["S: Shared","gültig, sauber","teilbar"],False),
                         (770,["I: Invalid","lokal ungültig","kein Treffer"],False)]:
        p += marked_box(x,100,210,155,labels) if red else box(x,100,210,155,labels)
    p += [text(500,322,"M oder E: keine weitere gültige Kopie · S-Kopien stimmen überein",23,anchor="middle"),
          text(500,367,"S kann allein übrig bleiben · I muss alte Bits nicht löschen",23,anchor="middle")]
    save("mesi","MESI-Gültigkeit, Sauberkeit und Schreibrecht",398,p)

    table("silent","Ein lokaler Write auf E benötigt keine fremde Invalidierung",
          ["Schritt","Kern 0","Kern 1","L"],
          [["vor Write","E:0","I","0"],["Write x = 5","M:5","I","0"]],[360,230,230,140],1)

    table("read","Read-Miss: drei getrennte Ausgangslagen, jeweils abgeschlossener Schritt",
          ["vorher beim anderen","Antwort","danach Leser / anderer","L"],
          [["I, keine Kopie","aus L","E / I","gleich"],["E oder S, sauber","sauberer Wert","S / S","gleich"],
           ["M:5, L war 0","aktuelle 5","S:5 / S:5","5"]],[280,240,320,120],2)

    p=[text(20,30,"Write auf Shared · Zeit nach rechts · nur stabile Endzustände benannt")]
    for x,labels in [(20,["Start","S:0 / S:0"]),(260,["Kern 0","fordert Rechte"]),(500,["Kern 1","I + Bestätigung"]),(740,["Abschluss","M:5 / I"] )]:p += box(x,110,220,100,labels)
    for x in [240,480,720]:p += [line(x,160,x+15,160,RED if x==720 else INK,3,arrow=True)]
    p += [text(500,280,"Anfrage ist noch kein Abschluss · unterer Stand L bleibt 0",24,anchor="middle")]
    save("own","Schreibrechtsübernahme mit Invalidierung und Bestätigung",310,p)

    table("trace","Modell K · x startet 0 · Rechte und Werte getrennt verfolgen",
          ["Aktion","Kern 0","Kern 1","L"],
          [["Start","I","I","0"],["Read Kern 0","E:0","I","0"],["Read Kern 1","S:0","S:0","0"],
           ["Write Kern 0: 5","M:5","I","0"],["Read Kern 1","S:5","S:5","5"]],[360,230,230,140],3)

    p=[text(20,30,"Auswerfen ist ein eigenes Ereignis · keine verlorenen geänderten Daten")]
    for y,a,b,caption in [(100,"M:5, L:0","I, L:5","geänderte Daten vorher nach unten"),
                           (260,"S:5 / S:5","I / S:5","verbleibende Kopie kann S bleiben")]:
        p += box(30,y,310,65,[a])+box(640,y,310,65,[b])
        p += [line(350,y+32,630,y+32,RED if y==100 else INK,3,arrow=True),text(500,y+104,caption,23,anchor="middle")]
    save("evict","M-Auswurf und verbleibende saubere S-Kopie",402,p)

    p=[text(20,30,"64-Byte-Zeile ab 0x20001000 · zwei verschiedene Vier-Byte-Objekte")]
    p += [rect(30,105,940,95,"#FFFFFF",LIGHT)]
    for x,label,col in [(30,"a: +0",RED),(90,"b: +4",INK)]:
        p += [rect(x,105,60,95,BG,col),text(x+30,165,label[0],26,anchor="middle")]
    p += [text(30,242,"0x20001000",23),text(970,242,"…103F",23,anchor="end"),
          text(100,295,"Kern 0 schreibt a",24),text(590,295,"Kern 1 schreibt b",24),
          text(500,365,"Verschiedene Wörter verlangen Schreibrecht derselben ganzen Zeile",23,anchor="middle")]
    save("false","False Sharing trotz verschiedener Datenobjekte",397,p)

    p=[text(20,30,"Ausrichtung nur der Basis genügt nicht · Objektgröße 4 Byte · Line 64 Byte")]
    for y,stride in [(105,4),(245,64)]:
        p += [text(20,y+38,f"Abstand {stride}",23)]
        for j in range(2):
            p += [rect(260+j*310,y,300,65,"#FFFFFF",LIGHT),text(410+j*310,y+102,"…1000" if j==0 else "…1040",23,anchor="middle")]
        for i in range(2):
            x=260+stride*i*310/64
            p += [rect(x,y,19,65,BG,RED)]
    p += [text(500,403,"Abstand 4: gleiche Line · Abstand 64: verschiedene Lines",24,anchor="middle")]
    save("v_stride","Basisadresse, Elementabstand und Zeilengrenze",435,p)

    table("race","Hardware-Interleaving · Zähler anfangs 0 · getrennte RMW",
          ["Schritt","Hart 0 Register","Hart 1 Register","Speicher"],
          [["beide lesen","0","0","0"],["beide addieren","1","1","0"],
           ["Hart 0 speichert","1","1","1"],["Hart 1 speichert","1","1","1"]],[340,230,230,160],3)

    p=[text(20,30,"Links: Check und Set getrennt · rechts: atomare Übernahme")]
    p += box(20,85,430,85,["beide lesen frei 0","beide setzen 1"])
    p += marked_box(550,85,430,85,["erster Test-and-Set sieht 0","zweiter sieht schon 1"])
    p += [line(235,180,235,245,arrow=True),line(765,180,765,245,RED,3,arrow=True)]
    p += box(20,255,430,85,["zwei vermeintliche Besitzer","gegenseitiger Ausschluss verletzt"])
    p += marked_box(550,255,430,85,["genau eine Übernahme","anderer wartet"])
    p += [text(500,407,"Status prüfen, dann eintreten · Nutzdatenordnung zusätzlich erforderlich",23,anchor="middle")]
    save("v_check","Logische Race Condition und unteilbare Entscheidung",438,p)

    table("lrsc","Binäres Schloss · freie 0 · belegt 1 · SC-Erfolg ist Status 0",
          ["Aktion","LR-Wert / SC-Status","Schloss"],
          [["beide LR","Wert 0 / Wert 0","0"],["SC Hart 0: 1","Status 0, Erfolg","1"],
           ["SC Hart 1: 1","Status ungleich 0","1"],["neuer LR Hart 1","Wert 1, wartet","1"],
           ["Release, neuer Versuch","LR 0, SC-Status 0","1 nach Übernahme"]],[370,350,240],1)

    p=[text(20,30,"Passende Übergabe ordnet geschützte Daten · zwei Threadabläufe")]
    for y,label in [(105,"Besitzer 0"),(255,"Besitzer 1")]:p += [text(20,y+35,label,24)]
    p += box(215,100,275,70,["Nutzdaten schreiben"])+marked_box(570,100,290,70,["Release: freigeben"])
    p += marked_box(215,250,275,70,["Acquire: übernehmen"])+box(570,250,290,70,["Nutzdaten lesen"])
    p += [line(500,135,560,135,arrow=True),line(500,285,560,285,arrow=True),
          line(715,180,715,208,RED,3),line(352,208,715,208,RED,3),line(352,208,352,240,RED,3,arrow=True),
          text(500,383,"Passende Release-/Acquire-Beobachtung verbindet die beiden Phasen",23,anchor="middle")]
    save("order","Ordnung über die passende Sperrübergabe",415,p)

    p=[text(20,30,"Drei Phasen für gewöhnlichen Speicher · kein Cacheflush")]
    for x,labels in [(20,["Übernahme","lr.w.aq / erfolgreicher SC"]),(355,["kritischer Abschnitt","geschützte Reads / Writes"]),(700,["Freigabe","fence rw,w dann sw 0"])]:
        p += box(x,85,280,95,labels)
    p += [line(300,133,350,133,arrow=True),line(635,133,695,133,RED,3,arrow=True),
          text(500,248,"Die Freigabeordnung steht vor dem Store des freien Schlosswerts",23,anchor="middle")]
    # Assembly labels remain readable inside a single compact phase box.
    p=[e.replace('font-size="24"','font-size="20"') if 'lr.w.aq /' in e or 'Reads /' in e or 'fence rw' in e else e for e in p]
    save("lock","Übernahme, Nutzdaten und geordnete Freigabe",280,p)

    p=[text(20,30,"amoadd.w · unterstütztes ausgerichtetes Wort · Addend 3")]
    p += box(25,105,240,90,["Speicher vorher","10"])+box(380,105,240,90,["atomare Addition","+3"])
    p += marked_box(735,70,240,80,["Rückgabe alt: 10"])+marked_box(735,215,240,80,["Speicher neu: 13"])
    p += [line(275,150,370,150,arrow=True),line(630,150,680,150),line(680,110,680,255),
          line(680,110,725,110,arrow=True),line(680,255,725,255,RED,3,arrow=True),
          text(500,375,"Zwei Inkremente ab 0: alte Werte 0 und 1 · Endwert 2",24,anchor="middle")]
    save("atomic","Altes Rückgabeergebnis und neuer Speicherwert",407,p)

    p=[text(20,30,"Einmalpublikation · links beide Objekte atomar, rechts passende Synchronisation")]
    p += box(20,90,430,160,["relaxed data = 42","relaxed ready = 1","Leser kann ready 1, data 0 sehen"])
    p += marked_box(550,90,430,160,["gewöhnliche data = 42","Release ready = 1","Acquire dieser 1 → data 42"])
    p += [text(500,322,"Kein späteres Überschreiben · kein automatischer Vertrag für eine neue Runde",23,anchor="middle")]
    # Long comparison labels use 22px, while the rest retains the standard size.
    p=[e.replace('font-size="24"','font-size="22"') if 'Leser kann' in e or 'Acquire dieser' in e else e for e in p]
    save("v_flag","Atomare Einzelobjekte und geordnete Einmalveröffentlichung",354,p)

    p=[text(20,30,"Wartekreis trotz korrekter atomarer Sperrprimitive")]
    p += marked_box(80,100,330,100,["Kern 0 hält A","will B"])+marked_box(590,100,330,100,["Kern 1 hält B","will A"])
    p += [line(420,130,580,130,RED,3,arrow=True),line(580,170,420,170,RED,3,arrow=True),
          text(500,281,"Einheitliche Reihenfolge A vor B verhindert diesen Kreis",24,anchor="middle"),
          text(500,332,"Timeout darf keine fremde aktive Sperre einfach löschen",23,anchor="middle")]
    save("dead","Zyklisches Warten und feste Lockreihenfolge",364,p)

    p=[text(20,30,"Derselbe Hart · unterbrochener Besitzer kann während der ISR nicht freigeben")]
    for x,labels in [(20,["Kontext hält L"]),(355,["IRQ / ISR","spinnt auf L"]),(700,["Kontext wartet","auf ISR-Rückkehr"])]:p += box(x,105,280,100,labels)
    p += [line(300,155,350,155,arrow=True),line(635,155,695,155,RED,3,arrow=True),
          text(500,285,"ISR wartet auf Release · Release wartet auf Rückkehr der ISR",24,anchor="middle"),
          text(500,340,"Lokale IRQ-Sperre schließt andere Harts nicht aus",23,anchor="middle")]
    save("v_isr","Selbstdeadlock durch blockierte Interrupt-Rückkehr",372,p)

    p=[text(20,30,"Feste Aufgabe · T(1) = 100 · 20 seriell, 80 parallel · kein Zusatzaufwand")]
    for r,n in enumerate([1,4,100]):
        y=90+r*92;par=80/n
        p += [text(20,y+40,f"N = {n}",24),rect(170,y,20*7,55,BG,LIGHT),
              rect(310,y,max(par*7,5),55,BG,RED),text(240,y+37,"20",24,anchor="middle"),
              text(330+par*7,y+37,f"Zeit {20+par:g}".replace('.',','),23)]
    p += [text(500,398,"S(4) = 2,5 · S(100) ≈ 4,8077 · Grenzfaktor 5",24,anchor="middle")]
    save("amdahl","Lineare Zeitbalken und unveränderte serielle Phase",430,p)

    p=[text(20,30,"Gleiche 80 parallele Zeiteinheiten · Abschluss beim langsamsten Kern")]
    for r,vals in enumerate([[20,20,20,20],[10,10,10,50]]):
        x=210+r*390
        p += [text(x+130,85,"gleichmäßig" if r==0 else "ungleich",25,anchor="middle")]
        for i,v in enumerate(vals):
            y=115+i*62;p += [text(x-35,y+33,f"K{i}",22,anchor="end"),rect(x,y,v*5,45,BG,RED if v==max(vals) else LIGHT),text(x+v*5+12,y+31,v,23)]
        p += [text(x+130,410,"Ende 20" if r==0 else "Ende 50",25,anchor="middle")]
    save("balance","Arbeitsverteilung und letzte Fertigstellung",443,p)

    p=[text(20,30,"4-KiB-Lehrcache · direkt abgebildet · 64-Byte-Line · 32-Bit-Adresse")]
    for x,w,label in [(20,600,"Tag: 20 Bit"),(620,180,"Index: 6 Bit"),(800,180,"Offset: 6 Bit")]:
        p += [rect(x,100,w-4,70,BG,RED if x==800 else LIGHT),text(x+w/2,144,label,24,anchor="middle")]
    p += [text(500,232,"Adresse 0x20001084",26,anchor="middle"),
          text(500,284,"Tag 0x20001 · Index 2 · Offset 4 · Linebasis 0x20001080",24,anchor="middle"),
          text(500,346,"64 Sätze · Metadaten sind keine Nutzdatenbytes",23,anchor="middle")]
    save("mapping","Tag, Index und Byteoffset einer konkreten Adresse",378,p)

    p=[text(20,30,"Lehrtimer · Zähler 0–999 · High bei 0–249")]
    x=lambda t:100+t*.8
    p += [line(x(0),300,x(1000),300,MUTED)]
    for t in [0,250,500,750,1000]:p += [line(x(t),295,x(t),305,MUTED),text(x(t),336,t,22,anchor="middle")]
    p += [path([(x(0),250),(x(0),130),(x(250),130),(x(250),250),(x(1000),250)]),
          text(200,108,"250 High-Takte",24,anchor="middle"),text(650,227,"750 Low-Takte",24,anchor="middle"),
          text(500,395,"1 MHz / 10 / 1000 = 100 Hz · aktive Zeit 25 %",24,anchor="middle")]
    save("timer","Zählertakte und PWM-Periode",427,p)

    p=[text(20,30,"Konzeptweg, kein vorhandenes Labor-SoC · Datenfluss und Zuständigkeit")]
    for x,labels in [(20,["Sensor","Peripherie"]),(355,["DMA","Puffer"]),(700,["CPU-Threads","Ergebnis"])]:p += box(x,100,280,95,labels)
    p += [line(300,147,350,147,arrow=True),line(635,147,695,147,RED,3,arrow=True)]
    p += [text(500,265,"Abschluss / IRQ → Puffer übernehmen → Daten korrekt synchronisieren",23,anchor="middle"),
          text(500,326,"Kopienkoordination und DMA-Maintenance separat prüfen",23,anchor="middle"),
          text(500,381,"DLP oder NPU sind optionale Rechenwege innerhalb des Systemvertrags",23,anchor="middle")]
    save("v_soc","Sensortransfer und gemeinsame Rechenarbeit",413,p)


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
    print("29 Lehrdiagramme geschrieben"+(" (SVG und PNG)." if args.png else " (SVG)."))
