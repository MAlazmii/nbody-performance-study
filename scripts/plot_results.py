"""Render the recorded historical stages and the fresh benchmark samples."""
import csv
import json
import math
from pathlib import Path
import statistics

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
INK = "#e6eef3"
MUTED = "#a9bbca"
BACKGROUND = "#101923"
PANEL = "#172431"
TEAL = "#58d5bb"
GOLD = "#f2b968"


def main():
    with (ROOT / "data/cirrus-stages.csv").open(newline="") as file:
        stages = list(csv.DictReader(file))
    labels = [stage["stage"] for stage in stages]
    historical = [float(stage["seconds"]) for stage in stages]
    local = json.loads((ROOT / "data/local-comparison.json").read_text())
    samples = local["seconds"]
    variants = ["supplied", "submitted"]
    assert len(labels) == 6 and all(math.isfinite(x) and x > 0 for x in historical)
    for variant in variants:
        values = samples[variant]
        assert len(values) == 5 and all(math.isfinite(x) and x > 0 for x in values)
        assert statistics.median(values) == local["median_seconds"][variant]

    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 12, "text.color": INK,
        "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": INK,
        "svg.hashsalt": "nbody-performance-study-v1",
    })
    fig, (left, right) = plt.subplots(
        1, 2, figsize=(13, 6.8), facecolor=BACKGROUND,
        gridspec_kw={"width_ratios": [1.55, 1]},
    )
    fig.subplots_adjust(left=.295, right=.95, bottom=.22, top=.73, wspace=.55)
    fig.text(.07, .91, "Optimising an N-body simulation", size=27, weight="bold")
    fig.text(.07, .855, "A Cirrus coursework retrospective and a same-flags local comparison", color=MUTED, size=13)
    for ax in (left, right):
        ax.set_facecolor(PANEL)
        ax.spines[:].set_visible(False)
        ax.grid(axis="x", color=MUTED, alpha=.18, linewidth=.7)
        ax.tick_params(length=0, pad=8)
        ax.set_axisbelow(True)

    y = list(range(len(labels)))
    plot_labels = ["Baseline (−O0)", "Compiler (−O3 −ipo)", "Manual changes + fusion",
                   "Tiling and aliasing", "Arithmetic and aliasing", "Fast-math + host flags"]
    left.set_title("Cirrus · historical 500-step runs", loc="left", color=INK, pad=16, weight="bold", size=13)
    left.set_xscale("log")
    left.set_xlim(10, 1400)
    left.set_xticks([10, 30, 100, 300, 1000], ["10", "30", "100", "300", "1,000"])
    left.hlines(y, 10, historical, color=TEAL, alpha=.40, linewidth=2)
    left.scatter(historical, y, c=[MUTED, TEAL, TEAL, TEAL, TEAL, GOLD], s=60, zorder=3)
    left.set_yticks(y, plot_labels)
    left.invert_yaxis()
    left.set_xlabel("Runtime (s, log scale)")
    for yi, value in zip(y, historical):
        left.annotate(f"{value:.2f}", (value, yi), xytext=(9, 0), textcoords="offset points", va="center", size=10)

    right.set_title("Apple M1 · fresh 20-step runs", loc="left", color=INK, pad=16, weight="bold", size=13)
    right.set_yticks([0, 1], ["Supplied", "Submitted"])
    right.set_ylim(1.55, -.55)
    right.set_xlim(0, max(samples["supplied"] + samples["submitted"]) * 1.15)
    right.set_xlabel("Solver runtime (s)")
    for y_pos, name, color in zip([0, 1], variants, [MUTED, TEAL]):
        values = samples[name]
        median = local["median_seconds"][name]
        right.scatter(values, [y_pos + offset for offset in [-.12, -.06, 0, .06, .12]], color=color, s=28, alpha=.85)
        right.scatter(median, y_pos + .23, marker="D", color=GOLD, s=42)
        right.annotate(f"{median:.2f} s median", (median, y_pos + .42),
                       va="center", ha="right" if name == "supplied" else "left", size=10)

    fig.text(.07, .105, "Cirrus records six reported stages with different source or compiler settings. Repeat counts were unavailable.", size=10, color=MUTED)
    fig.text(.07, .067, "Apple M1 shows every sample and the median (gold diamond). Both builds used the same flags and input.", size=10, color=MUTED)
    for ext in ("png", "svg"):
        metadata = {"Software": "N-body performance study"} if ext == "png" else {"Date": None, "Title": "N-body performance study"}
        output = ROOT / f"figures/performance.{ext}"
        fig.savefig(output, dpi=170, facecolor=BACKGROUND, metadata=metadata)
        if ext == "svg":
            output.write_text("\n".join(line.rstrip() for line in output.read_text(encoding="utf-8").splitlines()) + "\n", encoding="utf-8")
    plt.close(fig)


if __name__ == "__main__":
    main()
