# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""Lattices, Gram–Schmidt, and a pure-Python LLL implementation.

Treatise correspondence: see Appendix G of the book (The Reference Implementation).
Genuine computation: exact Fraction-based LLL and relation search.
Interface-only: BKZ and high-dimensional optimized lattice reduction.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import floor, gcd
from typing import Iterable, Sequence


def dot(left: Sequence[Fraction], right: Sequence[Fraction]) -> Fraction:
    return sum((a * b for a, b in zip(left, right)), Fraction(0))


def nearest_integer(value: Fraction) -> int:
    lower = floor(value)
    remainder = value - lower
    if remainder == Fraction(1, 2):
        # LLL is not unique at a half-integral Gram--Schmidt coefficient.
        # Ties towards zero give a deterministic, sign-symmetric convention.
        return lower if value > 0 else lower + 1
    return lower if remainder < Fraction(1, 2) else lower + 1


@dataclass(frozen=True)
class LLLResult:
    basis: tuple[tuple[int, ...], ...]
    swaps: int
    size_reductions: int
    delta: Fraction

    def determinant_squared(self) -> Fraction:
        vectors = [[Fraction(x) for x in row] for row in self.basis]
        orthogonal, _ = gram_schmidt(vectors)
        product = Fraction(1)
        for vector in orthogonal:
            product *= dot(vector, vector)
        return product


def gram_schmidt(
    basis: Sequence[Sequence[Fraction]],
) -> tuple[list[list[Fraction]], list[list[Fraction]]]:
    if not basis:
        return [], []
    width = len(basis[0])
    if any(len(vector) != width for vector in basis):
        raise ValueError("lattice basis must be rectangular")
    orthogonal: list[list[Fraction]] = []
    coefficients = [
        [Fraction(0) for _ in range(len(basis))]
        for _ in range(len(basis))
    ]
    for index, vector in enumerate(basis):
        current = list(vector)
        for previous in range(index):
            denominator = dot(orthogonal[previous], orthogonal[previous])
            if denominator == 0:
                raise ValueError("basis vectors must be linearly independent")
            mu = dot(list(vector), orthogonal[previous]) / denominator
            coefficients[index][previous] = mu
            current = [
                value - mu * old
                for value, old in zip(current, orthogonal[previous])
            ]
        orthogonal.append(current)
    return orthogonal, coefficients


def lll_reduce(
    basis: Sequence[Sequence[int]],
    delta: Fraction = Fraction(3, 4),
) -> LLLResult:
    if not Fraction(1, 4) < delta < 1:
        raise ValueError("LLL delta must lie strictly between 1/4 and 1")
    if not basis:
        return LLLResult((), 0, 0, delta)
    width = len(basis[0])
    if any(len(vector) != width for vector in basis):
        raise ValueError("basis must be rectangular")
    work = [list(map(int, vector)) for vector in basis]
    swaps = reductions = 0
    k = 1
    while k < len(work):
        orthogonal, mu = gram_schmidt(
            [[Fraction(x) for x in row] for row in work]
        )
        for j in range(k - 1, -1, -1):
            quotient = nearest_integer(mu[k][j])
            if quotient:
                work[k] = [
                    value - quotient * base
                    for value, base in zip(work[k], work[j])
                ]
                reductions += 1
                orthogonal, mu = gram_schmidt(
                    [[Fraction(x) for x in row] for row in work]
                )
        left = dot(orthogonal[k], orthogonal[k])
        right = (delta - mu[k][k - 1] ** 2) * dot(
            orthogonal[k - 1], orthogonal[k - 1]
        )
        if left >= right:
            k += 1
        else:
            work[k], work[k - 1] = work[k - 1], work[k]
            swaps += 1
            k = max(k - 1, 1)
    return LLLResult(tuple(tuple(row) for row in work), swaps, reductions, delta)


def hadamard_bound_squared(basis: Sequence[Sequence[int]]) -> int:
    product = 1
    for vector in basis:
        product *= sum(value * value for value in vector)
    return product


def primitive(vector: Sequence[int]) -> tuple[int, ...]:
    common = 0
    for value in vector:
        common = gcd(common, abs(value))
    common = common or 1
    result = tuple(value // common for value in vector)
    first = next((value for value in result if value), 1)
    return tuple(-value for value in result) if first < 0 else result


def integer_relation(values: Sequence[float], scale: int = 10**8) -> tuple[int, ...]:
    """Find a small candidate relation using the standard embedding trick."""

    if len(values) < 2:
        raise ValueError("at least two values are needed")
    basis: list[list[int]] = []
    for index, value in enumerate(values):
        row = [0] * (len(values) + 1)
        row[index] = 1
        row[-1] = round(scale * value)
        basis.append(row)
    reduced = lll_reduce(basis).basis
    candidate = min(reduced, key=lambda row: abs(row[-1]))
    return primitive(candidate[:-1])
