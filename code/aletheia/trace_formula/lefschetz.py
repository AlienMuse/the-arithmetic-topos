# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""Categorical Lefschetz and Atiyah–Bott index assembly.

Treatise correspondence: see Appendix G of the book (The Reference Implementation).
Genuine computation: finite fixed-point contributions, normal determinant
factors, cohomological supertraces, and exact comparison diagnostics.
Interface-only: nonproper localization and renormalized analytic indices.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Mapping, Sequence

from aletheia.core.trace import supertrace


@dataclass(frozen=True)
class FixedPointContribution:
    component: str
    numerator_trace: Fraction | complex
    normal_determinant: Fraction | complex
    multiplicity: int = 1

    @property
    def value(self) -> complex:
        if self.normal_determinant == 0:
            raise ZeroDivisionError("degenerate fixed point needs derived localization")
        return (
            self.multiplicity * complex(self.numerator_trace)
            / complex(self.normal_determinant)
        )


@dataclass(frozen=True)
class LefschetzIndex:
    cohomology_actions: Mapping[int, Sequence[Sequence[complex]]]
    fixed_points: tuple[FixedPointContribution, ...]
    boundary_residue: complex = 0j

    @property
    def spectral(self) -> complex:
        return supertrace(self.cohomology_actions)

    @property
    def geometric(self) -> complex:
        return sum((point.value for point in self.fixed_points), 0j) + self.boundary_residue

    def discrepancy(self) -> complex:
        return self.geometric - self.spectral

    def verifies(self, tolerance: float = 1e-10) -> bool:
        return abs(self.discrepancy()) <= tolerance
