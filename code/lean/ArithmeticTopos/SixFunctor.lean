-- SPDX-License-Identifier: Apache-2.0
-- Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
/-!
The Arithmetic Topos — Vincent Liu · WiseMotif.ai
An interface-only six-functor signature inspired by KHÔRA.
-/
import ArithmeticTopos.Basic

namespace ArithmeticTopos

class SixFunctor (Obj Mor Sheaf : Type) where
  pullback : Mor → Sheaf → Sheaf
  pushforward : Mor → Sheaf → Sheaf
  exceptionalPushforward : Mor → Sheaf → Sheaf
  exceptionalPullback : Mor → Sheaf → Sheaf
  tensor : Sheaf → Sheaf → Sheaf
  internalHom : Sheaf → Sheaf → Sheaf

structure Correspondence (Obj Mor : Type) where
  left : Obj
  apex : Obj
  right : Obj
  leftMap : Mor
  rightMap : Mor

end ArithmeticTopos
