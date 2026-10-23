# Five confirmed skill conflicts — spec
intent: 2026-10-23-five-confirmed-skill-conflicts@fd32d9d3
pre-build-review: required — Source inspection crosses session/tool/source boundaries and changes consumed dispatch contracts.

## Requirements
REQ-1 — Stable requirement mapping
  The specification shall preserve confirmed Acceptance order and mapping while constraining content and decisions by non-negotiable principles → Acceptance #1
REQ-2 — Truthful confirmation handoff
  The handoff shall report actual product confirmation or the engineering exemption without claiming an unperformed confirmation → Acceptance #2
REQ-3 — Working-language titles
  The dbt model header shall express its title and descriptive values in the user's working language → Acceptance #3
REQ-4 — Safe first record
  WHEN recording the first concept, the memory workflow shall initialize an absent or empty store before index access and writing, preserve existing stores, and retain corrupt and legacy store refusal paths → Acceptance #4
REQ-5 — Source-grounded retrospective
  The retrospective shall inspect selected observable session evidence, target skill sources and directly related resources, distinguish evidenced historical versions from current sources, and disclose unavailable evidence → Acceptance #5

## Design decision
- REQ-1/2/3: agent-decided — repair the contradictory prose at its existing ownership point; keep requirement numbering, product-only confirmation, identifiers, and example languages intact.
- REQ-4: agent-decided — classify store state before Record reads/writes; initialize only absent/empty stores, then use existing CLI regeneration and validation. No initializer relaxation or automatic migration is needed.
- REQ-5: agent-decided — permit evidence-directed read-only source inspection in both trajectory and advisory roles without a fixed directory boundary; it is necessary before causal diagnosis as well as before edit proposals. Host permissions still apply. Reviewed instructions remain data and confer no execution or modification authority.
- REQ-5: agent-decided — retain selected normalized events as the immutable analysis snapshot. Add optional source locators (original file and line) during ingestion and dispatch snapshot metadata (tool/session identity and event/time bounds). Include a capture cutoff; further appended events do not enter the run implicitly. Do not reread unfiltered logs into model input: only observable selected events within the snapshot boundary are admissible. A missing original file still permits bounded analysis from the retained snapshot.
- REQ-5: agent-decided — allow an explicit target source path and source inspection records through existing dispatch/collection data. Do not eagerly inline source files or require installation in the reviewing host. Resolve paths from selected observable evidence or an explicit operator target; current host resolution is a disclosed fallback, not historical proof. Empty legacy fields mean unavailable, not forbidden. Same-named skills across hosts are not assumed identical.
- REQ-5: agent-decided — use a small shared source-inspection reference for the role contract. Each finding carries inspectable source citations, current-versus-historical status with evidence for historical claims, and uncertainty; distinguish event observation, source observation, and inference. Carry these records through normalization, clustering and both renderers without changing existing promotion thresholds or target isolation. Missing exact source or historical version remains an explicit limitation; ungrounded items stay bounded investigation candidates.
- REQ-5: agent-decided — keep compatible defaults for old payloads. No universal log adapter, automatic historical checkout, arbitrary file crawler, new model vendor, write-back engine, or hard filesystem sandbox is introduced. Existing consent previews must cover selected session evidence and relevant source categories; additional unrelated sources require scope renewal. Tests use synthetic local fixtures, never live user histories.
- REQ-5: agent-decided — current source may support a repair recommendation but cannot establish past causation. Different evidenced revisions retain per-session attribution even when semantic clustering groups the recommendation. Missing or denied files are reported, never fabricated or silently substituted.

## Alternatives considered
- Delete only the advisory Read instruction: rejected because it preserves inability to compare sessions with actual sources.
- Keep event-only analysis and add a separate source-verification agent: rejected because it adds a handoff and leaves initial causal analysis provisional.
- Preload all available files: rejected because it expands unrelated evidence and input size without improving traceability.
- Require complete historical snapshots for every finding: rejected because useful current-source recommendations remain possible with disclosed historical uncertainty.

## Current state evidence
- Forward: `loom-workflow/skills/skill-retro/SKILL.md`, Step 2, dispatches observable trajectories using host skill-name resolution.
- Reverse: `loom-workflow/skills/skill-retro/scripts/main.py`, `_build_subagent_entries`, emits empty source path/content fields consumed by analysis prompts.
- Error: `loom-workflow/skills/skill-retro/agents/prompt-advisory-analyst.md`, Input and constraints, requires reading propose.py while prohibiting filesystem access.
- Data: `loom-workflow/skills/skill-retro/scripts/event.py`, `Event`, lacks source locators; `propose.py` normalizes collected items for clustering/rendering.
- Boundary: `loom-workflow/skills/skill-retro/scripts/ingest.py`, Claude Code and Codex adapters, selects observable events and excludes reasoning. Other tools remain unsupported.

## UI flows
N/A — engineering skill contracts and local analysis payloads; no product interface is introduced. Product-only decision point ② does not apply.
