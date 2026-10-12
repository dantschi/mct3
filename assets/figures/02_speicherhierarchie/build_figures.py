#!/usr/bin/env python3
"""Abbildungen für VL02: SVG; mit --png zusätzlich PNG via Playwright/Chromium.

Alle Zahlen sind Lehrmodelle. PNGs werden direkt aus den SVGs gerendert,
damit Folien und PDF-Handout denselben Inhalt zeigen.
"""
from pathlib import Path
from html import escape
import argparse

OUT = Path(__file__).resolve().parent
INK, MUTED, HAIR, BG, RED = "#1D1D1F", "#86868B", "#E5E5EA", "#F5F5F7", "#E2001A"
FIGURES = []

def text(x, y, value, size=24, anchor="start", color=INK):
    return f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" fill="{color}">{escape(str(value))}</text>'

def box(x, y, w, h, fill=BG, stroke=HAIR):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'

def arrow(x1, y1, x2, y2):
    return f'<path d="M{x1},{y1} H{x2} V{y2}" fill="none" stroke="{MUTED}" stroke-width="2" marker-end="url(#arrow)"/>'

def save(name, height, parts, description):
    head = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="{height}" viewBox="0 0 1000 {height}" role="img">',
        f'<title>{escape(description)}</title>',
        '<style>text{font-family:Inter,Arial,sans-serif;font-weight:400}</style>',
        f'<rect width="1000" height="{height}" fill="#FFFFFF"/>',
        f'<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="{MUTED}"/></marker></defs>',
    ]
    (OUT / f"{name}.svg").write_text("\n".join(head + parts + ["</svg>"]) + "\n", encoding="utf-8")
    FIGURES.append((name, height))

def hierarchy():
    p = []
    for x,y,w,h,label in [(20,95,130,70,"CPU"),(210,25,180,65,"L1-I"),(210,165,180,65,"L1-D"),(470,95,190,70,"L2"),(740,95,235,70,"DRAM")]:
        p += [box(x,y,w,h),text(x+w/2,y+h/2+8,label,28,"middle")]
    p += [arrow(150,115,180,58),arrow(180,58,210,58),arrow(150,145,180,198),arrow(180,198,210,198)]
    p += [arrow(390,58,430,115),arrow(430,115,470,115),arrow(390,198,430,145),arrow(430,145,470,145),arrow(660,130,740,130)]
    p += [text(300,120,"Befehle",22,"middle"),text(300,260,"Daten",22,"middle"),text(565,205,"gemeinsam",22,"middle")]
    save("hierarchy",285,p,"Anfragewege: CPU zu L1-I/L1-D, danach L2 und DRAM.")

def locality():
    p=[]
    for y,title,addresses in [(35,"Zeitlich",["0x1000","0x1000","0x1000"]),(175,"Räumlich",["0x1000","0x1004","0x1008"])]:
        p += [text(20,y,title,26)]
        for j,(a,result) in enumerate(zip(addresses,["Miss","Hit","Hit"])):
            x=210+j*250
            p += [box(x,y-25,220,90,stroke=RED if j==0 else HAIR),text(x+110,y+4,a,26,"middle"),text(x+110,y+40,result,24,"middle",RED if j==0 else INK)]
            if j<2:p.append(arrow(x+220,y+20,x+250,y+20))
    p += [text(20,290,"Jeweils kalt; 64-Byte-Lines; keine Verdrängung.",24)]
    save("locality",315,p,"Zwei getrennte Zugriffsspuren mit Miss, Hit, Hit.")

def line():
    p=[text(20,30,"Dezimaladressen · Blockgröße 64 Byte",26)]
    # Byte cells: marker at byte 40, not an arbitrary location.
    p += [box(50,70,896,65),text(50,170,"960",24),text(946,170,"1023",24,"end")]
    x=50+40*14
    p += [f'<path d="M{x},60 V145" stroke="{RED}" stroke-width="3"/>',text(x,205,"1000",26,"middle",RED)]
    p += [text(500,255,"40 Byte ab Blockbeginn",26,"middle")]
    save("line-bounds",280,p,"Adresse 1000 innerhalb des Blocks 960 bis 1023 mit Offset 40.")

def layout():
    p=[text(20,30,"Array: benachbarte 4-Byte-Elemente",26)]
    for j in range(8):
        p += [box(20+j*112,55,110,65),text(75+j*112,97,f"+{4*j}",26,"middle")]
    p += [text(20,165,"Liste: ein mögliches Streulayout",26)]
    for j,a in enumerate(["0x2000","0x8040","0x4010","0x9000"]):
        x=20+j*250
        p += [box(x,190,200,65),text(x+100,232,a,26,"middle")]
        if j<3:p.append(arrow(x+200,222,x+250,222))
    save("array-list",280,p,"Zusammenhängende Arrayelemente und verteilte per Zeiger verbundene Listenknoten.")

def amat():
    p=[text(20,30,"100 Zugriffe: Prüfung + zusätzliche Miss-Kosten",26)]
    # Both bars use 1.6 pixels per accumulated cycle.
    p += [text(20,80,"100 × 1 = 100 Takte",24),box(20,95,160,40)]
    p += [text(20,180,"5 × 100 = 500 Takte zusätzlich",24),box(20,195,800,40,stroke=RED)]
    p += [text(20,280,"Gesamt: 600 Takte / 100 Zugriffe = 6 Takte pro Zugriff",26)]
    save("amat",305,p,"Gleich skalierte Balken: hundert Takte Prüfung und fünfhundert Takte zusätzliche Miss-Kosten.")

def bits():
    p=[text(20,30,"32 Bit · 32 KiB Daten · 64-Byte-Lines",26)]
    for y,label,widths,labels in [(75,"Direct Mapped",[17,9,6],["Tag 17","Index 9","Offset 6"]),(195,"4-Way",[19,7,6],["Tag 19","Index 7","Offset 6"])]:
        p += [text(20,y,label,24)]
        x=20
        for w,t in zip(widths,labels):
            width=w*30
            p += [box(x,y+15,width,60,fill="#FFFFFF"),text(x+width/2,y+55,t,26,"middle")]
            x+=width
    save("bitfields",290,p,"Proportionale Bitfelder: 17/9/6 für Direct Mapped und 19/7/6 für vier Ways.")

def datapath():
    p=[]
    # Independent address components; stored and requested tags converge at compare.
    for x,y,w,h,label in [(20,20,170,60,"Index"),(20,140,170,60,"Anfrage-Tag"),(20,260,170,60,"Offset"),(270,20,330,85,"Cache-Eintrag"),(680,135,270,65,"Tag-Vergleich"),(350,260,250,60,"Offset-MUX")]:
        p += [box(x,y,w,h),text(x+w/2,y+38,label,25,"middle")]
    p += [text(435,87,"Tag · Valid · Daten",22,"middle")]
    p += [arrow(190,50,270,50),arrow(190,170,680,170)]
    # Stored tag and Valid leave at top, so their route never crosses the data box.
    p += [arrow(600,50,815,135),arrow(600,90,640,240),arrow(640,240,475,260)]
    p += [arrow(190,290,350,290),arrow(600,290,900,290),text(910,298,"Daten",22)]
    p += [text(815,230,"Valid = 1 und Tag gleich → Hit",22,"middle",RED)]
    save("datapath",345,p,"Index liest den Eintrag; gespeichertes und angefragtes Tag werden geprüft; Offset wählt Daten.")

def thrash():
    p=[text(20,30,"32 KiB · 64-Byte-Lines · beide Caches kalt",24)]
    p += [text(25,80,"Load",25),text(455,80,"Direct Mapped",25),text(785,80,"4-Way",25)]
    for j in range(8):
        y=100+j*36
        p += [text(25,y+25,f"{j+1}.  0x{'1000' if j%2==0 else '9000'}",24)]
        for x,value in [(455,"Miss"),(785,"Miss" if j<2 else "Hit")]:
            p += [text(x,y+25,value,24,color=RED if value=="Miss" else INK)]
    p += [text(20,430,"Ein Set: 1 Platz gegenüber 4 Plätzen",25)]
    save("thrashing",455,p,"Acht wechselnde Loads: acht Misses gegenüber zwei Misses und sechs Hits.")

def replacement():
    p=[text(20,30,"Nach A, B, C, D, A · alt links, neu rechts",26)]
    for y,title,order,victim in [(90,"FIFO",["A","B","C","D"],"A"),(210,"LRU",["B","C","D","A"],"B")]:
        p += [text(20,y+35,title,27)]
        for j,name in enumerate(order):
            x=150+j*125
            p += [box(x,y,105,60,stroke=RED if j==0 else HAIR),text(x+52,y+39,name,28,"middle")]
        p += [text(700,y+38,f"E verdrängt {victim}",26)]
    save("fifo-lru",300,p,"FIFO behält die Ladereihenfolge; LRU verjüngt A und verdrängt B.")

def writes():
    p=[text(20,30,"Store-Hits: 0 → 5 → 7",26)]
    rows=[
        ("Write-Through", "Cache 7", "nächste Ebene 7"),
        ("mit Schreibpuffer", "Cache 7", "Updates ggf. ausstehend"),
        ("Write-Back", "Cache 7, Dirty 1", "nächste Ebene noch 0"),
    ]
    for j,(title,left,right) in enumerate(rows):
        y=60+j*85
        p += [text(20,y+38,title,23),box(290,y,280,65),box(650,y,330,65),text(430,y+40,left,24,"middle"),text(815,y+40,right,22,"middle")]
        if j!=2:p.append(arrow(570,y+32,650,y+32))
    save("write-states",325,p,"Gleiche Stores, getrennte Weitergabestrategien und Zustände.")

def allocate():
    p=[text(20,30,"Zwei Fragen an eine Schreibstrategie",26)]
    p += [box(20,65,460,150),box(520,65,460,150)]
    p += [text(250,105,"Änderung weitergeben?",27,"middle"),text(250,155,"Write-Through",25,"middle"),text(250,190,"oder Write-Back",25,"middle")]
    p += [text(750,105,"Bei Store-Miss laden?",27,"middle"),text(750,155,"Write-Allocate",25,"middle"),text(750,190,"oder No-Write-Allocate",25,"middle")]
    save("write-allocate",240,p,"Weitergabe und Anlegen einer Line bei Store-Miss sind getrennte Entscheidungen.")

def matrix():
    p=[text(20,28,"16 × 16 Wörter · 64 Byte je Zeile · 8 Cache-Sets",25)]
    # Two array halves pair rows with the same set; all sixteen columns remain visible.
    p += [text(250,70,"Zeilen 0–7",24,"middle"),text(750,70,"Zeilen 8–15",24,"middle")]
    for r in range(8):
        y=90+r*25
        p += [text(50,y+19,r,22,"middle"),text(550,y+19,r+8,22,"middle"),text(485,y+19,f"Set {r}",20,"middle")]
        for c in range(16):
            for x,fill in [(90+c*20,BG),(590+c*20,"#FFFFFF")]:
                p += [f'<rect x="{x}" y="{y}" width="20" height="25" fill="{fill}" stroke="{HAIR}"/>']
    # Outside-grid arrows mark visit direction; pairing is represented by set labels.
    p += [text(140,335,"Zeilenweise:  →  +4 Byte",26),text(570,335,"Spaltenweise:  ↓  +64 Byte",26)]
    p += [text(140,375,"1 Miss, dann 15 Hits je Zeile",25),text(570,375,"Zeile r + 8 ersetzt Zeile r",25)]
    save("matrix",405,p,"Arrayraster: sechzehn Zeilen mit acht Set-Indizes und zwei Traversalrichtungen.")

def blocksize():
    p = [text(20, 30, "Dezimaladressen: 0, 4, 64, 68 · beide Caches kalt", 25)]
    p += [text(20, 75, "16-Byte-Lines: Miss, Hit, Miss, Hit", 26)]
    for j in range(8):
        x = 50 + j * 112
        p += [box(x, 100, 112, 60, stroke=RED if j in (0, 4) else HAIR)]
        p += [text(x + 56, 139, f"{16*j}–{16*j+15}", 21, "middle")]
    p += [text(20, 245, "128-Byte-Line: Miss, Hit, Hit, Hit", 26)]
    p += [box(50, 270, 896, 60, stroke=RED), text(498, 308, "0–127", 26, "middle")]
    # Identical spatial scale for both block sizes; paired labels avoid overlap.
    for y in (160, 330):
        for address in (0, 4, 64, 68):
            x = 50 + address * 7
            p += [f'<path d="M{x},{y} V{y+15}" stroke="{RED}" stroke-width="2"/>']
        p += [text(80, y + 40, "0 und 4", 22, "middle"), text(530, y + 40, "64 und 68", 22, "middle")]
    save("blocksize", 390, p, "Gleiche Adressen innerhalb kleiner und großer Cache-Blöcke; zwei gegenüber einem Fill.")

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--png",action="store_true")
    parser.add_argument("--chromium",default="/usr/bin/chromium")
    args=parser.parse_args()
    for build in (hierarchy,locality,line,layout,amat,bits,datapath,thrash,replacement,writes,allocate,matrix,blocksize):build()
    if args.png:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser=p.chromium.launch(executable_path=args.chromium,headless=True,args=["--no-sandbox"])
            page=browser.new_page(device_scale_factor=2)
            for name,height in FIGURES:
                page.set_viewport_size({"width":1000,"height":height})
                page.set_content('<body style="margin:0">' + (OUT/f"{name}.svg").read_text(encoding="utf-8") + '</body>')
                page.locator("svg").screenshot(path=str(OUT/f"{name}.png"))
            browser.close()
    print(f"{len(FIGURES)} SVGs" + (" und PNGs" if args.png else ""))

if __name__=="__main__":main()
