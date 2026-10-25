# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""Finite Hecke algebras and commuting eigensystems.

Treatise correspondence: see Appendix G of the book (The Reference Implementation).
Genuine computation: exact matrix commutators, generated-word action,
common eigenvectors over F_p, and packet records.
Interface-only: correspondence matrices must come from a certified complex.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from itertools import product
from typing import Mapping, Sequence

from aletheia.numerics.linalg import kernel_mod_p


def matmul_mod(
    left: Sequence[Sequence[int]], right: Sequence[Sequence[int]], prime: int
) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple(
        sum(left[i][k] * right[k][j] for k in range(len(right))) % prime
        for j in range(len(right[0]))
    ) for i in range(len(left)))


def matrix_sub_mod(
    left: Sequence[Sequence[int]], right: Sequence[Sequence[int]], prime: int
) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple((a - b) % prime for a, b in zip(x, y))
                 for x, y in zip(left, right))


@dataclass(frozen=True)
class HeckeOperator:
    label: str
    matrix: tuple[tuple[int, ...], ...]
    prime: int

    @property
    def dimension(self) -> int:
        return len(self.matrix)

    def apply(self, vector: Sequence[int]) -> tuple[int, ...]:
        return tuple(
            sum(row[j] * vector[j] for j in range(len(vector))) % self.prime
            for row in self.matrix
        )

    def commutes_with(self, other: "HeckeOperator") -> bool:
        return matmul_mod(self.matrix, other.matrix, self.prime) == matmul_mod(
            other.matrix, self.matrix, self.prime
        )

    def eigenspace(self, eigenvalue: int) -> tuple[tuple[int, ...], ...]:
        shifted = tuple(tuple(
            (value - (eigenvalue if i == j else 0)) % self.prime
            for j, value in enumerate(row)
        ) for i, row in enumerate(self.matrix))
        return tuple(tuple(vector)
                     for vector in kernel_mod_p(shifted, self.prime))


@dataclass(frozen=True)
class HeckeEigenpacket:
    eigenvalues: Mapping[str, int]
    common_vectors: tuple[tuple[int, ...], ...]
    coefficient_prime: int

    @property
    def multiplicity(self) -> int:
        return len(self.common_vectors)


@dataclass
class FiniteHeckeAlgebra:
    operators: dict[str, HeckeOperator] = field(default_factory=dict)

    def add(self, operator: HeckeOperator) -> None:
        if self.operators and any(
            existing.prime != operator.prime
            or existing.dimension != operator.dimension
            for existing in self.operators.values()
        ):
            raise ValueError("all operators need common field and dimension")
        self.operators[operator.label] = operator

    def is_commutative(self) -> bool:
        values = list(self.operators.values())
        return all(values[i].commutes_with(values[j])
                   for i in range(len(values))
                   for j in range(i + 1, len(values)))

    def eigenpackets(self) -> tuple[HeckeEigenpacket, ...]:
        if not self.operators:
            return ()
        labels = tuple(self.operators)
        prime = next(iter(self.operators.values())).prime
        dimension = next(iter(self.operators.values())).dimension
        packets = []
        for values in product(range(prime), repeat=len(labels)):
            common = []
            for vector in product(range(prime), repeat=dimension):
                if not any(vector):
                    continue
                if all(
                    self.operators[label].apply(vector)
                    == tuple(value * x % prime for x in vector)
                    for label, value in zip(labels, values)
                ):
                    common.append(tuple(vector))
            if common:
                packets.append(HeckeEigenpacket(
                    dict(zip(labels, values)), tuple(common), prime
                ))
        return tuple(packets)
