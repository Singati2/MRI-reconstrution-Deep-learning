# 01 — Executive Overview (section-by-section)

**Paper:** Toner et al., "Accelerated free-breathing abdominal T2 mapping with deep learning reconstruction of
radial turbo spin-echo data," *Magn Reson Med* 2025;94:2475–2491. DOI 10.1002/mrm.70017.

## One-paragraph thesis
RADTSE (radial turbo spin-echo) with respiratory-triggered PACE acquires a co-registered multicontrast TE
time-series in a single free-breathing scan, from which a voxel-wise T2 map is fit. The catch: to accelerate,
you acquire few radial views per TE, so per-TE images are badly aliased. The authors train a **cascaded unrolled
network with data-consistency layers** (physics-driven DL) in two flavors — a **supervised composite network**
for anatomical T2-weighted images, and a **self-supervised subspace-constrained network** for the T2 maps
(no clean target exists). Result: full-liver coverage from **160 views (5 views/TE)** in **< 3 min**, ~**1 s/slice**
reconstruction, lower T2 error and more stable behavior under acceleration than adjoint NUFFT and Locally-Low-Rank CS.

---

## §1 Introduction — what problem, why hard
- **Clinical need:** quantitative abdominal T2 mapping is more reproducible than qualitative T2w, useful for
  differentiating normal/abnormal tissue, lesions, cancer.
- **Why hard:** Cartesian SE/TSE/EPI trade temporal vs spatial resolution; breath-holds limit coverage;
  navigator/PACE free-breathing costs long scan time. Few-TE methods hurt T2 accuracy. GRAPPATINI limited slices.
- **RADTSE (refs 17–19):** radial → motion-robust, high spatiotemporal resolution, fittable voxel-wise T2.
  PACE (ref 20) gives free-breathing at the cost of scan time.
- **Prior acceleration:** echo-sharing (spurious T2), CS with temporal correlations (slow recon).
- **Prior DL for RADTSE (ref 27):** patch-based, supervised, CS recon as "ground truth", **no data-consistency
  layers**, breath-hold only, phase discarded. The authors position their contribution against exactly these gaps.
- **Contribution:** flexible framework, **cascaded unrolled net with DC layers**, trained separately for
  (a) high-res T2w imaging (supervised) and (b) T2 mapping (self-supervised + SVD temporal subspace).

## §2 Methods
- **2.1 RADTSE acq/recon** — Eq 1–6. Radial pseudo-golden-angle; two recon routes: composite (TE-averaged,
  Eq 2) and per-TE (Eq 3). Density compensation `D`; the `A/A*` unified notation and the `A*:=AᴴD` convention.
  PC/subspace model via SVD of a SEPG signal dictionary (Eq 4), `P = 4` PCs (99.96% variance).
- **2.2 Network** — Eq 7–9. `K = 5` cascades alternating **CNN block** (L = 5 conv layers + nonlinearity +
  residual) and **DC block** (learned-step gradient descent, Eq 9). Composite net: 1 channel. TE/T2 net: multi-
  channel (P PC channels).
- **2.3 Training** — Eq 10–13. Zero-fill a *random* number of entire echo trains. Composite = supervised image
  loss (Eq 11). TE/T2 = self-supervised k-space loss (Eq 12–13), SSDU-inspired but loss over the **entire** `y`.
- **2.4 Dataset** — 121 volunteers, 3T Skyra/Vida, 85/9/27 split. ETL 32, 384 views, matrix 320². 6 virtual
  coils (SVD). Training acceleration 1.5–6× (`r ∈ {2..8}` of 12 echo trains kept). NAdam, cosine LR, 450/150 epochs.
- **2.5 T2-error validation** — T2 error is **not** in the loss; used only for **epoch/model selection** (lowest
  mean ROI T2 error on val, ROIs in liver/kidney/spleen/muscle). Targets from 384-view LLR (ref 22).
- **2.6 T2 quantification** — reference = 8192-view scan (7 subjects, ~25 min, 5 slices), retrospectively
  undersampled to 192/160/128, compared DL vs LLR against 8192-view NUFFT reference.
- **2.7 Anatomical-image error** — composite net (supervised); 384-view test data as reference; ℓ¹/ℓ²/PSNR.
- **2.8 Prospective data** — 15 subjects at 384/192/160/128 views; **qualitative only** (no voxel-wise reference).
- **2.9 System/code** — PyTorch + MERLIN (complex support); trained on P100 / RTX 3090 / RTX A6000; speed on A6000.
  Code public (github.com/UA-MRI/radtse-dl-recon).

## §3 Results
- **3.1 T2 quantification (Fig 3, Table 1)** — DL T2 correlates better with the 8192-view reference than LLR;
  DL regression lines closer to identity, higher R². **Table 1 headline:** at 192 views DL≈LLR; at 160 and 128
  views LLR error rises sharply while DL stays stable. Performance **drops 160→128 views** ⟹ **160 = sweet spot**.
- **3.2 Anatomical error (Fig 4/5, Table 2)** — DL TE and composite images have lower ℓ¹/ℓ² and higher PSNR than
  NUFFT and LLR at all accelerations; DL TE at **128 views beats** NUFFT/LLR TE at **192 views**.
- **3.3 Prospective (Fig 6/7)** — 384/192/160/128-view scans take 8:19 / 3:33 / 2:57 / 2:37 min; 58–67% less
  k-space → 64–68% scan-time reduction. 160 views → 28 slices, 28 T2 maps, 896 TE images in **2:57 min**, 1 s/slice.
- **3.4 Pathology (Fig 8)** — two patients (cholangiohepatitis, hemangioma, hepatic/splenic cysts, GIST);
  model qualitatively robust to 160-view undersampling, though trained on (mostly) healthy volunteers.

## §4 Discussion — honest limitations (read these carefully)
- Radial: susceptible to off-resonance & gradient-delay errors (partly mitigated by fat-sat, sequence design).
- **Residual streaks** in high-motion regions (stomach peristalsis, CSF pulsation) — motion doesn't average out
  at high acceleration. Might improve if trained on 8192-view data (impractical: ~25 min/5 slices).
- Model is **application-specific**: trained for free-breathing abdominal T2; other apps need new protocols + fine-tuning.
- Dataset **predominantly healthy**; pathology cohort tiny — needs larger, more varied validation.
- Small/simple CNN (5 cascades × 5 layers) **limited by GPU memory** — bigger nets may help.
- SAR limits from constant 150° flip; variable-flip could raise efficiency further.

## §5 Conclusion
Efficient free-breathing full-abdomen T2 mapping via a novel **self-supervised** DL recon on RADTSE; anatomical
T2w images + accurate T2 maps in one accelerated respiratory-triggered acquisition, mean **< 3 min**, without
sacrificing image quality or T2 accuracy.

---

## What the paper does NOT teach (your gaps → see 14_OPEN_QUESTIONS)
- No formal CS theory (RIP, incoherence, sample complexity, phase transitions) — it *uses* subspace sparsity but
  doesn't derive it.
- No uncertainty quantification / calibration (their *other* 2026 paper does — that's a natural pairing).
- No proof of convergence for the unrolled scheme; `K = 5` is empirical.
- Adjoint-NUFFT reference is treated as truth (Audit A7); no fully-independent gold standard for anatomy.
- Ablation lives only in Supporting Information (Audit A12) — not in this PDF.
- Self-supervised loss over the *entire* `y` (not a disjoint mask) — leakage question left open (E12 flag).
