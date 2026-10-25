# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""Reproducibility and provenance records.

Treatise correspondence: see Appendix G of the book (The Reference Implementation).
Genuine computation: file/environment hashes and deterministic manifests.
Interface-only: container signing and independent hardware replay.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
from typing import Iterable


def hash_file(path: str | Path) -> str:
    digest = sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


@dataclass(frozen=True)
class Provenance:
    operation: str
    inputs: tuple[str, ...] = ()
    code_hash: str = ""
    environment_hash: str = ""
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    notes: tuple[str, ...] = ()

    def canonical_hash(self) -> str:
        encoded = json.dumps(asdict(self), sort_keys=True, separators=(",", ":"))
        return sha256(encoded.encode()).hexdigest()


def environment_manifest() -> dict[str, str]:
    return {
        "python": sys.version.split()[0],
        "implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "executable": str(Path(sys.executable).resolve()),
        "hash_seed": os.environ.get("PYTHONHASHSEED", "random"),
    }


def environment_hash() -> str:
    data = json.dumps(environment_manifest(), sort_keys=True).encode()
    return sha256(data).hexdigest()


def tree_hash(paths: Iterable[str | Path]) -> str:
    digest = sha256()
    for path in sorted((Path(item) for item in paths), key=lambda p: str(p)):
        digest.update(str(path).encode())
        digest.update(hash_file(path).encode())
    return digest.hexdigest()


def git_revision(cwd: str | Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=cwd, check=True,
            capture_output=True, text=True, timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return result.stdout.strip() or None
