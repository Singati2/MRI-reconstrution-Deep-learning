# 13 — Reference Map (with a Compressed-Sensing reading path)

This maps the paper's 48 references to *what you should read and why*, and — per your request — pulls out the
**compressed-sensing references the Introduction actually leans on**, then honestly flags the canonical CS
foundations the paper *assumes but never cites*.

> **Accuracy labels (your own rules §2.2):** **Source-cited** = literally in Toner 2025's reference list;
> **Background** = standard CS foundation I'm recalling from knowledge (not in this paper — verify before quoting);
> **Needs verification** = read it yourself before relying on details.

---

## A. The CS references the Introduction points you to  (Source-cited)

The intro's key CS sentence (p.2476): *"Compressed sensing (CS) techniques that rely on temporal correlations
between neighboring TEs have been shown to be effective in reconstructing undersampled RADTSE data without the
limitations of echo-sharing¹⁸,¹⁹,²²⁻²⁴."* These are the author's own "read this for the CS background" pointers —
note they are the **Arizona group's applied subspace/temporal-CS lineage**, not the abstract CS theory papers.

| Ref | Citation (as in paper) | What it gives you | Read for |
|---|---|---|---|
| **22** ⭐ | Huang, Graff, Clarkson, Bilgin, Altbach. *T2 mapping from highly undersampled data by reconstruction of principal-component coefficient maps using compressed sensing.* MRM 2012;67:1355–1366. | **The foundational CS-for-RADTSE paper.** Introduces the **PC/subspace coefficient-map CS** that Eq (4) in Toner 2025 reuses (SVD of a signal-decay dictionary → few PCs → sparse temporal representation → CS recon). Also the **LLR baseline** family. | **START HERE.** This is the single most load-bearing CS reference for understanding *why* the DL net works in a 4-PC subspace. |
| **23** | Mandava, Keerthivasan, Martin, Altbach, Bilgin. *Improving subspace-constrained radial fast spin echo MRI using block matching and non-local low-rank regularization.* Phys Med Biol 2021;66:04NT03. | **Subspace + low-rank** regularization — the direct predecessor of the LLR baseline (ref 22's descendant) that DL is compared against. Shows the classical prior the network implicitly replaces. | Understand the LLR baseline and low-rank temporal priors. |
| **21** | Altbach, Bilgin, Li, Clarkson, Trouard, Gmitro. *Processing of radial fast spin-echo data for obtaining T2 estimates from a single k-space data set.* MRM 2005;54:549–559. | **Echo-sharing** — the pre-CS method CS *improves upon*. Explains why sharing k-space across TEs causes spurious T2. | The "before CS" baseline; motivates everything. |
| **18** | Huang, Bilgin, Barr, Altbach. *T2 relaxometry with indirect echo compensation from highly undersampled data.* MRM 2013;70:1026–1037. | Dictionary-matching T2 fit **with stimulated/indirect-echo compensation** from undersampled data. | The T2-fitting side (dictionary matching) that consumes the CS-reconstructed TE images. |
| **19** | Huang, Altbach, Fakhri. *Pattern recognition for rapid T2 mapping with stimulated echo compensation.* MRI 2014;32:969–974. | Pattern-recognition / dictionary approach to rapid T2 mapping. | Same fitting lineage as ref 18. |
| **24** | Lebel, Wilman. *Transverse relaxometry with stimulated-echo compensation.* MRM 2010;64:1005–1014. | The **SEPG** (slice-resolved extended phase graph) **signal model** used to build the dictionary whose SVD gives the PCs (Eq 4). | *Why* the temporal subspace is low-dimensional in the first place — the physics of the decay curves. |

**How they connect (the CS story of this paper):**
```
echo-sharing (21)   →  spurious T2, so...
SEPG signal model (24)  gives realistic decay curves  →  build a dictionary
   →  SVD the dictionary → few PCs (temporal sparsity)  →  subspace/PC-coefficient CS (22, 23)
   →  Toner 2025 puts that same subspace INSIDE an unrolled DL net (Eq 4, 12, 13)
dictionary matching (18, 19)  fits the final TE images voxel-wise → T2 map
```

## B. Physics-driven / unrolled DL references (Source-cited) — the CS→DL bridge
| Ref | What it gives you |
|---|---|
| **25** | Hammernik, Küstner, Yaman, et al. *Physics-driven DL for computational MRI* (review). **The best single survey** of combining physics + ML for MRI recon. |
| **28** | Schlemper, Caballero, Hajnal, Price, Rueckert. *Deep cascade of CNNs for MR recon* — the cascaded-network architecture Toner builds on. |
| **29** | Schlemper et al. *Nonuniform variational network* — radial/NUFFT unrolled net. |
| **30** | Hammernik et al. *Learning a Variational Network* — VarNet, the canonical unrolled recon. |
| **43** | Yaman et al. *Self-supervised learning of physics-guided recon without fully sampled reference* — **SSDU**, the basis for the self-supervised loss (Eq 12–13). |

## C. Canonical CS FOUNDATIONS the paper ASSUMES but does NOT cite  (Background — verify before quoting)
> ⚠️ Important honesty flag: Toner 2025 is an *applied* paper. It never cites the theory that "compressed
> sensing" rests on. If you want the **fundamental concepts** (sparsity, incoherence, RIP, sample complexity,
> ℓ¹ recovery, phase transitions), you must go **outside** this reference list. These are the standard sources
> (I'm recalling them from background knowledge — confirm details yourself):

| Topic | Standard source (Background — not in Toner 2025) |
|---|---|
| CS-MRI birth | Lustig, Donoho, Pauly. *Sparse MRI: the application of CS for rapid MR imaging.* MRM 2007;58:1182–1195. **The** CS-MRI paper — read this for fundamentals. |
| CS theory | Candès, Romberg, Tao (2006) — robust uncertainty principles / stable recovery; Donoho (2006) — *Compressed Sensing*, IEEE T-IT. |
| RIP & recovery | Candès, Tao — restricted isometry property, ℓ¹ recovery guarantees. |
| Radial + TV CS-MRI | Block, Uecker, Frahm (2007) — *Undersampled radial MRI with TV constraint*, MRM. (Closest classical analog to RADTSE CS.) |
| Phase transitions | Donoho–Tanner — ℓ¹/ℓ⁰ phase-transition diagrams (relevant to your open question #9 on failure boundaries). |
| Optimization | Beck–Teboulle 2009 (FISTA); Boyd et al. 2011 (ADMM); Parikh–Boyd (proximal algorithms). |

**Takeaway:** for the *fundamentals of CS*, read **Lustig 2007 (Sparse MRI)** first, then the theory pair
(Candès–Romberg–Tao / Donoho). For *this paper's flavor of CS* (temporal-subspace CS on RADTSE), read the
author's own lineage — **ref 22 (Huang 2012) is the keystone**, supported by 23, 21, 24, 18, 19. The
recommended order is in `05_COMPRESSED_SENSING_THEORY.md`.
