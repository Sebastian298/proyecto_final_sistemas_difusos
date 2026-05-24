"""Fuzzy membership functions and defuzzification utilities."""

from __future__ import annotations

import numpy as np


def triangular(x: np.ndarray, a: float, b: float, c: float) -> np.ndarray:
    """Triangular membership function."""
    y = np.zeros_like(x, dtype=float)
    if b != a:
        rising = (x >= a) & (x <= b)
        y[rising] = (x[rising] - a) / (b - a)
    if c != b:
        falling = (x >= b) & (x <= c)
        y[falling] = np.maximum(y[falling], (c - x[falling]) / (c - b))
    y[x == b] = 1.0
    return np.clip(y, 0.0, 1.0)


def trapezoidal(x: np.ndarray, a: float, b: float, c: float, d: float) -> np.ndarray:
    """Trapezoidal membership function."""
    y = np.zeros_like(x, dtype=float)

    if b != a:
        rising = (x >= a) & (x <= b)
        y[rising] = (x[rising] - a) / (b - a)
    else:
        y[(x >= a) & (x <= b)] = 1.0

    middle = (x >= b) & (x <= c)
    y[middle] = 1.0

    if d != c:
        falling = (x >= c) & (x <= d)
        y[falling] = np.maximum(y[falling], (d - x[falling]) / (d - c))
    else:
        y[(x >= c) & (x <= d)] = 1.0

    return np.clip(y, 0.0, 1.0)


def centroid(x: np.ndarray, mu: np.ndarray) -> float:
    """Centroid defuzzification."""
    if np.allclose(np.sum(mu), 0.0):
        return 0.0
    return float(np.sum(x * mu) / np.sum(mu))
