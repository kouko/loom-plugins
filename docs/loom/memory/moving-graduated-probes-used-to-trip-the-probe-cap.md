---
name: moving-graduated-probes-used-to-trip-the-probe-cap
description: A branch-delta count read without rename detection sees every moved file as a removal plus a new file, so a count of "new" programs must pair renames of removed paths before counting, and must still count copies and rewrites, or a pure file move can fail a cap it never spent against
type: gotcha
sources:
  - resource: PR #52 (refactor/move every test into tests folders), merged unattested 2026-09-25
  - resource: change 2026-09-25-probe-cap-ignores-moved-tests (fix commit d4dbb19c)
---

PR #52 moved every test into `tests/` folders. At finalize-review the
`adversarial.proportionate` rule counted 9 probe programs against its cap
of 5: 8 were graduated probes carrying a `concern:` line that the move had
only renamed, and 1 was new. The probe count read the branch delta, which
is built with `--no-renames`, so each renamed probe looked like a newly
added program. The review episode had already used its three digests, so
the PR shipped with "Verification status: absent".

The fix counts only added paths that are not renames of paths the branch
removed, paired at git's default 50% similarity, and only when the removed
path carried a `concern:` line at the branch base. The pairing is computed
inside the probe count only; the shared branch delta and its other callers
still read with `--no-renames`. A probe copied under a new name while the
original stays is still counted, and so is a move rewritten below the
similarity threshold. Programs under `tests/local/`, which the package
suite skips through pytest `--ignore=`, are no longer counted as graduated
into the suite, unless a tracked symlink under a test root leads pytest back
into that folder, in which case the suite runs them and they still count.

**Why:** a count of new programs is a claim about what a branch produced.
Without rename pairing a refactor that only moves files spends the whole
cap, and the failure lands at finalize-review, the most expensive place to
discover it. Pairing renames anywhere else would change what every other
rule reads from the branch delta.

**How to apply:** when a rule counts additions in a branch delta, decide
explicitly whether a rename is an addition, and pair renames only where
that rule needs it. Expect a large move to still pair its exact renames.
Pin git's rename limit (`-l0`, unlimited) rather than inheriting
`diff.renameLimit`, which differs by machine and would leave edited moves
unpaired on one and paired on another. When the pairing cannot be read, exclude nothing, so the cap
fails closed.
