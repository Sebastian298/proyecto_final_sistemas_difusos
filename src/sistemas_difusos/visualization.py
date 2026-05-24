"""Plot generation and validation output for the air purifier controller."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from sistemas_difusos.controller import FuzzyAirPurifierController, SimulationCase
from sistemas_difusos.membership import trapezoidal, triangular

VALIDATION_CASES: tuple[SimulationCase, ...] = (
    # Universe extremes
    SimulationCase(aqi=0, occupancy=0),
    SimulationCase(aqi=200, occupancy=100),
    # Crisp threshold boundary (occupancy fixed at 50%)
    SimulationCase(aqi=89, occupancy=50),
    SimulationCase(aqi=90, occupancy=50),
    SimulationCase(aqi=95, occupancy=50),
    # All 12 fuzzy rule combinations (AQI x occupancy)
    SimulationCase(aqi=25, occupancy=10),
    SimulationCase(aqi=25, occupancy=50),
    SimulationCase(aqi=25, occupancy=90),
    SimulationCase(aqi=85, occupancy=10),
    SimulationCase(aqi=85, occupancy=50),
    SimulationCase(aqi=85, occupancy=90),
    SimulationCase(aqi=130, occupancy=10),
    SimulationCase(aqi=130, occupancy=50),
    SimulationCase(aqi=130, occupancy=90),
    SimulationCase(aqi=180, occupancy=10),
    SimulationCase(aqi=180, occupancy=50),
    SimulationCase(aqi=180, occupancy=90),
    # Transition zones between membership sets
    SimulationCase(aqi=70, occupancy=40),
    SimulationCase(aqi=115, occupancy=70),
    SimulationCase(aqi=145, occupancy=50),
    # Additional operational scenarios
    SimulationCase(aqi=80, occupancy=30),
    SimulationCase(aqi=120, occupancy=70),
    SimulationCase(aqi=170, occupancy=85),
)


def save_membership_plots(controller: FuzzyAirPurifierController, output_dir: Path) -> None:
    """Save input and output membership function plots."""
    aqi_u = controller.aqi_u
    occ_u = controller.occ_u
    p_u = controller.power_u

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    axes[0].plot(aqi_u, trapezoidal(aqi_u, 0, 0, 40, 70), label="AQI bueno")
    axes[0].plot(aqi_u, triangular(aqi_u, 55, 85, 115), label="AQI moderado")
    axes[0].plot(aqi_u, triangular(aqi_u, 100, 130, 160), label="AQI malo")
    axes[0].plot(aqi_u, trapezoidal(aqi_u, 145, 170, 200, 200), label="AQI critico")
    axes[0].set_title("Membresias de entrada: calidad de aire")
    axes[0].set_xlabel("AQI")
    axes[0].set_ylabel("Membresia")
    axes[0].set_ylim(0, 1.05)
    axes[0].legend(loc="best")

    axes[1].plot(occ_u, trapezoidal(occ_u, 0, 0, 20, 40), label="Ocupacion baja")
    axes[1].plot(occ_u, triangular(occ_u, 30, 50, 70), label="Ocupacion media")
    axes[1].plot(occ_u, trapezoidal(occ_u, 60, 80, 100, 100), label="Ocupacion alta")
    axes[1].set_title("Membresias de entrada: ocupacion")
    axes[1].set_xlabel("Ocupacion (%)")
    axes[1].set_ylabel("Membresia")
    axes[1].set_ylim(0, 1.05)
    axes[1].legend(loc="best")

    fig.tight_layout()
    fig.savefig(output_dir / "pf_membresias_entradas.png", dpi=180)
    plt.close(fig)

    fig2, ax2 = plt.subplots(figsize=(7, 4))
    ax2.plot(p_u, trapezoidal(p_u, 0, 0, 10, 20), label="Muy baja")
    ax2.plot(p_u, triangular(p_u, 15, 28, 40), label="Baja")
    ax2.plot(p_u, triangular(p_u, 35, 50, 65), label="Media")
    ax2.plot(p_u, triangular(p_u, 60, 75, 88), label="Alta")
    ax2.plot(p_u, trapezoidal(p_u, 82, 92, 100, 100), label="Muy alta")
    ax2.set_title("Membresias de salida: potencia del purificador")
    ax2.set_xlabel("Potencia (%)")
    ax2.set_ylabel("Membresia")
    ax2.set_ylim(0, 1.05)
    ax2.legend(loc="best")
    fig2.tight_layout()
    fig2.savefig(output_dir / "pf_membresias_salida.png", dpi=180)
    plt.close(fig2)


def save_control_surface(controller: FuzzyAirPurifierController, output_dir: Path) -> None:
    """Save the control surface power(AQI, occupancy)."""
    aqi_grid = np.linspace(0, 200, 61)
    occ_grid = np.linspace(0, 100, 41)

    surface = np.zeros((occ_grid.size, aqi_grid.size), dtype=float)
    for i, occ in enumerate(occ_grid):
        for j, aqi in enumerate(aqi_grid):
            power, _ = controller.infer(float(aqi), float(occ))
            surface[i, j] = power

    aqi_mesh, occ_mesh = np.meshgrid(aqi_grid, occ_grid)
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(aqi_mesh, occ_mesh, surface, cmap="cividis", edgecolor="none")
    ax.set_title("Superficie de control difuso del purificador")
    ax.set_xlabel("AQI")
    ax.set_ylabel("Ocupacion (%)")
    ax.set_zlabel("Potencia (%)")
    fig.tight_layout()
    fig.savefig(output_dir / "pf_superficie_control.png", dpi=180)
    plt.close(fig)


def save_threshold_comparison(controller: FuzzyAirPurifierController, output_dir: Path) -> None:
    """Compare threshold control vs fuzzy control as a function of AQI."""
    aqi_values = np.linspace(70, 105, 141)
    fuzzy_values = []
    crisp_values = []
    occ_fixed = 50.0

    for aqi in aqi_values:
        fuzzy_power, _ = controller.infer(float(aqi), occ_fixed)
        fuzzy_values.append(fuzzy_power)
        crisp_values.append(controller.crisp_baseline(float(aqi)))

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(aqi_values, fuzzy_values, label="Control difuso", linewidth=2.2)
    ax.plot(aqi_values, crisp_values, label="Control por umbral", linestyle="--", linewidth=2.0)
    ax.axvline(89.0, color="gray", linestyle=":", label="AQI=89")
    ax.set_title("Comparacion: umbral vs logica difusa")
    ax.set_xlabel("AQI (ocupacion fija 50%)")
    ax.set_ylabel("Potencia del purificador (%)")
    ax.set_ylim(-2, 102)
    ax.legend(loc="best")
    fig.tight_layout()
    fig.savefig(output_dir / "pf_comparacion_umbral_vs_difuso.png", dpi=180)
    plt.close(fig)


def save_validation_table(controller: FuzzyAirPurifierController, output_dir: Path) -> None:
    """Save validation scenarios to a plain text file."""
    lines = [
        "Validacion - Purificador de aire con logica difusa",
        "=" * 52,
        f"Escenarios evaluados: {len(VALIDATION_CASES)}",
        "AQI | Ocupacion(%) | Potencia umbral(%) | Potencia difusa(%)",
    ]
    for case in VALIDATION_CASES:
        baseline = controller.crisp_baseline(case.aqi)
        fuzzy_power, _ = controller.infer(case.aqi, case.occupancy)
        lines.append(
            f"{case.aqi:>3.0f} | {case.occupancy:>11.1f} | {baseline:>18.1f} | {fuzzy_power:>17.2f}"
        )

    (output_dir / "pf_validacion.txt").write_text("\n".join(lines), encoding="utf-8")
