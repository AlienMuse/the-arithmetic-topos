# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""Finite shtuka legs and excursion-operator matrices.

Treatise correspondence: see Appendix G of the book (The Reference Implementation).
Genuine computation: creation-action-annihilation matrix composition,
fusion checks, and finite commuting excursion algebras.
Interface-only: geometric shtuka cohomology and number-field excursion theory.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping, Sequence

from aletheia.numerics.linalg import matmul


@dataclass(frozen=True)
class ShtukaLeg:
    label: str
    place: str
    representation: str
    modification_bound: tuple[int, ...] = ()


@dataclass(frozen=True)
class ExcursionDatum:
    legs: tuple[ShtukaLeg, ...]
    galois_elements: tuple[str, ...]
    invariant_function: str

    def __post_init__(self) -> None:
        if len(self.legs) != len(self.galois_elements):
            raise ValueError("one Galois element is required per leg")


@dataclass(frozen=True)
class ExcursionOperator:
    datum: ExcursionDatum
    matrix: tuple[tuple[complex, ...], ...]

    @classmethod
    def assemble(
        cls,
        datum: ExcursionDatum,
        creation: Sequence[Sequence[int]],
        action: Sequence[Sequence[int]],
        annihilation: Sequence[Sequence[int]],
    ) -> "ExcursionOperator":
        first = matmul(action, creation)
        final = matmul(annihilation, first)
        return cls(datum, tuple(tuple(complex(value) for value in row)
                                for row in final))

    def commutes_with(self, other: "ExcursionOperator", tolerance: float = 1e-12) -> bool:
        left = matmul(self.matrix, other.matrix)
        right = matmul(other.matrix, self.matrix)
        return all(
            abs(complex(a) - complex(b)) <= tolerance
            for row_a, row_b in zip(left, right)
            for a, b in zip(row_a, row_b)
        )


@dataclass
class ExcursionAlgebra:
    operators: dict[str, ExcursionOperator] = field(default_factory=dict)

    def add(self, label: str, operator: ExcursionOperator) -> None:
        self.operators[label] = operator

    def is_commutative(self) -> bool:
        values = list(self.operators.values())
        return all(values[i].commutes_with(values[j])
                   for i in range(len(values))
                   for j in range(i + 1, len(values)))
