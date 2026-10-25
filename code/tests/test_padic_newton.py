# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""The Arithmetic Topos — Vincent Liu · WiseMotif.ai."""
from fractions import Fraction

from aletheia.padic.newton import (
    GLnSigmaConjugacyClass, NewtonPolygon, hodge_newton_decomposition,
    kottwitz_set_gl_n,
)


def test_newton_polygon_slopes() -> None:
    polygon = NewtonPolygon.from_coeff_valuations((0, 1, 1))
    assert polygon.slopes() == (Fraction(1, 2), Fraction(1, 2))


def test_kottwitz_class_and_hodge_newton() -> None:
    value = GLnSigmaConjugacyClass.from_slopes((0, 1))
    assert value.kottwitz_invariant == 1
    assert not value.is_basic
    assert value.acceptable_for_hodge((0, 1))
    result = hodge_newton_decomposition((0, 1), (0, 1))
    assert result.admissible


def test_bounded_kottwitz_enumeration() -> None:
    classes = kottwitz_set_gl_n(2, 1, 0, 1)
    assert any(item.slopes == (Fraction(0), Fraction(1)) for item in classes)
