"""Style-guide test round 2: polar/radar + conditioned table."""

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

from plot_style import ACCENT, CASING, GRAY, GREEN, MONO, RED, TITLE_FONT, bottom_block, title

TMP = Path(__file__).parent
OUTDIR = Path("/Users/rahimhashim/Projects/metapod/reports/kobe")

rows = json.loads((TMP / "kobe_pergame.json").read_text())
by_season = {r["Season"]: r for r in rows}

# ---------------------------------------------------------------- radar
CATS = [("PTS", "PTS"), ("TRB", "REB"), ("AST", "AST"), ("STL", "STL"), ("FG%", "FG%")]
ERAS = [("1996-97", "Rookie", "#b0b7c0"),
        ("2015-16", "Farewell", "#5a6572"),
        ("2005-06", "Peak", ACCENT)]

cat_max = {c: max(float(r[c]) for r in rows) for c, _ in CATS}
angles = np.linspace(0, 2 * np.pi, len(CATS), endpoint=False)

fig, ax = plt.subplots(figsize=(7.4, 6.6), subplot_kw=dict(polar=True))
ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)
ax.grid(color="#e8e8e8", linewidth=0.6)
ax.spines["polar"].set_visible(False)
ax.set_ylim(0, 1.02)
ax.set_yticks([0.25, 0.5, 0.75, 1.0])
ax.set_yticklabels([])
ax.set_xticks(angles)
ax.set_xticklabels([lbl for _, lbl in CATS])
for t in ax.get_xticklabels():
    t.set_fontfamily(MONO)
    t.set_color("#555555")
    t.set_fontsize(10)
ax.tick_params(axis="x", pad=14)

for season, label, color in ERAS:
    r = by_season[season]
    vals = [float(r[c]) / cat_max[c] for c, _ in CATS]
    th = np.concatenate([angles, angles[:1]])
    vv = np.array(vals + vals[:1])
    is_peak = label == "Peak"
    ax.plot(th, vv, color=color, linewidth=3.0 if is_peak else 2.2, zorder=5 if is_peak else 3)
    ax.fill(th, vv, color=color, alpha=0.16 if is_peak else 0.08, zorder=2)

# peak-season values just inside each vertex
peak = by_season["2005-06"]
for ang, (c, lbl) in zip(angles, CATS):
    ax.text(ang, float(peak[c]) / cat_max[c] - 0.11, f"{peak[c]}", ha="center",
            va="center", fontsize=9, fontfamily=MONO, color=ACCENT, fontweight="bold",
            path_effects=CASING)

# direct series labels, axes coords (stable regardless of polar geometry)
for label, color, xy in [("Peak  2005–06", ACCENT, (0.76, 0.90)),
                         ("Farewell  2015–16", "#5a6572", (0.68, 0.13)),
                         ("Rookie  1996–97", "#9aa1aa", (0.30, 0.55))]:
    ax.text(*xy, label, fontsize=10, color=color, fontweight="bold",
            ha="left", transform=ax.transAxes, path_effects=CASING)

title(ax, "Even in decline, late Kobe out-produced his rookie year\neverywhere except shooting efficiency")
bottom_block(fig,
             "Source: Basketball-Reference · per-game table, bryanko01",
             "Per-game means by season · each axis scaled to Kobe's career-best season in that category · "
             "blue values = 2005-06 · no game-level variance at this aggregation")

fig.savefig(OUTDIR / "kobe_radar.svg")
fig.savefig(OUTDIR / "kobe_radar.png")
plt.close(fig)

# ---------------------------------------------------------------- conditioned table
FS = 11            # cell font size — fills the row
HFS = 9.5          # header font size
CHAR_W = FS * 0.6 / 72   # IBM Plex Mono advance is 0.6 em → exact char width in inches
PITCH = FS * 1.75 / 72   # row pitch in inches
GAP = 3                  # inter-column gap, chars

# darker shades for text sitting on its own tint
GREEN_TXT = "#357c17"
RED_TXT = "#b84632"


def delta_txt(d, dec):
    v = f"{abs(d):.{dec}f}"
    if dec == 3:
        v = v.lstrip("0")
    return f"{'▲' if d > 0 else '▼'} {v}"


tbl, prev = [], None
for r in rows:
    d_pts = None if prev is None else float(r["PTS"]) - float(prev["PTS"])
    d_fg = None if prev is None else float(r["FG%"]) - float(prev["FG%"])
    tbl.append({
        "SEASON": r["Season"].replace("-", "–"),
        "AGE": f"{int(r['Age'])}", "G": f"{int(r['G'])}",
        "MPG": f"{float(r['MP']):.1f}", "PPG": f"{float(r['PTS']):.1f}",
        "ΔPPG": "" if d_pts is None else delta_txt(d_pts, 1),
        "FG%": f"{float(r['FG%']):.3f}".lstrip("0"),
        "ΔFG%": "" if d_fg is None else delta_txt(d_fg, 3),
        "_season": r["Season"], "_dpts": d_pts, "_dfg": d_fg,
    })
    prev = r

COLS = ["SEASON", "AGE", "G", "MPG", "PPG", "ΔPPG", "FG%", "ΔFG%"]
w = {c: max(len(c), max(len(t[c]) for t in tbl)) for c in COLS}  # content-driven widths
x_left, x_right, cur = {}, {}, 0
for c in COLS:
    x_left[c], x_right[c] = cur, cur + w[c]
    cur = x_right[c] + GAP
total = cur - GAP

n = len(tbl)
fig, ax = plt.subplots(figsize=(total * CHAR_W + 0.5, n * PITCH + 1.7))
ax.set_axis_off()
ax.set_xlim(-0.5, total + 0.5)
ax.set_ylim(-0.25, n + 1.45)


def put(c, y, txt, **kw):
    ha = "left" if c == "SEASON" else "right"
    x = x_left[c] if c == "SEASON" else x_right[c]
    ax.text(x, y, txt, ha=ha, va="center", fontfamily=MONO, **kw)


hy = n + 1
for c in COLS:
    put(c, hy, c, fontsize=HFS, color="#999999")
ax.plot([-0.5, total + 0.5], [n + 0.55] * 2, color="#cccccc", linewidth=0.8)

dmax_p = max(abs(t["_dpts"]) for t in tbl if t["_dpts"] is not None)
dmax_f = max(abs(t["_dfg"]) for t in tbl if t["_dfg"] is not None)
worst_seasons = {r["Season"] for r in sorted(rows, key=lambda r: float(r["FG%"]))[:2]}
EXT = {}
for c, key in [("G", "G"), ("MPG", "MP"), ("PPG", "PTS"), ("FG%", "FG%")]:
    vals = [float(r[key]) for r in rows]
    EXT[c] = (max(vals), min(vals))

for i, t in enumerate(tbl):
    y = n - i - 0.5
    if t["_season"] == "2005-06":
        ax.add_patch(Rectangle((-0.5, y - 0.5), total + 1, 1,
                               color=ACCENT, alpha=0.08, lw=0, zorder=0))
    # Δ cells: full-cell tint, intensity scaled to |Δ| within the column
    for c, d, dmax in [("ΔPPG", t["_dpts"], dmax_p), ("ΔFG%", t["_dfg"], dmax_f)]:
        if d is None:
            continue
        fill = GREEN if d > 0 else RED
        alpha = 0.10 + 0.25 * abs(d) / dmax
        ax.add_patch(Rectangle((x_left[c] - 1.2, y - 0.5), w[c] + 2.4, 1,
                               color=fill, alpha=alpha, lw=0, zorder=0))
        txt_color = GREEN_TXT if d > 0 else RED_TXT
        ax.text(x_left[c] + 0.5, y, "▲" if d > 0 else "▼", ha="center", va="center",
                fontsize=FS - 2.5, color=txt_color, fontfamily=MONO)
        ax.text(x_right[c], y, t[c].split(" ")[1], ha="right", va="center",
                fontsize=FS, color=txt_color, fontfamily=MONO)
    for c in ["SEASON", "AGE", "G", "MPG", "PPG", "FG%"]:
        color, weight = "#1a1a1a", "normal"
        if c == "SEASON":
            weight = "bold"
        if c in EXT:
            v = float(t[c] if not t[c].startswith(".") else "0" + t[c])
            hi, lo = EXT[c]
            if v in (hi, lo):
                weight = "bold"
                ax.add_patch(Rectangle((x_left[c] - 1.2, y - 0.5), w[c] + 2.4, 1,
                                       color=GREEN if v == hi else RED,
                                       alpha=0.12, lw=0, zorder=0))
        if c == "FG%" and t["_season"] in worst_seasons:
            color, weight = RED, "bold"
        put(c, y, t[c], fontsize=FS, color=color, fontweight=weight)
    if i < n - 1:
        ax.plot([-0.5, total + 0.5], [n - i - 1] * 2, color="white",
                linewidth=1.2, zorder=1)

ax.set_title("Kobe's two worst shooting seasons were his last two",
             fontfamily=TITLE_FONT, pad=10)
bottom_block(fig,
             "Source: Basketball-Reference · per-game table, bryanko01",
             "Per-game means by season · Δ vs prior season, tint scaled to size of change · "
             "career highs tinted green, lows red · 2013–14 was a 6-game season")

fig.savefig(OUTDIR / "kobe_table.svg")
fig.savefig(OUTDIR / "kobe_table.png")
plt.close(fig)
print("saved radar + table")
