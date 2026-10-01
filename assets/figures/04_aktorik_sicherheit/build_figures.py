#!/usr/bin/env python3
"""Lehrfiguren VL04. GPT/WDT sind kein RISC-V-ISA-Bestandteil."""
from pathlib import Path
OUT = Path(__file__).resolve().parent
INK, MUTED = "#1D1D1F", "#5F6368"
CNT, CCR, OUTP, WDT = "#1565C0", "#E65100", "#1B5E20", "#6A1B9A"

def svg(w, h):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">',
            f'<rect width="{w}" height="{h}" fill="#fff"/>',
            '<style>text{font-family:Arial,Helvetica,sans-serif;fill:#1D1D1F}</style>']

def T(x, y, s, size=16, fill=INK, w="600"):
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{w}" fill="{fill}">{s}</text>'

def save(name, p):
    (OUT / name).write_text("\n".join(p)+"\n</svg>\n", encoding="utf-8"); print(name)

def fig_paths():
    p = svg(1100, 240)
    p += [T(16, 22, "Lehr-Modell. GPIO steuert, die externe Versorgung leistet.", 15, MUTED, "400")]
    p += [T(16, 58, "Sensor, Main, PWM-Timer, Pin-Mux, Treiber, Aktor", 17, CNT)]
    p += [T(16, 92, "Getrennter Leistungsweg, z. B. 12 V, gemeinsame Masse ohne galvanische Trennung", 16, CCR)]
    p += [T(16, 126, "CLINT ist die Systemzeit. Der GPT erzeugt das Pin-Signal und laeuft weiter, wenn Main haengt.", 16, OUTP)]
    p += [T(16, 166, "Watchdog und Reset sind die Ueberwachung. Ein Reset trennt die Motorversorgung nicht.", 16, WDT)]
    p += [T(16, 210, "Kein direktes GPIO am Motor.", 16)]
    save("paths.svg", p)

def fig_prescaler():
    p = svg(1100, 220)
    p += [T(16, 22, "Kernbeispiel: f_tim = 100 MHz, PSC = 99, Teiler 100, f_cnt = 1 MHz, 1 us/Tick.", 16)]
    p += [T(16, 58, "PSC = 0 teilt durch 1. PSC = 3 ist nur die Detailansicht eines Teilers durch 4.", 16, CNT)]
    p += [T(16, 96, "Separates Beispiel: PSC = 9999 ergibt 10 kHz und 100 us pro Tick.", 16, CCR)]
    p += [T(16, 136, "16 Bit: Werte 0..65535 sind 65536 Zustaende.", 16)]
    p += [T(16, 170, "Bei 100 MHz ohne Teiler: 0,65536 ms. Bei 1 MHz: 65,536 ms.", 16, WDT)]
    p += [T(16, 206, "Up, Down und Center-Aligned haben eigene Endpunkte. Nicht eine Formel fuer alle.", 15, MUTED, "400")]
    save("prescaler.svg", p)

def fig_power():
    p = svg(1100, 250)
    p += [T(16, 20, "T = 1 ms, Pegel 0/3,3 V. 25, 50 und 75 Prozent sowie die Konstanten 0 und 100 Prozent.", 15)]
    p += [T(16, 56, "25 Prozent: Mittelwert 0,825 V, RMS 1,65 V. Die Mittelwertlinie ist keine geglaettete Pin-Spannung.", 16, CNT)]
    p += [T(16, 96, "Ideale ohmsche Last, R = 1 kOhm: P = D * V^2 / R = 2,7225 mW.", 16, OUTP)]
    p += [T(16, 132, "Konstante 0,825 V an derselben Last: 0,680625 mW. Nicht V_avg^2/R fuer das Rechteck.", 16, CCR)]
    p += [T(16, 172, "Motor: Strom, Gegen-EMK und Treiber. LED: ungefaehre Lichtleistung, Wahrnehmung extra.", 16)]
    p += [T(16, 214, "Multimeter nur mit Messart und Bandbreite deuten. 50 Prozent Duty ist nicht halbe Motorleistung.", 15, MUTED, "400")]
    save("pwm-power.svg", p)

def fig_edge():
    p = svg(1100, 240)
    p += [T(16, 20, "Up-Counting 0..999, ARR = 999, CCR = 250, Active-High wenn CNT kleiner CCR.", 16)]
    p += [T(16, 56, "Ticks 0..249 aktiv: 250 Intervalle. Ticks 250..999 inaktiv: 750 Intervalle.", 16, OUTP)]
    p += [T(16, 96, "N = 1000, f_PWM = 1 kHz, t_HIGH = 250 us, D = 25 Prozent.", 17, CNT)]
    p += [T(16, 136, "CCR 0, 250, 500, 1000 ergeben 0, 25, 50 und 100 Prozent.", 16, CCR)]
    p += [T(16, 176, "Match ist CNT gleich CCR. Danach ist der Ausgang inaktiv, weil CNT nicht kleiner CCR ist.", 16)]
    p += [T(16, 214, "Der Pin braucht keinen Compare-Interrupt. ARR = 999 ist ein voller Zustand.", 15, MUTED, "400")]
    save("edge-pwm.svg", p)

def fig_resolution():
    p = svg(1100, 200)
    p += [T(16, 22, "f_cnt = 1 MHz, berechnetes Modell, keine Messung.", 15, MUTED, "400")]
    p += [T(16, 60, "1 kHz: N = 1000, ARR = 999, Schritt 0,1 Prozent", 17, CNT)]
    p += [T(16, 96, "4 kHz: N = 250, ARR = 249, Schritt 0,4 Prozent", 17, CCR)]
    p += [T(16, 132, "20 kHz: N = 50, ARR = 49, Schritt 2 Prozent", 17, WDT)]
    p += [T(16, 176, "Ein 16-Bit-Zaehler liefert bei kurzer Periode nicht 16 Bit Tastverhaeltnis.", 16)]
    save("resolution.svg", p)

def fig_software():
    p = svg(1100, 220)
    p += [T(16, 20, "Ideal 50 us / 50 us waere 10 kHz. Laufzeit der Funktionen kommt dazu.", 15, MUTED, "400")]
    p += [T(16, 58, "Busy-Wait bindet Main. Freigegebene Interrupts koennen trotzdem laufen.", 16, CCR)]
    p += [T(16, 96, "Konstruiert: fallende Flanke 20 us zu spaet. HIGH 70 us, LOW 50 us, Periode 120 us, etwa 58,3 Prozent.", 15, CNT)]
    p += [T(16, 140, "ISR-PWM gibt Zeit frei, bleibt aber softwarelatenzbehaftet.", 16, OUTP)]
    p += [T(16, 180, "Hardware-PWM folgt dem Timer, nicht der ISR-Latenz.", 16, WDT)]
    save("sw-vs-hw.svg", p)

def fig_preload():
    p = svg(1100, 220)
    p += [T(16, 20, "Gewaehltes Timer-Modell, kein universelles Registerrezept.", 15, MUTED, "400")]
    p += [T(16, 56, "Ungepuffert: CCR von 250 auf 750 bei CNT = 500 kann den schon inaktiven Pin wieder einschalten.", 16, CCR)]
    p += [T(16, 100, "Gepuffert: der neue Wert wird erst beim Update-Ereignis aktiv.", 16, OUTP)]
    p += [T(16, 144, "Init: Takt, Pin-Mux, Modus, Polaritaet, PSC/ARR/CCR, Preload, Flags, Kanal und Timer.", 16, CNT)]
    p += [T(16, 188, "PSC, ARR und CCR allein schalten noch keinen Ausgang.", 16, WDT)]
    save("preload.svg", p)

def fig_rgb():
    p = svg(1100, 230)
    p += [T(16, 20, "Ein ARR, drei CCR. Active-Low: aktiver LED-Anteil ist nicht der HIGH-Anteil.", 15)]
    p += [T(16, 56, "Common-Cathode und Common-Anode brauchen je Zweig eine Strombegrenzung.", 16, CNT)]
    p += [T(16, 96, "Gamma-Lehrannahme D = b^2,2. Bei N = 1000: b 0 / 0,25 / 0,5 / 0,75 / 1", 16, CCR)]
    p += [T(16, 132, "ergibt gerundet CCR 0, 47, 218, 531 und 1000.", 17, OUTP)]
    p += [T(16, 176, "R=100, G=50, B=0 kann orange wirken. Spektrum und Abgleich sind nicht garantiert.", 15, MUTED, "400")]
    save("rgb-gamma.svg", p)

def fig_apps():
    p = svg(1100, 250)
    p += [T(16, 20, "Drei Anwendungen, drei Perioden. RC ist kein Motortreiber.", 15, MUTED, "400")]
    p += [T(16, 52, "RC: 1 kOhm, 10 uF, 1 kHz, 25 Prozent. Tau 10 ms, fc etwa 15,9 Hz, Mittel 0,825 V.", 15, CNT)]
    p += [T(16, 84, "Unbelastete Welligkeit etwa 61,9 mV. 95 Prozent eines Sprungs etwa 30 ms.", 15, CNT)]
    p += [T(16, 124, "Servo: 20 ms, Pulse 1,0 / 1,5 / 2,0 ms. ARR = 19999, CCR = 1000 / 1500 / 2000 bei 1 MHz.", 15, CCR)]
    p += [T(16, 168, "H-Bruecke: 3,3 V steuern, z. B. 12 V leisten. Keine komplementaeren Roh-Gates ohne Totzeit.", 15, WDT)]
    p += [T(16, 214, "Winkel und Wiederholrate sind servospezifisch.", 15, MUTED, "400")]
    save("applications.svg", p)

def fig_wdt():
    p = svg(1100, 210)
    p += [T(16, 20, "Ideales Timeout 2 s. Feeds bei 0, 0,5 und 1,0 s. Kein weiterer Feed, Reset bei 3,0 s.", 16)]
    p += [T(16, 60, "Eigener Takt und Zeitfenster sind zwei Eigenschaften.", 16, WDT)]
    p += [T(16, 100, "Ein Fenster-Watchdog muss keinen eigenen Takt haben. Ein unabhaengiger WDT kann ein Fenster haben.", 15)]
    p += [T(16, 144, "0xAA55 ist ein fiktiver Feed. Laborcode braucht die dokumentierte Sequenz.", 16, CCR)]
    p += [T(16, 184, "Nicht jeder Watchdog hat nur Reset. Vorwarnung ist moeglich.", 15, MUTED, "400")]
    save("watchdog.svg", p)

def fig_window():
    p = svg(1100, 210)
    p += [T(16, 20, "Haengt Main und der Tick fuettert weiter, gibt es keinen Reset.", 16, CCR)]
    p += [T(16, 56, "Fehlt der Fortschritt, bleibt der Feed aus und das Timeout kommt.", 16, WDT)]
    p += [T(16, 100, "Beispiel-Fenster 0,5 bis 2 s: 0,2 s zu frueh, 1 s gueltig, nach 2 s zu spaet.", 16, CNT)]
    p += [T(16, 144, "Raender sind datenblattabhaengig. 10 ms Fading-Feed passt nicht automatisch ins Fenster.", 15)]
    p += [T(16, 184, "Ein Feed beweist keine korrekte Rechnung.", 16, OUTP)]
    save("window.svg", p)

def fig_safe():
    p = svg(1100, 220)
    p += [T(16, 20, "Letzter Feed 1,0 s, Main steht ab 1,2 s, idealer Reset 3,0 s.", 16)]
    p += [T(16, 56, "1,8 s laeuft die PWM ohne frischen Main-Fortschritt weiter.", 16, CCR)]
    p += [T(16, 96, "Erkennung, Ausgang aus, Neustart und sicherer Aktorzustand sind verschiedene Zeiten.", 16, WDT)]
    p += [T(16, 136, "Lampe: aus. Motor: aus, bremsen oder halten sind nicht dasselbe.", 16, CNT)]
    p += [T(16, 176, "Enable-Pin waehrend Reset definiert halten. Externe Versorgung bleibt.", 15, MUTED, "400")]
    p += [T(16, 206, "Nominell 2 s bei +/-20 Prozent Takt: etwa 1,667 bis 2,5 s. Keine Auslegungsempfehlung.", 14, MUTED, "400")]
    save("safe-state.svg", p)

if __name__ == "__main__":
    for fn in (fig_paths, fig_prescaler, fig_power, fig_edge, fig_resolution, fig_software,
               fig_preload, fig_rgb, fig_apps, fig_wdt, fig_window, fig_safe):
        fn()
