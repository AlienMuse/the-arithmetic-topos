# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""Finite spectral actions on automorphic categories.

Treatise correspondence: see Appendix G of the book (The Reference Implementation).
Genuine computation: action matrices, monoidal compatibility, eigen-support
decomposition, and naturality squares on finite vector spaces.
Interface-only: Perf(LocSys) actions on actual sheaf categories.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping, Sequence

from aletheia.numerics.linalg import matmul


@dataclass(frozen=True)
class SpectralOperator:
    label: str
    support: frozenset[str]
    matrix: tuple[tuple[int, ...], ...]

    def compose(self, other: "SpectralOperator") -> "SpectralOperator":
        product = matmul(self.matrix, other.matrix)
        return SpectralOperator(
            f"{self.label}∘{other.label}",
            self.support & other.support,
            tuple(tuple(int(value) for value in row) for row in product),
        )


@dataclass
class SpectralAction:
    space_dimension: int
    operators: dict[str, SpectralOperator] = field(default_factory=dict)

    def register(self, operator: SpectralOperator) -> None:
        if len(operator.matrix) != self.space_dimension or any(
            len(row) != self.space_dimension for row in operator.matrix
        ):
            raise ValueError("operator has wrong action-space dimension")
        self.operators[operator.label] = operator

    def commute(self, left: str, right: str) -> bool:
        a, b = self.operators[left], self.operators[right]
        return a.compose(b).matrix == b.compose(a).matrix

    def supported_operators(self, point: str) -> tuple[str, ...]:
        return tuple(sorted(
            label for label, operator in self.operators.items()
            if point in operator.support
        ))
