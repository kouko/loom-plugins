# Optional project roadmap and planning-mechanism retirement — spec
intent: 2026-11-16-roadmap-simplification@6c3b1663
pre-build-review: required — retires distributed skill and document contracts across three plugins

## Requirements

REQ-1 — Optional ordinary project planning
  WHERE a project needs staged cross-session planning, Loom shall support an optional root ROADMAP.md containing current goals, completion conditions, status, next actions, unresolved questions and evidence links without the map runtime or a prescribed machine-readable schema → Acceptance #1

REQ-2 — Contextual creation and maintenance
  WHEN the user requests cross-session staged planning, resumes that work or asks for its next action, Loom shall create or read the applicable project planning document and update affected summary content when direction or verified results change → Acceptance #2

REQ-3 — Retire overlapping capabilities only
  The released plugins shall remove decision-map and repository-purpose drafting while preserving ordinary delivery, research, handoff and goal-create session execution goals → Acceptance #3

REQ-4 — Preserve existing project data
  WHEN a plugin is upgraded, Loom shall leave existing project planning documents and historical evidence in place without automatic deletion, rewriting or conversion → Acceptance #4

REQ-5 — Preserve authorization and evidence boundaries
  The roadmap guidance shall preserve existing implementation confirmation and delivery verification and shall distinguish proposed, observed and accepted results → Acceptance #5

## Design decision

- user-decided — Root ROADMAP.md is optional, used for projects needing long-term planning; it is a current summary with evidence links, not mandatory scaffolding for every repository.
- agent-decided — Existing capture-intent, whats-next and handoff instructions carry the relevant contextual guidance; no roadmap skill, CLI, validator, ticket type, identifier grammar or background hook is added. These are already the owners of intake, next-action advice and continuation.
- agent-decided — Follow an explicitly named existing planning document when one exists, rather than silently creating a competing root summary. Use root ROADMAP.md as the default for new project-wide planning. An existing detailed initiative document may remain the evidence/detail target; do not relocate or rewrite it simply to standardize filenames.
- agent-decided — New document creation is limited to an actual request for staged planning. Asking for next-action advice or resuming work alone does not force creation of an absent roadmap. Continue from available intent, handoff and evidence and disclose a material gap.
- agent-decided — Read the selected roadmap before recommending a new direction for its long-running work. A viable approved implementation continues through its existing station; roadmap advice does not interrupt it or reset intent interviews.
- agent-decided — Update only affected current entries after verified results or an authorized direction change. Preserve unknowns and failed evidence as links; do not append full operational transcripts or duplicate task/PR/CI ledgers. Routine formatting or unchanged evidence does not trigger status advancement.
- agent-decided — If a document is missing, ambiguous, unreadable or contradicts authoritative delivery evidence, disclose the specific uncertainty and use existing evidence. Do not replace an unreadable document, guess which unrelated initiative owns the work, or silently overwrite a user change. Ask only for unresolved user outcomes or necessary authorization.
- agent-decided — Remove the decision-map skill directory and its dedicated test directory. Remove its manifest/discovery entries, live guide references, map-origin intent validation and matching template guidance/tests. Preserve unrelated intent validation. Historical records under docs remain history, not advertised current operations.
- agent-decided — Keep goal-create's skill identity and SESSION implementation; remove only ARC-specific runtime guidance, offers, examples and tests, plus the obsolete PURPOSE scaffold and its current contract references. Generic contextual reading of an existing purpose document is not itself a reason to delete that document.
- agent-decided — Skill inventory changes by minus one in loom-workflow, zero in loom-code and loom-design; no replacement skill. Regenerate derived manifests through the existing sync command rather than editing generated inventories independently.
- user-decided — Existing maps remain readable documents but the upgraded plugin no longer manages them. Do not automatically close or migrate the old family-relocation map or modify other checkouts; this loss of operational support was disclosed at intent confirmation.
- agent-decided — No new root roadmap is required in the Loom repository merely to implement this convention. Scope is instruction/contract retirement, not inventing a project backlog.
- agent-decided — Release metadata must include the applicable minor bumps for changed station guidance/contracts, changelog entries and synchronized versions before final review; no installed-cache refresh is implied by a source change.
- agent-decided — This is engineering guidance/contract work per repository interface policy; no product behavior confirmation is added at decision point ②. Required independent spec review still applies.

## Alternatives considered

- Keep the map with better naming: retains the dedicated lifecycle and maintenance surface without demonstrated need for its enforcement in the finance-style use case.
- Add a roadmap facade over maps: adds another representation and leaves the old runtime necessary.
- Add a dedicated roadmap skill/schema: recreates the mechanism being removed; existing entry points can carry concise contextual guidance.
- Require ROADMAP.md in every project: forces maintenance even for a single bounded change and conflicts with the confirmed optional scope.
- Delete all of goal-create: removes independent session-goal functionality outside the requested retirement.
- Automatically convert old maps: rewrites user data and requires a migration not justified by actual current inputs; retain history instead.
- Keep permanent dual active stores: introduces competing update ownership; existing detailed documents are linked or selected, not duplicated.

## Current state evidence

- Forward: `loom-workflow/skills/decision-map/SKILL.md`, Chart and Re-enter and select — dedicated creation, activation and store selection.
- Reverse: `loom-workflow/skills/using-loom-workflow/SKILL.md`, discovery table; `loom-code/contract/manifest.yaml`, station/tool inventory — exposes the map as a supported capability.
- Error: `loom-code/scripts/loom_checker/rule_checks/intent.py`, check_map_exists — rejects map origin claims without a MAP.md; this special validation retires with its origin mechanism.
- Data: `loom-workflow/skills/decision-map/references/map-format.md`, MAP.md template and ticket template; `loom-code/contract/templates/PURPOSE.md`, Why and Done when — specialized formats replaced for future planning, not rewritten in existing projects.
- Boundary: `loom-workflow/skills/goal-create/SKILL.md`, ARC mode versus SESSION; `loom-workflow/skills/handoff/SKILL.md`, continuation ownership; `docs/loom/research/2026-11-16-roadmap-simplification.md`, source/session evidence and adoption limits — preserve distinct execution goals and history.

## UI flows

N/A — No GUI, TUI, CLI command or API is introduced; existing conversational skills receive engineering guidance and retired capability references are removed.

## Validation boundaries

Use fresh-context behavioral cases to distinguish request-driven creation, existing-document resumption, next-action advice, verified-result updates and unchanged/failed/ambiguous inputs. Judge semantic results and unchanged user data, not exact explanatory sentences. Static inventory checks must show one skill removed and SESSION retained; focused tests must preserve unrelated intent and goal behavior. Preserve the existing package suite, independent review and acceptance-report requirements. No agent compliance, installed-host activation or adoption claim follows from prose alone.
