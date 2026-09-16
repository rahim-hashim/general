"""Style-guide test: Kobe Bryant career scoring, Basketball-Reference game logs."""

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from plot_style import ACCENT, CASING, GRAY, MONO, bottom_block, key_dot, mono_ticks, title

TMP = Path(__file__).parent
OUTDIR = Path("/Users/rahimhashim/Projects/metapod/reports/kobe")
OUTDIR.mkdir(parents=True, exist_ok=True)

raw = json.loads((TMP / "kobe_gamelogs.json").read_text())
# each scraped table carries one season-total row; no real game exceeds 81 points
data = {k: {"points": [p for p in v["points"] if p <= 100]} for k, v in raw.items()}
seasons = sorted(int(k) for k in data)
mean = np.array([np.mean(data[str(y)]["points"]) for y in seasons])
std = np.array([np.std(data[str(y)]["points"], ddof=1) for y in seasons])


def season_label(end_year):
    return f"{end_year - 1}–{str(end_year)[2:]}"


# ---------------------------------------------------------------- figure 1
fig, ax = plt.subplots(figsize=(9, 5.4))

ax.fill_between(seasons, mean - std, mean + std, color=ACCENT, alpha=0.15, linewidth=0)
ax.plot(seasons, mean, color=ACCENT)

peak_i = int(np.argmax(mean))
peak_year, peak_val = seasons[peak_i], mean[peak_i]
key_dot(ax, peak_year, peak_val)
ax.annotate(f"{peak_val:.1f}", (peak_year, peak_val), xytext=(0, 14),
            textcoords="offset points", ha="center",
            fontsize=12, fontweight="bold", color=ACCENT, fontfamily=MONO,
            path_effects=CASING)

key_dot(ax, seasons[-1], mean[-1], s=45)
ax.annotate(f"{mean[-1]:.1f}", (seasons[-1], mean[-1]), xytext=(10, 0),
            textcoords="offset points", va="center", fontsize=10, color=ACCENT,
            fontfamily=MONO, path_effects=CASING)

y_top = float(np.ceil((mean + std).max())) + 2
ax.set_ylim(0, y_top)
ticks = [1997, 2000, 2003, 2006, 2009, 2012, 2015]
ax.set_xticks(ticks)
ax.set_xticklabels([season_label(t) for t in ticks])
ax.set_xlim(1996.4, 2017.6)

for yr, label, y in [(2004.55, "Shaq traded", 8),
                     (2013.3, "Achilles tear", y_top - 1.5)]:
    ax.axvline(yr, color=GRAY, linewidth=0.8, linestyle=(0, (4, 3)), zorder=1)
    ax.text(yr + 0.2, y, label, fontsize=9.5, color=GRAY, va="top",
            path_effects=CASING)
ax.text(2014.05, 12, "band widens: only\n6 games in 2013–14", fontsize=9,
        color=GRAY, va="top", ha="left", path_effects=CASING)

title(ax, "Kobe peaked at 35.4 points a game in 2005–06 —\nhis farewell season averaged half that")
ax.set_xlabel("SEASON", fontfamily=MONO)
ax.set_ylabel("POINTS PER GAME", fontfamily=MONO)
mono_ticks(ax)

bottom_block(fig,
             "Source: Basketball-Reference · game logs, bryanko01",
             "Points per game, regular season · shaded band = ±1σ across games played · 1996–97 to 2015–16")

fig.savefig(OUTDIR / "kobe_ppg_career.svg")
fig.savefig(OUTDIR / "kobe_ppg_career.png")
plt.close(fig)

# ---------------------------------------------------------------- figure 2
ERAS = [(1997, "Rookie"), (2003, "Three-peat era"), (2006, "Peak"), (2016, "Farewell")]
fig, ax = plt.subplots(figsize=(8, 5.4))

samples = [np.array(data[str(y)]["points"]) for y, _ in ERAS]
pos = np.arange(len(ERAS))

parts = ax.violinplot(samples, positions=pos, widths=0.72,
                      showextrema=False, showmedians=False)
for i, body in enumerate(parts["bodies"]):
    is_peak = ERAS[i][0] == 2006
    body.set_facecolor(ACCENT if is_peak else "#c6cdd6")
    body.set_alpha(0.55 if is_peak else 0.75)
    body.set_edgecolor("none")

for i, s in enumerate(samples):
    med = np.median(s)
    q1, q3 = np.percentile(s, [25, 75])
    ax.vlines(pos[i], q1, q3, color="#1a1a1a", linewidth=3, alpha=0.85)
    ax.scatter([pos[i]], [med], color="white", edgecolor="#1a1a1a",
               zorder=5, s=40, linewidth=1.4)
    ax.annotate(f"{med:.0f}", (pos[i], med), xytext=(12, 0),
                textcoords="offset points", va="center", fontsize=9.5,
                fontweight="bold", color="#1a1a1a", fontfamily=MONO,
                path_effects=CASING)

ax.set_xticks(pos)
ax.set_xticklabels([f"{season_label(y)}\n{lbl}\nn = {len(s)} games"
                    for (y, lbl), s in zip(ERAS, samples)], fontsize=9)
ax.set_ylim(-2, 85)

ax.annotate("81 vs. Toronto,\nJan 22, 2006", xy=(2, 81), xytext=(2.45, 76),
            fontsize=9.5, color=GRAY, va="center", path_effects=CASING,
            arrowprops=dict(arrowstyle="-", color=GRAY, linewidth=0.7))
key_dot(ax, 2, 81, s=36)
ax.annotate("60 in his\nfinal game", xy=(3, 60), xytext=(3.32, 62),
            fontsize=9.5, color=GRAY, va="center", path_effects=CASING,
            arrowprops=dict(arrowstyle="-", color=GRAY, linewidth=0.7))

q1_peak = np.percentile(data["2006"]["points"], 25)
title(ax, f"At his peak, a “bad night” for Kobe still meant {q1_peak:.0f} points")
ax.set_xlabel("SEASON", fontfamily=MONO)
ax.set_ylabel("POINTS SCORED IN A GAME", fontfamily=MONO)
mono_ticks(ax)

bottom_block(fig,
             "Source: Basketball-Reference · game logs, bryanko01",
             "Distribution of points per game, regular season · white dot = median, black bar = IQR")

fig.savefig(OUTDIR / "kobe_distributions.svg")
fig.savefig(OUTDIR / "kobe_distributions.png")
plt.close(fig)
print("saved figs 1-2")
