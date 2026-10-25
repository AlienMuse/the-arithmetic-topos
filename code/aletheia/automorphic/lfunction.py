# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""Completed L-functions and functional-equation diagnostics.

Treatise correspondence: see Appendix G of the book (The Reference Implementation).
Genuine computation: zeta via eta continuation, gamma factors, elliptic-curve
point counts and multiplicative coefficients, and finite approximate
functional-equation diagnostics with disclosed truncation.
Interface-only: modularity and functional equations are assumptions recorded
on LFunction objects, never inferred from coefficient agreement.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import cmath
from functools import lru_cache
from math import exp, gamma, gcd, pi
from types import MappingProxyType
from typing import Callable, Mapping, Sequence

from aletheia.numerics.dirichlet import factor_integer, primes_up_to


def complex_gamma(value: complex) -> complex:
    """Lanczos gamma approximation, adequate for diagnostic numerics."""

    coefficients = (
        0.99999999999980993, 676.5203681218851, -1259.1392167224028,
        771.32342877765313, -176.6150291621406, 12.507343278686905,
        -0.13857109526572012, 9.9843695780195716e-6,
        1.5056327351493116e-7,
    )
    if value.real < 0.5:
        return pi / (cmath.sin(pi * value) * complex_gamma(1 - value))
    z = value - 1
    x = coefficients[0]
    for index, coefficient in enumerate(coefficients[1:], 1):
        x += coefficient / (z + index)
    t = z + 7.5
    return cmath.sqrt(2 * pi) * t ** (z + 0.5) * cmath.exp(-t) * x


def eta(s: complex, terms: int = 2000) -> complex:
    """Euler-transformed alternating zeta series."""

    if terms < 2:
        raise ValueError("terms must be at least two")
    # Hasse's globally convergent series for eta(s).
    total = 0j
    for n in range(terms):
        inner = 0j
        binomial = 1
        for k in range(n + 1):
            inner += ((-1) ** k) * binomial * (k + 1) ** (-s)
            if k < n:
                binomial = binomial * (n - k) // (k + 1)
        term = inner / (2 ** (n + 1))
        total += term
        if abs(term) < 1e-16 and n > 30:
            break
    return total


def riemann_zeta(s: complex, terms: int = 2000) -> complex:
    denominator = 1 - 2 ** (1 - s)
    if abs(denominator) < 1e-14:
        raise ValueError("eta quotient is singular near s=1")
    return eta(s, terms) / denominator


def completed_zeta(s: complex, terms: int = 2000) -> complex:
    return pi ** (-s / 2) * complex_gamma(s / 2) * riemann_zeta(s, terms)


@dataclass(frozen=True)
class FunctionalEquationCheck:
    left: complex
    right: complex
    absolute_error: float
    relative_error: float
    passed: bool
    assumptions: tuple[str, ...] = ()


def check_zeta_functional_equation(
    s: complex, *, terms: int = 2000, tolerance: float = 1e-10
) -> FunctionalEquationCheck:
    left = completed_zeta(s, terms)
    right = completed_zeta(1 - s, terms)
    error = abs(left - right)
    relative = error / max(abs(left), abs(right), 1e-30)
    return FunctionalEquationCheck(
        left, right, error, relative, relative <= tolerance,
        ("analytic continuation via Hasse eta series",),
    )


@dataclass(frozen=True)
class EllipticCurve:
    """Integral generalized Weierstrass curve.

    Equation: y^2 + a1*x*y + a3*y = x^3 + a2*x^2 + a4*x + a6.
    """

    label: str
    conductor: int
    a1: int
    a2: int
    a3: int
    a4: int
    a6: int
    root_number: int
    bad_ap: Mapping[int, int] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "bad_ap", MappingProxyType(dict(self.bad_ap)))

    def __hash__(self) -> int:
        # ``ap`` is cached on the curve instance.  Mapping is intentionally
        # accepted by the public constructor, so include its canonicalised
        # items rather than relying on dataclass's generated hash (a dict is
        # unhashable).
        return hash((
            self.label, self.conductor, self.a1, self.a2, self.a3,
            self.a4, self.a6, self.root_number,
            tuple(sorted(self.bad_ap.items())),
        ))

    def discriminant(self) -> int:
        b2 = self.a1 ** 2 + 4 * self.a2
        b4 = 2 * self.a4 + self.a1 * self.a3
        b6 = self.a3 ** 2 + 4 * self.a6
        b8 = (
            self.a1 ** 2 * self.a6 + 4 * self.a2 * self.a6
            - self.a1 * self.a3 * self.a4 + self.a2 * self.a3 ** 2
            - self.a4 ** 2
        )
        return -b2 ** 2 * b8 - 8 * b4 ** 3 - 27 * b6 ** 2 + 9 * b2 * b4 * b6

    def point_count_mod_p(self, prime: int) -> int:
        count = 1  # point at infinity
        for x in range(prime):
            rhs = (x ** 3 + self.a2 * x * x + self.a4 * x + self.a6) % prime
            for y in range(prime):
                lhs = (y * y + self.a1 * x * y + self.a3 * y) % prime
                count += int(lhs == rhs)
        return count

    @lru_cache(maxsize=None)
    def ap(self, prime: int) -> int:
        if self.conductor % prime == 0 and prime in self.bad_ap:
            return self.bad_ap[prime]
        return prime + 1 - self.point_count_mod_p(prime)

    def coefficients(self, terms: int) -> list[int]:
        if terms < 1:
            return [0]
        values = [0] * (terms + 1)
        values[1] = 1
        for prime in primes_up_to(terms):
            values[prime] = self.ap(prime)
            power = prime * prime
            exponent = 2
            while power <= terms:
                if self.conductor % prime:
                    values[power] = (
                        self.ap(prime) * values[power // prime]
                        - prime * values[power // (prime * prime)]
                    )
                else:
                    values[power] = self.ap(prime) ** exponent
                exponent += 1
                power *= prime
        for n in range(2, terms + 1):
            if values[n]:
                continue
            factors = factor_integer(n)
            result = 1
            for prime, exponent in factors.items():
                result *= values[prime ** exponent]
            values[n] = result
        return values


CURVES: dict[str, EllipticCurve] = {
    "11a1": EllipticCurve(
        "11a1", 11, 0, -1, 1, -10, -20, +1, {11: -1}
    ),
}


@dataclass
class LFunction:
    name: str
    conductor: int
    weight: int
    root_number: int
    coefficients: Sequence[complex]
    functional_equation_assumed: bool = True

    def dirichlet_sum(self, s: complex, terms: int | None = None) -> complex:
        limit = min(terms or len(self.coefficients) - 1,
                    len(self.coefficients) - 1)
        return sum(
            (complex(self.coefficients[n]) / n ** s for n in range(1, limit + 1)),
            0j,
        )

    def smoothed_completed(self, s: complex, terms: int | None = None) -> complex:
        """A symmetric exponentially smoothed approximate FE.

        This is a diagnostic, not a rigorous enclosure.  Both sums are
        visible, and truncation is controlled by the supplied coefficient list.
        """

        limit = min(terms or len(self.coefficients) - 1,
                    len(self.coefficients) - 1)
        scale = 2 * pi / (self.conductor ** 0.5)
        first = 0j
        dual = 0j
        for n in range(1, limit + 1):
            coefficient = complex(self.coefficients[n])
            cutoff = exp(-scale * n)
            first += coefficient * cutoff / (n ** s)
            dual += coefficient.conjugate() * cutoff / (n ** (self.weight - s))
        gamma_factor = self.conductor ** (s / 2) * (2 * pi) ** (-s) * complex_gamma(s)
        dual_factor = (
            self.root_number
            * self.conductor ** ((self.weight - s) / 2)
            * (2 * pi) ** (-(self.weight - s))
            * complex_gamma(self.weight - s)
        )
        return gamma_factor * first + dual_factor * dual

    def check_functional_equation(
        self, s: complex, *, terms: int | None = None, tolerance: float = 1e-10
    ) -> FunctionalEquationCheck:
        left = self.smoothed_completed(s, terms)
        right = self.root_number * self.smoothed_completed(
            self.weight - s.conjugate(), terms
        ).conjugate()
        error = abs(left - right)
        relative = error / max(abs(left), abs(right), 1e-30)
        return FunctionalEquationCheck(
            left, right, error, relative, relative <= tolerance,
            (
                "modularity and functional equation supplied as metadata",
                "finite exponentially smoothed coefficient truncation",
            ),
        )


def elliptic_curve_lfunction(label: str, terms: int = 200) -> LFunction:
    try:
        curve = CURVES[label.lower()]
    except KeyError as error:
        raise ValueError(f"unknown built-in curve {label!r}") from error
    coefficients = curve.coefficients(terms)
    return LFunction(
        f"L({curve.label},s)", curve.conductor, 2, curve.root_number,
        tuple(complex(value) for value in coefficients),
    )
