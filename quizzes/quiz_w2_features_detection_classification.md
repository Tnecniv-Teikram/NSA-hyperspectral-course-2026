# Quiz W2 — Feature extraction, material discrimination, target detection and classification

**Space Academy 2026 · Hyperspectral course · Week 2**
Sessions: *Feature extraction and dimensionality reduction* · *Material discrimination and target detection* · *Classification approaches for hyperspectral data*
Companion notebooks: `13_…`, `14_…`, `15_…` · 20 minutes · answers in `answers/`

---

**1.** The *Hughes phenomenon* ("curse of dimensionality") states that, for a fixed number of training samples…
- a) accuracy first increases and then decreases as more bands are added, because the model has too many parameters to estimate reliably
- b) accuracy always increases with the number of bands
- c) only deep learning suffers from it
- d) the number of bands has no influence

**2.** PCA and MNF both produce ordered components. The difference is that…
- a) MNF works only on multispectral data
- b) PCA orders by variance; MNF orders by signal-to-noise ratio after whitening the noise, so noisy bands do not dominate the first components
- c) MNF orders by variance; PCA by SNR
- d) They are identical for hyperspectral data

**3.** Why might you prefer *band selection* over PCA for a project that must be explained to agronomists?
- a) PCA cannot be computed on reflectance
- b) Band selection is always more accurate
- c) Selected bands keep their physical meaning (e.g. 705 nm red edge), which makes the model interpretable
- d) Band selection removes noise better

**4.** A key property of the Spectral Angle Mapper (SAM) is that it is…
- a) able to estimate sub-pixel fractions
- b) only usable with 3 bands
- c) insensitive to multiplicative brightness changes (e.g. illumination or topographic shading), because it compares the shape (direction) of the spectrum vector
- d) sensitive to overall brightness

**5.** The matched filter (MF) and ACE detectors need…
- a) only the target spectrum
- b) a DEM
- c) the target spectrum and the background mean and covariance (estimated from the image)
- d) training labels for every class

**6.** In a target-implantation experiment you mix the target into real background pixels at 5 %, 10 %, 20 % … fractions. What do you learn?
- a) The detector's detection rate vs false-alarm rate as a function of sub-pixel target fraction, i.e. how small a target it can find
- b) The spatial resolution of the sensor
- c) Nothing, because implanted targets are synthetic
- d) The atmospheric correction accuracy

**7.** The fully constrained linear mixing model assumes each pixel spectrum is…
- a) a non-negative, sum-to-one weighted sum of endmember spectra plus noise
- b) a product of endmember spectra
- c) independent of the endmembers
- d) the brightest endmember

**8.** When is the linear mixing assumption most likely violated?
- a) Intimate mixtures such as mineral grains in sand, or multiple scattering inside a vegetation canopy
- b) Never
- c) A pixel that is half water, half beach
- d) A pixel that is half asphalt roof, half grass lawn (side by side)

**9.** N-FINDR extracts endmembers by…
- a) clustering the image with k-means
- b) taking the darkest and brightest pixels
- c) using a spectral library only
- d) searching for the set of pixels that spans the simplex with the largest volume in (reduced) spectral space

**10.** k-means on a hyperspectral image produces…
- a) spectral clusters without names; you still have to interpret or match them to classes, and one class may split into several clusters (e.g. shaded and sunlit)
- b) labelled land-cover classes
- c) a validated map
- d) endmember abundances

**11.** You train an RF on randomly selected pixels and test on other random pixels from the same fields and get 99 % accuracy. On a new area you get 75 %. The most likely reason is:
- a) the new area has a different number of bands
- b) RF does not work on hyperspectral data
- c) the RF has too few trees
- d) spatial autocorrelation: neighbouring, near-identical pixels were in both training and test sets, so the test was not independent

**12.** RF feature importance on hyperspectral data is often "smeared" over many neighbouring bands. Why?
- a) It is a bug
- b) Neighbouring bands are highly correlated, so the importance is shared between interchangeable bands
- c) RF ignores the red edge
- d) The bands are not sorted

**13.** Which classifier is a sensible, strong first baseline for pixel-based hyperspectral classification with a few thousand labelled pixels?
- a) k-means
- b) Random forest or an RBF-SVM on standardised spectra (or on PCA/MNF features)
- c) A 50-layer CNN trained from scratch
- d) Thresholding a single band

---

### Short answers

**14.** Explain why the Cellulose Absorption Index (CAI, based on 2000, 2100 and 2200 nm) cannot be computed with
Sentinel-2, and name an application where it matters.

**15.** You must find small, bright industrial roofs in a city. Would you use SAM, a matched filter/ACE, or a
classifier? Justify your choice in 3–4 sentences, including how you would choose the detection threshold.
