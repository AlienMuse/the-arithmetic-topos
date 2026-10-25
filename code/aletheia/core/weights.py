# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""Weight structures, weight complexes, and purity bookkeeping.

Treatise correspondence: see Appendix G of the book (The Reference Implementation).
Genuine computation: bounded weight complexes, filtrations, pure graded
pieces, and trace polynomials. Interface-only: existence of motivic weight
structures and purity theorems.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable, Mapping, Sequence


@dataclass(frozen=True)
class WeightedPiece:
    weight: int
    rank: int
    frobenius_eigenvalues: tuple[complex, ...] = ()
    pure: bool | None = None

    def __post_init__(self) -> None:
        if self.rank < 0:
            raise ValueError("rank is nonnegative")
        if self.frobenius_eigenvalues and len(self.frobenius_eigenvalues) != self.rank:
            raise ValueError("eigenvalue count must equal rank")

    def trace(self, power: int = 1) -> complex:
        if not self.frobenius_eigenvalues:
            raise ValueError("no Frobenius eigenvalues were supplied")
        return sum((value ** power for value in self.frobenius_eigenvalues), 0j)

    def purity_error(self, cardinality: int) -> float | None:
        if not self.frobenius_eigenvalues:
            return None
        target = cardinality ** (self.weight / 2)
        return max(abs(abs(value) - target) for value in self.frobenius_eigenvalues)


@dataclass(frozen=True)
class WeightComplex:
    pieces: tuple[WeightedPiece, ...]
    differentials: tuple[int, ...] = ()

    def __post_init__(self) -> None:
        if tuple(sorted(piece.weight for piece in self.pieces)) != tuple(
            piece.weight for piece in self.pieces
        ):
            raise ValueError("pieces must be ordered by weight")
        if self.differentials and len(self.differentials) != len(self.pieces) - 1:
            raise ValueError("differential rank count is invalid")

    @property
    def weight_range(self) -> tuple[int, int] | None:
        if not self.pieces:
            return None
        return self.pieces[0].weight, self.pieces[-1].weight

    @property
    def virtual_rank(self) -> int:
        return sum((-1) ** index * piece.rank
                   for index, piece in enumerate(self.pieces))

    def trace(self, power: int = 1) -> complex:
        return sum(
            (((-1) ** index) * piece.trace(power)
             for index, piece in enumerate(self.pieces)),
            0j,
        )

    def is_pure(self, weight: int | None = None) -> bool:
        nonzero = [piece for piece in self.pieces if piece.rank]
        if not nonzero:
            return True
        target = nonzero[0].weight if weight is None else weight
        return all(piece.weight == target and piece.pure is not False
                   for piece in nonzero)

    def filtration(self) -> dict[int, tuple[WeightedPiece, ...]]:
        return {
            cutoff: tuple(piece for piece in self.pieces if piece.weight <= cutoff)
            for cutoff in sorted({piece.weight for piece in self.pieces})
        }


def weight_polynomial(complex_: WeightComplex) -> dict[int, int]:
    output: dict[int, int] = {}
    for index, piece in enumerate(complex_.pieces):
        output[piece.weight] = (
            output.get(piece.weight, 0) + (-1) ** index * piece.rank
        )
    return output
