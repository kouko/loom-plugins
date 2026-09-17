# Coexist visualization card header
originator: kouko
kind: engineering
needs-design: no — one header line in an existing hook card
status: confirmed 2026-09-17
publication: automatic — authorized 2026-09-17 by kouko

## Problem
When ascii-graph-toolkit is active, the per-turn visualization card that loom-workflow sends is headed "Visualization card (ascii-graph-toolkit)", so it looks like it comes from the other plugin even though it points at loom-visualization.

## Proposed outcome
The card names the plugin that sends it, the same way the full card does.

## Acceptance
1. The first line of `loom-workflow/skills/loom-visualization/assets/trigger-card-coexist.md` is `# Visualization card (loom-workflow)`.
2. The coexist card's word count is unchanged, so the README's per-turn word figure still holds.

## Constraints
- Only the header line changes.

## Out of scope
- Historical evidence files under `docs/loom/` that quote the old header.

## Open questions
- none
