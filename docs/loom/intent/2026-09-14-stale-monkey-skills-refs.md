# Remove stale present-tense monkey-skills references
originator: kouko
kind: engineering
needs-design: no — this edits wording in documentation, comments, a test script's printed hint and two document titles; it changes no plugin behavior, CLI, or interface surface
status: confirmed 2026-09-14
publication: automatic — authorized 2026-09-14 by kouko

## Problem
After the move to the public `kouko/loom-plugins` repository, a few places
still describe `monkey-skills` as the current home: a skill README says the
skill belongs to it, an integration test prints an install command for the old
marketplace, code comments call this repository by the old name, and the
repository's principles and kickoff-defaults documents carry the old name in
their titles. Readers following them are misled or install from the wrong place.

## Proposed outcome
Present-tense references name `loom-plugins`, while historical records,
license attribution, and test fixtures keep their original wording.

## Acceptance
1. The three `distill-sessions` README language versions describe `monkey-skills` only as where the skill was developed, not as its current home, and keep the license-compatibility statement.
2. The superpowers integration test's printed install hint uses the `loom` marketplace, and the integration-test README's example path no longer names `monkey-skills`.
3. The code comments in `check_contract_citations.py` and `distill-sessions/scripts/main.py` no longer call this repository `monkey-skills`.
4. The titles of `PRINCIPLES.md` and `docs/loom/KICKOFF-DEFAULTS.md` name `loom-plugins` instead of `monkey-skills`, with every other line of both files unchanged.
5. The repository's existing package test suite passes.

## Constraints
- CHANGELOGs, historical plans, research, memory entries, announcements, license and NOTICE files, and test fixtures keep their `monkey-skills` wording.
- `PRINCIPLES.md` ratification lines and all principle content stay unchanged.

## Out of scope
- Any behavior, manifest, or README change beyond the lines named above.

## Open questions
- none
