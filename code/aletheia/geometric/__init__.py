# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""Layer 4 geometric and categorical models.

Treatise correspondence: see Appendix G of the book (The Reference Implementation).
Genuine computation: finite groupoids, sheaf metadata, excursion matrices.
Interface-only: arithmetic Bun_G and categorical equivalences.
"""
from __future__ import annotations

from .bung import BundleClass, FiniteBunG
from .shtuka import ExcursionDatum, ExcursionOperator, ShtukaLeg

__all__ = ["BundleClass", "ExcursionDatum", "ExcursionOperator", "FiniteBunG", "ShtukaLeg"]
