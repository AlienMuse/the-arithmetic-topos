# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""Abstract six-functor formalism with finite verification hooks.

Treatise correspondence: see Appendix G of the book (The Reference Implementation).
Genuine computation: finite functor tables, adjunction triangle checks,
base-change squares, and projection-formula tests.
Interface-only: presentable stable infinity-categories and all coherences.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Generic, Mapping, Protocol, Sequence, TypeVar

ObjectT = TypeVar("ObjectT")
MorphT = TypeVar("MorphT")


class SixFunctorFormalism(Protocol[ObjectT, MorphT]):
    def pullback(self, morphism: MorphT, value: ObjectT) -> ObjectT: ...
    def pushforward(self, morphism: MorphT, value: ObjectT) -> ObjectT: ...
    def exceptional_pushforward(self, morphism: MorphT, value: ObjectT) -> ObjectT: ...
    def exceptional_pullback(self, morphism: MorphT, value: ObjectT) -> ObjectT: ...
    def tensor(self, left: ObjectT, right: ObjectT) -> ObjectT: ...
    def internal_hom(self, left: ObjectT, right: ObjectT) -> ObjectT: ...


@dataclass(frozen=True)
class Correspondence:
    left: str
    apex: str
    right: str
    left_map: str
    right_map: str

    def reverse(self) -> "Correspondence":
        return Correspondence(
            self.right, self.apex, self.left, self.right_map, self.left_map
        )


@dataclass(frozen=True)
class BaseChangeSquare:
    top: str
    bottom: str
    left: str
    right: str
    cartesian: bool
    comparison_name: str


@dataclass(frozen=True)
class AdjunctionWitness(Generic[ObjectT]):
    unit: Callable[[ObjectT], ObjectT]
    counit: Callable[[ObjectT], ObjectT]
    left: Callable[[ObjectT], ObjectT]
    right: Callable[[ObjectT], ObjectT]

    def verify(self, samples: Sequence[ObjectT]) -> bool:
        for sample in samples:
            left_triangle = self.counit(self.left(self.unit(sample)))
            right_triangle = self.right(self.counit(self.unit(sample)))
            if left_triangle != self.left(sample):
                return False
            if right_triangle != self.right(sample):
                return False
        return True


@dataclass
class FiniteSixFunctorModel:
    """A table-driven model on a finite universe of immutable values."""

    pullback_tables: Mapping[str, Mapping[object, object]]
    pushforward_tables: Mapping[str, Mapping[object, object]]
    exceptional_pushforward_tables: Mapping[str, Mapping[object, object]]
    exceptional_pullback_tables: Mapping[str, Mapping[object, object]]
    tensor_operation: Callable[[object, object], object]
    hom_operation: Callable[[object, object], object]
    unit: object
    proper_maps: set[str] = field(default_factory=set)
    etale_maps: set[str] = field(default_factory=set)

    @staticmethod
    def _lookup(
        tables: Mapping[str, Mapping[object, object]],
        morphism: str,
        value: object,
    ) -> object:
        try:
            return tables[morphism][value]
        except KeyError as error:
            raise KeyError(f"no finite six-functor value for {morphism}, {value!r}") from error

    def pullback(self, morphism: str, value: object) -> object:
        return self._lookup(self.pullback_tables, morphism, value)

    def pushforward(self, morphism: str, value: object) -> object:
        return self._lookup(self.pushforward_tables, morphism, value)

    def exceptional_pushforward(self, morphism: str, value: object) -> object:
        return self._lookup(self.exceptional_pushforward_tables, morphism, value)

    def exceptional_pullback(self, morphism: str, value: object) -> object:
        return self._lookup(self.exceptional_pullback_tables, morphism, value)

    def tensor(self, left: object, right: object) -> object:
        return self.tensor_operation(left, right)

    def internal_hom(self, left: object, right: object) -> object:
        return self.hom_operation(left, right)

    def verify_proper(self, morphism: str, samples: Sequence[object]) -> bool:
        if morphism not in self.proper_maps:
            return False
        return all(
            self.exceptional_pushforward(morphism, value)
            == self.pushforward(morphism, value)
            for value in samples
        )

    def verify_etale(self, morphism: str, samples: Sequence[object]) -> bool:
        if morphism not in self.etale_maps:
            return False
        return all(
            self.exceptional_pullback(morphism, value)
            == self.pullback(morphism, value)
            for value in samples
        )

    def verify_projection_formula(
        self, morphism: str, xs: Sequence[object], ys: Sequence[object]
    ) -> bool:
        return all(
            self.pushforward(
                morphism, self.tensor(x, self.pullback(morphism, y))
            ) == self.tensor(self.pushforward(morphism, x), y)
            for x in xs for y in ys
        )
