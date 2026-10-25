# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""Conjecture representation and falsification protocols.

Treatise correspondence: see Appendix G of the book (The Reference Implementation).
Genuine computation: bounded-domain checks, witness minimization, and
hypothesis tracking. Interface-only: generative mathematical creativity.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Generic, Iterable, Sequence, TypeVar

from aletheia.verification.status import EpistemicStatus, Provisional

T = TypeVar("T")


@dataclass(frozen=True)
class TestProtocol:
    domain_description: str
    bound_description: str
    normalization: str
    null_model: str | None = None
    seed: int | None = None


@dataclass(frozen=True)
class Counterexample(Generic[T]):
    witness: T
    explanation: str
    checked: bool
    complexity: int = 0


@dataclass(frozen=True)
class Conjecture(Generic[T]):
    identifier: str
    statement: str
    predicate: Callable[[T], bool] = field(repr=False, compare=False)
    protocol: TestProtocol
    hypotheses: tuple[str, ...] = ()
    reference: str | None = None

    def test(self, values: Iterable[T]) -> Provisional[dict[str, object]]:
        tested = 0
        counterexamples: list[Counterexample[T]] = []
        for value in values:
            tested += 1
            try:
                valid = bool(self.predicate(value))
            except Exception as error:
                counterexamples.append(
                    Counterexample(value, f"predicate failed: {error}", False)
                )
                continue
            if not valid:
                counterexamples.append(
                    Counterexample(value, "exact predicate returned false", True)
                )
        report = {
            "identifier": self.identifier,
            "tested": tested,
            "survived": not counterexamples,
            "counterexamples": counterexamples,
            "protocol": self.protocol,
        }
        return Provisional(report, self.reference or self.identifier)


def minimize_integer_counterexample(
    witness: int, predicate: Callable[[int], bool]
) -> int:
    if predicate(witness):
        raise ValueError("provided value is not a counterexample")
    sign = -1 if witness < 0 else 1
    for magnitude in range(abs(witness)):
        candidate = sign * magnitude
        if not predicate(candidate):
            return candidate
    return witness
