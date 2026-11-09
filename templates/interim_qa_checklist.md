# Project quality-assurance checklist

**Space Academy 2026 · Hyperspectral course · self-check before you submit**

*There is no scheduled interim review in the three-week run of the course. Use this checklist yourself, and
for peer review if you swap notebooks with another team — it is the fastest way to find the things that cost
marks under the Validity criterion.*

Mark each item ✅ (done), ⚠️ (partly) or ❌ (missing), and add one line of comment. Anything marked ❌ in
sections A–C should be fixed before you submit on Thursday 26 November.

Team: ______________________   Reviewer: ______________________   Date: ___________

## A. Reproducibility

| # | Check | Status | Comment |
|---|-------|--------|---------|
| A1 | *Kernel → Restart & Run All* finishes without errors | | |
| A2 | No absolute or personal paths (`C:\Users\…`, `/Users/…`); data found via `hu.get_scene()` or relative paths | | |
| A3 | Scene IDs, windows, thresholds and parameters are defined in one config cell at the top | | |
| A4 | Random seeds fixed (`np.random.default_rng(42)`, `random_state=42`, `torch.manual_seed`) | | |
| A5 | Dependencies listed (extra packages beyond `requirements.txt` are named) | | |
| A6 | Runtime reasonable (< 15 min) or heavy steps are cached and clearly marked | | |

## B. Data and preprocessing

| # | Check | Status | Comment |
|---|-------|--------|---------|
| B1 | Every dataset credited (Tanager CC-BY-4.0 © Planet Labs PBC, WorldCover, …) | | |
| B2 | QA masks applied **and inspected**: no-data, cloud, cirrus (look for false positives, e.g. bright sabkha flagged as cloud) | | |
| B3 | Bad bands removed (water vapour 1340–1445 / 1790–1970 nm, < 400 nm, > 2450 nm) and the choice explained | | |
| B4 | Band choices for every index state the wavelength actually used (e.g. "NIR = 862 nm") | | |
| B5 | Units and value ranges checked (reflectance 0–1; negative values over water understood) | | |

## C. Method and validity

| # | Check | Status | Comment |
|---|-------|--------|---------|
| C1 | The method matches the problem in the scoping canvas (or the change is explained) | | |
| C2 | The hyperspectral advantage is demonstrated or honestly discussed (e.g. comparison with simulated Sentinel-2) | | |
| C3 | Train and test data are **spatially separated** (no neighbouring pixels in both) | | |
| C4 | Validation metrics reported with the confusion matrix / residual plot, not only one number | | |
| C5 | Baseline included (simple threshold, index, or RF) so the gain of the complex model is visible | | |
| C6 | Failure cases shown (where does the method go wrong, and why?) | | |
| C7 | Uncertainty or confidence communicated (probability map, CI on area, σ from the uncertainty layer) | | |

## D. Communication

| # | Check | Status | Comment |
|---|-------|--------|---------|
| D1 | Every figure has a title, axis labels/units, colour bar, legend and a north/scale hint where relevant | | |
| D2 | Colour maps are perceptually sensible (no rainbow for continuous data; categorical colours for classes) | | |
| D3 | Markdown explains *why* before each major step | | |
| D4 | Key numbers are summarised in one results table | | |
| D5 | The user-facing product is sketched (dashboard/API/report mock-up) | | |

## E. Reviewer summary

- **Biggest strength:**
- **Most important fix before submission:**
- **One idea to make the result more convincing for the end user:**
