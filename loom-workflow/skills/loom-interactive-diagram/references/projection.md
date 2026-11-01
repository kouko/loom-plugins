# Text projection

Every managed diagram in `docs/loom/<change-id>/diagrams/` and every standalone
diagram has an adjacent same-named `<name>.projection.md`. A selected external
original receives one beside it after `project --in-place`. Diagrams linked
from a change's `spec.md` with a registered extension are also checked against
their adjacent projections. The projection's first line is
`backend: <backend-id>`. The rest is generated from the diagram, with sorted
nodes and edges:

```text
backend: drawio
# Nodes
- node-1: Start
- node-2: End
# Edges
- edge-1: node-1 -> node-2 | next
```

Each section uses `- none` when empty. A draw.io node is an `mxCell` with
`vertex="1"`; an edge has `edge="1"`, `source`, and `target`. For the demo JSON
backend, nodes have `id` and `label`, and edges have `id`, `source`, `target`,
and `label`. A draw.io `object` wrapping an `mxCell` supplies its visible
`label` and, when the cell has no ID, its `id` to the projection. The
projection is text for review and conversation. Edit the diagram first, then
run `python3 <plugin-root>/skills/loom-interactive-diagram/scripts/diagram.py
project diagrams/<name>.<ext>` to regenerate the projection.
For a standalone diagram or an external original the user explicitly chose to
edit, run `project <diagram-path> --in-place`; an absent adjacent projection is
created for a registered format. If the adjacent projection is a symlink,
the command refuses to write it.
`python3 <plugin-root>/skills/loom-interactive-diagram/scripts/diagram.py check`
includes all registered files under `diagrams/` and
Markdown links in `spec.md` that end in a registered diagram extension.
It compares the projection and names the first differing line for each file.
