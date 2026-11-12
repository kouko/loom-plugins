# Bounded research and active proposal simplification — spec
intent: 2026-11-12-design-research-method-selection@6869846f
pre-build-review: required — both distributed research contracts gain a consequential proposal-evaluation obligation

## Requirements
REQ-1 — Bounded acquisition
  The design research skill shall acquire new evidence only through online research and dialogue with the current user, using supplied existing artifacts as context and excluding participant, workshop, field, product-operation, prototype and experiment activities. → Acceptance #1
REQ-2 — Proportionate selection
  WHEN a consequential gap remains after reusing applicable evidence, the skill shall select only useful question-appropriate reasoning or inquiry without mandatory frameworks, quotas or repeated settled questions. → Acceptance #2
REQ-3 — Evidence honesty
  The skill shall distinguish inspected source claims, user accounts and preferences, inference and unknowns, without treating published methods or current-user dialogue as performed studies, population validation or implementation proof. → Acceptance #3
REQ-4 — Engineering boundary
  WHEN a mixed question requires actual capability, compatibility, feasibility or security-control evidence, the skill shall separate the design finding from a bounded unresolved engineering research handoff by skill name, without automatic delegation or private cross-plugin imports. → Acceptance #4
REQ-5 — Continuing records
  WHEN reassessment changes a conclusion, the skill shall update the matching retained record and read back its substantive evidence, conclusion and limitations before delivery, preserving the reason for change. → Acceptance #5
REQ-6 — Observable validation
  The change shall retain actual behavioral executions with inputs, outputs and observable checks supporting all applicable research obligations, including REQ-7. → Acceptance #6
REQ-7 — Active equivalent simplification
  WHEN proposing or materially restructuring an important design or engineering solution, the owning research skill shall actively consider a smaller alternative satisfying the same confirmed outcomes and mandatory constraints, explain adopting simplification or retaining necessary complexity, and revisit consequential evidence gaps without fixed iteration quotas or extra workflow stages. → Acceptance #7

## Design decision
- agent-decided — REQ-1–5: retain the already implemented design-research scope, optional method selection, evidence distinctions and record safeguards; no template or caller change.
- agent-decided — REQ-7: integrate a short active simplification check into each skill's existing comparison guidance. Keep the two owners self-contained; do not introduce a shared runtime file, router, critique dispatch, new gate, scoring matrix or mandatory round count.
- agent-decided — REQ-7: consider keeping the current approach, removing unnecessary elements, narrowing the solution or combining overlapping responsibilities only when applicable. Do not generate a quota of alternatives or require deletion to earn completion.
- agent-decided — REQ-7: design-owned simplification concerns user steps, roles and behavior choices. Engineering-owned simplification concerns components, dependencies, abstractions and operational work. Neither may remove confirmed outcomes or mandatory correctness, security, accessibility or compatibility requirements that apply.
- agent-decided — REQ-2/7: routine facts and adequate-evidence reuse return directly. For an important proposal, continue inquiry only when a consequential unresolved premise could change the comparison; stop with adequate support or explicitly return an unresolved condition when permitted research cannot settle it.
- agent-decided — REQ-5/7: retain the chosen smaller shape, removed burden or concrete reason necessary complexity remains in the existing record's findings/decision impact. No new schema field or separate report is required.
- agent-decided — REQ-6/7: use native behavioral cases for removable burden, necessary complexity and adequate-evidence reuse in each owner. Add a decision-changing unknown case where needed; source inspection or framework-name output alone does not establish behavior. Keep these controlled inputs distinct from real participant evidence.
- agent-decided — release: the unshipped design release remains 2.25.0; extend its changelog. Bump code from 3.70.0 to 3.71.0 because its skill guidance changes; synchronize derived manifests, README versions and existing release pins.
- user-decided — the 2026-11-13 confirmation covers both skills' simplification responsibility. It does not authorize GitHub publication or merge; the earlier inferred publication field is removed.

## Requirements change and evidence continuity
The renewed intent adds REQ-7 to both owners and expands REQ-6 coverage. This is
a substantive new obligation, not a wording-only reconfirmation. It starts a
new bounded closing-review episode for the changed requirements, after their
implementation and checks pass. Earlier semantic cases and dogfood remain
evidence only for the unchanged behavior they actually exercised; they do not
prove active simplification, necessity preservation or its stopping behavior.

The earlier episode used three reviewed functional digests and generated an
attestation for the old requirements. Preserve that historical evidence without
presenting it as verification of the new intent. Earlier failed fixture-repair
task counts remain retained; no further timeout-fixture repair is authorized by
this added requirement. The two external-review test files remain exact trunk
bytes. A new suite failure needs attribution, not a retry-budget reset.

## Alternatives considered
- Keep comparison guidance unchanged: misses the user's explicit active-simplification outcome.
- Add one paragraph in each owner: smallest self-contained shape; integrate overlapping wording rather than duplicate it.
- Introduce a shared simplification skill or automatic critique call: adds cross-plugin dependency and orchestration without a demonstrated need.
- Fixed research rounds or simplify-every-lookup: adds work even when evidence is sufficient.
- Delete important safeguards to reduce steps: not equivalent to the confirmed outcome.

## Current state evidence
- Forward: loom-design/skills/design-research/SKILL.md :: Choose the smallest useful investigation; loom-code/skills/engineering-research/SKILL.md :: Choosing an evaluation approach.
- Reverse: loom-design/skills/write-spec/SKILL.md :: Step 2; loom-code/skills/write-plan/SKILL.md :: optional research for consequential gaps.
- Error: engineering-research/references/evaluation-selection.md already permits smaller changes, postponement and combinations, but neither owner explicitly requires an active simplification check before a material recommendation.
- Data: both skills' templates/research.md provide method, findings, evidence and decision impact; no field addition is needed.
- Boundary: station callers, external-review implementation, existing timeout tests and publication authorization remain outside the simplification implementation.

## UI flows
N/A — internal research guidance; no new product interface or Loom station.
