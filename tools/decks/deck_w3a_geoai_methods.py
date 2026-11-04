"""Week 3 · Session 1 — GeoAI methods for hyperspectral applications."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from deckbuild import Deck  # noqa: E402

F = "20_geoai_deep_learning/"

d = Deck("GeoAI methods for hyperspectral applications",
         "Week 3 · Session 1",
         notebook="20_geoai_deep_learning.ipynb",
         subtitle="Deep learning on spectra and patches — what it adds, and where it breaks",
         week="Week 3 · 16–19 November 2026")

d.objectives([
    "Choose between pixel, patch and scene models for a hyperspectral task",
    "Explain how 1D, 2D and 3D convolutions use spectral and spatial information",
    "Say what a **loss**, a **gradient step** and an **epoch** actually are, and read a training curve",
    "Set up training that does not fool you: blocked splits, buffers, class weights, early stopping",
    "Describe what foundation models and self-supervised pre-training offer, and their limits",
    "Recognise **domain shift** and quantify it before deploying a model elsewhere",
], notes="Week 2 ended with random forest at 0.895. Today we ask what deep learning adds — and the "
         "honest answer is: a few points here, and a large new set of ways to deceive yourself. "
         "Set that expectation at the start.")

d.section("1. What GeoAI adds", "Three ways to look at a hyperspectral cube")

d.callout("Classical models see a list of numbers.\nDeep models can see a neighbourhood.",
          "A random forest treats each pixel's 352 bands as an unordered feature vector. A convolutional "
          "network knows that band 120 sits next to band 121, and that this pixel sits next to that one.",
          kicker="the core idea",
          notes="Both facts — spectral ordering and spatial context — are information the classical "
                "model throws away. That is where the gain comes from, and also where leakage comes from.")

d.table("Three model families",
        ["Family", "Input", "Typical architectures", "Main weakness"],
        [["Pixel / spectral", "one spectrum (~350 values)",
          "RF, SVM, 1D-CNN, SpectralFormer (Hong et al. 2022)", "no spatial context, salt-and-pepper maps"],
         ["Patch / spectral–spatial", "small cube, e.g. 9 × 9 × bands",
          "2D-CNN on PCA, 3D-CNN (Chen et al. 2016), HybridSN (Roy et al. 2020)",
          "leakage risk, more compute, blurred boundaries"],
         ["Scene / segmentation", "a whole tile, e.g. 128 × 128",
          "Fully convolutional nets, U-Net, segmentation transformers",
          "needs *dense* labels — rare in hyperspectral"]],
        col_widths=[1, 1, 2, 2], kicker="pixel · patch · scene",
        notes="Most hyperspectral projects live in the first two rows. The third needs wall-to-wall "
              "labelled maps, which almost nobody has for a tasked 30 m sensor.")

d.section("2. How a network actually learns", "Weights, loss, one small step — repeated")

d.bullets("A layer is weights and a non-linearity", [
    "A **layer** multiplies its inputs by a table of numbers (**weights**), adds an offset, then passes the "
    "result through a simple non-linear function",
    "Stack a few layers and the network can represent shapes a single band ratio cannot",
    "**Training = choosing the weights.** Nothing else about the model changes",
    "You already use a fixed-weight model: NDVI is (+1, −1) on two bands, chosen by a human in 1973",
    ("Our 1D-CNN holds **42,309** such numbers; HybridSN holds **265,349**", 1),
], kicker="the building block",
   notes="This is the slide that demystifies the whole thing. Say plainly: a trained model is a big list of "
         "numbers, and training is a search for good values. The NDVI comparison usually lands well with this "
         "audience — they have been using a hand-designed one-layer model for their whole career.")

d.bullets("The loss: one number for how wrong the model is", [
    "Show the network a **batch** of pixels, let it guess, and score the guesses with a **loss function**",
    "For classification we use **cross-entropy**: it is small when the right class gets a high probability, "
    "and large when the model is confidently wrong",
    "Our loss is **class-weighted**, so a mistake on cropland (2,166 training pixels) costs more than one "
    "on mangrove (33,995)",
    "The loss is what the optimiser minimises — but it is *not* the number you report",
    ("Judge the model on **macro-F1** over a blocked test set; watch the loss only to see if training is working", 1),
], kicker="the score the model optimises",
   notes="Draw the distinction early and repeat it: loss is the training signal, accuracy metrics are the "
         "evaluation. A beginner who conflates them will tune towards a lower loss and a worse map.")

d.bullets("One gradient step, and the learning rate", [
    "Compute the loss on one batch, then ask: **which way should each weight move to make it smaller?**",
    "That direction is the **gradient**; computing it backwards through the layers is *backpropagation*",
    "Nudge every weight a little in that direction — one **gradient step**. That is the whole algorithm",
    "The **optimiser** (we use Adam) decides the step; the **learning rate** (1e-3 here) sets its size",
    "Too large and the loss jumps around; too small and it crawls. It is the first thing to adjust",
], kicker="how the weights change",
   notes="The fog analogy works: you cannot see the valley floor, but you can feel which way is downhill, so "
         "you take a step and feel again. Mention that 1e-3 with Adam is a sane default for small models — "
         "they do not need to derive anything, just recognise the knob.")

d.table("Epoch, batch and iteration — in this notebook's numbers",
        ["Term", "What it means", "In notebook 20"],
        [["Batch", "the group of pixels scored before one weight update", "128 pixels"],
         ["Iteration", "one batch in, one gradient step out", "~57 per epoch"],
         ["Epoch", "one pass through all the training data", "7,332 training pixels"],
         ["Training run", "epochs until it stops improving", "stopped at 12 of a possible 40"],
         ["Total updates", "iterations × epochs", "~690 gradient steps"]],
        col_widths=[1, 3, 1.4], kicker="the vocabulary, made concrete",
        notes="Having the real numbers on screen stops 'epoch' from sounding mysterious. Point out that 690 "
              "updates is tiny by deep-learning standards — which is exactly why the random forest stays "
              "competitive here, and why the models train in under a minute on a laptop.")

d.bullets("Dropout, batch normalisation, weight decay", [
    "**Dropout** switches off a random share of units each batch (0.3 and 0.4 in our models), so the network "
    "cannot lean on any single feature — it is the main brake on overfitting",
    "**Batch normalisation** rescales each layer's outputs to a stable range, which makes training faster "
    "and far less sensitive to the learning rate",
    "**Weight decay** (1e-4) gently pulls weights towards zero, preferring simpler solutions",
    "All three fight the same enemy: a model that memorises 7,332 pixels instead of learning spectra",
    ("Later, dropout earns a second job: left on at prediction time it gives the MC-dropout uncertainty "
     "you will map in section 5", 1),
], kicker="the three regularisers in our models",
   notes="These three appear in the notebook's model definitions and are otherwise black boxes. One line each "
         "is enough — the point is that they are deliberate choices against overfitting, not magic incantations.")

d.figure_bullets("Reading the training curves",
                 F + "02_6_model_2_a_spectral_spatial_patch_cnn_h.png",
                 ["Left: **training** loss. Right: **validation** macro-F1 — the one that matters",
                  "HybridSN's loss falls to 0.03 while its validation score stops improving: that gap is "
                  "**overfitting**",
                  "**Early stopping** keeps the best epoch (7, macro-F1 0.927) and gives up after a few more",
                  "Safe to change: learning rate, epochs, patch size, number of PCA components",
                  "Leave alone until the curves make sense: layer counts, kernel sizes, the optimiser"],
                 caption="Both models, 12 epochs, class-weighted loss",
                 image_left=True,
                 notes="Walk the shape out loud: falling loss plus a flat validation curve means it is "
                       "memorising. Ask what they would do if validation F1 were still climbing at epoch 12 "
                       "(train longer). This slide is the one to return to when their own training looks odd.")

d.section("3. The families in detail", "What each architecture does with a hyperspectral cube")

d.bullets("1D-CNN: convolving along the spectrum", [
    "Kernels slide along the **wavelength axis**, learning shapes: slopes, peaks, absorption dips",
    "Equivalent to learning the band-maths that indices hard-code, but fitted to your data",
    "Small and fast: our model has **42,309 parameters** and trains in about 40 seconds on a laptop CPU",
    "Applies to any pixel of any scene — no neighbourhood needed, so no patch-leakage risk",
    ("Input must be standardised per band, or the first layer is dominated by the brightest region", 1),
], kicker="spectral models",
   notes="A useful framing: NDVI is a hand-designed one-layer network with two inputs. The 1D-CNN "
         "learns hundreds of such combinations and how to weigh them.")

d.bullets("3D and hybrid networks: adding the neighbourhood", [
    "A **3D convolution** moves a kernel through rows, columns *and* wavelengths at once",
    "**HybridSN** (Roy et al. 2020): a few 3D layers for spectral–spatial features, then 2D layers for texture",
    "Almost always run on **PCA-reduced** bands — 30 components here explain 99.99 % of the variance",
    "Our patch model has **265,349 parameters**, six times the 1D-CNN, and still trains in ~35 s",
    "Smoother, more accurate maps — at the cost of blurred class boundaries and mixed-pixel errors",
], kicker="spectral–spatial models",
   notes="Ask why PCA first: a 3D convolution over 352 bands is expensive and mostly redundant. "
         "Thirty components keep the information and cut the compute by an order of magnitude.")

d.bullets("Attention and transformers", [
    "Self-attention lets every band (or patch) weigh every other, instead of only its neighbours",
    "**SpectralFormer** (Hong et al. 2022) treats groups of adjacent bands as tokens",
    "Strong when relationships are **long-range** — a feature at 700 nm modulating one at 2200 nm",
    "Data-hungry: with a few thousand labelled pixels, a CNN or even a random forest often wins",
    ("Rule of thumb: try the simple model first and make the complex one prove its worth", 1),
], kicker="the newer family",
   notes="Do not oversell transformers here. In the label-limited regime that dominates this course, "
         "they rarely beat a well-tuned CNN, and they are much harder to train.")

d.section("4. Making it work", "The parts that decide whether your number is real")

d.figure("The data: a Tanager window and its labels",
         F + "00_2_data_a_tanager_window_and_worldcover_l.png",
         caption="El Salvador, 400 × 400 px, 352 good bands, five WorldCover classes (pure pixels only)",
         kicker="the practical set-up",
         notes="Same scene as notebook 15, so today's numbers are directly comparable with the random "
               "forest baseline from Week 2.")

d.figure_bullets("Split by blocks, and buffer the patches",
                 F + "01_3_a_spatial_train_validation_test_split_.png",
                 ["Blocks of 50 px (1.5 km) assigned to train, validation and test",
                  "A **9 × 9 patch** centred near a block edge reaches into the next block",
                  "So we also drop pixels whose full patch is not inside one split — the **buffer**",
                  "Without it, test patches literally contain training pixels",
                  "This is the single most common way to publish an inflated accuracy"],
                 caption="Spatial blocks with a buffer for patch models",
                 image_left=True,
                 notes="Roberts et al. 2017 and Ploton et al. 2020 document the inflation. Notebook 21 "
                       "measures it directly: random splits can look several points better than reality.")

d.bullets("Training essentials, in order of how often they are forgotten", [
    "**Standardise** inputs per band, using statistics from the *training* set only",
    "**Class weights** or balanced sampling — our classes range from 9,993 to 57,479 pure pixels",
    "**Early stopping** on a validation set: both our models stopped after 12 epochs",
    "**Fix every seed** (numpy, torch) and record it, or your results are not reproducible",
    "Monitor **macro-F1**, not loss, and not overall accuracy",
], kicker="the checklist",
   notes="Ask what happens if you standardise using the whole dataset: test statistics leak into "
         "training. It is a small leak compared with spatial leakage, but it is free to avoid.")

d.bullets("Label scarcity is the real constraint", [
    "Our training set is 7,332 pixels — large for hyperspectral, tiny for deep learning",
    "Labels are **weak**: ESA WorldCover 2021 versus Tanager imagery from 2025",
    "Deep models with 10⁵–10⁶ parameters overfit such sets easily",
    "Mitigations: augmentation, class weighting, early stopping, smaller models — and pre-training",
    "**Always report a random forest next to your deep model**",
], kicker="why the baseline matters",
   notes="This bullet list is the argument for the foundation-model section later: if labels are the "
         "bottleneck, the leverage is in using unlabelled data.")

d.section("5. What the models actually did", "Measured on spatially separated test blocks")

d.table("Three models, one window, blocked test set",
        ["Model", "Parameters", "Training time", "Overall accuracy", "Macro F1"],
        [["Random forest (baseline)", "—", "2.5 s", "0.925", "0.861"],
         ["1D-CNN on spectra", "42,309", "41 s", "0.940", "0.892"],
         ["HybridSN, 9 × 9 patches", "265,349", "35 s", "**0.959**", "**0.925**"]],
        col_widths=[2, 1, 1, 1, 1], kicker="the honest comparison",
        notes="Macro-F1 rises from 0.861 to 0.925 — a real gain, earned mostly on the hard classes. "
              "All three trained on a laptop CPU in under a minute.")

d.figure("Where the gain actually came from",
         F + "03_7_honest_comparison_on_the_test_blocks.png",
         caption="Per-class F1 on the test blocks: random forest, 1D-CNN, HybridSN",
         kicker="per-class results",
         notes="Water and mangrove were already above 0.97 for every model — there was nothing to win. "
               "Grassland went 0.646 → 0.720 → 0.804, and cropland 0.851 → 0.960. Spatial context helps "
               "exactly where spectra alone are ambiguous.")

d.figure("From model to map",
         F + "05_8_from_model_to_map.png",
         caption="True colour, reference labels, confidence, and the three model maps",
         kicker="the visual check",
         notes="Compare the salt-and-pepper texture of the per-pixel models with the smoother patch model. "
               "Ask which they would rather hand to a user — and what the smoothing costs at boundaries.")

d.figure_bullets("Confidence and uncertainty",
                 F + "06_9_mc_dropout_uncertainty.png",
                 ["Max softmax is a **confidence score**, not a calibrated probability",
                  "**MC dropout**: run the network several times with dropout active and look at the spread",
                  "Ten passes over 16,900 pixels took 32 s",
                  "High uncertainty concentrates at class boundaries and mixed pixels",
                  "Ship the uncertainty layer; let the user decide the threshold"],
                 caption="Monte-Carlo dropout uncertainty on a sub-window",
                 notes="Softmax over-confidence is well documented (Guo et al. 2017). Treat these maps as "
                       "'where the model is unsure', which is useful even when uncalibrated.")

d.figure("Scaling to the whole scene",
         F + "07_10_sliding_window_tiled_inference_over_t.png",
         caption="Tiled sliding-window inference over 655 × 785 pixels, 88 s on CPU",
         kicker="inference at scale",
         notes="Tiling with a halo keeps memory bounded and avoids edge artefacts. The same pattern "
               "appears in notebooks 30 and 31 for production runs.")

d.section("6. Where it breaks", "Domain shift, and the limits of a trained model")

d.figure("Does the model travel?",
         F + "08_11_domain_shift_does_the_model_travel.png",
         caption="The El Salvador model applied to Ho Chi Minh City",
         kicker="domain shift",
         notes="Let the room look at this before you give the numbers. The map looks plausible at a "
               "glance, which is exactly the danger.")

d.table("The same models, three test sets",
        ["Test set", "Random forest", "1D-CNN", "HybridSN"],
        [["El Salvador, blocked test", "0.925", "0.940", "0.959"],
         ["Rest of the same scene", "—", "—", "0.843"],
         ["Ho Chi Minh City", "0.261", "0.334", "0.335"],
         ["…of which predicted 'mangrove'", "41 %", "44 %", "0 %"]],
        col_widths=[2, 1, 1, 1], kicker="accuracy collapses off-domain",
        notes="Two separate lessons. First, even within the same scene, accuracy drops from 0.959 to "
              "0.843 outside the training window. Second, in a new city it collapses entirely.")

d.callout("The random forest labelled 41 % of Ho Chi Minh City as mangrove.",
          "Different species, background, atmosphere, illumination and class definitions. The model was "
          "never wrong about El Salvador — it was simply asked a question outside its experience.",
          kicker="domain shift, in one number",
          notes="Interesting detail worth mentioning: the patch model predicted no mangrove at all in "
                "HCMC — it used spatial texture that simply does not occur there. Different failure "
                "mode, equally wrong.")

d.bullets("Living with domain shift", [
    "Validate in the domain you will deploy in — a new site, a new date, a new sensor",
    "Collect a small number of **local labels**; even a few hundred help a great deal",
    "Consider domain adaptation, fine-tuning, or simply retraining per scene",
    "Use the **confidence layer** as an early warning: off-domain data often looks uncertain",
    "State the validated domain in your metadata, as notebook 31's product does",
], kicker="what to do about it",
   notes="Link forward to the mangrove product in notebook 31, whose metadata records exactly where the "
         "model was validated and flags runs outside it.")

d.section("7. Foundation models", "Using unlabelled data to fix the label bottleneck")

d.bullets("Self-supervised pre-training, in one slide", [
    "Pre-train on a **large unlabelled archive** with a pretext task — masked reconstruction, or "
    "matching two views of the same place",
    "The model learns general spectral–spatial structure without any labels",
    "Then **fine-tune** on your few thousand labelled pixels, or train a small classifier on its embeddings",
    "The promise: far fewer labels for the same accuracy",
    ("The field moves fast — check current versions and benchmarks before committing", 1),
], kicker="the idea",
   notes="This is the most likely direction for a team with very few labels. Be clear that it is an "
         "active research area, not a solved, push-button workflow.")

d.table("Models you will meet in the literature",
        ["Model", "Pre-trained on", "Note for us"],
        [["HyperSIGMA (Wang et al. 2024/25)", "Hyperion and GaoFen-5 hyperspectral", "genuinely hyperspectral"],
         ["SpectralEarth (Braham et al. 2024/25)", "EnMAP patches", "closest sensor to Tanager"],
         ["SpectralGPT (Hong et al. 2024)", "Sentinel-2 multispectral", "despite the name, not hyperspectral"],
         ["Prithvi (Jakubik et al. 2023)", "Harmonized Landsat–Sentinel-2, 6 bands", "multispectral"],
         ["DOFA (Xiong et al. 2024)", "multiple sensors, wavelength-aware", "can ingest varied band sets"]],
        col_widths=[2, 2, 2], kicker="read the fine print",
        notes="The recurring trap is assuming that a 'spectral' foundation model is hyperspectral. "
              "Two of these five are multispectral. Check what the model was actually trained on.")

d.bullets("Sensor mismatch: the practical catch", [
    "A model pre-trained on Sentinel-2 or EnMAP has **never seen Tanager's 426-band grid**",
    "Either resample Tanager to the model's bands (`hu.resample_to_sensor`, notebook 30)",
    "…or use a **wavelength-aware** architecture that conditions on each band's centre",
    "At the time of writing, few if any public foundation models are trained on Tanager itself",
    "Resampling throws away exactly the narrow-band detail you bought the sensor for",
], kicker="before you fine-tune anything",
   notes="This is the honest catch in the foundation-model story for this course. It is also a good "
         "project idea: quantify what is lost when Tanager is resampled to EnMAP for a pre-trained model.")

d.table("Compute budget: what runs where",
        ["Task", "Laptop CPU", "Single GPU"],
        [["Random forest, 7k pixels", "2.5 s", "not needed"],
         ["1D-CNN, 12 epochs", "41 s", "seconds"],
         ["HybridSN, 12 epochs", "35 s", "seconds"],
         ["Full-scene tiled inference", "88 s", "~10 s"],
         ["Fine-tuning a foundation model", "impractical", "hours"]],
        col_widths=[2, 1, 1], kicker="plan your week accordingly",
        notes="The whole practical runs in about five minutes on a CPU. Nobody needs a GPU for this "
              "course, but fine-tuning a foundation model in a project would need one — plan for Colab.")

d.handover("20_geoai_deep_learning.ipynb", [
    "Build the blocked split with a buffer and check the class counts",
    "Train the random forest baseline, then the 1D-CNN, then HybridSN",
    "Compare per-class F1 and explain which classes gained and why",
    "Map the full scene with tiled inference and inspect the confidence layer",
    "Apply your model to Ho Chi Minh City and quantify the domain shift",
], minutes=120,
   notes="Warn them the notebook takes about five minutes end to end. The quiz "
         "quizzes/quiz_w3_geoai_validation.md covers this session and the validation session together.")

d.recap([
    "Pixel, patch or scene: choose by **how much context** the class needs and how many labels you have",
    "Deep learning gained macro-F1 0.861 → 0.925 here, mostly on the **hard** classes",
    "**Blocked splits with buffers** are what make that number believable",
    "Accuracy collapsed off-domain: 0.96 → 0.26 in a new city, 41 % of it labelled mangrove",
    "Foundation models address the label bottleneck, but mind the **sensor mismatch**",
], next_up="Session 3 — Validation methods and accuracy assessment (notebook 21)",
   notes="Close by asking what number they would put in a report: 0.959, 0.843 or 0.261. The answer is "
         "all three, each with its domain stated.")

d.references([
    "Chen, Y. et al. (2016). Deep feature extraction and classification of hyperspectral images based on CNNs. IEEE TGRS 54, 6232–6251.",
    "Roy, S.K. et al. (2020). HybridSN: exploring 3D–2D CNN feature hierarchy for hyperspectral image classification. IEEE GRSL 17, 277–281.",
    "Hong, D. et al. (2022). SpectralFormer: rethinking hyperspectral image classification with transformers. IEEE TGRS 60, 1–15.",
    "Roberts, D.R. et al. (2017). Cross-validation strategies for data with spatial structure. Ecography 40, 913–929.",
    "Ploton, P. et al. (2020). Spatial validation reveals poor predictive performance of large-scale ecological mapping models. Nature Comms 11, 4540.",
    "Guo, C. et al. (2017). On calibration of modern neural networks. ICML.",
    "Wang, D. et al. (2024/25). HyperSIGMA; Braham, N.A.A. et al. (2024/25). SpectralEarth; Hong, D. et al. (2024). SpectralGPT; Jakubik, J. et al. (2023). Prithvi; Xiong, Z. et al. (2024). DOFA.",
    "Course material: notebook 20, quiz quizzes/quiz_w3_geoai_validation.md",
])

d.save("w3a_geoai_methods.pptx")
