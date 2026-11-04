# Answer key — Quiz W2 — Feature extraction, material discrimination, target detection and classification

*Instructor copy. Do not distribute to students before the quiz.*

| # | Answer | Why |
|---|:---:|-----|
| 1 | **a** | Hughes (1968): with limited samples, adding dimensions first helps and then hurts, because parameter estimates become unreliable. |
| 2 | **b** | MNF (Green et al. 1988) whitens the noise first, then applies PCA, so components are ordered by SNR rather than raw variance. |
| 3 | **c** | Selected bands keep physical meaning and are easy to explain; PCA components mix all bands. |
| 4 | **c** | SAM measures the angle between vectors; scaling a spectrum by a constant does not change its direction. |
| 5 | **c** | Both use the target signature plus background statistics (mean, covariance), typically estimated from the scene itself. |
| 6 | **a** | Implantation gives controlled ground truth to measure detection vs false alarms as a function of sub-pixel fraction. |
| 7 | **a** | Linear mixing model with abundance non-negativity and sum-to-one constraints (FCLS). |
| 8 | **a** | Intimate (particulate) mixtures and multiple scattering in canopies produce non-linear mixing; side-by-side areal mixtures are close to linear. |
| 9 | **d** | N-FINDR (Winter 1999) maximises simplex volume in a dimension-reduced space. |
| 10 | **a** | Clusters are unlabeled spectral groups; the analyst must interpret them, and classes and clusters rarely map one-to-one. |
| 11 | **d** | Spatial autocorrelation leaks information between random train/test pixels; use spatially separated blocks. |
| 12 | **b** | Correlated neighbouring bands are interchangeable for the trees, so importance is spread among them. |
| 13 | **b** | RF and RBF-SVM are strong, cheap baselines for pixel-based hyperspectral classification. |

## Model answers for the short questions

**14.** CAI = 0.5·(R2000 + R2200) − R2100 measures the narrow cellulose/lignin absorption at ~2100 nm. Sentinel-2 has no band at 2000 or 2100 nm; B12 (2190 nm, ~175 nm wide) averages the whole region. CAI matters for crop-residue cover (conservation tillage, soil erosion) and for dry vs green vegetation, e.g. fuel mapping.

**15.** A detector (ACE or matched filter) is a good fit for rare, small targets whose spectrum is known: it suppresses the background using its covariance and handles sub-pixel targets. SAM is simpler and brightness-invariant but ignores background statistics, which gives more false alarms. A classifier needs many labelled examples of the rare class. Set the threshold from a false-alarm budget (e.g. the 99.9th percentile of detector scores over a target-free area), check it with implanted targets or known roofs, and then inspect the detections visually.
