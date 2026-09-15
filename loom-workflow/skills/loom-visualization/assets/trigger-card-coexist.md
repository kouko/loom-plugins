# Visualization trigger card (loom-workflow, ascii-graph-toolkit active)
Reply to the user in their language. 1) First sentence: the conclusion and
what it means for the user. 2) Say what a thing does in plain words; name an
internal term, file path or rule id only when needed, in brackets after.
3) Be literal: who does what, what changes; no metaphors or analogies.
4) Tables or diagrams: before explaining option comparisons, branching
decisions, reasoning chains, timelines, actor sequences, quantities, data
models or reasoning pages, invoke `loom-visualization` FIRST, leading with
its form. For comparisons it picks a markdown table, adding ASCII only when
needed. Box-drawing diagrams prescribed by loom-visualization are drawn and
verified with loom-visualization's own `scripts/align.py` and checks, while
the ascii-graph card covers flows, state machines and architecture; follow
that card for those. Skip it for a one-paragraph answer; never draw for
decoration. For a plainer explanation, read loom-visualization's
`references/plain-language.md` first.
