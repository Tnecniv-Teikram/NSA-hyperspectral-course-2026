"""Week 2 · Session 2 — Feature extraction and dimensionality reduction."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from deckbuild import Deck  # noqa: E402

FIG = "13_feature_extraction_dim_reduction/"

d = Deck("Feature extraction and dimensionality reduction",
         "Week 2 · Session 2",
         notebook="13_feature_extraction_dim_reduction.ipynb",
         subtitle="From 352 redundant bands to 16 features you can defend",
         week="Week 2 · 16–19 November 2026")

d.objectives([
    "Explain why neighbouring hyperspectral bands are redundant, and what the Hughes phenomenon costs you",
    "Apply **PCA** and **MNF**, and say which one to use when noise matters",
    "Select a small set of *physical* bands, and recognise when a supervised selector is fooled by artefacts",
    "Compute **derivative** features and the red-edge position",
    "Choose narrow-band indices and absorption depths that Sentinel-2 cannot reproduce",
    "Assemble a compact, interpretable feature stack for classification",
], notes="This is the session where hyperspectral data starts paying for itself. Tell the room the "
         "day ends with a feature stack that notebook 15 will classify tomorrow. Ask who has used PCA "
         "before — most will have, almost nobody will have used MNF.")

# ----------------------------------------------------------------- 1. the problem
d.section("1. Why reduce at all?", "Redundancy, and what it does to a classifier")

d.callout("A Tanager pixel is 352 numbers.\nIt is not 352 pieces of information.",
          "Neighbouring bands are 5 nm apart, but real surface spectra change over tens of nanometres. "
          "In the Konya window, three principal components already carry 99 % of the variance.",
          kicker="the starting point",
          notes="Anchor the whole session here. The question is never 'how do I use all 352 bands', "
                "it is 'which few numbers carry the signal I need'.")

d.bullets("Redundancy: the bands repeat each other", [
    "Tanager samples every ~5 nm; most reflectance spectra vary smoothly over tens of nanometres",
    "Almost every pair of **neighbouring bands has r > 0.99**",
    "The correlation matrix shows **blocks**: visible and SWIR behave alike, the NIR plateau opposes them",
    "The flip happens at the **red edge** — vegetation is dark in the visible, bright in the NIR",
    "**Effective dimensionality** of a scene is far below the band count",
], kicker="the first reason",
   notes="Ask the class to predict the sign of the correlation between a red band and a NIR band over "
         "farmland before you show the matrix. Many expect positive; it is strongly negative.")

d.figure("The correlation matrix of 352 bands", FIG + "01_2_why_reduce_dimensions_redundancy_and_t.png",
         caption="Band-to-band correlation for a 200 × 200 px window over irrigated fields, Konya", kicker="konya, türkiye",
         notes="Walk the diagonal blocks: visible, red edge, NIR plateau, the two SWIR windows. "
               "The white gaps are the removed water-vapour regions from notebook 11.")

d.bullets("The Hughes phenomenon (Hughes, 1968)", [
    "With a **fixed** number of training samples, accuracy rises with features, peaks, then **falls**",
    "The model has more parameters than the data can constrain reliably",
    "A Gaussian classifier needs a covariance matrix of *d(d+1)/2* numbers per class",
    "For d = 352 bands that is **62,128 parameters per class** — from a few thousand labelled pixels",
    "Still true in the deep-learning era: it is why we pretrain, regularise and reduce",
], kicker="the second reason",
   notes="This is the single most quoted result in hyperspectral machine learning. The quiz asks it. "
         "Stress 'for a fixed number of training samples' — with unlimited labels the effect disappears.")

d.table("Two families of solutions", ["", "Feature extraction", "Feature selection"], [
    ["What it does", "Builds new features from all bands", "Keeps a subset of real bands"],
    ["Examples", "PCA, MNF, derivatives, indices", "Variance/correlation, mutual information"],
    ["Interpretable?", "Mixtures of all bands — harder", "Yes, each band has a wavelength"],
    ["Good for", "Compression, denoising, classifiers", "Explaining, cheap sensors, fast products"],
], kicker="extraction vs selection", col_widths=[1.2, 2, 2],
   notes="Both are legitimate. The choice is driven by whether you must explain the model to a "
         "domain expert, or whether you only need accuracy.")

# ----------------------------------------------------------------- 2. PCA
d.section("2. Principal Component Analysis", "Ordering by variance")

d.bullets("What PCA actually computes", [
    "Rotates the data onto orthogonal axes ordered by **variance explained**",
    "The axes are the eigenvectors of the band covariance matrix: **Σ·v = λ·v**",
    "PC_k = (x − x̄)ᵀ·v_k — a weighted sum of all bands",
    "The **loadings** v_k tell you which wavelengths drive that component",
    "Covariance PCA is dominated by bright bands; **standardising first** gives every band equal weight",
    ("Always state which of the two you used — the components differ", 1),
], kicker="the maths in one slide",
   notes="Keep the algebra light but show that loadings are the interpretable part. Exercise 1 in the "
         "notebook repeats the analysis with standardised bands, which is a good homework check.")

d.figure_bullets("Konya: three components hold 99 % of the variance",
                 FIG + "02_3_principal_component_analysis_pca.png",
                 ["Explained variance: **87.8 %**, 10.4 %, 0.9 % for PC1–PC3",
                  "3 components reach 99 %, 10 components reach 99.9 %",
                  "PC1 is essentially **brightness**",
                  "PC2 is a **vegetation** axis, driven by the NIR plateau",
                  "PC3 contrasts visible/NIR against SWIR — moisture and dry matter"],
                 caption="Explained variance per component",
                 notes="The steep drop is typical. Ask: if 99 % of the variance is in three components, "
                       "is the rest noise? Answer on the next slide: no.")

d.callout("PCA ranks by variance.\nVariance is not the same as information.",
          "Subtle diagnostic features — the xanthophyll signal behind PRI, a weak clay absorption — have "
          "low variance. They land in high-order components, mixed with noise. MNF fixes the noise half "
          "of that problem.",
          kicker="the limitation that matters",
          notes="This is the bridge to MNF. A common student error is to keep 'the first 10 PCs' and "
                "wonder why a subtle mineral feature disappeared.")

# ----------------------------------------------------------------- 3. MNF
d.section("3. Minimum Noise Fraction", "Ordering by signal-to-noise")

d.bullets("MNF = PCA after whitening the noise (Green et al., 1988)", [
    "**1. Estimate the noise covariance** Σ_N — the classic *shift difference* trick",
    ("In a homogeneous area, x(i,j) − x(i,j+1) is almost pure noise, with covariance 2Σ_N", 1),
    "**2. Whiten**: transform with W = V_N·Λ_N^(−1/2) so noise has unit variance in every direction",
    "**3. PCA on the whitened data** — components are now ordered by **SNR**",
    "Eigenvalue ≈ SNR + 1, so components with eigenvalue ≈ 1 are pure noise",
], kicker="three steps",
   notes="Lee et al. (1990) is the companion reference. The intuition: PCA asks 'where is the data "
         "spread out', MNF asks 'where is the data spread out relative to its own noise'.")

d.bullets("Estimating the noise honestly", [
    "The notebook searches the scene for the **most homogeneous 40 × 40 px window** (lowest CV at 1650 nm)",
    "Shift-difference and the file's own uncertainty layer agree in the blue, differ by 1.5–3.5× in NIR/SWIR",
    "Real texture is counted as noise, so shift difference is an **upper bound**",
    "Noise is of order **0.002–0.007 reflectance** — small against signals of 0.05–0.5, not negligible",
    "Tanager's noise covariance is **near-singular** (eigenvalues ~1e−15)",
    ("Add a small **ridge** — 0.1 % of mean noise variance — before whitening; standard practice", 1),
], kicker="a numerical detail that bites",
   notes="If you skip the ridge, you divide by the square root of 1e-15 and amplify meaningless "
         "directions. This is the kind of practical detail that separates a working pipeline from a "
         "crashed one.")

d.figure("MNF isolates sensor artefacts", FIG + "06_4_minimum_noise_fraction_mnf.png",
         caption="MNF components: low orders show fields and the town, high orders show detector striping", kicker="pushbroom striping",
         notes="Tanager is a pushbroom imager: each across-track pixel has its own detector element. "
               "Slight response differences leave stripes along the flight direction — diagonal here "
               "because the scene is rotated to north-up. MNF corrals them into their own components.")

d.figure_bullets("Denoising with the inverse transform",
                 FIG + "07_4_1_mnf_denoising.png",
                 ["Keep the first K components, zero the rest, transform back",
                  "K = 64 of 352 gave a median change of **0.0029 reflectance**",
                  "Biggest gains at the noisy ends: 410 nm and the 2440 nm SWIR edge",
                  "**Rule of thumb:** use MNF, not PCA, as classifier input when noise matters",
                  "Always inspect the *removed* image — it must look like stripes and speckle"],
                 caption="Original vs MNF-denoised spectrum",
                 notes="Warn about over-denoising: with too small a K you delete rare real signals. The "
                       "notebook shows a systematic 0.005 SWIR offset for an extreme pixel.")

# ----------------------------------------------------------------- 4. band selection
d.section("4. Band selection", "Keeping bands you can name")

d.bullets("Two strategies", [
    "**Unsupervised** — pick bands with high variance that are least correlated with those already chosen",
    "**Supervised** — rank bands by **mutual information** with class labels, then remove redundancy",
    ("In the spirit of mRMR: maximum relevance, minimum redundancy (Peng et al., 2005)", 1),
    "Labels here: ESA WorldCover 2021, pure 30 m pixels only",
    "The labels are **four years older** than the image — treat them as approximate",
], kicker="unsupervised and supervised",
   notes="Note the honesty about label age. Students will reuse these labels in notebooks 15, 20 and 21, "
         "and the mismatch is a deliberate teaching point about label noise.")

d.figure_bullets("A supervised selector can be fooled",
                 FIG + "09_5_band_selection_keep_a_few_physical_ban.png",
                 ["Naive top-MI picks cluster at **400–430 nm** and **1450–1480 nm**",
                  "Both are low-SNR or atmosphere-affected regions",
                  "**Noise hides redundancy** — noisy bands look independent of each other",
                  "**Spurious correlation** — haze and water vapour vary with terrain, and terrain "
                  "correlates with land cover",
                  "It predicts the label for the wrong reason, and will not transfer"],
                 caption="Bands chosen by each strategy",
                 notes="This is the most valuable slide in the deck. A supervised method finds whatever "
                       "separates your labels in this scene — including artefacts. Ask the room how they "
                       "would guard against it before you show the fix.")

d.bullets("The fix: constrain the search", [
    "Consider only **trustworthy bands** — ≥ 430 nm, away from the water-vapour shoulders",
    "After choosing a band, **exclude everything correlated above |r| = 0.95**",
    "This forces the picks to spread across the spectrum",
    "Result: 441, 551, 706, 776, 957, 1137, 1297, 1503, 2350, 2449 nm",
    ("Physically sensible: blue, green, red edge, NIR, water bands, SWIR minerals", 1),
], kicker="two constraints",
   notes="Read the ten wavelengths out and ask what each one is for. That check — can I name why this "
         "band is here — is what makes selection defensible in a report.")

d.table("Ten features can match 352", ["Feature set", "Features", "Accuracy"], [
    ["All bands", "352", "0.870"],
    ["10 naive top-MI bands", "10", "0.695"],
    ["10 MI bands, constrained", "10", "0.869"],
    ["10 unsupervised bands", "10", "0.835"],
    ["10 evenly spaced bands", "10", "0.849"],
    ["10 PCA components", "10", "0.900"],
    ["10 MNF components", "10", "0.859"],
], kicker="random forest, konya window", col_widths=[3, 1, 1],
   notes="Two lessons. First, ten well-chosen features match the full spectrum — a small-scale Hughes "
         "effect. Second, the naive MI set is far worse: ten near-identical noisy bands carry little "
         "more than one. Caveat loudly: this used a random split, which is optimistic — notebook 21 "
         "does it properly. Do not over-read differences of 1–2 %.")

# ----------------------------------------------------------------- 5. shape features
d.section("5. Shape features", "Derivatives, the red edge and narrow-band indices")

d.bullets("Derivatives emphasise shape, not brightness", [
    "Suppress additive offsets: soil background, residual haze",
    "Sharpen overlapping features",
    "They **amplify noise** — always smooth first (Savitzky–Golay, 1964)",
    "The best-known derivative feature is the **red-edge position (REP)**",
    "REP shifts to **longer** wavelengths as chlorophyll increases; shorter under stress",
], kicker="first derivatives",
   notes="Savitzky–Golay fits a local polynomial, so it preserves peak position and depth far better "
         "than a moving average — which matters when the feature you want *is* a peak position.")

d.code("Red-edge position, four-point method (Guyot & Baret, 1988)", """
# R_re is the midpoint between the red trough and the NIR shoulder
R_re = (R670 + R780) / 2

# linear interpolation between the 700 and 740 nm bands
REP  = 700 + 40 * (R_re - R700) / (R740 - R700)
""", kicker="cheap and robust",
   caption="Four bands, no fitting, no smoothing — and it agrees with the max-derivative REP at r = 0.87",
   notes="Give them both: max first derivative between 680 and 760 nm is the textbook definition, but "
         "it is quantised to the 5 nm band spacing. The interpolated version gives a smoother map.")

d.figure_bullets("REP keeps working after NDVI saturates",
                 FIG + "10_6_derivative_spectra_and_the_red_edge_po.png",
                 ["REP over vegetated pixels: 716.4 / 720.3 / 727.9 nm (5th / 50th / 95th)",
                  "Between NDVI 0.75 and 0.9, REP still spans **more than 10 nm**",
                  "NDVI saturates; the red edge keeps separating dense canopies",
                  "The two branches at high NDVI are different crops or growth stages",
                  "This is why red-edge features dominate nitrogen and stress monitoring"],
                 caption="Derivative spectra and the NDVI–REP relationship",
                 notes="Saturation is the standard argument for red-edge bands and it is why Sentinel-2 "
                       "carries three of them. Tanager resolves the edge with about a dozen bands.")

d.table("Narrow-band indices: what only a spectrum can give", ["Index", "Bands (nm)", "Sensitive to", "From S-2?"], [
    ["PRI", "531, 570", "Xanthophyll cycle, light-use efficiency", "No"],
    ["MCARI", "550, 670, 700", "Chlorophyll, reduced soil effect", "Approx."],
    ["TCARI/OSAVI", "550, 670, 700, 800", "Chlorophyll, ignores canopy density", "Approx."],
    ["CRI1", "510, 550", "Carotenoids", "No"],
    ["ARI1", "550, 700", "Anthocyanins (senescence, stress)", "Approx."],
    ["NDWI (Gao, 1996)", "860, 1240", "Canopy liquid water", "No"],
    ["NDNI", "1510, 1680", "Canopy nitrogen", "No"],
    ["CAI", "2031, 2101, 2211", "Cellulose and lignin: crop residue", "No"],
], kicker="eight indices, five impossible on sentinel-2", col_widths=[1.4, 1.5, 3, 1],
   notes="References: Gamon 1992 (PRI), Daughtry 2000 (MCARI), Haboudane 2002 (TCARI/OSAVI), "
         "Gitelson 2001/2002 (ARI, CRI), Gao 1996, Serrano 2002 (NDNI), Nagler 2003 and Daughtry 2005 "
         "(CAI). 'Approx.' means a broadband version exists but is less specific.")

d.figure_bullets("Reading the index maps",
                 FIG + "11_7_narrow_band_indices_what_only_a_hypers.png",
                 ["**CAI** is only meaningful on **non-green** pixels — the notebook masks NDVI > 0.3",
                  ("In green canopies, leaf water dominates the 2000–2200 nm shape", 1),
                  "Among bare fields, higher CAI marks **dry residue and stubble**",
                  "**NDWI (Gao)** peaks on the irrigated strips",
                  "**PRI** is a physiological signal and is noisy from space — compare within one scene only"],
                 caption="Narrow-band indices over the Konya window",
                 notes="The CAI masking rule is a real methodological point: the first version of this "
                       "notebook tracked leaf water instead of residue. Separating residue from bare soil "
                       "is essentially impossible with broadband sensors, and it matters for "
                       "conservation agriculture and erosion risk.")

d.figure_bullets("Absorption band depths: geology in the SWIR",
                 FIG + "12_7_1_mineral_absorption_depths_clay_and_c.png",
                 ["Depth **D = 1 − R_centre / R_continuum**, continuum = line between two shoulders",
                  "**Al–OH in clays** near 2200 nm — kaolinite doublet at ~2165 and ~2205 nm",
                  "**Carbonates**: calcite ≈ 2340 nm, dolomite ≈ 2320 nm",
                  "Mask vegetation and water — they have their own SWIR shapes",
                  "Korba clay on mine overburden · Al Dhafra and Konya carbonate"],
                 caption="Clay (2205 nm) and carbonate (2340 nm) depths, three scenes",
                 image_left=True,
                 notes="These results are geologically sensible and were not tuned: the Konya plain is an "
                       "ancient lake basin with marl deposits, and the Gulf coast is carbonate sand. Same "
                       "principle as USGS Tetracorder and the mineral products from AVIRIS, EnMAP and EMIT. "
                       "Always check features against residual CO₂ (~2010, 2060 nm) and water vapour.")

d.figure("The same spectra through Sentinel-2's bands", FIG + "14_7_2_what_would_sentinel_2_see.png",
         caption="Konya carbonate soil and irrigated crop, resampled to Sentinel-2 bands", kicker="why the detail disappears",
         notes="B12 is 175 nm wide, so the 2340 nm carbonate feature and the 2100 nm cellulose feature "
               "are averaged away. The same happens to the 1240 nm water band and the 531 nm PRI band. "
               "This slide is the answer to the quiz's short question.")

# ----------------------------------------------------------------- 6. the stack
d.section("6. The feature stack", "Sixteen numbers instead of 352")

d.table("A stack you can defend to a domain expert", ["Group", "Features"], [
    ["Extracted, noise-aware", "MNF 1–8"],
    ["Vegetation physiology", "NDVI, REP, TCARI/OSAVI, PRI, NDWI (Gao)"],
    ["Dry matter and soil", "CAI, clay depth, carbonate depth"],
], kicker="16 features", col_widths=[1.5, 3.5],
   notes="Saved as a GeoTIFF with band names, ready for notebook 15. Each feature has a physical "
         "meaning, which is what a reviewer wants to see.")

d.figure_bullets("Still some redundancy — and that is fine",
                 FIG + "15_8_the_feature_stack.png",
                 ["MNF components are uncorrelated by construction",
                  "MNF1, NDVI, NDWI (Gao) and CAI all respond to green vegetation",
                  "Clay depth is **negatively** correlated with them — canopies hide the soil feature",
                  "For a classifier, correlated features are acceptable",
                  "For **interpretation**, pick one representative per group"],
                 caption="Correlation between the 16 stacked features",
                 notes="REP is set to 700 nm on non-vegetated pixels so the stack has no gaps — mention "
                       "it, because a student will notice the flat area in the REP layer.")

d.handover("13_feature_extraction_dim_reduction.ipynb", [
    "Run PCA and MNF on the Konya window and compare the component images",
    "Reproduce the naive vs constrained band selection and the random-forest comparison",
    "Map REP and compare it with NDVI on dense canopies",
    "Compute CAI, clay and carbonate depths, then resample to Sentinel-2 and see what survives",
    "Build and save the 16-feature stack for tomorrow's classification session",
], minutes=120,
   notes="Exercises 2 (how many MNF components) and 5 (a six-band satellite) are the ones to discuss "
         "as a group afterwards — both have no single right answer.")

d.recap([
    "Bands are **redundant** (neighbour r > 0.99); too many features hurt — **Hughes, 1968**",
    "**PCA** orders by variance; **MNF** orders by SNR, isolates striping and enables denoising",
    "Supervised band selection can lock onto **artefacts** — constrain it and check the wavelengths",
    "**Ten well-chosen features matched all 352** on this scene",
    "**REP** keeps discriminating after NDVI saturates",
    "**Narrow-band indices and band depths** are the hyperspectral payoff — most are impossible on S-2",
    "For your project: a small, **justified** stack beats all 352 bands",
], next_up="Session 3 — Material discrimination and target detection",
   notes="Point at quizzes/quiz_w2_features_detection_classification.md for self-check, and note that "
         "assignment W2 asks for a PCA vs MNF comparison in their own area.")

d.references([
    "Hughes, G.F. (1968). On the mean accuracy of statistical pattern recognisers. IEEE Trans. Inf. Theory 14, 55–63.",
    "Green, A.A. et al. (1988). A transformation for ordering multispectral data in terms of image quality. IEEE TGRS 26, 65–74.",
    "Lee, J.B. et al. (1990). Enhancement of high spectral resolution remote sensing data by a noise-adjusted principal components transform. IEEE TGRS 28, 295–304.",
    "Savitzky, A. & Golay, M.J.E. (1964). Smoothing and differentiation of data by simplified least squares procedures. Anal. Chem. 36, 1627–1639.",
    "Guyot, G. & Baret, F. (1988). Utilisation de la haute résolution spectrale pour suivre l'état des couverts végétaux. Proc. 4th Int. Colloquium on Spectral Signatures.",
    "Gamon, J.A. et al. (1992) RSE 41, 35–44 (PRI) · Daughtry, C.S.T. et al. (2000) RSE 74, 229–239 (MCARI) · Haboudane, D. et al. (2002) RSE 81, 416–426 (TCARI/OSAVI).",
    "Gao, B.-C. (1996) RSE 58, 257–266 (NDWI) · Serrano, L. et al. (2002) RSE 81, 355–364 (NDNI) · Nagler, P.L. et al. (2003) RSE 87, 310–325 and Daughtry, C.S.T. et al. (2005) Agron. J. 97, 864 (CAI).",
    "Peng, H. et al. (2005). Feature selection based on mutual information: mRMR. IEEE TPAMI 27, 1226–1238.",
    "Clark, R.N. et al. (2003). Imaging spectroscopy: Earth and planetary remote sensing with Tetracorder. JGR 108(E12), 5131.",
])

d.save("w2b_feature_extraction.pptx")
