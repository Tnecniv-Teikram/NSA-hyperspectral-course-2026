"""Week 2 · Session 4 (pre-session) — Machine learning in 20 minutes, for multispectral analysts."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from deckbuild import Deck  # noqa: E402

F15 = "15_classification_classical/"
F20 = "20_geoai_deep_learning/"
F21 = "21_validation_accuracy_assessment/"

d = Deck("Machine learning in 20 minutes",
         "Week 2 · Session 4",
         notebook="15_classification_classical.ipynb",
         subtitle="For multispectral analysts: the vocabulary is new, the workflow is not",
         week="Week 2 · 9–12 November 2026")

d.objectives([
    "Map the machine-learning vocabulary onto the classification work you already do",
    "Explain what training, validation and test data are, and why EO needs a **spatial** split",
    "Recognise overfitting from its signature, and name its usual causes and cures",
    "Tell a parameter from a hyperparameter, and know which you are allowed to tune on what",
    "Read a confusion matrix in both languages: commission/omission and precision/recall",
], notes="Twenty minutes, no equations, no code. The aim is that nobody meets a word for the first time "
         "in the practical. Ask who has run a supervised classification in ENVI, SNAP, ERDAS or QGIS — "
         "usually most hands go up, and that is the foundation this whole session is built on.")

d.section("1. You have already done this", "Only the names are unfamiliar")

d.table("Your vocabulary, and the machine-learning word for it",
        ["What you do today", "What it is called here", "Note"],
        [["Digitise ROIs / training polygons", "labelling", "the label is the class you assign to a pixel"],
         ["Collect spectra inside those ROIs", "building a training set", "each pixel becomes one sample"],
         ["Run maximum likelihood / minimum distance", "fitting a model", "the algorithm learns the rule"],
         ["Apply the signature to the whole image", "inference / prediction", "same model, unseen pixels"],
         ["Accuracy assessment on check points", "evaluation on a test set", "must be independent data"],
         ["Commission and omission error", "precision and recall", "same numbers, different names"],
         ["Separability (Jeffries-Matusita, divergence)", "class separability", "still the same question"]],
        col_widths=[3, 2, 3], kicker="a translation table",
        notes="Spend real time here — this slide is why the session works. Invite people to call out the "
              "software they use. The message: you are not starting from zero, you are renaming a workflow "
              "you have run many times, and then automating it.")

d.bullets("Features and labels", [
    "A **feature** is any number describing a pixel. With Sentinel-2 you might use 4 bands plus NDVI",
    "With Tanager, the **whole spectrum is the feature vector** — 352 numbers per pixel",
    "A **label** is the class you want predicted: mangrove, cropland, water",
    "**Band maths**: you write the rule yourself — *NDVI > 0.4 is vegetation*",
    "**Machine learning**: you give examples and the algorithm writes the rule, including rules across "
    "350 bands that nobody would write by hand",
    ("That is the whole difference. Everything else today is about trusting the rule it wrote", 1),
], kicker="the two words you need first",
   notes="The honest framing: ML is not magic, it is automated rule-writing. A threshold on NDVI *is* a "
         "classifier — a very small one you fitted by eye. Ask what rule they would write by hand for "
         "mangrove versus other tree cover; the room usually concedes it is hard, which is the point.")

d.section("2. Training, testing and the trap", "Why your accuracy number is usually too good")

d.bullets("Training, validation and test — three jobs, three sets", [
    "**Training set** — the examples the model learns from",
    "**Validation set** — used while you choose settings and decide when to stop",
    "**Test set** — touched **once**, at the end, to report accuracy",
    "Scoring a model on its training pixels is like marking an exam with the answer sheet the student "
    "revised from: it measures memory, not understanding",
    ("If you tune anything by looking at the test set, it stops being a test set", 1),
], kicker="three sets",
   notes="The exam analogy lands well. Stress the one-shot nature of the test set: every time you peek and "
         "adjust, you leak information. In projects this is the most common silent mistake, and it is "
         "invisible in the final numbers.")

d.figure_bullets("In EO, neighbouring pixels are nearly the same pixel",
                 F15 + "01_2_a_spatially_separated_train_test_split.png",
                 ["A random pixel split puts a pixel in training and its neighbour in test",
                  "They share the same field, the same shadow, often the same mixed signal",
                  "So the model is tested on data it has effectively already seen",
                  "**Fix:** split by spatially separated **blocks**, not by pixels",
                  "This is the one change that matters most in an EO classification"],
                 caption="Blocked split: orange = test blocks, cyan/magenta = sampled pixels",
                 kicker="spatial autocorrelation",
                 notes="This is the EO-specific part that general ML courses never mention. Connect it to "
                       "their own practice: good accuracy assessment already demands independent check "
                       "points, often from a different site or date — this is the same instinct, formalised.")

d.callout("A model that memorises your training pixels looks brilliant and maps badly.",
          "That is overfitting. It fits the noise and the particular pixels it saw, instead of the pattern "
          "that generalises to the rest of the scene — and it is the default outcome when you have many "
          "bands and few labelled pixels.",
          kicker="the word you will hear all week",
          notes="Say the definition slowly, then give the human version: a student who memorised past "
                "exam papers rather than learning the subject. Everything in the next two slides is about "
                "spotting it and preventing it.")

d.figure("The same map, two honest-looking numbers",
         F21 + "02_4_random_vs_spatial_cross_validation.png",
         caption="Random cross-validation says 0.81; blocked cross-validation at 1.5 km says 0.76",
         kicker="measured on our own data",
         notes="Both numbers come from the same model and the same scene — only the split changed. The "
               "gap is the optimism you are buying with a random split. Ask which number they would put "
               "in a report for a client, and why. Notebook 21 reproduces this plot.")

d.bullets("Overfitting: the signature, the causes, the cures", [
    "**Signature:** training accuracy keeps rising while validation accuracy flattens, then falls",
    "**Cause 1 — too many features, too few labels.** 352 bands need a great many examples; "
    "this is the *Hughes phenomenon* you will meet in notebook 13",
    "**Cause 2 — leaky splits.** Neighbouring pixels in both sets (previous slide)",
    "**Cause 3 — tuning on the test set.** Peeking, then adjusting",
    "**Cures:** fewer or better features (PCA, MNF, band selection), more and better labels, "
    "simpler models, regularisation, early stopping",
    ("A random forest on 20 good features usually beats a deep network on 352 noisy ones", 1),
], kicker="diagnosis and treatment",
   notes="In the practical they will watch validation accuracy diverge in notebook 20's training curves — "
         "tell them to look for it. The last bullet is the honest one and sets up the baseline message.")

d.bullets("Parameters and hyperparameters", [
    "**Parameters** are what the model learns from data: the split thresholds in a tree, the weights "
    "in a network. You never set these by hand",
    "**Hyperparameters** are what *you* choose before fitting: how many trees (`n_estimators`), "
    "SVM's `C` and `gamma`, the learning rate, dropout, patch size",
    "They change how the model learns, so they change the result — sometimes a lot",
    "**Tune them on validation data, never on the test set**",
    "Sensible defaults go a long way: the course notebooks use them and say so",
    ("If you report an accuracy, report the hyperparameters that produced it", 1),
], kicker="what you choose vs what it learns",
   notes="This word appears in every library's documentation and was missing from the course until now. "
         "Reassure them: nobody is expected to tune by hand this week — but they must know which knobs "
         "exist, and that turning them while looking at the test set invalidates the test.")

d.section("3. Reading the result", "The numbers you already know, in new clothes")

d.figure_bullets("The confusion matrix is your error matrix",
                 F15 + "03_4_supervised_classification.png",
                 ["Rows are reference classes, columns are what the model predicted",
                  "**Producer's accuracy = recall** — of the real mangrove, how much did we find?",
                  "**User's accuracy = precision** — of what we called mangrove, how much really is?",
                  "**F1** combines the two into one number per class",
                  "Read the **off-diagonal** cells: 12 % of tree cover predicted as grassland is a "
                  "real, explainable confusion, not a bug"],
                 caption="Random forest and SVM on the El Salvador scene, row-normalised",
                 kicker="same table, new names",
                 notes="Start in their language — commission and omission — then overlay precision and "
                       "recall. Emphasise that the interesting information is off the diagonal: which "
                       "classes get mixed, and whether that mixture makes physical sense.")

d.bullets("Why overall accuracy flatters a map", [
    "Our scene is roughly **45 % water and 40 % mangrove** — both easy, both large",
    "A model that got every small class wrong could still report ~85 % overall accuracy",
    "**Report per-class F1 and macro-F1**, which average classes equally, alongside overall accuracy",
    "Balance the training set or weight the classes so rare classes are learned at all",
    "Say which classes you could not support with enough reference data, and drop them honestly",
], kicker="class imbalance",
   notes="Ask: if a client wants a mangrove map, which number tells them whether it works? Not overall "
         "accuracy. This is the habit that separates a credible map from a pretty one.")

d.table("The methods you will meet this week",
        ["Method", "Needs labels?", "Use it when"],
        [["k-means / GMM", "no", "exploring, finding structure you did not expect"],
         ["LDA", "yes", "a fast, well-behaved baseline on few features"],
         ["Random forest", "yes", "the default first choice: robust, handles many bands, gives importances"],
         ["SVM (RBF)", "yes", "few training samples, high dimensions, clean classes"],
         ["1D-CNN", "yes", "the spectrum has shape worth learning; you have thousands of labels"],
         ["Patch CNN (3D)", "yes", "spatial context matters as much as the spectrum"]],
        col_widths=[2, 1, 4], kicker="a map of the week",
        notes="Read the table top to bottom as increasing cost, not increasing quality. In notebook 20 the "
              "patch CNN does win on this scene — macro-F1 0.925 against 0.861 for the random forest — but "
              "it costs labels, compute and explainability, and the gap is smaller than most people expect.")

d.recap([
    "You already know the workflow: ROIs, fitting, prediction, accuracy assessment",
    "**Features** describe a pixel, **labels** are what you want predicted",
    "Train, validate and test on **spatially separated** data, or your accuracy is fiction",
    "**Overfitting** = memorising the training pixels; watch validation accuracy to catch it",
    "**Hyperparameters** are your choices — tune on validation, never on test",
    "Report **per-class** numbers, not just overall accuracy",
    "**Ask about any word you do not recognise** — today and all week. Nobody should nod along",
], next_up="Classification approaches for hyperspectral data (notebook 15)",
   notes="Close on the last bullet and mean it: the fastest way to lose a mixed-background room is to let "
         "unfamiliar vocabulary pass unchallenged. Invite questions now, before the practical starts.")

d.references([
    "Hughes, G.F. (1968). On the mean accuracy of statistical pattern recognizers. IEEE Trans. Inf. Theory 14, 55–63.",
    "Congalton, R.G. & Green, K. (2019). Assessing the Accuracy of Remotely Sensed Data, 3rd ed. CRC Press.",
    "Roberts, D.R. et al. (2017). Cross-validation strategies for data with spatial, temporal, phylogenetic "
    "or hierarchical structure. Ecography 40, 913–929.",
    "Olofsson, P. et al. (2014). Good practices for estimating area and assessing accuracy of land change. RSE 148, 42–57.",
    "Breiman, L. (2001). Random forests. Machine Learning 45, 5–32.",
    "Course notebooks: 15 (classification), 20 (deep learning), 21 (validation).",
])

d.save("w2d0_ml_primer_for_eo.pptx")
