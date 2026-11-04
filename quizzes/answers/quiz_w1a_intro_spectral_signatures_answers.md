# Answer key — Quiz W1a — Hyperspectral Earth observation, spectral signatures and sensor concepts

*Instructor copy. Do not distribute to students before the quiz.*

| # | Answer | Why |
|---|:---:|-----|
| 1 | **b** | Hyperspectral = many narrow *contiguous* bands giving a near-continuous spectrum; band count alone is not the definition. |
| 2 | **d** | Tanager-1: 426 bands, ~380–2500 nm, ~5 nm sampling, ~30 m GSD. (224 bands/420–2450 nm describes EnMAP; 13 bands is Sentinel-2.) |
| 3 | **a** | Chlorophyll a/b absorb strongly in blue and red; multiple scattering at cell wall–air interfaces in the mesophyll makes the NIR plateau bright. |
| 4 | **a** | More chlorophyll broadens the red absorption well, pushing the red-edge inflection to longer wavelengths (the 'red shift'). |
| 5 | **a** | Liquid-water overtone/combination bands: ~970, ~1200, ~1450, ~1940 nm. The last two coincide with atmospheric water-vapour windows. |
| 6 | **b** | Al-OH ~2200 nm, carbonate (CO3) ~2340 nm, Fe3+ crystal-field ~850–950 nm plus charge-transfer absorption in the blue/green. |
| 7 | **c** | Sampling = spacing of band centres; resolution = width (FWHM) of each spectral response function. With FWHM > sampling, neighbouring bands overlap. |
| 8 | **b** | At the pixel scale, side-by-side materials mix approximately linearly by area fraction (the basis of linear unmixing). |
| 9 | **b** | Radiance is a physical at-sensor quantity with units that includes the atmosphere; reflectance is a unitless surface property. |
| 10 | **b** | Little signal (low solar irradiance, strong atmospheric absorption, detector-edge response) gives low SNR. |
| 11 | **d** | Distinguishing clay species needs the shape/position of the ~2160–2210 nm doublet, resolvable only with narrow contiguous SWIR bands. |
| 12 | **a** | CH4 has strong absorption near 2300 nm (and around 1650 nm); retrievals use imaging-spectrometer SWIR radiance. |
| 13 | **b** | Fire removes leaf structure and water: NIR drops, SWIR rises (char, ash, exposed soil), so NBR decreases. |

## Model answers for the short questions

**14.** The clay Al-OH feature (~2160–2210 nm) and the carbonate feature (~2330–2345 nm) both fall inside, or at the edge of, one ~175 nm wide band, which averages them into a single number. Brightness differences from moisture or organic matter dominate that number. Tanager samples the region every ~5 nm, so the position, depth and shape of each absorption can be measured (e.g. with continuum removal or band depth).

**15.** Any well-argued feature, e.g. the red-edge position (700–750 nm) for chlorophyll/N stress before visible symptoms; cellulose/lignin at ~2100 nm for crop residue; the CH4 absorption near 2300 nm for plumes; phycocyanin at ~620 nm and chlorophyll-a at ~665/709 nm for algal blooms; the 2200/2340 nm features for soil and mineral mapping; and char/ash SWIR behaviour for burn severity.
