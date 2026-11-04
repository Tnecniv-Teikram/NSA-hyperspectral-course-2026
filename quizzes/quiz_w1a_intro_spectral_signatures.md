# Quiz W1a — Hyperspectral Earth observation, spectral signatures and sensor concepts

**Space Academy 2026 · Hyperspectral course · Week 1**
Sessions: *Introduction to hyperspectral Earth observation* · *Spectral signatures, sensor concepts, and hyperspectral use cases*
Companion notebook: `10_spectral_signatures_and_libraries.ipynb` · 15 minutes · answers in `answers/`

---

**1.** What best distinguishes a *hyperspectral* sensor from a *multispectral* one?
- a) It measures emitted thermal radiation
- b) It records many narrow, contiguous bands, so each pixel has a near-continuous spectrum
- c) It has a finer spatial resolution
- d) It has more than 20 bands

**2.** Tanager-1 records approximately…
- a) 4 bands, visible and NIR, 3 m
- b) 224 bands, 420–2450 nm, 30 m
- c) 13 bands, 443–2190 nm, 10–60 m
- d) 426 bands, ~380–2500 nm at ~5 nm sampling, ~30 m

**3.** Healthy leaves are dark in the red (~670 nm) and bright in the near-infrared (~850 nm) because…
- a) chlorophyll absorbs red light, and the internal leaf structure (mesophyll cell walls and air spaces) scatters NIR
- b) leaves emit NIR radiation
- c) water absorbs red light and chlorophyll reflects NIR
- d) the atmosphere absorbs red light

**4.** As a crop's chlorophyll content increases, the red-edge position (the inflection point between ~690 and 750 nm)…
- a) shifts to longer wavelengths
- b) disappears
- c) does not move; only the NIR plateau rises
- d) shifts to shorter wavelengths

**5.** Which set lists absorption features of **liquid water** in vegetation and soils?
- a) ~970, ~1200, ~1450, ~1940 nm
- b) 760 nm only
- c) 2200 and 2340 nm only
- d) 450, 550, 650 nm

**6.** Match each mineral group to its diagnostic feature: (i) Al-OH clays (kaolinite, montmorillonite), (ii) carbonates (calcite, dolomite), (iii) iron oxides (hematite, goethite).
- a) All three are identified only by overall brightness
- b) (i) ~2200 nm · (ii) ~2340 nm · (iii) ~900 nm and a steep visible slope
- c) (i) ~680 nm · (ii) ~970 nm · (iii) ~2200 nm
- d) (i) ~2340 nm · (ii) ~2200 nm · (iii) ~1450 nm

**7.** A band has a centre of 2200 nm and a FWHM of 6 nm; the next band is centred at 2205 nm. Which statement is correct?
- a) Neighbouring bands never overlap
- b) FWHM is the spatial resolution in metres
- c) Spectral sampling is the spacing between band centres (5 nm); spectral resolution is the width of each band's response (6 nm FWHM)
- d) Spectral sampling (5 nm) and spectral resolution (6 nm FWHM) are the same thing

**8.** A 30 m Tanager pixel covering half mangrove and half open water will most likely record…
- a) the mangrove spectrum, because vegetation dominates
- b) approximately the area-weighted mix of both spectra (linear mixing)
- c) the water spectrum, because water is darker
- d) random noise

**9.** Radiance vs reflectance: which statement is correct?
- a) Both are unitless
- b) At-sensor radiance has units (W m⁻² sr⁻¹ µm⁻¹) and includes atmospheric effects; surface reflectance is a unitless ratio describing the surface
- c) Reflectance can only be measured in the laboratory
- d) Reflectance depends on the sun angle, radiance does not

**10.** Why is the signal-to-noise ratio lower in some bands (e.g. < 400 nm, > 2450 nm and in atmospheric absorption bands)?
- a) The pixels are larger at those wavelengths
- b) Less light reaches the sensor there (low solar irradiance, atmospheric absorption, detector edge sensitivity)
- c) These bands have a larger FWHM
- d) The sensor deliberately adds noise there

**11.** Which task really *requires* hyperspectral data rather than Sentinel-2?
- a) Mapping green vegetation extent with NDVI
- b) Producing a true-colour image
- c) Detecting open water with NDWI
- d) Discriminating kaolinite from montmorillonite by the shape of the ~2200 nm feature

**12.** Methane is detectable from space with imaging spectrometers mainly through absorption in…
- a) the SWIR, especially around 2300 nm (and weaker near 1650 nm)
- b) thermal infrared only (Tanager can therefore not see it)
- c) the red edge
- d) the visible blue

**13.** Burned vegetation typically shows, compared to healthy vegetation…
- a) identical spectra; burns are only visible in thermal
- b) lower NIR and higher SWIR reflectance, which is why NBR = (NIR − SWIR)/(NIR + SWIR) drops
- c) a stronger chlorophyll absorption at 680 nm
- d) higher NIR and lower SWIR reflectance

---

### Short answers (3–4 sentences each)

**14.** Sentinel-2 band 12 is centred at ~2202 nm with a ~175 nm bandwidth. Explain why it cannot tell a clay-rich soil
from a carbonate-rich soil, while Tanager can.

**15.** Pick one challenge theme (agriculture, land cover, GHG, disasters, blue carbon, water quality). Name one
spectral feature (with wavelength) that hyperspectral data resolves and explain how it improves the application.
