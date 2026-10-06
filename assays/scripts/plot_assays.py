"""Plot turnaround time from assays-instrument-turnaround.csv to see which assays take the most time.

Counts of how many of each assay are run are not available, so every plot is per assay (or per group
of assays) and not weighted by volume.
Run from anywhere:  python assays/scripts/plot_assays.py   (writes PNG files to assays/plots/)
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ASSAY_DIR = Path(__file__).resolve().parent.parent
PLOT_DIR = ASSAY_DIR / "plots"
BAND_ORDER = ["likely in house", "uncertain", "likely outsourced"]
BAND_COLORS = {"likely in house": "#2f855a", "uncertain": "#d69e2e", "likely outsourced": "#c53030"}
NOTE = "Unweighted: how many of each assay are run is unknown."


def save(fig, name):
    PLOT_DIR.mkdir(exist_ok=True)
    fig.tight_layout()
    fig.savefig(PLOT_DIR / name, dpi=130)
    plt.close(fig)


def range_bars(ax, labels, mins, maxs, colors=None):
    """Horizontal bar from min to max days per label."""
    y = range(len(labels))
    ax.barh(y, [mx - mn + 0.4 for mn, mx in zip(mins, maxs)], left=mins, color=colors or "#1b5e8a", height=0.6)
    ax.set_yticks(list(y))
    ax.set_yticklabels(labels, fontsize=8)
    ax.invert_yaxis()
    ax.set_xlim(left=0)
    ax.set_xlabel("Turnaround (days; bar spans min to max, drawn 0.4 wider so single values are visible)")
    ax.grid(axis="x", alpha=0.3)


def main():
    df = pd.read_csv(ASSAY_DIR / "assays-instrument-turnaround.csv", dtype={"min_sample_size": str})
    df["category"] = df["category"].fillna("(none)")
    df["mid_days"] = (df["turnaround_min_days"] + df["turnaround_max_days"]) / 2

    # 1. Distribution of the longest turnaround, colored by in-house guess
    fig, ax = plt.subplots(figsize=(9, 5))
    counts = df.groupby(["turnaround_max_days", "in_house_guess"]).size().unstack(fill_value=0)
    counts = counts.reindex(columns=BAND_ORDER, fill_value=0)
    counts.plot.bar(stacked=True, ax=ax, color=[BAND_COLORS[b] for b in BAND_ORDER], width=0.85)
    ax.set_xlabel("Longest quoted turnaround (days)")
    ax.set_ylabel("Number of assays")
    ax.set_title(f"How long do assays take?\n{NOTE}", fontsize=10)
    ax.legend(title="In-house guess")
    save(fig, "01-turnaround-distribution.png")

    # 2. Slowest 30 assays
    top = df.sort_values(["turnaround_max_days", "turnaround_min_days", "assay"], ascending=[False, False, True]).head(30)
    fig, ax = plt.subplots(figsize=(10, 8))
    range_bars(ax, [a[:55] for a in top["assay"]], top["turnaround_min_days"], top["turnaround_max_days"],
               [BAND_COLORS[b] for b in top["in_house_guess"]])
    ax.set_title("30 slowest assays by longest quoted turnaround", fontsize=11)
    save(fig, "02-slowest-assays.png")

    # 3. Category summary: median min and max across assays
    cat = df.groupby("category").agg(assays=("assay", "size"), min_days=("turnaround_min_days", "median"),
                                     max_days=("turnaround_max_days", "median")).sort_values("max_days", ascending=False)
    fig, ax = plt.subplots(figsize=(10, 5))
    range_bars(ax, [f"{c} (n={n})" for c, n in zip(cat.index, cat["assays"])], cat["min_days"], cat["max_days"])
    ax.set_title(f"Median turnaround range by category\n{NOTE}", fontsize=10)
    save(fig, "03-turnaround-by-category.png")

    # 4. Instrument type summary: median min and max across assays
    inst = df.groupby("instrument_type").agg(assays=("assay", "size"), min_days=("turnaround_min_days", "median"),
                                             max_days=("turnaround_max_days", "median")).sort_values(
        ["max_days", "assays"], ascending=[False, False])
    fig, ax = plt.subplots(figsize=(10, 9))
    range_bars(ax, [f"{i} (n={n})" for i, n in zip(inst.index, inst["assays"])], inst["min_days"], inst["max_days"])
    ax.set_title(f"Median turnaround range by instrument type\n{NOTE}", fontsize=10)
    save(fig, "04-turnaround-by-instrument-type.png")

    # 5. In-house guess by instrument type (counts)
    by_inst = df.groupby(["instrument_type", "in_house_guess"]).size().unstack(fill_value=0)
    by_inst = by_inst.reindex(columns=BAND_ORDER, fill_value=0)
    by_inst = by_inst.loc[by_inst.sum(axis=1).sort_values().index]
    fig, ax = plt.subplots(figsize=(10, 9))
    by_inst.plot.barh(stacked=True, ax=ax, color=[BAND_COLORS[b] for b in BAND_ORDER])
    ax.set_xlabel("Number of assays")
    ax.set_ylabel("")
    ax.set_title("In-house guess by instrument type (a guess from turnaround time)", fontsize=10)
    ax.legend(title="In-house guess")
    save(fig, "05-in-house-guess-by-instrument-type.png")

    # 6. In-house guess by category (counts)
    by_cat = df.groupby(["category", "in_house_guess"]).size().unstack(fill_value=0)
    by_cat = by_cat.reindex(columns=BAND_ORDER, fill_value=0)
    by_cat = by_cat.loc[by_cat.sum(axis=1).sort_values().index]
    fig, ax = plt.subplots(figsize=(10, 4.5))
    by_cat.plot.barh(stacked=True, ax=ax, color=[BAND_COLORS[b] for b in BAND_ORDER])
    ax.set_xlabel("Number of assays")
    ax.set_ylabel("")
    ax.set_title("In-house guess by category (a guess from turnaround time)", fontsize=10)
    ax.legend(title="In-house guess")
    save(fig, "06-in-house-guess-by-category.png")

    print(df["in_house_guess"].value_counts().to_string())
    print(f"wrote {len(list(PLOT_DIR.glob('*.png')))} plots to {PLOT_DIR}")


if __name__ == "__main__":
    main()
