"""Week 1 · Session 5 — Preprocessing concepts for hyperspectral data."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from deckbuild import Deck  # noqa: E402

d = Deck("Preprocessing concepts for hyperspectral data",
         "Week 1 · Session 5",
         notebook="11_preprocessing.ipynb",
         subtitle="Which pixels and which bands deserve your trust",
         week="Week 1 · 9–12 November 2026")

d.objectives([
    "Place a product on the chain radiance → TOA reflectance → surface reflectance",
    "Explain what atmospheric correction removes, and what it leaves behind",
    "Inspect quality masks critically, and build your own test when they fail",
    "Justify which bands you drop, using the flag, the SNR and residual features",
    "Apply smoothing, continuum removal and brightness normalisation without damaging the signal",
    "Cut, subset and export data so your project runs fast and travels well",
], notes="Frame the session: this is the least glamorous and most consequential part of the course. "
         "Every wrong map later in the project can usually be traced back to a decision made here. "
         "Ask how many students have ever inspected a cloud mask rather than simply applying it.")

d.section("1. Processing levels", "From photons at the sensor to reflectance of the ground")

d.table("What the number in the file means", ["Level", "Quantity", "What has been done", "Tanager asset"], [
    ["Radiance", "L(λ), W m⁻² sr⁻¹ µm⁻¹", "calibrated counts, as seen at the satellite", "ortho_radiance_hdf5"],
    ["TOA reflectance", "ρ_TOA, 0–1", "radiance ÷ incoming sunlight", "computed by the user"],
    ["Surface reflectance", "ρ_s, 0–1", "atmospheric absorption and scattering removed", "ortho_sr_hdf5"],
], col_widths=[1.1, 1.3, 2.2, 1.4], kicker="processing levels",
   notes="ρ_TOA = π L d² / (E_sun cos θ_s). Stress that only surface reflectance is comparable between dates, "
         "places and sensors — and that gas retrievals such as methane deliberately work on radiance instead.")

d.bullets("Basic or ortho?", [
    "**Basic** products stay in the sensor's viewing geometry; a separate geolocation array gives each pixel's lon/lat",
    "**Ortho** products are terrain-corrected and resampled onto a map grid — UTM, 30 m for Tanager",
    "Orthorectification uses a DEM and the sensor model to remove relief and viewing distortions",
    "Use ortho unless you have a reason not to, such as avoiding resampling before a physics retrieval",
    ("The rotated swath inside a north-up grid is why 20–30 % of every scene is no-data", 1),
], kicker="product variants",
   notes="Connect the no-data corners to something they have already seen in the quicklooks. "
         "A common beginner error is to compute statistics over the whole grid including those corners.")

d.bullets("What the atmosphere does to your signal", [
    "**Absorbs**: water vapour (940, 1130, 1380, 1880 nm), O₂ (760 nm), CO₂ (2010, 2060 nm), CH₄ (2300 nm)",
    "**Scatters**: molecules (Rayleigh, strongest in the blue) and aerosols — haze, dust, smoke",
    "Scattering adds *path radiance*: light that never touched the ground but reaches the sensor",
    "Radiative-transfer codes (MODTRAN, 6S, the open-source ISOFIT used for EMIT) model both effects",
    "They need per-pixel **column water vapour** and **aerosol optical depth** — Tanager ships both as layers",
], kicker="absorption and scattering",
   notes="Point out that the same water-vapour bands we must discard are the bands the correction uses to "
         "retrieve water vapour. The instrument measures the atmosphere in order to remove it.")

d.figure("The atmosphere varies inside a single scene",
         "11_preprocessing/00_1_processing_levels_from_photons_to_surf.png",
         caption="Al Dhafra, UAE — true colour, column water vapour (1.21–2.16 g/cm²), aerosol optical depth (0.12–0.54)",
         kicker="why correction is per-pixel",
         notes="Ask the room what is wrong with the water-vapour map before you say it: it changes abruptly at "
               "the coastline, which the real atmosphere does not do. Dark water returns almost no signal in the "
               "retrieval bands, so the retrieval behaves differently there.")

d.bullets("Read the ancillary layers critically", [
    "The water-vapour map jumps at the **coastline** — an artefact of the retrieval over dark water, not weather",
    "The highest AOD sits over the **brightest sabkha**, where separating aerosol from surface is hardest",
    "These layers are retrievals with their own errors, not ground truth",
    "Use them as **quality covariates**: is my anomaly correlated with AOD, or does it follow the coastline?",
], kicker="quality covariates",
   notes="This is a transferable habit: whenever a map surprises you, ask whether it follows a physical gradient "
         "or an artefact boundary such as a coastline, a swath edge or a tile seam.")

d.figure_bullets("Did the correction work?",
                 "11_preprocessing/01_1_processing_levels_from_photons_to_surf.png",
                 ["Test: the residual depth of the 1130 nm water-vapour feature should not track column water vapour",
                  "Over UAE land the correlation is essentially flat",
                  "Median residual depth is **0.030** — small, but systematic",
                  "You will see small dips near 940 and 1130 nm in almost every spectrum",
                  "**Do not** interpret them as surface features"],
                 caption="Residual 1130 nm band depth vs column water vapour, UAE land pixels",
                 kicker="a sanity check you can run",
                 notes="This is a good example of validating a processing step you did not perform yourself. "
                       "If the residual depth grew with water vapour, the correction would have left water-vapour "
                       "signal behind and any narrow-band index near 1130 nm would be contaminated.")

d.section("2. Quality masks", "Inspect before you trust")

d.callout("A mask is somebody else's classification of your data.",
          "Tanager's cloud and cirrus masks are labelled *beta*. On the Al Dhafra scene, a cloud-free day, the "
          "cloud mask flags 40 % of the grid — and 97 % of the bare land.",
          kicker="the lesson of this session",
          notes="Say plainly: a mask is a model output with its own errors. Applying it blindly is the same "
                "mistake as trusting a classifier without validation, which is the subject of week 3.")

d.table("The three quality layers in every Tanager file", ["Layer", "Meaning"], [
    ["nodata_pixels", "outside the imaged footprint — the rotated strip leaves 20–30 % of the grid empty"],
    ["beta_cloud_mask", "cloud, from Planet's beta cloud classifier"],
    ["beta_cirrus_mask", "thin high cirrus"],
], col_widths=[1, 3], kicker="what you get",
   notes="hu.TanagerScene.valid_mask() combines all three, and read_cube applies it by default. "
         "The cloud=False argument turns off the cloud and cirrus part when you have decided not to trust it.")

d.figure_bullets("False positives: bright ground read as cloud",
                 "11_preprocessing/02_2_quality_masks_inspect_before_you_trust.png",
                 ["Al Dhafra, 11 May 2025 — a clear scene",
                  "**97.1 %** of bare/sparse vegetation flagged as cloud",
                  "**63.2 %** of built-up, but only **2.2 %** of water",
                  "Bright white surfaces are the classic failure mode of cloud detectors",
                  "Blind use would delete half the land in the scene"],
                 caption="True colour · beta cloud mask · ESA WorldCover classes",
                 kicker="Al Dhafra, UAE",
                 notes="Note this is not unique to the UAE scene: in the Tanager catalogue, Riyadh is listed at "
                       "74 % cloud, Al Mahrah in Yemen at 53 % and Al Dhafra at 51 % — all three thumbnails are clear. "
                       "A hard filter of max 20 % cloud would discard the only scenes over Saudi Arabia, Yemen and the UAE.")

d.figure_bullets("False negatives: thin cloud the mask misses",
                 "11_preprocessing/03_2_quality_masks_inspect_before_you_trust.png",
                 ["Malibu, 15 Dec 2024 — only **36 pixels** flagged in the entire scene",
                  "Thin cloud over the ocean adds a nearly flat offset, including in the SWIR",
                  "Clear water is almost black beyond 1000 nm",
                  "Flagged sabkha, by contrast, shows real mineral structure",
                  "**Spectra let you audit a mask** pixel by pixel"],
                 caption="Thin cloud over the ocean vs clear ocean vs flagged sabkha",
                 kicker="the opposite error",
                 notes="The two errors have opposite causes but the same remedy: look at the spectra of the pixels "
                       "the mask claims are cloud, and of the pixels it claims are clear.")

d.figure_bullets("Build the test your target needs",
                 "11_preprocessing/04_2_quality_masks_inspect_before_you_trust.png",
                 ["Rule: water pixels with R(1650 nm) > 0.01 are cloud or glint",
                  "Finds **16,682** suspect water pixels where the beta mask found 36",
                  "It also catches the **surf zone** — add a coastal buffer",
                  "And a faint vertical **detector stripe** from the pushbroom array",
                  "Artefacts are only visible over uniform, dark surfaces"],
                 caption="Custom SWIR cloud/glint test on the Malibu scene",
                 kicker="ten lines of code",
                 notes="The detector stripe is worth dwelling on: each image column is recorded by a different "
                       "detector element, so a slightly miscalibrated element leaves a permanent stripe. "
                       "This is also why destriping exists as a preprocessing step for other sensors.")

d.bullets("Your masking decision, written down", [
    "Use the masks as delivered (`cloud=True`) when they are right for your scene",
    "Ignore them (`cloud=False`) when they fail — as in the UAE sabkha scene",
    "Or build a target-specific rule, like the SWIR water test, and document it",
    "**Always** overlay the mask on an RGB image before deciding",
    "Record the decision and the reason in your project report — a reviewer will ask",
], kicker="what to do about it",
   notes="Tie this to the QA checklist (templates/interim_qa_checklist.md), item B2, which asks exactly "
         "this question. Students who skip it lose marks under Validity in the rubric.")

d.section("3. Bad bands", "Which of the 426 bands carry information?")

d.figure_bullets("The flag and the placeholders",
                 "11_preprocessing/05_3_1_the_good_wavelengths_flag_and_placeh.png",
                 ["The file carries a per-band `good_wavelengths` flag: 0 = unusable",
                  "58 bands are flagged, in the deep water-vapour windows",
                  "In the core of those ranges the file stores a constant **−0.01**, not a measurement",
                  "44 of the 58 flagged bands hold that placeholder",
                  "Edge bands look plausible but are unreliable"],
                 caption="A Konya crop pixel: all 426 bands, the flagged bands, and the 352 bands we keep",
                 kicker="1340–1440 nm and 1780–1970 nm",
                 notes="Emphasise that a placeholder is not a small number — it is not a number at all. "
                       "Leaving them in silently corrupts every mean spectrum, PCA and classifier.")

d.figure_bullets("Signal-to-noise decides the ends of the spectrum",
                 "11_preprocessing/06_3_2_signal_to_noise_per_band.png",
                 ["SNR per band = reflectance ÷ the file's uncertainty layer",
                  "Below 400 nm the SNR runs **1.9, 3.8, 5.4, 7.5, 9.3** — unusable",
                  "Little UV reaches the ground and Rayleigh scattering is strongest there",
                  "Beyond 2450 nm the window closes and edge detectors are least reliable",
                  "SNR also collapses at the edges of the water-vapour windows"],
                 caption="Median SNR over bright land, Konya",
                 kicker="reading the uncertainty layer",
                 notes="This is the evidence behind hu.MIN_WL_NM = 400 and hu.SWIR_EDGE_NM = 2450. "
                       "Make the point that these are defaults derived from data, not conventions to be copied blindly: "
                       "for water work you may cut everything beyond about 1000 nm instead.")

d.bullets("The three cuts applied by `bands=\"good\"`", [
    "The two **water-vapour windows**, slightly wider than the file flag: 1340–1445 and 1790–1970 nm",
    "Everything **below 400 nm** — SNR under 10",
    "Everything **above 2450 nm** — erratic spectra at the detector edge",
    "426 bands in, **352 bands** out",
    ("Add your own ranges with `extra_bad=((1440, 1490), (1995, 2020))` for water studies", 1),
], kicker="hu.good_band_mask",
   notes="Ask: why keep a band that is noisy rather than wrong? Because classifiers can down-weight noise, "
         "but nothing can recover a placeholder. Quiz W1b question 11 tests exactly this.")

d.figure("What the correction left behind",
         "11_preprocessing/07_3_3_residual_atmospheric_features.png",
         caption="UAE desert, continuum-removed median spectrum — narrow dips at gas absorption bands are residuals",
         kicker="residual atmospheric features",
         notes="Walk the line: the O₂ dip at 760 nm and the H₂O dip at 1130 nm are residuals; the 940 nm dip mixes "
               "residual with the real iron-oxide band of the sand; the broad feature beyond 2300 nm is real carbonate. "
               "If a residual sits on your index, move the index bands or extend extra_bad.")

d.section("4. Noise, smoothing and features", "Improving the signal without inventing it")

d.figure_bullets("Two independent noise estimates",
                 "11_preprocessing/08_4_how_noisy_are_the_data_two_noise_estim.png",
                 ["**Uncertainty layer**: the provider's per-band estimate",
                  "**Shift difference**: σ ≈ 1.4826 · MAD(xᵢ₊₁ − xᵢ) / √2 over a homogeneous patch",
                  "Over open ocean the two agree — noise ≈ 0.0002 reflectance",
                  "Over desert they agree within about a factor of two",
                  "Over fields and sediment plumes the shift estimate is several times larger"],
                 caption="Four targets, two estimators",
                 kicker="how noisy are the data?",
                 notes="The discrepancy over textured targets is the point: the shift-difference estimator counts "
                       "real spatial variation as noise. Never estimate noise on a textured area. "
                       "MNF in notebook 13 uses this same shift-difference idea, which is why it needs care.")

d.bullets("Savitzky-Golay smoothing, done correctly", [
    "Fits a low-order polynomial in a moving window along the spectrum (Savitzky & Golay, 1964)",
    "Keeps feature position and depth better than a moving average",
    "**Trap 1:** never smooth across a removed gap — 1335 and 1450 nm are not neighbours",
    "**Trap 2:** `savgol_filter` fails on NaN, so masked pixels need temporary filling",
    "With ~5 nm sampling, windows of 5–11 bands (25–55 nm) are sensible",
    "Choose the **smallest** window that gives stable results",
], kicker="scipy.signal.savgol_filter",
   notes="Derivative products such as red-edge position benefit most, because differentiation amplifies noise. "
         "The notebook's savgol_segments() handles both traps; students should reuse it rather than rewrite it.")

d.bullets("When not to smooth", [
    "When **narrow features are the signal**: mineral doublets, gas absorption for methane retrieval",
    "Before **noise-dependent methods**: MNF, matched filters, covariance estimation — smoothing changes the noise",
    "When comparing with **lab spectra** convolved to the sensor response",
    "Smoothing is a modelling choice: state the window and order in your report",
], kicker="a deliberate decision",
   notes="Quiz W1b question 13 asks for two of these. The general principle: any operation that assumes a noise "
         "model must see the noise you actually have.")

d.figure_bullets("From spectrum to map: band depth",
                 "11_preprocessing/10_5_2_band_depth_maps.png",
                 ["Continuum removal makes absorption depths comparable between bright and dark materials",
                  "Applied per pixel, a band depth becomes a **mineral map**",
                  "Al–OH depth at 2205 nm over the Korba coalfield",
                  "Pit walls and clay-rich overburden light up; fields and forest stay dark",
                  "Smoothing changes map noise only modestly here: 0.0140 → 0.0123"],
                 caption="Korba coalfield — true colour, Al–OH depth raw, Al–OH depth smoothed",
                 kicker="continuum removal at scale",
                 notes="Tanager's SNR is high over these bright surfaces, so much of the pixel-to-pixel variation "
                       "is real. Smoothing matters far more for dark targets, weak features and derivatives.")

d.section("5. Water, geometry and space", "Three practical decisions")

d.figure_bullets("Negative reflectance is not a bug to delete",
                 "11_preprocessing/11_6_negative_reflectances_over_water.png",
                 ["Clear ocean, Malibu: **28 bands** have more than 10 % negative values",
                  "Worst at 1448, 1468, 2449 and 2012 nm — absorption-window edges",
                  "Setting negatives to NaN: complete water spectra fall from **100 % to 0 %**",
                  "It also **biases** means upward: −0.0019 becomes +0.0016 at 2012 nm",
                  "Keep them, or drop the offending bands; clip to zero only for display"],
                 caption="Share of negative reflectances per band over clear ocean",
                 kicker="the most common beginner mistake",
                 notes="The physics: water-leaving reflectance in the SWIR is essentially zero, so the measurement "
                       "is noise around zero plus a small correction error. Noise is symmetric — keeping it "
                       "keeps averages unbiased. Truncating one half of a symmetric distribution is a bias machine.")

d.figure_bullets("Illumination changes brightness, and a little of the shape",
                 "11_preprocessing/13_7_illumination_and_viewing_geometry.png",
                 ["Malibu in December: sun zenith ≈ 58.6°, strong topographic shading",
                  "Sunlit vs shaded chaparral of similar greenness differ **6.7×** in NIR brightness",
                  "Vector normalisation ρ/‖ρ‖₂ cuts Euclidean distance from 3.73 to 0.16",
                  "The **spectral angle stays 9.3°** — SAM is invariant to brightness by construction",
                  "Shaded slopes are lit by bluer diffuse skylight, so shape changes slightly too"],
                 caption="Shaded and sunlit chaparral, raw and vector-normalised",
                 kicker="brightness normalisation",
                 notes="This slide previews week 2: SAM's brightness invariance is exactly why it is the workhorse "
                       "of spectral matching. Full topographic correction needs a DEM and is beyond this course.")

d.figure("Cut it down: preview, window, subset, export",
         "11_preprocessing/14_8_spatial_preprocessing_cut_preview_shar.png",
         caption="Strided preview of the Korba scene with a 200 × 200 pixel AOI around the Kusmunda mine",
         kicker="spatial preprocessing",
         notes="Workflow habit: strided preview to find the area, then a window for the real work. "
               "Students who analyse whole scenes at full resolution spend their week waiting for cells to finish.")

d.bullets("Subset, export, reproject", [
    "`hu.write_subset` stores a window as int16 × 10 000: **7.4 MB** against a **1.23 GB** scene",
    "Round-trip difference is 5 × 10⁻⁵ reflectance, and the georeferencing is identical",
    "Export results as a **Cloud-Optimised GeoTIFF** with band names — QGIS and web maps read it directly",
    "Reprojection **resamples**: analyse on the native grid, reproject only final products",
    ("Nearest neighbour for class maps, bilinear for continuous values", 1),
], kicker="sharing your work",
   notes="The subset trick is how you send data to a teammate or run an exercise in a session with poor "
         "connectivity. tools/make_subsets.py does this for all course scenes at once.")

d.code("The whole chain, as one reusable function", """
def preprocess(scene, window=None, stride=1, use_cloud_mask=True,
               extra_bad=(), smooth_window=0, normalize=None):
    # use_cloud_mask : apply beta cloud/cirrus masks — inspect them first
    # extra_bad      : extra (start, stop) nm ranges to drop, e.g. for water
    # smooth_window  : Savitzky-Golay window in bands (0 = none)
    # normalize      : None, "vector" or "brightness"
    ...
    return cube, wavelengths, valid, report
""", kicker="notebook 11, section 9",
   caption="The report dictionary records every choice, ready to paste into your method section.",
   notes="Tell them to copy this into their project and keep the report dict — it is half of the "
         "provenance record that week 2 will formalise as a JSON sidecar.")

d.handover("11_preprocessing.ipynb", [
    "Compare the cloud mask with WorldCover over the UAE scene and quantify the false positives",
    "Build the SWIR water test on the Malibu scene and find the detector stripe",
    "Plot per-band SNR and justify where you would cut the spectrum for your own theme",
    "Write a subset and export a COG, then open both again to check they are correct",
], minutes=120,
   notes="Circulate during the mask section — that is where the discussion is richest. "
         "Ask each student which masking decision they will make for their project scene, and why.")

d.recap([
    "Know your level: **surface reflectance** for analysis, radiance for gas retrievals",
    "Atmospheric correction leaves **residuals** near 760, 940, 1130 and 2010 nm",
    "Masks are **beta**: 97 % of UAE bare land flagged as cloud, thin cloud over Malibu missed",
    "Drop bands with evidence: the flag, the placeholders, SNR, residual features — 426 → 352",
    "Keep negative water reflectances; deleting them destroys water spectra and biases means",
    "Normalise brightness with care; smooth only when the noise, not the feature, dominates",
    "Subset early: 7.4 MB travels, 1.23 GB does not",
], next_up="Week 2 — Hyperspectral image processing workflows: turning these decisions into a pipeline",
   notes="Close on the mask slide: the single habit to take away is to look at the data before trusting a label. "
         "Point them to quizzes/quiz_w1b_preprocessing.md, and tell them these are the checks their mini project will be marked on.")

d.references([
    "Savitzky, A. & Golay, M.J.E. (1964). Smoothing and differentiation of data by simplified least squares procedures. Analytical Chemistry 36, 1627–1639.",
    "Clark, R.N. & Roush, T.L. (1984). Reflectance spectroscopy: quantitative analysis techniques for remote sensing applications. JGR 89, 6329–6340.",
    "Gao, B.-C., Montes, M.J., Davis, C.O. & Goetz, A.F.H. (2009). Atmospheric correction algorithms for hyperspectral remote sensing data of land and ocean. RSE 113, S17–S24.",
    "Thompson, D.R. et al. (2018). Optimal estimation for imaging spectrometer atmospheric correction (ISOFIT). RSE 216, 355–373.",
    "Green, A.A. et al. (1988). A transformation for ordering multispectral data in terms of image quality with implications for noise removal. IEEE TGRS 26, 65–74.",
    "Course material: notebook 11_preprocessing.ipynb · quizzes/quiz_w1b_preprocessing.md",
])

d.save("w1e_preprocessing.pptx")
