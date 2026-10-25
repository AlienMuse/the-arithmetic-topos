# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""The Arithmetic Topos — Vincent Liu · WiseMotif.ai."""
from fractions import Fraction

from aletheia.automorphic.lfunction import (
    check_zeta_functional_equation, elliptic_curve_lfunction,
)
from aletheia.numerics.dirichlet import EulerProduct, zeta_euler_factor
from aletheia.numerics.lattice import lll_reduce
from aletheia.numerics.linalg import (
    kernel, kernel_mod_p, rref, smith_invariants, smith_normal_form,
)


def test_exact_linear_algebra() -> None:
    reduced, pivots = rref([[1, 2, 3], [2, 4, 6]])
    assert pivots == (0,)
    assert kernel([[1, 2, 3]]) == [
        [Fraction(-2), Fraction(1), Fraction(0)],
        [Fraction(-3), Fraction(0), Fraction(1)],
    ]
    assert kernel_mod_p([[1, 2]], 5) == [[3, 1]]
    assert smith_invariants([[2, 4], [4, 8]]) == (2,)
    assert smith_normal_form([[2, 4], [6, 8]]) == [[2, 0], [0, 4]]


def test_lll_known_basis() -> None:
    original = [[1, 1, 1], [-1, 0, 2], [3, 5, 6]]
    result = lll_reduce(original)
    assert result.basis == ((0, 1, 0), (1, 0, 1), (-1, 0, 2))
    assert result.swaps > 0


def test_euler_product_coefficients() -> None:
    coefficients = EulerProduct(zeta_euler_factor).coefficients(30)
    assert all(abs(coefficients[n] - 1) < 1e-12 for n in range(1, 31))


def test_zeta_completed_functional_equation() -> None:
    result = check_zeta_functional_equation(0.37 + 2.5j, terms=400)
    assert result.relative_error < 1e-9


def test_elliptic_curve_coefficients_and_fe() -> None:
    function = elliptic_curve_lfunction("11a1", 200)
    assert int(function.coefficients[2].real) == -2
    assert int(function.coefficients[3].real) == -1
    check = function.check_functional_equation(0.8 + 1.1j, terms=200)
    assert check.relative_error < 1e-12
