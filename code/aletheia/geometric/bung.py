# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""Combinatorial Bun_G over a finite base.

Treatise correspondence: see Appendix G of the book (The Reference Implementation).
Genuine computation: finite groupoid masses, Harder–Narasimhan strata,
degree-zero loci, and automorphism-weighted point counts.
Interface-only: algebraic/analytic mapping stacks and descent.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from typing import Iterable, Mapping, Sequence


@dataclass(frozen=True)
class BundleClass:
    identifier: str
    degree: int
    slopes: tuple[Fraction, ...]
    automorphism_order: int
    stable: bool = False
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.automorphism_order < 1:
            raise ValueError("automorphism group order must be positive")
        if tuple(sorted(self.slopes, reverse=True)) != self.slopes:
            raise ValueError("HN slopes must be nonincreasing")

    @property
    def semistable(self) -> bool:
        return len(set(self.slopes)) <= 1

    @property
    def mass(self) -> Fraction:
        return Fraction(1, self.automorphism_order)


@dataclass
class FiniteBunG:
    group: str
    base: str
    bundles: dict[str, BundleClass] = field(default_factory=dict)

    def add(self, bundle: BundleClass) -> None:
        if bundle.identifier in self.bundles:
            raise ValueError("bundle class identifier already exists")
        self.bundles[bundle.identifier] = bundle

    def stacky_count(self) -> Fraction:
        return sum((bundle.mass for bundle in self.bundles.values()), Fraction(0))

    def semistable_degree_zero(self) -> tuple[BundleClass, ...]:
        return tuple(
            bundle for bundle in self.bundles.values()
            if bundle.degree == 0 and bundle.semistable
        )

    def hn_strata(self) -> dict[tuple[Fraction, ...], tuple[BundleClass, ...]]:
        output: dict[tuple[Fraction, ...], list[BundleClass]] = {}
        for bundle in self.bundles.values():
            output.setdefault(bundle.slopes, []).append(bundle)
        return {key: tuple(value) for key, value in output.items()}

    def mass_by_degree(self) -> dict[int, Fraction]:
        output: dict[int, Fraction] = {}
        for bundle in self.bundles.values():
            output[bundle.degree] = output.get(bundle.degree, Fraction(0)) + bundle.mass
        return output
