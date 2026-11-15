---
title: "<Research question>"
type: loom-research
status: in-progress
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags:
  - loom/research
---

# <Research question>

## Question and scope

State the pending decision, concrete unknowns and evidence sufficient to answer
each under the relevant constraints and project/version/environment conditions.
Add a flat `change` property above when an active change is known.

## Method and rationale

Name the selected investigation method or combination, why it answers this
question, and the bounded scope or stopping condition. Reusing sufficient
existing evidence is valid; explain its continued applicability. For evaluations,
state the relevant criteria and mandatory constraints, why the approach fits,
and any complementary method needed for a distinct gap. A simple factual check
needs no framework label or evaluation matrix.

## Findings

For each material evidence condition, state what is supported, unsupported or
unresolved and why, distinguishing observations, source-supported facts and
inference. Completed investigation does not mean every condition was met.

## Evidence

For each decision-critical claim, cite supporting content with URLs or relative
Markdown links. Identify the source kind, applicable version/commit and relevant
conditions, what was actually inspected, and whether support comes from a
runtime observation, source inspection, documentation, a reported case or inference.
Do not count a search result or inaccessible source as inspected content.
For repository implementation claims, cite relevant source paths and anchors;
a README citation alone is insufficient. Pin upstream code to a commit when
available; identify any missing revision information.
For measurements,
retain the actual command, relevant conditions and observed result. Identify
missing historical output; a fresh run does not recover it.

## Structural relationships (optional; omit when unhelpful)

Use a compact Mermaid diagram only if relationships clarify the question.
Follow the structured-relationships reference. State the relationship meaning
and evidence status in words; map decision-critical nodes/edges to evidence.
Keep the findings understandable without the rendered diagram. Record actual
syntax/render checks and their limits; do not invent successful validation.

## Decision impact

Explain what this evidence permits, rules out, or leaves dependent on more work.
For a recommendation, fairly compare credible smaller alternatives under the
same outcomes and mandatory constraints; explain important additions, why they
are needed and their consequential burdens. Retain necessary complexity when a
smaller option fails a mandatory condition. State what would alter the choice.
For revised conditions or recommendations, explain the evidentiary basis or
correction and update affected sections consistently; a challenge alone is not
new evidence. An unresolved comparison is valid; do not hide gaps in a score.
Link a related spec, plan or earlier research only when the target exists.

## Limitations and open questions

Record unmet conditions, missing evidence and affected decisions without lowering
requirements to claim completion, plus changes that would require revalidation.
