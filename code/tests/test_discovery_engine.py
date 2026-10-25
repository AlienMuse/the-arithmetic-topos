# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""The Arithmetic Topos — Vincent Liu · WiseMotif.ai."""
import pytest

from aletheia.discovery.corpus import (
    DependencyCycleError, Statement, StatementCorpus,
)
from aletheia.verification.status import EpistemicStatus


def sample_corpus() -> StatementCorpus:
    corpus = StatementCorpus()
    corpus.add(Statement("a", "A", "base", EpistemicStatus.ESTABLISHED))
    corpus.add(Statement("b", "B", "bridge", EpistemicStatus.CONJECTURE, ("a",)))
    corpus.add(Statement("c", "C", "result", EpistemicStatus.THEOREM, ("b",)))
    corpus.add(Statement("d", "D", "parallel", EpistemicStatus.DESIGN, ("a",)))
    return corpus


def test_topological_order_impact_and_status() -> None:
    corpus = sample_corpus()
    order = corpus.topological_order()
    assert order.index("a") < order.index("b") < order.index("c")
    assert corpus.what_breaks_if_false("b") == ("c",)
    assert set(corpus.what_breaks_if_false("a")) == {"b", "c", "d"}
    assert corpus.effective_status("c") is EpistemicStatus.CONJECTURE


def test_cycle_detection() -> None:
    corpus = sample_corpus()
    # Mutate only to test validator against imported/corrupt data.
    corpus.statements["a"] = Statement(
        "a", "A", "base", EpistemicStatus.ESTABLISHED, ("c",)
    )
    with pytest.raises(DependencyCycleError):
        corpus.topological_order()
