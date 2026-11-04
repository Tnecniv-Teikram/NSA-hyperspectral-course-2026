"""Week 4 · Session 1 — Advanced hyperspectral analytics and solution refinement."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from deckbuild import Deck  # noqa: E402

d = Deck("Advanced analytics and solution refinement",
         "Week 4 · Session 1",
         notebook="30_advanced_analytics.ipynb",
         subtitle="Two dates, one honest answer — change, uncertainty, harmonisation and scale",
         week="Week 4 · 23–26 November 2026")

d.objectives([
    "Put two acquisitions on a common grid and **co-register** them before comparing pixels",
    "Map burn severity with dNBR, and confirm a detection with the **full spectrum**",
    "Separate real change from **artefacts** using an unchanged control area",
    "Propagate **uncertainty** and say which changes are statistically meaningful",
    "Harmonise Tanager with Sentinel-2, Landsat and EnMAP, and quantify the difference",
    "Process a whole scene within a **bounded memory** budget",
    "Run a refinement loop: sensitivity → error analysis → targeted fix → measure again",
], notes="This is the session where projects get good rather than merely finished. Frame it as: everything "
         "up to now produced a result; today we ask whether the result is real, how sure we are, and whether "
         "it survives contact with another sensor and a full scene.")

d.section("1. Two dates on one grid", "Geometry before analysis")

d.callout("Change detection starts with geometry, not with indices.",
          "Two orthorectified products of the same sensor over the same place were still about one pixel "
          "apart. Subtracting them directly would have produced change along every ridge and edge.",
          kicker="the lesson of this session",
          notes="Ask how many students have subtracted two rasters without checking alignment. Most have. "
                "This slide is the reason their edges lit up.")

d.bullets("The working example: Malibu, California", [
    "**15 December 2024** — after the Franklin fire, before the January fires",
    "**23 January 2025** — after the Palisades fire burned the Santa Monica Mountains",
    "Same sensor, same CRS (EPSG:32611), same 30 m pixel size",
    "January grid offset from December by **dx = +114 px, dy = −295 px** — a whole-pixel lattice shift",
    "Overlap: **713 × 677 px = 43 443 ha**, of which 22.7 % is land valid on both dates",
    ("Because the lattices align, we can slice instead of resample — checked: max difference 0.0", 1),
], kicker="the data",
   notes="Point out the luck and the discipline: the lattices happened to align, but we verified it rather "
         "than assumed it. If they had not aligned, the notebook resamples the January bands onto the "
         "December grid with rasterio.")

d.figure_bullets("Co-registration with FFT phase correlation",
                 "30_advanced_analytics/01_2_co_registration_check_with_fft_phase_c.jpg",
                 ["Cross-correlate in the frequency domain; the peak gives the shift",
                  "Validation first: an **artificial (+3, −5) px** shift was recovered exactly",
                  "Real pair: median **dy = −0.59, dx = −0.82 px** across ten land tiles (≈ 30 m)",
                  "After sub-pixel correction the residual is **dy +0.10, dx −0.27 px**",
                  "NIR correlation between dates improves 0.669 → 0.692"],
                 caption="Phase-correlation shift estimates per tile",
                 notes="Always validate a registration method on a known shift before trusting it on real "
                       "data. A peak height of 0.14 is modest — that is why we use the median of tiles "
                       "rather than one global estimate.")

d.section("2. Mapping the change", "dNBR, severity classes and change vector analysis")

d.bullets("NBR and dNBR", [
    "NBR = (NIR − SWIR₂₂₀₀) / (NIR + SWIR₂₂₀₀) — high for healthy vegetation, low for char and ash",
    "**dNBR = NBR_pre − NBR_post**: positive where vegetation was lost",
    "Severity thresholds follow **Key & Benson (2006)**: low 0.10, moderate 0.27, high 0.44, very high 0.66",
    "dNBR measures **change between your two dates**, not the state of the landscape",
    ("The Franklin fire burned *before* the December image, so it does not appear in dNBR at all", 1),
], kicker="the index",
   notes="The Franklin point is the one students miss: your 'before' image must be before the event you "
         "care about. Ask what would happen if they had used the January image as the pre-fire scene.")

d.figure("Burn severity across the overlap",
         "30_advanced_analytics/02_3_bi_temporal_burn_mapping_with_dnbr.jpg",
         caption="dNBR and the USGS severity classes over the Santa Monica Mountains",
         kicker="the first result",
         notes="Measured areas: unburned 3 968 ha (41.4 % of land), low 2 379 ha, moderate-low 758 ha, "
               "moderate-high 983 ha, high 1 095 ha, plus small enhanced-regrowth classes. Note that 'low "
               "severity' is suspiciously large — section 6 explains why.")

d.figure_bullets("Is the new scar real? Three independent checks",
                 "30_advanced_analytics/03_4_is_the_new_burn_scar_real_checking_wit.jpg",
                 ["**The image:** unburned green in December, dark red in January false colour",
                  "**The shape:** one connected region holds 89 % of all dNBR > 0.27 pixels",
                  "**The spectrum:** the January scar matches the older Franklin scar to **1.7°**",
                  "For contrast: new scar vs stable vegetation is **31.9°** apart",
                  "Area: 28 115 px = **2 530 ha**, centred 118.637° W, 34.061° N"],
                 caption="December and January, true and false colour, with both scars outlined",
                 notes="This is the hyperspectral advantage in a nutshell: with 352 bands you can ask whether "
                       "the new thing looks like a known thing, using the whole spectrum rather than one index. "
                       "A multispectral sensor gives a much weaker version of this argument.")

d.bullets("Change vector analysis on full spectra", [
    "Treat each pixel's spectrum as a vector; change is the **difference vector** between dates",
    "**Magnitude** = how much changed · **direction** = what kind of change",
    "Burn-like = NIR down and SWIR-2 up; green-up = NIR up and SWIR-2 down",
    "Inside the new scar: **84.6 %** burn-like · outside it: only **7.0 %**",
    "Computed tiled over 713 × 677 px × 352 bands × 2 dates in **22.8 s**",
], kicker="beyond a single index",
   notes="CVA is the generalisation of dNBR: instead of collapsing to one number you keep the direction of "
         "change. That is what lets us separate a burn from a brightness shift in the next section.")

d.section("3. What the change map gets wrong", "Artefacts, control areas and offsets")

d.figure_bullets("The January image is systematically brighter",
                 "30_advanced_analytics/08_a_systematic_difference_the_january_imag.jpg",
                 ["Pick a **control area**: land that certainly did not change",
                  "Median dNBR there should be ~0. It is **+0.079**",
                  "That pushes **40 %** of unchanged control pixels into 'low severity'",
                  "82 % of land outside the scar got brighter in VIS, NIR and SWIR-2 at once",
                  "Cause: viewing geometry (7° vs 20°) and atmospheric correction, not fire"],
                 caption="Control-area spectra, December vs January",
                 image_left=True,
                 notes="A brightness change in *all* bands at once is the signature of geometry or atmosphere, "
                       "not of a surface change. This is why CVA direction matters and why we subtract a "
                       "dNBR offset estimated on unchanged land.")

d.table("Artefacts and remedies", ["Artefact", "Cause", "Remedy"], [
    ["Haze over the ocean", "Missed by the cloud mask", "Inspect imagery, add a haze test, mask water"],
    ["Diagonal stripe", "Detector column error", "Destriping; ignore thin linear features"],
    ["Cirrus-mask gaps", "Conservative flag on bright slopes", "Check what the mask removes; relax it"],
    ["Systematic brightening", "Geometry (BRDF) and atmosphere", "dNBR offset from a control area"],
    ["1–2 px misregistration", "Ortho over terrain, view angles", "Co-registration (section 1)"],
    ["Earlier burn not detected", "It burned before the first image", "Choose a true pre-event image"],
], kicker="know your failure modes",
   col_widths=[1.2, 1.3, 2],
   notes="Sun zenith was 58.6° in December against 55.9° in January, and view zenith 7.3° against 20.3°. "
         "Those differences alone change reflectance on slopes. Students should include a table like this "
         "in their project limitations slide.")

d.section("4. How sure are we?", "From sensor noise to between-date variability")

d.bullets("Two very different uncertainties", [
    "**Sensor uncertainty**: shipped per pixel and band in the Tanager product",
    "Median relative uncertainty over land: **0.42 % (NIR)**, **1.05 % (SWIR-2)**",
    "Monte Carlo through the index gives **σ(dNBR) ≈ 0.0075** — analytic propagation agrees (0.0076)",
    "**Between-date variability** measured on the control area: **σ ≈ 0.087**, more than ten times larger",
    "Atmosphere, geometry and registration dominate; sensor noise is the small term",
], kicker="the number that matters is not the one in the file",
   notes="This is the slide that changes how students report uncertainty. The instrument's own uncertainty "
         "flatters you. The honest error bar for change comes from land you know did not change.")

d.figure_bullets("What counts as a significant change",
                 "30_advanced_analytics/09_7_uncertainty_how_sure_are_we_about_each.jpg",
                 ["With sensor noise only: **91 % of land** looks 'significant' — and 85.6 % of the control area",
                  "With total σ: **35.4 % of land**, and only **10.3 %** of the control area",
                  "Significant NBR decrease with total σ: **2 941 ha**",
                  "A significance test is only as good as the σ you feed it",
                  "Report the σ you used and where it came from"],
                 caption="Monte-Carlo σ(dNBR) and the resulting significance masks",
                 notes="85.6 % of an area you know did not change being flagged as significant is the "
                       "reductio ad absurdum. Use it to make the point stick.")

d.section("5. Harmonisation and scale", "Other sensors, whole scenes")

d.bullets("Would another sensor see the same thing?", [
    "Simulate Sentinel-2, Landsat 8/9 and EnMAP by convolving Tanager with their **response functions**",
    "Compare indices pixel by pixel over 41 577 land pixels",
    "**EnMAP** is nearly identical to Tanager — similar narrow bands (NBR bias −0.0015)",
    "**Sentinel-2** NBR carries a bias of **+0.025** (RMSE 0.031); Landsat is similar (+0.026)",
    "NDVI and NDMI agree much better than NBR — wide SWIR bands are the problem",
    ("Bandpass differences alone shift indices: harmonise before mixing sensors or thresholds", 1),
], kicker="cross-sensor consistency",
   notes="Emphasise that this is a *bandpass* effect, not a calibration error: Sentinel-2's B12 is 175 nm "
         "wide and sits differently on the char spectrum. A threshold tuned on one sensor does not transfer.")

d.table("Same thresholds, different sensors", ["dNBR threshold", "Tanager", "Simulated S-2", "Pixel agreement"], [
    ["> 0.10", "5 215 ha", "5 273 ha (+1.1 %)", "98.1 %"],
    ["> 0.27", "2 836 ha", "2 894 ha (+2.1 %)", "99.2 %"],
    ["> 0.44", "2 078 ha", "2 192 ha (+5.5 %)", "98.8 %"],
], kicker="the disagreement grows with severity",
   notes="Good news for the project: for burned-area mapping the sensors broadly agree. But the disagreement "
         "grows at higher thresholds, exactly where the policy-relevant 'high severity' number sits.")

d.bullets("Processing a full scene without running out of memory", [
    "The full cube (1 063 × 957 px × 426 bands, float32) would need **1.73 GB** in one array",
    "Tiled processing with a pure per-tile function: **8.3 s**, peak memory **0.24 GB**",
    "The same pattern as tiled inference in notebook 20 — read, compute, write, discard",
    "`dask.array` over the HDF5 dataset gives the same answer lazily in **5.6 s**",
    "Verified identical to the tiled numpy result on all valid pixels",
], kicker="scaling up",
   notes="Keep the per-tile function pure — inputs in, arrays out, no global state — and it parallelises "
         "for free. That is the difference between a notebook and something that runs over an archive.")

d.section("6. Refinement", "Sensitivity, error analysis, targeted fixes")

d.figure_bullets("How sensitive is your answer to the threshold?",
                 "30_advanced_analytics/13_10_1_threshold_sensitivity.jpg",
                 ["Mapped area is a steep function of the dNBR threshold",
                  "Raw Tanager: 5 215 ha above 0.10; after the offset correction: **3 621 ha**",
                  "The offset moves the answer more than the sensor choice does",
                  "Simulated Sentinel-2 with its own offset: 3 665 ha — close agreement",
                  "**Report a range and the threshold, never a single bare number**"],
                 caption="Mapped area against threshold, raw and offset-corrected",
                 notes="Ask the class which number they would put in a ministry briefing. The answer is "
                       "'both, with the assumption stated' — that is what the rubric rewards.")

d.table("Where the false alarms come from", ["Group", "Brighter in all bands", "Burn-like direction", "Median CVA angle"], [
    ["Control (unchanged) pixels", "80.4 %", "6.3 %", "6.3°"],
    ["False alarms, dNBR > 0.10", "85.6 %", "12.9 %", "8.4°"],
    ["False alarms, dNBR > 0.27", "83.7 %", "16.0 %", "15.3°"],
    ["The real new scar", "15.2 %", "84.6 %", "30.2°"],
], kicker="error analysis, not guesswork",
   notes="The real scar behaves in the opposite way to the false alarms on every diagnostic. That is what "
         "makes the targeted fix on the next slide defensible rather than arbitrary tuning.")

d.figure_bullets("The refinement loop, measured at each step",
                 "30_advanced_analytics/14_10_3_refine_and_measure.jpg",
                 ["0 · naive dNBR > 0.27: 2 793 ha, 1 724 clusters, **4.65 %** control false alarms",
                  "1 · co-registration: false alarms 4.11 %, scar interior 100 %",
                  "2 · dNBR offset: **1.37 %** false alarms, 653 clusters",
                  "4 · require burn-like CVA direction: **0.20 %**, scar 90.1 %",
                  "5 · minimum mapping unit (10 px): **0.00 %** false alarms, 22 clusters, scar 89.8 %"],
                 caption="Naive map versus the refined map after five measured steps",
                 image_left=True,
                 notes="Each step was measured on the same reference before and after. That is the difference "
                       "between refinement and fiddling. Note the trade: false alarms fall to zero, but we "
                       "give up about 10 % of the scar interior. Which error costs more depends on the user.")

d.handover("30_advanced_analytics.ipynb", [
    "Sections 1–2: align the two scenes and co-register them; check the residual shift",
    "Sections 3–5: dNBR, severity classes, spectral confirmation, change vector analysis",
    "Sections 6–7: find the artefacts, build a control area, propagate uncertainty",
    "Sections 8–9: harmonise with other sensors, then process a full scene tiled",
    "Section 10: sensitivity, error analysis and the refinement loop on your own thresholds",
], minutes=150,
   notes="The January scene is a 1.3 GB download on first run — start it before the break. Students should "
         "finish with the refinement checklist applied to their own project pipeline.")

d.recap([
    "**Geometry first**: CRS, lattice, co-registration better than half a pixel",
    "**Confirm detections** with the image, the spectrum and independent knowledge",
    "Measure the **systematic difference on unchanged land** and correct for it",
    "The honest error bar comes from **between-date variability**, not the sensor's own uncertainty",
    "**Harmonise** before mixing sensors: bandpass alone shifted NBR by 0.025",
    "**Tile** everything that needs full spectra; keep the per-tile function pure",
    "Refinement is a loop: sensitivity → error analysis → targeted fix → **measure again**",
], next_up="Session 2 — Final project implementation and testing (notebook 31)",
   notes="Close by pointing at the refinement checklist in the notebook: it is a ready-made structure for "
         "the 'limitations and next steps' slide of their final presentation.")

d.references([
    "Key, C.H. & Benson, N.C. (2006). Landscape assessment: sampling and analysis methods. FIREMON, USDA RMRS-GTR-164.",
    "Miller, J.D. & Thode, A.E. (2007). Quantifying burn severity in a heterogeneous landscape with a relative version of dNBR. Remote Sensing of Environment 109, 66–80.",
    "Malila, W.A. (1980). Change vector analysis: an approach for detecting forest changes with Landsat. LARS Symposia.",
    "Kuglin, C.D. & Hines, D.C. (1975). The phase correlation image alignment method. IEEE Int. Conf. Cybernetics and Society.",
    "Olofsson, P. et al. (2014). Good practices for estimating area and assessing accuracy of land change. Remote Sensing of Environment 148, 42–57.",
    "Tanager open data CC-BY-4.0 © Planet Labs PBC · ESA WorldCover 2021 v200 (CC-BY 4.0)",
])

d.save("w4a_advanced_analytics.pptx")
