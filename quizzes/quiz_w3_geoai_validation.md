# Quiz W3 — GeoAI methods and validation

**Space Academy 2026 · Hyperspectral course · Week 3**
Sessions: *GeoAI methods for hyperspectral applications* · *Validation methods and accuracy assessment*
Companion notebooks: `20_geoai_deep_learning.ipynb`, `21_validation_accuracy_assessment.ipynb` · 20 minutes · answers in `answers/`

---

**1.** What is the key difference between a 1D-CNN and a 3D-CNN for hyperspectral classification?
- a) The 1D-CNN uses only the spectrum of each pixel; the 3D-CNN convolves jointly over the spectral and both spatial dimensions of a patch
- b) The 3D-CNN is used for elevation data only
- c) There is no difference
- d) The 1D-CNN needs RGB input

**2.** With patch-based models (e.g. 9×9 patches), why is a random pixel split between train and test especially dangerous?
- a) Random splits are slower
- b) It only matters for RF
- c) Patches are too small to learn anything
- d) Patches centred on neighbouring pixels overlap, so test patches contain pixels the model has already seen during training

**3.** What does self-supervised pretraining (as used by hyperspectral foundation models) offer?
- a) It removes the need for any validation
- b) It learns general representations from large amounts of *unlabelled* imagery, so a downstream task can be fine-tuned with far fewer labels
- c) It increases spatial resolution
- d) It guarantees transfer to any sensor without adaptation

**4.** During training the loss keeps decreasing on the training set but increases on the validation set after epoch 15. You should…
- a) train longer
- b) evaluate on the training set instead
- c) recognise overfitting: stop early (keep the epoch with the best validation score), add regularisation/augmentation or more data
- d) increase the learning rate

**5.** Your classes are 45 % water, 40 % mangrove, 10 % cropland, 5 % built-up. Which combination is most appropriate?
- a) Report only overall accuracy
- b) Remove the small classes
- c) Use class weights or balanced sampling during training, and report per-class F1 and macro-F1
- d) Duplicate the test set

**6.** In an error matrix with map classes as rows and reference classes as columns, *user's accuracy* for class k is…
- a) kappa for class k
- b) correct_k / map total_k (= precision; 1 − commission error)
- c) correct_k / reference total_k (= recall; 1 − omission error)
- d) the overall accuracy

**7.** Why do Pontius & Millones (2011) and Olofsson et al. (2014) discourage relying on Cohen's kappa?
- a) Kappa is always higher than OA
- b) Its "chance agreement" baseline is not a meaningful reference for map accuracy; it adds no information beyond the error matrix and can mislead comparisons. Report OA, user's/producer's accuracy and area-adjusted estimates instead
- c) Kappa only works for two classes
- d) Kappa is hard to compute

**8.** Counting mapped pixels gives 1 200 ha of mangrove. Why do Olofsson et al. (2014) recommend an area-adjusted estimate?
- a) Because hectares must be converted to km²
- b) Because the map is projected
- c) Pixel counting ignores classification errors; commission and omission errors bias the area. Combining a stratified reference sample with the error matrix gives an unbiased area estimate *with a confidence interval*
- d) Pixel counts are always too low

**9.** IoU (intersection over union) for a class is…
- a) TP / (TP + FN)
- b) TP / (TP + FP + FN)
- c) 2TP / (2TP + FP + FN)
- d) (TP + TN) / N

**10.** A chlorophyll model has R² = 0.92 but a bias of +8 µg/L. What does this tell you?
- a) The model is perfect
- b) It captures the pattern (high correlation) but systematically overestimates. R² alone hides bias, so always report bias and RMSE, and look at a scatter/Bland-Altman plot
- c) R² and bias cannot both be reported
- d) The bias is caused by too many bands

**11.** The maximum softmax probability of a CNN is 0.97 for a pixel. Which statement is correct?
- a) It cannot be mapped
- b) It equals the user's accuracy
- c) The pixel is correctly classified with 97 % certainty
- d) It is a model confidence score, often over-confident and not calibrated; it is useful for ranking and for flagging low-confidence areas, but should be checked against reference data

**12.** A model trained on El Salvador mangroves performs poorly on UAE mangroves (*Avicennia marina*). This is an example of…
- a) a bug in the code
- b) domain shift: different species, background, atmosphere and illumination change the spectra. You need local labels, domain adaptation or more diverse training data
- c) the Hughes phenomenon
- d) overfitting to noise only

---

### Short answers

**13.** Describe a validation design (reference data, sampling, split, metrics) for a mangrove-extent map of a
coastal region, in 5–6 sentences.

**14.** Your teammate says "our CNN has 98 % accuracy, so we don't need a random-forest baseline." Give two reasons
why the baseline is still important.
