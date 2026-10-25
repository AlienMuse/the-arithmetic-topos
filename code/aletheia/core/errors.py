# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""Domain-specific failures.

Treatise correspondence: see Appendix G of the book (The Reference Implementation).
Genuine computation: structured failures with missing-input metadata.
Interface-only: exception messages describe unavailable mathematics.
"""
from __future__ import annotations

from dataclasses import dataclass


class AletheiaError(Exception):
    """Base class for all package errors."""


@dataclass(frozen=True)
class MissingMathematicalInput:
    """A precise description of an unavailable theorem or construction."""

    object_name: str
    requirement: str
    reference: str | None = None

    def explain(self) -> str:
        suffix = f" ({self.reference})" if self.reference else ""
        return f"{self.object_name}: requires {self.requirement}{suffix}"


class NotYetImplemented(AletheiaError):
    """Raised when a finite model is impossible without new mathematics."""

    def __init__(self, missing: MissingMathematicalInput | str) -> None:
        self.missing = (
            missing if isinstance(missing, MissingMathematicalInput)
            else MissingMathematicalInput("construction", missing)
        )
        super().__init__(self.missing.explain())


class VerificationError(AletheiaError):
    """A certificate or hash chain did not verify."""


class ProvisionalUnwrapError(AletheiaError):
    """Attempted to erase conjectural status."""


class PrecisionLossError(AletheiaError):
    """The requested precision cannot be certified."""


class MathematicalDomainError(AletheiaError, ValueError):
    """Inputs violate the mathematical domain of an algorithm."""
