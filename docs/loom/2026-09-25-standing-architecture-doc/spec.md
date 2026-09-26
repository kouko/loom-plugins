# A standing ARCHITECTURE.md that agents are held to, the way DESIGN.md is — spec
intent: 2026-09-25-standing-architecture-doc@448fad32
pre-build-review: not-required — additive, reversible skill and text changes; no security, data, or cross-system risk; the contract manifest only gains entries

## Requirements
REQ-1 — Design with the user
  WHEN a user invokes the loom-design `architecture` tool in a repository without ARCHITECTURE.md, the tool shall read the project's requirements and existing code and propose module split and dependency direction, main technology choices, folder structure and required CI stages, with at least two options and trade-offs per open choice, and record the user's picks → Acceptance #1
REQ-2 — Ratified decisions-and-rules document
  WHEN the user has picked, the tool shall write ARCHITECTURE.md at the root holding design decisions with reasons and structural rules only (no overview, data models or API interfaces), read it back, and write `ratified-by:` only on the user's yes → Acceptance #2
REQ-3 — A guard per checkable rule
  WHEN a rule can be checked mechanically, the tool shall write a guard test where the repository's package suite runs it, and record that path on the rule line → Acceptance #3
REQ-4 — Actionable guard failure
  WHEN a guard fails, its message shall name the rule id and text, the offending path, and both ways out (conform, or change the rule and its guard together) → Acceptance #4
REQ-5 — Planning reads it
  WHEN ARCHITECTURE.md exists, write-plan shall read it before the Task DAG, place added or moved files by its rules, and name the rule id on the task's Risk line → Acceptance #5
REQ-6 — Review checks conformance
  WHEN ARCHITECTURE.md exists, the code lens `architecture-conformance` dimension shall score the diff against its rules, a violation being a finding with a fix; no reviewer is added → Acceptance #6
REQ-7 — Absent is a warning
  WHEN ARCHITECTURE.md is absent, `standing` shall name it in the existing never-blocking WARN, the blanket `standing-docs: waived` shall silence it, and the dimension shall score N/A → Acceptance #7
REQ-8 — Re-design on structural change
  WHEN a change alters the structure, the tool shall re-design the affected part with the user and update its decisions, rules and guards in the same commit, then re-ratify → Acceptance #8

## Design decision
- Tool name `architecture`, owner loom-design, produces ARCHITECTURE.md; mirrors design-system (agent-decided: same shape, one place to look).
- File at repository root (user-decided 2026-09-25).
- Document shape: a `## Decisions` section (one entry per choice: what was chosen, options considered, reason) plus four rule sections — Module boundaries, File placement, File size, CI stages; each rule is one line `- <ID> — <rule> — check: <guard path> | review`; no overview section, because overview text does not change agent behaviour (agent-decided).
- Design know-how lives in a reference file built from `evidence/architecture-design-research.md` (per-ecosystem folder conventions, boundary heuristics, technology comparison dimensions, CI baseline); the tool reads code first and proposes options, never a single answer (agent-decided).
- A validator script `loom-design/scripts/architecture-design/validate_architecture_output.py` checks the ratified line, the four sections, the rule-line grammar and that every guard path exists; the tool runs it before read-back, like design-system's validator (agent-decided).
- Guards are written in the target repository's own test framework under a path its `package-tests:` command already collects; when none collects them, the tool extends that command in KICKOFF-DEFAULTS (agent-decided: the guard only holds if the suite runs it).
- A new code-lens dimension `architecture-conformance` rather than widening the existing generic `architecture` (SOLID) dimension, so N/A with no document never erases the SOLID check (agent-decided).
- write-spec is not changed (out of scope); capture-intent's needs-design clause is not changed, since ARCHITECTURE.md covers structure, not an interface surface (agent-decided).
- No new prose gate marker and no new checker rule id: the standing WARN reuses `standing.warn` with widened text (agent-decided: mechanism budget).

## Alternatives considered
- Widen the SOLID `architecture` dimension: rejected, N/A would drop the generic check in repos without the document.
- A per-document waiver key: rejected, the intent says the existing waiver silences it.
- A new checker rule validating ARCHITECTURE.md at every change: rejected, prose is not a gate and the guards already fail the suite.

## Current state evidence
- Forward: `loom-code/scripts/loom_checker/rule_checks/standing.py:13-17` builds the WARN from a hardcoded PRINCIPLES.md/DESIGN.md tuple.
- Reverse: `loom-code/scripts/loom_checker/command_handlers/standing.py:25-28` looks up both documents and passes them to `check_standing_warn`.
- Error: `loom-code/skills/write-plan/SKILL.md:311` Step 5 reads no standing document, so nothing structural shapes file placement today.
- Data: `loom-code/contract/manifest.yaml:21-34,237-240,266-272` declares tools, standing_docs and standing artifact types; `loom-code/tests/test_contract_manifest.py:120-125` pins ten counted tools against a ceiling of eighteen.
- Boundary: `loom-code/skills/closing-review/references/lenses.md:42-60` holds the N/A rule and the eleven code dimensions; `loom-code/agents/reviewer.md:49` lists them by name.

## UI flows
N/A — no carried details; the tool's interview is a skill conversation, not an interface surface.
