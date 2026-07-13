# 05 — Compressed-Sensing Theory & Fundamentals

Built to answer your request directly: *use the Introduction's CS references to build the fundamental concepts
of compressed sensing.* This file gives (1) the fundamentals with honest source-labeling, and (2) a graded
**reading path** that starts from the author's own recommended CS references (§13 Reference Map).

> **Reality check up front:** Toner 2025 *uses* CS (the temporal-subspace / PC-coefficient kind) but does **not**
> teach or cite CS theory. So "the fundamentals the author recommends" = the **Arizona subspace-CS lineage**
> (refs 22, 23, 21, 24, 18, 19). The **abstract CS theory** (RIP, incoherence, ℓ¹ recovery) comes from *outside*
> this paper (Lustig 2007; Candès–Romberg–Tao; Donoho) — labeled **Background** below.

---

## 1. The three ingredients of compressed sensing  (Background — standard CS theory)

CS recovers a signal from **far fewer measurements than Nyquist** when three conditions hold:

1. 🔵 **Sparsity / compressibility.** The signal `x` has a representation `x = Ψα` in some transform `Ψ`
   (wavelets, temporal PCs, finite differences) where `α` has few large entries (`‖α‖₀ = k ≪ N`) or decays fast
   (compressible). *In this paper:* the **temporal** decay across 32 TEs lives in a `P = 4`-dim SVD subspace
   (Eq 4) — 99.96% of variance in 4 PCs. That is the sparsity CS exploits here.
2. 🔵 **Incoherence.** The sensing operator (Fourier sampling) must be incoherent with the sparsity basis, so
   undersampling artifacts look like **noise**, not structured aliasing. *In this paper:* **radial
   pseudo-golden-angle** sampling → incoherent, noise-like streaks (ideal for CS), and each TE sees different
   angles → temporal incoherence.
3. 🔵 **Nonlinear recovery.** Solve a convex program that promotes sparsity:
   `min_x ½‖Ax − y‖₂² + λ‖Ψx‖₁` (analysis) or `min_α ½‖AΨα − y‖₂² + λ‖α‖₁` (synthesis).

🟢 **Intuition:** Nyquist says "sample at 2× the bandwidth." CS says "if the signal is sparse *and* your
sampling is incoherent, a handful of random-ish measurements plus an ℓ¹ solve recovers it." Radial MRI is
almost purpose-built for this: it's naturally incoherent and motion-robust.

## 2. Why ℓ¹? (Background)
🟣 The ℓ⁰ "count the nonzeros" problem is NP-hard. ℓ¹ is its **convex relaxation** — the tightest convex norm
that still promotes sparsity (the ℓ¹ ball's corners lie on the axes). Under the **Restricted Isometry Property**
(RIP) — `A` nearly preserves norms of sparse vectors — ℓ¹ minimization **provably** recovers the ℓ⁰ solution.
RIP is the theoretical guarantee; incoherence is the practical, checkable proxy.

## 3. Sample complexity & phase transitions (Background — relevant to your open questions)
🟡 CS theory predicts recovery needs `M ≳ k · log(N/k)` measurements. As you cross that boundary, recovery
undergoes a **sharp phase transition** (Donoho–Tanner) — perfect below acceleration `R_c`, collapse above it.
**This is directly relevant to your Open Question #9 and the Table-1 "160→128 view cliff":** the paper *empirically*
finds 160 views is the sweet spot and performance drops at 128 — a phase-transition-flavored phenomenon, though
the paper never frames it that way. A defensible PhD thread: *does the DL recon inherit a CS-like failure
boundary, and can classical phase-transition theory predict it?* (See `11_RESEARCH_ROADMAP.md`, `14_OPEN_QUESTIONS.md`.)

## 4. The subspace / low-rank flavor of CS this paper uses  (Source-cited: refs 22, 23, 24)
This is the CS you actually need for Toner 2025:

- 🟠 The T2 decay at each voxel follows a smooth (multi-)exponential governed by the **SEPG signal model**
  (ref 24). Build a **dictionary** of plausible decay curves.
- 🟣 **SVD the dictionary** → the decay space is nearly low-rank; keep the top `P = 4` singular vectors `U`.
  Any TE time-series ≈ a linear combo of 4 temporal basis functions ⟹ **temporal sparsity/low-rank**.
- 🟣 Reconstruct the **PC coefficient maps** (4 spatial maps) instead of 32 TE images — fewer unknowns, and CS/
  low-rank regularization stabilizes the inverse (refs 22 "PC-coefficient CS", 23 "subspace + non-local low-rank").
- ➡️ **Toner 2025's move:** put this exact subspace `U` (Eq 4) *inside* an unrolled DL network, and let a CNN
  supply the regularizer instead of a hand-designed ℓ¹/low-rank prior. **That is the CS→DL bridge of the paper.**

## 5. Analysis vs synthesis sparsity (fundamental distinction)
| | Synthesis | Analysis |
|---|---|---|
| Model | `x = Ψα`, penalize `‖α‖₁` | penalize `‖Ψx‖₁` directly |
| Unknown | coefficients `α` | image `x` |
| TV is... | — | an **analysis** prior (`Ψ = ∇`) |
| This paper | PC/subspace = a **synthesis**-flavored temporal model (`x` built from PC basis `U`) | (spatial CNN prior is neither — it's *learned*) |

## 6. Where the fundamentals live vs. where this paper lives
```
   CS THEORY (Background, NOT cited here)          THIS PAPER'S CS (Source-cited)
   ─────────────────────────────────────           ──────────────────────────────
   sparsity · incoherence · RIP · ℓ¹        →       temporal SVD subspace (P=4), radial incoherence
   Lustig 2007 (Sparse MRI)                 →       Huang 2012 (ref 22, PC-coefficient CS)  ⭐
   Candès/Donoho (recovery guarantees)      →       Mandava 2021 (ref 23, subspace + LLR)
   Block 2007 (radial TV CS)                →       Altbach 2005 (ref 21, echo-sharing predecessor)
   FISTA / ADMM (optimization)              →       replaced by learned unrolled DC (Eq 9)
```

---

## 7. Recommended reading path (graded) 📌

**Tier 0 — the true CS fundamentals (do these first even though the paper skips them):**
1. **Lustig, Donoho, Pauly 2007, *Sparse MRI*** (MRM 58:1182). The canonical CS-MRI paper. — *Background.*
2. Candès–Romberg–Tao 2006 **or** Donoho 2006 for the recovery theorem + RIP intuition. — *Background.*
3. Block, Uecker, Frahm 2007 — radial + TV CS-MRI (closest classical analog to RADTSE). — *Background.*

**Tier 1 — the author's own CS lineage (what the Introduction actually recommends, §13.A):**
4. **Ref 22 — Huang 2012, PC-coefficient-map CS** ⭐ (the keystone for this paper's subspace idea).
5. Ref 24 — Lebel 2010, SEPG signal model (why the temporal subspace is low-dimensional).
6. Ref 23 — Mandava 2021, subspace + non-local low-rank (the LLR baseline lineage).
7. Refs 21, 18, 19 — echo-sharing predecessor + dictionary-matching T2 fitting.

**Tier 2 — the CS→DL bridge (physics-driven unrolled nets):**
8. **Ref 25 — Hammernik physics-driven-DL review** (best survey).
9. Ref 30 — VarNet; Ref 28 — deep cascade; Ref 43 — SSDU (self-supervision, Eq 12–13).

👉 If you read only three things: **Lustig 2007** (fundamentals) → **Huang 2012 / ref 22** (this paper's CS) →
**Hammernik review / ref 25** (how CS becomes DL). That trio takes you from CS first principles to exactly where
Toner 2025 sits.

✅ **Mastery check for this file:** (a) Name the three CS ingredients and give the RADTSE instance of each.
(b) Explain why `P = 4` PCs is "temporal sparsity." (c) State which reference is the keystone CS paper *for this
work* and which is the keystone CS paper *for the field* — and why they're different.
