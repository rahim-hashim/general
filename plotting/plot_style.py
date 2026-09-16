"""Canonical plot style baseline — import this in any project. Spec: STYLE.md alongside."""

import matplotlib as mpl
import matplotlib.patheffects as pe

ACCENT = "#2166ac"
RED = "#d6604d"
GREEN = "#4dac26"
GRAY = "#878787"

TITLE_FONT = "Playfair Display"                       # titles only
MONO = ["IBM Plex Mono", "Menlo", "DejaVu Sans Mono"]  # numerals; list gives per-glyph fallback

mpl.rcParams.update({
    "font.family": "serif",
    "font.serif": ["EB Garamond", "Iowan Old Style", "Georgia", "DejaVu Serif"],
    "font.size": 11, "axes.titlesize": 16, "axes.titleweight": "bold",
    "axes.titlelocation": "left", "axes.titlepad": 16, "axes.labelsize": 10,
    "xtick.labelsize": 9.5, "ytick.labelsize": 9.5,
    "text.color": "#1a1a1a", "axes.labelcolor": "#555555",
    "xtick.color": "#1a1a1a", "ytick.color": "#1a1a1a",
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.edgecolor": "#cccccc", "axes.linewidth": 0.8,
    "axes.grid": True, "axes.grid.axis": "y", "axes.axisbelow": True,
    "grid.color": "#e8e8e8", "grid.linewidth": 0.6,
    "xtick.major.size": 0, "ytick.major.size": 0,
    "lines.linewidth": 3.0,
    "legend.frameon": False, "legend.fontsize": 10,
    "figure.constrained_layout.use": True,
    "figure.dpi": 150, "savefig.dpi": 200,
    "savefig.bbox": "tight", "savefig.pad_inches": 0.15,
    "axes.prop_cycle": mpl.cycler(color=[
        ACCENT, RED, GREEN, "#8073ac", "#f1a340", GRAY]),
})


def title(ax, text):
    ax.set_title(text, fontfamily=TITLE_FONT)


def mono_ticks(ax):
    for lbl in ax.get_xticklabels() + ax.get_yticklabels():
        lbl.set_fontfamily(MONO)


def bottom_block(fig, source, note):
    """Source + descriptive note, bottom-left. The note auto-wraps to the figure
    width so long captions never stretch the canvas wider than the plot."""
    import textwrap
    budget = max(30, int((fig.get_size_inches()[0] - 0.35) / (8.5 * 0.6 / 72)))
    note = "\n".join(textwrap.wrap(note, budget, break_long_words=False))
    fig.text(0.01, -0.025, source, fontsize=8.5, color="#999999",
             ha="left", va="top", fontfamily=MONO)
    fig.text(0.01, -0.055, note, fontsize=8.5, color="#999999",
             ha="left", va="top", fontfamily=MONO, linespacing=1.5)


# white casing stroke — mandatory on every text element inside the axes,
# so labels read identically whether or not they cross a fill/band/line
CASING = [pe.withStroke(linewidth=3, foreground="white")]


def key_dot(ax, x, y, s=80, color=ACCENT):
    """Stylized key datapoint: soft halo + white-stroked accent dot."""
    ax.scatter([x], [y], s=s * 3.4, color=color, alpha=0.18, linewidth=0, zorder=4)
    ax.scatter([x], [y], s=s, color=color, edgecolor="white", linewidth=1.5, zorder=5)
