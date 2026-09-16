# Loom asks git which files belong to the repository it is running in
originator: kouko
kind: engineering
needs-design: no — this changes how loom enumerates a repository's files and how its gates and this repository's own checks consume that list; no command, output format, or interface surface a user types into changes
status: confirmed 2026-09-16
publication: automatic — authorized 2026-09-16 by kouko

## Problem
Loom decides what counts as the content of the repository it is running in by
walking the filesystem, and never asks git. A git linked worktree created
inside a repository directory is invisible to git but fully visible to a
filesystem walk, and Claude Code places worktrees there by default, so loom
reads another change's files as if they were the repository's own. Paths
excluded by `.gitignore` and by `.git/info/exclude` are read the same way.
This affects every repository that adopts loom, not only this one: on
2026-09-16 finalize-review here stopped on six reported violations that all
came from another session's worktree and had nothing to do with the change
under test, and `loom-code/scripts/loom_checker/probes.py` picks a repository's
test command by walking for test files with no exclusions at all, so in an
adopting repository it can pick one that belongs to a worktree or to ignored
build output. Neither available response is acceptable to the person hit by
it: the other worktree may be locked and hold uncommitted work that is not
theirs to remove, and widening the check would let real violations pass.

## Proposed outcome
Loom ships one way of answering "which files belong to this repository", and
it answers by asking git, so a git worktree inside the repository directory
and paths excluded by `.gitignore` are never treated as repository content.
Loom's own gates and probes use it wherever they run, including inside a
repository that has adopted loom. It keeps working where there is no git at
all, and it still sees a file that git does not track yet. This repository's
own development checks consume the same shipped mechanism rather than each
walking the filesystem their own way.

## Acceptance
1. In a repository that has adopted loom and contains a git linked worktree
   inside its directory at a path that repository's git ignores, loom's checker
   takes no file inside that worktree into account, using only the loom-code
   plugin as installed. Where the worktree's path is not ignored, the checker's
   pre-existing clean-tree check stops finalization because git reports the
   worktree as uncommitted content; that is a stated exception.
2. With a git linked worktree present inside this repository's directory, each
   of the six scanners listed in Constraints passes, and no reported finding
   points at a file inside that worktree.
3. With a git linked worktree present inside this repository's directory, the
   package-test command collects no test file from inside that worktree.
4. Extracted from the same commit with `git archive` into a copy that has no
   `.git`, the five archive-capable scanners named in Constraints still run and
   reach the verdict they reach in the git checkout.
   `loom-code/scripts/rehearse_probes.py` is the stated exception: it works by
   cloning the repository, so it cannot run without git. In that copy it
   reports an explicit skip naming that reason instead of failing.
5. A violating file that git does not track and that `.gitignore` does not
   exclude is reported by the scanner whose rule it violates.
6. A directory excluded by `.gitignore` produces no finding from any of those
   six scanners.

## Constraints
- The mechanism ships with the loom-code plugin and must run inside an
  adopting repository using only files installed with that plugin; it may not
  depend on anything that exists only in this repository.
- Scope is fixed to these six scanners that walk from the repository root:
  `loom-code/scripts/loom_checker/probes.py`,
  `loom-code/scripts/check_doc_citations.py`,
  `loom-code/scripts/rehearse_probes.py`,
  `loom-workflow/scripts/test_no_live_cot_explain_references.py`,
  `scripts/check_plugin_boundaries.py`,
  `scripts/test_state_anchor_carrier_inventory.py`; plus the collection roots
  the package-test runner hands to pytest.
- The ability to run these scanners in a `git archive` copy is already relied
  on and must be kept; `loom-code/scripts/test_write_plan_station_text.py:269`
  documents that purpose. Five of the six are archive-capable; the exception is
  `loom-code/scripts/rehearse_probes.py`, which clones the repository to do its
  work and so depends on git by construction. That dependency predates this
  change.
- The clean-tree check that stops finalization when git reports uncommitted
  content guards publication and is not one of the six scanners; this change
  does not alter it. Its behaviour toward a nested worktree at a path git does
  not ignore predates this change.
- The fixed ignore-directory list keeps the names already in use in this
  repository (`__pycache__`, `node_modules`, `.pytest_cache` and the like); no
  new ignore convention is introduced.

## Out of scope
- The roughly ten scanners that walk a single plugin subtree; their hardcoded
  exclusion lists are left as they are.
- Scanners that walk user data directories, such as the decision-map maps root.
- Scanners that walk an installed-plugin copy in a temporary directory.
- Changing the rules by which a scanner decides something is a violation. The
  set of files a scanner is shown does change — that is the point of this
  change — so a verdict can move in either direction: a match that was
  ambiguous because of an ignored or foreign copy can become unique and get
  checked, and a target that is present but excluded by `.gitignore` becomes
  unchecked rather than resolved.
- Documenting the mechanism as an interface for callers outside loom's own
  gates, or promising its shape will stay stable for them. Nothing is added to
  prevent such a call; none is designed for.

## Open questions
- none
