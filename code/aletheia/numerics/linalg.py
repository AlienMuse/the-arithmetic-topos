# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""Exact linear algebra over Q, F_p, and Z.

Treatise correspondence: see Appendix G of the book (The Reference Implementation).
Genuine computation: RREF, rank, kernels, determinants, and Smith invariant
factors. Interface-only: high-performance sparse and multimodular backends.
"""
from __future__ import annotations

from fractions import Fraction
from functools import reduce
from itertools import combinations
from math import gcd
from typing import Iterable, Sequence, TypeVar

Number = TypeVar("Number", int, Fraction)
Matrix = list[list[Fraction]]


def _rectangular(matrix: Sequence[Sequence[object]]) -> tuple[int, int]:
    rows = len(matrix)
    cols = len(matrix[0]) if rows else 0
    if any(len(row) != cols for row in matrix):
        raise ValueError("matrix must be rectangular")
    return rows, cols


def as_fraction_matrix(matrix: Sequence[Sequence[int | Fraction]]) -> Matrix:
    _rectangular(matrix)
    return [[Fraction(value) for value in row] for row in matrix]


def identity(size: int) -> Matrix:
    if size < 0:
        raise ValueError("size must be nonnegative")
    return [
        [Fraction(int(i == j)) for j in range(size)]
        for i in range(size)
    ]


def transpose(matrix: Sequence[Sequence[Number]]) -> list[list[Number]]:
    rows, cols = _rectangular(matrix)
    return [[matrix[i][j] for i in range(rows)] for j in range(cols)]


def matmul(
    left: Sequence[Sequence[int | Fraction]],
    right: Sequence[Sequence[int | Fraction]],
) -> Matrix:
    lr, lc = _rectangular(left)
    rr, rc = _rectangular(right)
    if lc != rr:
        raise ValueError("incompatible matrix dimensions")
    return [
        [
            sum(
                (Fraction(left[i][k]) * Fraction(right[k][j])
                 for k in range(lc)),
                Fraction(0),
            )
            for j in range(rc)
        ]
        for i in range(lr)
    ]


def rref(
    matrix: Sequence[Sequence[int | Fraction]],
) -> tuple[Matrix, tuple[int, ...]]:
    result = as_fraction_matrix(matrix)
    rows, cols = _rectangular(result)
    pivot_columns: list[int] = []
    pivot_row = 0
    for column in range(cols):
        selected = next(
            (row for row in range(pivot_row, rows) if result[row][column]),
            None,
        )
        if selected is None:
            continue
        result[pivot_row], result[selected] = result[selected], result[pivot_row]
        pivot = result[pivot_row][column]
        result[pivot_row] = [value / pivot for value in result[pivot_row]]
        for row in range(rows):
            if row == pivot_row:
                continue
            factor = result[row][column]
            if factor:
                result[row] = [
                    value - factor * pivot_value
                    for value, pivot_value in zip(result[row], result[pivot_row])
                ]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == rows:
            break
    return result, tuple(pivot_columns)


def rank(matrix: Sequence[Sequence[int | Fraction]]) -> int:
    return len(rref(matrix)[1])


def kernel(matrix: Sequence[Sequence[int | Fraction]]) -> Matrix:
    reduced, pivots = rref(matrix)
    _, columns = _rectangular(reduced)
    free = [column for column in range(columns) if column not in pivots]
    basis: Matrix = []
    for free_column in free:
        vector = [Fraction(0) for _ in range(columns)]
        vector[free_column] = Fraction(1)
        for row, pivot_column in enumerate(pivots):
            vector[pivot_column] = -reduced[row][free_column]
        basis.append(vector)
    return basis


def determinant(matrix: Sequence[Sequence[int | Fraction]]) -> Fraction:
    rows, cols = _rectangular(matrix)
    if rows != cols:
        raise ValueError("determinant requires a square matrix")
    work = as_fraction_matrix(matrix)
    sign = 1
    output = Fraction(1)
    for column in range(cols):
        selected = next(
            (row for row in range(column, rows) if work[row][column]), None
        )
        if selected is None:
            return Fraction(0)
        if selected != column:
            work[column], work[selected] = work[selected], work[column]
            sign *= -1
        pivot = work[column][column]
        output *= pivot
        for row in range(column + 1, rows):
            factor = work[row][column] / pivot
            for j in range(column + 1, cols):
                work[row][j] -= factor * work[column][j]
    return sign * output


def inverse(matrix: Sequence[Sequence[int | Fraction]]) -> Matrix:
    rows, cols = _rectangular(matrix)
    if rows != cols:
        raise ValueError("inverse requires a square matrix")
    augmented = [
        [*map(Fraction, row), *identity(rows)[index]]
        for index, row in enumerate(matrix)
    ]
    reduced, pivots = rref(augmented)
    if tuple(range(rows)) != pivots[:rows]:
        raise ValueError("matrix is singular")
    return [row[cols:] for row in reduced]


def solve(
    matrix: Sequence[Sequence[int | Fraction]],
    vector: Sequence[int | Fraction],
) -> list[Fraction]:
    rows, cols = _rectangular(matrix)
    if len(vector) != rows:
        raise ValueError("right-hand side has wrong dimension")
    augmented = [
        [*map(Fraction, row), Fraction(vector[index])]
        for index, row in enumerate(matrix)
    ]
    reduced, pivots = rref(augmented)
    if cols in pivots:
        raise ValueError("linear system is inconsistent")
    if len([p for p in pivots if p < cols]) != cols:
        raise ValueError("linear system does not have a unique solution")
    return [reduced[i][-1] for i in range(cols)]


def _inv_mod(value: int, prime: int) -> int:
    value %= prime
    if gcd(value, prime) != 1:
        raise ZeroDivisionError(f"{value} is not invertible modulo {prime}")
    return pow(value, -1, prime)


def rref_mod_p(
    matrix: Sequence[Sequence[int]], prime: int
) -> tuple[list[list[int]], tuple[int, ...]]:
    if prime < 2:
        raise ValueError("modulus must be prime")
    rows, cols = _rectangular(matrix)
    result = [[value % prime for value in row] for row in matrix]
    pivots: list[int] = []
    pivot_row = 0
    for column in range(cols):
        selected = next(
            (row for row in range(pivot_row, rows)
             if result[row][column] % prime),
            None,
        )
        if selected is None:
            continue
        result[pivot_row], result[selected] = result[selected], result[pivot_row]
        scalar = _inv_mod(result[pivot_row][column], prime)
        result[pivot_row] = [(value * scalar) % prime
                             for value in result[pivot_row]]
        for row in range(rows):
            if row == pivot_row:
                continue
            factor = result[row][column]
            result[row] = [
                (value - factor * pivot) % prime
                for value, pivot in zip(result[row], result[pivot_row])
            ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == rows:
            break
    return result, tuple(pivots)


def kernel_mod_p(matrix: Sequence[Sequence[int]], prime: int) -> list[list[int]]:
    reduced, pivots = rref_mod_p(matrix, prime)
    _, columns = _rectangular(reduced)
    free = [column for column in range(columns) if column not in pivots]
    basis: list[list[int]] = []
    for column in free:
        vector = [0] * columns
        vector[column] = 1
        for row, pivot in enumerate(pivots):
            vector[pivot] = (-reduced[row][column]) % prime
        basis.append(vector)
    return basis


def _minor_gcd(matrix: Sequence[Sequence[int]], size: int) -> int:
    rows, cols = _rectangular(matrix)
    values: list[int] = []
    for row_set in combinations(range(rows), size):
        for col_set in combinations(range(cols), size):
            minor = [[matrix[i][j] for j in col_set] for i in row_set]
            values.append(abs(int(determinant(minor))))
    return reduce(gcd, values, 0)


def smith_normal_form(matrix: Sequence[Sequence[int]]) -> list[list[int]]:
    """Return the diagonal Smith normal form.

    Determinantal divisors are used rather than fragile row-operation
    heuristics.  This is exact and excellent for certificate-sized matrices,
    but exponential in the matrix dimensions.
    """

    rows, cols = _rectangular(matrix)
    maximum_rank = min(rows, cols)
    divisors = [1]
    for size in range(1, maximum_rank + 1):
        divisor = _minor_gcd(matrix, size)
        if divisor == 0:
            break
        divisors.append(divisor)
    invariants = [
        divisors[index] // divisors[index - 1]
        for index in range(1, len(divisors))
    ]
    output = [[0 for _ in range(cols)] for _ in range(rows)]
    for index, value in enumerate(invariants):
        output[index][index] = abs(value)
    return output


def smith_invariants(matrix: Sequence[Sequence[int]]) -> tuple[int, ...]:
    normal = smith_normal_form(matrix)
    return tuple(
        normal[i][i]
        for i in range(min(len(normal), len(normal[0]) if normal else 0))
        if normal[i][i]
    )


def characteristic_polynomial_2x2(
    matrix: Sequence[Sequence[int | Fraction]],
) -> tuple[Fraction, Fraction, Fraction]:
    rows, cols = _rectangular(matrix)
    if (rows, cols) != (2, 2):
        raise ValueError("this small exact routine requires a 2x2 matrix")
    trace = Fraction(matrix[0][0]) + Fraction(matrix[1][1])
    det = determinant(matrix)
    return Fraction(1), -trace, det
