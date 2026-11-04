# Answer key — Quiz W3 — GeoAI methods and validation

*Instructor copy. Do not distribute to students before the quiz.*

| # | Answer | Why |
|---|:---:|-----|
| 1 | **a** | 1D-CNN: spectral convolutions per pixel; 3D-CNN: joint spectral-spatial kernels over patches. |
| 2 | **d** | Overlapping patches share pixels, so test inputs are partly training inputs, giving inflated accuracy. |
| 3 | **b** | Self-supervised pretraining learns from unlabelled data; fine-tuning then needs fewer labels. Transfer across sensors still needs adaptation. |
| 4 | **c** | Diverging train/validation loss = overfitting; use early stopping and regularisation. |
| 5 | **c** | Class weighting or balanced sampling plus per-class and macro metrics make minority classes visible. |
| 6 | **b** | User's accuracy = diagonal / row (map) total = precision; producer's accuracy = diagonal / column (reference) total = recall. |
| 7 | **b** | Pontius & Millones (2011): 'Death to Kappa'. Report OA, UA/PA and quantity/allocation disagreement or area-adjusted estimates. |
| 8 | **c** | Olofsson et al. (2014) good-practice: stratified estimators of area and accuracy with confidence intervals. |
| 9 | **b** | IoU = TP / (TP + FP + FN). Option d is the F1/Dice score. |
| 10 | **b** | Correlation does not capture systematic offsets; report bias and RMSE too. |
| 11 | **d** | Softmax scores are confidence scores, usually over-confident unless calibrated. |
| 12 | **b** | Changes in species, background, atmosphere and illumination between regions cause domain shift. |

## Model answers for the short questions

**13.** Reference: an independent, higher-quality source (field GPS points, VHR imagery interpretation), not the training labels. Sampling: stratified random sampling by map class (mangrove, non-mangrove, plus a buffer stratum along the water edge where errors concentrate), with sample size from Olofsson et al. (e.g. ≥50–100 per stratum). Split: training data from separate spatial blocks or sites, never overlapping the validation samples. Metrics: error matrix, user's/producer's accuracy, F1/IoU for mangrove, and an area-adjusted mangrove area with a 95% CI. Report the date mismatch between image and reference.

**14.** (1) A baseline shows how much the CNN actually adds. If an RF reaches 97%, the extra complexity, compute and opacity may not be worth it. (2) It is a sanity check: a much larger gap than expected often reveals leakage (overlapping patches, random splits), label noise or a bug. It also gives a robust fallback for deployment.
