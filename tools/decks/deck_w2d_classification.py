"""Week 2 · Session 4 — Classification approaches for hyperspectral data."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from deckbuild import Deck  # noqa: E402

F = "15_classification_classical/"

d = Deck("Classification approaches for hyperspectral data",
         "Week 2 · Session 4",
         notebook="15_classification_classical.ipynb",
         subtitle="From clusters to trained models — and how to know the accuracy is real",
         week="Week 2 · 9–12 November 2026")

# Run the 20-minute primer first: this session assumes the ML vocabulary it introduces.
d.prs.slides[0].notes_slide.notes_text_frame.text = (
    "Before this session, deliver slides/w2d0_ml_primer_for_eo.pptx (about 20 minutes).\n"
    "It introduces features and labels, training/validation/test, spatial splits, overfitting, "
    "hyperparameters and the confusion matrix, bridging from the ROI-and-maximum-likelihood workflow "
    "the participants already know. This deck assumes that vocabulary from the first slide onwards."
)

d.objectives([
    "Choose between unsupervised and supervised classification for a mapping task",
    "Explain where labels come from, and why labels are usually the hard part",
    "Select a feature set: raw spectra, PCA or MNF components, or indices",
    "Apply k-means, GMM, LDA, random forest and SVM, and read the results honestly",
    "Design a **spatially blocked** split, and say why a random split inflates accuracy",
], notes="This session is the workhorse of the course: most student projects end in a classifier. "
         "Stress that the modelling is the easy part — labels and evaluation are where projects fail. "
         "Ask who has trained a classifier before, on any data.")

d.section("1. The problem", "Turning 352 numbers per pixel into one class label")

d.bullets("What we are doing today", [
    "**Input:** one spectrum per pixel — 352 good bands after preprocessing",
    "**Output:** one class label per pixel, plus a confidence value",
    "**Scene:** Usulután, El Salvador — mangroves, tree cover, grassland, cropland, water",
    "**Reference:** ESA WorldCover 2021, aggregated to the 30 m Tanager grid",
    ("A 400 × 440 pixel window holds 173,721 valid pixels — a large training set by "
     "hyperspectral standards, and still a small one by deep-learning standards", 1),
], kicker="the set-up",
   notes="Point out the asymmetry: we have many pixels but few *independent* samples, because "
         "neighbouring pixels are nearly identical. That single fact drives the whole session.")

d.figure("The scene and its reference labels",
         F + "00_1_image_and_reference_labels.png",
         caption="Tanager true colour (left) and ESA WorldCover 2021 classes on the same grid",
         kicker="data and reference",
         notes="Ask the room to find the mangroves before showing the label map. Then point at the "
               "estuary edges — that is where every classifier in this session will make its mistakes.")

d.bullets("Two families of method", [
    "**Unsupervised** — the algorithm groups similar spectra; you name the groups afterwards",
    ("k-means, Gaussian mixture models, ISODATA. No labels needed, fast, exploratory", 1),
    "**Supervised** — you give labelled examples; the algorithm learns the mapping",
    ("LDA, k-NN, random forest, SVM, neural networks. Needs labels, usually much more accurate", 1),
    "**In practice you use both:** clustering to explore and to find classes you did not expect, "
    "then a supervised model for the product",
], kicker="unsupervised vs supervised",
   notes="A common student mistake is to run k-means and call the result a land-cover map. "
         "Clusters are spectral groups, not classes — the naming step is a human judgement.")

d.callout("A classifier is only as good as its labels.",
          "You can swap random forest for a transformer and gain a few points. Fix your labels and "
          "you can gain twenty. In this session the same model scores 0.89 or 0.48 depending on how "
          "the reference pixels were chosen.",
          kicker="the message of the day",
          notes="Foreshadow the label-noise experiment in part 3. Come back to this slide at the recap.")

d.section("2. Labels: the hard part", "Where they come from and what they cost")

d.bullets("Four ways to get labels, and what each costs", [
    "**Field survey** — the gold standard, geolocated and dated. Expensive, small, often seasonal",
    "**Visual interpretation** of very-high-resolution imagery. Cheap, but limited to classes you can see",
    "**Existing maps** (ESA WorldCover, Dynamic World, national land cover). Free and large — but made "
    "for another purpose, another year and another sensor",
    "**Weak or synthetic labels** — thresholds, unmixing, simulation. Useful when nothing else exists",
    ("Whatever you use, record the **source, date and definition** of each class in your metadata", 1),
], kicker="provenance matters",
   notes="Ask students which of these their own project can realistically afford. Most will end up with "
         "option three, which is exactly why the next slides matter.")

d.bullets("WorldCover as a weak label source", [
    "10 m global land cover for **2021**; our Tanager scenes are from **2024–2025**",
    "Aggregated to 30 m by majority vote of the nine 10 m cells inside each Tanager pixel",
    "**Purity** = how many of those nine cells agree (0–9). Purity 9 means a spectrally pure pixel",
    "Class definitions are WorldCover's, not ours — 'Cropland' includes bare fallow fields",
    "**Real change** between 2021 and 2025 appears as apparent classifier error",
], kicker="the course label set",
   notes="This is honest weak supervision, and it is what most teams will do. The trick is to know "
         "the failure modes before you report an accuracy number.")

d.table("Pure pixels available in the training window",
        ["WorldCover class", "All pixels", "Pure (9/9)", "Kept"],
        [["Mangroves", "62,335", "59,169", "yes"],
         ["Permanent water", "50,898", "48,333", "yes"],
         ["Grassland", "21,306", "15,037", "yes"],
         ["Tree cover", "20,231", "14,900", "yes"],
         ["Cropland", "16,551", "13,731", "yes"],
         ["Herbaceous wetland", "1,294", "603", "too few"],
         ["Built-up", "911", "359", "too few"],
         ["Bare / sparse vegetation", "163", "57", "too few"]],
        col_widths=[3, 1, 1, 1], kicker="class imbalance is normal",
        notes="Note how the purity filter costs little for big homogeneous classes and almost everything "
              "for small ones. Built-up drops to 359 pixels — too few to train or to trust.")

d.bullets("Class imbalance: what to do about it", [
    "Mangroves have **165 times** more pure pixels than built-up, and over 1,000 times more than bare ground",
    "An accuracy-maximising model will happily ignore the rare classes",
    "**Balance the training set** (we take 1,500 pixels per class) or weight the loss",
    "**Report per-class F1 and macro-F1**, never overall accuracy alone",
    "Merge classes you cannot support with data, and say so in the report",
], kicker="imbalance",
   notes="Macro-F1 averages classes equally, so rare classes count. Overall accuracy on this scene is "
         "flattered by water and mangrove, which are easy.")

d.section("3. Features", "Full spectrum, components, or a few indices?")

d.figure_bullets("Neighbouring bands say the same thing",
                 "13_feature_extraction_dim_reduction/01_2_why_reduce_dimensions_redundancy_and_t.png",
                 ["Adjacent Tanager bands correlate almost perfectly",
                  "352 bands carry far fewer than 352 independent dimensions",
                  "**Hughes phenomenon** (Hughes 1968): with a fixed training-set size, accuracy rises "
                  "then falls as dimensionality grows",
                  "Remedies: reduce dimensions, select bands, or use a model that tolerates redundancy"],
                 caption="Band-to-band correlation matrix, Konya window",
                 notes="Random forest and regularised LDA are fairly robust to redundancy; distance-based "
                       "methods such as k-NN suffer most. This figure comes from notebook 13.")

d.table("The same classifiers on four feature sets",
        ["Feature set", "LDA", "Random forest", "SVM (RBF)"],
        [["Full spectrum (352 bands)", "0.903", "0.895", "**0.912**"],
         ["PCA, 20 components", "0.891", "0.910", "0.897"],
         ["Simulated Sentinel-2 (12 bands)", "0.869", "0.893", "0.909"],
         ["Five broadband indices", "0.792", "0.839", "0.845"]],
        col_widths=[3, 1, 1, 1], kicker="overall accuracy, blocked split",
        notes="Read this table slowly. The jump from five indices to twelve bands is large; the jump from "
              "twelve bands to 352 is small. That is the honest finding for broad land-cover classes.")

d.callout("For broad land cover, the full spectrum beats simulated Sentinel-2 by 0.3 points.",
          "0.912 versus 0.909 overall accuracy. Hyperspectral data earns its keep on narrow-band "
          "problems — mineral species, pigments, gases, crop residue — not on separating water from trees.",
          kicker="an honest result",
          notes="Students often expect hyperspectral to win everything. Tell them the project rubric "
                "rewards reporting this kind of result honestly, and that notebooks 13 and 14 show "
                "the problems where the spectrum does win decisively.")

d.figure("Accuracy against feature set",
         F + "06_5_does_the_hyperspectral_detail_help.png",
         caption="Full spectrum · PCA-20 · simulated Sentinel-2 · five indices",
         kicker="the same result as a chart",
         notes="Ask: if the gain is this small, why did we buy a hyperspectral image? Answer: for the "
               "classes and quantities the broadband sensor cannot see at all.")

d.section("4. The classifiers", "Four models, one window")

d.bullets("Unsupervised: k-means and Gaussian mixtures", [
    "**k-means** assigns each spectrum to the nearest of *k* cluster centres, iteratively",
    "**GMM** fits Gaussian components and gives soft, probabilistic membership",
    "Both need *k* chosen in advance, and both are sensitive to scaling and to bright outliers",
    "Clusters must then be **named** — by majority overlap with reference data, or by an analyst",
    "Running with **more clusters than classes** and merging afterwards usually works better",
], kicker="no labels required",
   notes="The Hungarian algorithm does an optimal one-to-one cluster-to-class assignment; majority "
         "voting allows several clusters to map to one class, which is why k = 12 wins below.")

d.table("Unsupervised results on the test blocks",
        ["Method", "Overall accuracy", "Macro F1"],
        [["k-means, k = 5, one-to-one matching", "0.747", "0.724"],
         ["Gaussian mixture, k = 5, one-to-one", "0.672", "0.622"],
         ["k-means, k = 12, majority matching", "**0.801**", "**0.782**"]],
        col_widths=[3, 1, 1], kicker="clusters into classes",
        notes="Twelve clusters beat five because real classes are spectrally multi-modal: sunlit and "
              "shaded mangrove, turbid and clear water. One class, several clusters.")

d.figure("What the clusters look like",
         F + "02_3_unsupervised_classification.png",
         caption="k-means and GMM clusters mapped to the reference classes",
         kicker="unsupervised",
         notes="Point at the salt-and-pepper texture at class boundaries — a per-pixel method with no "
               "spatial context. Notebook 20 fixes this with patch-based models.")

d.bullets("Supervised: three workhorses", [
    "**LDA with shrinkage** — linear, closed-form, needs a regularised covariance in 352 dimensions",
    "**Random forest** — many decision trees on bootstrapped samples; robust, no scaling needed, "
    "gives feature importance",
    "**SVM with an RBF kernel** — maximum-margin boundary in a transformed space; **must** be scaled, "
    "and needs C and gamma tuned",
    "All three are strong baselines. Report one of them next to any deep model you build",
], kicker="the models",
   notes="Emphasise scaling for SVM: forgetting to standardise is the single most common bug in "
         "student SVM code, and it silently produces a weak model rather than an error.")

d.table("Supervised results on spatially separated test blocks",
        ["Model", "Overall accuracy", "Macro F1", "Fit time", "Predict 174k px"],
        [["SVM (RBF)", "**0.912**", "0.911", "0.4 s", "29 s"],
         ["LDA (shrinkage)", "0.903", "0.901", "0.04 s", "< 1 s"],
         ["Random forest", "0.895", "0.894", "3.3 s", "1 s"]],
        col_widths=[2, 1, 1, 1, 1], kicker="accuracy and cost",
        notes="The accuracy spread is 1.7 points; the prediction-time spread is thirty-fold. For a product "
              "that runs over whole scenes, that matters more than the third decimal of accuracy.")

d.figure("The maps the models produce",
         F + "04_4_1_mapping_the_whole_window.png",
         caption="Random forest and SVM predictions over the full window",
         kicker="from model to map",
         notes="Compare the two maps at the estuary. Differences cluster exactly where mixed pixels are, "
               "which is the honest limit of a 30 m per-pixel classifier.")

d.figure_bullets("Which wavelengths does the forest use?",
                 F + "05_4_2_which_wavelengths_does_the_random_fo.png",
                 ["Top bands: **531, 536, 561 nm** — pigment and green-peak region",
                  "**1112, 1327, 1332 nm** — NIR plateau and its edge, leaf structure and water",
                  "**1668–1688 nm** — SWIR, canopy water and dry matter",
                  "Importance is **smeared** across neighbouring correlated bands, so read regions, "
                  "not individual bands"],
                 caption="Random forest feature importance by wavelength",
                 notes="This is a sanity check on physics: if the model's important bands make no physical "
                       "sense, suspect leakage or an artefact rather than a discovery.")

d.section("5. Evaluation", "Making the accuracy number mean something")

d.figure_bullets("Split by space, not at random",
                 F + "01_2_a_spatially_separated_train_test_split.png",
                 ["Neighbouring pixels are nearly duplicates of each other",
                  "A random split puts near-duplicates in train **and** test",
                  "The score then measures memorisation, not generalisation",
                  "**Blocks** (here 50 px ≈ 1.5 km) keep the two sets genuinely apart",
                  "Add a **buffer** when the model sees neighbourhoods (patch CNNs, notebook 20)"],
                 caption="Spatial blocks: training, validation and test",
                 image_left=True,
                 notes="Roberts et al. 2017 and Ploton et al. 2020 document how large this bias can be in "
                       "ecological and EO models. Notebook 21 quantifies it for this scene.")

d.bullets("Reading a confusion matrix", [
    "Rows = reference class, columns = prediction (check the convention before you read anyone's matrix)",
    "**Diagonal** = correct. Everything else tells you *which* classes get confused, and that is the useful part",
    "**User's accuracy** = correct / predicted total — the map user's risk of a false positive",
    "**Producer's accuracy** = correct / reference total — how much of the real class was found",
    "Confusions here are systematic: grassland ↔ tree cover, and mangrove ↔ water at the estuary edge",
], kicker="beyond one number",
   notes="Have the class predict which pairs will be confused before showing the matrix. They usually "
         "get mangrove/water right and miss grassland/tree cover.")

d.figure_bullets("Label noise: it is the *test* labels that bite",
                 F + "07_6_label_noise_training_and_evaluating_wi.png",
                 ["Training on less pure labels barely hurt: 0.893 at purity 9, 0.885 at purity 1",
                  "Testing on less pure labels collapsed the score: **0.889 → 0.481**",
                  "The model did not get worse — the *yardstick* did",
                  "Mixed pixels have no single true class, so they cannot be scored fairly",
                  "**Report the purity of your reference data** alongside the accuracy"],
                 caption="Accuracy against the purity of training and of test labels",
                 notes="This is the most transferable lesson in the deck. A team reporting 0.48 may have a "
                       "fine model and a broken evaluation set. Random forest is quite tolerant of noisy "
                       "training labels because of bootstrapping and voting.")

d.bullets("Confidence, and knowing when not to trust the map", [
    "Random forest gives a vote fraction; SVM and neural nets give scores you can calibrate",
    "Mean confidence by class here: water **0.98**, mangrove **0.97**, cropland 0.84, "
    "tree cover 0.83, grassland **0.75**",
    "Low-confidence pixels concentrate at class boundaries and in mixed pixels",
    "Ship the confidence layer with the map, and let the user threshold it",
    ("Confidence is not calibrated probability unless you calibrate it — see notebook 21", 1),
], kicker="uncertainty",
   notes="Grassland's 0.75 matches its weak F1 and its confusion with tree cover. The confidence layer "
         "told us where the problem was without any reference data at all.")

d.code("Exporting the map as a product",
       """
# classes + confidence, written as a Cloud-Optimised GeoTIFF on the scene's own grid
hu.save_geotiff(
    out_dir / f"{scene.scene_id}_rf_classes.tif",
    classes.astype("uint8"),
    scene.transform(WINDOW), scene.crs,
    band_names=["worldcover_class"],
)
# → EPSG:32616, 30 m pixels, 400 x 440, layout: COG
       """,
       kicker="deliverable",
       caption="A map that is not georeferenced, with no metadata, is not a product (notebook 31).",
       notes="Insist on CRS, transform and band descriptions in every exported layer. The submission "
             "checklist requires it.")

d.handover("15_classification_classical.ipynb", [
    "Run k-means and a GMM, then map the clusters onto classes two different ways",
    "Train LDA, random forest and SVM on a spatially blocked split and compare per-class F1",
    "Repeat with simulated Sentinel-2 bands and with five indices — quantify the hyperspectral gain",
    "Rerun the label-noise experiment and explain the training/test asymmetry in your own words",
    "Export your best map as a COG with a confidence band",
], minutes=120,
   notes="Then set assignments/assignment_w2_detection_classification.md, due at the start of Week 3. "
         "Warn them the SVM prediction step over the full window takes about half a minute.")

d.recap([
    "Unsupervised finds **clusters**, not classes; use more clusters than classes and merge",
    "**Labels dominate**: source, date, class definition and purity decide your accuracy",
    "For broad land cover the full spectrum gains little over Sentinel-2 bands — say so honestly",
    "**Blocked splits** give the number that transfers to a new area; random splits flatter you",
    "Report per-class F1, a confusion matrix and a confidence layer, never one number alone",
], next_up="Session 5 — Project scoping and use case definition (notebook 16 and the scoping canvas)",
   notes="Close on the callout slide: a classifier is only as good as its labels.")

d.references([
    "Hughes, G.F. (1968). On the mean accuracy of statistical pattern recognizers. IEEE Trans. Inf. Theory 14, 55–63.",
    "Breiman, L. (2001). Random forests. Machine Learning 45, 5–32.",
    "Melgani, F. & Bruzzone, L. (2004). Classification of hyperspectral remote sensing images with SVMs. IEEE TGRS 42, 1778–1790.",
    "Roberts, D.R. et al. (2017). Cross-validation strategies for data with spatial, temporal, phylogenetic or hierarchical structure. Ecography 40, 913–929.",
    "Ploton, P. et al. (2020). Spatial validation reveals poor predictive performance of large-scale ecological mapping models. Nature Communications 11, 4540.",
    "Zanaga, D. et al. (2022). ESA WorldCover 10 m 2021 v200 (CC-BY 4.0).",
    "Course material: notebook 15, quiz quizzes/quiz_w2_features_detection_classification.md, assignment assignments/assignment_w2_detection_classification.md",
])

d.save("w2d_classification.pptx")
