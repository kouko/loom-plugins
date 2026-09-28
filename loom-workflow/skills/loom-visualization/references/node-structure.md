# loom-visualization node structure

Structure, body forms, separator and bullet marks, alignment, content rule,
width budget, scope A, Mermaid counterpart.

## Structure
A structured node consists of three parts:
- Title line
- In-box separator row (`├───┤`)
- Body (wrapped prose or `* `-prefixed bullet lines)

Title and body are left-aligned.

## Body forms
Two forms are supported:
1. **Wrapped prose**: Long text wraps inside the box at the width budget
2. **Bullet lines**: Each line prefixed with `* `, wrapped independently

## Separator and bullet marks
- Separator: full-width `├───┤` row
- Bullets: `* ` prefix (ASCII); Mermaid uses `• ` per `references/mermaid-cot-spec.md`

## Left alignment
Title and body are left-aligned inside the box (users 2026-09-27 selected).

## Container rule / content rule
A node with only one word to say is expanded into an informative phrase
or removed from the diagram — never drawn with an empty separator.
This rule avoids padding nodes to satisfy a format.

## Width budget
Long prose wraps in-box at the default width budget (40 cells) or an
explicit `width` payload field. Width budget does not widen the box
without limit (see `SKILL.md` width table).

## Scope A
Applies to box-drawn nodes:
- Flow steps
- Architecture layer names  
- Tree continuation
- Hierarchy connectors
Not to non-box text slots (which stay single-line):
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