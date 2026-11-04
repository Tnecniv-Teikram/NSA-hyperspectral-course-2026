# Assignment W3 — A validated AI map (interim project milestone)

**Space Academy 2026 · Hyperspectral course · Week 3** · project team · due before the *Interim project feedback and quality assurance* session · 15 % of the course grade

**Goal:** produce the first validated version of your project's main map, using an AI/GeoAI model and a rigorous
validation design.
**Builds on:** notebooks `20_geoai_deep_learning`, `21_validation_accuracy_assessment`, `templates/project_template.ipynb`.

## Task

Work in your project notebook (based on `templates/project_template.ipynb`):

1. **Model:** train at least one ML/DL model for your problem (RF/SVM, 1D-CNN, patch CNN, or a regression model
   for continuous targets) **and** a simple baseline (threshold or index).
2. **Validation design:** write down your reference data, sampling design and train/test split before looking at
   the results. The split must be spatially independent (blocks, sites or dates).
3. **Metrics:**
   - classification: error matrix, OA, user's/producer's accuracy, F1 (and IoU for a target class);
   - continuous products: RMSE, MAE, bias, R² plus a scatter or Bland-Altman plot;
   - detection: detection rate at a fixed false-alarm rate.
4. **Random vs spatial validation:** report both and explain the difference.
5. **Area or uncertainty:** give an area-adjusted estimate with a 95 % CI (Olofsson et al. 2014) **or** a
   per-pixel uncertainty/confidence map with interpretation.
6. **Error analysis:** show three concrete failure cases (location, spectrum, likely cause).
7. Fill in `templates/interim_qa_checklist.md` for your own notebook and attach it.

## Grading

| Component | Points |
|-----------|:------:|
| Model + baseline, reproducible | 20 |
| Validation design written before the results, spatially independent | 25 |
| Correct, complete metrics | 20 |
| Random vs spatial comparison + area/uncertainty | 20 |
| Error analysis + self-QA checklist | 15 |
