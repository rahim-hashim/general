"""Reference renders for plotting/STYLE.md.

Self-contained on purpose: every recipe STYLE.md quotes lives here and is
exercised by `python make_examples.py`, which also runs the text-overlap
check and fails loudly if any text collides or leaves the canvas.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.font_manager as fm
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm, to_rgb
from matplotlib.patches import Rectangle

fm._load_fontmanager(try_read_cache=False)

OUT = Path(__file__).parent

# ---------------------------------------------------------------- tokens
INK = "#1a1a1a"
MUTED = "#6b6b6b"
FAINT = "#b8b8b8"
GRID = "#e6e6e6"
ZEBRA = "#f5f5f3"
BG = "#ffffff"
ACCENT = "#2166ac"
POS = "#4dac26"
NEG = "#d6604d"

TITLE_FONT = ["Playfair Display", "DejaVu Serif"]
PROSE_FONT = ["EB Garamond", "DejaVu Serif"]
MONO_FONT = ["IBM Plex Mono", "Menlo", "DejaVu Sans Mono"]

CASING = [pe.withStroke(linewidth=3, foreground=BG)]

# Spacing scale in points; every gap in a figure is one of these.
SP = {"xs": 2, "s": 4, "m": 8, "l": 12, "xl": 18, "xxl": 28}

plt.rcParams.update({
    "figure.facecolor": BG,
    "axes.facecolor": BG,
    "axes.edgecolor": INK,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "axes.grid.axis": "y",
    "grid.color": GRID,
    "grid.linewidth": 0.8,
    "axes.axisbelow": True,
    "font.family": MONO_FONT,
    "font.size": 9,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "xtick.labelsize": 8.5,
    "ytick.labelsize": 8.5,
    "axes.labelcolor": MUTED,
    "axes.labelsize": 8.5,
    "legend.frameon": False,
    "savefig.dpi": 200,
})


# ---------------------------------------------------------------- frame
def title(fig, text, y=0.975):
    """Left-aligned, insight-stating title. No subtitle underneath."""
    fig.text(0.04, y, text, ha="left", va="top", fontsize=15,
             family=TITLE_FONT, weight="bold", color=INK)


def bottom_block(fig, source, description, notes=None, y=0.02):
    """Source line, then descriptive line, then optional notes; bottom-left."""
    lines = [source, description] + ([notes] if notes else [])
    for i, line in enumerate(reversed(lines)):
        fig.text(0.04, y + i * 0.028, line, ha="left", va="bottom",
                 fontsize=8.5, family=PROSE_FONT, color=MUTED)


def axis_label(ax, x=None, y=None):
    """Mono, uppercase, every axis, always."""
    if x:
        ax.set_xlabel(x.upper(), family=MONO_FONT, labelpad=SP["m"])
    if y:
        ax.set_ylabel(y.upper(), family=MONO_FONT, labelpad=SP["m"])


def key_dot(ax, x, y, label, color=ACCENT, dx=SP["m"], dy=SP["m"]):
    """Halo dot + bold mono value for the one datapoint the title is about."""
    ax.scatter([x], [y], s=160, color=color, alpha=0.18, lw=0, zorder=5)
    ax.scatter([x], [y], s=34, color=color, lw=1.2, edgecolor=BG, zorder=6)
    ax.annotate(label, (x, y), xytext=(dx, dy), textcoords="offset points",
                family=MONO_FONT, weight="bold", fontsize=9, color=color,
                path_effects=CASING, zorder=7)


def direct_labels(ax, ends, min_gap_pt=11, x_pad_pt=SP["m"]):
    """Label line ends in the right margin without collisions.

    ends: list of (y_data, text, color). Labels are sorted by y and pushed
    apart until neighbours are at least `min_gap_pt` apart (≈ 1.2 × font
    size); a thin leader joins each label to its true endpoint when it moved.
    """
    ax.figure.canvas.draw()
    x_end = ax.get_xlim()[1]
    pt_per_px = 72 / ax.figure.dpi
    # Work in points relative to the axes bottom so offsets are exact.
    y0_px = ax.transAxes.transform((0, 0))[1]
    top_pt = (ax.transAxes.transform((0, 1))[1] - y0_px) * pt_per_px
    true = sorted(((ax.transData.transform((x_end, y))[1] - y0_px) * pt_per_px, t, c, y)
                  for y, t, c in ends)
    placed = []
    for y_pt, *_ in true:
        placed.append(max(y_pt, placed[-1] + min_gap_pt) if placed else y_pt)
    overflow = placed[-1] - top_pt
    if overflow > 0:  # stack ran off the top: slide it all down
        placed = [p - overflow for p in placed]
    for (y_pt, t, c, y), lab_pt in zip(true, placed):
        dy = lab_pt - y_pt
        ax.annotate(t, xy=(x_end, y), xytext=(x_pad_pt, dy),
                    textcoords="offset points", va="center", ha="left",
                    fontsize=9, family=MONO_FONT, color=c, weight="bold",
                    annotation_clip=False, path_effects=CASING,
                    arrowprops=None if abs(dy) < 0.5 else
                    dict(arrowstyle="-", color=c, lw=0.6, shrinkA=0, shrinkB=2))


# ---------------------------------------------------------------- overlap check
def check_text_overlap(fig, pad_px=1.0):
    """Return a list of problems: text/text collisions, text off-canvas.

    Checked on the rendered figure, not the code. Run before every save.
    """
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    texts = [t for t in fig.findobj(matplotlib.text.Text)
             if t.get_visible() and t.get_text().strip()]
    boxes = [(t, t.get_window_extent(r)) for t in texts]
    W, H = fig.canvas.get_width_height()
    problems = []
    for t, b in boxes:
        if b.x0 < 0 or b.y0 < 0 or b.x1 > W or b.y1 > H:
            problems.append(f"off-canvas: {t.get_text()!r}")
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            a, b = boxes[i][1], boxes[j][1]
            if (a.x0 < b.x1 - pad_px and b.x0 < a.x1 - pad_px
                    and a.y0 < b.y1 - pad_px and b.y0 < a.y1 - pad_px):
                problems.append(f"overlap: {boxes[i][0].get_text()!r} × {boxes[j][0].get_text()!r}")
    return problems


def save(fig, stem):
    problems = check_text_overlap(fig)
    if problems:
        raise SystemExit(f"{stem}: " + "; ".join(problems))
    for ext in ("png", "svg"):
        fig.savefig(OUT / f"{stem}.{ext}")
    plt.close(fig)
    print(f"{stem}: ok")


# ---------------------------------------------------------------- table
def _luminance(rgb):
    r, g, b = rgb
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def draw_table(ax, rows, columns, groups, delta_key, fmt, label_key="name",
               row_h=1.0, label_w=3.2, col_w=1.25):
    """Grouped table with heavy group rules and one conditioned Δ column.

    rows: list of dicts. columns: list of (key, header). groups: list of
    (header or None, [keys]) in column order; a heavy vertical rule separates
    adjacent groups. delta_key: signed column filled on a diverging
    green/red scale centred at 0, with ▲/▼ glyphs so sign survives greyscale.
    """
    n = len(rows)
    keys = [k for k, _ in columns]
    headers = dict(columns)
    x = {}
    cursor = label_w
    for _, ks in groups:
        for k in ks:
            x[k] = cursor
            cursor += col_w
    width = cursor
    ax.set_xlim(0, width)
    ax.set_ylim(n * row_h, -2.2 * row_h)
    ax.axis("off")

    vals = np.array([r[delta_key] for r in rows], dtype=float)
    lim = np.nanmax(np.abs(vals))
    cmap = LinearSegmentedColormap.from_list("div", [NEG, "#f7f7f7", POS])
    norm = TwoSlopeNorm(vmin=-lim, vcenter=0, vmax=lim)

    for i, row in enumerate(rows):
        y0 = i * row_h
        if i % 2:
            ax.add_patch(Rectangle((0, y0), width, row_h, color=ZEBRA, lw=0, zorder=0))
        ax.text(0.15, y0 + row_h / 2, row[label_key], va="center", ha="left",
                family=PROSE_FONT, weight="semibold", fontsize=10.5, color=INK)
        for k in keys:
            v = row[k]
            color = INK
            if k == delta_key:
                fill = cmap(norm(v))
                ax.add_patch(Rectangle((x[k], y0), col_w, row_h, color=fill, lw=0, zorder=1))
                color = BG if _luminance(to_rgb(fill)) < 0.55 else INK
                glyph = "▲" if v > 0 else "▼" if v < 0 else " "
                text = f"{glyph} {fmt[k](v)}"
            else:
                text = fmt[k](v)
            ax.text(x[k] + col_w - 0.18, y0 + row_h / 2, text, va="center",
                    ha="right", family=MONO_FONT, fontsize=9.5, color=color, zorder=2)

    # Column headers + spanners.
    for k in keys:
        ax.text(x[k] + col_w - 0.18, -0.45 * row_h, headers[k].upper(), ha="right",
                va="bottom", family=MONO_FONT, fontsize=8.5, weight="bold", color=INK)
    for head, ks in groups:
        if head:
            x0, x1 = x[ks[0]] + 0.12, x[ks[-1]] + col_w - 0.12
            ax.plot([x0, x1], [-1.35 * row_h] * 2, color=INK, lw=0.8)
            ax.text((x0 + x1) / 2, -1.5 * row_h, head, ha="center", va="bottom",
                    family=PROSE_FONT, fontsize=10.5, weight="semibold", color=INK)

    # Rules: heavy under header, heavy between groups, light closing rule.
    ax.plot([0, width], [0, 0], color=INK, lw=1.8, solid_capstyle="butt")
    for _, ks in groups[1:]:
        ax.plot([x[ks[0]]] * 2, [0, n * row_h], color=INK, lw=1.4)
    ax.plot([label_w] * 2, [0, n * row_h], color=INK, lw=1.4)
    ax.plot([0, width], [n * row_h] * 2, color=FAINT, lw=0.8)


def example_table():
    # Recreated from source/datakabas_tennis_table.jpg (subset) as a style
    # reference; values transcribed from that image.
    data = [
        ("Ben Shelton", 41, 16, 71.9, 110, 75, 59.5),
        ("Karen Khachanov", 83, 41, 66.9, 251, 203, 55.3),
        ("Stan Wawrinka", 182, 87, 67.7, 409, 309, 57.0),
        ("Carlos Alcaraz", 95, 13, 88.0, 209, 56, 78.9),
        ("Novak Djokovic", 442, 67, 86.8, 745, 176, 80.9),
        ("Jannik Sinner", 100, 22, 82.0, 270, 72, 78.9),
        ("Casper Ruud", 57, 31, 64.8, 260, 142, 64.7),
        ("Cameron Norrie", 47, 37, 56.0, 217, 165, 56.8),
        ("Hubert Hurkacz", 42, 35, 54.5, 202, 134, 60.1),
        ("Ugo Humbert", 22, 30, 42.3, 170, 138, 55.2),
    ]
    rows = [dict(name=n, w5=a, l5=b, p5=c, w3=d, l3=e, p3=f, diff=round(c - f, 1))
            for n, a, b, c, d, e, f in data]
    columns = [("w5", "W"), ("l5", "L"), ("p5", "Win %"),
               ("w3", "W"), ("l3", "L"), ("p3", "Win %"), ("diff", "Δ pts")]
    groups = [("Best of 5", ["w5", "l5", "p5"]),
              ("Best of 3", ["w3", "l3", "p3"]),
              (None, ["diff"])]
    integer = "{:d}".format
    pct = "{:.1f}".format
    fmt = dict(w5=integer, l5=integer, p5=pct, w3=integer, l3=integer, p3=pct,
               diff=lambda v: f"{v:+.1f}".replace("-", "\u2212"))

    fig = plt.figure(figsize=(8.4, 6.0))
    title(fig, "Shelton gains 12.4 pts in best-of-five; Humbert loses 12.9")
    ax = fig.add_axes([0.04, 0.18, 0.92, 0.72])
    draw_table(ax, rows, columns, groups, "diff", fmt, col_w=1.0)
    bottom_block(
        fig,
        "Source: Tennis Abstract, via Lev Akabas (reference recreation, 10 of 26 rows)",
        "Career Grand Slam (best-of-5) vs tour (best-of-3) match win rate, active players",
        notes="Δ = Bo5 win % − Bo3 win %; ▲▼ carry sign in greyscale. No uncertainty: counts are complete records.",
    )
    save(fig, "table_grouped_delta")


# ---------------------------------------------------------------- line chart
def example_lines():
    rng = np.random.default_rng(7)
    t = np.arange(0, 60)
    series = {
        "Condition A": (0.35 + 0.45 * (1 - np.exp(-t / 14)), ACCENT),
        "Condition B": (0.35 + 0.38 * (1 - np.exp(-t / 18)), "#7a7a7a"),
        "Condition C": (0.35 + 0.36 * (1 - np.exp(-t / 20)), "#a8a8a8"),
    }
    gap = series["Condition A"][0][-1] - series["Condition B"][0][-1]
    fig = plt.figure(figsize=(8, 5))
    title(fig, f"Condition A plateaus {gap:.2f} above B by trial {t[-1] + 1}")
    ax = fig.add_axes([0.1, 0.22, 0.7, 0.64])
    ends = []
    for name, (mu, c) in series.items():
        sd = 0.04 + 0.01 * rng.standard_normal(t.size).cumsum() / 20
        ax.fill_between(t, mu - np.abs(sd), mu + np.abs(sd), color=c, alpha=0.15, lw=0)
        ax.plot(t, mu, color=c, lw=2 if c == ACCENT else 1.3)
        ends.append((mu[-1], name, c))
    ax.set_xlim(0, t[-1])
    ax.set_ylim(0.3, 0.9)
    axis_label(ax, x="Trial", y="Accuracy")
    y20 = series["Condition A"][0][20]
    key_dot(ax, 20, y20, f"{y20:.2f}", dx=-SP["xl"], dy=SP["l"])
    direct_labels(ax, ends)
    ax.text(0.01, 0.97, "n = 12 sessions per condition", transform=ax.transAxes,
            ha="left", va="top", fontsize=8.5, color=MUTED, path_effects=CASING)
    bottom_block(fig, "Source: synthetic data for style demonstration",
                 "Mean accuracy by trial; bands ± 1 SEM across sessions")
    save(fig, "lines_direct_labels")


# ---------------------------------------------------------------- legend band
def legend_band(fig, ax, handles, labels, gap_pt=SP["l"]):
    """Legend in a reserved band above the axes, never over data.

    Starts with every entry on one row and drops columns until the legend
    fits inside the figure's side margins. Entries wrap whole: a label is
    never split across lines. Returns the legend so the caller can size the
    band (axes top) to it.
    """
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    left_px = fig.transFigure.transform((0.04, 0))[0]
    right_px = fig.transFigure.transform((0.96, 0))[0]
    for ncol in range(len(labels), 0, -1):
        leg = ax.legend(handles, labels, ncol=ncol, loc="lower left",
                        bbox_to_anchor=(0, 1), borderaxespad=0,
                        bbox_transform=ax.transAxes, handlelength=1.2,
                        handleheight=0.9, handletextpad=0.5,
                        columnspacing=1.6, labelspacing=0.6,
                        prop={"family": MONO_FONT, "size": 8.5})
        # Lift the legend by gap_pt above the axes.
        leg.set_bbox_to_anchor(
            (0, 1 + gap_pt * fig.dpi / 72 / ax.get_window_extent(r).height),
            transform=ax.transAxes)
        fig.canvas.draw()
        box = leg.get_window_extent(r)
        if box.x0 >= left_px - 1 and box.x1 <= right_px + 1:
            return leg
    return leg


def example_legend():
    rng = np.random.default_rng(3)
    years = np.arange(2014, 2026)
    names = ["Subsidies", "Import restrictions", "Localization and procurement",
             "Export promotion", "Export restrictions", "Other"]
    # One accent for the category the title is about; the rest muted.
    colors = ["#c9c9c9", "#b1b1b1", "#999999", ACCENT, "#818181", "#dcdcdc"]
    base = np.linspace(1, 3, years.size)
    vals = np.array([base * w * (1 + 0.1 * rng.standard_normal(years.size))
                     for w in (120, 70, 50, 30, 40, 10)])
    fig = plt.figure(figsize=(8, 5.4))
    title(fig, f"Export promotion measures rose {vals[3, -1] / vals[3, 0]:.1f}× since 2014")
    ax = fig.add_axes([0.1, 0.2, 0.86, 0.55])
    bottom = np.zeros(years.size)
    handles = []
    for v, c in zip(vals, colors):
        handles.append(ax.bar(years, v, bottom=bottom, color=c, width=0.72, lw=0))
        bottom += v
    axis_label(ax, x="Year", y="Measures announced")
    ax.set_xticks(years[::2])
    legend_band(fig, ax, handles, names)
    bottom_block(fig, "Source: synthetic data for style demonstration",
                 "Restrictive measures announced per year, stacked by category",
                 notes="Counts are complete tallies; no sampling uncertainty.")
    save(fig, "bars_legend_band")


if __name__ == "__main__":
    example_table()
    example_lines()
    example_legend()
