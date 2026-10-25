# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""The Taylor–Wiles/derived defect l_0 in finite signature models.

Treatise correspondence: see Appendix G of the book (The Reference Implementation).
Genuine computation: the standard real-rank defect for split GL_n and
classical groups across number-field signatures.
Interface-only: automorphic cohomological ranges for arbitrary inner forms.
"""
from __future__ import annotations

from dataclasses import dataclass
import re

from .cohomology import NumberFieldSignature


@dataclass(frozen=True)
class ReductiveGroupModel:
    family: str
    rank: int
    label: str

    @classmethod
    def parse(cls, text: str) -> "ReductiveGroupModel":
        cleaned = text.upper().replace("_", "").replace(" ", "")
        match = re.fullmatch(r"(GL|SL|SP|SO)([0-9]+)", cleaned)
        if not match:
            raise ValueError(f"unsupported group {text!r}")
        family, degree = match.group(1), int(match.group(2))
        if family in {"GL", "SL"}:
            rank = degree - 1
        elif family == "SP":
            if degree % 2:
                raise ValueError("Sp degree must be even")
            rank = degree // 2
        else:
            rank = degree // 2
        return cls(family, rank, cleaned)

    @property
    def degree(self) -> int:
        if self.family in {"GL", "SL"}:
            return self.rank + 1
        if self.family == "SP":
            return 2 * self.rank
        return 2 * self.rank if self.label.endswith(str(2 * self.rank)) else 2 * self.rank + 1

    def local_defect_real(self) -> int:
        if self.family == "GL":
            n = self.rank + 1
            return max(0, n - n // 2 - 1)
        if self.family == "SL":
            n = self.rank + 1
            return max(0, (n - 1) - n // 2)
        if self.family == "SP":
            return 0
        if self.family == "SO":
            return 0
        return 0

    def local_defect_complex(self) -> int:
        if self.family in {"GL", "SL"}:
            return self.rank
        return self.rank


@dataclass(frozen=True)
class DefectResult:
    group: ReductiveGroupModel
    field: NumberFieldSignature
    l0: int
    real_contribution: int
    complex_contribution: int
    formula: str

    @property
    def classical_taylor_wiles(self) -> bool:
        return self.l0 == 0


def defect(
    group: str | ReductiveGroupModel,
    field: str | NumberFieldSignature,
) -> DefectResult:
    group_model = (
        ReductiveGroupModel.parse(group) if isinstance(group, str) else group
    )
    field_model = (
        NumberFieldSignature.parse(field) if isinstance(field, str) else field
    )
    real = field_model.real_places * group_model.local_defect_real()
    complex_value = (
        field_model.complex_places * group_model.local_defect_complex()
    )
    total = real + complex_value
    return DefectResult(
        group_model,
        field_model,
        total,
        real,
        complex_value,
        "l0 = r1*(rank_R G-rank K-rank A_G) + "
        "r2*(complex semisimple rank)",
    )


def is_classical_taylor_wiles_case(group: str, field: str) -> bool:
    return defect(group, field).classical_taylor_wiles
