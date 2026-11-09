# Assignment W2 — Material discrimination and classification mini-project

**Space Academy 2026 · Hyperspectral course · Week 2** · pairs · due at the start of Week 3 · 15 % of the course grade

> **Not used in the 2026 three-week course.** Assessment is the mini project alone — see
> [`final_project_brief.md`](final_project_brief.md). This brief is kept for reference and for a
> future longer run, and is still a good self-directed exercise.

**Goal:** apply feature extraction, spectral matching or detection, and supervised classification to one area, and
measure what the hyperspectral bands add.
**Builds on:** notebooks `13_feature_extraction_dim_reduction`, `14_material_discrimination_target_detection`, `15_classification_classical`.

## Task

Use a window of about 300 × 300 pixels from **one** scene that has WorldCover labels in `data/labels/` (all course
scenes), or your own labels.

1. **Features:** compute PCA **and** MNF on your window. Show the first 6 components of each and explain which
   is more useful for your area and why (look at the noise).
2. **Spectral matching:** choose one material of interest. Take its reference spectrum from `hu.load_library()` or
   from the image, and map it with **SAM** and with **one** statistical detector (MF, ACE or CEM). Justify your
   thresholds, and show the detections over a true-colour image.
3. **Classification:** train a random forest (and optionally an SVM) on pure pixels with a **spatially separated**
   train/test split. Report OA, per-class F1 and the confusion matrix.
4. **The hyperspectral question:** repeat step 3 with (a) simulated Sentinel-2 bands and (b) 3–5 indices.
   Present the three results in one table and interpret the difference honestly. "No gain" is a valid finding
   if it is explained.
5. **Map:** export the classification as a COG (`hu.save_geotiff`) and include a figure with a legend.

## Grading

| Component | Points |
|-----------|:------:|
| PCA vs MNF comparison and interpretation | 15 |
| SAM + detector, with threshold justification | 25 |
| Classification with a correct spatial split | 25 |
| Hyperspectral vs multispectral comparison and interpretation | 25 |
| Map export, figure quality, clarity | 10 |
