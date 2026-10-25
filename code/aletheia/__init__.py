# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""Aletheia-LDE reference implementation.

Treatise correspondence: see Appendix G of the book (The Reference Implementation).
Genuine computation: finite algebraic models and evidence handling.
Interface-only: general Langlands correspondences remain explicit protocols.
"""
from __future__ import annotations

from .version import VERSION, __version__
from .verification.status import EpistemicStatus, Provisional, conjectural

__all__ = ["VERSION", "__version__", "EpistemicStatus", "Provisional", "conjectural"]
