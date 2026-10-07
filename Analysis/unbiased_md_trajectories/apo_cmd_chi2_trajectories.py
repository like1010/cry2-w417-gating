#!/usr/bin/env python3
"""Generate the Figure 1A-C apo cMD chi2 trajectory panels.

Panels 1-4 are the 100 ns, 500 ns (stable), 500 ns (rare transition) and 1 us
apo conventional-MD trajectories of the W417 chi2 dihedral; panel 5 is the
zoomed view of the rare transition. Figure 1A-C of the manuscript uses panels
2, 3 and 4; panels 1 and 5 appear as Figure S2A-B.
"""

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

script_dir = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--input-dir", type=Path, default=script_dir / "data",
                    help="Directory containing the four chi2 .xvg files")
parser.add_argument("--output-dir", type=Path, default=script_dir / "results",
                    help="Directory for the five output PNG files")
args = parser.parse_args()

base = args.input_dir.resolve()
out_dir = args.output_dir.resolve()
out_dir.mkdir(parents=True, exist_ok=True)

files = [
    base / "chi2_W417_mda_100ns.xvg",
    base / "chi2_W417_500ns_mda.xvg",
    base / "chi2_mda_apo_chi2_res417_500ns.xvg",
    base / "chi2_W417_mda_1us.xvg",
]
out_files = [
    out_dir / "Fig1a_panel1_100ns_fixed.png",
    out_dir / "Fig1a_panel2_500ns_run1_fixed.png",
    out_dir / "Fig1a_panel3_500ns_rare_fixed.png",
    out_dir / "Fig1a_panel4_1us_fixed.png",
    out_dir / "Fig1a_panel5_rare_zoom_fixed.png",
]

def load_xvg(path):
    return pd.read_csv(path, comment="#", sep=r"\s+", header=None, names=["time_ps", "chi2_deg"])

def smooth_series(y, window=151):
    s = pd.Series(y)
    return s.rolling(window=window, center=True, min_periods=1).mean().to_numpy()

dfs = [load_xvg(f) for f in files]
scatter_neutral = "#A9C7E8"
line_neutral = "#145DA0"
highlight_fill = "#E8B0AA"
highlight_red = "#C53A32"
guide_gray = "#4A4A4A"

rare_df = dfs[2].copy()
rare_time_ns = rare_df["time_ps"] / 1000.0
chi2 = rare_df["chi2_deg"].to_numpy()
pos_idx = np.where(chi2 > 0)[0]
first_pos_ns = float(rare_time_ns.iloc[pos_idx[0]]) if len(pos_idx) else None
bins = np.linspace(-180, 180, 120)

def make_panel(df, outfile, rare=False, zoom=None):
    fig = plt.figure(figsize=(6.8, 3.2), constrained_layout=True)
    gs = fig.add_gridspec(1, 2, width_ratios=[5.5, 1.3])
    ax = fig.add_subplot(gs[0, 0])
    axd = fig.add_subplot(gs[0, 1], sharey=ax)

    t_ns = df["time_ps"] / 1000.0
    y = df["chi2_deg"].to_numpy()
    if zoom is not None:
        mask = (t_ns >= zoom[0]) & (t_ns <= zoom[1])
        t_ns = t_ns[mask]
        y = y[mask]

    y_sm = smooth_series(y, window=151 if len(y) > 5000 else 51)

    ax.axhspan(-180, 0, alpha=0.03, color=line_neutral)
    ax.axhspan(0, 180, alpha=0.02, color=highlight_red)
    ax.axhline(0, linestyle="--", linewidth=0.8, color=guide_gray)

    if rare and first_pos_ns is not None:
        pre = t_ns <= first_pos_ns
        post = t_ns > first_pos_ns
        ax.scatter(t_ns[pre], y[pre], s=4, color=scatter_neutral, alpha=0.35, linewidths=0)
        ax.scatter(t_ns[post], y[post], s=4, color=highlight_fill, alpha=0.35, linewidths=0)
        ax.plot(t_ns[pre], y_sm[pre], color=line_neutral, linewidth=2.0)
        ax.plot(t_ns[post], y_sm[post], color=highlight_red, linewidth=2.0)
        ax.axvline(first_pos_ns, linestyle=":", linewidth=1.0, color=guide_gray)

        neg = y[y < 0]
        pos = y[y > 0]
        if len(neg) > 0:
            hist_n, edges = np.histogram(neg, bins=bins, density=True)
            centers = 0.5 * (edges[:-1] + edges[1:])
            axd.fill_betweenx(centers, 0, hist_n, color=scatter_neutral, alpha=0.45)
            axd.plot(hist_n, centers, color=line_neutral, linewidth=2.0)
        if len(pos) > 0:
            hist_p, edges = np.histogram(pos, bins=bins, density=True)
            centers = 0.5 * (edges[:-1] + edges[1:])
            axd.fill_betweenx(centers, 0, hist_p, color=highlight_fill, alpha=0.55)
            axd.plot(hist_p, centers, color=highlight_red, linewidth=2.0)
    else:
        ax.scatter(t_ns, y, s=4, color=scatter_neutral, alpha=0.35, linewidths=0)
        ax.plot(t_ns, y_sm, color=line_neutral, linewidth=2.0)

        hist, edges = np.histogram(y, bins=bins, density=True)
        centers = 0.5 * (edges[:-1] + edges[1:])
        axd.fill_betweenx(centers, 0, hist, color=scatter_neutral, alpha=0.45)
        axd.plot(hist, centers, color=line_neutral, linewidth=2.0)

    if zoom is not None:
        ax.set_xlim(*zoom)
    ax.set_ylim(-180, 180)
    ax.set_xlabel("Time (ns)")
    ax.set_ylabel("χ₂ Angle (deg)")
    axd.axhline(0, linestyle="--", linewidth=0.8, color=guide_gray)
    axd.set_xlim(left=0)
    axd.set_xlabel("Density")
    axd.tick_params(axis="y", labelleft=False)

    plt.savefig(outfile, dpi=600, bbox_inches="tight")
    plt.close(fig)

make_panel(dfs[0], out_files[0], rare=False)
make_panel(dfs[1], out_files[1], rare=False)
make_panel(dfs[2], out_files[2], rare=True)
make_panel(dfs[3], out_files[3], rare=False)
make_panel(dfs[2], out_files[4], rare=True, zoom=(360, 500))

print("\n".join(str(p) for p in out_files))
