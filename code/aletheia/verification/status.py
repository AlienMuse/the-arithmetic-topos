# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""Epistemic status algebra and conjectural-value discipline.

Treatise correspondence: see Appendix G of the book (The Reference Implementation).
Genuine computation: a conservative status lattice and decorators.
Interface-only: statuses record evidence; only an external Lean kernel can
confer FORMAL status on mathematical propositions.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from functools import wraps
from typing import Any, Callable, Generic, ParamSpec, TypeVar, cast

from aletheia.core.errors import ProvisionalUnwrapError

T = TypeVar("T")
P = ParamSpec("P")


class EpistemicStatus(str, Enum):
    """The five badges used by the reference corpus.

    ``F`` is kernel-formal, ``T`` is theorem/certified computation,
    ``E`` is established external mathematics, ``D`` is design/interface,
    and ``C`` is conjectural.  Dependency composition is conservative.
    """

    FORMAL = "F"
    THEOREM = "T"
    ESTABLISHED = "E"
    DESIGN = "D"
    CONJECTURE = "C"

    @property
    def label(self) -> str:
        return {
            self.FORMAL: "kernel checked",
            self.THEOREM: "certified theorem/computation",
            self.ESTABLISHED: "externally established",
            self.DESIGN: "design/interface",
            self.CONJECTURE: "conjectural",
        }[self]

    @property
    def strength(self) -> int:
        return {
            self.CONJECTURE: 0,
            self.DESIGN: 1,
            self.ESTABLISHED: 2,
            self.THEOREM: 3,
            self.FORMAL: 4,
        }[self]

    def compose(self, *dependencies: "EpistemicStatus") -> "EpistemicStatus":
        """Return the weakest status in a dependency chain.

        Thus ``E ⊗ C = C`` and a theorem depending on a conjecture is
        downgraded to conjectural.  The operation is associative,
        commutative, and idempotent.
        """

        statuses = (self, *dependencies)
        return min(statuses, key=lambda value: value.strength)

    def meet(self, other: "EpistemicStatus") -> "EpistemicStatus":
        return self.compose(other)

    def join(self, other: "EpistemicStatus") -> "EpistemicStatus":
        return max((self, other), key=lambda value: value.strength)


@dataclass(frozen=True)
class Provisional(Generic[T]):
    """A value which cannot be used without explicit epistemic acknowledgement."""

    value: T = field(repr=False)
    reference: str
    status: EpistemicStatus = EpistemicStatus.CONJECTURE
    assumptions: tuple[str, ...] = ()

    def unwrap(self) -> T:
        """Refuse silent promotion to an ordinary value."""

        raise ProvisionalUnwrapError(
            f"{self.reference} has status [{self.status.value}]; "
            "use acknowledge() and record the dependency"
        )

    def acknowledge(self, *, reason: str) -> T:
        """Explicitly access the payload for experiments, never certification."""

        if not reason.strip():
            raise ValueError("an explicit experimental reason is required")
        return self.value

    def map(self, function: Callable[[T], Any]) -> "Provisional[Any]":
        return Provisional(
            function(self.value), self.reference, self.status, self.assumptions
        )


def conjectural(*, reference: str) -> Callable[[Callable[P, T]], Callable[P, Provisional[T]]]:
    """Mark a conjectural construction and wrap every returned value."""

    if not reference.strip():
        raise ValueError("a conjectural construction requires a reference")

    def decorate(function: Callable[P, T]) -> Callable[P, Provisional[T]]:
        @wraps(function)
        def wrapped(*args: P.args, **kwargs: P.kwargs) -> Provisional[T]:
            return Provisional(function(*args, **kwargs), reference)

        setattr(wrapped, "__aletheia_status__", EpistemicStatus.CONJECTURE)
        setattr(wrapped, "__aletheia_reference__", reference)
        return cast(Callable[P, Provisional[T]], wrapped)

    return decorate


def status_of(value: object) -> EpistemicStatus:
    if isinstance(value, Provisional):
        return value.status
    return cast(
        EpistemicStatus,
        getattr(value, "__aletheia_status__", EpistemicStatus.DESIGN),
    )


def compose_statuses(statuses: list[EpistemicStatus]) -> EpistemicStatus:
    if not statuses:
        return EpistemicStatus.FORMAL
    result = statuses[0]
    for status in statuses[1:]:
        result = result.compose(status)
    return result
