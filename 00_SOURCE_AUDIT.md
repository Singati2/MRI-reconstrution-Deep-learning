# 00 — Source Manifest & Document Audit

> ⚠️ **Source correction (traceable):** The prompt named
> `/home/mpcrlab/Desktop/cs_techniques_toner2025.html`. That file does **not exist** on this machine.
> The audited source is the **PDF** you confirmed:
> `~/Desktop/Magnetic Resonance in Med - 2025 - Toner - Accelerated free‐breathing abdominal T2 mapping with deep learning.pdf`
> Because the source is a PDF (not HTML), the "HTML-rendering artifact / empty-box / broken-LaTeX"
> parts of the audit are replaced by **PDF text-extraction** concerns. Everything below was read
> directly from the 17-page PDF.

---

## 1. Source Manifest (§23 Step 3)

| Field | Value |
|---|---|
| **Title** | Accelerated free-breathing abdominal T2 mapping with deep learning reconstruction of radial turbo spin-echo data |
| **Authors** | B. Toner, S. Arberet, S. Zhang, F. Han, E. Ahanonu, U. Goerke, K. Johnson, Z. Abouelfetouh, I. Codreanu, S. Sridhar, H. Arif-Tiwari, V. Deshpande, D. R. Martin, M. Nadar, M. I. Altbach, A. Bilgin |
| **Corresponding** | Ali Bilgin, Program in Applied Mathematics, University of Arizona (bilgin@arizona.edu) |
| **Journal** | *Magnetic Resonance in Medicine* 2025;94:2475–2491 |
| **DOI** | 10.1002/mrm.70017 |
| **Type** | Research Article (open access, Creative Commons) |
| **Dates** | Received 12 May 2025; Revised 22 June 2025; Accepted 15 July 2025 |
| **Code** | https://github.com/UA-MRI/radtse-dl-recon.git (public) |
| **Data** | Human MRI data **not** approved for public sharing (code only) |
| **Sections** | 1 Intro · 2 Methods (2.1 RADTSE acq/recon, 2.2 Network, 2.3 Training, 2.4 Dataset, 2.5 T2-error validation, 2.6 T2 quantification, 2.7 Anatomical-image error, 2.8 Prospective data, 2.9 System/code) · 3 Results (3.1 T2 quant, 3.2 Anatomical error, 3.3 Prospective, 3.4 Pathology) · 4 Discussion · 5 Conclusion |
| **Equations** | 13 numbered (Eq 1–13) |
| **Figures** | 8 (Fig 1 acq/recon overview; Fig 2 network + training schemes; Fig 3 T2 correlation + maps; Fig 4 sample TE image + error maps; Fig 5 composite images; Fig 6 prospective composite/TE/T2; Fig 7 all-slice coverage; Fig 8 pathology cases) |
| **Tables** | 2 (Table 1 mean relative T2 error % by organ × acceleration; Table 2 voxel-wise ℓ¹/ℓ²/PSNR for TE & composite) |
| **References** | 48 |
| **Supporting Info** | Data S1 (ablation study; not in the main PDF — **not accessible to this audit**) |

### Key quantitative facts (as stated in source — for grounding, do not misquote)
- **Cohort:** 121 volunteers, two 3T sites (MAGNETOM Skyra, MAGNETOM Vida, Siemens). 85 train / 9 val / 27 test.
- **Protocol:** 28 axial slices, 6 mm, 0.78 mm (13%) gap → 189.06 mm coverage. ETL = 32. Echo spacing 8.1 ms (Skyra) / 8.46 ms (Vida). Flip 150°. TR = 1 respiratory cycle. FoV 380×380 mm². **384 radial views**, 512 readout points, 2× readout oversampling; reconstructed at matrix 320×320. Fat sat via CHESS.
- **Coils:** compressed to **6 virtual coils** via SVD.
- **Subspace:** **P < ETL** principal components; **P = 4** PCs used (first 4 PCs = 99.96% explained variance).
- **Training undersampling:** random `r ∈ {2,…,8}` echo trains kept out of 12 → acceleration **1.5–6×**.
- **Network:** **K = 5** cascades, **L = 5** conv layers/CNN block, kernel 3×3, 64 hidden channels, ReLU modified for complex weights, NAdam, cosine-annealed LR (init 1e−4). Composite net 450 epochs; TE/T2 net 150 epochs. Batch 1–4.
- **Reconstruction time:** ≈ **1 s/slice** (DL) vs > 30 min/slice (LLR).
- **Headline:** full-liver free-breathing coverage from **160 total views (5 views/TE)** in **< 3 min** (mean 2:57).
- **Key result:** **160 views is the sweet spot** — performance drops going 160 → 128 views.
- **Baselines compared:** adjoint NUFFT, Locally Low Rank (LLR) iterative (ref 22), proposed DL.

---

## 2. Document Audit Table (§4)

> Labels: **Confirmed error · Probable error · Formatting/rendering · Notation inconsistency · Ambiguity · Pedagogical weakness · No issue.**
> No file was altered during this audit (§4 requirement).

| # | Item | Location | Status | Problem | Recommended correction | Confidence |
|---|---|---|---|---|---|---|
| A1 | NUFFT symbol switches from 𝒯 to ℱ | Eq (1)–(3) use `𝒯ᵢ`/`𝒯*_comp`; Eq (4)–(6) use `ℱ`/`ℱ*` | **Notation inconsistency** | The nonuniform FFT operator is written `𝒯` in the sampling equations but `ℱ` once the PC model is introduced. Same operator, two glyphs. | Standardize to one symbol (e.g. `F` for the (nonuniform) Fourier encoding) throughout, or explicitly state `ℱ ≡ 𝒯`. | High |
| A2 | `A` / `A*` deliberately **not** true adjoints | p.2477–2478, after Eq (6): "we will assume `A* := A*D` … `A` and `A*` are no longer true adjoints under this convention" | **Ambiguity (author-acknowledged)** | The density-compensation `D` is folded into the "adjoint" so `A*` is a *preconditioned* back-projection, not the mathematical adjoint. A reader running an inner-product adjoint test on the paper's `A`,`A*` will see it **fail by design**. | Not an error — but for your own code, keep a *true* adjoint `Aᴴ` (passes the dot-product test) separate from the paper's preconditioned `A*=AᴴD`. See Equation Register E5/E6. | High |
| A3 | `F`/`F*` orientation vs. Eq (4) | `A := ℱ*SU*` (PC case, p.2477) vs. Eq (4) `Ux = US*ℱ*Dy` | **Ambiguity** | Which of `ℱ`,`ℱ*` is the image→k-space direction is easy to lose track of because `A` (the *forward* op, image→k-space) is defined with a starred `ℱ*`. Consistent only once you accept the A2 convention (D absorbed, adjoints relabeled). | State the direction of every operator once in a table (image→kspace vs kspace→image). Handled in E-register. | Medium |
| A4 | `D` vs `D̄` | Eq (2) uses full `D ∈ ℝ^{(M·ETL)×(M·ETL)}`; Eq (3) uses `D̄ ∈ ℝ^{M×M}` | **No issue (well-defined)** | Two ramp density-compensation operators of different sizes (all-TE vs single-TE). Correctly distinguished in text. | None — just note the bar means "single-TE slice of D." | High |
| A5 | `x̄ᵢ` (ground truth) vs `x'` (network image) vs `x̂` (estimate) | Eq (1) `x̄ᵢ`; Eq (5)–(9) `x'`; Eq (10)/(11) `x̂` | **Pedagogical weakness** | Three decorations of `x` (bar, prime, hat) carry distinct meanings (ground truth / current-iterate PC-or-composite image / final estimate) but the distinction is never tabulated. Easy to conflate. | Keep a symbol table (provided in Glossary). Not an error. | High |
| A6 | Subspace dimension symbol `P` vs `τ` | `P` = #PCs (2.2, 2.4); DC block text uses `τ` ("τ = 1 for composite, τ = P for PC") | **Notation inconsistency (minor)** | `τ` is introduced only in the Fig 2 caption / Eq (7)–(9) region as the channel count; it equals 1 or `P`. Reader may not connect `τ` to `P`. | State `τ ∈ {1, P}` explicitly at first use. | Medium |
| A7 | "adjoint NUFFT" used as *reference/ground truth* for anatomical error | 2.7, 3.2, Table 2 | **Pedagogical weakness / methodological caveat** | The 8192-view **adjoint-NUFFT** reconstruction is treated as the gold standard for TE-image error, but adjoint NUFFT ≠ true inverse (it is a density-compensated back-projection). Errors are *relative to a non-ideal reference*. The authors are aware (they call it "gold standard" only for the 8192-view case). | For your reading: interpret Table 2 numbers as agreement-with-a-strong-reference, not agreement-with-truth. | High |
| A8 | Eq (8) chain-rule result | `d/dx̂'⁽ʲ⁾ [½‖Ax̂'⁽ʲ⁾−y‖²] = A*(Ax̂'⁽ʲ⁾−y)` | **Correct under A2 convention** | With a *true* adjoint the gradient is `Aᴴ(Ax−y)`; the paper writes `A*` which under their convention is `AᴴD`. So the "gradient" is a *preconditioned* gradient, not the exact one. | Fine for a learned step-size `η` (backprop absorbs the preconditioner), but flag it: Eq (9) is preconditioned gradient descent, not vanilla GD. | Medium |
| A9 | `α` set to ½ | Eq (11), Eq (13): "α ∈ [0,1] … (set to ½)" | **No issue** | Balances ℓ¹ and ℓ² terms equally. Clearly stated. | None. | High |
| A10 | Loss normalization | Eq (11)/(13) divide by `‖x‖₁`,`‖x‖₂` / `‖y‖₁`,`‖y‖₂` | **No issue (worth noting)** | Relative (scale-invariant) loss. Good practice, but means the loss magnitude is not comparable across normalization schemes. | Note the [0,1] magnitude normalization step (2.4) that precedes it. | High |
| A11 | Prospective data has **no** voxel-wise ground truth | 2.8, 3.3 | **No issue (correctly caveated)** | Prospective results are qualitative only (no retrospective reference). Authors state this. | Don't quote prospective numbers as accuracy. | High |
| A12 | Supporting Information (ablation) not in main PDF | "SUPPORTING INFORMATION: Data S1" | **Inaccessible element** | The ablation study (network-size, hyperparameters) lives only in the online SI, which is not in this file. Any claim about ablations is **Needs verification** against the SI. | Fetch Data S1 from the publisher if you want the ablation details. | High |
| A13 | PDF ligature extraction (`ﬂ`, `ﬁ`) | throughout | **Formatting/rendering** | The PDF uses typographic ligatures ("ﬂexible", "ﬁt"); some extractors mangle these. Cosmetic only, no scientific impact. | Ignore. | High |

### Audit summary
- **Confirmed errors:** none.
- **Probable errors:** none.
- **Notation inconsistencies:** A1 (𝒯↔ℱ), A6 (P↔τ) — cosmetic, do not change results.
- **Ambiguities (author-acknowledged):** A2, A3, A8 — the `A*:=AᴴD` convention. Important to understand, not a mistake.
- **Pedagogical weaknesses:** A5, A7 — symbol decorations & non-ideal reference.
- **Inaccessible:** A12 (Supporting Information ablation).

**Bottom line:** the paper is mathematically clean. The single most important thing to internalize is the **A2 convention** — the paper's `A*` is a *density-compensated back-projection*, not a true adjoint. This is standard in the physics-driven-DL literature but trips up first readers, and it is why an adjoint dot-product test on the paper's operators "fails" (it is supposed to). Your own code should keep the mathematically-true `Aᴴ` for testing separate from the preconditioned `A*` used in the DC step.
