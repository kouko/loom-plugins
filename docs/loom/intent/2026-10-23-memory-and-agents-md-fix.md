---
change-id: 2026-10-23-memory-and-agents-md-fix
originator: kouko
kind: engineering
needs-design: no — internal documentation/rules change; no user-visible surface
status: confirmed 2026-10-23
publication: automatic — authorized 2026-10-23 by kouko
---

# Record two lessons and fix AGENTS.md manifest description

## Problem

After the ship memory timing rule (2026-10-21-ship-memory-write-timing), two durable lessons were earned but not recorded because the new rule itself defers post-finalize lessons to the next change's branch. Additionally, the AGENTS.md "three manifests must sync" description is stale and does not match the actual repo structure.

## Proposed outcome

1. `docs/loom/memory/` receives two entries via git-memory trailers:
   - Direction D: Ship does not write memory entries after finalize-review; qualifying lessons discovered at or after Ship ride the next change's branch.
   - Version bump must go through the Claude SSOT (`.claude-plugin/plugin.json`) then `scripts/sync_codex_manifests.py --all`; hand-editing derived manifests fails version-sync tests.

2. AGENTS.md "three manifests" description corrected to: one manifest (`loom-code/plugin.json`) is the SSOT; `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, and `package.json` are derived by `scripts/sync_codex_manifests.py --all`.

## Acceptance

1. `docs/loom/memory/` contains two entries (one per lesson) with `Decision:`/`Learning:`/`Gotcha:` trailers.
2. AGENTS.md no longer claims "three manifests must sync"; instead describes the single SSOT + derived manifest structure.
3. All git-memory and version-sync tests pass.

## Constraints

- Loom 1.0 flow: capture-intent → write-plan → build → closing-review → ship
- Version bump follows existing repo convention (minor for station guidance, patch for docs-only)
- Memory entries must land before finalize-review (per the rule this change records)

## Out of scope

- claude_reviewer.py silent-hang fix (separate change)
- PRINCIPLES.md or DESIGN.md (not applicable)
- Any user-facing behaviour change

## Open questions

- none
