# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""Finite certificate types and independent verification.

Treatise correspondence: see Appendix G of the book (The Reference Implementation).
Genuine computation: canonical JSON hashing, equality/range/matrix checks.
Interface-only: proof-assistant certificates are delegated to lean_bridge.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass
from fractions import Fraction
from hashlib import sha256
import json
from typing import Any, Callable, Generic, Mapping, Protocol, TypeVar

from aletheia.core.errors import VerificationError

T = TypeVar("T")


def canonicalize(value: Any) -> Any:
    if is_dataclass(value):
        return canonicalize(asdict(value))
    if isinstance(value, Fraction):
        return {"numerator": value.numerator, "denominator": value.denominator}
    if isinstance(value, Mapping):
        return {str(k): canonicalize(value[k]) for k in sorted(value, key=str)}
    if isinstance(value, (list, tuple)):
        return [canonicalize(item) for item in value]
    if isinstance(value, set):
        return sorted((canonicalize(item) for item in value), key=repr)
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return repr(value)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        canonicalize(value), sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def content_hash(value: Any) -> str:
    return sha256(canonical_bytes(value)).hexdigest()


class Checker(Protocol[T]):
    def verify(self, payload: T) -> bool:
        """Return whether the finite payload satisfies its specification."""


@dataclass(frozen=True)
class Certificate(Generic[T]):
    kind: str
    specification: str
    payload: T
    payload_hash: str
    checker: str

    @classmethod
    def issue(
        cls, kind: str, specification: str, payload: T, checker: str
    ) -> "Certificate[T]":
        return cls(kind, specification, payload, content_hash(payload), checker)

    def intact(self) -> bool:
        return self.payload_hash == content_hash(self.payload)

    def require_intact(self) -> None:
        if not self.intact():
            raise VerificationError(f"{self.kind} certificate payload was modified")


@dataclass(frozen=True)
class EqualityWitness:
    left: Any
    right: Any

    def verify(self) -> bool:
        return self.left == self.right


@dataclass(frozen=True)
class IntervalWitness:
    value: float
    lower: float
    upper: float

    def verify(self) -> bool:
        return self.lower <= self.value <= self.upper


@dataclass(frozen=True)
class MatrixProductWitness:
    left: tuple[tuple[int, ...], ...]
    right: tuple[tuple[int, ...], ...]
    product: tuple[tuple[int, ...], ...]

    def verify(self) -> bool:
        if not self.left or not self.right:
            return self.product == ()
        rows, inner, cols = len(self.left), len(self.right), len(self.right[0])
        if any(len(row) != inner for row in self.left):
            return False
        expected = tuple(
            tuple(sum(self.left[i][k] * self.right[k][j] for k in range(inner))
                  for j in range(cols))
            for i in range(rows)
        )
        return expected == self.product


def verify_certificate(
    certificate: Certificate[T], predicate: Callable[[T], bool]
) -> bool:
    certificate.require_intact()
    if not predicate(certificate.payload):
        raise VerificationError(
            f"checker {certificate.checker!r} rejected {certificate.specification}"
        )
    return True
