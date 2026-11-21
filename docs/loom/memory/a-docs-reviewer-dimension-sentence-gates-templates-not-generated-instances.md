---
name: a-docs-reviewer-dimension-sentence-gates-templates-not-generated-instances
description: In 2026-08 (docs-reviewer, since retired), a sentence added to docs-reviewer's omission (or any) dimension row reached only contract-class `.md` — skill files, references, agents, hooks — because record-class `docs/**` was outside its jurisdiction; it never gated the generated briefs, plans, or specs the sentence was written about. The lesson stands: check which artifact a reviewer actually reads before counting a lens sentence as enforcement. Today no `loom_checker.py` rule enforces a slot such as a diagram or table in generated plans or specs (the closing-review Plan lens scores deletion-first only), so enforcing one needs a new checker rule; the change's plan should name it or record the gap — recorded twice (2026-08-11 diagram slot, 2026-08-17 table routing)
type: gotcha
sources:
  - resource: branch loom-doc-container (loom-code 0.85.0, 2026-08-17) — brief Decision, Task 5; precedent docs/loom/plans/2026-08-11-visualization-trigger-layer.md Decision Log 1
---

Both slot arcs added a docs-reviewer omission sentence "so reviewers catch
a missing/false slot" — and both discovered at review time that the
reviewer's scope contract excludes `docs/**`, so the sentence gates the
templates that define the slot, never the briefs/plans/specs that fill
it. The 2026-08-11 arc recorded it as plan Decision Log 1; this arc caught
it at planning and wrote the reach into the brief.

**Why:** the 0.75.0 contract-class narrowing made docs review cheap by
exempting record-class prose; a dimension sentence inherits that scope
whatever it talks about. Instance gating lives elsewhere: the spec
validator (mechanical, at freeze), plan-document-reviewer (reads plan
instances), and human sign-off gates with the adjudication view.

**How to apply:** when a brief proposes "add a docs-reviewer sentence" as
enforcement for a slot, state in the same sentence what gates the
generated instances; if the answer is "nothing mechanical", either add
the instance gate (validator / plan-document-reviewer check) or record it
as debt explicitly — never let the docs-reviewer sentence stand in for
instance enforcement.

**Historical (note 2026-11-21):** docs-reviewer, plan-document-reviewer
and the 0.75.0 scope contract named above are retired; the setup is
2026-08 history. The lesson stands: before a lens sentence counts as
enforcement, check whether the reviewer actually reads the generated
artifact. Today's reviewer is `loom-code/agents/reviewer.md`, scored
against the lenses in
`loom-code/skills/closing-review/references/lenses.md`; check which
files the dispatching station hands it (for example, the plan lens reads
a draft plan before Build) rather than assuming a lens sees every
generated brief, plan or spec.

(Note 2026-11-22: the Plan lens scores `deletion-first` only, so it does
not enforce a slot's presence; no current `loom_checker.py` rule checks a
diagram or table slot either. Enforcing one would need a new checker
rule, for example a `plan.*` rule beside `plan.field-caps`.)
