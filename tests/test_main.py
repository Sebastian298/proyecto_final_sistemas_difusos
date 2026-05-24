"""Tests for the main module."""

import pytest

from sistemas_difusos.main import main


def test_main_runs_without_error(capsys: pytest.CaptureFixture[str]) -> None:
    """Ensure main executes without raising exceptions."""
    main()
    captured = capsys.readouterr()
    assert "Sistemas Difusos" in captured.out
