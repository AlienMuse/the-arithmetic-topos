# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""Exact and guarded numerical kernels.

Treatise correspondence: see Appendix G of the book (The Reference Implementation).
Genuine computation: rational/modular algebra, LLL, series arithmetic.
Interface-only: optional accelerated libraries are never trusted as proofs.
"""
from __future__ import annotations

from .lattice import LLLResult, integer_relation, lll_reduce
from .linalg import kernel, kernel_mod_p, rref, rref_mod_p, smith_normal_form

__all__ = [
    "LLLResult", "integer_relation", "kernel", "kernel_mod_p", "lll_reduce",
    "rref", "rref_mod_p", "smith_normal_form",
]
