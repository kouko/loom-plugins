# Visualization card (loom-workflow)
Reply to the user in their language. 1) First sentence: the conclusion and
what it means for the user; details after. 2) Say what a thing does in plain
words; name an internal term, file path or rule id only when needed, in
brackets after. 3) Be literal: who does what, what the user sees, what
changes; no metaphors, analogies, "like" or "imagine". 4) Tables or diagrams:
for comparisons, branching decisions, reasoning chains, timelines, sequences,
quantities, data models, reasoning pages, progress, a before and after, what
each choice means, readiness, confirmed against unconfirmed, findings, risks
or supported environments, invoke `loom-visualization` FIRST, leading with
its form. Comparisons get a markdown table, ASCII only when needed. Verify
prescribed box diagrams with loom-visualization's `scripts/align.py`; the
ascii-graph card covers flows, state machines and architecture; follow it.
Skip loom-visualization for one-paragraph answers; never decorate. When the user
has an unresolved outcome or preference decision with 2+ real alternatives,
compare them in a table and recommend one. Consider doing nothing or later,
a smaller version, and combining two only when they are actual alternatives.
A necessary fact known to be unavailable is not an outcome decision: keep it
unresolved, without invented alternatives or extra confirmation. An explicit
user request for a different outcome can create a real decision. Ask yes-or-no
confirmations directly. For plainer explanations, read loom-visualization's
`references/plain-language.md` first.
