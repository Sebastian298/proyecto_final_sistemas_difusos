"""Tests for membership functions."""

import numpy as np
import pytest

from sistemas_difusos.membership import trapezoidal, triangular


def test_trapezoidal_plateau() -> None:
    """Trapezoidal membership should be 1.0 on the flat top."""
    x = np.array([50.0])
    assert trapezoidal(x, 10, 30, 70, 90)[0] == pytest.approx(1.0)
