# Separate research ownership with small stage handoffs — spec
intent: 2026-11-12-design-code-research-routing@ed10de55
pre-build-review: required — Cross-plugin responsibility and research authority boundaries change.

## Requirements

REQ-1 — Distinct discoverable research capabilities
  WHEN a design or engineering question requires research, Loom shall expose separately owned design and engineering research capabilities with distinguishable responsibilities → Acceptance #1
REQ-2 — Proportionate code-stage activation
  WHEN a code stage faces a consequential evidence gap, the stage shall identify its pending decision and use engineering research as needed while avoiding unnecessary research for adequate evidence or immaterial uncertainty → Acceptance #2
REQ-3 — Design-stage activation and bounded return
  WHEN a design stage needs research, Loom shall use its design-owned capability and return findings or unresolved uncertainty to the original task without changing confirmed goals, authorization or user decisions → Acceptance #3
REQ-4 — Supported material choices
  WHEN a material alternative is recommended, research shall compare credible alternatives against relevant common criteria and distinguish constraints, preferences, facts and unknowns without claiming unsupported superiority → Acceptance #4
REQ-5 — Traceable continuing conclusions
  WHEN a research question continues or a recommendation changes, research shall retain inspectable evidence and keep the applicable saved conclusion consistent with the conversation while preserving earlier decisions under changed conditions → Acceptance #5
REQ-6 — Observable behavioral evidence
  WHEN the change is verified, the evidence shall demonstrate routing, non-routing, return and follow-up record maintenance through actual task behavior rather than file structure or claimed skill activation alone → Acceptance #6

## Design decision

- user-decided — Separate research capabilities belong to loom-design and
  loom-code. Complexity stays inside research skills; stage flows remain small.
- agent-decided — Add `loom-design:design-research` for evidence about user
  problems, usage context, outcome/quality priorities, behavior alternatives and
  design/architecture decisions owned by design. Preserve
  `loom-code:engineering-research` for technical capability, implementation,
  compatibility, operational diagnosis and execution evidence. Classify by the
  question, not merely the current station or by whether it mentions code.
- agent-decided — A design-owned architecture assessment may inspect technical
  sources; an implementation feasibility question remains engineering. A mixed
  question is separated into bounded questions and existing records reused.
  Design does not read code-plugin internals or automatically delegate to it.
  An engineering-only gap discovered in design is identified for a skill-name
  handoff at the task boundary; it must not be answered by relabeling it design.
- agent-decided — Keep stage additions to one short, context-specific paragraph:
  identify the decision and material evidence gap, name the owned skill, and
  return evidence/uncertainty without expanding authorization. No new station,
  required matrix, trigger ledger, artifact type or generic research router.
  Existing adequate evidence permits a short direct decision.
- agent-decided — Capture-intent and write-spec use design research; other
  design tools may use the same bounded capability when their own decisions
  need it. Code stages write-plan, build, closing-review, ship and maintain use
  engineering research for their respective questions. The code-only entry uses
  its existing research skill; absent loom-design does not require installing it.
- agent-decided — Review research may investigate a factual contradiction, but
  does not edit artifacts, replace reviewers or acceptance testing, prove a
  successful historical run from source definitions, or create missing delivery
  evidence. Ship retains its independent observed publication requirements.
- agent-decided — Put method selection, relevant quality prompts, alternatives,
  source applicability, smallest useful checks and conclusion maintenance inside
  each research skill. Design guidance includes constraints/alternatives and
  evidence quality without duplicating the engineering method catalog. User
  preference, consent and feasibility evidence remain distinct.
- agent-decided — Each material recommendation needs applicable support; evidence
  for a top-level integration choice does not settle a nested tool choice. A
  follow-up challenge is a reason to reassess, not new factual evidence or an
  instruction to agree. Update the matching record before delivering a changed
  conclusion; an unsupported earlier recommendation may be withdrawn explicitly.
- agent-decided — Preserve the existing flat research metadata and project-local
  record paths. Design uses the same question/conditions-based record principles
  with a self-contained template. Do not copy optional post-merge Vault lifecycle
  behavior into the new skill; existing engineering preservation remains intact.
- agent-decided — Add only portable package/discovery invariants required by the
  new capability; verify prose behavior using fresh-context task executions and
  retained actual outputs. Cover all code stages with positive and negative
  scenarios, plus design handoff, unsupported nested choices and follow-up drift.
- agent-decided — Register the new nonstation tool and explicitly account for one
  extra skill in the existing mechanism budget, without an extra artifact type
  or session-start injection. Bump loom-code and loom-design minor releases and
  associated synchronized metadata before final attestation.

### Behavioral verification cases

| Case | Actual task | Expected boundary |
|---|---|---|
| D1 | Design evidence conflicts about a user's workflow and behavior options | Inspect supplied sources, distinguish report from observation, compare relevant outcomes, retain research and return |
| D2 | User has already fixed the outcome and supplied adequate evidence | No mandatory study, interview quota or reopened preference |
| D3 | Architecture question contains an implementation capability gap | Separate questions, identify engineering handoff without reading another plugin's internal files |
| C1 | Plan assumes a dependency capability contradicted by supplied version evidence | Research the applicable version before committing the choice |
| C2 | Build repeatedly fails under conflicting environmental assumptions | Investigate competing premises, retain the original task and authorization |
| C3 | Review encounters a contradictory completion claim | Research without changing artifacts or awarding missing execution evidence |
| C4 | Ship lacks evidence of current publication/check success | Retain unknown status; research cannot manufacture delivery proof |
| C5 | Maintain receives a contradictory failure report | Establish factual evidence without implementing a fix or replacing intent capture |
| N1–N5 | Same five stages have adequate evidence and no consequential new gap | Proceed within the station; no mandatory new research |
| F1 | Initial recommendation contains a nested tool choice; user challenges it | Do not infer superiority from capability/tool count alone; justify change or explicitly withdraw; update saved conclusion |
| F2 | Conditions materially change or saving is prohibited | Preserve earlier applicable decision or return an explicitly unsaved draft |

Behavioral tests may use isolated source fixtures and bounded task execution;
they must retain the actual input, operations, outputs and final saved record.
Deterministic package assertions alone are insufficient. No claimed activation
rate or cross-model generalization follows from these bounded cases.

## Alternatives considered

- One research skill for both plugins — rejected because the user selected
  separate responsibility and the existing dependency boundary is intentional.
- Copy the complete engineering research package — rejected: implementation
  diagnosis and optional Vault preservation do not become design methods.
- Full evaluation checklist at every stage — rejected: adds repeated complexity
  and contradicts the user's explicit simplicity constraint.
- Always run research before a decision — rejected: adequate evidence and
  immaterial questions need no new investigation.
- Add a new semantic checker/router or require an outside model — rejected:
  existing independent verification can test this bounded change first.

## Current state evidence

- Forward: `loom-design/skills/capture-intent/SKILL.md` Step 1 and
  `write-spec/SKILL.md` Step 2 own intent/design; no design research exists.
- Reverse: `loom-code/skills/using-loom-code/SKILL.md` research row and
  `write-plan/SKILL.md` evidence-based forks call engineering-research.
- Error: `docs/loom/research/2026-11-12-recommendation-evidence-gap.md`
  Historical observations records unsupported nested choice and stale conclusion.
- Data: `loom-code/skills/engineering-research/templates/research.md` defines
  flat metadata; `loom-code/contract/manifest.yaml` tools registers nonstations.
- Boundary: `PRINCIPLES.md` Fixed choices forbids cross-plugin internal-file
  dependencies; `loom-code/tests/engineering-research/test_package.py` protects
  code ownership. No existing user installation or dotfiles runtime changes.

## UI flows

N/A — This engineering change modifies skill/gate contracts and their research
records, not a product interface. Question to owned research to original task
is an internal handoff; existing user decision points remain unchanged.
