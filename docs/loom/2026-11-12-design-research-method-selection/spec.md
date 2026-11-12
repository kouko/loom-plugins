# Bounded design research method selection — spec
intent: 2026-11-12-design-research-method-selection@bd14580d
pre-build-review: required — the distributed skill contract changes its permitted evidence acquisition and engineering handoff boundary

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
  The change shall retain actual behavioral case executions with inputs, outputs and observable checks sufficient for independent assessment of REQ-1 through REQ-5. → Acceptance #6

## Design decision
- agent-decided — REQ-1/2: replace the broader acquisition paragraph and add at most one concise bundled reference for question-led selection and source/dialogue practice; keep existing stage callers unchanged because the skill owns this complexity.
- agent-decided — REQ-2/3: adapt reasoning, not full branded methods. Concrete episode questions, outcome/need/option relationships, assumption checks, described journeys and quality scenarios remain optional aids; none constitutes a workshop, validated opportunity tree or formal architecture evaluation.
- agent-decided — REQ-3: permit reading published participant studies while attributing their results and transfer limits. Current-user answers establish their stated context, not others' behavior; missing population evidence may remain unresolved.
- agent-decided — REQ-4: retain the existing question-based ownership boundary and explicitly include security-control evidence. No engineering-research behavior change is needed.
- agent-decided — REQ-5: preserve the existing template, paths, flat metadata, follow-up and readback contract; no new record schema.
- agent-decided — REQ-6: use isolated agent trials with controlled source/user fixtures and retained transcripts, including a baseline and candidate run on matched cases. Trial actors simulate inputs only; their answers are not product research. Case assertions evaluate behavior and artifacts, not framework keywords. No general superiority claim from this small sample.
- agent-decided — release: bump only loom-design minor version and synchronize its derived manifests, changelog, localized README strings and affected pins before final review.
- agent-decided — integration repair after first finalization: an existing blocked-input timeout regression expired in its five-second preflight instead of reaching its six-second review branch. Remove the fake CLI's Python cold-start dependency while preserving real subprocess/pipe, deadline and cleanup checks. This changes only test machinery, not research requirements or production external review; the existing design trial evidence remains applicable.

- agent-decided — technical re-look after recurrence: the initial single-test boundary missed a shared sibling CLI factory. Repair the shared short-deadline fixtures and all their existing consumers as one bounded obligation, preserving actual stdin EOF detection, exited-parent/lingering-child distinctions and process cleanup. Reject higher deadlines, bypassed preflights, fewer workers and weakened assertions. Longer-budget progress fixtures are a different condition and remain unchanged. No research requirement or review-episode reset follows; only one terminal functional digest remains.

Supplemental acceptance for this added shared-factory obligation must check a
clean package load plus the newly affected model-list EOF, exit/descendant and
review-stage protocol cases. It retains the completed design-trial evidence
because no research guidance or production runner changes; it is not another
execution of that completed trial task or a reset of its task continuity.

The bounded phase-marker experiment passed without reproducing the failure;
native fixtures had also failed in the original full workload. Therefore their
reliability advantage remains unproved. agent-decided — withdraw both incidental
test-file rewrites and restore their exact trunk bytes, preserving all original
coverage and deadlines. Keep the diagnosis and unsuccessful attempts as history,
not shipped repairs. The final candidate returns to the requested research
guidance/release scope; complete mechanical verification and the same terminal
review remain required. This is a smaller technical shape, not a requirement,
test skip, evidence substitution or review-budget reset.

## Alternatives considered
- No skill edit, trials only: leaves the installed acquisition scope inconsistent with the requested boundary.
- Selection hints entirely inline: viable if shorter after implementation; prefer this over a separate reference when the latter adds no meaningful reading boundary.
- One manual per design capability or a stage router: unnecessary scope and ongoing dependencies.
- Keyword-only assertions: cannot establish actual research behavior; preserve existing packaging checks instead.

## Current state evidence
- Forward: loom-design/skills/design-research/SKILL.md :: Bound the question identifies pending decisions and evidence reuse.
- Reverse: loom-design/skills/write-spec/SKILL.md :: Step 2 calls design-research only for consequential gaps.
- Error: loom-design/skills/design-research/SKILL.md :: Choose the smallest useful investigation allows walkthrough/prototype checks and participant work under authorization, exceeding the requested scope.
- Data: loom-design/skills/design-research/templates/research.md :: flat metadata and evidence/findings/conclusion sections already retain bounded research.
- Boundary: loom-design/tests/test_design_research_package.py :: portable resources remain self-contained; code-owned research is named, never imported.

## UI flows
N/A — internal skill guidance, no new product interface or Loom station.
