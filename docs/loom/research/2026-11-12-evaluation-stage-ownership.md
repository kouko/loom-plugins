---
title: Ownership of engineering evaluation across Loom stages
type: loom-research
status: concluded
created: 2026-11-12
updated: 2026-11-12
tags:
  - loom/research
---

# Ownership of engineering evaluation across Loom stages

## Question and scope

Should the dimensions and five-step evaluation described in the dotfiles session
belong to engineering-research, capture-intent, specification, or planning? When
should a stage invoke research? This is design discussion, not authorization to
implement a new workflow. Conditions: checkout
248d5272ac71ff2926f1fc675db4884f1e589f4d and the incident studied in the
[companion diagnosis](2026-11-12-recommendation-evidence-gap.md).

## Method and rationale

Compare existing artifact responsibilities and runtime guidance against the
decision being made. Criteria: clear accountability, proportionate work, no
duplicated rationale/evidence, standalone research support, no premature solution
selection, and compatibility with one-way plugin dependencies. Local contracts
suffice for this ownership proposal; no claim of external industry consensus or
behavioral improvement is made. No new model experiment was run.

## Findings

Evaluation and evidence acquisition are different responsibilities. A stage
must justify the decision it makes even when no new research is needed. Research
resolves a consequential uncertainty and returns evidence or an explicit limit;
it need not own or finalize the caller's design decision.

| Owner | Proposed responsibility | What should not move here |
|---|---|---|
| Intent capture | Establish wanted outcomes, user-fixed boundaries and important consequences; resolve factual uncertainty that would invalidate scope/feasibility before promising it | Routine library selection, invented quality guarantees, detailed design comparison |
| Specification/design | Select relevant quality criteria, compare material design alternatives, define applicable behavior and record design decisions | Raw research transcripts or task scheduling |
| Planning | Turn settled design and risks into implementation/test work; assess choices within its remit; reopen design if a new finding invalidates it | A duplicate design rationale or silent alteration of confirmed behavior |
| Research capability | Choose and execute proportionate source inspection, experiments or analysis for a named uncertainty; retain evidence, limits and conditional recommendations | Exclusive ownership of all engineering judgment or new approval authority |

Current support is partial, not absent: intent forbids design rationale; spec
already requires Design decision, Alternatives considered and Current state
evidence; plan already requires evidence-based agent decisions and explicitly
considers research for consequential factual gaps. Research already supports
standalone work. The additional proposal is to make evaluation accountability
clear at the decision owner, rather than relying on optional research activation
to cause all assessment.

### Which parts of the five steps belong where?

1. Mandatory conditions originate in confirmed outcomes, existing constraints
   and principles. The design owner derives relevant technical criteria; it must
   not pretend an agent preference was a user requirement.
2. Credible alternatives are considered by the design/decision owner. Research
   can discover and compare them when evidence is missing.
3. The decision owner identifies which unknown could change its choice.
4. Research obtains missing evidence when warranted. Adequate existing evidence
   permits a direct decision; unfamiliar terminology alone is not a research job.
5. Research retains evidence and revalidation conditions; spec or the owning
   decision record retains the selected design and reason. Plan references these
   and arranges necessary implementation verification.

The eight dimensions are prompts to select relevant criteria, not eight mandatory
new sections in every stage. They can affect intent when the user has fixed an
outcome, design when a solution is selected, and planning when checks and work
are arranged. Their detailed method catalog can remain in research; the obligation
to make a supported decision must apply without invoking that catalog.

### Research trigger boundary

| Situation | Appropriate response |
|---|---|
| Existing applicable evidence makes the choice clear | Decide, record a short reason; no separate research invocation required |
| Missing/contradictory factual evidence could change the choice | Invoke bounded research or make the smallest applicable check; preserve uncertainty if unresolved |
| The missing input is the user's desired outcome or authorization | Ask within the existing human decision boundaries; research cannot determine consent or preference |
| A minor unresolved detail cannot change the bounded decision | State an assumption/limit where material; defer deeper investigation |

Invocation remains proportionate. "Research is optional" must not be interpreted
as permission to present an unsupported comparative preference as established.
No new mandatory experiment or separate user confirmation is proposed.

## Evidence

- [Intent station](../../../loom-design/skills/capture-intent/SKILL.md), interview,
  field boundaries, one-way-door handling and handoff; [interview reference](../../../loom-design/skills/capture-intent/references/interview.md).
- [Spec station](../../../loom-design/skills/write-spec/SKILL.md), Step 2 design
  decisions, alternatives and current evidence; Step 3 technical choices.
- [Plan station](../../../loom-code/skills/write-plan/SKILL.md), Step 4 rationale
  requiring a spec and Step 5 evidence-based forks/research delegation.
- [Artifact charter](../../../loom-code/contract/manifest.yaml), intent/spec/plan
  ownership and forbidden duplication.
- [Research contract](../../../loom-code/skills/engineering-research/SKILL.md),
  applicability, proportionality, retained records and return to caller;
  [evaluation reference](../../../loom-code/skills/engineering-research/references/evaluation-selection.md).
- [Principles](../../../PRINCIPLES.md), fixed one-way plugin dependency and no
  prose-only blocking gates; [ownership test](../../../loom-code/tests/engineering-research/test_package.py),
  test_code_owns_the_only_discoverable_package_without_design_routing.

These are source observations, not runtime results. The current test explicitly
forbids direct engineering-research references under loom-design skills. Therefore
"add a call in capture-intent/write-spec" is not a compatible wording-only patch:
it would require an explicit change to the current ownership/routing convention
and its tests, or an orchestration handoff that preserves that boundary. No such
implementation route is chosen here. A shared filesystem reference across plugins
would also violate the standing portable dependency rule.

## Decision impact

| Option | Benefit | Limit |
|---|---|---|
| Keep assessment entirely behind optional research activation | Smallest present structure | Design decisions can escape assessment when research is not selected |
| Repeat the entire evaluation procedure in every station | Local visibility | Duplication and unnecessary assessment; unclear canonical ownership |
| Decision-owning stages assess; research resolves evidence gaps (recommended) | Accountability applies to all material decisions; preserves bounded research | Needs a tested, dependency-compatible handoff rather than copying references |

A smaller first step is to test this division on one design-choice case and one
clear-choice negative control, without adding a global checker or artifact type.
Deferring changes preserves current behavior and its demonstrated incident.
Combining stage accountability with the existing research catalog is the
recommended composition; combining duplicated full procedures adds no established
benefit. A semantic reviewer can be considered only if residual failures justify
its cost. None of these proposals has been implemented or behaviorally validated.

For the archive example: intent establishes what conversion should achieve and
which existing data must remain untouched, without inventing guarantees. Design
compares whole-7-Zip with extraction-plus-Python against relevant conditions.
If applicable evidence is insufficient, research checks that particular gap.
Plan schedules the selected integration and meaningful failure/integrity tests;
it does not restart the same tool debate. In a standalone research discussion,
the research skill performs the bounded assessment itself because there is no
spec or plan owner yet; its recommendation remains conditional on known inputs.

## Limitations and open questions

This proposal follows inspected local responsibilities and the observed incident,
not a demonstrated causal improvement. Exact cross-plugin dispatch and enforcement
are unresolved implementation choices. Moving responsibilities does not itself
ensure compliance: the original session loaded applicable research guidance and
still omitted a material comparison. A future test must inspect actual decision
evidence, follow-up reversals and retained-record consistency, not just skill reads.

Verification: saved substantive content read back; relative Markdown targets
resolved from this record's directory. No production instruction was changed.

## Subsequent scope choice and complexity assessment

The user selected separate research skills owned by loom-design and loom-code,
and requested planning for research activation across loom-code stages. This
supersedes the earlier undecided skill-count alternatives, not the historical
evidence or the absence of a demonstrated behavioral improvement. A separate
[confirmed intent](../intent/2026-11-12-design-code-research-routing.md) captures
this direction. The user additionally confirmed that detailed research work
belongs inside each research skill and existing stage flows should stay simple.

Complexity assessment uses the Design-Is-Taking-Apart reference from the installed
critique skill: separate responsibilities without unnecessary coupling.

- Q1, smallest end state: one design-owned research capability alongside the
  existing code-owned capability, with bounded activation/return guidance at
  relevant stages. Neither a third research router nor a mandatory study at
  every stage is needed by the current outcome. A single capability would not
  meet the user's explicit ownership choice.
- Q2, volume: the current engineering-research package contains eight files and
  574 lines, counted by Python over its files. It is prose, with zero executable
  functions. A full copy would add another eight files/574 lines before routing
  and tests; this is a comparison baseline, not the proposed implementation.
  The selected direction adds one discoverable skill. Exact final files, prose
  lines and test functions are not yet designed and cannot honestly be counted.
  Additional maintained surface must be costed in the implementation plan; it
  is justified only by distinct design research and actual integration.
- Q3, deletions: none verified at intent stage. Duplicated station-specific
  research recipes, if the later inventory finds any, are removal candidates,
  not promised deletions. Existing engineering methods should not be removed
  merely to offset the new capability's count.
- Verdict: RESHAPE. Keep separate ownership and the user's requested activation
  behavior, but use Q1's minimal integrated form rather than cloning the full
  research package or adding a universal mandatory research step. This verdict
  does not establish a final size reduction. Intent confirmation is now recorded;
  the admitted extra skill and mechanism-budget impact
  must be handled explicitly during design/planning under existing rules.
