# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""Based root data and Langlands dual groups.

Treatise correspondence: see Appendix G of the book (The Reference Implementation).
Genuine computation: Cartan matrices for A/B/C/D/G2, dual root datum,
Weyl reflections, Dynkin metadata, and duality involution.
Interface-only: non-split Galois actions and exceptional E/F types.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import re
from typing import Iterable, Sequence


def _cartan(type_name: str, rank: int) -> tuple[tuple[int, ...], ...]:
    if rank < 1:
        raise ValueError("rank must be positive")
    family = type_name.upper()
    if family == "A":
        matrix = [[2 if i == j else -1 if abs(i - j) == 1 else 0
                   for j in range(rank)] for i in range(rank)]
    elif family == "B":
        if rank < 2:
            raise ValueError("B_n requires n >= 2")
        matrix = [[2 if i == j else -1 if abs(i - j) == 1 else 0
                   for j in range(rank)] for i in range(rank)]
        matrix[-2][-1], matrix[-1][-2] = -2, -1
    elif family == "C":
        if rank < 2:
            raise ValueError("C_n requires n >= 2")
        matrix = [[2 if i == j else -1 if abs(i - j) == 1 else 0
                   for j in range(rank)] for i in range(rank)]
        matrix[-2][-1], matrix[-1][-2] = -1, -2
    elif family == "D":
        if rank < 4:
            raise ValueError("D_n requires n >= 4")
        matrix = [[0] * rank for _ in range(rank)]
        for i in range(rank):
            matrix[i][i] = 2
        for i in range(rank - 3):
            matrix[i][i + 1] = matrix[i + 1][i] = -1
        branch = rank - 3
        matrix[branch][rank - 2] = matrix[rank - 2][branch] = -1
        matrix[branch][rank - 1] = matrix[rank - 1][branch] = -1
    elif family == "G":
        if rank != 2:
            raise ValueError("only G2 exists")
        matrix = [[2, -1], [-3, 2]]
    else:
        raise ValueError(f"unsupported root-system family {family!r}")
    return tuple(tuple(row) for row in matrix)


@dataclass(frozen=True)
class RootDatum:
    family: str
    rank: int
    cartan: tuple[tuple[int, ...], ...]
    name: str
    isogeny: str = "simply-connected"

    @classmethod
    def classical(
        cls, family: str, rank: int, *, isogeny: str = "simply-connected"
    ) -> "RootDatum":
        family = family.upper()
        label = "G2" if family == "G" else f"{family}{rank}"
        return cls(family, rank, _cartan(family, rank), label, isogeny)

    @classmethod
    def parse(cls, text: str) -> "RootDatum":
        cleaned = text.upper().replace("_", "").replace(" ", "")
        match = re.fullmatch(r"([ABCD])([0-9]+)|G2", cleaned)
        if not match:
            raise ValueError(f"cannot parse root datum {text!r}")
        if cleaned == "G2":
            return cls.classical("G", 2)
        return cls.classical(cleaned[0], int(cleaned[1:]))

    @property
    def dual_family(self) -> str:
        return {"B": "C", "C": "B"}.get(self.family, self.family)

    def dual(self) -> "RootDatum":
        dual_isogeny = {
            "simply-connected": "adjoint",
            "adjoint": "simply-connected",
        }.get(self.isogeny, self.isogeny)
        family = self.dual_family
        label = "G2" if family == "G" else f"{family}{self.rank}"
        transposed = tuple(
            tuple(self.cartan[j][i] for j in range(self.rank))
            for i in range(self.rank)
        )
        return RootDatum(family, self.rank, transposed, label, dual_isogeny)

    def duality_involution_holds(self) -> bool:
        return self.dual().dual() == self

    def simple_reflection(
        self, index: int, weight: Sequence[int | Fraction]
    ) -> tuple[Fraction, ...]:
        if not 0 <= index < self.rank or len(weight) != self.rank:
            raise ValueError("reflection index or weight dimension is invalid")
        pairing = Fraction(weight[index])
        return tuple(
            Fraction(value) - pairing * self.cartan[index][j]
            for j, value in enumerate(weight)
        )

    def weyl_orbit(
        self, weight: Sequence[int], *, max_size: int = 100_000
    ) -> tuple[tuple[Fraction, ...], ...]:
        start = tuple(Fraction(value) for value in weight)
        seen = {start}
        frontier = [start]
        while frontier:
            current = frontier.pop()
            for index in range(self.rank):
                candidate = self.simple_reflection(index, current)
                if candidate not in seen:
                    seen.add(candidate)
                    frontier.append(candidate)
                    if len(seen) > max_size:
                        raise OverflowError("Weyl orbit exceeded configured bound")
        return tuple(sorted(seen))

    def positive_root_count(self) -> int:
        return {
            "A": self.rank * (self.rank + 1) // 2,
            "B": self.rank * self.rank,
            "C": self.rank * self.rank,
            "D": self.rank * (self.rank - 1),
            "G": 6,
        }[self.family]

    def dimension(self) -> int:
        return self.rank + 2 * self.positive_root_count()


@dataclass(frozen=True)
class LGroup:
    original: RootDatum
    dual_root_datum: RootDatum
    galois_action: tuple[tuple[int, ...], ...] = ()

    @classmethod
    def split(cls, root_datum: RootDatum) -> "LGroup":
        identity_action = tuple(
            tuple(int(i == j) for j in range(root_datum.rank))
            for i in range(root_datum.rank)
        )
        return cls(root_datum, root_datum.dual(), identity_action)

    @property
    def name(self) -> str:
        return f"^{chr(76)}{self.original.name} ({self.dual_root_datum.name})"

    def dual_again(self) -> "LGroup":
        return LGroup.split(self.dual_root_datum)


def langlands_dual(type_name: str) -> RootDatum:
    return RootDatum.parse(type_name).dual()
