#!/usr/bin/env python3
"""Reproduzierbare Lehrdiagramme für VL05; keine Messdaten oder Schaltpläne.

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


def dot(x, y, radius=5, fill=RED):
    return f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{fill}"/>'


def bits_wave(bits, x0, scale, high, low, color=RED, start=0):
    return digital([(start+i, start+i+1, bool(bit)) for i, bit in enumerate(bits)],
                   x0, scale, high, low, color)


def fields(tokens, x, y, widths=None):
    result = []
    for i, token in enumerate(tokens):
        width = widths[i] if widths else (30 if token in ["A", "N"] else 65)
        result += [rect(x, y, width-2, 45), text(x+(width-2)/2, y+30,
                                             token, 23, anchor="middle")]
        x += width
    return result


def figures():
    p = box(20, 70, 220, 105, ["Prozessor", "lokale Register"])
    p += box(330, 70, 270, 105, ["I²C-Controller", "Busprotokoll"])
    p += box(705, 70, 275, 105, ["Sensor: Adresse 68", "Registerindex 3B"])
    p += [line(240, 118, 325, 118, arrow=True), line(600, 118, 700, 118, arrow=True),
          text(35, 35, "Drei Adressarten · Hexwerte 68 und 3B"),
          text(135, 225, "MMIO-Adresse", anchor="middle"),
          text(465, 225, "Geräteadresse", anchor="middle"),
          text(842, 225, "Register im Sensor", anchor="middle"),
          line(900, 275, 100, 275, MUTED, arrow=True),
          text(500, 265, "Empfangene Bytes zurück zur Verarbeitung", anchor="middle")]
    save("path", "Lokaler Gerätezugriff, Busadresse und Sensorregister", 315, p)

    p = [text(20, 30, "Wort: 0x53 = 0101 0011"), text(20, 165, "Zeitfolge: LSB zuerst")]
    for top, bits, order in [(55, [0,1,0,1,0,0,1,1], list(range(7,-1,-1))),
                              (190, [1,1,0,0,1,0,1,0], list(range(8)))]:
        for i, (bit, index) in enumerate(zip(bits, order)):
            x=150+i*98
            p += [rect(x,top,83,47), text(x+41.5,top+32,bit,27,anchor="middle"),
                  text(x+41.5,top+75,f"d{index}",22,anchor="middle")]
    p += [line(150, 295, 930, 295, MUTED, arrow=True), text(930, 324, "Zeit →",22,anchor="end")]
    save("shift", "Schriftliche Bitgewichte und serielle LSB-Reihenfolge", 340, p)

    p = box(30, 55, 235, 195, ["Endpunkt 1"])
    p += box(735, 55, 235, 195, ["Endpunkt 2"])
    p += [text(245,90,"TX",22,anchor="end"),text(755,90,"RX",22),
          text(245,225,"RX",22,anchor="end"),text(755,225,"TX",22),
          line(265,85,730,85,arrow=True),line(735,220,270,220,arrow=True),
          text(500,55,"Senden 1 → 2",22,anchor="middle"),
          text(500,205,"Senden 2 → 1",22,anchor="middle"),
          line(150,280,850,280,MUTED),line(150,250,150,280,MUTED),
          line(850,250,850,280,MUTED),text(500,315,"Gemeinsamer GND-Bezug",anchor="middle")]
    save("uart-wiring", "UART-Sende- und Empfangspfade mit gemeinsamem Bezug", 340, p)

    data=[1,1,0,0,1,0,1,0]
    p=[text(20,30,"UART 8N1 · 0x53 · LSB zuerst")]
    p += [bits_wave([1,0]+data+[1,1],180,65,65,120,start=-1)]
    for i,label in enumerate(["Start"]+[f"d{i}" for i in range(8)]+["Stop"]):
        p += [text(180+(i+.5)*65,159,label,22,anchor="middle"),
              line(180+i*65,55,180+i*65,125,LIGHT,1)]
    p += [text(125,159,"Idle",22,anchor="middle"),text(900,159,"Idle",22,anchor="middle"),
          text(30,70,"HIGH",22),text(30,125,"LOW",22)]
    p += axis(180,830,215,[(180,"0"),(830,"10")],"Zeit / Bitintervalle")
    save("uart-frame", "Start, acht Datenintervalle und Stop für das Byte 0x53", 285, p)

    p=[text(20,30,"Startflanke als Zeitnullpunkt · Punkte sind Samples")]
    p += [bits_wave([0]+data+[1],170,75,70,125),
          line(170,50,170,175,MUTED,dash=True)]
    for i in range(8):
        x=170+(1.5+i)*75
        p += [dot(x,70 if data[i] else 125),text(x,174,f"d{i}",22,anchor="middle")]
    p += [dot(170+9.5*75,70),text(170+9.5*75,174,"Stop",22,anchor="middle")]
    p += axis(170,920,220,[(170,"0"),(282.5,"1,5"),(807.5,"8,5"),(882.5,"9,5")],"Zeit / Tᵦ")
    save("uart-sampling", "Ideale Abtastmitten relativ zur Startflanke", 290, p)

    p=[text(20,30,"16 RX-Plätze · anfangs 8 belegt · keine Entnahme")]
    for i in range(16):
        x=100+i*52
        p += [rect(x,60,46,50,fill=LIGHT if i<8 else "#FFFFFF"),
              text(x+23,94,i+1,22,anchor="middle")]
    p += [text(100,146,"8 belegt"),text(520,146,"8 frei")]
    marks=[(100,"0"),(660,"8T_f"),(730,"9T_f")]
    p += axis(100,900,230,marks,"Zeit nach letztem Abschluss")
    p += [line(660,175,660,230,MUTED),line(730,175,730,230,RED),
          text(660,172,"voll",22,anchor="end"),
          text(745,205,"Overrun",22),
          text(500,332,"8T_f ≈ 694,4 µs · 9T_f = 781,25 µs",anchor="middle")]
    save("uart-fifo", "Frei, voll und überlaufen bei lückenlosem UART-Empfang", 365, p)

    p=box(20,45,250,250,["Controller"])
    p+=box(730,45,250,250,["Target"])
    for y,label,reverse in [(70,"SCK",False),(130,"MOSI",False),
                             (210,"MISO",True),(275,"CS, Active-Low",False)]:
        p += [line(730 if reverse else 270,y,275 if reverse else 725,y,arrow=True),
              text(500,y-12,label,23,anchor="middle")]
    p.append(text(500,340,"GND und Versorgung kommen zusätzlich hinzu",anchor="middle"))
    save("spi-wiring", "Vier SPI-Signale mit getrenntem Rückpfad", 370, p)

    p=box(25,35,235,100,["Controller","0x96"])
    p+=box(740,35,235,100,["Target","0x3C"])
    p += [line(260,67,735,67,arrow=True),text(500,55,"MOSI",22,anchor="middle"),
          line(740,112,265,112,arrow=True),text(500,101,"MISO",22,anchor="middle"),
          text(170,180,"Takte"),text(480,180,"Controller"),text(780,180,"Target")]
    for y,k,a,b in [(220,0,"96","3C"),(260,1,"2C","79"),(300,4,"63","C9"),(340,8,"3C","96")]:
        p += [text(170,y,k),text(480,y,"0x"+a),text(780,y,"0x"+b)]
    save("spi-ring","Gleichzeitiger Austausch in zwei Acht-Bit-Modellregistern",365,p)

    p=box(20,120,240,105,["Controller","SCK, MOSI, MISO"])
    p += [line(260,172,380,172),line(380,65,380,305),
          text(20,35,"SCK / MOSI / MISO gemeinsam"),text(950,25,"CS vom Controller",22,anchor="end")]
    for i,y in enumerate([30,150,270],1):
        p+=box(505,y,270,70,[f"Target {i}"])
        p += [line(380,y+35,500,y+35,arrow=True),
              line(940,y+35,780,y+35,arrow=True),text(850,y+22,f"CS{i}",22,anchor="middle")]
    p.append(text(500,380,"Drei Targets: 3 + 3 = 6 Signalpins",anchor="middle"))
    save("spi-topo","Gemeinsame SPI-Signale und getrennte Auswahl je Target",410,p)

    p=[text(20,30,"Geeignete 8-Bit-Stufen · Hexbytes 11 → 22 → 33")]
    for x,label in [(30,"Controller"),(280,"A: nah"),(530,"B"),(780,"C: fern")]:
        p+=box(x,60,195,70,[label])
    for x in [225,475,725]:p.append(line(x,95,x+50,95,arrow=True))
    p += [text(20,180,"Takte"),text(340,180,"A"),text(590,180,"B"),text(840,180,"C")]
    for y,k,values in [(220,8,["11","00","00"]),(260,16,["22","11","00"]),
                        (300,24,["33","22","11"])]:
        p.append(text(20,y,k))
        for x,value in zip([340,590,840],values):p.append(text(x,y,"0x"+value))
    p += [line(280,340,975,340,MUTED),text(500,374,"SCK und CS gemeinsam; Übernahme gerätespezifisch",22,anchor="middle")]
    save("spi-chain","Bytewanderung in drei geeigneten Schiebestufen",400,p)

    p=[text(20,28,"SPI: Punkte = Samples · jeweils zwei Taktperioden")]
    for mode in range(4):
        cpol=mode//2;cpha=mode%2;top=65+mode*78
        p += [text(20,top+25,f"Modus {mode}",24),
              text(140,top+25,f"CPOL {cpol}, CPHA {cpha}",22)]
        levels=[cpol,1-cpol]*2+[cpol]
        p.append(bits_wave(levels,400,105,top,top+35))
        for cycle in range(2):
            phase=(cycle*2+1 if cpha==0 else cycle*2+2)
            y=top if (1-cpol if cpha==0 else cpol) else top+35
            p.append(dot(400+phase*105,y))
    save("spi-modes","Ruhepegel und Abtastflanken der vier SPI-Modi",380,p)

    p=[text(20,30,"Modus 0 · Wechsel bei 0 ns, nächstes Sample bei 50 ns"),
       text(20,112,"SCK"),text(20,222,"Daten")]
    p += [digital([(0,50,False),(50,100,True)],190,7.4,75,125,INK),
          digital([(0,25,False),(25,100,True)],190,7.4,185,235),
          line(190+25*7.4,170,190+25*7.4,285,MUTED,dash=True),
          line(190+40*7.4,170,190+40*7.4,285,MUTED,dash=True),
          line(190+50*7.4,55,190+50*7.4,285,RED,dash=True),
          text(375,160,"gültig ab 25 ns",22,anchor="middle"),
          text(560,160,"Sample",22,anchor="middle"),
          text(730,265,"10 ns Setup: 40 … 50 ns",22,anchor="middle")]
    p += axis(190,930,300,[(190,"0"),(375,"25"),(486,"40"),(560,"50"),(930,"100")],"Zeit / ns")
    save("spi-timing","Bereitstellung, Setup und Sample im Halbperiodenbudget",370,p)

    p=[text(20,30,"I²C: SDA und SCL gemeinsam · je ein Pull-up")]
    p+=box(20,100,200,95,["Controller"])
    for x,i in [(365,1),(575,2),(785,3)]:
        p+=box(x,100,190,95,[f"Target {i}"])
    p += [line(120,70,900,70,INK),line(120,230,900,230,INK),
          text(20,70,"SDA",22),text(20,230,"SCL",22)]
    for x in [120,460,670,880]:
        p += [line(x,70,x,100,MUTED),line(x,195,x,230,MUTED),dot(x,70,3,INK),dot(x,230,3,INK)]
    p += [text(285,60,"Pull-ups nach V_IO",22,anchor="middle"),
          line(285,68,285,70,MUTED),line(285,195,285,230,MUTED),
          text(285,185,"Pull-up",22,anchor="middle"),
          text(500,300,"Zwei Signalpins; Adressen und elektrische Grenzen bleiben",22,anchor="middle")]
    save("i2c-wiring","Gemeinsam angeschlossene I²C-Teilnehmer und Pull-ups",330,p)

    p=[text(20,30,"Ein Leitungsmodell · aktive LOW-Anforderung dominiert"),
       text(500,66,"V_IO",24,anchor="middle"),line(500,75,500,90),
       rect(480,90,40,65,fill="#FFFFFF",stroke=INK,radius=0),
       text(555,129,"R_P",24),line(500,155,500,190),
       line(170,190,830,190,INK),text(830,180,"Leitung",22,anchor="end")]
    for x,label in [(280,"Teilnehmer A"),(720,"Teilnehmer B")]:
        p += [line(x,190,x,225),dot(x,190,4,INK)]
        p+=box(x-130,225,260,70,[label,"LOW oder frei"])
        p += [line(x,295,x,320),line(x-25,320,x+25,320),
              text(x,350,"GND",22,anchor="middle")]
    save("open-drain","Pull-up und freigebende beziehungsweise sinkende Ausgänge",375,p)

    p=[text(20,30,"START und STOP bei SCL HIGH · getrennte Ausschnitte")]
    for x,label,levels in [(180,"START",[1,1,0,0]),(620,"STOP",[0,0,1,1])]:
        p += [text(x+150,70,label,24,anchor="middle"),text(x-70,124,"SCL",22),
              text(x-70,224,"SDA",22),
              bits_wave([1]*4,x,75,105,150,INK),
              bits_wave(levels,x,75,205,250),
              line(x+150,85,x+150,265,MUTED,dash=True),
              line(x,285,x+300,285,MUTED,arrow=True)]
    p.append(text(500,325,"Normale Datenwechsel erfolgen bei SCL LOW",anchor="middle"))
    save("i2c-conditions","Besondere Datenflanken bei hohem Taktpegel",350,p)

    p=[text(20,30,"Adressbyte D0 = 1101 0000 · danach Quittung")]
    p += [bits_wave([1,1,0,1,0,0,0,0,0],160,85,65,110)]
    for i,label in enumerate(["1","1","0","1","0","0","0","0","ACK"]):
        p += [text(160+(i+.5)*85,150,label,23,anchor="middle"),
              line(160+i*85,55,160+i*85,117,LIGHT,1)]
    p += [text(500,200,"Sender: acht Bits; Empfänger: neunter Takt",23,anchor="middle")]
    p += fields(["S","D0","A","6B","A","00","A","P"],240,230)
    p.append(text(500,320,"Write: Target bestätigt Adresse und beide Schreibbytes",22,anchor="middle"))
    save("i2c-byte","Acht Adressbits, ACK und Aufweckfolge",345,p)

    p=[text(20,30,"Feldschema, keine maßstäbliche Zeitachse")]
    p += [text(20,104,"Auswahl",22)]
    p += fields(["S","D0","A","3B","A"],170,75)
    p += [text(20,225,"Lesen",22)]
    p += fields(["Sr","D1","A","10","A","00","A","E0","A","00","A","40","A","00","N","P"],
                160,190,[50,65,28]+[65,28]*6+[45])
    p += [text(500,155,"Kein STOP dazwischen · Sr = Repeated START",22,anchor="middle"),
          text(500,285,"Target: Adress-ACK · Controller: fünf ACK, zuletzt NACK",22,anchor="middle"),
          text(500,325,"9 Bytes × 9 Takte = 81 SCL-Takte",anchor="middle")]
    save("i2c-burst","Registerzeiger und sechs gelesene Datenbytes mit Quittungsrollen",350,p)

    p=[text(20,30,"Freigabeabsicht und wirklicher Leitungspegel trennen")]
    p += [text(20,92,"Controller",22),text(20,121,"Sollpegel",22),
          digital([(0,2,False),(2,6,True)],280,110,65,110,INK),
          text(20,213,"SCL gemessen",22),
          digital([(0,4,False),(4,6,True)],280,110,175,220),
          rect(500,245,220,35),
          text(610,270,"Stretching",22,anchor="middle"),
          line(500,50,500,230,MUTED,dash=True),line(720,150,720,230,MUTED,dash=True)]
    p += [line(280,295,940,295,MUTED,arrow=True), text(940,280,"Zeit, schematisch",22,anchor="end"), text(20,325,"Oben HIGH: Controller gibt frei; unten HIGH: Leitung ist gestiegen",22)]
    save("stretch","Zusätzliche LOW-Zeit trotz Freigabe des Controllers",350,p)

    p=[text(20,30,"Arbitration: A sendet A0, B plant D0 · MSB zuerst")]
    for top,label,bits in [(70,"A",[1,0,1,0,0,0,0,0]),(160,"B",[1,1,1,1,1,1,1,1]),
                            (250,"Bus",[1,0,1,0,0,0,0,0])]:
        p += [text(20,top+25,label),bits_wave(bits,190,90,top,top+42,
                                           start=0)]
    p += [line(325,55,325,310,MUTED,dash=True),
          text(340,145,"B: wollte 1, liest 0 → verliert",22),
          text(500,350,"Entscheidung beim zweiten Bit, Stelle 6",anchor="middle")]
    # HIGH in a participant row means released, not actively driven.
    p += [text(20,385,"Ab Verlust gibt B frei; seine übrigen Bits werden nicht gesendet",21)]
    save("i2c-arbitration","Erster Unterschied entscheidet durch dominantes LOW",410,p)

    p=[text(20,30,"Gleiche Erhöhung beider Leitungen: +0,8 V")]
    for x,a,b,cm,label in [(275,2.5,.5,1.5,"vorher"),(720,3.3,1.3,2.3,"danach")]:
        base=255;scale=50
        p += [text(x,68,label,24,anchor="middle"),
              rect(x-90,base-a*scale,65,a*scale,fill=BG),
              rect(x+25,base-b*scale,65,b*scale,fill=LIGHT),
              text(x-57.5,max(100,base-a*scale-12),str(a).replace(".",","),22,anchor="middle"),
              text(x+57.5,base-b*scale-12,str(b).replace(".",","),22,anchor="middle"),
              text(x-57.5,285,"A",22,anchor="middle"),text(x+57.5,285,"B",22,anchor="middle"),
              line(x-110,base-cm*scale,x+110,base-cm*scale,RED,dash=True),
              text(x,325,f"V_CM = {str(cm).replace('.', ',')} V",22,anchor="middle")]
    p += [line(100,255,950,255,MUTED),text(20,90,"Volt",22),text(70,261,"0",22),
          text(500,374,"V_d bleibt 2 V · gestrichelt: gemeinsamer Pegel",anchor="middle")]
    save("diff","Differenzspannung und steigender Common-Mode-Pegel",400,p)


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
    print("20 Lehrdiagramme geschrieben" + (" (SVG und PNG)." if args.png else " (SVG)."))
