"""Week 3 · Session 3 — Validation methods and accuracy assessment."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from deckbuild import Deck  # noqa: E402

FIG = "21_validation_accuracy_assessment/"

d = Deck("Validation methods and accuracy assessment",
         "Week 3 · Session 3",
         notebook="21_validation_accuracy_assessment.ipynb",
         subtitle="How good is your map, really — and how do you defend that number",
         week="Week 3 · 16–19 November 2026")

d.objectives([
    "Build and read an error matrix, and compute user's, producer's, F1 and IoU correctly",
    "Explain why kappa is no longer recommended, and what to report instead",
    "Design a train/test split that is *spatially* independent",
    "Draw a probability sample and estimate area-adjusted accuracy with confidence intervals",
    "Validate continuous products with bias, RMSE and Bland–Altman, not R² alone",
], notes="This is the session that most changes project marks. Validity carries 30 % of the rubric, "
         "the single largest weight. Tell them that now, so they listen to the sampling part.")

d.section("1. What validation is for", "A map is a model, so it has errors — the question is how many")

d.callout("\"It looks right on the map\" is not a validation.",
          "A validation estimates how many errors, of which kind, and where — for the whole map, "
          "not just the pixels you happened to label. And it comes with an uncertainty.",
          kicker="the standard to meet",
          notes="Ask the room how they would check a map they were handed. Most answers are 'look at it' "
                "or 'check a few places I know' — both are exactly the biased approaches we are replacing.")

d.bullets("Three parts of a rigorous assessment", [
    "**Sampling design** — how reference locations are chosen (random, stratified, systematic)",
    "**Response design** — how the true class at each location is determined, independently of the map",
    "**Analysis** — the estimators that turn the sample into accuracy and area, with confidence intervals",
    ("Skip any one of the three and the number you report is not defensible", 1),
], kicker="Stehman & Foody (2019)",
   notes="Students almost always jump straight to 'analysis' and compute an OA on whatever pixels they have. "
         "The first two parts are what make the third meaningful.")

d.table("Where reference data comes from", ["Source", "Quality", "Cost", "Watch out for"], [
    ["Field survey / GPS points", "Highest", "Highest", "Small sample, access bias, date mismatch"],
    ["VHR image interpretation", "High", "Medium", "Interpreter bias; needs a protocol"],
    ["Existing maps (WorldCover, CLC)", "Medium", "Lowest", "Its own errors, different legend and date"],
    ["Crowd-sourced (Geo-Wiki, OSM)", "Variable", "Low", "Uneven coverage and quality"],
], kicker="and its own error", col_widths=[2, 1, 1, 3],
   notes="Emphasise the last row of the third option: reference data is not truth, it is better data. "
         "In this course we use WorldCover as a stand-in and we say so explicitly in every result.")

d.bullets("Reference data must be independent", [
    "Independent of the **training** pixels — otherwise you measure memorisation, not generalisation",
    "Independent of the **map**: never look at the map label while assigning the reference class",
    "Matched in **time**: WorldCover 2021 against a 2025 image contains real change, not only error",
    "Matched in **legend**: harmonise classes before comparing, and say how you did it",
], kicker="four kinds of independence",
   notes="The legend point bites every year: WorldCover 'cropland' includes fallow fields, so a greenness "
         "threshold can never match it. That mismatch is a finding to explain, not an error to hide.")

d.section("2. The error matrix", "Everything else is derived from this table")

d.bullets("Orientation and notation", [
    "Convention in remote sensing: **rows = map class**, **columns = reference class**",
    "scikit-learn's `confusion_matrix(y_true, y_pred)` is the transpose — check before you read it",
    "Diagonal = agreement; off-diagonal = the two kinds of error",
    "**Commission** (row): mapped as X, is not X. **Omission** (column): is X, mapped as something else",
], kicker="read it the right way round",
   notes="Have them say out loud which way the matrix in their own notebook is oriented. A transposed "
         "matrix silently swaps user's and producer's accuracy and no plot will warn you.")

d.table("The metrics, and what each one answers", ["Metric", "Formula", "Question it answers"], [
    ["Overall accuracy", "Σ diagonal / N", "What fraction of the map is right?"],
    ["User's accuracy (precision)", "n_ii / row total", "If the map says X, how often is it X?"],
    ["Producer's accuracy (recall)", "n_ii / column total", "If it is X, how often did the map find it?"],
    ["F1", "2·UA·PA / (UA + PA)", "One number balancing both, per class"],
    ["IoU (Jaccard)", "TP / (TP + FP + FN)", "Overlap of mapped and true extent"],
], kicker="definitions", col_widths=[2, 2, 3],
   notes="User's and producer's accuracy are precision and recall with different names — say that explicitly, "
         "because the ML-trained half of the room and the RS-trained half use different words for the same thing.")

d.table("Notebook 21: a five-class Tanager map of Ho Chi Minh City", ["Class", "UA", "PA", "F1", "IoU"], [
    ["Tree cover", "0.828", "0.696", "0.757", "0.608"],
    ["Grassland", "0.509", "0.657", "0.573", "0.402"],
    ["Cropland", "0.591", "0.632", "0.611", "0.440"],
    ["Built-up & bare", "0.898", "0.901", "0.899", "0.817"],
    ["Water", "0.806", "0.859", "0.832", "0.712"],
    ["Overall accuracy 0.763 · macro F1 0.734 · weighted F1 0.766", "", "", "", ""],
], kicker="pure-pixel test set",
   notes="Point at grassland: UA 0.51 means half of what the map calls grassland is not grassland. "
         "A single OA of 0.76 would have hidden that completely — always report per class.")

d.bullets("Macro or weighted?", [
    "**Macro** averages the per-class scores equally — small classes count as much as large ones",
    "**Weighted** averages by class frequency — dominated by whatever covers most of the scene",
    "Report both when classes are imbalanced; they differ here (0.734 vs 0.766)",
    "For a rare target class (a plume, a mangrove fringe), macro F1 or that class's F1 is the honest headline",
], kicker="averaging choices",
   notes="A model that ignores the rarest class entirely can still post a high weighted score. "
         "Ask which average a team mapping a rare feature should lead with, and why.")

d.bullets("Kappa: why it is no longer recommended", [
    "κ = (p_o − p_e)/(1 − p_e) 'corrects' accuracy for agreement expected by chance",
    "The chance baseline is not meaningful for maps, and κ is highly correlated with overall accuracy",
    "It adds no information the error matrix does not already give (Pontius & Millones 2011; Foody 2020)",
    "**Instead:** report OA with a confidence interval, per-class UA/PA, and quantity vs allocation disagreement",
    ("Notebook 21: κ = 0.693, while Q = 0.051 and A = 0.186 — allocation is the real problem here", 1),
], kicker="Pontius & Millones (2011)",
   notes="Quantity disagreement asks whether the class totals are right; allocation asks whether they are in "
         "the right places. Here the areas are nearly right but the placement is not — κ never tells you that.")

d.section("3. Independence", "The spatial trap that inflates every accuracy figure")

d.figure_bullets("Random splits leak through space",
                 FIG + "01_4_random_vs_spatial_cross_validation.png",
                 ["Neighbouring pixels are nearly identical — a random split puts them in both sets",
                  "Random 5-fold CV: **OA 0.812 ± 0.011**",
                  "Blocked CV, 100-px (3 km) blocks: **OA 0.764 ± 0.042**",
                  "The gap is the optimism; the blocked number is what to expect in a new area"],
                 caption="Accuracy falls as test blocks move away from training data",
                 kicker="measured in notebook 21",
                 notes="Nearly 5 accuracy points, on a deliberately simple example. With patch-based CNNs and "
                       "overlapping windows the gap is larger. Ask what their own projects are doing right now.")

d.bullets("How to split properly", [
    "Split by **blocks, sites or dates** — never by individual pixels",
    "Add a **buffer** so patch-based models cannot see test pixels inside their training patches",
    "Block size should exceed the spatial autocorrelation range of the target",
    "Report which design you used; 'random 80/20' on pixels is a red flag to any reviewer",
], kicker="practical rules",
   notes="Notebook 20 shows the buffered block split for the CNN. Point out that this is not pedantry: "
         "a model that scores 0.96 in-window scored 0.84 outside it in that notebook.")

d.section("4. Design-based accuracy and area", "Olofsson et al. (2014) good practice")

d.bullets("Why the test set above is still optimistic", [
    "It contains only **pure** pixels — the easy ones, with mixed boundary pixels excluded",
    "Its class proportions follow the reference map, not the map being assessed",
    "It cannot give you **area** estimates, because it is not a probability sample of the map",
    "**Fix:** draw a random sample *from the map*, stratified by mapped class",
], kicker="two hidden biases",
   notes="This is the conceptual jump of the session: stop evaluating on leftover training data, and start "
         "sampling the map itself. Everything after this slide follows from that change.")

d.code("How many reference points do you need?", """
# Olofsson et al. (2014), Eq. 13 — target a standard error on overall accuracy
S_O = 0.015                                   # desired SE of OA (±0.03 at 95 %)
W   = mapped_area_fraction                    # per mapped class (strata weights)
U   = conjectured_user_accuracy               # a prior guess per class, e.g. 0.6-0.95

n = (np.sum(W * np.sqrt(U * (1 - U))) / S_O) ** 2     # total sample size
n_i = allocate(n, W, floor=50)                        # spread over strata, floor for rare classes
""", kicker="sample size",
   caption="Notebook 21: n = 677 points over five strata, with a 50-point floor per class",
   notes="The floor matters more than the formula: proportional allocation alone starves the rare class "
         "that the project usually cares about most.")

d.figure("Where the sample points land",
         FIG + "03_5_2_draw_the_sample_and_collect_referenc.png",
         caption="677 stratified random points drawn from the map's own classes",
         kicker="sampling design",
         notes="Each point must now be interpreted independently — in a real project by field visit or VHR "
               "photo-interpretation, blind to the map label. Here WorldCover plays that role.")

d.bullets("From sample counts to area-weighted estimates", [
    "Each stratum was sampled at a different rate, so counts must be reweighted by stratum area",
    "Estimated area proportion: **p̂_ij = W_i · n_ij / n_i+**",
    "Overall accuracy Ô = Σ p̂_jj ; user's Û_i = p̂_ii / p̂_i+ ; producer's P̂_j = p̂_jj / p̂_+j",
    "Error-adjusted area of class j = total area × p̂_+j, with a 95 % confidence interval",
    ("Pixel counting ignores commission and omission, so it is biased — this corrects it", 1),
], kicker="the estimators",
   notes="Walk the first formula slowly. The intuition: a point in a small stratum represents fewer hectares "
         "than a point in a large stratum, so it cannot count the same.")

d.table("Mapped area vs error-adjusted area", ["Class", "Mapped (ha)", "Adjusted (ha)", "95 % CI", "UA ± CI"], [
    ["Tree cover", "1 897", "2 320", "± 223", "0.687 ± 0.068"],
    ["Grassland", "1 150", "974", "± 173", "0.394 ± 0.092"],
    ["Cropland", "1 306", "1 250", "± 195", "0.407 ± 0.087"],
    ["Built-up & bare", "1 900", "1 804", "± 173", "0.737 ± 0.065"],
    ["Water", "921", "826", "± 135", "0.632 ± 0.102"],
], kicker="notebook 21, 677 sample points",
   notes="Tree cover is under-mapped by about 22 %: the adjusted estimate sits well outside the pixel count. "
         "This is the table a ministry or a reviewer actually wants to see.")

d.callout("Pure-pixel test set: OA 0.763.\nProbability sample of the same map: OA 0.595 ± 0.035.",
          "Same map, same day, two evaluation designs. The lower number is the honest one — it includes the "
          "mixed pixels at every boundary, which is where maps really fail.",
          kicker="the number that survives scrutiny",
          notes="Expect pushback: 'so should we report the worse number?' Yes — and explain why it is lower. "
                "A defensible 0.60 beats an indefensible 0.95 in the rubric and in the real world.")

d.figure_bullets("Accuracy depends on how mixed the pixel is",
                 FIG + "04_5_3_analysis_area_weighted_error_matrix_.png",
                 ["Agreement by WorldCover purity of the 30 m pixel:",
                  ("purity 1–5 (very mixed): **0.337**", 1),
                  ("purity 6–8: **0.462**", 1),
                  ("purity 9 (pure): **0.736**", 1),
                  "At 30 m, most error lives at class boundaries, not in field interiors"],
                 caption="Area-weighted accuracy and area estimates with confidence intervals",
                 kicker="mixed pixels",
                 notes="This also explains the previous slide's drop. It is a property of 30 m data, not a "
                       "failure of the classifier — and it is why sub-pixel unmixing exists.")

d.bullets("Does the confidence interval actually work?", [
    "Notebook 21 simulates 1 000 repeated samples from a known population",
    "Stratified: mean OA estimate 0.636, **95 % CI covers the truth 95.3 %** of the time",
    "Simple random: 0.638, coverage 94.3 % — also unbiased for OA",
    "The gain from stratification shows up for the **rarest class**: tighter UA intervals with the same budget",
], kicker="a simulation you can trust",
   notes="Good moment to note that an interval is a promise about repeated sampling. If a team reports a CI, "
         "they should be able to say what it means.")

d.section("5. Continuous products", "When the output is a number, not a class")

d.figure_bullets("Agreement metrics for continuous maps",
                 FIG + "05_6_continuous_products_agreement_metrics.png",
                 ["**Bias** — systematic offset (the thing R² cannot see)",
                  "**MAE / RMSE** — typical error magnitude, RMSE punishes outliers",
                  "**R² about the 1:1 line** — not Pearson r², which ignores offset and slope",
                  "**Bland–Altman** — difference vs mean, reveals magnitude-dependent error"],
                 caption="Simulated Sentinel-2 vs Tanager indices over 20 000 land pixels",
                 kicker="the right four numbers",
                 notes="Ask what a high correlation with a constant offset would look like on each plot. "
                       "Bland-Altman is the one that makes it unmissable.")

d.table("The same comparison, four ways", ["Index", "Bias", "RMSE", "R² (1:1)", "Pearson r²"], [
    ["NDVI, S2-simulated vs Tanager", "−0.0285", "0.0296", "0.973", "0.999"],
    ["NDRE, S2-simulated vs Tanager", "+0.0102", "0.0114", "0.994", "0.999"],
], kicker="R² hides the offset",
   notes="Pearson r² is 0.999 for both — it would let you claim perfect agreement. The bias column shows NDVI "
         "is systematically lower by 0.03, enough to shift any threshold-based area estimate.")

d.figure_bullets("Cross-date consistency on stable targets",
                 FIG + "06_7_optional_cross_date_consistency_on_sta.png",
                 ["Compare two acquisitions over pixels that should not have changed",
                  "1 011 pseudo-invariant pixels between the two Malibu scenes",
                  "Relative RMSE **25–36 %** depending on wavelength",
                  "**Use:** a change smaller than that cannot be distinguished from noise"],
                 caption="Pseudo-invariant targets, December 2024 vs January 2025",
                 kicker="a measured detection threshold",
                 notes="This turns a vague 'there is some noise' into a number a change-detection project can "
                       "quote as its detection limit. Notebook 30 uses exactly this logic for dNBR.")

d.section("6. What to report", "Turning this into marks and into trust")

d.table("Minimum validation reporting for the project", ["Report", "Because"], [
    ["Sampling and response design, in words", "Shows the number is defensible"],
    ["Error matrix (counts) + per-class UA/PA/F1", "One OA hides class failures"],
    ["OA with a 95 % confidence interval", "A number without uncertainty is not a result"],
    ["Area-adjusted area if you quote hectares", "Pixel counting is biased"],
    ["Random vs spatial split comparison", "Proves you controlled for leakage"],
    ["A baseline (threshold or index)", "Shows what the complex model added"],
    ["Three failure cases, with the spectra", "Turns errors into understanding"],
], kicker="rubric: Validity, 30 %", col_widths=[3, 3],
   notes="This table is effectively the mark scheme for the largest rubric criterion. Assignment W3 asks for "
         "exactly these items, due before the interim review.")

d.handover("21_validation_accuracy_assessment.ipynb", [
    "Build the error matrix and compute UA, PA, F1 and IoU by hand, then check against scikit-learn",
    "Compare random and blocked cross-validation, and plot accuracy against block size",
    "Draw a stratified sample, then estimate area-adjusted accuracy and area with 95 % CIs",
    "Validate a continuous product with bias, RMSE and a Bland–Altman plot",
], minutes=100,
   notes="The area-adjusted section is the hard part; pair students up. Then apply it to their own project "
         "map for assignment W3.")

d.recap([
    "Sampling design, response design and analysis — all three, or the number means little",
    "Report the **error matrix and per-class** accuracies, not a single overall figure",
    "Kappa adds nothing; quantity and allocation disagreement say more",
    "**Spatially** independent splits, always; random pixel splits inflate accuracy",
    "Quote **area-adjusted** areas with confidence intervals, not pixel counts",
    "For continuous products, R² without bias and RMSE is a half-truth",
], next_up="Session 4 — Applied project development workshop, then the interim QA review",
   notes="Close on the honest-number slide: 0.763 became 0.595 and the map did not change.")

d.references([
    "Olofsson, P. et al. (2014). Good practices for estimating area and assessing accuracy of land change. RSE 148, 42–57.",
    "Stehman, S.V. & Foody, G.M. (2019). Key issues in rigorous accuracy assessment of land cover products. RSE 231, 111199.",
    "Pontius, R.G. & Millones, M. (2011). Death to Kappa. International Journal of Remote Sensing 32, 4407–4429.",
    "Foody, G.M. (2020). Explaining the unsuitability of the kappa coefficient. RSE 239, 111630.",
    "Congalton, R.G. & Green, K. (2019). Assessing the Accuracy of Remotely Sensed Data, 3rd ed. CRC Press.",
    "Bland, J.M. & Altman, D.G. (1986). Statistical methods for assessing agreement. The Lancet 327, 307–310.",
    "Roberts, D.R. et al. (2017). Cross-validation strategies for data with spatial dependence. Ecography 40, 913–929.",
])

d.save("w3c_validation_accuracy.pptx")
