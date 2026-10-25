# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""Command-line interface for the reference implementation.

Treatise correspondence: see Appendix G of the book (The Reference Implementation).
Genuine computation: root duals, defects, finite L-function diagnostics,
ledger verification, roadmap status propagation, and integrated self-checks.
Interface-only: CLI output is evidence, never a proof-kernel verdict.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import json
from pathlib import Path
import tempfile
from typing import Sequence

from aletheia.automorphic.lfunction import (
    check_zeta_functional_equation, elliptic_curve_lfunction,
)
from aletheia.automorphic.satake import SatakeParameter
from aletheia.discovery.corpus import Statement, StatementCorpus
from aletheia.galois.defect import defect
from aletheia.galois.lgroup import RootDatum
from aletheia.numerics.lattice import lll_reduce
from aletheia.numerics.linalg import smith_normal_form
from aletheia.padic.newton import hodge_newton_decomposition
from aletheia.verification.ledger import EvidenceLedger
from aletheia.verification.status import EpistemicStatus
from aletheia.version import __version__


def default_ledger_path() -> Path:
    return Path.cwd() / ".aletheia" / "evidence.jsonl"


def build_roadmap() -> StatementCorpus:
    corpus = StatementCorpus()
    corpus.add(Statement(
        "finite-kernels", "Certified finite kernels",
        "Exact algebra and canonical certificates",
        EpistemicStatus.THEOREM,
    ))
    corpus.add(Statement(
        "six-functor", "Restricted six-functor formalisms",
        "Construct six operations in controlled settings",
        EpistemicStatus.DESIGN, ("finite-kernels",),
    ))
    corpus.add(Statement(
        "arithmetic-base", "Arithmetic gauge base",
        "Construct the global Lambda-twistor base",
        EpistemicStatus.CONJECTURE, ("six-functor",),
    ))
    corpus.add(Statement(
        "categorical-reciprocity", "Categorical arithmetic reciprocity",
        "Automorphic and spectral category equivalence",
        EpistemicStatus.CONJECTURE, ("arithmetic-base",),
    ))
    corpus.add(Statement(
        "trace-resolution", "Trace-theoretic resolution",
        "Recover classical reciprocity from categorical trace",
        EpistemicStatus.DESIGN, ("categorical-reciprocity",),
    ))
    return corpus


def command_status(_: argparse.Namespace) -> int:
    print(f"Aletheia-LDE {__version__}")
    print("Constitution: only a proof-assistant kernel confers [F] status.")
    print("Badges: [F] formal, [T] certified, [E] established, [D] design, [C] conjecture")
    return 0


def command_defect(args: argparse.Namespace) -> int:
    result = defect(args.group, args.field)
    print(f"group={result.group.label} field={result.field.name}")
    print(
        f"l_0={result.l0} "
        f"(real={result.real_contribution}, complex={result.complex_contribution})"
    )
    print("classical Taylor–Wiles case" if result.classical_taylor_wiles
          else "derived patching required")
    return 0


def command_dual(args: argparse.Namespace) -> int:
    datum = RootDatum.parse(args.type)
    dual = datum.dual()
    print(f"{datum.name} -> {dual.name}")
    print("Cartan:")
    for row in dual.cartan:
        print(" ".join(f"{value:2d}" for value in row))
    print(f"duality involution: {datum.duality_involution_holds()}")
    return 0


def command_lfunction(args: argparse.Namespace) -> int:
    function = elliptic_curve_lfunction(args.curve, args.terms)
    point = complex(args.real, args.imag)
    check = function.check_functional_equation(point, terms=args.terms)
    coefficients = function.coefficients
    print(function.name)
    print(f"conductor={function.conductor} root_number={function.root_number}")
    print(f"a_1..a_10={[int(coefficients[i].real) for i in range(1, min(11, len(coefficients)))]}")
    print(f"functional-equation relative error={check.relative_error:.3e}")
    print(f"passed={check.passed}; assumptions={'; '.join(check.assumptions)}")
    return 0 if check.passed else 1


def command_ledger(args: argparse.Namespace) -> int:
    ledger = EvidenceLedger(args.path)
    try:
        ledger.verify_chain()
    except Exception as error:
        print(f"INVALID: {error}")
        return 1
    print(f"OK entries={len(list(ledger.entries()))} head={ledger.head()}")
    return 0


def command_roadmap(_: argparse.Namespace) -> int:
    corpus = build_roadmap()
    for item in corpus.roadmap():
        print(
            f"[{item['effective']}] {item['id']}: {item['title']} "
            f"(impact={item['impact']}, deps={','.join(item['blocked_by']) or '-'})"
        )
    return 0


def command_selfcheck(_: argparse.Namespace) -> int:
    checks: list[tuple[str, bool, str]] = []
    root = RootDatum.parse("B3")
    checks.append(("root duality", root.dual().name == "C3"
                   and root.duality_involution_holds(), "B3 <-> C3"))
    satake = SatakeParameter((2 + 0j, 3 + 0j), 5)
    checks.append(("Satake conversion", satake.hecke_eigenvalues() == (5 + 0j, 6 + 0j),
                   "elementary symmetric values"))
    hn = hodge_newton_decomposition((Fraction(0), Fraction(1)), (0, 1))
    checks.append(("Hodge–Newton", hn.admissible, hn.explanation))
    checks.append(("defect", defect("GL2", "Q").l0 == 0
                   and defect("GL2", "Q(i)").l0 == 1, "Q=0, Q(i)=1"))
    checks.append(("Smith form", smith_normal_form([[2, 4], [4, 8]]) == [[2, 0], [0, 0]],
                   "determinantal divisors"))
    reduced = lll_reduce([[1, 1, 1], [-1, 0, 2], [3, 5, 6]])
    checks.append(("LLL", len(reduced.basis) == 3, f"swaps={reduced.swaps}"))
    zeta_check = check_zeta_functional_equation(0.37 + 3.0j, terms=300)
    checks.append(("zeta functional equation", zeta_check.relative_error < 1e-8,
                   f"error={zeta_check.relative_error:.2e}"))
    ledger_path = Path.cwd() / ".aletheia" / "selfcheck-ledger.jsonl"
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    ledger_path.unlink(missing_ok=True)
    ledger = EvidenceLedger(ledger_path)
    ledger.append("selfcheck-root", EpistemicStatus.THEOREM, {"ok": True})
    ledger.append(
        "selfcheck-chain", EpistemicStatus.THEOREM, {"ok": True},
        ("selfcheck-root",),
    )
    checks.append(("evidence ledger", ledger.verify_chain(), ledger.head()[:12]))
    ledger_path.unlink(missing_ok=True)
    for name, passed, detail in checks:
        print(f"{'PASS' if passed else 'FAIL'} {name}: {detail}")
    passed_count = sum(passed for _, passed, _ in checks)
    print(f"{passed_count}/{len(checks)} checks passed")
    return 0 if passed_count == len(checks) else 1


def parser() -> argparse.ArgumentParser:
    output = argparse.ArgumentParser(prog="aletheia")
    sub = output.add_subparsers(dest="command", required=True)
    status_parser = sub.add_parser("status")
    status_parser.set_defaults(func=command_status)
    defect_parser = sub.add_parser("defect")
    defect_parser.add_argument("--group", required=True)
    defect_parser.add_argument("--field", required=True)
    defect_parser.set_defaults(func=command_defect)
    dual_parser = sub.add_parser("dual")
    dual_parser.add_argument("--type", required=True)
    dual_parser.set_defaults(func=command_dual)
    lf_parser = sub.add_parser("lfunction")
    lf_parser.add_argument("--curve", required=True)
    lf_parser.add_argument("--terms", type=int, default=200)
    lf_parser.add_argument("--real", type=float, default=0.8)
    lf_parser.add_argument("--imag", type=float, default=1.2)
    lf_parser.set_defaults(func=command_lfunction)
    ledger_parser = sub.add_parser("ledger")
    ledger_sub = ledger_parser.add_subparsers(dest="ledger_command", required=True)
    verify_parser = ledger_sub.add_parser("verify")
    verify_parser.add_argument("--path", type=Path, default=default_ledger_path())
    verify_parser.set_defaults(func=command_ledger)
    roadmap_parser = sub.add_parser("roadmap")
    roadmap_parser.set_defaults(func=command_roadmap)
    selfcheck_parser = sub.add_parser("selfcheck")
    selfcheck_parser.set_defaults(func=command_selfcheck)
    return output


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    return int(args.func(args))
