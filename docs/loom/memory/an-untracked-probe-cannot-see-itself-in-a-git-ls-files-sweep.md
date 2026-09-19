---
name: an-untracked-probe-cannot-see-itself-in-a-git-ls-files-sweep
description: an adversarial or regression probe that greps `git ls-files` for a stale pattern across "every tracked file" passes locally while it is still uncommitted (git does not list it), then fails the moment it is committed and rescanned — the probe's own source becomes the finding; either exclude the probe's own path from the sweep, or run it once already committed before declaring green
type: gotcha
sources:
  - resource: "PR #32 (2026-09-19), change 2026-09-19-bump-loom-code-3-7-2 — a fresh-context adversary wrote `test_no_operative_file_still_carries_the_previous_version`, sweeping every `git ls-files` entry outside `docs/` and `CHANGELOG.md` for a stale version string, reported \"13 passed\" while the file sat uncommitted, then a second reviewer's independent re-run at the committed sha found `1 failed` — the probe's own docstring and a legitimate `changelog.split(\"## [3.7.1]\")` boundary-parse both contain the string it was built to catch"
---

A sweep built on `git ls-files` (or any other "every tracked file" enumeration)
only sees what git already has staged or committed. A probe file that
legitimately needs to mention the old value it is testing for — in a
docstring explaining the check, or in a literal used to parse a boundary —
is invisible to its own sweep for as long as it stays untracked, and starts
failing the instant `git add`/`git commit` makes it visible.

**Why:** the adversary in this branch verified the fix with a mutation
check (flip a real file back to the stale value, confirm the probe catches
it) and ran the full suite before handing off — both passed, because the
probe file itself was still untracked at that moment. The failure was real
but had zero chance of surfacing before the file was committed, and nothing
in the adversary's own verification loop could have caught it: `git status`
would have shown it as untracked, not as a discrepancy.

**How to apply:** when a probe scans "every file the repo tracks" for a
pattern the probe's own source must legitimately contain (a docstring
explaining what it catches, a literal used for parsing), exclude the
probe's own path from the scan explicitly — resolve it from `__file__`
rather than hardcoding the filename, so a later rename does not silently
reopen the gap. If the probe is authored and verified before its first
commit, re-run it once more immediately after committing, before declaring
the branch green; a green run pre-commit does not prove a green run
post-commit for this exact class of check.
