# Text projection

Every diagram in `docs/loom/<change-id>/diagrams/`, or linked from that
change's `spec.md` with a registered extension, has a same-named
`<name>.projection.md`. Its first line is `backend: <backend-id>`. The rest
is generated from the diagram, with sorted nodes and edges:

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
run `diagram.py project` to regenerate the projection.
`diagram.py check` includes all registered files under `diagrams/` and
Markdown links in `spec.md` that end in a registered diagram extension.
It compares the projection and names the first differing line for each file.
