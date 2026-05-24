"""Tests for the fuzzy air purifier controller."""

from pathlib import Path

import pytest

from sistemas_difusos.controller import FuzzyAirPurifierController
from sistemas_difusos.main import main
from sistemas_difusos.membership import centroid, triangular
import numpy as np


def test_triangular_peak() -> None:
    """Triangular membership should reach 1.0 at the peak."""
    x = np.array([50.0])
    assert triangular(x, 30, 50, 70)[0] == pytest.approx(1.0)


def test_centroid_returns_zero_for_empty_membership() -> None:
    """Centroid should return 0 when all membership values are zero."""
    x = np.array([0.0, 1.0, 2.0])
    mu = np.zeros(3)
    assert centroid(x, mu) == 0.0


def test_infer_returns_power_within_range() -> None:
    """Inferred power should stay within the output universe."""
    controller = FuzzyAirPurifierController()
    power, _ = controller.infer(aqi=120.0, occupancy=70.0)
    assert 0.0 <= power <= 100.0


def test_crisp_baseline_threshold() -> None:
    """Threshold control should switch at AQI 90."""
    controller = FuzzyAirPurifierController()
    assert controller.crisp_baseline(89.0) == 0.0
    assert controller.crisp_baseline(90.0) == 85.0


def test_main_generates_outputs(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """Main should generate all expected artifacts."""
    output_dir = tmp_path / "outputs"
    result_dir = main(output_dir=output_dir)
    captured = capsys.readouterr()

    assert result_dir == output_dir
    assert "purificador difuso" in captured.out
    assert (output_dir / "pf_membresias_entradas.png").exists()
    assert (output_dir / "pf_membresias_salida.png").exists()
    assert (output_dir / "pf_superficie_control.png").exists()
    assert (output_dir / "pf_comparacion_umbral_vs_difuso.png").exists()
    validation_file = output_dir / "pf_validacion.txt"
    assert validation_file.exists()
    validation_text = validation_file.read_text(encoding="utf-8")
    assert "Escenarios evaluados: 23" in validation_text
