# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""Layers 0–1 foundational kernel interfaces.

Treatise correspondence: see Appendix G of the book (The Reference Implementation).
Genuine computation: finite categories, traces, weights, certificates.
Interface-only: the Lean kernel remains the sole formal authority.
"""
from __future__ import annotations

from .category import Arrow, Path, QuiverCategory
from .dualizable import DualizabilityCertificate
from .trace import LefschetzDatum, matrix_trace, supertrace
from .weights import WeightComplex, WeightedPiece

__all__ = [
    "Arrow", "DualizabilityCertificate", "LefschetzDatum", "Path",
    "QuiverCategory", "WeightComplex", "WeightedPiece", "matrix_trace",
    "supertrace",
]
