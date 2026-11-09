"""Week 3 · Session 2 — AI-assisted hyperspectral classification and mapping (Practical)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from deckbuild import Deck  # noqa: E402

d = Deck("AI-assisted classification and mapping",
         "Week 3 · Session 2",
         notebook="20_geoai_deep_learning.ipynb",
         subtitle="Training, inference and honest maps — the practical half of GeoAI",
         week="Week 3 · 23–26 November 2026")

d.objectives([
    "Prepare a labelled dataset from WorldCover pure pixels, and know why purity matters",
    "Build a **spatially blocked** split with a buffer that matches your patch size",
    "Read a training curve: early stopping, overfitting, underfitting, unstable validation",
    "Run **tiled inference** over a whole scene and export a Cloud-Optimised GeoTIFF",
    "Produce and interpret a confidence map and an MC-dropout uncertainty map",
    "Diagnose the usual failures: NaNs in patches, class collapse, memory, slow CPUs",
], notes="This session is hands-on: the theory was this morning. Say at the start that nobody needs "
         "prior PyTorch experience, and that the whole notebook runs in about 5–8 minutes on a laptop CPU. "
         "Ask who has a GPU — nobody needs one today.")

d.section("1. The dataset", "Labels, purity and class balance")

d.bullets("What we train on, and how the labels are cleaned", [
    "One **400 × 400 pixel window** (12 × 12 km) of the El Salvador mangrove coast",
    "**352 good bands** — water-vapour windows, SWIR edge and sub-400 nm bands already removed",
    "Labels: **ESA WorldCover 2021** at 10 m, aggregated to the Tanager 30 m grid",
    "Five classes with enough pure pixels: tree cover, grassland, cropland, water, mangroves",
    "**purity = 9**: all nine 10 m cells inside the 30 m pixel agree — mixed pixels are dropped",
    ("Cost: labels become sparse along boundaries — mangrove edges, field margins, creeks", 1),
], kicker="the working example",
   notes="Stress that the labels are a map, not ground truth: WorldCover is about 75 % accurate globally and "
         "dates from 2021 while the image is 2025. Notebook 15 measured the price of ignoring purity: test "
         "accuracy fell from 0.90 at purity 9 to 0.48 at purity 5.")

d.figure("The window, the labels and what survives the purity filter",
         "20_geoai_deep_learning/00_2_data_a_tanager_window_and_worldcover_l.png",
         caption="True colour · WorldCover classes · pure-pixel labels used for training",
         kicker="look at the data first",
         notes="Point out the gaps along the mangrove channels: that is the purity filter at work. "
               "Pure pixels available: tree cover 13 141, grassland 12 923, cropland 9 993, water 46 326, "
               "mangroves 57 479.")

d.section("2. Splitting the data", "The step that decides whether your accuracy is real")

d.callout("A random pixel split does not measure generalisation.\nIt measures memorisation.",
          "Neighbouring hyperspectral pixels are nearly identical. With 9 × 9 patches, a test patch can "
          "literally contain pixels the network trained on.",
          kicker="the most common mistake in the literature",
          notes="Tell them many published benchmark numbers on Indian Pines and Pavia use random splits "
                "on a single small image, which is why those numbers look implausibly high.")

d.figure_bullets("Blocks, buffers and what gets thrown away",
                 "20_geoai_deep_learning/01_3_a_spatial_train_validation_test_split_.png",
                 ["Cut the window into **50 × 50 px blocks** (1.5 × 1.5 km)",
                  "Assign blocks 60 / 20 / 20 to train / validation / test",
                  "Patch radius R = 4, so drop any pixel whose 9 × 9 window crosses another split",
                  "**The buffer must grow with the patch size** — change R, change the buffer",
                  "Validation drives early stopping; the test set is touched **once**"],
                 caption="Block split with a 4-pixel buffer between splits",
                 notes="Labelled pixels after the split — train/val/test: tree cover 5 196/3 041/2 473, "
                       "grassland 6 670/2 400/1 674, cropland 2 166/3 596/2 712, water 25 310/5 775/6 765, "
                       "mangroves 33 995/6 154/8 406. We then train on only 10 % of the training pixels "
                       "(7 332 spectra) to imitate a realistic label budget.")

d.section("3. Training", "Two models, one baseline, and how to read the curves")

d.bullets("What we run, and why in this order", [
    "**Random Forest** on the full 352-band spectrum — the baseline, trains in ~2.5 s",
    "**1D-CNN** on spectra — 42 309 parameters, ~41 s on CPU, stopped after 12 epochs",
    "**HybridSN-style 3D→2D CNN** on 9 × 9 × 30 PCA patches — 265 349 parameters, ~35 s",
    "PCA is fitted on **training pixels only**; fitting on everything leaks test information",
    "30 components keep **99.99 %** of the training variance, so the patch model loses almost nothing",
    ("Always report the baseline next to the deep model — it is the honest comparison", 1),
], kicker="the practical sequence",
   notes="The order matters pedagogically: if the Random Forest is already good, the deep model has to earn "
         "its complexity. Class imbalance is handled in the loss, not by discarding data.")

d.code("The ingredients that make it train on small data", '''
# class-weighted loss: rare classes count as much as common ones
w = N / (K * counts)                      # w_k = N / (K · N_k)
loss = nn.CrossEntropyLoss(weight=torch.tensor(w, dtype=torch.float32))

# standardise with TRAIN statistics only — never the test set
band_mean, band_std = Xtr.mean(0), Xtr.std(0) + 1e-6

# early stopping: keep the weights with the best validation macro-F1
if val_f1 > best_f1:
    best_f1, best_state = val_f1, copy.deepcopy(model.state_dict())
''', kicker="four lines that matter",
   caption="Class weighting, standardisation, early stopping — the rest is plumbing",
   notes="Ask why we standardise with training statistics: because at deployment you will not have the "
         "test data. The same rule applies to PCA, scalers and any normalisation.")

d.figure_bullets("Reading the training curves",
                 "20_geoai_deep_learning/02_6_model_2_a_spectral_spatial_patch_cnn_h.png",
                 ["Training loss falls, validation macro-F1 rises, then flattens — stop there",
                  "**Overfitting:** validation F1 turns down while training loss keeps falling",
                  "**Underfitting:** both stay flat and poor — model too small or learning rate wrong",
                  "**Noisy validation curve:** the validation set is small or unrepresentative",
                  "Both models stopped after 12 epochs here"],
                 caption="Training loss and validation macro-F1 per epoch",
                 image_left=True,
                 notes="Early stopping restores the best epoch, so curves may run a few epochs past the model "
                       "we keep. If the validation curve jumps around, do not trust small differences between models.")

d.section("4. Results, maps and shipping", "Comparing models, then scaling to a whole scene")

d.table("Per-class F1 on the spatially independent test blocks",
        ["", "Random Forest", "1D-CNN", "HybridSN"], [
            ["Tree cover", "0.836", "0.830", "0.882"],
            ["Grassland", "0.646", "0.720", "0.804"],
            ["Cropland", "0.851", "0.940", "0.960"],
            ["Permanent water", "0.995", "0.994", "0.994"],
            ["Mangroves", "0.979", "0.974", "0.983"],
            ["macro F1", "0.861", "0.892", "0.925"],
            ["overall accuracy", "0.925", "0.940", "0.959"],
        ], kicker="measured, not quoted",
   col_widths=[2, 1, 1, 1],
   notes="Water and mangroves are near-perfect for everything — they are spectrally distinctive. The gains "
         "are in grassland and cropland, the classes that overlap spectrally and where WorldCover is weakest. "
         "Warn them: 1–2 F1 points between models is within the noise of one split.")

d.figure("From model to map",
         "20_geoai_deep_learning/05_8_from_model_to_map.png",
         caption="True colour · WorldCover · HybridSN confidence · the three model maps",
         kicker="the output that matters",
         notes="Pixel models give salt-and-pepper speckle; the patch model is smoother but blurs creeks and "
               "field margins. Low confidence concentrates on boundaries and on materials never trained on "
               "(villages, sand bars) — the open-set problem. Softmax confidence is not calibrated probability.")

d.figure_bullets("MC-dropout: a second opinion on uncertainty",
                 "20_geoai_deep_learning/06_9_mc_dropout_uncertainty.png",
                 ["Keep dropout **on** at prediction time and run the model several times",
                  "Different neurons drop each pass, so predictions differ",
                  "Summarise with predictive entropy H = −Σ p̄ log p̄ (0 = certain)",
                  "10 passes over 16 900 pixels took 32 s here",
                  "High entropy marks boundaries and out-of-legend materials"],
                 caption="Mean prediction, confidence and MC-dropout entropy",
                 notes="Gal & Ghahramani (2016). It is cheap and approximate — a sanity layer, not a calibrated "
                       "posterior. For the project it is enough to show where the model is unsure.")

d.figure_bullets("Tiled inference over the full scene",
                 "20_geoai_deep_learning/07_10_sliding_window_tiled_inference_over_t.png",
                 ["The full cube here is ~650 × 785 px × 352 bands ≈ **0.75 GB** in memory",
                  "Read **one strip of rows** at a time, with a halo of R rows above and below",
                  "Predict the core rows, write them out, move on — memory stays bounded",
                  "Full scene in **88 s** on CPU, exported as a COG plus a confidence layer",
                  "Yellow box = the training window; everything else is extrapolation"],
                 caption="HybridSN applied to the whole Tanager scene, tile by tile",
                 image_left=True,
                 notes="The halo is the same idea as the split buffer, for a different reason: patches at tile "
                       "edges must see their real neighbours. Ask whether they would trust the map outside the "
                       "yellow box — that is the next slide.")

d.table("Does the model travel?", ["Test", "Overall accuracy", "Macro F1"], [
    ["Test blocks (same window)", "0.959", "0.925"],
    ["Same scene, outside the window", "0.843", "0.792"],
    ["Ho Chi Minh City — HybridSN", "0.335", "—"],
    ["Ho Chi Minh City — 1D-CNN", "0.334", "—"],
    ["Ho Chi Minh City — Random Forest", "0.261", "—"],
], kicker="domain shift, measured",
   notes="The pixel models label 41 % (RF) and 44 % (1D-CNN) of Ho Chi Minh City as mangrove — a class that "
         "does not occur there. The patch model avoids that but sends cropland to water: rice paddies are "
         "flooded, so the same label has different spectra.")

d.bullets("Troubleshooting: what actually goes wrong", [
    "**NaNs in a patch** — no-data or cloud inside the window: mask, or fill with the PCA mean (zero)",
    "**Class collapse** (everything one class) — imbalance: check the class weights and the loss",
    "**Validation F1 stuck at chance** — labels and features misaligned, or learning rate too high",
    "**MemoryError on patches** — build patches with a sliding-window *view*, predict in batches",
    "**Training is slow** — `torch.set_num_threads(4)`, fewer PCs, smaller patches, fewer pixels",
    "**Test accuracy suspiciously high** — check the split: leakage before celebration",
], kicker="the six calls for help we expect",
   notes="Leave this on screen during the lab. The last bullet is the most important: if a student reports "
         "0.99, the first question is about the split, not the model.")

d.handover("20_geoai_deep_learning.ipynb", [
    "Sections 2–3: build the dataset and the blocked split — check the buffer",
    "Sections 4–6: train the RF baseline, the 1D-CNN and the HybridSN patch model",
    "Sections 7–9: compare honestly, map the window, add confidence and MC-dropout entropy",
    "Sections 10–11: tiled inference, export the COG, then the domain-shift test",
    "Exercises: patch size R = 2 vs 6 · random split vs block split · learning curve with 1–30 % of labels",
], minutes=120,
   notes="Circulate during training runs — that is when questions come. Students on slow machines should "
         "reduce the training fraction rather than skip sections. The random-split exercise is the one that "
         "changes behaviour: accuracy jumps several points and they see how easy inflation is. "
         "Quiz: quizzes/quiz_w3_geoai_validation.md. Teams should now run this on their own scene.")

d.recap([
    "Labels are a **map, not truth** — filter for purity and say what that costs",
    "**Spatial blocks plus a buffer** matched to the patch size; the test set is touched once",
    "Report the **baseline**: 0.861 macro F1 (RF) against 0.925 for the patch CNN",
    "Maps need **confidence and uncertainty layers**, and someone to look at them",
    "**Tiled inference** scales the same code from one window to an archive",
    "Accuracy is **local**: 0.959 in the test blocks, 0.84 outside the window, ~0.3 in another country",
], next_up="Session 3 — Validation methods and accuracy assessment (notebook 21)",
   notes="Close on the last bullet and connect it to tomorrow: the validation session gives the tools to "
         "report this properly, including area-adjusted accuracy and confidence intervals.")

d.references([
    "Roy, S.K. et al. (2020). HybridSN: exploring 3-D–2-D CNN feature hierarchy for hyperspectral image classification. IEEE GRSL 17(2), 277–281.",
    "Chen, Y. et al. (2016). Deep feature extraction and classification of hyperspectral images based on convolutional neural networks. IEEE TGRS 54(10), 6232–6251.",
    "Gal, Y. & Ghahramani, Z. (2016). Dropout as a Bayesian approximation: representing model uncertainty in deep learning. ICML.",
    "Breiman, L. (2001). Random forests. Machine Learning 45, 5–32.",
    "Hughes, G. (1968). On the mean accuracy of statistical pattern recognizers. IEEE Trans. Information Theory 14(1), 55–63.",
    "ESA WorldCover 2021 v200 (CC-BY 4.0) · Tanager open data CC-BY-4.0 © Planet Labs PBC",
])

d.save("w3b_ai_assisted_mapping.pptx")
