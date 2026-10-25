# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""Combinatorial Fargues–Fontaine vector bundles.

Treatise correspondence: see Appendix G of the book (The Reference Implementation).
Genuine computation: slope decompositions, degree/rank, HN polygons,
semistability, duals, tensor slopes, and Hom vanishing predictions.
Interface-only: the analytic curve, untilts, and sheaf cohomology.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from typing import Sequence

from .newton import NewtonPolygon


@dataclass(frozen=True)
class FFBundle:
    slopes: tuple[Fraction, ...]
    label: str = "E"

    @classmethod
    def from_slopes(
        cls, slopes: Sequence[int | Fraction], label: str = "E"
    ) -> "FFBundle":
        return cls(tuple(sorted((Fraction(x) for x in slopes), reverse=True)), label)

    @property
    def rank(self) -> int:
        return len(self.slopes)

    @property
    def degree(self) -> Fraction:
        return sum(self.slopes, Fraction(0))

    @property
    def average_slope(self) -> Fraction:
        if not self.slopes:
            raise ValueError("zero bundle has no average slope")
        return self.degree / self.rank

    @property
    def semistable(self) -> bool:
        return len(set(self.slopes)) <= 1

    def dual(self) -> "FFBundle":
        return FFBundle.from_slopes((-slope for slope in self.slopes), f"{self.label}∨")

    def tensor(self, other: "FFBundle") -> "FFBundle":
        return FFBundle.from_slopes(
            (left + right for left, right in product(self.slopes, other.slopes)),
            f"{self.label}⊗{other.label}",
        )

    def hn_polygon(self) -> NewtonPolygon:
        return NewtonPolygon.from_slopes(tuple(reversed(self.slopes)))

    def hom_may_be_nonzero_to(self, other: "FFBundle") -> bool:
        if not self.slopes or not other.slopes:
            return False
        return min(self.slopes) <= max(other.slopes)
