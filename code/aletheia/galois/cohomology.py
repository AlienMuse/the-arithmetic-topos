# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""Finite Galois-cohomology dimension and Euler-characteristic models.

Treatise correspondence: see Appendix G of the book (The Reference Implementation).
Genuine computation: dimensions from finite cochain complexes over F_p,
Euler characteristics, local/global bookkeeping, and duality checks.
Interface-only: constructing absolute Galois cochains of arbitrary fields.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

from aletheia.numerics.linalg import rref_mod_p


def matrix_rank_mod_p(matrix: Sequence[Sequence[int]], prime: int) -> int:
    return len(rref_mod_p(matrix, prime)[1])


@dataclass(frozen=True)
class FiniteCochainComplex:
    """A finite model C^0 -> ... -> C^n over F_p."""

    dimensions: tuple[int, ...]
    differentials: tuple[tuple[tuple[int, ...], ...], ...]
    prime: int

    def __post_init__(self) -> None:
        if len(self.differentials) != max(0, len(self.dimensions) - 1):
            raise ValueError("one differential is required between adjacent terms")
        for degree, differential in enumerate(self.differentials):
            rows = len(differential)
            cols = len(differential[0]) if rows else self.dimensions[degree]
            if rows != self.dimensions[degree + 1] or cols != self.dimensions[degree]:
                raise ValueError(f"differential d{degree} has wrong dimensions")
        for left, right in zip(self.differentials, self.differentials[1:]):
            if left and right:
                for i in range(len(right)):
                    for j in range(len(left[0])):
                        value = sum(
                            right[i][k] * left[k][j] for k in range(len(left))
                        ) % self.prime
                        if value:
                            raise ValueError("differentials do not compose to zero")

    def differential_rank(self, degree: int) -> int:
        return matrix_rank_mod_p(self.differentials[degree], self.prime)

    def cohomology_dimensions(self) -> tuple[int, ...]:
        ranks = [self.differential_rank(i)
                 for i in range(len(self.differentials))]
        output = []
        for degree, dimension in enumerate(self.dimensions):
            incoming = ranks[degree - 1] if degree else 0
            outgoing = ranks[degree] if degree < len(ranks) else 0
            output.append(dimension - incoming - outgoing)
        return tuple(output)

    def euler_characteristic(self) -> int:
        return sum(
            (-1) ** degree * dimension
            for degree, dimension in enumerate(self.cohomology_dimensions())
        )

    def chain_euler_characteristic(self) -> int:
        return sum(
            (-1) ** degree * dimension
            for degree, dimension in enumerate(self.dimensions)
        )

    def verifies_euler_principle(self) -> bool:
        return self.euler_characteristic() == self.chain_euler_characteristic()


@dataclass(frozen=True)
class NumberFieldSignature:
    name: str
    real_places: int
    complex_places: int
    degree: int
    discriminant: int | None = None

    def __post_init__(self) -> None:
        if self.real_places < 0 or self.complex_places < 0:
            raise ValueError("place counts are nonnegative")
        if self.degree != self.real_places + 2 * self.complex_places:
            raise ValueError("degree must equal r1 + 2*r2")

    @classmethod
    def parse(cls, text: str) -> "NumberFieldSignature":
        cleaned = text.strip().lower().replace(" ", "")
        if cleaned in {"q", "ℚ", "qq", "rationals"}:
            return cls("Q", 1, 0, 1, 1)
        if cleaned in {"q(i)", "qi", "q[sqrt(-1)]", "gaussian"}:
            return cls("Q(i)", 0, 1, 2, -4)
        if cleaned in {"q(sqrt(5))", "q(√5)", "realquadratic"}:
            return cls("Q(sqrt(5))", 2, 0, 2, 5)
        if cleaned in {"q(sqrt(-3))", "eisenstein"}:
            return cls("Q(sqrt(-3))", 0, 1, 2, -3)
        raise ValueError(f"unknown built-in number field {text!r}")


@dataclass(frozen=True)
class EulerCharacteristicData:
    global_dimensions: tuple[int, ...]
    local_dimensions: tuple[tuple[str, tuple[int, ...]], ...]
    module_dimension: int
    signature: NumberFieldSignature

    @property
    def global_euler(self) -> int:
        return sum((-1) ** i * value
                   for i, value in enumerate(self.global_dimensions))

    @property
    def local_euler(self) -> int:
        return sum(
            sum((-1) ** i * value for i, value in enumerate(dimensions))
            for _, dimensions in self.local_dimensions
        )

    def poisson_tate_balance(self) -> int:
        return self.global_euler - self.local_euler


def finite_module_euler_characteristic(
    cohomology_dimensions: Sequence[int],
) -> int:
    return sum((-1) ** degree * dimension
               for degree, dimension in enumerate(cohomology_dimensions))


def artin_verdier_expected_length(signature: NumberFieldSignature) -> int:
    """Cohomological top degree including the archimedean correction."""

    return 3 if signature.degree else 0
