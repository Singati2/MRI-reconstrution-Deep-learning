"""Unit + math tests for code/mri_operators.py  (curriculum §15 items 1–4, 7, 8).

Run:  python3 -m pytest tests/ -q     (from the study-directory root)
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))
from mri_operators import (  # noqa: E402
    fft2c, ifft2c, cartesian_mask, acceleration_of, forward, adjoint, adjoint_test,
)


def test_fft_inverse_recovers_image():        # §15.1
    rng = np.random.default_rng(0)
    x = rng.standard_normal((64, 64)) + 1j * rng.standard_normal((64, 64))
    assert np.allclose(ifft2c(fft2c(x)), x, atol=1e-10)


def test_parseval_energy_preserved():          # Stage 1 Parseval
    rng = np.random.default_rng(1)
    x = rng.standard_normal((48, 48)) + 1j * rng.standard_normal((48, 48))
    assert np.isclose(np.linalg.norm(x), np.linalg.norm(fft2c(x)), rtol=1e-10)


def test_adjoint_dot_product():                # §15.2  (TRUE adjoint, not the paper's A*)
    assert adjoint_test((64, 64)) < 1e-10


def test_full_mask_reproduces_fully_sampled(): # §15.3
    rng = np.random.default_rng(2)
    x = rng.standard_normal((32, 32)) + 1j * rng.standard_normal((32, 32))
    full = np.ones((32, 32))
    assert np.allclose(adjoint(forward(x, full), full), x, atol=1e-10)


def test_acceleration_computed_correctly():    # §15.4
    m = cartesian_mask((64, 64), accel=4, center_frac=0.0, seed=3)
    assert 3.0 < acceleration_of(m) < 5.0      # ~4x, integer rounding on columns


def test_shapes_and_complex_preserved():       # §15.7, §15.8
    x = np.ones((16, 16), dtype=np.complex128)
    m = cartesian_mask((16, 16), accel=2, seed=4)
    y = forward(x, m)
    assert y.shape == (16, 16) and np.iscomplexobj(y)
    assert np.iscomplexobj(adjoint(y, m))
