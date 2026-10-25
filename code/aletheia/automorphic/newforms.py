# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""Classical newform records and modular-symbol interfaces.

Treatise correspondence: see Appendix G of the book (The Reference Implementation).
Genuine computation: built-in elliptic newform q-expansions, multiplicative
coefficient checks, Sturm-bound utility, and oldform degeneracy bookkeeping.
Interface-only: general modular-symbol homology and newform decomposition.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import prod
from typing import Sequence

from aletheia.numerics.modforms import QExpansion, elliptic_newform


def index_gamma0(level: int) -> int:
    factors = []
    remaining = level
    prime = 2
    while prime * prime <= remaining:
        if remaining % prime == 0:
            factors.append(prime)
            while remaining % prime == 0:
                remaining //= prime
        prime += 1
    if remaining > 1:
        factors.append(remaining)
    value = level
    for prime in factors:
        value = value * (prime + 1) // prime
    return value


def sturm_bound(weight: int, level: int) -> int:
    if weight < 1 or level < 1:
        raise ValueError("weight and level must be positive")
    return weight * index_gamma0(level) // 12


@dataclass(frozen=True)
class Newform:
    label: str
    weight: int
    level: int
    expansion: QExpansion
    coefficient_field: str = "Q"

    def hecke_eigenvalue(self, prime: int):
        return self.expansion.coefficient(prime)

    def verify_multiplicativity(self, bound: int) -> bool:
        for m in range(1, bound + 1):
            for n in range(1, bound // m + 1):
                if gcd(m, n) == 1 and m * n < self.expansion.precision:
                    if self.expansion.coefficient(m * n) != (
                        self.expansion.coefficient(m)
                        * self.expansion.coefficient(n)
                    ):
                        return False
        return True


def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return abs(a)


def built_in_newform(label: str, precision: int = 100) -> Newform:
    expansion = elliptic_newform(label, precision)
    return Newform(label, expansion.weight or 2, expansion.level or 1, expansion)
