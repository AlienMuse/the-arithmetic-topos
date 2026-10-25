# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""Layer 2 spectral/Galois models.

Treatise correspondence: see Appendix G of the book (The Reference Implementation).
Genuine computation: root data, finite cohomology dimensions, defects.
Interface-only: universal global Galois representations and derived stacks.
"""
from __future__ import annotations

from .lgroup import LGroup, RootDatum, langlands_dual

__all__ = ["LGroup", "RootDatum", "langlands_dual"]
