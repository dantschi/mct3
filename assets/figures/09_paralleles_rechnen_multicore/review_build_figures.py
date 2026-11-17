#!/usr/bin/env python3
"""Generate VL09's explicitly assumed Amdahl/coordination-cost example.

Run with Python 3, NumPy and Matplotlib; no network access is needed.
The single-core reference has no coordination overhead.  The two curves
apply only for N >= 2 and are calculations, not measurements.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

FIGURES = Path(__file__).resolve().parent
ROOT = FIGURES.parents[2]
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / ".quarto/cache/vl09-matplotlib"))
os.environ.setdefault("XDG_CACHE_HOME", str(ROOT / ".quarto/cache"))
Path(os.environ["MPLCONFIGDIR"]).mkdir(parents=True, exist_ok=True)
Path(os.environ["XDG_CACHE_HOME"]).mkdir(parents=True, exist_ok=True)

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

T1 = 100.0
SERIAL = 0.2
COORDINATION = 0.02


def ideal_time(cores):
    return T1 * (SERIAL + (1.0 - SERIAL) / cores)


def coordinated_time(cores):
    return ideal_time(cores) + T1 * COORDINATION * cores


def main():
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 22,
        "axes.labelsize": 23,
        "xtick.labelsize": 20,
        "ytick.labelsize": 20,
        "legend.fontsize": 19,
        "text.color": "#1D1D1F",
        "axes.labelcolor": "#1D1D1F",
        "xtick.color": "#1D1D1F",
        "ytick.color": "#1D1D1F",
        "axes.edgecolor": "#656D76",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.facecolor": "white",
        "figure.facecolor": "white",
        "grid.color": "#D7DADF",
        "grid.linewidth": 0.7,
        "svg.hashsalt": "mct3-vl09-growing-overhead",
    })
    cores = np.linspace(2, 24, 600)
    integer_cores = np.arange(2, 25)
    times = coordinated_time(integer_cores)
    best = int(integer_cores[times.argmin()])
    assert best == 6
    assert np.isclose(coordinated_time(4), 48.0)
    assert np.isclose(coordinated_time(6), 136 / 3)
    assert np.isclose(coordinated_time(7), 318 / 7)

    fig, ax = plt.subplots(figsize=(14, 6), layout="constrained")
    ax.plot(cores, coordinated_time(cores), color="#E2001A", linewidth=2.8,
            label="mit wachsendem Zusatzaufwand")
    ax.plot(integer_cores, times, linestyle="none", marker="o", markersize=4.8,
            color="#E2001A")
    ax.plot(cores, ideal_time(cores), color="#1D1D1F", linewidth=2.2,
            linestyle="--", label="ideales Amdahl-Modell")
    ax.scatter([1], [T1], color="#1D1D1F", marker="D", s=65, zorder=4,
               label="Ein-Kern-Referenz ohne Zusatzaufwand")
    ax.scatter([best], [coordinated_time(best)], color="#E2001A", edgecolors="#1D1D1F",
               linewidths=1.4, s=115, zorder=5)
    ax.annotate("Minimum für ganze N\nN = 6, T ≈ 45,33", (best, coordinated_time(best)),
                xytext=(9.4, 61), fontsize=22,
                arrowprops={"arrowstyle": "->", "color": "#1D1D1F", "linewidth": 1.4},
                color="#1D1D1F")
    ax.set(xlim=(0.5, 24.5), ylim=(15, 106),
           xlabel="Kernzahl N", ylabel="Laufzeit T(N) [Zeiteinheiten]",
           xticks=[1, 2, 4, 6, 8, 12, 16, 20, 24])
    ax.grid(axis="y", alpha=0.75)
    ax.legend(loc="upper right", frameon=False)
    svg = FIGURES / "overhead.svg"
    fig.savefig(svg, bbox_inches="tight", metadata={"Date": None})
    svg.write_text("\n".join(line.rstrip() for line in svg.read_text().splitlines()) + "\n",
                   encoding="utf-8")
    fig.savefig(FIGURES / "overhead.png", dpi=180, bbox_inches="tight",
                metadata={"Software": "MCT3 calculated Amdahl example"})
    plt.close(fig)
    print(json.dumps({"T1": T1, "s": SERIAL, "c": COORDINATION,
                      "minimum_integer_cores": best,
                      "T4": float(coordinated_time(4)),
                      "T6": float(coordinated_time(6)),
                      "T7": float(coordinated_time(7))}, ensure_ascii=False))


if __name__ == "__main__":
    main()
