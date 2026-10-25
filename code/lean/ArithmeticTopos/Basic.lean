-- SPDX-License-Identifier: Apache-2.0
-- Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
/-!
The Arithmetic Topos — Vincent Liu · WiseMotif.ai
Finite foundational vocabulary. This skeleton intentionally has no mathlib
dependency and confers no factual status until checked by a pinned Lean kernel.
-/

namespace ArithmeticTopos

inductive Status where
  | formal | theorem | established | design | conjecture
  deriving Repr, DecidableEq

structure Certified (α : Type) where
  value : α
  specification : String
  checker : String

def composeStatus : Status → Status → Status
  | .conjecture, _ => .conjecture
  | _, .conjecture => .conjecture
  | .design, _ => .design
  | _, .design => .design
  | .established, _ => .established
  | _, .established => .established
  | .theorem, _ => .theorem
  | _, .theorem => .theorem
  | .formal, .formal => .formal

end ArithmeticTopos
