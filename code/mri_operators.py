"""
mri_operators.py — Stages 1–3 of the coding curriculum (Toner 2025 study).

Cartesian single-coil stand-in for the RADTSE forward model. We use the *Cartesian*
FFT here (not NUFFT) so the operators are exact and the adjoint test passes cleanly;
the radial NUFFT version comes in a later lab (SigPy/torchkbnufft) — the linear-operator
*structure* (forward A, true adjoint A^H, mask P) is identical.

Design note tied to Source Audit A2:
  * `forward`/`adjoint` here are a TRUE adjoint pair  ->  they PASS the dot-product test.
  * The paper's `A*` folds in density compensation (A* := A^H D) and is NOT a true adjoint.
    Keep the two ideas separate: test with the true adjoint, precondition only in the DC step.

Runs on CPU; NumPy only. No GPU needed for these stages.
Shapes are asserted everywhere. Complex dtype is preserved end to end.
"""
from __future__ import annotations
import numpy as np

# ----------------------------------------------------------------------------- Stage 1: centered FFT
def fft2c(x: np.ndarray) -> np.ndarray:
    """Centered orthonormal 2D FFT (image -> k-space). Preserves complex dtype."""
    assert np.iscomplexobj(x) or np.isrealobj(x), "x must be array-like"
    return np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(x), norm="ortho"))


def ifft2c(k: np.ndarray) -> np.ndarray:
    """Centered orthonormal 2D inverse FFT (k-space -> image)."""
    return np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(k), norm="ortho"))


# ----------------------------------------------------------------------------- Stage 2: sampling masks
def cartesian_mask(shape, accel: int, center_frac: float = 0.08, seed: int | None = 0) -> np.ndarray:
    """1D phase-encode undersampling mask (columns kept), fully sampled center.

    Returns a float64 {0,1} mask of `shape`. Acceleration `accel` = 1/fraction-of-lines-kept.
    """
    ny, nx = shape
    rng = np.random.default_rng(seed)
    n_center = max(1, int(round(center_frac * nx)))
    n_total = max(n_center, int(round(nx / accel)))
    c0 = (nx - n_center) // 2
    keep = set(range(c0, c0 + n_center))
    remaining = [j for j in range(nx) if j not in keep]
    n_extra = max(0, n_total - n_center)
    keep |= set(rng.choice(remaining, size=min(n_extra, len(remaining)), replace=False).tolist())
    mask = np.zeros((ny, nx), dtype=np.float64)
    mask[:, sorted(keep)] = 1.0
    return mask


def acceleration_of(mask: np.ndarray) -> float:
    """Effective acceleration = total / sampled."""
    return mask.size / max(1.0, float(mask.sum()))


# ----------------------------------------------------------------------------- Stage 3: forward / adjoint
def forward(x: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """A x = P F x  (image -> undersampled k-space). Single coil."""
    assert x.shape == mask.shape, f"shape mismatch {x.shape} vs {mask.shape}"
    return mask * fft2c(x)


def adjoint(y: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """A^H y = F^H P^H y  (undersampled k-space -> image). TRUE adjoint of `forward`."""
    assert y.shape == mask.shape, f"shape mismatch {y.shape} vs {mask.shape}"
    return ifft2c(mask * y)   # P is a real diagonal 0/1 -> P^H = P


def zero_filled(y: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """Zero-filled reconstruction x_ZF = A^H y (aliased)."""
    return adjoint(y, mask)


# ----------------------------------------------------------------------------- adjoint (dot-product) test
def adjoint_test(shape=(64, 64), seed: int = 0) -> float:
    """Return relative error of  <A x, y> vs <x, A^H y>.  Should be ~1e-12 (machine eps)."""
    rng = np.random.default_rng(seed)
    mask = cartesian_mask(shape, accel=4, seed=seed)
    x = (rng.standard_normal(shape) + 1j * rng.standard_normal(shape))
    y = (rng.standard_normal(shape) + 1j * rng.standard_normal(shape))
    lhs = np.vdot(forward(x, mask), y)      # <A x, y>
    rhs = np.vdot(x, adjoint(y, mask))      # <x, A^H y>
    return abs(lhs - rhs) / max(abs(lhs), 1e-30)


if __name__ == "__main__":
    print(f"adjoint-test relative error = {adjoint_test():.2e}  (expect < 1e-10)")
