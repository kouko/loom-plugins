# Fix artifact-type pointer in the loom README
originator: kouko
kind: engineering
needs-design: no — one pointer fix in one internal document
status: confirmed 2026-09-17
publication: automatic — authorized 2026-09-17 by kouko

## Problem
The loom store README still names the concept model as the authority on how
paths map to artifact types. That document lives in a different repository,
so the pointer leads nowhere here, and the live mapping is in fact
`loom-code/contract/manifest.yaml`.

## Proposed outcome
The README points at the mapping that lives in this repository and is read
by the checker.

## Acceptance
1. `docs/loom/README.md` names `loom-code/contract/manifest.yaml` (`artifact_types`) as where the path-to-type mapping lives.
2. `docs/loom/README.md` no longer cites the concept model for that mapping.
3. `loom-code/contract/manifest.yaml` exists and declares `artifact_types`.

## Constraints
- Documentation prose only.

## Out of scope
- Anything else in the README or the repository.

## Open questions
- none