# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""Package version for the reference implementation.

Treatise correspondence: see Appendix G of the book (The Reference Implementation).
Genuine computation: semantic version parsing. Interface-only: none.
"""
from __future__ import annotations

__version__ = "0.1.0"
VERSION = tuple(int(part) for part in __version__.split("."))
