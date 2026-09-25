# The probe-program cap counts only probes a change adds, not tests it moves
originator: kouko
kind: engineering
needs-design: no — checker logic behind the adversarial.proportionate rule, its tests and a repo memory entry; checker/test artifacts, not interface surfaces under the manifest globs
status: confirmed 2026-09-25
publication: automatic — authorized 2026-09-25 by kouko

## Problem
finalize-review refuses a change that produces more than five adversarial
probe programs. When it counts the programs a change graduated into the test
suite, it treats a test file that the change only moved or renamed as a new
program, as long as that file keeps the `concern:` line earlier probes carry.
On 2026-09-25 this blocked PR #52, which moved every test into `tests/`
folders: the check counted nine programs when the change had produced one,
the review episode had no round left to fix it, and the PR shipped without an
attestation. Any later change that moves or renames an earlier probe's test
file hits the same refusal.

The same count also treats a program placed in a `tests/local/` folder as
collected by the package suite, although the suite skips those folders.

## Proposed outcome
The cap counts only probe programs the change itself produces: a test file
that the change moved or renamed without it being a new probe is not counted,
and a program the package suite does not run is not counted as graduated into
it.

## Acceptance
1. A change that moves or renames test files carrying a `concern:` line, and adds no probe of its own, passes the probe-program cap in finalize-review.
2. A change that adds a new probe program into the suite, including one copied from an existing probe under a new name, is still counted, and more than five still makes finalize-review refuse it.
3. A program placed under a `tests/local/` folder is not counted as graduated into the package suite.
4. The repository memory store records that moving graduated probes used to trip the cap and why PR #52 shipped unattested.
5. The checker's rule list does not grow and no new step, reviewer or dispatch is added.

## Constraints
- How the other checker rules read the branch's changed files stays unchanged (renames stay a removal plus an addition for them).
- No new checker rule, no new flow step, no extra agent dispatch.

## Out of scope
- The two local-only integration scripts that fail on this machine.
- Attesting PR #52 after the fact.
- Changing the five-program limit itself.

## Open questions
- none
