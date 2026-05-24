"""Mamdani fuzzy controller for an air purifier."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from sistemas_difusos.membership import centroid, trapezoidal, triangular


@dataclass(frozen=True)
class SimulationCase:
    """Input scenario for validation."""

    aqi: float
    occupancy: float


class FuzzyAirPurifierController:
    """Mamdani fuzzy controller for an air purifier."""

    def __init__(self) -> None:
        self.aqi_u = np.linspace(0, 200, 401)
        self.occ_u = np.linspace(0, 100, 401)
        self.power_u = np.linspace(0, 100, 501)

    def aqi_memberships(self, value: float) -> dict[str, float]:
        """Membership degrees for air quality index (AQI)."""
        x = np.array([value], dtype=float)
        return {
            "bueno": float(trapezoidal(x, 0, 0, 40, 70)[0]),
            "moderado": float(triangular(x, 55, 85, 115)[0]),
            "malo": float(triangular(x, 100, 130, 160)[0]),
            "critico": float(trapezoidal(x, 145, 170, 200, 200)[0]),
        }

    def occupancy_memberships(self, value: float) -> dict[str, float]:
        """Membership degrees for room occupancy."""
        x = np.array([value], dtype=float)
        return {
            "baja": float(trapezoidal(x, 0, 0, 20, 40)[0]),
            "media": float(triangular(x, 30, 50, 70)[0]),
            "alta": float(trapezoidal(x, 60, 80, 100, 100)[0]),
        }

    def power_sets(self) -> dict[str, np.ndarray]:
        """Output fuzzy sets for purifier power."""
        u = self.power_u
        return {
            "muy_baja": trapezoidal(u, 0, 0, 10, 20),
            "baja": triangular(u, 15, 28, 40),
            "media": triangular(u, 35, 50, 65),
            "alta": triangular(u, 60, 75, 88),
            "muy_alta": trapezoidal(u, 82, 92, 100, 100),
        }

    def infer(self, aqi: float, occupancy: float) -> tuple[float, np.ndarray]:
        """Mamdani inference with AND=min, aggregation=max, and centroid."""
        aqi_mu = self.aqi_memberships(aqi)
        occ_mu = self.occupancy_memberships(occupancy)
        output_sets = self.power_sets()

        rule_map = {
            ("bueno", "baja"): "muy_baja",
            ("bueno", "media"): "baja",
            ("bueno", "alta"): "media",
            ("moderado", "baja"): "baja",
            ("moderado", "media"): "media",
            ("moderado", "alta"): "alta",
            ("malo", "baja"): "media",
            ("malo", "media"): "alta",
            ("malo", "alta"): "muy_alta",
            ("critico", "baja"): "alta",
            ("critico", "media"): "muy_alta",
            ("critico", "alta"): "muy_alta",
        }

        activations: dict[str, list[float]] = {
            "muy_baja": [],
            "baja": [],
            "media": [],
            "alta": [],
            "muy_alta": [],
        }

        for aqi_label, aqi_degree in aqi_mu.items():
            for occ_label, occ_degree in occ_mu.items():
                out_label = rule_map[(aqi_label, occ_label)]
                activations[out_label].append(min(aqi_degree, occ_degree))

        aggregated = np.zeros_like(self.power_u)
        for label, values in activations.items():
            if not values:
                continue
            alpha = max(values)
            clipped = np.minimum(alpha, output_sets[label])
            aggregated = np.maximum(aggregated, clipped)

        return centroid(self.power_u, aggregated), aggregated

    def crisp_baseline(self, aqi: float) -> float:
        """Classical threshold control for comparison with fuzzy logic."""
        return 85.0 if aqi >= 90.0 else 0.0
