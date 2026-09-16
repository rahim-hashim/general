# Plot Style Guide — canonical spec

Applies to every project (metapod, second-brain, Neural-Geometry, and anything else).
The enforced summary lives in `~/.claude/CLAUDE.md`; **this file is the source of truth** —
when they disagree, this one wins and the summary should be updated.

- `plot_style.py` (this directory) — the importable baseline: rcParams, palette, fonts, helpers. Import it or copy it verbatim; never restyle from scratch.
- `examples/` — reference renders (Kobe Bryant test set) showing what correct output looks like, with their source scripts.

Reference aesthetic: FT (Burn-Murdoch) × NYT × Economist — restrained, high information-to-ink ratio, declarative titles, direct labels, uncertainty always visible.

## Library choice

| Need | Use |
|---|---|
| Static figure (Python) | matplotlib; seaborn on top for distributions, heatmaps, small multiples |
| Interactive chart, standalone (Python) | Plotly |
| Interactive chart in the metapod dashboard | Bokeh (established there) |
| Interactive timeline / custom layout (JS) | Vanilla JS + CSS per the second-brain `living_history` gravity pattern (`/Users/rahimhashim/Projects/second-brain/living_history/web/`); D3 only if the geometry demands it (force layouts, projections, trees) |

Never introduce Altair, Vega, Chart.js, vis.js, or timeline.js.
Export SVG/PDF; PNG only at ≥150 dpi (baseline saves at 200).

## Typography — three tiers

| Role | Font | How |
|---|---|---|
| Title | **Playfair Display**, bold, left-aligned | `title(ax, text)` helper / `axes.titlelocation: left` |
| On-figure prose (annotations, direct labels, legends) | **EB Garamond**, always upright — **never italic** | rcParams default |
| All numerals (ticks, axis labels, value callouts, n=, source/notes) | **IBM Plex Mono** via fallback list | `MONO` constant; axis labels UPPERCASE |

- The split that matters: **prose is serif, numbers are mono.** A value callout (`35.4`) is mono even when bold and colored. Mixed text-with-digits ("81 vs. Toronto, Jan 22, 2006") counts as prose.
- **No italics anywhere by default.**
- Always use `MONO` as a *list* (`["IBM Plex Mono", "Menlo", "DejaVu Sans Mono"]`): the Plex Mono static lacks `± σ Δ ▲ ▼`; the list enables per-glyph fallback. Verify special glyphs in the rendered PNG, not the code.
- Fonts are installed as static instances in `~/Library/Fonts` (PlayfairDisplay-Regular/Bold, EBGaramond-Regular/SemiBold/Italic, IBMPlexMono-Regular/Medium; plus Onest for web dashboards and retired Fraunces). Instanced from google/fonts OFL variables with fontTools. Fallbacks: Iowan Old Style/Georgia (serif), Inter/Helvetica Neue (sans), Menlo (mono).
- **After installing a font, force a matplotlib cache rebuild** — `fm._load_fontmanager(try_read_cache=False)` — a stale cache silently falls back to DejaVu.

## Color

- Palette (in `plot_style.py`): accent `#2166ac`, red `#d6604d`, green `#4dac26`, gray `#878787`.
- One vivid accent for the key series; everything else muted or gray. Never the default matplotlib cycle, never rainbow.
- Semantic: red = negative/down, green = positive/up, gray = baseline/comparison.
- Background white; warm off-white (`#FFF9F0`) acceptable for print-style pieces.

## Text on the figure

- **Title states the insight** ("Every governing party facing election this year lost vote share"), never the variable name. Numbers in titles come from the data, never hardcoded.
- **No subtitle under the title.** The descriptive line (measure, units, period, encoding notes like "shaded band = ±1σ") goes bottom-left **underneath the source line** — `bottom_block(fig, source, note)`.
- **Source line**: always, bottom-left, small gray mono — `Source: provider · provider2`.
- **Bottom notes never exceed the figure width** — `bottom_block` auto-wraps the note to the canvas; a caption wider than the plot stretches the saved image with dead whitespace.
- **Every axis gets a label — all plots, always.** Mono, uppercase, even when the unit seems obvious.
- **Casing — mandatory.** Every text element inside the axes gets a white casing stroke (`path_effects=CASING`) so it reads identically whether or not it crosses a fill, band, or line. Text never half-overlaps a shaded region uncased.
- **Direct-label series** at line ends when ≤5 series; a legend box only when direct labels would collide.
- Callout the single most important datum with a bold mono value and mark the point with `key_dot(ax, x, y)` (soft halo + white-stroked accent dot); thin leader line if needed; no boxed annotations.
- Event markers: vertical dashed gray line + short upright gray label. Position label text only after axis limits are final.

## Variance — mandatory

| Chart | Show |
|---|---|
| Time series | Shaded 95% CI or ±1σ band around the line |
| Bars | Error bars with caps (`capsize=3`) |
| Scatter | Error bars both axes when available |
| Distribution comparison | Violin (full shape); box + strip overlay if violins unreadable |
| Scientific panels | n= (cells and subjects) under the x-axis; p-value + effect size in-panel |

Every reported number carries its uncertainty (`mean ± std` or `median [IQR]`). If variance truly isn't available (single observation, pre-aggregated source), say so in the bottom notes line. If a band balloons from small n, annotate the cause on the figure ("band widens: only 6 games in 2013–14").

## Special chart types

- **Conditioned tables**: build as a figure (hidden axes + text grid), not `ax.table`. Rules, all shown in `examples/kobe_table.png` / `plot_kobe_extra.py`:
  - **Content-driven geometry.** All cell text is mono, so widths are exact: column width = max character count (header vs cells), positions accumulate with a 3-char gap, figure size derives from `chars × 0.6em` and `rows × 1.75em`. Never hand-pick column x-positions or figure size.
  - **Full-cell tint on signed columns** — the whole cell gets the green/red background, alpha scaled to the magnitude within the column (`0.10 + 0.25·|Δ|/|Δ|max`), like heat-mapped assessment tables. Delta text in darker green `#357c17` / red `#b84632` on top; hairline white row separators so the tint bands read as cells.
  - **Arrows get their own mini-column** inside the cell: `▲`/`▼` drawn as a separate text element, centered at a fixed x near the cell's left edge, ~2.5pt smaller than the numerals (optically centers the glyph); the number right-aligns at the cell edge. Never render `▲7.8` as one right-aligned string — the arrow drifts with number width.
  - **Primary-key column bold** (e.g. SEASON).
  - **Per-column extremes get a light highlight**: career high → green tint at ~12% alpha + bold; career low → red tint ~12% + bold. Quieter than the Δ columns; skip columns where extremes are meaningless (AGE).
  - Cell text 11pt filling a 1.75em row pitch; headers 9.5pt gray; title via `ax.set_title(..., pad=10)` — tables don't get the default (larger) title pad.
  - Tint the single most important row with the accent at ~8% alpha. Colored +/- applies anywhere a signed change is displayed.
  - Rows span `[0, n]` in y — set the bottom y-limit **below** 0 (e.g. −0.25) or the last row clips.
- **Polar/radar**: category labels via `set_xticks(angles)` + mono tick labels — never leave default degree labels; one accent series, others muted grays; series labels placed in axes coords, not polar coords; note the radial normalization in the bottom block. Example: `examples/kobe_radar.png`.

## Layout

- Small multiples share y-scale by default; independent scales only when justified and labeled.
- Labels never overlap each other, the axes, or the data. `constrained_layout` is the layout engine — never also call `tight_layout()`.
- **Render the figure and look at it before shipping.** The checklist is checked against the PNG, not the code.

## Plotly baseline

```python
layout = dict(
    plot_bgcolor="#ffffff", paper_bgcolor="#ffffff",
    font=dict(family="Onest, Inter, Helvetica Neue, Arial, sans-serif", size=12, color="#1a1a1a"),
    xaxis=dict(showgrid=False, zeroline=False, showline=True, linecolor="#cccccc"),
    yaxis=dict(showgrid=True, gridcolor="#e8e8e8", zeroline=False, showline=False),
    legend=dict(bgcolor="rgba(0,0,0,0)", borderwidth=0),
    margin=dict(l=48, r=24, t=56, b=48),
    hoverlabel=dict(bgcolor="white", bordercolor="#cccccc", font_size=12),
)
```

Hover always on (series name + value with units + date). Fill under the primary line only, `opacity≈0.18`. `autosize=True`; check labels at 375px width.

## Bokeh (metapod)

Match the existing dashboard conventions: custom `HoverTool` tooltips (never the default), the palette above, `sizing_mode="stretch_width"`.

## Pre-ship checklist

- [ ] Title is the insight, Playfair Display left-aligned, data-derived numbers; source + notes block bottom-left
- [ ] Every axis labeled (mono, uppercase) — no exceptions
- [ ] All in-axes text cased (`CASING`); no italics; no default degree labels on polar axes; special glyphs (± σ Δ ▲▼) render in the PNG
- [ ] Baseline `plot_style.py` applied (no default styles); typography tiers respected
- [ ] Variance shown — or its absence explained in the bottom notes line
- [ ] Series direct-labeled where possible; nothing overlaps; rendered PNG inspected before shipping
- [ ] Interactive: hover shows name + value + units
