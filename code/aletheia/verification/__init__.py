# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""Constitutional verification layer.

Treatise correspondence: see Appendix G of the book (The Reference Implementation).
Genuine computation: status, certificates, hashes, and ledgers.
Interface-only: Lean kernel checking depends on an installed toolchain.
"""
from __future__ import annotations

from .certificate import Certificate, content_hash, verify_certificate
from .ledger import EvidenceLedger, LedgerEntry
from .status import EpistemicStatus, Provisional, conjectural

__all__ = [
    "Certificate", "EvidenceLedger", "EpistemicStatus", "LedgerEntry",
    "Provisional", "conjectural", "content_hash", "verify_certificate",
]
