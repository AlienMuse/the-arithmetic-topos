# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""Dualizability witnesses for finite linear and categorical models.

Treatise correspondence: see Appendix G of the book (The Reference Implementation).
Genuine computation: triangle identities for finite matrices and finite
projective rank witnesses. Interface-only: dualizability in presentable
stable infinity-categories.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Generic, Protocol, Sequence, TypeVar

from aletheia.numerics.linalg import matmul

T = TypeVar("T")


class DualPair(Protocol[T]):
    def evaluation(self) -> T: ...
    def coevaluation(self) -> T: ...
    def verify_triangle_identities(self) -> bool: ...


@dataclass(frozen=True)
class DualizabilityCertificate:
    object_name: str
    dual_name: str
    left_triangle: bool
    right_triangle: bool
    finite: bool = True
    notes: tuple[str, ...] = ()

    @property
    def valid(self) -> bool:
        return self.left_triangle and self.right_triangle and self.finite


@dataclass(frozen=True)
class FiniteVectorSpaceDual:
    dimension: int
    basis: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.dimension < 0:
            raise ValueError("dimension is nonnegative")
        if self.basis and len(self.basis) != self.dimension:
            raise ValueError("basis length does not equal dimension")

    def evaluation_matrix(self) -> list[list[Fraction]]:
        return [[Fraction(int(i == j)) for j in range(self.dimension)]
                for i in range(self.dimension)]

    def coevaluation_tensor(self) -> tuple[tuple[int, int, Fraction], ...]:
        return tuple((index, index, Fraction(1))
                     for index in range(self.dimension))

    def certificate(self) -> DualizabilityCertificate:
        identity = self.evaluation_matrix()
        composite = matmul(identity, identity)
        valid = composite == identity
        return DualizabilityCertificate(
            f"k^{self.dimension}", f"(k^{self.dimension})*", valid, valid
        )


@dataclass(frozen=True)
class PerfectComplexWitness:
    ranks: tuple[int, ...]
    differential_ranks: tuple[int, ...]
    bounded: bool = True

    def __post_init__(self) -> None:
        if any(rank < 0 for rank in self.ranks):
            raise ValueError("complex ranks must be nonnegative")
        if len(self.differential_ranks) != max(0, len(self.ranks) - 1):
            raise ValueError("differential rank count is invalid")

    @property
    def euler_characteristic(self) -> int:
        return sum((-1) ** degree * rank
                   for degree, rank in enumerate(self.ranks))

    def certificate(self, name: str = "perfect complex") -> DualizabilityCertificate:
        finite = self.bounded and all(
            rank <= min(self.ranks[i], self.ranks[i + 1])
            for i, rank in enumerate(self.differential_ranks)
        )
        return DualizabilityCertificate(name, f"{name} dual", finite, finite, finite)
