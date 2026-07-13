# 11 — Research Roadmap (source-grounded, for your CS+DL imaging dissertation)

Directions **traceable to Toner 2025**, split into replication (A), extension (B), and PhD-level (C). Each carries
a **novelty risk** flag — nothing here is claimed novel until a literature check confirms it (§2.4).

> ⚠️ Novelty caveat: promising directions often die at the literature check. So each item below states **what must
> be checked first** before you invest. Do the lit-check *before* scaffolding any pilot.

## Research-translation table
| Source concept | What it means | Classical MRI use | DL translation | Possible experiment | Novelty risk |
|---|---|---|---|---|---|
| Temporal SVD subspace (Eq 4, P=4) | 32 TEs live in a 4-D decay space | PC-coefficient CS (ref 22) | subspace inside unrolled net | vary P; measure T2-error vs compute | Low (replication) |
| DC layer (Eq 9) | learned-step gradient descent to data | CG / ISTA data term | trainable η, K cascades | ablate K, η-sharing | Low–Med |
| Self-supervised k-space loss (Eq 12–13) | train with no clean target | — | SSDU variant, loss over full y | true-disjoint SSDU vs full-y leakage test | **Med** (see below) |
| 160-view "sweet spot" (Fig 3, Table 1) | performance cliff 160→128 | CS phase transition | DL failure boundary | map error vs views finely | **Med–High** |
| Adjoint-NUFFT-as-reference (Audit A7) | non-ideal gold standard | gridding recon | — | sensitivity of conclusions to reference | Low |

## A. Safe replication projects (build understanding, low risk)
- **A1. Reproduce the Table-1 acceleration trend on a public dataset.** Use fastMRI knee/brain or an open radial
  set; implement adjoint-NUFFT, an LLR/subspace CS baseline, and a small unrolled DC net; reproduce "DL more
  stable than CS as acceleration rises." *Check first:* dataset availability (fastMRI DUA is a known blocker).
  *Minimum publishable result:* a clean replication of the DL-vs-CS-stability curve.
- **A2. Re-derive and unit-test the operators.** Already started in `code/` — extend to radial NUFFT + multicoil,
  verify the *true* adjoint test, then show the paper's `A*=AᴴD` deliberately fails it (Audit A2). Pure understanding.

## B. Methodological extension projects (defensible modification)
- **B1. Disjoint-mask SSDU vs full-y loss.** The paper computes the self-supervised loss over the **entire** `y`
  (Eq 12), unlike vanilla SSDU's disjoint held-out set. **Test whether this leaks** and inflates apparent T2
  accuracy: compare true-disjoint SSDU, full-y, and a supervised oracle. *Check first:* whether SSDU-leakage in
  subspace recon is already characterized (search Yaman 2020+, Millard/Chiew 2023 "theoretical framework for
  self-supervised MRI"). *Novelty risk: Med* — the general leakage question is studied; the *subspace-constrained
  full-y* variant may be a gap. **Verify before committing.**
- **B2. Classical CS prior as an out-of-distribution stabilizer.** Add a TV/low-rank term to the DC step and test
  whether it improves generalization to unseen acceleration/masks (Open Q #2). *Check first:* plug-and-play +
  unrolled hybrids (RED, PnP-VarNet) already exist — position carefully.

## C. Potential PhD-level contributions (real scientific question, higher risk)
- **C1. Does DL recon inherit a CS-style phase transition, and can theory predict the failure boundary?**
  The paper's 160→128 cliff is *empirically* a sharp transition. Map reconstruction error and **uncertainty**
  finely vs. #views; test whether a Donoho–Tanner-style boundary predicts where DL collapses; whether
  **uncertainty rises *before* PSNR collapses** (Open Q #3). Aligns with your standing MRI phase-transition
  prereg — Toner's cliff is concrete supporting motivation. *Check first:* the phase-transition prereg's own
  novelty audit still governs. *Novelty risk: the H0/smooth prior is strong — treat honestly.*
- **C2. Joint calibration of reconstruction quality and downstream T2/lesion task.** Toner evaluates ROI T2 error
  and shows pathology cases but never links reconstruction uncertainty to **lesion detectability / T2 decision**.
  Question: can recon quality and a downstream clinical task be *jointly calibrated*, and do data-consistency
  residuals (Eq 7) predict clinically meaningful failure (Open Q #4, #8, #12)? Natural pairing with the
  **Toner 2026 UQ paper** already on your Desktop. *Novelty risk: Med–High; needs annotated lesion data.*

## Ranking (for your constraints: RTX 2080 Ti, biostat strength, novelty-check discipline)
| Rank | Project | Sci value | Feasibility | Novelty | Data risk | Compute | Verdict |
|---|---|---|---|---|---|---|---|
| 1 | **A1 replication** | Med | High | (n/a) | Med | Low | **Start here** — builds credibility + code. |
| 2 | **C1 phase transition** | High | Med | Med* | Med | Med | Highest upside; ties to your existing prereg. Lit-check H0 first. |
| 3 | **B1 SSDU leakage** | Med-High | Med | Med | Med | Med | Sharp, testable; **must** lit-check Millard/Chiew 2023 first. |
| 4 | **C2 joint calibration** | High | Low-Med | Med-High | High (lesions) | Med | Big, but data-gated; pair with Toner 2026. |

**Immediate next action (before any pilot):** run the lit-checks named in B1 and C1. The novelty check kills more
ideas than the method does — do it *first*.
