# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""Aletheia-LDE orchestration loop.

Treatise correspondence: see Appendix G of the book (The Reference Implementation).
Genuine computation: state transitions, status propagation, bounded
counterexample runs, ranking, and ledger publication.
Interface-only: neural generation and human semantic review are callbacks.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Callable, Iterable

from aletheia.verification.ledger import EvidenceLedger
from aletheia.verification.status import EpistemicStatus
from .conjecture import Conjecture
from .corpus import Statement, StatementCorpus


class CandidateState(str, Enum):
    PROPOSED = "proposed"
    FALSIFICATION = "falsification"
    SEMANTIC_REVIEW = "semantic-review"
    PROOF_SEARCH = "proof-search"
    CERTIFIED = "certified"
    CONJECTURAL = "conjectural"
    REFUTED = "refuted"


@dataclass
class CandidateRecord:
    identifier: str
    state: CandidateState
    history: list[tuple[str, str]] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)

    def transition(self, state: CandidateState, note: str) -> None:
        allowed = {
            CandidateState.PROPOSED: {CandidateState.FALSIFICATION},
            CandidateState.FALSIFICATION: {
                CandidateState.REFUTED, CandidateState.SEMANTIC_REVIEW,
            },
            CandidateState.SEMANTIC_REVIEW: {
                CandidateState.PROOF_SEARCH, CandidateState.CONJECTURAL,
            },
            CandidateState.PROOF_SEARCH: {
                CandidateState.CERTIFIED, CandidateState.CONJECTURAL,
            },
            CandidateState.CERTIFIED: set(),
            CandidateState.CONJECTURAL: {CandidateState.FALSIFICATION},
            CandidateState.REFUTED: set(),
        }
        if state not in allowed[self.state]:
            raise ValueError(f"invalid transition {self.state} -> {state}")
        self.state = state
        self.history.append((datetime.now(timezone.utc).isoformat(), note))


@dataclass
class DiscoveryEngine:
    corpus: StatementCorpus
    ledger: EvidenceLedger
    candidates: dict[str, CandidateRecord] = field(default_factory=dict)

    @classmethod
    def at_path(cls, ledger_path: str | Path) -> "DiscoveryEngine":
        return cls(StatementCorpus(), EvidenceLedger(ledger_path))

    def register(self, conjecture: Conjecture[object]) -> CandidateRecord:
        if conjecture.identifier in self.candidates:
            raise ValueError("candidate identifier already exists")
        record = CandidateRecord(conjecture.identifier, CandidateState.PROPOSED)
        record.history.append((
            datetime.now(timezone.utc).isoformat(), "typed conjecture registered"
        ))
        self.candidates[conjecture.identifier] = record
        return record

    def falsify(
        self, conjecture: Conjecture[object], domain: Iterable[object]
    ) -> CandidateRecord:
        record = self.candidates.get(conjecture.identifier) or self.register(conjecture)
        if record.state == CandidateState.PROPOSED:
            record.transition(CandidateState.FALSIFICATION, "bounded exact search started")
        report = conjecture.test(domain).acknowledge(reason="registered falsification run")
        if report["survived"]:
            record.transition(
                CandidateState.SEMANTIC_REVIEW,
                f"survived {report['tested']} registered cases",
            )
        else:
            record.transition(
                CandidateState.REFUTED,
                f"found {len(report['counterexamples'])} counterexamples",
            )
        return record

    def semantic_review(
        self, identifier: str, source_agrees: bool, backtranslation_agrees: bool
    ) -> CandidateRecord:
        record = self.candidates[identifier]
        if record.state != CandidateState.SEMANTIC_REVIEW:
            raise ValueError("candidate is not awaiting semantic review")
        if source_agrees and backtranslation_agrees:
            record.transition(CandidateState.PROOF_SEARCH, "dual semantic review passed")
        else:
            record.transition(CandidateState.CONJECTURAL, "semantic review incomplete")
        return record

    def publish(
        self,
        identifier: str,
        statement: str,
        proof_checked: bool,
        dependencies: tuple[str, ...] = (),
    ) -> Statement:
        record = self.candidates[identifier]
        if record.state != CandidateState.PROOF_SEARCH:
            raise ValueError("candidate is not in proof search")
        status = (
            EpistemicStatus.FORMAL if proof_checked else EpistemicStatus.CONJECTURE
        )
        terminal = (
            CandidateState.CERTIFIED if proof_checked else CandidateState.CONJECTURAL
        )
        record.transition(terminal, "kernel replay passed" if proof_checked
                          else "proof search ended without kernel proof")
        node = Statement(identifier, identifier, statement, status, dependencies)
        self.corpus.add(node)
        self.ledger.append(
            identifier, status,
            {"statement": statement, "state": record.state.value},
            dependencies,
        )
        return node

    def selfcheck(self) -> dict[str, object]:
        return {
            "corpus_valid": self.corpus.validate(),
            "ledger_valid": self.ledger.verify_chain(),
            "candidates": len(self.candidates),
            "statements": len(self.corpus.statements),
        }
