# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""Layer 8 discovery interfaces.

Treatise correspondence: see Appendix G of the book (The Reference Implementation).
Genuine computation: DAGs, bounded falsification, fair search, ranking.
Interface-only: AI proposals have no authority and remain provisional.
"""
from __future__ import annotations

from .corpus import DependencyCycleError, Statement, StatementCorpus
from .engine import DiscoveryEngine

__all__ = ["DependencyCycleError", "DiscoveryEngine", "Statement", "StatementCorpus"]
