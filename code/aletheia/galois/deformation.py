# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""Derived and truncated Galois-deformation presentations.

Treatise correspondence: see Appendix G of the book (The Reference Implementation).
Genuine computation: tangent/obstruction dimension bookkeeping, truncated
power-series monomials, and relation evaluation over finite fields.
Interface-only: representability and universality require external theorems.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Iterable, Mapping, Sequence

from aletheia.verification.certificate import Certificate


@dataclass(frozen=True)
class DeformationCondition:
    name: str
    tangent_constraints: int = 0
    obstruction_constraints: int = 0
    determinant_fixed: bool = False


@dataclass(frozen=True)
class TangentObstructionData:
    h0: int
    h1: int
    h2: int
    local_conditions: tuple[DeformationCondition, ...] = ()

    @property
    def tangent_dimension(self) -> int:
        return max(0, self.h1 - sum(
            condition.tangent_constraints for condition in self.local_conditions
        ))

    @property
    def obstruction_dimension(self) -> int:
        return max(0, self.h2 - sum(
            condition.obstruction_constraints for condition in self.local_conditions
        ))

    @property
    def virtual_dimension(self) -> int:
        return self.tangent_dimension - self.obstruction_dimension - self.h0


Monomial = tuple[int, ...]
Polynomial = Mapping[Monomial, int]


@dataclass(frozen=True)
class TruncatedDeformationRing:
    prime: int
    variables: tuple[str, ...]
    relations: tuple[Polynomial, ...]
    maximal_ideal_order: int
    p_precision: int
    universal: bool
    hypotheses: tuple[str, ...] = ()

    def monomials(self) -> tuple[Monomial, ...]:
        output = []
        for exponents in product(
            range(self.maximal_ideal_order), repeat=len(self.variables)
        ):
            if sum(exponents) < self.maximal_ideal_order:
                output.append(exponents)
        return tuple(output)

    def evaluate(self, polynomial: Polynomial, point: Sequence[int]) -> int:
        if len(point) != len(self.variables):
            raise ValueError("point dimension does not match variables")
        modulus = self.prime ** self.p_precision
        return sum(
            coefficient * product_power(point, monomial)
            for monomial, coefficient in polynomial.items()
        ) % modulus

    def is_point(self, point: Sequence[int]) -> bool:
        return all(self.evaluate(relation, point) == 0
                   for relation in self.relations)

    def finite_points(self) -> tuple[tuple[int, ...], ...]:
        modulus = self.prime ** self.p_precision
        return tuple(
            point for point in product(range(modulus), repeat=len(self.variables))
            if self.is_point(point)
        )

    def certificate(self) -> Certificate[dict[str, object]]:
        payload = {
            "prime": self.prime,
            "variables": self.variables,
            "relations": self.relations,
            "orders": (self.maximal_ideal_order, self.p_precision),
            "universal": self.universal,
        }
        return Certificate.issue(
            "deformation-presentation",
            "finite truncated relation presentation",
            payload,
            "aletheia.galois.deformation",
        )


def product_power(point: Sequence[int], exponents: Sequence[int]) -> int:
    result = 1
    for coordinate, exponent in zip(point, exponents):
        result *= coordinate ** exponent
    return result


def deformation_ring_from_cohomology(
    data: TangentObstructionData,
    prime: int,
    maximal_ideal_order: int = 3,
    p_precision: int = 1,
) -> TruncatedDeformationRing:
    variables = tuple(f"x{i + 1}" for i in range(data.tangent_dimension))
    relations: list[Polynomial] = []
    for index in range(data.obstruction_dimension):
        if not variables:
            relations.append({(): 1})
            continue
        exponents = [0] * len(variables)
        exponents[index % len(variables)] = 2
        relations.append({tuple(exponents): 1})
    universal = data.h0 == 0
    hypotheses = () if universal else ("nontrivial infinitesimal automorphisms",)
    return TruncatedDeformationRing(
        prime, variables, tuple(relations), maximal_ideal_order, p_precision,
        universal, hypotheses,
    )
