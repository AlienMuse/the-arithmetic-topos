# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""Layer 3 automorphic models.

Treatise correspondence: see Appendix G of the book (The Reference Implementation).
Genuine computation: finite Hecke modules, Satake parameters, Euler factors.
Interface-only: full automorphic representations and packet classification.
"""
from __future__ import annotations

from .satake import SatakeParameter, hecke_from_satake, satake_from_hecke

__all__ = ["SatakeParameter", "hecke_from_satake", "satake_from_hecke"]
