# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""Newton polygons, isocrystal slope data, and B(GL_n).

Treatise correspondence: see Appendix G of the book (The Reference Implementation).
Genuine computation: lower convex hulls, rational slope multisets,
dominance, Kottwitz invariant, and Hodge–Newton break tests.
Interface-only: B(G) for arbitrary reductive groups and actual isocrystals.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import accumulate
from typing import Iterable, Sequence


@dataclass(frozen=True, order=True)
class PolygonPoint:
    x: int
    y: Fraction


def _cross(origin: PolygonPoint, left: PolygonPoint, right: PolygonPoint) -> Fraction:
    return (
        Fraction(left.x - origin.x) * (right.y - origin.y)
        - (left.y - origin.y) * Fraction(right.x - origin.x)
    )


@dataclass(frozen=True)
class NewtonPolygon:
    vertices: tuple[PolygonPoint, ...]

    @classmethod
    def from_coeff_valuations(
        cls, valuations: Sequence[int | Fraction | None]
    ) -> "NewtonPolygon":
        points = [
            PolygonPoint(index, Fraction(value))
            for index, value in enumerate(valuations)
            if value is not None
        ]
        if len(points) < 2 or points[0].x != 0:
            raise ValueError("valuation data must include x=0 and one later point")
        hull: list[PolygonPoint] = []
        for point in points:
            while len(hull) >= 2 and _cross(hull[-2], hull[-1], point) <= 0:
                hull.pop()
            hull.append(point)
        return cls(tuple(hull))

    @classmethod
    def from_slopes(
        cls, slopes: Sequence[int | Fraction]
    ) -> "NewtonPolygon":
        ordered = sorted(Fraction(slope) for slope in slopes)
        heights = [Fraction(0), *accumulate(ordered)]
        return cls(tuple(PolygonPoint(i, height) for i, height in enumerate(heights)))

    @property
    def rank(self) -> int:
        return self.vertices[-1].x

    def slopes(self) -> tuple[Fraction, ...]:
        output: list[Fraction] = []
        for left, right in zip(self.vertices, self.vertices[1:]):
            slope = (right.y - left.y) / (right.x - left.x)
            output.extend([slope] * (right.x - left.x))
        return tuple(output)

    def height_at(self, x: int) -> Fraction:
        if not 0 <= x <= self.rank:
            raise ValueError("abscissa lies outside polygon")
        for left, right in zip(self.vertices, self.vertices[1:]):
            if left.x <= x <= right.x:
                return left.y + Fraction(x - left.x) * (
                    (right.y - left.y) / (right.x - left.x)
                )
        return self.vertices[-1].y

    def dominates(self, other: "NewtonPolygon") -> bool:
        if self.rank != other.rank:
            return False
        if self.vertices[-1].y != other.vertices[-1].y:
            return False
        return all(self.height_at(x) >= other.height_at(x)
                   for x in range(self.rank + 1))

    def breakpoints(self) -> tuple[int, ...]:
        return tuple(point.x for point in self.vertices[1:-1])


@dataclass(frozen=True)
class GLnSigmaConjugacyClass:
    """The B(GL_n) invariant represented by a nondecreasing slope multiset."""

    slopes: tuple[Fraction, ...]

    def __post_init__(self) -> None:
        if not self.slopes:
            raise ValueError("B(GL_n) class must have positive rank")
        if tuple(sorted(self.slopes)) != self.slopes:
            raise ValueError("slopes must be nondecreasing")

    @classmethod
    def from_slopes(
        cls, slopes: Iterable[int | Fraction]
    ) -> "GLnSigmaConjugacyClass":
        return cls(tuple(sorted(Fraction(value) for value in slopes)))

    @property
    def n(self) -> int:
        return len(self.slopes)

    @property
    def kottwitz_invariant(self) -> Fraction:
        return sum(self.slopes, Fraction(0))

    @property
    def newton_point(self) -> tuple[Fraction, ...]:
        return tuple(reversed(self.slopes))

    @property
    def is_basic(self) -> bool:
        return len(set(self.slopes)) == 1

    def polygon(self) -> NewtonPolygon:
        return NewtonPolygon.from_slopes(self.slopes)

    def acceptable_for_hodge(self, hodge_slopes: Sequence[int | Fraction]) -> bool:
        hodge = NewtonPolygon.from_slopes(hodge_slopes)
        newton = self.polygon()
        return (
            hodge.rank == newton.rank
            and hodge.vertices[-1].y == newton.vertices[-1].y
            and hodge.dominates(newton)
        )


def kottwitz_set_gl_n(
    n: int,
    denominator_bound: int,
    height_min: int,
    height_max: int,
) -> tuple[GLnSigmaConjugacyClass, ...]:
    """Enumerate a bounded finite window in B(GL_n)."""

    if n < 1 or denominator_bound < 1:
        raise ValueError("rank and denominator bound must be positive")
    candidates = sorted({
        Fraction(numerator, denominator)
        for denominator in range(1, denominator_bound + 1)
        for numerator in range(height_min * denominator,
                               height_max * denominator + 1)
    })
    output: list[GLnSigmaConjugacyClass] = []

    def recurse(prefix: list[Fraction], start: int) -> None:
        if len(prefix) == n:
            output.append(GLnSigmaConjugacyClass(tuple(prefix)))
            return
        for index in range(start, len(candidates)):
            recurse([*prefix, candidates[index]], index)

    recurse([], 0)
    return tuple(output)


@dataclass(frozen=True)
class HodgeNewtonResult:
    admissible: bool
    decomposition_breaks: tuple[int, ...]
    common_endpoint: bool
    explanation: str


def hodge_newton_decomposition(
    newton_slopes: Sequence[int | Fraction],
    hodge_slopes: Sequence[int | Fraction],
) -> HodgeNewtonResult:
    newton = NewtonPolygon.from_slopes(newton_slopes)
    hodge = NewtonPolygon.from_slopes(hodge_slopes)
    if newton.rank != hodge.rank:
        return HodgeNewtonResult(False, (), False, "ranks differ")
    common_endpoint = newton.height_at(newton.rank) == hodge.height_at(hodge.rank)
    admissible = common_endpoint and hodge.dominates(newton)
    shared = tuple(
        x for x in range(1, newton.rank)
        if newton.height_at(x) == hodge.height_at(x)
        and x in newton.breakpoints()
    )
    explanation = (
        f"admissible with Hodge–Newton breaks {shared}"
        if admissible else
        "Newton polygon is not below the Hodge polygon with equal endpoint"
    )
    return HodgeNewtonResult(admissible, shared, common_endpoint, explanation)
