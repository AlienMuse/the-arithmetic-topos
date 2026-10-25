# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""Satake parameters and spherical Hecke data for GL_n.

Treatise correspondence: see Appendix G of the book (The Reference Implementation).
Genuine computation: elementary-symmetric conversion, Euler polynomials,
normalized/unnormalized scaling, and inverse root recovery for n <= 2.
Interface-only: general reductive Satake is represented by finite orbit data.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations
import cmath
from typing import Iterable, Sequence

Scalar = complex | float | int | Fraction


def elementary_symmetric(values: Sequence[Scalar]) -> tuple[complex, ...]:
    output: list[complex] = []
    converted = [complex(value) for value in values]
    for degree in range(1, len(converted) + 1):
        output.append(sum(
            (complex_product(choice) for choice in combinations(converted, degree)),
            0j,
        ))
    return tuple(output)


def complex_product(values: Iterable[complex]) -> complex:
    result = 1 + 0j
    for value in values:
        result *= value
    return result


def polynomial_from_roots(roots: Sequence[Scalar]) -> tuple[complex, ...]:
    coefficients = [1 + 0j]
    for root in roots:
        updated = [0j] * (len(coefficients) + 1)
        for index, coefficient in enumerate(coefficients):
            updated[index] += coefficient
            updated[index + 1] -= coefficient * complex(root)
        coefficients = updated
    return tuple(coefficients)


def roots_quadratic(coefficients: Sequence[Scalar]) -> tuple[complex, complex]:
    if len(coefficients) != 3 or complex(coefficients[0]) == 0:
        raise ValueError("quadratic coefficients must be (a,b,c) with a != 0")
    a, b, c = map(complex, coefficients)
    discriminant = cmath.sqrt(b * b - 4 * a * c)
    return ((-b + discriminant) / (2 * a), (-b - discriminant) / (2 * a))


@dataclass(frozen=True)
class SatakeParameter:
    """An unordered semisimple conjugacy class for unramified GL_n."""

    eigenvalues: tuple[complex, ...]
    residue_cardinality: int
    normalized: bool = True
    place: str | None = None

    def __post_init__(self) -> None:
        if not self.eigenvalues:
            raise ValueError("a Satake parameter has positive rank")
        if self.residue_cardinality < 2:
            raise ValueError("residue cardinality must be at least 2")

    @property
    def rank(self) -> int:
        return len(self.eigenvalues)

    def hecke_eigenvalues(self) -> tuple[complex, ...]:
        return elementary_symmetric(self.eigenvalues)

    def standard_euler_polynomial(self) -> tuple[complex, ...]:
        return polynomial_from_roots(self.eigenvalues)

    def local_factor(self, s: complex) -> complex:
        q_power = self.residue_cardinality ** (-s)
        denominator = complex_product(
            1 - alpha * q_power for alpha in self.eigenvalues
        )
        return 1 / denominator

    def central_character(self) -> complex:
        return complex_product(self.eigenvalues)

    def unnormalized(self) -> "SatakeParameter":
        if not self.normalized:
            return self
        exponent_shift = (self.rank - 1) / 2
        scale = self.residue_cardinality ** exponent_shift
        return SatakeParameter(
            tuple(alpha * scale for alpha in self.eigenvalues),
            self.residue_cardinality,
            False,
            self.place,
        )

    def unitary_bound_error(self) -> float:
        return max(abs(abs(alpha) - 1.0) for alpha in self.eigenvalues)


def satake_from_hecke_gl2(
    trace_eigenvalue: Scalar,
    determinant_eigenvalue: Scalar,
    residue_cardinality: int,
    *,
    normalized: bool = True,
) -> SatakeParameter:
    roots = roots_quadratic((1, -complex(trace_eigenvalue),
                             complex(determinant_eigenvalue)))
    return SatakeParameter(roots, residue_cardinality, normalized)


def satake_from_hecke(
    hecke_eigenvalues: Sequence[Scalar],
    residue_cardinality: int,
    *,
    normalized: bool = True,
) -> SatakeParameter:
    rank = len(hecke_eigenvalues)
    if rank == 1:
        roots = (complex(hecke_eigenvalues[0]),)
    elif rank == 2:
        roots = roots_quadratic(
            (1, -complex(hecke_eigenvalues[0]), complex(hecke_eigenvalues[1]))
        )
    else:
        raise NotImplementedError(
            "pure-Python root recovery is implemented for GL_1 and GL_2; "
            "higher GL_n parameters can be constructed from eigenvalues directly"
        )
    return SatakeParameter(roots, residue_cardinality, normalized)


def hecke_from_satake(parameter: SatakeParameter) -> tuple[complex, ...]:
    return parameter.hecke_eigenvalues()


@dataclass(frozen=True)
class SatakeTransformTerm:
    coweight: tuple[int, ...]
    coefficient: Fraction


@dataclass(frozen=True)
class FiniteSatakeTransform:
    """A sparse toy transform with explicit support and normalization."""

    terms: tuple[SatakeTransformTerm, ...]
    residue_cardinality: int
    normalization: str

    def evaluate(self, torus_point: Sequence[Scalar]) -> complex:
        total = 0j
        for term in self.terms:
            monomial = 1 + 0j
            for coordinate, exponent in zip(torus_point, term.coweight):
                monomial *= complex(coordinate) ** exponent
            total += float(term.coefficient) * monomial
        return total

    def support(self) -> tuple[tuple[int, ...], ...]:
        return tuple(term.coweight for term in self.terms)
