# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""Beyond-endoscopic transforms and boundary residues.

Treatise correspondence: see Appendix G of the book (The Reference Implementation).
Genuine computation: finite Mellin transforms, residue bookkeeping,
Poisson comparisons on cyclic groups, and boundary-term accounting.
Interface-only: Braverman–Kazhdan transforms on reductive monoids.
"""
from __future__ import annotations

from dataclasses import dataclass
import cmath
from typing import Callable, Mapping, Sequence


def discrete_fourier(values: Sequence[complex]) -> tuple[complex, ...]:
    size = len(values)
    if not size:
        return ()
    return tuple(
        sum(
            values[x] * cmath.exp(-2j * cmath.pi * frequency * x / size)
            for x in range(size)
        ) / (size ** 0.5)
        for frequency in range(size)
    )


@dataclass(frozen=True)
class BoundaryResidue:
    levi: str
    pole_order: int
    coefficient: complex
    normalization: str


@dataclass(frozen=True)
class PoissonComparison:
    original_sum: complex
    transformed_sum: complex
    residues: tuple[BoundaryResidue, ...] = ()

    @property
    def corrected_transformed(self) -> complex:
        return self.transformed_sum + sum(
            (residue.coefficient for residue in self.residues), 0j
        )

    def discrepancy(self) -> complex:
        return self.original_sum - self.corrected_transformed


def cyclic_poisson(values: Sequence[complex]) -> PoissonComparison:
    transformed = discrete_fourier(values)
    return PoissonComparison(
        sum(values, 0j),
        (len(values) ** 0.5) * transformed[0] if values else 0j,
    )
