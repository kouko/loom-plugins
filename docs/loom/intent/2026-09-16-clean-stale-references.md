# Clean stale references
originator: kouko
kind: engineering
needs-design: no — mechanical cleanup of documentation references
status: confirmed 2026-09-16
publication: automatic — authorized 2026-09-16 by kouko

## Problem
Some repository documents point readers and agents at files or folders that no longer exist, so anyone following those pointers hits a dead end.

## Proposed outcome
Every pointer this change touches leads to something that exists, and nothing that still exists loses its pointer.

## Acceptance
1. `loom-workflow/skills/distill-sessions/references/codex-tools.md` no longer names a `codex-tools.md` or any other file that does not exist in `loom-code`.
2. Every folder or file the frozen-store list in `docs/loom/README.md` links to exists, and `docs/loom/plans/` is still listed.
3. `loom-code/docs/examples/README.md` no longer links to `skills/using-loom-code/references/codex-tools.md`.

## Constraints
- Documentation prose only; no skill behaviour changes.

## Out of scope
- Other items from the 2026-09-16 follow-up scan.
- `loom-design/skills/write-spec/SKILL.md`: its "ten completeness questions" sentence matches `references/spec-forms.md` and stays.

## Open questions
- none
