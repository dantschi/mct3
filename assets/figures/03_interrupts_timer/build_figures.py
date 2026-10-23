#!/usr/bin/env python3
"""VL03-Lehrmodelle als SVG; --png rendert dieselben Quellen mit Chromium."""
from pathlib import Path
from html import escape
import argparse

OUT=Path(__file__).resolve().parent
INK,MUTED,HAIR,BG,RED="#1D1D1F","#86868B","#E5E5EA","#F5F5F7","#E2001A"
FIGURES=[]

def text(x,y,value,size=24,anchor="start",color=INK):
    return f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" fill="{color}">{escape(str(value))}</text>'

def box(x,y,w,h,stroke=HAIR):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{BG}" stroke="{stroke}" stroke-width="2"/>'

def line(x1,y1,x2,y2,color=MUTED):
    return f'<path d="M{x1},{y1} H{x2} V{y2}" fill="none" stroke="{color}" stroke-width="2"/>'

def arrow(x1,y1,x2,y2):
    return line(x1,y1,x2,y2).replace('/>', ' marker-end="url(#arrow)"/>')

def save(name,h,p,description):
    head=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="{h}" viewBox="0 0 1000 {h}" role="img">',
          f'<title>{escape(description)}</title>',
          '<style>text{font-family:Inter,Arial,sans-serif;font-weight:400}</style>',
          f'<rect width="1000" height="{h}" fill="#FFFFFF"/>',
          f'<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="{MUTED}"/></marker></defs>']
    (OUT/f"{name}.svg").write_text("\n".join(head+p+["</svg>"])+"\n",encoding="utf-8")
    FIGURES.append((name,h))

def poll():
    # Common time scale: x=200+375*t with t in milliseconds.
    p=[text(20,30,"Modell: Ereignis 1,2 ms · ISR-Eintritt 1,3 ms · Ende 1,5 ms",24)]
    p += [text(20,90,"Busy-Wait",23),box(200,60,450,45),text(425,90,"wiederholt prüfen",23,"middle")]
    p += [text(20,165,"Periodisch",23),line(200,155,950,155)]
    for t in (0,1,2):
        x=200+375*t
        p += [f'<circle cx="{x}" cy="155" r="6" fill="{INK}"/>']
    p += [text(20,240,"Interrupt",23),box(200,210,450,45),text(425,240,"Hauptprogramm",23,"middle"),
          box(687.5,210,75,45,RED),text(725,240,"ISR",22,"middle"),
          box(762.5,210,187.5,45),text(855,240,"Main",23,"middle")]
    p += [line(650,45,650,260,RED),text(650,290,"1,2",22,"middle",RED),
          text(200,290,"0",22,"middle"),text(575,290,"1",22,"middle"),text(950,290,"2 ms",22,"end")]
    save("poll-vs-irq",315,p,"Alternative Abläufe auf derselben Millisekundenachse.")

def trap():
    p=[]
    stages=[(20,150,"Main"),(220,300,"Hardware"),(570,240,"Software"),(860,120,"mret")]
    for x,w,label in stages:
        p += [box(x,40,w,135),text(x+w/2,75,label,26,"middle")]
    p += [text(35,116,"MIE = 1",23),text(235,112,"mepc · mcause · MPP",23),
          text(235,151,"MPIE ← MIE; MIE ← 0",23),
          text(590,112,"Prolog · Handler",23),text(590,151,"Epilog",23),
          text(920,117,"Rückkehr",21,"middle")]
    for start,end in [(170,220),(520,570),(810,860)]:p.append(arrow(start,100,end,100))
    p += [text(20,220,"Hardware hält Trap-Zustand; Software erhält weitere Register.",25)]
    save("trap-state",245,p,"Arbeitsteilung beim Trap-Eintritt und bei der Rückkehr.")

def levels():
    p=[]
    for y,label in [(20,"Timer: mtime / mtimecmp"),(110,"Software: msip")]:
        p += [box(20,y,320,65),text(40,y+40,label,24)]
    p += [box(20,205,320,85),text(40,238,"UART 1 · Sensor 2 · Taster 3",23),
          text(40,271,"externe Geräte-IDs",22)]
    p += [box(400,215,200,65),text(500,255,"PLIC",27,"middle")]
    p += [box(760,50,220,240),text(870,92,"Hart",28,"middle"),
          text(780,142,"Kategorie 7",24),text(780,198,"Kategorie 3",24),text(780,254,"Kategorie 11",24)]
    p += [arrow(340,52,700,138),arrow(700,138,760,138),
          arrow(340,142,660,194),arrow(660,194,760,194),
          arrow(340,247,400,247),arrow(600,247,760,247)]
    p += [text(20,330,"Cause-Code der Kategorie ≠ Geräte-ID aus Claim",25)]
    save("two-levels",355,p,"Lokale Kategorien und externes PLIC-Sammelsignal zum Hart.")

def mtvec():
    p=[text(20,30,"BASE 0x80000100 · mtvec 0x80000101 · ausgewählte Slots",24)]
    for j,(kind,offset,address) in enumerate([
        ("Exception",0,"0x80000100"),("MSI, Cause 3",12,"0x8000010C"),
        ("MTI, Cause 7",28,"0x8000011C"),("MEI, Cause 11",44,"0x8000012C")]):
        y=60+j*62
        p += [text(20,y+37,kind,25),text(340,y+37,f"+{offset} Byte",25),
              box(560,y,420,50),text(770,y+34,address,27,"middle")]
    save("mtvec",315,p,"Adressbildung für ausgewählte Kategorien und Exception-Basis.")

def timer():
    p=[text(20,30,"Im Machine-Mode-Modell müssen alle Bedingungen gelten.",25)]
    for x,w,label,detail in [(20,350,"mtime ≥ mtimecmp","MTIP: pending"),
                             (420,220,"MTIE = 1","Kategorie frei"),
                             (710,260,"MIE = 1","global frei")]:
        p += [box(x,65,w,100),text(x+w/2,105,label,27,"middle"),text(x+w/2,143,detail,23,"middle")]
    p += [arrow(370,115,420,115),arrow(640,115,710,115),
          text(840,225,"Timer-Trap möglich",25,"middle"),arrow(840,165,840,195)]
    save("timer-gates",250,p,"Vergleichsbedingung und getrennte Freigaben für den Timer-Trap.")

def hilo():
    p=[text(20,30,"Zählerübergang:",25),text(250,30,"0x00000001_FFFFFFFF → 0x00000002_00000000",24)]
    for x,label,value in [(20,"HI vorher","1"),(375,"LO danach","0"),(730,"HI nochmals","2")]:
        p += [box(x,70,250,100),text(x+125,110,label,26,"middle"),text(x+125,151,value,28,"middle")]
    p += [arrow(270,120,375,120),arrow(625,120,730,120)]
    p += [text(20,225,"HI 1 + LO 0 wäre falsch: 0x00000001_00000000",25,color=RED),
          text(20,270,"HI vorher ≠ HI nochmals → Leseversuch wiederholen",25)]
    save("hi-lo",295,p,"Überlauf zwischen Zugriffen und Erkennung durch einen zweiten HI-Wert.")

def drift():
    # x=375+250*(t-10); only marked times are represented.
    p=[text(20,30,"Solltermin 10,0 ms · tatsächlicher Eintritt 10,2 ms",25)]
    p += [text(20,115,"Relativ",25),box(425,80,250,55),text(550,116,"1 ms ab Eintritt",24,"middle"),
          text(675,165,"11,2 ms",25,"middle",RED)]
    p += [text(20,230,"Sollraster",25),box(375,195,250,55),text(500,231,"1 ms ab Sollwert",24,"middle"),
          text(625,280,"11,0 ms",25,"middle")]
    p += [line(425,45,425,65,RED),text(375,320,"10,0",23,"middle"),text(875,320,"12,0 ms",23,"middle"),
          line(375,295,875,295)]
    save("tick-drift",345,p,"Relativer Termin verschiebt die Phase, absolutes Raster erhält sie.")

def plic():
    p=[]
    for j,label in enumerate(["UART · ID 1","Sensor · ID 2","Taster · ID 3"]):
        y=20+j*80
        p += [box(20,y,250,55),text(145,y+36,label,25,"middle"),arrow(270,y+27,400,y+27)]
    p += [box(400,20,260,215),text(530,60,"PLIC",29,"middle"),
          text(420,105,"Pending",24),text(420,145,"Priorität",24),text(420,185,"Kontext-Enable",24)]
    p += [box(790,65,190,120),text(885,105,"Hart 0",27,"middle"),text(885,147,"M-Mode",25,"middle"),
          arrow(660,120,790,120),text(780,260,"MEI · Cause 11",24,"middle")]
    save("plic-table",285,p,"Externe Quellen über PLIC zum Machine-Mode-Kontext.")

def claim():
    p=[text(20,30,"Normaler Lebenszyklus einer bekannten Gerätequelle",25)]
    stages=[(20,160,"Gerät aktiv"),(215,155,"Pending"),(405,155,"Claim ID"),
            (595,180,"Gerät bedienen"),(810,170,"Complete ID")]
    for x,w,label in stages:
        p += [box(x,65,w,95),text(x+w/2,116,label,22,"middle")]
    for a,b in [(180,215),(370,405),(560,595),(775,810)]:p.append(arrow(a,110,b,110))
    p += [text(410,210,"PLIC-Pending gelöscht",22),text(20,255,"Geräteursache bearbeiten, danach dieselbe ID abschließen.",25)]
    save("claim",285,p,"Claim, getrennte Gerätebearbeitung und Complete in Reihenfolge.")

def foreground():
    p=[text(20,30,"Ein Hart: ISR und Hauptprogramm laufen nacheinander.",25)]
    p += [box(20,80,240,80),text(140,128,"Main vorher",26,"middle"),
          box(330,80,200,80,RED),text(430,128,"kurze ISR",26,"middle"),
          box(650,80,330,80),text(815,114,"Main später:",25,"middle"),
          text(815,148,"Nutzarbeit",25,"middle")]
    p += [arrow(260,120,330,120),arrow(530,120,650,120),
          line(275,50,275,180,RED),text(275,220,"Ereignis",23,"middle",RED),
          text(590,220,"zusätzliche Wartezeit",23,"middle")]
    save("foreground",255,p,"Sofortige kurze Behandlung und spätere Hauptprogramm-Nutzarbeit.")

def nesting():
    p=[text(20,30,"Ein Hardware-mepc, getrennte Softwareframes bei Nesting",25)]
    p += [box(20,60,440,105),text(40,100,"äußerer Eintritt: mepc 0x80001000",24),
          text(40,144,"innerer Eintritt: mepc 0x80002040",24,color=RED)]
    p += [box(570,65,410,75),text(590,96,"äußerer Frame:",24),text(590,125,"Rückkehr 0x80001000",24)]
    p += [box(570,185,410,75,RED),text(590,216,"innerer Frame:",24),text(590,245,"Rückkehr 0x80002040",24)]
    p += [arrow(775,185,775,140),text(20,220,"Ohne Sicherung ist die",25),text(20,253,"ursprüngliche Adresse verloren.",25)]
    p += [text(20,310,"Rückkehr: innen → außen → Main; Register und Status ebenfalls erhalten.",24)]
    save("nesting",335,p,"Überschriebenes mepc und die nötigen getrennten Sicherungsrahmen.")

def event_capture():
    p=[text(20,30,"Ereignisse, gespeicherter Zustand und spätere Beobachtung",25)]
    p += [text(20,105,"Impulse",24),text(20,195,"Bereitschaft",24)]
    pulse_path="M200,110 H300 V65 H330 V110 H480 V65 H510 V110 H600 V65 H630 V110 H950"
    p += [f'<path d="{pulse_path}" fill="none" stroke="{RED}" stroke-width="3"/>']
    p += [f'<path d="M200,205 H300 V160 H950" fill="none" stroke="{INK}" stroke-width="3"/>',
          text(240,195,"0",22,"middle"),text(400,150,"1",22,"middle"),
          f'<path d="M850,50 V225" stroke="{MUTED}" stroke-width="2" stroke-dasharray="5 5"/>',
          text(850,280,"Status lesen: 1",24,"middle"),
          arrow(200,240,950,240),text(950,225,"Zeit",23,"end"),
          text(20,325,"Das Bit erhält einen Hinweis; die Zahl der Impulse bleibt unbekannt.",24)]
    save("event-capture",350,p,"Drei Ereignisse ergeben in einem Bereitschaftsbit nur einen gespeicherten Hinweis.")

def timer_vs_external():
    p=[box(20,35,350,80),text(195,68,"Timer",26,"middle"),
       text(195,99,"mtime / mtimecmp",24,"middle"),
       box(20,180,350,90),text(195,215,"UART 1 · Sensor 2 · Taster 3",23,"middle"),
       text(195,250,"externe Geräte-IDs",23,"middle"),
       box(450,180,160,90),text(530,235,"PLIC",28,"middle"),
       box(780,35,200,235),text(880,77,"Hart",29,"middle"),
       text(880,123,"Kategorie 7",23,"middle"),text(880,234,"Kategorie 11",23,"middle"),
       '<path d="M370,75 H690 V110 H780" fill="none" stroke="'+MUTED+'" stroke-width="2" marker-end="url(#arrow)"/>',
       arrow(370,225,450,225),arrow(610,225,780,225),
       text(560,52,"Timer-Anforderung",23,"middle"),text(690,205,"extern",22,"middle"),
       f'<path d="M880,270 V325 H530 V270" fill="none" stroke="{MUTED}" stroke-width="2" marker-end="url(#arrow)"/>',
       text(20,350,"Software fragt zusätzlich:",23),text(705,365,"Claim → konkrete Geräte-ID",24,"middle",RED)]
    save("timer-vs-external",390,p,"Timerkategorie und externe Sammelkategorie sind von der Geräte-ID aus Claim getrennt.")

def response_budget():
    # A single linear time axis: x=100+5*t, t in microseconds.
    p=[text(20,30,"Zwei Endpunkte derselben Ereignisbehandlung",25)]
    segments=[(0,40,"1",BG),(40,5,"2",HAIR),(45,8,"3",BG),
              (53,80,"4",BG),(133,30,"5",HAIR)]
    for start,duration,label,fill in segments:
        x=100+5*start
        p += [f'<rect x="{x}" y="85" width="{5*duration}" height="60" fill="{fill}" stroke="{MUTED}"/>',
              text(x+2.5*duration,123,label,22,"middle")]
    p += [arrow(100,175,945,175)]
    for t in (0,40,53,133,163):
        x=100+5*t
        p += [line(x,170,x,180),text(x,208,t,22,"middle")]
    for t,label,anchor in [(53,"Daten gesichert","start"),(163,"Ergebnis fertig","end")]:
        x=100+5*t
        p += [line(x,72,x,155,RED),text(x,65,label,23,anchor,RED)]
    p += [text(100,245,"Zeit ab Ereignis [µs]",23),
          text(20,295,"1  Blockierung: 40 µs",23),text(365,295,"2  Eintritt: 5 µs",23),
          text(670,295,"3  Sicherung: 8 µs",23),
          text(20,335,"4  Warten auf Hauptprogramm: 80 µs",23),text(600,335,"5  Auswertung: 30 µs",23)]
    save("response-budget",365,p,"Datensicherung nach 53 Mikrosekunden und fertige Auswertung nach 163 Mikrosekunden.")

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--png",action="store_true")
    parser.add_argument("--chromium",default="/usr/bin/chromium")
    builders={"poll-vs-irq":poll,"trap-state":trap,"two-levels":levels,"mtvec":mtvec,
              "timer-gates":timer,"hi-lo":hilo,"tick-drift":drift,"plic-table":plic,
              "claim":claim,"foreground":foreground,"nesting":nesting,
              "event-capture":event_capture,"timer-vs-external":timer_vs_external,
              "response-budget":response_budget}
    parser.add_argument("--only",nargs="+",choices=builders,
                        help="Nur die benannten Abbildungen erzeugen")
    args=parser.parse_args()
    for name in args.only or builders:builders[name]()
    if args.png:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser=p.chromium.launch(executable_path=args.chromium,headless=True,args=["--no-sandbox"])
            page=browser.new_page(device_scale_factor=2)
            for name,h in FIGURES:
                page.set_viewport_size({"width":1000,"height":h})
                page.set_content('<body style="margin:0">'+(OUT/f"{name}.svg").read_text(encoding="utf-8")+'</body>')
                page.locator("svg").screenshot(path=str(OUT/f"{name}.png"))
            browser.close()
    print(f"{len(FIGURES)} SVGs"+(" und PNGs" if args.png else ""))

if __name__=="__main__":main()
