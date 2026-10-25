# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""Finite delta-rings, prisms, and Frobenius windows.

Treatise correspondence: see Appendix G of the book (The Reference Implementation).
Genuine computation: delta identity checks modulo p^N, Frobenius lifts,
finite matrix windows, determinant bounds, and precision metadata.
Interface-only: geometric prismatic cohomology and descent between all prisms.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Sequence

from aletheia.numerics.linalg import determinant


@dataclass(frozen=True)
class TruncatedDeltaRing:
    prime: int
    precision: int
    delta: Callable[[int], int]

    @property
    def modulus(self) -> int:
        return self.prime ** self.precision

    def normalize(self, value: int) -> int:
        return value % self.modulus

    def frobenius(self, value: int) -> int:
        return self.normalize(value ** self.prime + self.prime * self.delta(value))

    def verify_samples(self, samples: Sequence[int]) -> bool:
        p, modulus = self.prime, self.modulus
        for x in samples:
            if (self.frobenius(x) - x ** p) % p:
                return False
            for y in samples:
                if self.frobenius(x + y) != (
                    self.frobenius(x) + self.frobenius(y)
                ) % modulus:
                    return False
                if self.frobenius(x * y) != (
                    self.frobenius(x) * self.frobenius(y)
                ) % modulus:
                    return False
        return True


@dataclass(frozen=True)
class BoundedPrism:
    ring: TruncatedDeltaRing
    distinguished: int
    ideal_power: int

    def is_distinguished(self) -> bool:
        return self.ring.delta(self.distinguished) % self.ring.prime != 0

    def quotient_modulus(self) -> tuple[int, int]:
        return self.ring.modulus, self.distinguished ** self.ideal_power


@dataclass(frozen=True)
class PrismaticWindow:
    prism: BoundedPrism
    frobenius_matrix: tuple[tuple[int, ...], ...]
    hodge_weights: tuple[int, ...]
    precision_loss: int = 0

    @property
    def rank(self) -> int:
        return len(self.frobenius_matrix)

    def determinant(self) -> int:
        return int(determinant(self.frobenius_matrix))

    def invertible_after_inverting_ideal(self) -> bool:
        return self.determinant() != 0

    def verify(self) -> bool:
        return (
            self.prism.is_distinguished()
            and all(len(row) == self.rank for row in self.frobenius_matrix)
            and len(self.hodge_weights) == self.rank
            and self.precision_loss < self.prism.ring.precision
        )
