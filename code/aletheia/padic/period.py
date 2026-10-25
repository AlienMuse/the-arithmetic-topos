# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""Period maps and Hodge–Tate/Newton stratification.

Treatise correspondence: see Appendix G of the book (The Reference Implementation).
Genuine computation: weak-admissibility inequalities, strata labels,
flag-dimension formulas, and finite incidence relations.
Interface-only: analytic period maps and admissible loci as spaces.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Sequence

from .newton import hodge_newton_decomposition


@dataclass(frozen=True)
class PeriodDatum:
    hodge_tate_weights: tuple[int, ...]
    newton_slopes: tuple[Fraction, ...]

    @classmethod
    def create(
        cls, hodge_tate_weights: Sequence[int],
        newton_slopes: Sequence[int | Fraction],
    ) -> "PeriodDatum":
        return cls(
            tuple(sorted(hodge_tate_weights)),
            tuple(sorted(Fraction(value) for value in newton_slopes)),
        )

    @property
    def weakly_admissible(self) -> bool:
        return hodge_newton_decomposition(
            self.newton_slopes, self.hodge_tate_weights
        ).admissible

    @property
    def stratum_label(self) -> str:
        slopes = ",".join(map(str, self.newton_slopes))
        weights = ",".join(map(str, self.hodge_tate_weights))
        return f"HT[{weights}]::N[{slopes}]"

    def flag_dimension(self) -> int:
        weights = self.hodge_tate_weights
        return sum(1 for i in range(len(weights)) for j in range(i + 1, len(weights))
                   if weights[i] != weights[j])
