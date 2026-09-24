# Reference inventory

Every file in [`source/`](source/), reviewed image by image on 2026-09-24. Each entry
records what to **borrow** and, where the reference fails, what to **avoid**. It is a
failure catalogue as much as an inspiration board. [STYLE.md](STYLE.md) cites these by
the short ID in the first column.

These are third-party works kept for study. Do not redistribute them, and do not present
a recreation of one as original work. Credit the source in the figure's bottom block.

Byte-identical duplicates: `reference_ft_typography.png` = `20260821_FT_Houthis.png`, and
`reference_condition_projections.png` = `Screenshot 2024-12-16 at 3.00.55 PM.png`.
`IMG_1990.JPG` and `IMG_1990.PNG` are **different** images. Several screenshot names
contain a narrow no-break space (U+202F) before AM/PM; quote them in shell commands.

## Tables

| ID | File | Borrow | Avoid |
|---|---|---|---|
| T1 | [datakabas_tennis_table.jpg](source/datakabas_tennis_table.jpg) | **The canonical table.** Heavy vertical rules separate column *groups* (label │ Bo5 │ Bo3 │ Δ), not every column. Heavy rule under the header. Faint zebra. Conditional fill on **only** the signed Δ column, diverging green → white → red centred at 0; text flips to white on dark fills. Bold row labels. Note and source bottom-left. | Signs carried by color alone (add ▲▼). Centred numerals (right-align mono instead). |
| T2 | [Screenshot 2026-07-19 at 7.53.44 AM.heic](source/Screenshot%202026-07-19%20at%207.53.44%E2%80%AFAM.heic) | Spanner headers ("Stats", "Scouts") over groups, divided by heavy vertical rules. Two-line row label: bold name plus small gray context line. Diverging fill for deviation from consensus. Code value ("UR") explained in a footnote. | Filling every cell (diverging fill across the whole grid): good for spotting outliers, too loud for one key column. |
| T3 | [Screenshot 2026-07-19 at 7.53.58 AM.heic](source/Screenshot%202026-07-19%20at%207.53.58%E2%80%AFAM.heic) | Two-line cells: primary value bold, secondary value small and muted beneath it. Sequential single-hue fill for magnitude. "–" for structurally empty cells, not blank and not 0. | Muted gray secondary text sitting on saturated fill loses contrast. |
| T4 | [Screenshot 2026-07-19 at 7.52.37 AM.heic](source/Screenshot%202026-07-19%20at%207.52.37%E2%80%AFAM.heic) | Heavy top rule, sortable ranking column on the right with a monochrome fill, right-aligned numerals, mixed-format cells (`9/12`, `+25`). | — |
| T5 | [IMG_1289.PNG](source/IMG_1289.PNG) | Grid table as a chart: rows × ordered states, filled cell = current state, outlined cell = new state, arrow = transition. Note line for the asterisk. | — |
| T6 | [IMG_3841.PNG](source/IMG_3841.PNG), [IMG_3842.PNG](source/IMG_3842.PNG) | Tile calendars: one tile per (entity, period), number printed inside, ordinal palette. Faint dashed column guides. Annotations with arrows placed in the table's empty whitespace. | Palette with no key (3842 relies on the number inside each tile; keep the number). |
| T7 | [NYT_Mayoral-Map.png](source/NYT_Mayoral-Map.png) (tooltip + side panel) | Micro-table: colored left border as the series key, bold percentage column, muted counts. | — |

## Distributions and variance

| ID | File | Borrow | Avoid |
|---|---|---|---|
| D1 | [Screenshot 2023-10-29 at 5.07.28 PM.png](source/Screenshot%202023-10-29%20at%205.07.28%E2%80%AFPM.png) | Raincloud: jittered points + box + half-violin per group. | Legend repeating the x-tick labels (redundant). Huge axis type crowding the panel. |
| D2 | [IMG_7308.PNG](source/IMG_7308.PNG) | Split half-violins for two groups on one axis. **n rows under the x-axis** (`n = 322 cells / 6 mice`), a table aligned to the categories. | Inset bar chart of means duplicating the violins. |
| D3 | [Screenshot 2023-12-09 at 3.11.00 PM.png](source/Screenshot%202023-12-09%20at%203.11.00%E2%80%AFPM.png) | Step histograms overlaid with CDF on a twin axis; percentile lines labeled in place (10%, 90%); small titled legend. | Twin y-axes (acceptable only when both are densities of the same variable, as here). |
| D4 | [IMG_1294.PNG](source/IMG_1294.PNG) | Strip plot per year with a pale range bar behind the dots, a heavy zero line, one highlighted point in the accent color. | — |
| D5 | [IMG_4056.JPG](source/IMG_4056.JPG) | Quantile dot plot: range bar + 5 percentile dots per row, rows sorted by median. **Legend drawn as a miniature of the glyph** in empty space. Top-coding shown by a labeled vertical dashed line. | Rotated x tick labels; five hues where a single ramp would do. |
| D6 | [2026_nuyujukian_cosine-similarity.jpg](source/2026_nuyujukian_cosine-similarity.jpg) | Overlaid step histograms with **colored-text legend** (no swatches); signed excess panel with fill above/below a dashed zero and threshold labeled in place. | — |

## Time series and lines

| ID | File | Borrow | Avoid |
|---|---|---|---|
| L1 | [20260821_FT_Houthis.png](source/20260821_FT_Houthis.png) | Small multiples with shared x; start value at left, end value at right of each panel; event lines through every panel, labeled once in a tinted band at the top; x ticks only on first and last panel. | Italic panel titles (our rule: never italic). |
| L2 | [IMG_2007.PNG](source/IMG_2007.PNG) | Gray context lines, highlighted series in color, **end labels with open-circle markers**; the highlight word colored in the title. | End labels for Google / xAI / DeepSeek jammed together: the collision the repel rule prevents. |
| L3 | [IMG_1990.JPG](source/IMG_1990.JPG) | End labels = color tick + bold name + muted mono metadata (`10×100M`). Threshold lines labeled inline at left. Envelope as a dashed line. | "M8"/"M7" threshold labels touching; threshold labels struck through by data lines; 5-pt annotation text. |
| L4 | [IMG_3843.PNG](source/IMG_3843.PNG) | Direct labels at line ends, value labels at a few marked points only, and a group header ("Recent World Bank data") over a cluster of labels. | — |
| L5 | [Screenshot 2026-05-29 at 6.07.04 PM.heic](source/Screenshot%202026-05-29%20at%206.07.04%E2%80%AFPM.heic) | Wilke's before/after argument: **direct labels replace the legend** and remove the need for markers. | — |
| L6 | [Screenshot 2024-09-24 at 12.19.33 PM.png](source/Screenshot%202024-09-24%20at%2012.19.33%E2%80%AFPM.png) | Raw observations as faint dots behind the smoothed estimate. Event annotations **stacked above the plot area** with leaders to dotted verticals. End labels carry name + value. | — |
| L7 | [Screenshot 2026-02-22 at 8.00.49 PM.png](source/Screenshot%202026-02-22%20at%208.00.49%E2%80%AFPM.png) | End label with bold value + date ("2.4% in Jan."), second series labeled in its own tint; gap shaded and labeled "No data for October". | Italic for the missing-data note. |
| L8 | [IMG_3175.PNG](source/IMG_3175.PNG) | Inline curve labels; **gap between two series shaded and bracketed** with its magnitude ("3.2-point gap"). | — |
| L9 | [IMG_5292.JPG](source/IMG_5292.JPG) | Key end point as halo dot + bold value (our `key_dot`). Shaded context bands (recessions) labeled at the base. | — |
| L10 | [IMG_2933.PNG](source/IMG_2933.PNG) | 4-column small multiples, per-panel mini-caption ("S8 · avg 6.4"), color = pass/fail against a threshold. | Tick labels at ~5 pt; independent x ranges that look shared. |
| L11 | [IMG_3098.PNG](source/IMG_3098.PNG) | Bars for raw counts + line for rolling average; KPI header line (`TOTAL … 3,037  14-DAY CHANGE −6%`); three sparklines with identical frames. | — |
| L12 | [ScreenRecording_11-06-2024 19-07-15_1.mp4](source/ScreenRecording_11-06-2024%2019-07-15_1.mp4) | Interactive toggle between years on the same basemap; the selected state is a filled chip. | — |
| L13 | [Screenshot 2026-04-30 at 10.25.42 AM.heic](source/Screenshot%202026-04-30%20at%2010.25.42%E2%80%AFAM.heic) | Plain one-series line with abbreviated year ticks ('45, '50). | Eleven gridlines for one line; no annotation of the peaks the title implies. |
| L14 | [IMG_0587.PNG](source/IMG_0587.PNG), [Screenshot 2023-10-04 at 9.53.07 PM.png](source/Screenshot%202023-10-04%20at%209.53.07%E2%80%AFPM.png) | Win-probability: one line, fill toward the 50% line in each side's color. | Axis labeled "100 / 50 / 100" (the scale flips meaning mid-axis without saying so). |
| L15 | [the-u-s-china-ai-race-in-frontend-coding-v0-rwsf16cjsvdh1.webp](source/the-u-s-china-ai-race-in-frontend-coding-v0-rwsf16cjsvdh1.webp) | Main panel + **signed difference panel** below with shared x, labeled "US advantage / China advantage". | Point labels with leaders scattered everywhere, crossing lines and each other. |
| L16 | [IMG_3840.PNG](source/IMG_3840.PNG) | Ridgeline sorted by peak date; subtitle states that scales are independent per row. | — |

## Bars, composition, ranking

| ID | File | Borrow | Avoid |
|---|---|---|---|
| B1 | [barchart_default.png](source/barchart_default.png), [barchart_clicked.png](source/barchart_clicked.png) | Interactive legend: clicking one category dims the rest to ~25%. Final (partial) period's tick in bold, explained in a note. | **Legend entry split across lines** ("Export / restrictions"). Seven hues at equal weight. |
| B2 | [IMG_1447.JPG](source/IMG_1447.JPG) | Signed stacked bars + total line; y-axis unit written once on the top tick ("$80 billion"). | — |
| B3 | [IMG_5828.PNG](source/IMG_5828.PNG) | Signed stacked composition + bold total line labeled in place. **Directional axis annotations** ("↑ Stretched capacity / ↓ Under-utilised"). Event line with a dot-ended label. | — |
| B4 | [IMG_1552.PNG](source/IMG_1552.PNG) | Outline the one bar being discussed; curved leader to a two-line label (name bold, value regular). | — |
| B5 | [IMG_2403.PNG](source/IMG_2403.PNG) | Series labels placed beside the last bar with a short rule (no legend). Horizontal stacked bars with labels **below** each segment. | Tick labels stacked over tick marks (hard to match). |
| B6 | [IMG_1295.PNG](source/IMG_1295.PNG) | 2×3 small multiples with shared y, one legend row above all panels. | — |
| B7 | [IMG_0739.JPG](source/IMG_0739.JPG) | Category color families; legend tucked into genuinely empty space inside the axes. | ~60 rotated x labels: flip to horizontal bars. |
| B8 | [IMG_1990.PNG](source/IMG_1990.PNG) | 100% diverging stacked bars, neutral middle category, **title-as-legend** (the words "Up" / "Down" colored). | "100%" tick label clipped at the right edge. |
| B9 | [ssaiyplyzvmd1.png](source/ssaiyplyzvmd1.png) | Back-to-back (butterfly) bars with shared center labels. **Broken bars (slash)** for off-scale values. | Infographic clutter around them. |
| B10 | [kwdqnagipmmd1.png](source/kwdqnagipmmd1.png) | 100% stacked area, EB Garamond throughout, end-values at right. | End-value boxes not colored or named: the reader must match them by position. |
| B11 | [IMG_5293.PNG](source/IMG_5293.PNG) | Net-income bars colored by sign. | A ratio (net margin) drawn on the dollar axis with no scale of its own. |
| B12 | [IMG_9428.PNG](source/IMG_9428.PNG) | Categorical strip of icons on a shared value axis. | Overplotted icons; unreadable clusters. |

## Scatter, bubbles, matrices

| ID | File | Borrow | Avoid |
|---|---|---|---|
| S1 | [mil0kcf2m24h1.jpeg](source/mil0kcf2m24h1.jpeg) | **Bubble-size key as nested circles** in a boxed corner. Axes through zero with bold axis names at the ends. Curved leaders pull labels out of the crowded cluster. | — |
| S2 | [IMG_1271.PNG](source/IMG_1271.PNG) | Beeswarm with highlight in the accent color and a dashed reference line; **directional captions under the axis** ("← Lower / Higher →"). | Labeling ~60 points: collisions ("Iraq", "Kenya"). |
| S3 | [IMG_2175.PNG](source/IMG_2175.PNG) | Heatmap where square size and color both encode effect; n per column in the column label; dendrograms; stars inside cells. | 45° column labels. |
| S4 | [kffyy8f1elzd1.png](source/kffyy8f1elzd1.png) | Heatmap rows grouped with **white gaps between groups**, group names in a tinted right-margin band. | 45° tick labels colored by party (unreadable). |
| S5 | [Screenshot 2026-05-22 at 7.49.42 AM.heic](source/Screenshot%202026-05-22%20at%207.49.42%E2%80%AFAM.heic) | 2×2 matrices with one shared colorbar; summary badge ("diag: 0.97") boxed inside the upper-left corner. | Rotated tick labels. |
| S6 | [2026_nuyujukian_heatmap.jpg](source/2026_nuyujukian_heatmap.jpg) | Mean ± band trace aligned above a matrix on the same x; bracket spines naming row groups (U, H); range-frame axes. | — |
| S7 | [7F23mlI.jpeg](source/7F23mlI.jpeg) | Bump/ribbon ranking with endpoint flags and values. | Value labels on every node: unreadable at 5 pt. |

## Neuroscience and scientific panels

| ID | File | Borrow | Avoid |
|---|---|---|---|
| N1 | [2026_nuyujukian_F3.jpg](source/2026_nuyujukian_F3.jpg) | Multi-panel atlas: letter labels, uniform gutters, shared axes, box + paired points, significance brackets. | Density: a style atlas, not a page layout to copy. |
| N2 | [2026_nuyujukian_single-neuron.jpg](source/2026_nuyujukian_single-neuron.jpg) | Stacked traces, labels in muted gray at the right end, **scale bars** instead of y-axes, gray-ramp dot key. | — |
| N3 | [2026_nuyujukian_PCA.jpg](source/2026_nuyujukian_PCA.jpg) | Gray context points + colored subsets; glyph key for task condition. | 3-D axes with no tick values. |
| N4 | [reference_condition_projections.png](source/reference_condition_projections.png) | Outlined centroid markers, fill = one variable, line = another, inset position key. | — |
| N5 | [Screenshot 2024-09-02 at 11.17.20 AM.png](source/Screenshot%202024-09-02%20at%2011.17.20%E2%80%AFAM.png) | PSTH over raster on shared time, shaded epochs, scale bar ("100 ms"), legend with a title in open space; r and P printed above scatter panels. | Italic panel titles. |
| N6 | [Screenshot 2024-10-30 at 11.39.03 PM.png](source/Screenshot%202024-10-30%20at%2011.39.03%E2%80%AFPM.png) | Rasters above rate traces; donut with **n in the center**; arrows linking a summary panel to its breakdowns. | 5-color line palette distinguished only by hue. |
| N7 | [F5.large.jpg](source/F5.large.jpg) | Radar small multiples per state; horizontal bars grouped by dashed separators with icon keys. | Radar for quantitative comparison (use bars). |
| N8 | [m2-res_1080p.mp4](source/m2-res_1080p.mp4) | Synchronized multi-view dashboard (video + 3-D + traces) sharing one time cursor. | 5-pt legends and ticks; a dashboard of this kind needs large type or fewer panels. |

## Editorial frame, annotation, infographics

| ID | File | Borrow | Avoid |
|---|---|---|---|
| E1 | [IMG_2706.PNG](source/IMG_2706.PNG), [IMG_2707.PNG](source/IMG_2707.PNG) | **Closest to our editorial profile.** Serif display title as a statement; mono tick labels and uppercase mono kicker; mono footnote block under a hairline; highlight point + serif label with value subline; dotted event line labeled at top. | Italic sublabels. |
| E2 | [Screenshot 2024-09-24 at 12.19.33 PM.png](source/Screenshot%202024-09-24%20at%2012.19.33%E2%80%AFPM.png) | Note + "Updated" line bottom-left, publisher mark bottom-right. | — |
| E3 | [IMG_1552.PNG](source/IMG_1552.PNG), [IMG_5828.PNG](source/IMG_5828.PNG) | Short accent bar above the title (Economist tag). | — |
| E4 | [HJMxTWSaQAAE6WZ.jpeg](source/HJMxTWSaQAAE6WZ.jpeg) | Small multiples of text-as-bars; one-line centred legend under the title; captions quoting the highlighted (boxed) segment. | — |
| E5 | [GWZ8NnmWwAApav8.jpeg](source/GWZ8NnmWwAApav8.jpeg) | Aligned list of labels with orthogonal leaders to map points: labels never sit on the map. | — |
| E6 | [IMG_4311.JPG](source/IMG_4311.JPG) | Patent-style numbered callouts with thin leaders. | — |
| E7 | [IMG_3460.PNG](source/IMG_3460.PNG) | Keyword in text colored to match the illustration element (EPF red / IPF teal). | — |
| E8 | [F-WbwckW0AE26n_.jpeg](source/F-WbwckW0AE26n_.jpeg) | Explanatory schematic of manifold size and alignment for talks. | Dark background (not our default). |
| E9 | [97pfzvx4ktmd1.jpeg](source/97pfzvx4ktmd1.jpeg), [NMAH-ET2014-41022.jpg](source/NMAH-ET2014-41022.jpg) | Lineage diagrams: a column per stage, color identity preserved through merges. | — |
| E10 | [hfxgwl8229kd1.png](source/hfxgwl8229kd1.png), [qiql2odnuggd1.jpeg](source/qiql2odnuggd1.jpeg) | Lifespan-bar timelines: name + dates above each bar, category colors, bracketed eras. | Density far past legibility. |
| E11 | [IMG_0038.PNG](source/IMG_0038.PNG) | Radial tree with time rings labeled along the baseline. | — |
| E12 | [IMG_4057.JPG](source/IMG_4057.JPG) | Decision-tree flowchart: node style = node type (dashed = intermediate). | Cartoon figures. |
| E13 | [NYT_Mayoral-Map.png](source/NYT_Mayoral-Map.png) | Two-hue sequential choropleth with a compact stepped key. | — |
| — | [IMG_1943.PNG](source/IMG_1943.PNG), [jgjce8bc2pmd1.jpeg](source/jgjce8bc2pmd1.jpeg), [IMG_4153.JPG](source/IMG_4153.JPG), [IMG_2374.PNG](source/IMG_2374.PNG) | Sunburst, treemap, infographic, radar. Kept as counter-examples: part-to-whole by angle or area, pictorial clutter, radar. | Prefer sorted bars. |
