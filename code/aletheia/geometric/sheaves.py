# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""Constructible and ind-coherent sheaf bookkeeping.

Treatise correspondence: see Appendix G of the book (The Reference Implementation).
Genuine computation: finite support conditions, shifts, cones, Euler
characteristics, and singular-support inclusion tests.
Interface-only: actual sheaf categories and six-functor descent.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Iterable, Mapping


@dataclass(frozen=True)
class SheafObject:
    name: str
    category: str
    cohomology_ranks: Mapping[int, int]
    support: frozenset[str] = frozenset()
    singular_support: frozenset[str] = frozenset()
    compact: bool = False

    @property
    def euler_characteristic(self) -> int:
        return sum((-1) ** degree * rank
                   for degree, rank in self.cohomology_ranks.items())

    def shift(self, amount: int) -> "SheafObject":
        return replace(
            self,
            name=f"{self.name}[{amount}]",
            cohomology_ranks={
                degree - amount: rank
                for degree, rank in self.cohomology_ranks.items()
            },
        )

    def satisfies_singular_support(self, allowed: Iterable[str]) -> bool:
        return self.singular_support <= frozenset(allowed)


def direct_sum(left: SheafObject, right: SheafObject) -> SheafObject:
    degrees = set(left.cohomology_ranks) | set(right.cohomology_ranks)
    return SheafObject(
        f"{left.name}⊕{right.name}",
        left.category if left.category == right.category else "mixed-presentation",
        {degree: left.cohomology_ranks.get(degree, 0)
         + right.cohomology_ranks.get(degree, 0) for degree in degrees},
        left.support | right.support,
        left.singular_support | right.singular_support,
        left.compact and right.compact,
    )


def mapping_cone(
    source: SheafObject, target: SheafObject, map_rank_by_degree: Mapping[int, int]
) -> SheafObject:
    degrees = set(source.cohomology_ranks) | set(target.cohomology_ranks)
    ranks = {}
    for degree in degrees:
        kernel = max(0, source.cohomology_ranks.get(degree, 0)
                     - map_rank_by_degree.get(degree, 0))
        cokernel = max(0, target.cohomology_ranks.get(degree, 0)
                       - map_rank_by_degree.get(degree, 0))
        ranks[degree] = cokernel
        ranks[degree + 1] = ranks.get(degree + 1, 0) + kernel
    return SheafObject(
        f"Cone({source.name}→{target.name})", target.category, ranks,
        source.support | target.support,
        source.singular_support | target.singular_support,
    )
