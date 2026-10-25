# Documentation edits in the published copy of the companion code

Applied by `release-kit/scripts/s04c_numerics.py` to the archived copy; the author's working tree is unchanged. No line of program code is changed: module docstrings, comments, the package metadata and the README only.

Every Python and Lean file (68) begins with the two lines

```
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
```

(as `--` comments in Lean). The design documents of the writing (A1–A6) that the docstrings and the Lean comments cited are not part of the publication; each citation now names the book.

| file | pattern | replacement | places |
|---|---|---|---:|
| `*.py` | `(?m)^Treatise correspondence: [^\n]*$` | Treatise correspondence: see Appendix G of the book (The Reference Implementation). | 56 |
| `aletheia/core/errors.py` | `Raised when an honest finite model is impossible without new mathemati` | Raised when a finite model is impossible without new mathematics. | 1 |
| `lean/ArithmeticTopos/Statements.lean` | `transcribed from the design briefs\.` | transcribed from the statements of the book. | 1 |
| `lean/ArithmeticTopos/Statements.lean` | ` \(A[1-6] [A-Z][a-z]+ \d+\)` |  | 14 |
| `lean/ArithmeticTopos/Statements.lean` | `\[F\] A[1-6](?: [A-Z][a-z]+ [\d.]+)? ` | [F]  | 12 |
| `pyproject.toml` | `license = \{text = "All rights reserved"\}` | license = {text = "Apache-2.0"} | 1 |
| `pyproject.toml` | `description = "Honest finite reference models for The Arithmetic Topos` | description = "Finite reference models for The Arithmetic Topos" | 1 |
| `README.md` | `Arithmetic Topos: Foundations of a Trace-Theoretic Resolution of the L` | Arithmetic Topos: Foundations of a Trace-Theoretic Approach to the Langlands Programme* | 1 |
| `README.md` | `evidence discipline, and discovery workflow described in briefs A1–A6\` | evidence discipline, and discovery workflow described in the book. | 1 |
| `README.md` | `the polyglot design of A6` | the polyglot design of Part VII of the book | 1 |
| `README.md` | `the interfaces in A3\.` | the interfaces of Part III of the book. | 1 |
| `README.md` | `are honest combinatorics\.` | are exact combinatorics. | 1 |
| `README.md` | `for honest use\.` | for sound use. | 1 |
| `README.md` | `## Honest limitations` | ## Limitations | 1 |
| `README.md` | ``Statements\.lean` contains\nthirty-two `\[F\]` targets with `sorry` b` | `Statements.lean` contains thirty-three `[F]` targets with `sorry` bodies, transcribed at  | 1 |
