# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""Layer 6 trace-formula models.

Treatise correspondence: see Appendix G of the book (The Reference Implementation).
Genuine computation: finite orbital sums, transfer matrices, indices.
Interface-only: stabilization and beyond endoscopy in general.
"""
from __future__ import annotations

from .lefschetz import FixedPointContribution, LefschetzIndex
from .orbital import OrbitalCell, OrbitalIntegralResult, orbital_integral_cells

__all__ = [
    "FixedPointContribution", "LefschetzIndex", "OrbitalCell",
    "OrbitalIntegralResult", "orbital_integral_cells",
]
