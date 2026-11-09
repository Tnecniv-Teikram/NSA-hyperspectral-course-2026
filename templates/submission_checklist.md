# Final graduation project — submission checklist

**Space Academy 2026 · Hyperspectral course · Thursday 26 November — mini project submission**

Submit **one folder (or repository) per team** named `team_<name>_hyperspectral_project/` containing:

```
team_<name>_hyperspectral_project/
├── README.md                ← 1 page: problem, data, method, key results, how to run
├── project.ipynb            ← based on templates/project_template.ipynb, executed with outputs
├── src/ (optional)          ← helper modules (e.g. your copy/extension of hsi_utils.py)
├── outputs/
│   ├── *.tif                ← main result layers as Cloud-Optimised GeoTIFFs
│   ├── *_metadata.json      ← provenance: scene IDs, parameters, software versions, date
│   └── figures/             ← the figures used in the presentation (PNG, ≥ 150 dpi)
├── validation/              ← validation table(s) as CSV + confusion matrix / scatter plots
├── presentation.pdf         ← final slides (see presentation_template.md)
└── requirements.txt         ← anything beyond the course requirements
```

## Before you submit

### Notebook
- [ ] *Restart & Run All* works on a clean kernel. Heavy steps are cached and a flag explains how to rerun them.
- [ ] Config cell at the top (scene IDs, AOI/window, thresholds, seeds).
- [ ] No raw HDF5 files in the submission (they are 1 GB each). Scene IDs are enough to re-download.
- [ ] Output layers written with `hu.save_geotiff()` (or rasterio) in the scene CRS, with band descriptions.
- [ ] Every figure is readable on its own (title, units, colour bar, legend).

### Science
- [ ] Hyperspectral-specific features are used and explained (wavelengths named).
- [ ] Validation: metric(s), confusion matrix or residual plot, spatially independent test data, baseline comparison.
- [ ] Limitations and failure cases discussed (mixed pixels, label noise, atmosphere, single date, …).
- [ ] Uncertainty communicated (probability/σ map or confidence interval).

### Product
- [ ] The user and the decision are named, and the delivery format (dashboard / API / alert / report) is shown as a mock-up or prototype.
- [ ] Scalability considered: what would it take to run this monthly over a whole country?

### Admin
- [ ] Data attribution: *"Tanager STAC Data, available at www.planet.com/data/stac © 2025 Planet Labs PBC"*
      (plus ESA WorldCover, Copernicus Sentinel data, EnMAP © DLR, etc. if used).
- [ ] Team members and contributions listed in the README.
- [ ] Submitted before the deadline announced by the course team.

The final evaluation uses `evaluation_rubric.md`. Read it before you finish.
