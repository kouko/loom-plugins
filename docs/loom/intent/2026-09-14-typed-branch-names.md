# Name loom change branches `<type>/<change-id>`
originator: kouko
kind: engineering
needs-design: no — this changes the branch-naming convention in station prose and one checker hint string; it touches no configured interface surface and adds no multi-state behavior
status: confirmed 2026-09-14
publication: automatic — authorized 2026-09-14 by kouko

## Problem
Loom tells agents to create a change branch named exactly `<change-id>`
(`2026-09-14-push-reason`). The common convention, and the one the maintainer
wants to keep, puts a type in front (`feat/...`, `fix/...`). Branches named
the loom way carry no type, so type-based branch rules, labelers, and a
reader scanning the branch list cannot tell a feature from a fix; in practice
branches in this repo already drift away from the loom name
(`fix-agy-adapter`, `w4-03-push-reason`), so the documented convention is
followed neither way.

## Proposed outcome
Every place loom tells an agent or a user what to name a change branch says
`<type>/<change-id>`, where `<type>` is a conventional-commit type the agent
picks and keeps consistent with the change's commit and PR title type.
The full change-id stays in the name so the branch still maps one-to-one to
`docs/loom/<change-id>/`.

## Acceptance
1. The write-plan station's branch instruction creates `<type>/<change-id>` (for example `feat/2026-09-14-push-reason`), names the allowed types, and says the agent picks the type and uses the same type in the change's commit and PR title.
2. When the loom checker refuses to run on the trunk, its hint tells the user to run `git switch -c <type>/<change-id>`.
3. The capture-intent station's branch note names `<type>/<change-id>` as the branch write-plan creates.
4. No loom station text, checker hint, or test still tells anyone to name a change branch bare `<change-id>` (search of `loom-code`, `loom-design`, `loom-workflow`, excluding CHANGELOG history).
5. In a scratch repository on a branch named `<type>/<change-id>`, the checker commands that compute the branch base accept the branch rather than refusing it for its name.
6. The repository's package test suite passes.

## Constraints
- The checker does not start enforcing or parsing branch names; only guidance text changes.
- The change-id format itself (`<YYYY-MM-DD>-<kebab-title>`) and every `docs/loom/<change-id>/` path stay unchanged.

## Out of scope
- Renaming existing branches in this or any other repository.
- Releasing a new plugin version to the marketplace cache.
- CHANGELOG entries and historical records under `docs/loom/` that quote the old form.

## Open questions
- none
