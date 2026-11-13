import Lake
open Lake DSL

package evidence where
  leanOptions := #[⟨`autoImplicit, false⟩]

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git"

@[default_target]
lean_lib Evidence where
  globs := #[.submodules `Evidence]
