# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""Append-only, content-addressed evidence ledger.

Treatise correspondence: see Appendix G of the book (The Reference Implementation).
Genuine computation: SHA-256 hash chaining, replay, tamper detection.
Interface-only: multi-party signatures and immutable remote object storage.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Iterable, Iterator

from aletheia.core.errors import VerificationError
from .certificate import canonical_bytes, content_hash
from .status import EpistemicStatus

GENESIS = "0" * 64


@dataclass(frozen=True)
class LedgerEntry:
    sequence: int
    timestamp: str
    claim_id: str
    status: str
    payload: Any
    payload_hash: str
    dependencies: tuple[str, ...]
    previous_hash: str
    entry_hash: str

    def body(self) -> dict[str, Any]:
        data = asdict(self)
        data.pop("entry_hash")
        return data

    def recompute_hash(self) -> str:
        return sha256(canonical_bytes(self.body())).hexdigest()

    def verify(self) -> bool:
        return (
            self.payload_hash == content_hash(self.payload)
            and self.entry_hash == self.recompute_hash()
        )


class EvidenceLedger:
    """A JSON-lines ledger whose records form a cryptographic hash chain."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def entries(self) -> Iterator[LedgerEntry]:
        if not self.path.exists():
            return
        with self.path.open("r", encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                if not line.strip():
                    continue
                try:
                    raw = json.loads(line)
                    raw["dependencies"] = tuple(raw.get("dependencies", ()))
                    yield LedgerEntry(**raw)
                except (json.JSONDecodeError, TypeError) as error:
                    raise VerificationError(
                        f"invalid ledger record at line {line_number}: {error}"
                    ) from error

    def append(
        self,
        claim_id: str,
        status: EpistemicStatus,
        payload: Any,
        dependencies: Iterable[str] = (),
        *,
        timestamp: str | None = None,
    ) -> LedgerEntry:
        current = list(self.entries())
        previous = current[-1].entry_hash if current else GENESIS
        body = {
            "sequence": len(current),
            "timestamp": timestamp or datetime.now(timezone.utc).isoformat(),
            "claim_id": claim_id,
            "status": status.value,
            "payload": payload,
            "payload_hash": content_hash(payload),
            "dependencies": tuple(dependencies),
            "previous_hash": previous,
        }
        entry_hash = sha256(canonical_bytes(body)).hexdigest()
        entry = LedgerEntry(**body, entry_hash=entry_hash)
        with self.path.open("a", encoding="utf-8", newline="\n") as stream:
            stream.write(json.dumps(asdict(entry), sort_keys=True, ensure_ascii=False))
            stream.write("\n")
            stream.flush()
        return entry

    def verify_chain(self, *, require_dependencies: bool = True) -> bool:
        previous = GENESIS
        known: set[str] = set()
        expected_sequence = 0
        for entry in self.entries():
            if entry.sequence != expected_sequence:
                raise VerificationError("ledger sequence is not contiguous")
            if entry.previous_hash != previous:
                raise VerificationError(
                    f"broken previous hash at sequence {entry.sequence}"
                )
            if not entry.verify():
                raise VerificationError(
                    f"tampered content at sequence {entry.sequence}"
                )
            if entry.claim_id in known:
                raise VerificationError(f"claim id {entry.claim_id!r} was reused")
            if require_dependencies:
                missing = set(entry.dependencies) - known
                if missing:
                    raise VerificationError(
                        f"claim {entry.claim_id!r} has unknown dependencies {missing}"
                    )
            known.add(entry.claim_id)
            previous = entry.entry_hash
            expected_sequence += 1
        return True

    def replay(self) -> list[dict[str, Any]]:
        self.verify_chain()
        return [
            {
                "claim_id": entry.claim_id,
                "status": EpistemicStatus(entry.status),
                "payload": entry.payload,
                "dependencies": entry.dependencies,
            }
            for entry in self.entries()
        ]

    def head(self) -> str:
        entries = list(self.entries())
        return entries[-1].entry_hash if entries else GENESIS
