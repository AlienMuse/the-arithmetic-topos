# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""Module entry point.

Treatise correspondence: see Appendix G of the book (The Reference Implementation).
Genuine computation: dispatch to the command-line implementation.
Interface-only: none.
"""
from __future__ import annotations

from .cli import main

raise SystemExit(main())
