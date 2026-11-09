# Project scoping canvas

**Space Academy 2026 · Hyperspectral course · Week 2 — Project scoping and use case definition**

Fill this in as a team (1–2 pages). You will present it in the scoping session, and it becomes the first section of
your project notebook (`templates/project_template.ipynb`). Keep it concrete: a reviewer should be able to tell
exactly **what** you will map, **where**, **with which data**, and **how you will know whether it worked**.

---

## 1. Team

| Name | Background | Role in the project |
|------|------------|---------------------|
|      |            |                     |

## 2. Problem statement (≤ 80 words)

> *Who* has *what* problem *where*, and why does it matter now?

## 3. Users and decisions

| Question | Your answer |
|----------|-------------|
| Who is the end user (organisation, role)? | |
| Which decision will your output support? | |
| What do they use today, and why is it not good enough? | |
| How often do they need the information (once, monthly, near-real-time)? | |
| In what form do they need it (map, number, alert, report, API)? | |

## 4. Why hyperspectral?

What can Tanager/EnMAP see that Sentinel-2 or Landsat cannot? Name the **specific spectral features** (wavelength
ranges, absorption features, indices) your method relies on. If multispectral data would work equally well, say so.
That is a valid finding, but then the project must add value in another way.

## 5. Area of interest and time frame

- AOI (name, bounding box in lon/lat, size in km²):
- Period of interest:
- Why this AOI is representative of the wider problem:

## 6. Data availability (use `16_scene_finder.ipynb`)

| Dataset | Scene IDs / product | Date(s) | Cloud % | Role in the project |
|---------|---------------------|---------|---------|---------------------|
| Tanager | | | | primary analysis |
| EnMAP / Sentinel-2 / Landsat (optional) | | | | temporal context, validation, scaling |
| Reference / labels | e.g. ESA WorldCover, field data, published maps | | | training / validation |
| Ancillary | e.g. DEM, weather, infrastructure locations | | | |

- [ ] At least one usable Tanager scene covers the AOI (checked with thumbnails and QA masks).
- [ ] If the method needs change detection: at least two dates over the same AOI.
- [ ] A source of reference data for validation exists (if not, say how you will validate).

## 7. Method (first version)

1. Preprocessing (bad bands, masks, subsetting) — `11_preprocessing.ipynb`
2. Features (indices, PCA/MNF, continuum removal…) — `13_feature_extraction_dim_reduction.ipynb`
3. Core analysis (target detection / unmixing / classification / regression / change detection) — notebooks 14, 15, 20, 30
4. Output product (map, statistic, alert)

Draw the processing chain as boxes and arrows. A photo of a whiteboard is fine.

## 8. Validation plan (use `21_validation_accuracy_assessment.ipynb`)

| Item | Plan |
|------|------|
| Reference data | |
| Metric(s) | e.g. OA + per-class F1, IoU, RMSE, detection rate at a fixed false-alarm rate |
| Sampling / split | spatially separated train/test blocks, stratified sample… |
| Success criterion | e.g. "F1 ≥ 0.8 for the mangrove class" |

## 9. Deliverables

- [ ] Reproducible notebook (runs top to bottom)
- [ ] Output layer(s) as Cloud-Optimised GeoTIFF + metadata
- [ ] Validation table
- [ ] Mock-up or prototype of how the user receives the result (dashboard, API, report)
- [ ] Final presentation (see `templates/presentation_template.md`)

## 10. Risks and fallbacks

| Risk | Likelihood | Impact | Fallback |
|------|-----------|--------|----------|
| No cloud-free scene over the AOI | | | use another AOI from the same collection |
| No reference data | | | visual interpretation plus VHR imagery, cross-sensor consistency |
| Method does not separate the classes | | | merge classes, add SWIR features, switch to unmixing |

## 11. Timeline

| When | Milestone |
|------|-----------|
| Thu 19 Nov | This canvas drafted in the scoping session |
| Mon 23 Nov | Canvas due · data downloaded, first quicklooks |
| Tue 24 Nov | Working method on one scene |
| Wed 25 Nov | Build afternoon — final validation numbers |
| Thu 26 Nov | Submission in the morning, presentation in the afternoon |

---
*Data: Tanager — CC-BY-4.0 © Planet Labs PBC. Credit every dataset you use.*
