# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""The Arithmetic Topos — Vincent Liu · WiseMotif.ai."""
from aletheia.automorphic.satake import (
    SatakeParameter, hecke_from_satake, satake_from_hecke_gl2,
)


def close_tuple(left, right, tolerance=1e-10):
    return all(abs(a - b) < tolerance for a, b in zip(left, right))


def test_gl2_satake_roundtrip() -> None:
    parameter = SatakeParameter((2 + 0j, 3 + 0j), 5)
    hecke = hecke_from_satake(parameter)
    assert close_tuple(hecke, (5, 6))
    recovered = satake_from_hecke_gl2(hecke[0], hecke[1], 5)
    assert close_tuple(sorted(recovered.eigenvalues, key=lambda z: z.real), (2, 3))


def test_euler_polynomial() -> None:
    parameter = SatakeParameter((1 + 1j, 1 - 1j), 7)
    assert close_tuple(parameter.standard_euler_polynomial(), (1, -2, 2))
    assert abs(parameter.central_character() - 2) < 1e-12
