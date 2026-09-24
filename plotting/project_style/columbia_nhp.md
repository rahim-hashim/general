# Columbia NHP plotting guide

Project layer over the general [STYLE.md](../STYLE.md). Everything there applies
here (spacing scale, legend hierarchy, overlap check, tables, variance, checklist)
**except** the rules this file overrides by name below. Reference IDs (N1–N6, S6,
D6 …) point into [REFERENCES.md](../REFERENCES.md).

## Purpose and ownership

This is the shared visual reference for the Columbia NHP projects. Reusable visual
conventions live here; scientific transformations, statistics and renderers live in
the analysis repository and are tested there. Do not turn a reference illustration
into an implied analysis result. Keep original source images in `../source/` unchanged.

`valence-geometry/src/valence_geometry/plotting/style.py` is the executable baseline for
this project. It originated from a 2026-09-13 snapshot; the 2026-09-17 revision introduced
journal sans typography while preserving the infographic's editorial profile. It is not
present in this checkout. Neither is the former `plot_style.py`, and this guide does not
claim to reconstruct either. No absolute dependency on this folder is required to render
figures.

## Overrides of the general guide

| General rule (STYLE.md) | NHP override | Why |
|---|---|---|
| §4 Editorial typography (Playfair / EB Garamond / Plex Mono) | **Publication and panel figures** use a journal sans stack: Arial, Helvetica, then DejaVu Sans. Bold panel titles, regular axis and legend labels. Mono only for compact provenance metadata. The pipeline **infographic** keeps the editorial profile. | Journal house styles; dense multi-panel pages |
| §2 Insight-stating title, no subtitle | Panel titles make **neutral** claims ("Monkey U, block-wise cPCs"). Dataset identity, cohort size, unit counts, exclusions and fit scope go in the figure caption, or in the bottom block when the figure stands alone. | Claims belong in the text and must survive review |
| §3 `ACCENT` blue for the subject | **Valence palette:** positive valence blue `#2166ac`, negative valence red `#d6604d`, identical across neural and behavioral plots. Encode intensity with a second channel (line style, marker, ordered lightness), never a second contradictory palette. | One meaning per color across the whole paper |
| §3 Green/red for signed change | On any figure that encodes valence, red already means *negative valence*. Signed change there uses ▲▼, `+`/`−` and position against a zero line in `INK`, not green/red. Green/red Δ fills remain fine in tables with no valence coding. | Avoids red meaning two things |
| §7 Scale bars | Stacked traces and raster/PSTH panels may replace the y-axis with a labeled scale bar ("2.1 ΔE", "100 ms") (N2, N5). The quantity and unit must still appear in the bar's label. | Standard in electrophysiology |

Everything else carries over unchanged: white background, no top/right spines, color never
the only identifier, SVG + PNG export (rasterize large point clouds inside vector figures),
and inspecting every final render for clipped or overlapping text with `check_text_overlap`.

The supplied [FT chart reference](../source/reference_ft_typography.png) (L1) motivates
compact, readable sans typography and aligned small multiples. It is not a font match to
copy, and it doesn't change our white backgrounds or scientific color semantics.

## Clarke–Nuyujukian (2026) reference family

Source: Stephen E. Clarke and Paul Nuyujukian, *Fast timescale reparameterization of
stable neural manifolds*, bioRxiv, version posted 7 September 2026.
[Paper and caption](https://www.biorxiv.org/content/10.64898/2026.01.26.701671v2).
This is a preprint. Use its visual organization as inspiration, not as validation of
an analysis method in our dataset. Attribute the reference; do not redistribute its
panels as our own results or reproduce its significance annotations.

Local references:

- [Figure 3 overview](../source/2026_nuyujukian_F3.jpg)
- [PCA reference](../source/2026_nuyujukian_PCA.jpg)
- [Channel-level trace reference](../source/2026_nuyujukian_single-neuron.jpg)
- [Cosine similarity](../source/2026_nuyujukian_cosine-similarity.jpg)
- [Heatmap](../source/2026_nuyujukian_heatmap.jpg)

### Figure 3: reusable panel vocabulary

| Reference panels | Visual convention to reuse | Required scientific distinction |
| --- | --- | --- |
| a, b, e, g | Small-multiple projections; consistent camera angle, coordinate basis and limits; gray contextual points; restrained highlighted subsets | These cPCs visualize collections of block-wise state eigenvectors. They are not ordinary PCA trajectories of trial activity. Name the rows of the matrix being projected. |
| b, h | Thin curves/step histograms; direct labeling; explicit null/reference line | State sample units, normalization and how the null was generated. |
| c, d, f, j | Compact distributions with visible observations, shared axes and a quiet reference band | Define whether observations are trials, units, sessions or subjects. Do not imply that all are independent biological replicates. |
| i | Overlaid similarity distributions plus a separate signed difference panel | Preserve negative differences, bin widths and density/probability units. Do not hide subchance values. |
| k | Train-by-test matrix next to dimension/performance curves and alignment comparisons | Explicit train/test axes, metric and chance level. Alignment fitted using test data is not an ordinary inductive held-out result. |
| l | Paired observations connected within session, separated by subject | Pairing is by identity, not row order. Only draw statistical brackets from saved, multiplicity-aware tests. |

The full reference Figure 3 is a style atlas, not a requirement to cram every analysis
into one page. Build panels independently, then compose them with uniform gutters,
panel labels and an explicit reading order. Share colorbars only when scales match.

### Single-unit activity: raster + PSTH

Use two vertically aligned axes with a shared event-time axis. Group raster trials by
the stated condition; retain within-condition trial order. Show unsmoothed mean rate
and an explicitly named uncertainty statistic. Display CS on, CS off and outcome using
actual event metadata. If events vary across trials, label aggregate markers as such
or use trial-specific raster marks; do not imply exact simultaneous timing.
Stack condition legend entries vertically in a reserved right margin outside both axes.
Keep raster and PSTH widths identical; legends must not cover data or event annotations.

State firing-rate units (spikes/s), bin width, trial counts, unit identity/quality and
coverage exclusions. A raster and its PSTH must bind to the same spike evidence.
Zero means observed silence; missing recording support is not zero. Separate optional
display smoothing from the unsmoothed decoding inputs. SEM across trials is descriptive
within-session variability, not a subject-level confidence interval.

### Stacked unit/stability traces

The image called `single-neuron` shows channel-level changes in subspace-energy
contribution, not a raster/PSTH. Reuse its aligned traces and compact labels for a
separate stability panel. Use one shared amplitude scale; report any mean centering.
Our initial synthetic template shows block mean firing rate, **not** subspace energy.
Name the measured quantity and block definition rather than copying the reference axis.

### Activity-space PCA

Render a two-dimensional projection alongside a consistently oriented three-dimensional
condition-mean trajectory and a variance-explained panel. Use faint trial-bin points as
context, readable condition means and marked trajectory endpoints. Preserve coordinate
scales across comparable panels and report whether counts were centered, scaled or
otherwise transformed. Show retained-unit and trial counts in the accompanying metadata.

Every PCA object must record the input identity, training trial IDs, mean/centering,
components and explained variance. PCA used by a decoder must be refitted inside every
training fold. A PCA fitted to all trials is allowed only as a labeled descriptive view;
it is not evidence of held-out separability. cPC/eigenvector clustering, rank matching
and Procrustes alignment are separate future recipes, not silently activated defaults.

### Connected condition-centroid reference

The supplied [three-subject projection reference](../source/reference_condition_projections.png)
adds a complementary visual vocabulary: outlined condition-centroid markers, distinct
marker-fill and connecting-line encodings, pale guides and consistently oriented facets.
Its source paper is not yet identified; retain it as a user-supplied visual reference,
not a methods citation. Do not redistribute the panel as an original result.

Use this design when the analysis actually supplies condition centroids and a defined
ordering. State what each point averages, what each visual channel means, and whether
connections encode time, ordered conditions or an experimental topology. Never connect
arbitrary categories as if they were a temporal trajectory. Preserve our valence palette;
use a second visual channel for intensity or identity with its own compact key.

Axes labeled "Unit Target PC" and "Unit Reward PC" in the reference are not interchangeable
with ordinary joint activity PCA. Our current renderer remains a time-ordered activity-PCA
view with PC1/PC2/PC3 labels. Task-specific subspaces require a separately specified and
validated projection method. Comparable panels must share a meaningful basis and scale;
independently fitted subjects do not acquire homologous axes merely by using the same view.

## Other neuro references in the inventory

These are visual conventions only; the same caveats apply (preprints and published
figures are not validation of a method on our data).

| Ref | Reuse for |
|---|---|
| N5 ([raster/PSTH with value tiers](../source/Screenshot%202024-09-02%20at%2011.17.20%E2%80%AFAM.png)) | Shaded epoch windows spanning raster and PSTH; a time scale bar in place of a full axis; stats (r, P) printed above each scatter. Retitle upright; the reference's italic panel titles break our never-italic rule. |
| N6 ([delay-period selectivity](../source/Screenshot%202024-10-30%20at%2011.39.03%E2%80%AFPM.png)) | Donut with n in the centre as a *count* summary; arrows linking the summary to per-category breakdown panels. Its six-hue line palette is what we avoid: use the valence palette plus a lightness ramp. |
| D2 ([split violin, n rows](../source/IMG_7308.PNG)) | Two-condition distributions with `n = … cells` / `n = … sessions` rows aligned under the categories. That makes it explicit which level is the replicate. |
| D3 ([histogram + CDF](../source/Screenshot%202023-12-09%20at%203.11.00%E2%80%AFPM.png)) | Response-amplitude distributions per stimulus class with percentile cut lines labeled in place. |
| S6 ([lag heatmap](../source/2026_nuyujukian_heatmap.jpg)) | Session-by-lag matrix under its mean ± band trace, with subject brackets (U, H) instead of per-row tick labels. |
| N7 ([facial-feature weights](../source/F5.large.jpg)) | Species-colored horizontal bars grouped by body part with dashed separators. Prefer this to its radar panels. |

## Implemented examples

In `valence-geometry`, run:

```bash
MPLBACKEND=Agg uv run python -m valence_geometry.analysis_cli examples --output /path/to/new/examples
```

This produces synthetic raster/PSTH, activity-PCA and stability SVG/PNG figures,
decoder fold scores and held-out predictions, plus a data/provenance manifest.
Synthetic labels must remain visible. The examples do not establish alignment or
tracking accuracy in any recorded session.
