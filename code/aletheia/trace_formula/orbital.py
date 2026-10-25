# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""Finite/local models of orbital integrals.

Treatise correspondence: see Appendix G of the book (The Reference Implementation).
Genuine computation: conjugacy orbits in finite matrix groups, weighted cell
sums, discriminant bookkeeping, and explicit tail intervals.
Interface-only: arbitrary p-adic orbital integrals and motivic integration.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Callable, Iterable, Sequence


Matrix = tuple[tuple[int, ...], ...]


def matmul_mod(left: Matrix, right: Matrix, modulus: int) -> Matrix:
    return tuple(tuple(
        sum(left[i][k] * right[k][j] for k in range(len(right))) % modulus
        for j in range(len(right[0]))
    ) for i in range(len(left)))


def inverse_2x2_mod(matrix: Matrix, prime: int) -> Matrix:
    a, b = matrix[0]
    c, d = matrix[1]
    det = (a * d - b * c) % prime
    inv = pow(det, -1, prime)
    return ((d * inv % prime, -b * inv % prime),
            (-c * inv % prime, a * inv % prime))


def conjugate_2x2(matrix: Matrix, by: Matrix, prime: int) -> Matrix:
    return matmul_mod(matmul_mod(inverse_2x2_mod(by, prime), matrix, prime), by, prime)


@dataclass(frozen=True)
class OrbitalCell:
    representative: Matrix
    volume: Fraction
    function_value: Fraction
    certified: bool = True


@dataclass(frozen=True)
class OrbitalIntegralResult:
    value: Fraction
    tail_bound: Fraction
    cells: tuple[OrbitalCell, ...]
    discriminant: int | None = None

    @property
    def interval(self) -> tuple[Fraction, Fraction]:
        return self.value - self.tail_bound, self.value + self.tail_bound

    @property
    def exact(self) -> bool:
        return self.tail_bound == 0 and all(cell.certified for cell in self.cells)


def orbital_integral_cells(
    cells: Iterable[OrbitalCell], tail_bound: Fraction = Fraction(0),
    discriminant: int | None = None,
) -> OrbitalIntegralResult:
    cells_tuple = tuple(cells)
    value = sum(
        (cell.volume * cell.function_value for cell in cells_tuple), Fraction(0)
    )
    return OrbitalIntegralResult(value, tail_bound, cells_tuple, discriminant)


def conjugacy_orbit_gl2(matrix: Matrix, prime: int) -> tuple[Matrix, ...]:
    group = []
    for a in range(prime):
        for b in range(prime):
            for c in range(prime):
                for d in range(prime):
                    if (a * d - b * c) % prime:
                        group.append(((a, b), (c, d)))
    return tuple(sorted({conjugate_2x2(matrix, element, prime) for element in group}))
