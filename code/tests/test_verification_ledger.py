# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""The Arithmetic Topos — Vincent Liu · WiseMotif.ai."""
import json

import pytest

from aletheia.core.errors import ProvisionalUnwrapError, VerificationError
from aletheia.verification.ledger import EvidenceLedger
from aletheia.verification.status import EpistemicStatus, Provisional


def test_status_lattice_and_provisional() -> None:
    E, T, C = (
        EpistemicStatus.ESTABLISHED,
        EpistemicStatus.THEOREM,
        EpistemicStatus.CONJECTURE,
    )
    assert E.compose(C) is C
    assert T.compose(C) is C
    assert T.meet(E) is E
    assert T.join(E) is T
    with pytest.raises(ProvisionalUnwrapError):
        Provisional(3, "Conjecture X").unwrap()
    assert Provisional(3, "Conjecture X").acknowledge(reason="finite test") == 3


def test_ledger_append_replay_and_tamper_detection(tmp_path) -> None:
    path = tmp_path / "ledger.jsonl"
    ledger = EvidenceLedger(path)
    first = ledger.append("a", EpistemicStatus.ESTABLISHED, {"value": 1})
    ledger.append("b", EpistemicStatus.THEOREM, {"value": 2}, ("a",))
    assert ledger.verify_chain()
    assert [item["claim_id"] for item in ledger.replay()] == ["a", "b"]
    lines = path.read_text(encoding="utf-8").splitlines()
    record = json.loads(lines[0])
    record["payload"]["value"] = 99
    lines[0] = json.dumps(record)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    with pytest.raises(VerificationError):
        ledger.verify_chain()
