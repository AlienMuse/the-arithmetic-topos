-- SPDX-License-Identifier: Apache-2.0
-- Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
/-!
The Arithmetic Topos — Vincent Liu · WiseMotif.ai
Primitive trace vocabulary; no claim about higher categorical existence.
-/
import ArithmeticTopos.Basic

namespace ArithmeticTopos

class TraceTheory (Endomorphism Shadow : Type) where
  trace : Endomorphism → Shadow
  traceIdentity : Endomorphism → Prop

structure Approximation (α : Type) where
  value : α
  precision : Nat
  assumptions : List String

def noImplicitUnwrap {α : Type} (_x : Approximation α) : Unit := ()

end ArithmeticTopos
