# Companion code — The Arithmetic Topos

This is the code that accompanies *The Arithmetic Topos — Foundations of a Trace-Theoretic Approach to the Langlands Programme* (WiseMotif Monograph of Mathematical Intelligence, Series 07) (Research Architecture Edition 1, version 1.0.0), by Vincent Liu, licensed under the Apache
License 2.0 (`LICENSE`); the monograph itself is licensed under CC BY-NC-ND 4.0. Nothing here proves the Langlands
correspondence or any case of the book's Main Conjecture: the package implements the finite algorithms of the book
and marks every non-computable object as an interface (Appendix G of the book records what it does and does not do).

| folder | what it is | book |
|---|---|---|
| `aletheia/` | the reference implementation: finite kernels for traces and weights, Satake and Hecke data, Galois defect counts, Newton and Hodge polygons, orbital sums, certificates, the status lattice and the evidence ledger | Ch. 37–38, App. G |
| `tests/` | 21 tests | App. G |
| `lean/` | the Lean 4 statement skeleton: 33 `[F]` targets with `sorry` bodies; not compiled | Ch. 6, 37–38 |

## Reproduce

Python 3.10 or later; the package uses the standard library only (tested: Python 3.11.9). From this folder:

```sh
python -m pytest tests -q         # all 21 tests (pytest required)
```

`REPRODUCIBILITY.md` is the C-3 report of the final edition: the tests, the numerical verification scripts of
Chapters 27, 33 and 36, and the numbers the book prints compared with their output.

## Changes from the working tree

The files are the author's working tree, with the documentation edits listed in `CODE-EDITS.md` and an SPDX licence
header on every Python and Lean file. No line of program code is changed.

---

# The Arithmetic Topos — Reference Implementation

**Vincent Liu · WiseMotif.ai**

This directory contains the runnable Python reference system accompanying *The
Arithmetic Topos: Foundations of a Trace-Theoretic Approach to the Langlands
Programme*.  It is an engineering model of the interfaces, finite algorithms,
evidence discipline, and discovery workflow described in the book.  It is
not, and does not claim to be, an implementation of currently unknown
mathematics.  Whenever the treatise asks for a general derived stack, an
arithmetic six-functor formalism, a categorical Langlands equivalence, or a
number-field excursion construction, this package supplies a typed interface,
a finite walking example, or an explicit `NotYetImplemented` boundary.  It
never manufactures a theorem from numerical agreement.

## Architecture

The implementation compresses the polyglot design of Part VII of the book into a standard-library
Python reference kernel plus a Lean 4 statement skeleton:

```text
                         ┌──────────────────────────────┐
                         │ Layer 8  discovery/          │
                         │ conjecture, search, ranking  │
                         └──────────────┬───────────────┘
                                        │ provisional values
                         ┌──────────────▼───────────────┐
                         │ Layer 7  verification/       │
                         │ status, certificates, ledger │
                         └──────────────┬───────────────┘
                                        │ checked finite artifacts
              ┌─────────────────────────┼─────────────────────────┐
              │                         │                         │
   ┌──────────▼──────────┐   ┌──────────▼──────────┐   ┌─────────▼──────────┐
   │ Layer 6 trace_formula│   │ Layer 5 padic/      │   │ Layer 4 geometric/ │
   │ orbital, stable,     │   │ Newton, FF, prisms  │   │ Bun_G, shtukas     │
   │ Lefschetz, boundary  │   │ periods             │   │ spectral actions   │
   └──────────┬──────────┘   └──────────┬──────────┘   └─────────┬──────────┘
              │                         │                         │
              └──────────────┬──────────┴──────────────┬──────────┘
                             │                         │
                  ┌──────────▼──────────┐   ┌─────────▼──────────┐
                  │ Layer 3 automorphic/│   │ Layer 2 galois/    │
                  │ Hecke, Satake, L     │   │ deformation, l0    │
                  └──────────┬──────────┘   └─────────┬──────────┘
                             └────────────┬────────────┘
                                          │
                              ┌───────────▼───────────┐
                              │ Layers 0–1 core/      │
                              │ categories, 6FF, trace│
                              │ weights, dualizability│
                              └───────────┬───────────┘
                                          │ emits statements
                              ┌───────────▼───────────┐
                              │ lean/ArithmeticTopos  │
                              │ kernel-check boundary │
                              └───────────────────────┘
```

`numerics/` is a horizontal finite-computation layer used by every stratum.  It
contains exact rational and finite-field row reduction, kernels, determinant
utilities, Smith invariant factors over the integers, pure-Python LLL, formal
q-expansions, Euler-product expansion, and analytic diagnostics.  The core,
verification, and discovery packages use only the Python standard library.
Optional numerical libraries are not required.

## The eight layers

**Layer 0 — kernel sovereignty.**  In the full Aletheia-LDE architecture this
is the pinned Lean kernel and its axiom audit.  Python cannot emulate dependent
type theory and is not treated as a substitute.  `verification/lean_bridge.py`
emits deterministic declarations and invokes `lake env lean` only if a
toolchain exists.  The return record distinguishes “tool unavailable” from
“kernel accepted.”  The supplied Lean statements use `sorry` and are therefore
targets, not established facts.

**Layer 1 — Formal Éléments.**  `core/` models the interfaces that a future
formal library must refine: correspondence presentations, six operations,
duality certificates, primitive shadows, categorical traces, and Bondarko-style
weight complexes.  The implementations are finite.  A quiver presentation can
enumerate bounded paths and normalize relations; a finite six-functor table can
check properness, étaleness, and projection-formula samples; a finite complex
can compute a supertrace.  None of these finite objects is silently identified
with an infinity-category.

**Layer 2 — symbolic and arithmetic kernels.**  `galois/`, `padic/`, and
`numerics/` contain the exact finite calculations.  Root data cover classical
types A, B, C, D and G2.  Taking the dual transposes the Cartan matrix and
exchanges B and C; applying duality twice restores the original datum and
isogeny form.  Galois cochain complexes over finite fields compute actual
cohomology dimensions.  Deformation rings are finite truncated presentations
whose `universal` flag is false when infinitesimal automorphisms remain.
Newton polygons use rational slopes, and bounded windows in B(GL_n) are
enumerated rather than pretending that an infinite Kottwitz set was exhausted.

**Layer 3 — typed object store and spectral/automorphic records.**  The small
reference package keeps immutable dataclasses in memory instead of deploying
PostgreSQL and object storage.  Canonical JSON serialization and SHA-256
content addressing are nevertheless real.  Satake parameters for GL_n convert
to elementary-symmetric Hecke eigenvalues and local Euler polynomials.  GL1 and
GL2 inversion is supplied directly.  Finite Hecke operators can be checked for
commutativity and enumerated over F_p.  The corpus records statement identity,
dependencies, declared status, effective status, and semantic hashes.

**Layer 4 — geometric and categorical finite models.**  `geometric/` includes
stacky masses for finite Bun_G groupoids, HN strata, sheaf support metadata,
creation–action–annihilation excursion matrices, and finite spectral actions.
These are walking examples for the interfaces of Part III of the book.  They do not construct the
arithmetic Lambda-twistor base, arithmetic Ran space, IndCoh, or the categorical
arithmetic Langlands equivalence.

**Layer 5 — p-adic and period geometry.**  The package computes exact Newton
and Hodge polygons, Kottwitz invariants for GL_n slope classes, basicness,
dominance, and Hodge–Newton decomposition breaks.  Fargues–Fontaine bundles are
represented by their classified slope multisets, so dual and tensor operations
are exact combinatorics.  Truncated delta-rings and prismatic windows check
finite congruence identities and determinant conditions.  No finite matrix is
called “the prismatic cohomology” of a general space.

**Layer 6 — trace formula.**  `trace_formula/` assembles exact weighted orbital
cell sums, finite GL2 conjugacy orbits, transfer-factor matrices, stable sums,
fixed-point terms, and cyclic Poisson transforms.  An orbital answer carries
its omitted-tail radius.  A zero tail and certified exhaustive cells give an
exact finite result; otherwise the interval remains visible.  Stabilization,
Arthur truncation, and Braverman–Kazhdan transforms for arbitrary reductive
groups remain interfaces.

**Layer 7 — constitutional verification.**  This is the most important layer
for sound use.  The epistemic badges are `[F]` kernel formal, `[T]` theorem or
certified finite computation, `[E]` externally established, `[D]` design, and
`[C]` conjectural.  Dependency composition takes the weaker status: `[E]`
composed with `[C]` is `[C]`, and `[T]` depending on `[C]` is also `[C]`.
The `@conjectural(reference=...)` decorator wraps values in `Provisional`.
Calling `unwrap()` raises an exception; experiments must call
`acknowledge(reason=...)`, making the epistemic crossing explicit.

The evidence ledger is JSON Lines, append-only by API, content-addressed, and
hash-chained.  Every entry includes a payload hash, previous-entry hash,
dependencies, timestamp, and status.  `verify_chain()` recomputes all hashes,
checks sequence continuity, rejects reused claim identifiers, and verifies that
dependencies were already present.  Tests modify an earlier payload on disk
and confirm that replay fails.

**Layer 8 — discovery.**  The discovery engine supports typed conjectures,
registered bounded tests, explicit counterexamples, dual semantic review,
finite fair search, value-of-information ranking, analogy transfer, and
publication to the ledger.  A candidate can move through proposed,
falsification, semantic review, proof search, certified, conjectural, or
refuted states.  Majority vote and model confidence never create formal status.

## Constitutional separation of mathematical powers

The implementation separates four powers.  The **generator** may propose a
typed conjecture.  The **experimental kernel** may test finite cases and issue
replayable certificates.  The **review layer** may establish that a formal
sentence matches its source and conventions.  Only the **proof-assistant
kernel** may accept a proof term and confer `[F]`.  These powers cannot promote
one another.  A million matching Euler factors remain evidence; they become a
theorem only through a converse theorem, Chebotarev argument, or another proof
whose hypotheses are checked.

This design also enforces no approximation erasure.  Newton slopes, p-adic
precision, truncation degree, tail bounds, and finite prime ranges remain in
the returned objects.  A `Provisional[T]` is not a `T`, a truncated bar complex
is not an exact categorical trace without a tail-vanishing certificate, and a
finite deformation presentation is not universal unless representability
hypotheses are discharged.

## Install and run

Python 3.10 or newer is required.  From this `src` directory:

```powershell
python -m pip install -e .
python -m pip install pytest
python -m pytest tests
python -m aletheia status
python -m aletheia defect --group GL2 --field "Q(i)"
python -m aletheia dual --type B3
python -m aletheia lfunction --curve 11a1 --terms 200
python -m aletheia ledger verify
python -m aletheia roadmap
python -m aletheia selfcheck
```

The ledger command treats a missing ledger as a valid empty chain.  Application
code can append records with `EvidenceLedger.append`.  The package has no
runtime dependency outside the standard library.  Tests use pytest.

## Numerical examples

The zeta implementation uses the globally convergent Hasse transformation of
the eta series and a Lanczos complex gamma approximation.  The completed
function is checked at nontrivial complex points against
`Lambda(s)=Lambda(1-s)`.  The elliptic-curve example `11a1` computes `a_p`
directly by counting points on its integral Weierstrass equation, extends
coefficients by the good- and bad-prime recurrences, and evaluates a symmetric
exponentially smoothed approximate functional equation.  Its result explicitly
records that modularity and the functional equation are supplied mathematical
metadata, and that the sum is truncated; it is a diagnostic rather than a
rigorous Arb enclosure.

The pure-Python LLL routine uses exact `Fraction` Gram–Schmidt coefficients and
checks the Lovász condition.  Smith normal form is computed through
determinantal divisors, which is exact and robust for certificate-sized
matrices but exponential in matrix dimensions.  This deliberate choice favors
a small trustworthy reference implementation over misleading performance
claims.

## Limitations

The following major objects are interface-only: general presentable stable
infinity-categories; coherent six-functor formalisms; derived and analytic
stacks; the arithmetic gauge curve and Lambda-twistor base; the arithmetic Ran
stack; global arithmetic Bun_G; IndCoh and nilpotent singular support;
categorical arithmetic Langlands; the cyclotomic trace conjecture; THH/TC
computations; general Galois representations and absolute cochain complexes;
universal deformation rings beyond finite truncations; Emerton–Gee stacks;
diamonds and perfectoid descent; general B(G); p-adic Hodge comparison
isomorphisms; modular symbols outside the built-in finite records; Arthur
packets; full stabilization; analytic trace formulas; Braverman–Kazhdan/Ngo
transforms; number-field excursion operators; and autonomous proof discovery.

The Lean package is intentionally a skeleton.  `Statements.lean` contains
thirty-three `[F]` targets with `sorry` bodies, transcribed at statement-name
level from the book.  They are syntactically plausible declarations, not proofs
and not a substitute for mathlib foundations.  If Lean is installed,
`lean_bridge` can run it and preserve the output and source hash; if it is not
installed, the bridge reports that fact without pretending success.

This package should therefore be read as a constitutional reference
implementation: it makes the computable portions run, exposes complexity and
precision, and makes the noncomputable portions impossible to mistake for
facts.  That disciplined boundary is the central engineering claim of
Aletheia-LDE.

---

**The Arithmetic Topos — Reference Implementation**  
**Vincent Liu · WiseMotif.ai**
