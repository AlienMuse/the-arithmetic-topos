# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""Dirichlet series and finite Euler-product arithmetic.

Treatise correspondence: see Appendix G of the book (The Reference Implementation).
Genuine computation: coefficient convolution, Euler-factor expansion,
prime generation, truncated sums/products, and rigorous tail bounds when
the caller provides coefficient-growth estimates.
Interface-only: analytic continuation is never inferred from finite data.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import log
from typing import Callable, Iterable, Iterator, Mapping, Sequence


def primes_up_to(limit: int) -> list[int]:
    if limit < 2:
        return []
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    for candidate in range(2, int(limit ** 0.5) + 1):
        if sieve[candidate]:
            start = candidate * candidate
            sieve[start:limit + 1:candidate] = b"\x00" * (
                (limit - start) // candidate + 1
            )
    return [index for index, flag in enumerate(sieve) if flag]


def factor_integer(value: int) -> dict[int, int]:
    if value < 1:
        raise ValueError("factorization requires a positive integer")
    result: dict[int, int] = {}
    remaining = value
    divisor = 2
    while divisor * divisor <= remaining:
        while remaining % divisor == 0:
            result[divisor] = result.get(divisor, 0) + 1
            remaining //= divisor
        divisor = 3 if divisor == 2 else divisor + 2
    if remaining > 1:
        result[remaining] = result.get(remaining, 0) + 1
    return result


def dirichlet_convolution(
    left: Sequence[complex | float | int],
    right: Sequence[complex | float | int],
) -> list[complex]:
    terms = min(len(left), len(right))
    output = [0j] * terms
    for n in range(1, terms):
        total = 0j
        for divisor in range(1, int(n ** 0.5) + 1):
            if n % divisor:
                continue
            quotient = n // divisor
            if divisor < len(left) and quotient < len(right):
                total += complex(left[divisor]) * complex(right[quotient])
            if divisor != quotient and quotient < len(left) and divisor < len(right):
                total += complex(left[quotient]) * complex(right[divisor])
        output[n] = total
    return output


@dataclass(frozen=True)
class LocalEulerFactor:
    prime: int
    denominator: tuple[complex, ...]
    numerator: tuple[complex, ...] = (1 + 0j,)

    def __post_init__(self) -> None:
        if self.prime < 2 or not self.denominator:
            raise ValueError("invalid local factor")
        if abs(self.denominator[0] - 1) > 1e-12:
            raise ValueError("Euler denominator must have constant term one")

    def evaluate(self, s: complex) -> complex:
        variable = self.prime ** (-s)
        numerator = sum(value * variable ** index
                        for index, value in enumerate(self.numerator))
        denominator = sum(value * variable ** index
                          for index, value in enumerate(self.denominator))
        return numerator / denominator

    def reciprocal_coefficients(self, count: int) -> tuple[complex, ...]:
        """Power-series coefficients of numerator/denominator."""

        if count < 1:
            return ()
        inverse = [0j] * count
        inverse[0] = 1 / self.denominator[0]
        for degree in range(1, count):
            inverse[degree] = -sum(
                self.denominator[j] * inverse[degree - j]
                for j in range(1, min(degree, len(self.denominator) - 1) + 1)
            ) / self.denominator[0]
        output = [0j] * count
        for degree in range(count):
            output[degree] = sum(
                self.numerator[j] * inverse[degree - j]
                for j in range(min(degree, len(self.numerator) - 1) + 1)
            )
        return tuple(output)


@dataclass
class DirichletSeries:
    coefficient: Callable[[int], complex]
    name: str = "Dirichlet series"
    abscissa_absolute: float | None = None

    def partial_sum(self, s: complex, terms: int) -> complex:
        if terms < 1:
            raise ValueError("terms must be positive")
        return sum(
            (self.coefficient(n) / (n ** s) for n in range(1, terms + 1)),
            0j,
        )

    def values(self, terms: int) -> tuple[complex, ...]:
        return tuple(self.coefficient(n) for n in range(1, terms + 1))

    def tail_bound_power_growth(
        self, sigma: float, terms: int, constant: float, exponent: float
    ) -> float:
        """Bound sum |a_n|n^-sigma if |a_n| <= constant*n^exponent."""

        decay = sigma - exponent
        if decay <= 1:
            raise ValueError("provided growth bound does not imply convergence")
        return constant * (terms ** (1 - decay)) / (decay - 1)


@dataclass
class EulerProduct:
    factor: Callable[[int], LocalEulerFactor]
    name: str = "Euler product"

    def partial_product(self, s: complex, prime_bound: int) -> complex:
        result = 1 + 0j
        for prime in primes_up_to(prime_bound):
            result *= self.factor(prime).evaluate(s)
        return result

    def coefficients(self, terms: int) -> list[complex]:
        """Expand multiplicatively from local reciprocal series."""

        output = [0j] * (terms + 1)
        output[1] = 1 + 0j
        for prime in primes_up_to(terms):
            maximum_power = 0
            power = 1
            while power * prime <= terms:
                power *= prime
                maximum_power += 1
            local = self.factor(prime).reciprocal_coefficients(maximum_power + 1)
            previous = output[:]
            for n in range(1, terms + 1):
                if n % prime == 0:
                    continue
                prime_power = 1
                for exponent in range(maximum_power + 1):
                    index = n * prime_power
                    if index > terms:
                        break
                    output[index] = previous[n] * local[exponent]
                    prime_power *= prime
        return output


def zeta_euler_factor(prime: int) -> LocalEulerFactor:
    return LocalEulerFactor(prime, (1 + 0j, -1 + 0j))


def mobius(n: int) -> int:
    factors = factor_integer(n)
    return 0 if any(exponent > 1 for exponent in factors.values()) else (-1) ** len(factors)


def divisor_count(n: int) -> int:
    result = 1
    for exponent in factor_integer(n).values():
        result *= exponent + 1
    return result
