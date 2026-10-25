# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""The Arithmetic Topos — Vincent Liu · WiseMotif.ai."""
from aletheia.galois.cohomology import FiniteCochainComplex, NumberFieldSignature
from aletheia.galois.defect import defect
from aletheia.galois.lgroup import RootDatum, langlands_dual


def test_classical_root_duality_and_involution() -> None:
    expected = {"A3": "A3", "B3": "C3", "C3": "B3", "D4": "D4", "G2": "G2"}
    for source, target in expected.items():
        datum = RootDatum.parse(source)
        assert datum.dual().name == target
        assert datum.duality_involution_holds()
        assert datum.dual().cartan == tuple(zip(*datum.cartan))


def test_defect_taylor_wiles_and_bianchi() -> None:
    assert defect("GL2", "Q").l0 == 0
    assert defect("GL2", "Q").classical_taylor_wiles
    assert defect("GL2", "Q(i)").l0 == 1
    assert defect("GL3", "Q").l0 == 1
    assert defect("Sp4", "Q").l0 == 0


def test_finite_cohomology_euler_characteristic() -> None:
    complex_ = FiniteCochainComplex(
        (2, 2),
        ((((1, 0), (0, 0))),),
        5,
    )
    assert complex_.cohomology_dimensions() == (1, 1)
    assert complex_.verifies_euler_principle()
    assert NumberFieldSignature.parse("Q(i)").complex_places == 1
