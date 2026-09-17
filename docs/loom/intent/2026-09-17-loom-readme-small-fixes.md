# Loom README small fixes
originator: kouko
kind: engineering
needs-design: no — two wording and link fixes in one internal document
status: confirmed 2026-09-17
publication: automatic — authorized 2026-09-17 by kouko

## Problem
The loom store README still has two small defects left from the previous cleanup: a sentence whose subject can be read as the removed stores, and a link to a maps folder that does not exist yet, so clicking it leads nowhere.

## Proposed outcome
The README reads unambiguously and every link in it opens something that exists, while still telling readers where decision maps will be kept.

## Acceptance
1. In `docs/loom/README.md`, the sentence after "survive only in git history" names the old plans as what stays in the tree.
2. Every relative link in `docs/loom/README.md` resolves to a path that exists.
3. `docs/loom/README.md` still lists `docs/loom/maps/` as the place decision maps are kept.

## Constraints
- Documentation prose only.

## Out of scope
- Creating a `docs/loom/maps/` folder or any decision map.
- Any other file.

## Open questions
- none
