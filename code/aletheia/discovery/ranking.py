# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""Value-of-information ranking of open statements.

Treatise correspondence: see Appendix G of the book (The Reference Implementation).
Genuine computation: transparent multi-criterion ranking and Pareto fronts.
Interface-only: numerical scores are priorities, never truth probabilities.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import log1p
from typing import Iterable, Mapping


@dataclass(frozen=True)
class OpenProblem:
    identifier: str
    impact: float
    tractability: float
    uncertainty: float
    verification_cost: float
    dependency_unlocks: int = 0
    ethical_risk: float = 0.0

    def validate(self) -> None:
        for name in ("impact", "tractability", "uncertainty", "ethical_risk"):
            value = getattr(self, name)
            if not 0 <= value <= 1:
                raise ValueError(f"{name} must lie in [0,1]")
        if self.verification_cost < 0 or self.dependency_unlocks < 0:
            raise ValueError("cost and unlock count must be nonnegative")


@dataclass(frozen=True)
class RankedProblem:
    problem: OpenProblem
    score: float
    components: Mapping[str, float]


def value_of_information(problem: OpenProblem) -> RankedProblem:
    problem.validate()
    unlock = log1p(problem.dependency_unlocks) / 5
    benefit = (
        0.35 * problem.impact
        + 0.25 * problem.tractability
        + 0.25 * problem.uncertainty
        + 0.15 * unlock
    )
    cost = 1 + problem.verification_cost
    safety = 1 - 0.75 * problem.ethical_risk
    score = benefit * safety / cost
    return RankedProblem(
        problem, score,
        {"benefit": benefit, "cost": cost, "safety": safety, "unlock": unlock},
    )


def rank_problems(problems: Iterable[OpenProblem]) -> tuple[RankedProblem, ...]:
    return tuple(sorted(
        (value_of_information(problem) for problem in problems),
        key=lambda item: (-item.score, item.problem.identifier),
    ))
