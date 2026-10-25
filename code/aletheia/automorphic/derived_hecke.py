# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""Derived Hecke exterior-algebra actions.

Treatise correspondence: see Appendix G of the book (The Reference Implementation).
Genuine computation: exterior basis, wedge signs, contractions, and
graded-dimension checks. Interface-only: arithmetic realization of generators.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Iterable, Sequence


@dataclass(frozen=True)
class ExteriorElement:
    terms: tuple[tuple[tuple[int, ...], int], ...]

    @classmethod
    def basis(cls, indices: Sequence[int], coefficient: int = 1) -> "ExteriorElement":
        if len(set(indices)) != len(indices):
            return cls(())
        inversions = sum(
            indices[i] > indices[j]
            for i in range(len(indices)) for j in range(i + 1, len(indices))
        )
        return cls(((tuple(sorted(indices)), coefficient * (-1) ** inversions),))


@dataclass(frozen=True)
class ExteriorAlgebra:
    generators: tuple[str, ...]

    @property
    def dimension(self) -> int:
        return 2 ** len(self.generators)

    def basis(self, degree: int | None = None) -> tuple[tuple[int, ...], ...]:
        degrees = range(len(self.generators) + 1) if degree is None else (degree,)
        return tuple(
            subset for size in degrees
            for subset in combinations(range(len(self.generators)), size)
        )

    def wedge_basis(
        self, left: Sequence[int], right: Sequence[int]
    ) -> tuple[int, tuple[int, ...]] | None:
        if set(left) & set(right):
            return None
        inversions = sum(a > b for a in left for b in right)
        return (-1) ** inversions, tuple(sorted((*left, *right)))

    def poincare_polynomial(self) -> tuple[int, ...]:
        return tuple(len(self.basis(degree))
                     for degree in range(len(self.generators) + 1))

    def contraction(
        self, generator: int, basis: Sequence[int]
    ) -> tuple[int, tuple[int, ...]] | None:
        if generator not in basis:
            return None
        position = tuple(basis).index(generator)
        return (-1) ** position, tuple(
            value for value in basis if value != generator
        )
