# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""The Arithmetic Topos — Vincent Liu · WiseMotif.ai."""
from fractions import Fraction

from aletheia.core.category import Path, QuiverCategory
from aletheia.core.dualizable import FiniteVectorSpaceDual
from aletheia.core.trace import LefschetzDatum, Shadow, matrix_trace, supertrace
from aletheia.core.weights import WeightComplex, WeightedPiece


def test_trace_and_supertrace() -> None:
    assert matrix_trace([[1, 2], [3, 4]]) == 5
    assert supertrace({0: [[3]], 1: [[2]]}) == 1


def test_lefschetz_and_shadow() -> None:
    datum = LefschetzDatum({0: ((2 + 0j,),)}, (1 + 0j, 1 + 0j))
    assert datum.verifies_localization()
    shadow = Shadow(("a", "b"))
    assert shadow.class_of(("b", "a")) == ("a", "b")


def test_quiver_relations_and_duality() -> None:
    category = QuiverCategory()
    category.add_object("X")
    category.add_object("Y")
    category.add_arrow("f", "X", "Y")
    category.add_arrow("g", "Y", "X")
    category.add_relation(("f", "g"), ())
    paths = category.paths("X", "X", 2)
    assert any(path.length == 0 for path in paths)
    assert category.normalize_word(("f", "g")) == ()
    assert FiniteVectorSpaceDual(3).certificate().valid


def test_weights() -> None:
    complex_ = WeightComplex((
        WeightedPiece(0, 1, (1 + 0j,), True),
        WeightedPiece(2, 1, (4 + 0j,), True),
    ))
    assert complex_.virtual_rank == 0
    assert complex_.trace() == -3
