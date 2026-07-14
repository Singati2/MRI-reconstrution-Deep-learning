# Toner 2025 — CS-MRI / Deep-Learning Study Program

Interactive, source-grounded curriculum built around:
**Toner et al., "Accelerated free-breathing abdominal T2 mapping with deep learning reconstruction of radial
turbo spin-echo data," *Magn Reson Med* 2025;94:2475–2491, DOI 10.1002/mrm.70017.**
Source PDF: `~/Desktop/Magnetic Resonance in Med - 2025 - Toner - Accelerated ... deep learning.pdf`
(The originally-named `cs_techniques_toner2025.html` does not exist — see `00_SOURCE_AUDIT.md`.)

## Build status (turn 1)
| File | Status | Notes |
|---|---|---|
| `00_SOURCE_AUDIT.md` | ✅ **complete** | Manifest + 13-item audit. Key finding: the `A*:=AᴴD` non-adjoint convention. |
| `01_EXECUTIVE_OVERVIEW.md` | ✅ **complete** | Section-by-section + honest gaps. |
| `02_EQUATION_REGISTER.md` | ✅ **complete** | All 13 equations verified + importance ranking. |
| `05_COMPRESSED_SENSING_THEORY.md` | ✅ **complete** | CS fundamentals + reading path from the intro's CS refs. |
| `13_REFERENCE_MAP.md` | ✅ **complete** | 48 refs mapped; CS reading path highlighted. |
| `code/mri_operators.py` | ✅ **runs** | Stages 1–3 (FFT, masks, forward/adjoint). Adjoint test = 5.8e-16. |
| `tests/test_operators.py` | ✅ **runs** | Unit tests for §15 items 1–4, 7, 8. |
| `11_RESEARCH_ROADMAP.md` | ✅ **complete** | Source-grounded PhD directions (A/B/C tiers). |
| `03,04,06,07` (concepts, forward model, optimization, CS→DL) | 🟡 **scaffolded** | Core content is in 01/02/05; these expand it. Build next sessions. |
| **1-Week Plan** (`day01.html` … `day05.html`) | ✅ **complete, interactive, offline** | 5-day arc: adjoints → SVD/DFT → signal/k-space/SEPG → forward model → regularized inverse. Each has a widget, quiz, mastery checklist; each a distinct colour. Linked from `index.html`. |
| `09_INTERACTIVE_QUIZZES.md`, `15_PROGRESS_TRACKER.md` | 🟡 **live in chat** | Lesson 1 started in-session; tracker seeded below. |
| `10_CODING_LABS.md`, `12_GLOSSARY.md`, `14_OPEN_QUESTIONS.md` | 🟡 **partially in 02/05/13** | Consolidate next. |

**Why not all 15 files at once:** this prompt is a semester-length course. Turn 1 delivers the parts that
*required actually reading this paper* (audit, equation register, overview, CS reference path, runnable
operators). The teaching files are built **interactively**, lesson by lesson, so they adapt to your mastery
scores (§12).

## Read order
1. `00_SOURCE_AUDIT.md` — what's in the paper, what to distrust.
2. `01_EXECUTIVE_OVERVIEW.md` — the whole paper in one pass.
3. `05_COMPRESSED_SENSING_THEORY.md` + `13_REFERENCE_MAP.md` — **your CS fundamentals reading path.**
4. `02_EQUATION_REGISTER.md` — the math, verified.
5. `code/` — run `python3 code/mri_operators.py` then `python3 -m pytest tests/`.
6. `11_RESEARCH_ROADMAP.md` — where this goes for your dissertation.

## Environment
- Python 3, NumPy (Stages 1–3, CPU). Later labs: PyTorch + a NUFFT lib (torchkbnufft / SigPy) on your RTX 2080 Ti.
- `requirements.txt` provided (minimal).

## Hardware target
RTX 2080 Ti, 11 GB. All planned labs fit: single-slice, single-coil first; small `K=5`×`L=5` net later,
batch 1, mixed precision if needed — matching the paper's own memory-limited design.
