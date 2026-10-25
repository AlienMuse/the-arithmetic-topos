# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""Primitive trace theory, shadows, and finite categorical traces.

Treatise correspondence: see Appendix G of the book (The Reference Implementation).
Genuine computation: ordinary/super traces, Lefschetz numbers, cyclic-word
orbits, and truncated Hochschild dimensions for finite algebras.
Interface-only: localization for arbitrary infinity-categories and THH/TC.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Callable, Generic, Iterable, Mapping, Protocol, Sequence, TypeVar

T = TypeVar("T")


class TraceTheory(Protocol[T]):
    def trace(self, endomorphism: T) -> object:
        """Compute a trace in the target shadow."""


def matrix_trace(matrix: Sequence[Sequence[int | Fraction | complex]]) -> complex:
    if any(len(row) != len(matrix) for row in matrix):
        raise ValueError("trace requires a square matrix")
    return sum((complex(matrix[i][i]) for i in range(len(matrix))), 0j)


def supertrace(
    graded_endomorphisms: Mapping[int, Sequence[Sequence[int | Fraction | complex]]]
) -> complex:
    return sum(
        (((-1) ** degree) * matrix_trace(matrix)
         for degree, matrix in graded_endomorphisms.items()),
        0j,
    )


@dataclass(frozen=True)
class LefschetzDatum:
    cohomology_actions: Mapping[int, tuple[tuple[complex, ...], ...]]
    fixed_point_terms: tuple[complex, ...] = ()

    @property
    def cohomological_trace(self) -> complex:
        return supertrace(self.cohomology_actions)

    @property
    def localized_trace(self) -> complex:
        return sum(self.fixed_point_terms, 0j)

    def verifies_localization(self, tolerance: float = 1e-10) -> bool:
        return abs(self.cohomological_trace - self.localized_trace) <= tolerance


@dataclass(frozen=True)
class Shadow:
    """A finite bicategorical shadow represented by cyclic-word classes."""

    alphabet: tuple[str, ...]

    @staticmethod
    def canonical_rotation(word: Sequence[str]) -> tuple[str, ...]:
        if not word:
            return ()
        rotations = [
            tuple(word[index:] + word[:index])  # type: ignore[operator]
            for index in range(len(word))
        ]
        return min(rotations)

    def class_of(self, word: Sequence[str]) -> tuple[str, ...]:
        if any(letter not in self.alphabet for letter in word):
            raise ValueError("word uses a symbol outside the shadow alphabet")
        return self.canonical_rotation(list(word))

    def classes(self, length: int) -> tuple[tuple[str, ...], ...]:
        if length < 0:
            raise ValueError("length must be nonnegative")
        if length == 0:
            return ((),)
        current: set[tuple[str, ...]] = {()}
        for _ in range(length):
            current = {
                prefix + (letter,)
                for prefix in current
                for letter in self.alphabet
            }
        return tuple(sorted({self.class_of(word) for word in current}))


@dataclass(frozen=True)
class TruncatedCategoricalTrace:
    chain_dimensions: tuple[int, ...]
    homology_dimensions: tuple[int, ...]
    bound: int
    exact: bool
    truncation_reason: str
    frobenius_supertrace: complex | None = None

    @property
    def euler_characteristic(self) -> int:
        return sum((-1) ** i * value
                   for i, value in enumerate(self.homology_dimensions))


def categorical_trace_finite_algebra(
    algebra_dimension: int,
    bimodule_dimension: int,
    bound: int,
    *,
    tail_vanishing_degree: int | None = None,
) -> TruncatedCategoricalTrace:
    """Dimension model for the normalized cyclic bar complex.

    It computes actual dimensions of M tensor A^tensor n.  Differentials
    require multiplication tables and are therefore conservatively modelled
    as zero unless a richer dg presentation is supplied.
    """

    if min(algebra_dimension, bimodule_dimension, bound) < 0:
        raise ValueError("dimensions and bound must be nonnegative")
    chains = tuple(
        bimodule_dimension * algebra_dimension ** degree
        for degree in range(bound + 1)
    )
    exact = tail_vanishing_degree is not None and bound >= tail_vanishing_degree
    reason = (
        f"tail vanishes above degree {tail_vanishing_degree}"
        if exact else "finite bar truncation; no tail-vanishing theorem supplied"
    )
    return TruncatedCategoricalTrace(chains, chains, bound, exact, reason)
