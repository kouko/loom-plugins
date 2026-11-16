---
name: roadmap
description: |
  Create, resume or update staged project plans across sessions. Use for project roadmaps, 長期規劃 or 段階的な長期計画 and their next-stage decisions.
user-invocable: true
---

# Roadmap

Keep the project's long-running goals and next stages understandable across
sessions in an ordinary planning document. Own its creation and maintenance;
keep detailed implementation and verification with their existing workflows.

## Establish the planning context

1. Recover the requested outcome, latest corrections, existing authorization
   and current work from the visible context. A sparse invocation needs only
   the missing outcome or project context; do not invent a backlog.
2. Follow an explicitly selected existing planning document. Otherwise inspect
   the applicable root ROADMAP.md and relevant project guidance before choosing
   a direction. Read linked evidence only as needed to resolve the decision.
   Keep an existing detailed initiative document in place; do not create a
   competing root summary merely to standardize its filename.
3. If the document or owning initiative is ambiguous, identify the specific
   uncertainty. Use available intent, handoff and delivery evidence without
   pretending it establishes the missing document's contents. Ask only for a
   user outcome or selection that materially prevents progress; explain what
   the answer changes. Wait for a required answer rather than silently default.
   An unreadable document is not absent: do not replace it or change permissions.

## Create or review the plan

Create an optional root ROADMAP.md only for an actual request for staged
project planning when no applicable document exists. Resuming work or asking
for advice alone does not require a new file. Continue from available evidence
and disclose a missing planning fact only when it affects the work.

Use ordinary Markdown and the project's language and conventions. Keep a
current summary of goals, observable completion conditions, current status,
next actions, unresolved questions and links to relevant evidence or detail.
Choose the structure that fits; no required fields, identifiers or parser.
Do not create a planning runtime, ticket store or duplicate task/PR/CI ledger.

Use planning judgment selectively for complex staged work, in software,
research, learning or other domains. Reuse confirmed context; these are reasoning
aids, not required steps, fields or interviews. A simple approved task continues
directly; do not delay viable work to resolve an unknown that cannot change it.

Frame the intended improvement: who has which problem, what becomes possible
or better, and what observation would support success. Do not invent numerical
targets. Split into small increments that can be used or verified independently,
rather than separating layers until only the final stage yields a result.
Foundational work or research can come first when it enables a concrete capability
or resolves a consequential question; bound what would establish that result.

Explain why the next stage precedes another or why an alternative is deferred.
Consider contribution to the goal, evidence confidence, effort and real
dependencies or constraints where relevant, without requiring scores. Identify
a weakly supported premise only when its answer could change the next investment;
suggest a bounded way to learn about it within existing authority. Name the
evidence or changed condition that would justify continuing, changing scope,
deferring or stopping, rather than advancing stages just because work occurred.

Detail near-term work; keep distant stages provisional. Distinguish an agreed
time/spending ceiling from an effort estimate or committed date. Keep unknown
effort and dates unknown; expose a conflict with a real deadline rather than
guaranteeing capacity. Reduce optional scope where needed, preserving mandatory
safety and quality. Do not turn an estimate into a commitment.

For software migrations, replacements or breaking changes only, consider affected
consumers/data, actual prerequisites, feasible coexistence, limited exposure and
recovery limits when relevant. Identify what must be decided before widening
exposure or retiring the old path; do not promise reversible data changes or
design/execute the migration in the roadmap. Other domains need no software intake.

## Maintain only what changed

Read the selected document before editing and check for newer user changes
before writing. Update affected current entries after an authorized direction
change or verified result, preserving unrelated content and the latest user
choices. Do not silently overwrite concurrent edits or restore an older scope.
When a conflict cannot be resolved from evidence, name it and ask for the
unresolved outcome; retain the existing document until resolved.

Distinguish proposed work, reported completion, observed implementation or test
results, and user acceptance. Preserve explicit prior pending states and reported
results with their source, revision and scope; retaining that attributed status
does not require a fresh rerun. Assess each component from its own evidence:
a missing result, an exit condition or a stage marked in progress does not prove
that every component is unfinished. Keep unsupported status unknown without
discarding supported prior status. A reported test pass is not fresh verification.
Link the evidence. Contradictory delivery evidence needs an explicit explanation
and a bounded correction, not a silent status advance. Keep failed evidence and
unknowns visible through links; formatting, unchanged evidence and partial tests
do not prove completion.
Implementation, independent verification, acceptance, publication and merge
remain separate states. Do not append operational transcripts to the summary.

## Continue authorized work

A roadmap is planning context, never execution permission. It does not replace
intent confirmation, independent review, verification or acceptance. Continue
the concrete implementation or review step already approved, within its existing
scope, without a new planning interview. For a newly authorized software change,
use `loom-design:capture-intent` when available, otherwise `loom-code:write-plan`.
If neither entry is available, disclose that limitation and finish the planning
response without inventing an execution route.

Advice-only requests stay advice-only. Plan entries grant no authorization to
implement, spend, disclose, delete, publish or merge. Do not schedule background
work, start an autonomous dispatch loop or promise timed continuation.
Existing maps, purpose documents and historical evidence stay in place; do not
convert, clean up or rewrite them merely because the plugin changed.

Report the selected document, the meaningful change or recommendation and its
evidence, plus any remaining uncertainty. Claim only actions actually observed.
For next-action advice use [whats-next](../whats-next/SKILL.md); session restart
records belong to [handoff](../handoff/SKILL.md). Those skills retain their own
responsibilities; durable planning-document maintenance belongs here.
