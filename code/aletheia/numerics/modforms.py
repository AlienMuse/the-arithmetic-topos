# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""q-expansions and finite Hecke-eigenvalue arithmetic.

Treatise correspondence: see Appendix G of the book (The Reference Implementation).
Genuine computation: truncated q-series products, powers, derivatives,
Hecke operators on formal q-expansions, and elliptic newform coefficients.
Interface-only: modularity proofs and general modular-symbol construction.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable, Sequence

from aletheia.automorphic.lfunction import CURVES


@dataclass(frozen=True)
class QExpansion:
    coefficients: tuple[Fraction, ...]
    weight: int | None = None
    level: int | None = None

    @classmethod
    def from_values(
        cls, values: Sequence[int | Fraction], **metadata: int | None
    ) -> "QExpansion":
        return cls(tuple(Fraction(value) for value in values), **metadata)

    @property
    def precision(self) -> int:
        return len(self.coefficients)

    def coefficient(self, n: int) -> Fraction:
        return self.coefficients[n] if 0 <= n < self.precision else Fraction(0)

    def truncate(self, precision: int) -> "QExpansion":
        values = self.coefficients[:precision]
        values += (Fraction(0),) * max(0, precision - len(values))
        return QExpansion(values, self.weight, self.level)

    def __add__(self, other: "QExpansion") -> "QExpansion":
        precision = max(self.precision, other.precision)
        values = tuple(
            self.coefficient(i) + other.coefficient(i) for i in range(precision)
        )
        return QExpansion(values, self.weight, self.level)

    def __mul__(self, other: "QExpansion") -> "QExpansion":
        precision = min(self.precision, other.precision)
        values = []
        for n in range(precision):
            values.append(sum(
                (self.coefficient(i) * other.coefficient(n - i)
                 for i in range(n + 1)),
                Fraction(0),
            ))
        weight = (
            self.weight + other.weight
            if self.weight is not None and other.weight is not None else None
        )
        return QExpansion(tuple(values), weight, self.level or other.level)

    def derivative_q(self) -> "QExpansion":
        return QExpansion(
            tuple(Fraction(n) * value
                  for n, value in enumerate(self.coefficients)),
            None,
            self.level,
        )

    def hecke(self, prime: int) -> "QExpansion":
        if self.weight is None:
            raise ValueError("Hecke action requires a weight")
        values = []
        for n in range(self.precision):
            first = self.coefficient(prime * n)
            second = (
                prime ** (self.weight - 1) * self.coefficient(n // prime)
                if n % prime == 0 else Fraction(0)
            )
            values.append(first + second)
        return QExpansion(tuple(values), self.weight, self.level)


def elliptic_newform(label: str, precision: int = 100) -> QExpansion:
    curve = CURVES[label.lower()]
    coefficients = curve.coefficients(precision - 1)
    return QExpansion(
        tuple(Fraction(value) for value in coefficients),
        weight=2,
        level=curve.conductor,
    )


def eisenstein_e4(precision: int) -> QExpansion:
    values = [Fraction(0)] * precision
    if precision:
        values[0] = Fraction(1)
    for n in range(1, precision):
        sigma3 = sum(d ** 3 for d in range(1, n + 1) if n % d == 0)
        values[n] = Fraction(240 * sigma3)
    return QExpansion(tuple(values), weight=4, level=1)
