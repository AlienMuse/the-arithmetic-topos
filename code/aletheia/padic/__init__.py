# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""Layer 5 p-adic geometry models.

Treatise correspondence: see Appendix G of the book (The Reference Implementation).
Genuine computation: Newton polygons, bounded B(GL_n), finite prisms.
Interface-only: general FF curves, diamonds, and global period stacks.
"""
from __future__ import annotations

from .newton import (
    GLnSigmaConjugacyClass, HodgeNewtonResult, NewtonPolygon,
    hodge_newton_decomposition, kottwitz_set_gl_n,
)

__all__ = [
    "GLnSigmaConjugacyClass", "HodgeNewtonResult", "NewtonPolygon",
    "hodge_newton_decomposition", "kottwitz_set_gl_n",
]
