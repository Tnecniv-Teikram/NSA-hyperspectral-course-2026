"""Week 2 · Session 3 — Material discrimination and target detection."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from deckbuild import Deck  # noqa: E402

FIG = "14_material_discrimination_target_detection/"

d = Deck("Material discrimination and target detection",
         "Week 2 · Session 3",
         notebook="14_material_discrimination_target_detection.ipynb",
         subtitle="What is this pixel made of — and what is hiding inside it?",
         week="Week 2 · 16–19 November 2026")

d.objectives([
    "Compare spectra with **SAM** and **SID**, and explain why both ignore brightness",
    "Build rule images, choose thresholds and produce a SAM classification map",
    "Use **continuum removal** to match diagnostic absorption features rather than whole spectra",
    "Derive the **matched filter**, **ACE** and **CEM** from background statistics",
    "Benchmark detectors honestly with a target-implantation experiment and ROC curves",
    "Unmix a pixel with **N-FINDR** endmembers and **FCLS** abundances, and read the residual map",
    "Explain why methane retrieval uses a matched filter on radiance, not a band ratio",
], notes="This is the densest session of the week. Signpost the three families early and keep "
         "returning to the table on slide 4 — students conflate classification and detection "
         "constantly. The practical is long, so keep the lecture tight.")

# ----------------------------------------------------------------- 1. framing
d.section("1. Three questions, three families", "Choosing the right tool before the right code")

d.callout("A multispectral sensor tells you a pixel is bright or green.\n"
          "A hyperspectral sensor can tell you what it is made of.",
          "And often whether a material you are looking for is hiding inside a 30 m pixel that is "
          "mostly something else.",
          kicker="why this session exists",
          notes="Link back to Monday: yesterday we compressed the spectrum, today we use its shape to "
                "identify materials. This is the capability that justifies the mission.")

d.table("Match the method to the question", ["Family", "Question it answers", "Methods"], [
    ["Spectral similarity", "Which reference does this whole pixel look like?", "SAM, SID, feature matching"],
    ["Target detection", "Is a small amount of material X present?", "Matched filter, ACE, CEM"],
    ["Spectral unmixing", "What fraction of the pixel is each material?", "N-FINDR / VCA + NNLS / FCLS"],
], kicker="the map of today", col_widths=[1.3, 2.6, 1.8],
   notes="Emphasise the middle row: detection assumes the target is rare and the background is unknown "
         "but statistically describable. That assumption is what makes it powerful.")

# ----------------------------------------------------------------- 2. similarity
d.section("2. Spectral similarity", "Comparing shapes, not brightness")

d.bullets("Three ways to compare two spectra", [
    "**Euclidean distance** ‖x − r‖ — sensitive to brightness *and* shape",
    "**SAM** (Kruse et al., 1993): the angle between the two vectors, α = arccos( x·r / (‖x‖‖r‖) )",
    ("Multiplying a spectrum by a constant does not change the angle — shape only", 1),
    "**SID** (Chang, 2000): treat each spectrum as a probability distribution over bands",
    ("Symmetric Kullback–Leibler divergence — weighs *where* the energy sits", 1),
    "Both SAM and SID are **brightness-invariant**; Euclidean distance is not",
], kicker="euclidean, sam, sid",
   notes="Geometry helps: draw two arrows from the origin. Euclidean compares the tips, SAM compares "
         "the directions. A shadowed slope moves the tip but not the direction.")

d.table("Brightness invariance, measured", ["Comparison", "Euclidean", "SAM (rad)", "SID"], [
    ["Dry bare soil vs the same soil at 50 % illumination", "3.837", "0.000", "0.000"],
    ["Dry bare soil vs dry steppe grassland", "0.948", "0.084", "0.010"],
], kicker="course library spectra", col_widths=[3.4, 1, 1, 1],
   notes="The punchline: Euclidean distance calls the shadowed copy of a soil four times more different "
         "than an actually different material. That is why angle-based measures are the default.")

d.figure_bullets("Which materials can be told apart at all?",
                 FIG + "00_2_2_which_library_materials_are_easy_or_.png",
                 ["Small angles (dark cells) mean confusion is inevitable",
                  "2.83° dense urban ↔ bright industrial roof",
                  "2.91° sabkha ↔ desert sand",
                  "4.45° tropical tree cover ↔ sugarcane",
                  "Fixes: texture, context, or a **time series** — not a better angle measure"],
                 caption="Pairwise SAM between the 19 course library spectra",
                 image_left=True,
                 notes="Run this matrix before you promise a client a classification. If two classes sit "
                       "at 3°, no whole-pixel method will separate them reliably, and you should say so "
                       "in the proposal rather than after the delivery.")

d.bullets("SAM classification in three steps", [
    "**1. Rule images** — one angle map per reference material (dark = similar)",
    "**2. Minimum-angle rule** — assign each pixel to its closest reference",
    "**3. Threshold** — if even the best angle is large, label the pixel *unclassified*",
    "Unclassified means: the material is not in the library, or the pixel is a mixture",
    "At 30 m, **most pixels are mixtures** — expect a large unclassified fraction",
], kicker="kusmunda coal mine, korba",
   notes="Kusmunda is one of the largest open-cast coal mines in Asia. The window has dark coal faces, "
         "bright overburden dumps, water in the pits, farmland and trees — a good test of a library "
         "built mostly from other scenes.")

d.figure_bullets("Minimum-angle classification of the mine",
                 FIG + "03_2_3_sam_classification_of_the_kusmunda_c.png",
                 ["Works where references came from **this** scene: coal and spoil",
                  "Farmland is forced into 'soil' or 'steppe' — imported references are weaker",
                  "Set thresholds **per class** from rule-image histograms, not one global value",
                  "Always **report the unclassified fraction** — it is a quality indicator",
                  "SAM and SID agree on **83.9 %** of pixels; they differ where classes are close"],
                 caption="SAM classification, Kusmunda window (180 × 540 px)",
                 image_left=True,
                 notes="Exercise 1 asks students to set per-class thresholds from histograms and "
                       "recompute the map — the fastest way to feel how arbitrary one global threshold "
                       "is. SAM and SID disagree exactly on soil vs spoil and steppe vs soil.")

# ----------------------------------------------------------------- 3. feature matching
d.section("3. Matching features, not spectra", "Continuum removal")

d.bullets("Why geologists do not use whole-spectrum SAM", [
    "Whole-spectrum SAM is dominated by broad shape: brightness slope, the vegetation red edge",
    "**Continuum removal** (Clark & Roush, 1984) divides the spectrum by its upper convex hull",
    "Absorption features become dips below 1.0, comparable between bright and dark materials",
    "Clays show **Al–OH near 2200 nm**; kaolinite has a doublet at ~2165 and ~2205 nm",
    "Match the *feature shape* with SAM restricted to 2120–2250 nm",
    ("Check against residual CO₂ (~2010, 2060 nm) and water vapour (~1900 nm) artefacts", 1),
], kicker="isolating the diagnostic part",
   notes="This is how mineral maps from AVIRIS, EnMAP and EMIT are made — the USGS Tetracorder approach, "
         "with a full mineral library and many features instead of one.")

d.figure("Feature depth and feature shape at the mine", FIG + "05_2_5_continuum_removal_matching_diagnosti.png",
                  caption="2205 nm band depth and continuum-removed shape matching, Kusmunda",
         kicker="clay in the overburden",
         notes="Feature mapping highlights the spoil heaps and the mine benches where clay-bearing rock "
               "is exposed, independent of brightness — a result that whole-spectrum SAM cannot give "
               "because brightness dominates the angle.")

# ----------------------------------------------------------------- 4. detection
d.section("4. Target detection", "Finding what is rare and partly hidden")

d.bullets("Why similarity measures fail for small targets", [
    "SAM compares the **whole** pixel with the reference",
    "If a target fills 10 % of a 30 m pixel, 90 % of the signal is background",
    "The angle to the target stays large, so the pixel is never selected",
    "**Detectors** instead model the background statistically",
    "They look for the *direction* in which the target pushes a pixel away from the background",
    ("Assumption: targets are **rare**, so scene statistics ≈ background statistics", 1),
], kicker="the sub-pixel problem",
   notes="Ask the room: what fraction of a 30 m pixel does a 10 m wide roof occupy? About 11 %. Almost "
         "every man-made target in Tanager data is sub-pixel, so this is the normal case, not an edge case.")

d.table("Three detectors", ["Detector", "Score", "Notes"], [
    ["Matched filter", "sᵀΣ⁻¹(x − μ) / sᵀΣ⁻¹s", "≈ target fraction under linear mixing"],
    ["ACE", "(sᵀΣ⁻¹(x − μ))² / (sᵀΣ⁻¹s · (x−μ)ᵀΣ⁻¹(x−μ))", "cos² of the whitened angle; range 0–1"],
    ["CEM", "wᵀx, w = R⁻¹t / (tᵀR⁻¹t)", "Minimises output energy; uses correlation R"],
], kicker="s = t − μ, the target direction", col_widths=[1, 2.6, 2.2],
   notes="Kraut & Scharf (1999) for ACE, Harsanyi (1993) for CEM. The key shared idea is Σ⁻¹: whiten the "
         "background so that ordinary variability is suppressed and the target direction stands out. "
         "ACE's 0–1 range makes its thresholds transferable between scenes.")

d.figure_bullets("The target: blue metal roofs in Ho Chi Minh City",
                 FIG + "06_3_2_the_target_blue_metal_roofs_in_ho_ch.png",
                 ["Blue roofs reflect relatively more blue than red",
                  "**113 target pixels** found in park A by blue/red ratio",
                  "Split in half: **56** give the detector signature, **57** are kept for implanting",
                  "Even the purest roof pixels are mixtures — the vegetation red edge is visible",
                  "That is acceptable: the detector needs a *direction*, not a pure spectrum"],
                 caption="Industrial park A, the signature source",
                 notes="Splitting the target pixels is the honest choice: implanting with the same "
                       "spectra you built the signature from would inflate every detector's score.")

d.bullets("Background statistics and shrinkage", [
    "μ and Σ come from all window pixels **outside** both parks",
    "With 350 bands, Σ is badly conditioned — condition number **1.6 × 10¹¹** without shrinkage",
    "Shrinkage λ on the diagonal: λ = 0.001 brings it to **2.8 × 10⁵**",
    "Too little shrinkage over-fits noise; too much throws away the whitening that gives the power",
    "Tune λ on implanted targets — best AUC here was around λ = 0.001",
    ("Alternative: reduce dimensions with PCA or MNF first (notebook 13)", 1),
], kicker="the practical detail that decides success",
   notes="Condition number is the ratio of largest to smallest eigenvalue: 1e11 means the inverse is "
         "numerically meaningless in some directions. This slide is the difference between a detector "
         "that works and one that outputs noise.")

d.bullets("Benchmarking honestly: target implantation", [
    "We rarely have ground truth for small targets, so we **make** some",
    "x_implant = (1 − f)·x_background + f·t_pixel, with sub-pixel fraction f",
    "t_pixel is a **random roof pixel from the held-out half** — real targets vary",
    "Score 5,000 clean background pixels and 1,000 implanted pixels with each detector",
    "Draw **ROC curves**: detection rate against false-alarm rate",
    ("Log-scale the false-alarm axis — operational use needs very low false-alarm rates", 1),
], kicker="making ground truth",
   notes="A scene has hundreds of thousands of background pixels, so a 1 % false-alarm rate still means "
         "thousands of false detections. That is why the log axis matters and why analysts care about "
         "the left-hand end of the ROC curve only.")

d.figure("ROC curves by sub-pixel fill fraction", FIG + "08_3_4_how_good_are_the_detectors_a_target_.png",
                  caption="5,000 background vs 1,000 implanted pixels, Ho Chi Minh City",
         kicker="detection rate vs false alarms",
         notes="Read the 10 % panel: at a 1 % false-alarm rate ACE finds about half the implanted "
               "targets while SAM finds almost none. That gap is the entire argument for statistical "
               "detectors over similarity measures.")

d.table("Area under the ROC curve by fill fraction", ["Fill", "MF", "CEM", "ACE", "SAM"], [
    ["2 %", "0.676", "0.669", "0.581", "0.537"],
    ["5 %", "0.828", "0.815", "0.772", "0.562"],
    ["10 %", "0.913", "0.902", "0.906", "0.612"],
    ["20 %", "0.937", "0.929", "0.937", "0.722"],
    ["30 %", "0.938", "0.930", "0.944", "0.790"],
], kicker="auc, higher is better", col_widths=[1, 1, 1, 1, 1],
   notes="Three readings. Detectors beat SAM everywhere. SAM only becomes usable at 20–30 % fill, by "
         "which point the target is nearly resolved. And AUC hides the low-false-alarm behaviour where "
         "ACE is strongest — always look at the curve, not only the summary number.")

d.bullets("Read implantation results with care", [
    "They are **optimistic**: linear mixing is assumed, with no misregistration or adjacency effects",
    "Implanted spectra come from the same park as the signature",
    "Treat AUC as an **upper bound** and as a way to *compare* detectors and settings",
    "The real value is relative: which detector, which λ, which band subset",
    "Then confirm on the real scene, and look at the map",
], kicker="the caveat slide",
   notes="Every benchmark in remote sensing is optimistic in some way. What matters is that you state "
         "the direction of the bias. The project rubric rewards exactly this kind of honesty.")

d.figure_bullets("On the real scene",
                 FIG + "09_3_5_running_the_detectors_on_the_real_sc.png",
                 ["SAM lights up every bright, flat-spectrum surface in the city",
                  "MF, ACE and CEM suppress the background and find **park B**",
                  ("The signature came only from park A — this is genuine generalisation", 1),
                  "Faint vertical stripes in MF and CEM are **pushbroom detector striping**",
                  ("Whitening amplifies tiny column-to-column calibration differences", 1),
                  "ACE above the 99.8th background percentile (0.223): **301 pixels**, 126 in A, 81 in B"],
                 caption="SAM, MF, ACE and CEM over the same window",
                 notes="The striping is a good teaching moment: whitening is powerful but amplifies "
                       "systematic sensor artefacts, which is another argument for MNF preprocessing.")

# ----------------------------------------------------------------- 5. unmixing
d.section("5. Spectral unmixing", "From detection to fractions")

d.bullets("The linear mixing model", [
    "If materials sit side by side at sub-pixel scale, the spectrum is a weighted sum of **endmembers**",
    "x = Σ aᵢ·eᵢ + n, with abundances aᵢ as area fractions",
    "**ANC**: aᵢ ≥ 0 — no negative areas",
    "**ASC**: Σ aᵢ = 1 — the fractions cover the pixel",
    "Breaks down for **intimate mixtures** (mineral grains) and **canopy multiple scattering**",
    ("The residual map tells you where the model failed", 1),
], kicker="jiquilisco bay, el salvador",
   notes="The estuary is a good test: water, breaking surf, sand bars, grassland, crops and mangroves "
         "in one window, with genuinely mixed 30 m pixels along every shoreline.")

d.bullets("Finding the endmembers", [
    "With p endmembers the data occupy a **(p − 1)-dimensional simplex**",
    "Here the first 4 PCs hold **99.89 %** of the variance, so p = 5 is a reasonable choice",
    "**N-FINDR** (Winter, 1999): find the p pixels spanning the **largest simplex volume**",
    "Alternatives: **PPI** (Boardman, 1993) and **VCA** (Nascimento & Bioucas-Dias, 2005)",
    "Endmembers are the most **extreme** pixels, not necessarily the materials you care about",
    ("Breaking surf appeared as an endmember here — bright, flat, not in any library", 1),
], kicker="n-findr and friends",
   notes="More formal ways to choose p exist — virtual dimensionality, HySime. In practice you try a "
         "few values and look at the spectra and the residual map, which is exercise 4.")

d.table("Three ways to estimate abundances", ["Method", "Negative fractions", "Median sum", "Median RMSE"], [
    ["Unconstrained LS", "94.2 % of pixels", "0.889", "0.0031"],
    ["NNLS (aᵢ ≥ 0)", "0 %", "0.940", "0.0065"],
    ["FCLS (aᵢ ≥ 0, Σ = 1)", "0 %", "1.000", "0.0065"],
], kicker="el salvador estuary", col_widths=[1.6, 1.6, 1.2, 1.2],
   notes="The trap: unconstrained least squares has the *lowest* residual and is the *worst* model — it "
         "explains spectra with physically impossible combinations. Lower RMSE does not mean a better "
         "physical model. FCLS (Heinz & Chang, 2001) is implemented with NNLS plus one extra row.")

d.figure_bullets("Abundance maps and the residual",
                 FIG + "13_4_3_abundance_estimation_ls_nnls_and_fcl.png",
                 ["FCLS fractions can be read as **area percentages**",
                  "The **residual map** is the diagnostic layer",
                  "High residual = a material no endmember represents, or non-linear mixing",
                  "Highest here on the **barrier island** (sand, palms, grass, fields in one pixel)",
                  "And in **mangroves**, where a green-crop endmember fits the canopy shape badly",
                  ("Remedies: more endmembers, MESMA (Roberts et al., 1998), non-linear models", 1)],
                 caption="Abundances and RMSE residual, Jiquilisco Bay",
                 notes="Tell students to always publish the residual map next to the abundance maps. It "
                       "is the unmixing equivalent of a confusion matrix.")

# ----------------------------------------------------------------- 6. methane
d.section("6. The methane case", "Where the matched filter earns its keep")

d.bullets("Methane retrieval is a matched filter on radiance", [
    "CH₄ absorbs in narrow lines between **2200 and 2400 nm** — Tanager was designed for this",
    "Standard retrieval: Thompson et al. (2015); **MAG1C**, Foote et al. (2020); Carbon Mapper operationally",
    "Target is a **unit absorption spectrum**: t = μ ⊙ k, with k from a radiative transfer model",
    "The output α̂ is the **methane enhancement** per pixel, in ppm·m",
    "**Why radiance?** Atmospheric correction treats gas absorption as atmosphere and partly removes the plume",
    ("So a reflectance-based band ratio is working on data the plume has been taken out of", 1),
], kicker="section 3, applied",
   notes="This closes the loop: the same maths as the blue roofs, with a physically derived target "
         "instead of an image-derived one. The background covariance is what suppresses surface "
         "variability, which is exactly what a band ratio cannot do.")

d.figure_bullets("Why notebook 03's MBSI is only a proxy",
                 FIG + "15_5_box_methane_the_matched_filter_at_work.png",
                 ["MBSI computed on **library spectra that contain no methane**",
                  "Vegetation scores positive — leaf water, cellulose and lignin absorb near 2300 nm",
                  "Carbonate- and sulphate-rich **sabkha** scores positive too",
                  "A real plume adds only a few percent absorption — surface variability swamps it",
                  "The matched filter whitens that variability away"],
                 caption="MBSI on methane-free reference spectra",
                 image_left=True,
                 notes="Be direct with students who used notebook 03: the index is a teaching tool, not "
                       "a retrieval. If their project claims plume detection, they need the radiance "
                       "product or Planet's operational layer.")

d.bullets("Planet ships the operational product", [
    "`ortho_radiance_hdf5` — the radiance you need for your own matched filter",
    "`ortho_ql_ch4` — a Carbon Mapper methane quick-look COG (qualitative concentration index)",
    "`ql_ch4_json` — plume origins as GeoJSON with emission rate, uncertainty and wind",
    "Example: Deir ez-Zor, Syria — **12 plumes**, roughly 170 to 3,200 kg/h, each with a quality flag",
    "Our Korba scene lists plume IDs, but its quick-look and plume file are empty",
    ("Check the quality flag: several plumes in that scene are marked *questionable*", 1),
], kicker="ghg-plumes stac collection",
   notes="Point at the emission rates and the uncertainties: 3,189 ± 390 kg/h. Any project claiming "
         "emission quantification must carry uncertainty like this, and the wind speed is usually the "
         "dominant term.")

d.handover("14_material_discrimination_target_detection.ipynb", [
    "Build SAM rule images for the Kusmunda mine and set per-class thresholds",
    "Map the 2205 nm clay feature with continuum removal",
    "Run MF, ACE and CEM on the blue-roof target, and tune the shrinkage λ",
    "Reproduce the implantation experiment and the ROC curves",
    "Unmix the El Salvador estuary with N-FINDR and FCLS, then inspect the residual map",
], minutes=150,
   notes="Exercise 2 (white roofs vs the cloud mask) is the one to highlight — it shows that the beta "
         "cloud mask confuses bright roofs with clouds, which connects back to notebook 11.")

d.recap([
    "**SAM and SID** compare shape, not brightness — check class separability before promising a map",
    "Report the **unclassified fraction**; at 30 m most pixels are mixtures",
    "**Continuum removal** isolates diagnostic features and beats whole-spectrum matching for minerals",
    "**Detectors** (MF, ACE, CEM) model the background and find **sub-pixel** targets that SAM misses",
    "**Shrinkage** of the covariance is not optional at 350 bands",
    "**Implantation** gives you an honest, if optimistic, way to compare detectors",
    "**FCLS** abundances are area fractions; the **residual map** shows where the model fails",
    "Methane needs a **matched filter on radiance** — band ratios respond to the surface",
], next_up="Session 4 — Classification approaches for hyperspectral data",
   notes="Close by returning to the three-family table. Tomorrow's session answers the first question "
         "for every pixel at once, with labels and validation.")

d.references([
    "Kruse, F.A. et al. (1993). The Spectral Image Processing System (SIPS). RSE 44, 145–163. (SAM)",
    "Chang, C.-I. (2000). An information-theoretic approach to spectral variability, similarity and discrimination. IEEE Trans. Inf. Theory 46, 1927–1932. (SID)",
    "Clark, R.N. & Roush, T.L. (1984). Reflectance spectroscopy: quantitative analysis techniques. JGR 89, 6329–6340. (Continuum removal)",
    "Harsanyi, J.C. (1993). Detection and classification of subpixel spectral signatures in hyperspectral image sequences. PhD thesis, UMBC. (CEM)",
    "Kraut, S. & Scharf, L.L. (1999). The CFAR adaptive subspace detector is a scale-invariant GLRT. IEEE Trans. Signal Processing 47, 2538–2541. (ACE)",
    "Winter, M.E. (1999). N-FINDR: an algorithm for fast autonomous spectral endmember determination. Proc. SPIE 3753, 266–275.",
    "Nascimento, J.M.P. & Bioucas-Dias, J.M. (2005). Vertex component analysis. IEEE TGRS 43, 898–910.",
    "Heinz, D.C. & Chang, C.-I. (2001). Fully constrained least squares linear spectral mixture analysis. IEEE TGRS 39, 529–545.",
    "Roberts, D.A. et al. (1998). Mapping chaparral in the Santa Monica Mountains using multiple endmember spectral mixture models. RSE 65, 267–279. (MESMA)",
    "Thompson, D.R. et al. (2015). Real-time remote detection and measurement for airborne imaging spectroscopy. AMT 8, 4383–4397.",
    "Foote, M.D. et al. (2020). Fast and accurate retrieval of methane concentration from imaging spectrometer data using sparsity prior. IEEE TGRS 58, 6480–6492. (MAG1C)",
])

d.save("w2c_material_discrimination_detection.pptx")
