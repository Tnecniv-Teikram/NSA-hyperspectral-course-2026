# Quiz W1b — Preprocessing concepts for hyperspectral data

**Space Academy 2026 · Hyperspectral course · Week 1**
Session: *Preprocessing concepts for hyperspectral data*
Companion notebook: `11_preprocessing.ipynb` · 15 minutes · answers in `answers/`

---

**1.** The main purpose of atmospheric correction is to…
- a) correct terrain displacement
- b) remove clouds from the image
- c) increase spatial resolution
- d) convert at-sensor radiance to surface reflectance by accounting for gas absorption and scattering by molecules and aerosols

**2.** Why do we remove the bands at ~1340–1445 nm and ~1790–1970 nm?
- a) Atmospheric water vapour absorbs almost all light there, so little or no surface signal reaches the sensor
- b) They contain the chlorophyll absorption
- c) These bands are redundant with the visible bands
- d) The detector is switched off there

**3.** Around 20–30 % of every Tanager ortho grid is flagged "no-data". The main reason is:
- a) water pixels are always removed
- b) the sensor fails for a third of the pixels
- c) permanent cloud cover
- d) the image swath is rotated inside the north-up map grid after orthorectification, leaving empty corners

**4.** In the Al Dhafra (UAE) scene the cloud mask flags ~40 % of pixels although the sky is clear. The most likely cause and the correct response are:
- a) haze; delete the scene
- b) sensor saturation; apply a stronger cloud mask
- c) a download error; download again
- d) very bright sabkha/salt surfaces confused with cloud; inspect the flagged spectra (mineral and water absorption features, no cloud-like shape) and decide whether to use `cloud=False` for that area

**5.** A water pixel shows slightly negative reflectance (−0.003) at 2200 nm. What is the best interpretation?
- a) The data are corrupt; set the pixel to NaN
- b) The water is emitting light
- c) Water absorbs almost all SWIR light; after atmospheric correction the true value is ≈0 and noise or small correction errors make it slightly negative. Keep it (or clip at 0) rather than discarding water pixels
- d) It is a cloud shadow

**6.** Compared with a simple moving average, a Savitzky-Golay filter…
- a) fits a local polynomial and preserves the position and depth of absorption features better, but too large a window still smooths away narrow features
- b) works only on images, not spectra
- c) removes all noise without side effects
- d) increases the number of bands

**7.** Continuum removal divides a spectrum by its upper convex hull. Why is this useful?
- a) It isolates absorption features, so their depth and shape can be compared between bright and dark materials
- b) It removes clouds
- c) It converts radiance to reflectance
- d) It removes the atmosphere

**8.** The Tanager SR file contains `surface_reflectance_uncertainty`. A simple per-band SNR estimate is…
- a) reflectance / uncertainty
- b) reflectance − uncertainty
- c) the FWHM divided by the wavelength
- d) uncertainty / reflectance

**9.** What is orthorectification?
- a) Removing geometric distortions from terrain relief and viewing geometry (using a DEM and the sensor model) so that pixels line up with a map grid
- b) Sharpening the image with a panchromatic band
- c) Removing bad bands
- d) Converting digital numbers to radiance

**10.** You read a full scene with `stride=4`. Which statement is true?
- a) It is identical to the full-resolution read
- b) The result is a 4× downsampled preview (every 4th row and column), which is fine for quicklooks but not for pixel-level statistics of small features
- c) The spectral resolution is reduced 4×
- d) It averages 4×4 blocks

**11.** In the core of the water-vapour windows, the bands flagged as bad by `good_wavelengths` contain a constant value of about −0.01 in every pixel. What does that mean for analysis?
- a) They should be replaced by interpolation and kept for classification
- b) They are placeholders, not measurements; always drop these bands before computing statistics, PCA or classifications
- c) They show the atmosphere is very clean
- d) These are valid low reflectances; keep them

---

### Short answers

**12.** List, in order, the preprocessing steps you would apply before training a classifier on a Tanager scene, and say
in one line for each step why it is needed.

**13.** Name two situations in which you would **not** want to smooth spectra before analysis.
