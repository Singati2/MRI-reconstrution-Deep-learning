# 02 — Equation Register (Toner 2025, Eq 1–13)

Every numbered equation, reproduced from the source, standardized, verified, and connected to MRI /
optimization / deep learning. **Convention flag (see Audit A2):** the paper defines `A* := Aᴴ D` (density
compensation `D` folded in), so the paper's `A*` is **not** the true adjoint `Aᴴ`. I mark where this matters.

**Symbol key**

```text
x, x̄, x', x̂   image (generic / ground-truth / current network iterate / final estimate)   ∈ ℂ^{N·τ}
y, yᵢ          measured radial k-space (all-TE / single echo time TEᵢ)                      ∈ ℂ^{M·ETL}, ℂ^{M}
S              coil-sensitivity operator (multiply by C coil maps)
𝒯ᵢ ≡ ℱᵢ        nonuniform FFT (NUFFT) for the radial samples of TEᵢ   (image → k-space)
D, D̄           ramp density-compensation (all-TE size / single-TE size), diagonal ≥ 0
U              SVD temporal-subspace compression  (TE images → PC images),  U ∈ ℂ^{(N·P)×(N·ETL)}
A, A*          paper's forward / preconditioned-back-projection operators (see per-eq notes)
ETL            echo-train length (= 32);  P            #principal components (= 4);  τ ∈ {1, P}
N              #image pixels;  M            #radial k-space samples per echo;  C            #coils (→ 6 virtual)
η              learned DC step size;   α∈[0,1]        ℓ¹/ℓ² loss balance (= ½)
```

---

## E1 — Radial sampling / forward model (single echo time)

**Source form**  `yᵢ = 𝒯ᵢ S x̄ᵢ + εᵢ`  (Eq 1)

**Standardized**  `y_i = \mathcal{T}_i\, S\, \bar{x}_i + \epsilon_i,\quad i=1,\dots,\text{ETL}`

**Meaning** — the measured radial k-space at echo time `TEᵢ` is: take the true TE image `x̄ᵢ`, apply coil
sensitivities `S`, sample its Fourier transform on the radial trajectory of that TE (`𝒯ᵢ`), add noise `εᵢ`.

**Dimensions** — `x̄ᵢ ∈ ℂ^{N}`, `S : ℂ^{N} → ℂ^{N·C}`, `𝒯ᵢ : ℂ^{N·C} → ℂ^{M·C}`, `yᵢ ∈ ℂ^{M·C}`, `εᵢ ∈ ℂ^{M·C}`.
(The paper writes `yᵢ ∈ ℂ^{M×1}` per coil; multi-coil stacks over `C`.)

**Assumptions** — linear MR signal model; known `S`; Gaussian(-ish) complex noise; each TE has its own
well-distributed radial angles (pseudo-golden-angle) so `𝒯ᵢ` differs per `i`.

**MRI interpretation** — this *is* the physics: spin density → coil weighting → k-space encoding → sampling.
Radial + golden-angle is what makes RADTSE motion-robust and per-TE incoherent.

**Optimization interpretation** — defines the data-fidelity operator; reconstruction inverts this map.

**DL connection** — this exact operator (and its adjoint) is baked into the **data-consistency (DC) layer**;
the network never has to *learn* the physics — it is handed `𝒯ᵢ`, `S`.

**Verification status** — ✅ correct as written.

---

## E2 — Composite (TE-averaged) reconstruction

**Source form**  `x_comp = S* 𝒯*_comp D y`  (Eq 2)

**Standardized**  `x_{\text{comp}} = S^{*}\,\mathcal{T}^{*}_{\text{comp}}\, D\, y`

**Meaning** — stack all TEs' k-space into one dataset `y`, density-compensate (`D`, a diagonal ramp that
up-weights outer k-space to counter radial oversampling of the center), adjoint-NUFFT back to image space,
coil-combine (`S*`). Result: a single high-SNR image at the *average* TE.

**Dimensions** — `y ∈ ℂ^{M·ETL·C}`, `D ∈ ℝ^{(M·ETL)×(M·ETL)}` (diag ≥ 0), `𝒯*_comp : ℂ^{M·ETL·C}→ℂ^{N·C}`,
`S* : ℂ^{N·C}→ℂ^{N}`, `x_comp ∈ ℂ^{N}`.

**Assumptions** — combining across TEs is acceptable *for anatomy* (contrast is averaged, lost for T2 fitting).
`D` makes `𝒯*_comp D` approximate a true inverse (gridding recon).

**MRI interpretation** — the "composite image": more views → fewer streaks → best anatomical image, at the cost
of T2 information. Ramp DCF is the classic filtered-back-projection weighting.

**DL connection** — `x_comp` (or its zero-filled version) is the **input** to the composite network `f_comp`.

**Verification status** — ✅ correct under the density-compensated-adjoint (gridding) convention.

---

## E3 — Per-TE image reconstruction

**Source form**  `xᵢ = S* 𝒯*ᵢ D̄ yᵢ`  (Eq 3)

**Standardized**  `x_i = S^{*}\,\mathcal{T}^{*}_i\, \bar{D}\, y_i`

**Meaning** — reconstruct each TE image separately (`D̄` = single-TE version of `D`). Each `yᵢ` is highly
undersampled (few views/TE), so `xᵢ` is streaky — this is exactly the problem the network fixes.

**Dimensions** — `yᵢ ∈ ℂ^{M·C}`, `D̄ ∈ ℝ^{M×M}`, `𝒯*ᵢ : ℂ^{M·C}→ℂ^{N·C}`, `xᵢ ∈ ℂ^{N}`.

**MRI interpretation** — the multicontrast time series `{xᵢ}_{i=1}^{ETL}` that gets voxel-wise fit to a T2 map
via dictionary matching (SEPG signal model). Highly aliased when views/TE is small.

**DL connection** — `{xᵢ}` are the **channels** the TE/T2 network cleans up before projection to the subspace.

**Verification status** — ✅ correct (bar notation = single-TE slice of D, Audit A4).

---

## E4 — Principal-component (subspace) model

**Source form**  `Ux = U S* ℱ* D y`  (Eq 4)

**Standardized**  `U x = U\, S^{*}\,\mathcal{F}^{*}\, D\, y`  ⟹ PC images `= U · (per-TE recon)`

**Meaning** — instead of `ETL = 32` TE channels, project onto the first `P = 4` SVD components of the SEPG
signal dictionary. `U` maps the 32 TE images to 4 PC images that capture 99.96% of signal-decay variance.

**Dimensions** — `U ∈ ℂ^{(N·P)×(N·ETL)}`, `x ∈ ℂ^{N·ETL}` (stacked TE images), `Ux ∈ ℂ^{N·P}`.

**Why it matters** — (1) cuts compute/memory 32→4; (2) exploits temporal sparsity, exactly as in CS
subspace reconstruction (refs 22, 23). This is the **CS→DL bridge in one line**: the learned network operates
in a *compressed temporal subspace* motivated by classical CS.

**Notation caveat** — here `ℱ` is the same NUFFT called `𝒯` in E1–E3 (Audit A1).

**Verification status** — ✅ correct; note glyph switch 𝒯→ℱ.

---

## E5 / E6 — Unified forward / adjoint notation

**Source form**  `x' = A* D y`  (Eq 5)   `ŷ = A x'`  (Eq 6)

**Standardized**  `x' = A^{*} D y` (image estimate),  `\hat{y} = A x'` (project back to k-space)

**Definitions (from text, p.2477):**
- Composite images: `A := 𝒯*_comp S`, `U = I`.
- PC images: `A := ℱ* S U*`, `U` as in E4.
- **Convention (A2):** thereafter `A* := Aᴴ D`, so `A`,`A*` are *not* true adjoints; `D` is used only in the
  image direction (k-space→image), never in the forward (image→k-space) direction.

**Meaning** — a single symbol pair to describe *both* pipelines. `A*` (with `D`) = go from measured k-space to
image; `A` = go from image to predicted k-space `ŷ`.

**Optimization interpretation** — `A`,`A*` are the forward/back operators inside every DC step (E7–E9) and the
self-supervised loss (E12–E13).

**DL connection** — the whole point of physics-driven DL: the network is wrapped *around* fixed `A`,`A*`.
🔍 **For your code (Audit A2):** implement a **true** `Aᴴ` that passes the dot-product test
`⟨Ax, y⟩ ≈ ⟨x, Aᴴy⟩`, and *separately* a preconditioned `A*_paper = Aᴴ D`. Test the first; use the second in DC.

**Verification status** — ✅ correct **only under the stated non-adjoint convention** — flag when teaching.

---

## E7 — Data-consistency objective (per cascade)

**Source form**  `½ ‖ A_{CNN}^{(j)}(x'^{(j-1)}) − y ‖²`  (Eq 7)

**Standardized**  `\tfrac12\big\| A\, f_{\text{CNN}}^{(j)}\!\big(x'^{(j-1)}\big) - y \big\|_2^2`

**Meaning** — after the `j`-th CNN block denoises the current image, measure how far its *predicted* k-space
`A f_CNN(x')` is from the *acquired* k-space `y`. DC minimizes this.

**Dimensions** — `x'^{(j-1)} ∈ ℂ^{N·τ}` (τ = 1 composite, τ = P PC), `y ∈ ℂ^{M·ETL·C}`.

**Optimization interpretation** — the quadratic data term of the unrolled variational problem; the CNN supplies
the (learned, implicit) regularizer.

**Verification status** — ✅ correct.

---

## E8 — Gradient of the DC objective

**Source form**  `d/dx̂'^{(j)} [ ½‖Ax̂'^{(j)} − y‖² ] = A*(Ax̂'^{(j)} − y)`  (Eq 8)

**Standardized**  `\nabla_{\hat{x}'^{(j)}}\Big[\tfrac12\|A\hat{x}'^{(j)}-y\|_2^2\Big] = A^{*}\big(A\hat{x}'^{(j)} - y\big)`

**Derivation** — `f(x)=½‖Ax−y‖²`. For complex `x`, the Wirtinger gradient is `∇f = Aᴴ(Ax−y)`. The paper writes
`A*` which under convention A2 is `AᴴD` ⟹ this is a **preconditioned** gradient, not the exact one.

**MRI interpretation** — residual in k-space `(Ax̂'−y)` pushed back to image space and used to correct the image.

**DL connection** — this is the gradient the DC layer descends; because `η` is learned (E9), backprop can absorb
the `D` preconditioner, so the swap is harmless in practice (Audit A8).

**Verification status** — ✅ correct as a **preconditioned** gradient under convention A2. (Exact gradient with a
true adjoint would drop `D`.)

---

## E9 — Data-consistency update (learned gradient descent)

**Source form**  `x''^{(j)} = DC^{(j)}(x̂'^{(j)}) = x̂'^{(j)} − η A*(A x̂'^{(j)} − y)`  (Eq 9)

**Standardized**  `x''^{(j)} = \hat{x}'^{(j)} - \eta\, A^{*}\big(A\hat{x}'^{(j)} - y\big)`,  with `x̂'^{(j)} := f_{\text{CNN}}^{(j)}(x'^{(j-1)})`, `x'^{(0)} = A* y`

**Meaning** — one gradient-descent step toward data consistency after each CNN denoise. `η` is a **trainable**
scalar step size learned by backprop. `K = 5` such CNN→DC cascades.

**This is the heart of the paper.** Compare directly to proximal gradient / ISTA:
```
ISTA:              x^{k+1} = prox_{γλR}( x^k − γ Aᴴ(Ax^k − y) )
Unrolled (E9):     x^{k+1} = DC^{(k)}( f_CNN^{(k)}(x^k) )     ← CNN replaces prox, learned η replaces γ
```
The CNN plays the role of the proximal operator of an *implicit, learned* regularizer; DC enforces the physics.

**DL connection** — a textbook **model-based DL / unrolled-optimization** block (MoDL/VarNet family, refs 25–30).
Weights may be shared or per-cascade; here `η` is learned.

**Verification status** — ✅ correct (learned-step preconditioned gradient descent).

---

## E10 — Composite network (supervised)

**Source form**  `x̂ = f_comp(y', S)`  (Eq 10)

**Standardized**  `\hat{x} = f_{\text{comp}}(y', S)`   (`y'` = zero-filled data, `S` = coil maps)

**Meaning** — the composite (anatomy) network maps zero-filled undersampled data + coil maps to a clean
composite image. Trainable in a **fully supervised** way because a well-sampled composite target *exists*.

**Verification status** — ✅ correct.

---

## E11 — Supervised image-space loss (composite)

**Source form**  `L_x(x̂,x) = α ‖x̂−x‖₁/‖x‖₁ + (1−α) ‖x̂−x‖₂/‖x‖₂`  (Eq 11)

**Standardized**  `\mathcal{L}_x(\hat{x},x)=\alpha\dfrac{\|\hat{x}-x\|_1}{\|x\|_1}+(1-\alpha)\dfrac{\|\hat{x}-x\|_2}{\|x\|_2},\quad \alpha=\tfrac12`

**Meaning** — scale-invariant blend of relative ℓ¹ (sharp/robust) and relative ℓ² (smooth) image error.
Normalizing by `‖x‖` makes the loss invariant to overall image scale.

**Statistical note (Expert E)** — mixing ℓ¹/ℓ² is a robustness/MAP-flavored choice, *not* an unbiased estimator
of anything in particular; treat the 50/50 split as a tuned hyperparameter (Audit A9).

**Verification status** — ✅ correct.

---

## E12 — Self-supervised k-space projection (TE/T2 network)

**Source form**  `ŷ = A f_{T2}(y', S)`  (Eq 12)

**Standardized**  `\hat{y} = A\, f_{T2}(y', S)`

**Meaning** — for T2 mapping there is **no** clean target (views/TE ≤ 12, no well-sampled reference). So the
network output `f_T2(y')` is projected *back to k-space* by `A`, and the loss is computed **in k-space** against
the acquired data `y`. This is a self-supervised, physics-consistency loss.

**Contrast with SSDU (ref 43)** — vanilla SSDU splits k-space into disjoint *input* and *loss* sets. Here the
loss is computed over the **entire** acquired `y` (not a disjoint held-out subset) "to further enforce data
consistency." 🔴 Common-mistake flag: this weakens the leakage protection SSDU was designed for — see Audit note
and Comparison #18 (supervised vs self-supervised). Worth interrogating for your own work.

**Verification status** — ✅ correct as stated; ⚠️ the "loss over entire y" choice is a design decision to scrutinize.

---

## E13 — Self-supervised k-space loss (TE/T2)

**Source form**  `L_y(ŷ,y) = α ‖ŷ−y‖₁/‖y‖₁ + (1−α) ‖ŷ−y‖₂/‖y‖₂`  (Eq 13)

**Standardized**  `\mathcal{L}_y(\hat{y},y)=\alpha\dfrac{\|\hat{y}-y\|_1}{\|y\|_1}+(1-\alpha)\dfrac{\|\hat{y}-y\|_2}{\|y\|_2},\quad \alpha=\tfrac12`

**Meaning** — same relative ℓ¹/ℓ² blend as E11 but in **k-space**. Minimizing k-space error is the only training
signal for the T2 pathway. Note (2.5): T2 error is *not* in the loss — it is used only for **model selection**
(pick the epoch with lowest ROI T2 error on the validation set).

**Verification status** — ✅ correct.

---

## Importance ranking for *your* PhD (accelerated CS + DL MRI)

| Rank | Eqs | Why it matters most for you |
|---|---|---|
| 1 | **E9 (+E7,E8)** | The unrolled DC step — the literal CS→DL bridge; ISTA/FISTA with a learned prox. Master this first. |
| 2 | **E5/E6 + A2** | The forward/adjoint convention. Everything (DC, self-supervision) rides on getting `A`,`Aᴴ` right. |
| 3 | **E1** | The MRI forward model. If you can't derive/implement `A` and its true `Aᴴ`, nothing downstream is trustworthy. |
| 4 | **E4** | Temporal-subspace (SVD/PC) compression — classical CS sparsity reused inside a DL net. |
| 5 | **E12/E13** | Self-supervision without ground truth — directly relevant to "can we train recon without fully-sampled data." |
| 6 | **E11** | Loss design / scale-invariance — the statistical-validity surface. |
| 7 | **E2/E3/E10** | Composite vs per-TE recon — the anatomy-vs-quantitative split. |
