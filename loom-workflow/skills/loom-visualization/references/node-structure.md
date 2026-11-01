# loom-visualization node structure

Structure, body forms, separator and bullet marks, alignment, content rule,
width budget, scope A, Mermaid counterpart.

## Structure
A structured ASCII node label has a title line and, when needed, a body
(wrapped prose or `* `-prefixed bullet lines). Box-drawn nodes separate
the title and body with an in-box row (`├───┤`). Unboxed tree labels use
continuation lines without a separator (see `templates/07-hierarchy.md`).

## Body forms
Two forms are supported:
1. **Wrapped prose**: Long text in a box wraps at the width budget
2. **Bullet lines**: Each line prefixed with `* `, wrapped independently

## Separator and bullet marks
- Boxed nodes: full-width `├───┤` separator row between title and body
- Unboxed tree labels: body on continuation lines, with no separator
- Bullets: `* ` prefix (ASCII); Mermaid uses `• ` per `references/mermaid-cot-spec.md`

## Left alignment
Boxed titles and bodies are left-aligned (users 2026-09-27 selected).

## Container rule / content rule
Use a short title that identifies the node's action, role, state, or claim
without requiring the body to explain what the node is. Add a body only when
it contributes a distinct condition, evidence, output, or other detail that
the title, edge labels, and adjacent cells do not already convey.
A node that needs no such detail stays title-only; a boxed title-only node
has no separator. If the title is too vague to stand alone, expand it into
an informative phrase or remove the node; never add an empty separator or
filler body to satisfy a format.

## Width budget
Long prose in a box wraps at the default width budget (40 cells) or an
explicit `width` payload field. Width budget does not widen the box
without limit (see `SKILL.md` width table).

## Scope A
The title/body content rule applies to ASCII node labels in:
- Flow steps
- Branching decisions
- Reasoning chains
- State lifecycles
- Architecture layer names
- Tree continuations and hierarchy labels (unboxed in the tree template)
- Task dependency steps (including a step with multiple prerequisites)
- Cross-role workflow steps (with the owner named in the title or lane)

Box separators and left alignment apply only to boxed nodes. This rule
does not apply to other text slots (which stay single-line):
- Edge labels / arrow labels
- Table cells
- Bar labels  
- Sequence participants / messages

## Mermaid counterpart
Flowchart rectangles use the page-mode div-label convention:
`<div style='text-align:left'>TITLE<br/>━━━━━━<br/>• …</div>`
Bullets are `• `. Diamonds and state nodes stay title-only
(no body, no separator). See `references/mermaid-cot-spec.md` for
its own rule; this rule does not redefine page-mode.
