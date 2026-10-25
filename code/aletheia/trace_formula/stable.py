# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""Stable conjugacy and transfer-factor bookkeeping.

Treatise correspondence: see Appendix G of the book (The Reference Implementation).
Genuine computation: finite stable packets, signed transfer matrices,
normalization audits, and finite fundamental-lemma comparisons.
Interface-only: canonical transfer factors and general endoscopy.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Mapping, Sequence


@dataclass(frozen=True)
class TransferFactor:
    source_orbit: str
    target_orbit: str
    value: Fraction
    normalization: str
    orientation_line: str | None = None


@dataclass(frozen=True)
class StableOrbitalPacket:
    identifier: str
    rational_orbits: tuple[str, ...]
    weights: tuple[Fraction, ...]

    def __post_init__(self) -> None:
        if len(self.rational_orbits) != len(self.weights):
            raise ValueError("each rational orbit needs a stable weight")

    def stable_sum(self, values: Mapping[str, Fraction]) -> Fraction:
        return sum(
            (weight * values.get(orbit, Fraction(0))
             for orbit, weight in zip(self.rational_orbits, self.weights)),
            Fraction(0),
        )


@dataclass(frozen=True)
class TransferComparison:
    source_value: Fraction
    target_values: Mapping[str, Fraction]
    factors: tuple[TransferFactor, ...]

    @property
    def transferred_value(self) -> Fraction:
        return sum(
            (
                factor.value * self.target_values[factor.target_orbit]
                for factor in self.factors
            ),
            Fraction(0),
        )

    @property
    def verifies(self) -> bool:
        return self.source_value == self.transferred_value

    def normalizations(self) -> frozenset[str]:
        return frozenset(factor.normalization for factor in self.factors)
