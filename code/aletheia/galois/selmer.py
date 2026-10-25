# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""Selmer structures and finite Poitou–Tate arithmetic.

Treatise correspondence: see Appendix G of the book (The Reference Implementation).
Genuine computation: dimensions of kernels from restriction matrices,
dual Selmer balances, and finite exact-sequence checks.
Interface-only: arithmetic local conditions must be supplied as finite maps.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

from aletheia.numerics.linalg import kernel_mod_p, rref_mod_p


@dataclass(frozen=True)
class LocalCondition:
    place: str
    ambient_dimension: int
    allowed_basis: tuple[tuple[int, ...], ...]
    description: str = "finite local condition"

    @property
    def dimension(self) -> int:
        return len(self.allowed_basis)


@dataclass(frozen=True)
class SelmerProblem:
    prime: int
    global_h1_dimension: int
    restriction_matrix: tuple[tuple[int, ...], ...]
    local_quotient_dimension: int
    local_conditions: tuple[LocalCondition, ...] = ()

    def selmer_basis(self) -> tuple[tuple[int, ...], ...]:
        return tuple(
            tuple(vector)
            for vector in kernel_mod_p(self.restriction_matrix, self.prime)
        )

    @property
    def selmer_dimension(self) -> int:
        return len(self.selmer_basis())

    @property
    def restriction_rank(self) -> int:
        return len(rref_mod_p(self.restriction_matrix, self.prime)[1])

    def verifies_rank_nullity(self) -> bool:
        return (
            self.selmer_dimension + self.restriction_rank
            == self.global_h1_dimension
        )


@dataclass(frozen=True)
class PoitouTateBalance:
    selmer_dimension: int
    dual_selmer_dimension: int
    h0_difference: int
    local_euler_correction: int

    @property
    def defect(self) -> int:
        return (
            self.selmer_dimension - self.dual_selmer_dimension
            - self.h0_difference - self.local_euler_correction
        )

    @property
    def balanced(self) -> bool:
        return self.defect == 0


def poisson_tate_balance(
    selmer_dimension: int,
    dual_selmer_dimension: int,
    h0_difference: int,
    local_euler_correction: int,
) -> PoitouTateBalance:
    return PoitouTateBalance(
        selmer_dimension, dual_selmer_dimension,
        h0_difference, local_euler_correction,
    )
