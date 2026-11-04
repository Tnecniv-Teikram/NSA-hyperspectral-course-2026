# Answer key — Quiz W1b — Preprocessing concepts for hyperspectral data

*Instructor copy. Do not distribute to students before the quiz.*

| # | Answer | Why |
|---|:---:|-----|
| 1 | **d** | Atmospheric correction models gas absorption and molecular/aerosol scattering to retrieve surface reflectance from at-sensor radiance. |
| 2 | **a** | Near-total absorption by atmospheric water vapour: almost no surface signal, extremely low SNR. |
| 3 | **d** | Orthorectified swaths are rotated inside a north-up grid; the corners outside the swath are no-data. |
| 4 | **d** | Bright evaporite surfaces (sabkha, salt, gypsum) resemble cloud in simple tests. Check spectra: sabkha shows mineral/water absorption features that clouds lack. |
| 5 | **c** | SWIR water-leaving reflectance is ~0; noise and small correction errors give slightly negative values. Discarding them biases water statistics. |
| 6 | **a** | Savitzky-Golay fits local polynomials and preserves feature shape better than a box filter, but the window length must stay smaller than the features of interest. |
| 7 | **a** | Dividing by the hull normalises the continuum so absorption depth/shape is comparable across brightness levels. |
| 8 | **a** | SNR ≈ signal / noise, i.e. reflectance / uncertainty. |
| 9 | **a** | Orthorectification uses a DEM and the sensor geometry to remove relief and viewing distortions and to map pixels onto a map grid. |
| 10 | **b** | Striding subsamples rows/columns (no averaging): good for previews, not for small-feature statistics. |
| 11 | **b** | The flagged bands hold placeholder values, not measurements; they must be dropped. |

## Model answers for the short questions

**12.** (1) Choose the scene and window; (2) apply QA masks (no-data, cloud, cirrus) after inspecting them; (3) remove bad bands (water vapour, <400 nm, >2450 nm, flagged placeholders); (4) check value ranges and negative values; (5) optionally smooth or normalise (Savitzky-Golay, brightness normalisation) with a justification; (6) extract features or reduce dimensionality; (7) ensure labels align with the grid (CRS, pixel size) before building train/test sets.

**13.** (a) When narrow absorption features are the signal (e.g. mineral doublets, gas absorption for CH4 matched filtering), because smoothing reduces their depth; (b) when noise statistics matter, e.g. before MNF, target detection or covariance estimation, where smoothing changes the noise covariance; also when validating against lab spectra convolved to the sensor response.
