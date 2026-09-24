# Scientific plotting guide

## Purpose and ownership

This is the shared visual reference for the Columbia NHP projects. Reusable visual
conventions live here; scientific transformations, statistics and renderers live in
the analysis repository and are tested there. Do not turn a reference illustration
into an implied analysis result. Keep original source images in `source/` unchanged.

`valence-geometry/src/valence_geometry/plotting/style.py` is the executable style baseline.
It originated from a 2026-09-13 snapshot; the 2026-09-17 revision introduces journal sans
typography while preserving the infographic's editorial profile. The former `plot_style.py`
source file is not present in this checkout; this guide does not claim to reconstruct it.
No absolute dependency on this folder is required to render figures.

## Baseline visual system

- White background, generous margins, sparse light-gray guides, no top/right spines.
- Scientific plots use a journal sans-serif stack: Arial, Helvetica, then DejaVu Sans.
  Use bold titles and regular axis/legend labels. Retain monospace only for compact
  provenance metadata. Dense multipanel labels must remain legible at publication size;
  do not shrink them to fit a crowded page. The pipeline infographic retains its separate
  editorial profile (Playfair Display titles and the original serif body stack).
- The supplied [FT chart reference](source/reference_ft_typography.png) motivates compact,
  readable sans typography and aligned small multiples, not an exact font match or a
  change to our white backgrounds and scientific color semantics.
- Positive valence: blue `#2166ac`; negative valence: red `#d6604d`. Keep this mapping
  identical across neural and behavioral plots. Encode intensity with a second visual
  channel (line style, marker or ordered lightness), not a second contradictory palette.
- Color is not the only identifier: provide labels, marker distinctions or facet titles.
- Neutral claims in titles. Put dataset identity, cohort size, unit counts, exclusions
  and fit scope in concise subtitles/captions, not over the data.
- SVG plus PNG are the default editable/raster pair. Rasterize large point clouds inside
  otherwise vector figures. Inspect every final render for clipped/overlapping text.

## Clarke–Nuyujukian (2026) reference family

Source: Stephen E. Clarke and Paul Nuyujukian, *Fast timescale reparameterization of
stable neural manifolds*, bioRxiv, version posted 7 September 2026.
[Paper and caption](https://www.biorxiv.org/content/10.64898/2026.01.26.701671v2).
This is a preprint. Use its visual organization as inspiration, not as validation of
an analysis method in our dataset. Attribute the reference; do not redistribute its
panels as our own results or reproduce its significance annotations.

Local references:

- [Figure 3 overview](source/2026_nuyujukian_F3.jpg)
- [PCA reference](source/2026_nuyujukian_PCA.jpg)
- [Channel-level trace reference](source/2026_nuyujukian_single-neuron.jpg)
- [Cosine similarity](source/2026_nuyujukian_cosine-similarity.jpg)
- [Heatmap](source/2026_nuyujukian_heatmap.jpg)

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

The supplied [three-subject projection reference](source/reference_condition_projections.png)
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

## Implemented examples

In `valence-geometry`, run:

```bash
MPLBACKEND=Agg uv run python -m valence_geometry.analysis_cli examples --output /path/to/new/examples
```

This produces synthetic raster/PSTH, activity-PCA and stability SVG/PNG figures,
decoder fold scores and held-out predictions, plus a data/provenance manifest.
Synthetic labels must remain visible. The examples do not establish alignment or
tracking accuracy in any recorded session.
