# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""Lean 4 statement emission and optional kernel invocation.

Treatise correspondence: see Appendix G of the book (The Reference Implementation).
Genuine computation: deterministic declaration emission, subprocess
invocation of `lake env lean`, output capture, and source hashing.
Interface-only: absent Lean installations return an unavailable result;
Python never promotes a statement to FORMAL by itself.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
import shutil
import subprocess
from typing import Iterable


@dataclass(frozen=True)
class LeanStatement:
    name: str
    proposition: str
    documentation: str
    status_marker: str = "F"

    def emit(self, *, sorry: bool = True) -> str:
        body = "by sorry" if sorry else ":= by trivial"
        return (
            f"/-- [{self.status_marker}] {self.documentation} -/\n"
            f"theorem {self.name} : {self.proposition} := {body.removeprefix(':= ')}\n"
        )


@dataclass(frozen=True)
class LeanCheckResult:
    available: bool
    success: bool
    command: tuple[str, ...]
    stdout: str
    stderr: str
    source_hash: str
    returncode: int | None


def emit_statements(
    statements: Iterable[LeanStatement], namespace: str = "ArithmeticTopos"
) -> str:
    declarations = "\n".join(statement.emit() for statement in statements)
    return (
        "# The Arithmetic Topos — Vincent Liu · WiseMotif.ai\n"
        f"namespace {namespace}\n\n{declarations}\nend {namespace}\n"
    )


def check_lean_file(path: str | Path, *, cwd: str | Path | None = None) -> LeanCheckResult:
    source = Path(path).read_bytes()
    digest = sha256(source).hexdigest()
    lake = shutil.which("lake")
    if lake is None:
        return LeanCheckResult(False, False, (), "", "lake not found", digest, None)
    command = (lake, "env", "lean", str(Path(path)))
    try:
        result = subprocess.run(
            command, cwd=cwd, capture_output=True, text=True, timeout=120
        )
    except (OSError, subprocess.SubprocessError) as error:
        return LeanCheckResult(True, False, command, "", str(error), digest, None)
    return LeanCheckResult(
        True, result.returncode == 0, command, result.stdout, result.stderr,
        digest, result.returncode,
    )
