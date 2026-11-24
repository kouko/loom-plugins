---
name: a-graduated-probe-keeps-its-concern-line
description: When a probe that caught a defect is graduated into a package test file, that test file becomes the adversarial artifact finalize-review checks, and `adversarial.proportionate` refuses it unless a non-empty `# concern:` line sits in its first 20 lines — merging the probe's cases into an existing test file that has no such header blocks finalization after review has already passed; add the concern line in the same graduation commit
type: gotcha
sources:
  - resource: branch feat/2026-11-23-record-kept-worktrees (2026-11-23) — finalize-review refused `BLOCK adversarial.proportionate: loom-code/tests/test_land_cleanup.py carries no non-empty concern: line in its first 20 lines` after both reviewers passed; fixing it cost one more suite run, acceptance re-test and review round
---

**Trigger:** a Build task graduates a probe from `docs/loom/<change-id>/evidence/probes/` into a file under a package test root (for example by moving its cases into an existing `loom-code/tests/test_*.py`), and that file is then declared as an adversarial artifact for `finalize-review`.

**Correct path:** in the same graduation commit, make sure every receiving test file has a `# concern: <one sentence naming the defect class it defends>` line within its first 20 lines (`head -20 <file> | grep "concern:"`). Hand that requirement to the implementer in the graduation task. `loom-code/tests/test_ship_station_text.py` line 1 shows the form.

**Why:** `check_adversarial_proportionate` in `loom-code/scripts/loom_checker/probes.py` reads graduated programs as well as the probe store, so the cap and the concern line still bind after graduation. A probe file written by the adversary carries the line; an existing test file the cases are merged into usually does not, and nothing before `finalize-review` checks it.

**Limits:** only files declared as adversarial artifacts need the line; ordinary test files do not.
