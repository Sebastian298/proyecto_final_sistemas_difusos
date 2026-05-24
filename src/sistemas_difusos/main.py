"""Application entry point for the fuzzy air purifier project."""

from __future__ import annotations

from pathlib import Path

from sistemas_difusos.controller import FuzzyAirPurifierController
from sistemas_difusos.visualization import (
    save_control_surface,
    save_membership_plots,
    save_threshold_comparison,
    save_validation_table,
)


def get_default_output_dir() -> Path:
    """Return the default directory for generated artifacts."""
    return Path.cwd() / "outputs"


def main(output_dir: Path | None = None) -> Path:
    """Run the fuzzy air purifier simulation and generate outputs."""
    target_dir = output_dir or get_default_output_dir()
    target_dir.mkdir(parents=True, exist_ok=True)

    controller = FuzzyAirPurifierController()
    save_membership_plots(controller, target_dir)
    save_control_surface(controller, target_dir)
    save_threshold_comparison(controller, target_dir)
    save_validation_table(controller, target_dir)

    print("Proyecto final (purificador difuso) ejecutado correctamente.")
    print(f"Resultados guardados en: {target_dir}")
    return target_dir


if __name__ == "__main__":
    main()
