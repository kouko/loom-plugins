# Unified independent external review — spec
intent: 2026-10-08-unify-independent-external-review@34ece76cee1980a8c4391b6401e7cafb528b8445
pre-build-review: required — external CLI dispatch crosses vendor and repository-data boundaries, and the change joins two plugins' review contracts

## Requirements
REQ-1 — Independent review routing
  WHEN a user explicitly requests an outside coding agent to review code, a plan, or a decision, Loom shall retain the incumbent review and produce a separately attributable outside opinion for that task → Acceptance #1

REQ-2 — Preserve the owning review contract
  WHEN an outside agent performs an existing Loom review task, Loom shall give it that task's requirements and accept its result only under the owning review skill's verdict format and checks → Acceptance #2

REQ-3 — Opt-in boundary
  WHEN no outside review has been requested or accepted, Loom shall keep the existing non-blocking second-vendor notice and shall not start an outside execution → Acceptance #3

REQ-4 — Explicit executor profile
  WHEN an authorized outside review is dispatched through Codex, Claude Code, or Antigravity CLI, Loom shall select a candidate supported by that CLI, invoke it with both model and effort specified, and retain the result of a bounded pre-review execution → Acceptance #4

REQ-5 — No false verification
  IF the selected CLI, model, effort, or required vendor identity cannot be established, or execution fails, THEN Loom shall report the concrete limitation and shall not accept an unverifiable outside verdict as a completed independent review → Acceptance #5

## Design decision
- agent-decided — Keep review criteria, task packet and result validation with the owning Loom review skill. Independent-advisor routes a requested independent task and the common external-execution contract owns CLI selection, explicit model/effort flags, bounded execution and provenance. This lets plan, code and decision reviews share execution without importing the advisor's explore-mode proposer and blind-judge protocol into every review.
- agent-decided — Preserve the ratified one-way plugin dependency: put the common executable boundary in loom-code and expose it to loom-workflow through a named skill handoff, never by reading or running a loom-code file from loom-workflow at runtime. The independent-advisor skill remains the requested entry point; closing-review may consume the same execution contract without depending on loom-workflow.
- agent-decided — Keep model candidates as observations, not a maintained exhaustive list. Use Codex app-server `model/list` and Antigravity `agy models` when available; use documented Claude Code aliases or an explicit model ID. Cross-vendor eligibility is based on the selected model's provider family, not just the CLI name, because `agy` lists models from several families.
- agent-decided — Run any network-backed model discovery and minimal live execution only after the existing independent-advisor approval boundary. Run the actual review with the same explicit model and effort pair. Keep the selected identity and evidence source distinguishable: Codex reports the model and effort; Claude Code and Antigravity can show a successful invocation with explicit flags but do not promise both effective values in ordinary JSON output. Do not label a requested value as independently observed.
- agent-decided — Do not silently downgrade to an executor default or another model after a failed explicit selection. Surface unsupported combinations and exhausted credentials as execution failures; any materially different vendor or capability needs the existing user checkpoint again.

## Alternatives considered
- A scheduled complete model table inside independent-advisor was rejected because a repository update cannot establish account entitlement, quota or current CLI support between updates.
- Automating `/model` interactive pickers was rejected because their display and controls are not a stable machine-readable interface.
- Routing every review through the advisor's full explore-mode comparison was rejected because it duplicates the owning review skill's judgment and expands leg count, cost and data transfer.
- Making loom-code call a loom-workflow runtime file was rejected because the repository's ratified plugin dependency goes in the opposite direction.

## Current state evidence
- Forward: `loom-workflow/skills/independent-advisor/SKILL.md` — description and mode routing accept a plan or decision, then call executor detection.
- Reverse: `loom-code/skills/closing-review/SKILL.md` — a selected second vendor fills one computed reviewer slot and the original reviewer contract still determines the verdict.
- Error: `loom-workflow/skills/independent-advisor/references/executor-detection.md` — the Codex sample uses effort but leaves the model at its local default; `loom-code/skills/closing-review/SKILL.md` allows override-free fallback.
- Data: `loom-code/scripts/second_vendor_policy.py` — usable vendors are recorded as `claude`, `codex`, or `gemini`, which does not describe `agy`'s model family.
- Boundary: `PRINCIPLES.md` — non-negotiables preserve explicit egress consent and the second vendor as a user choice; Fixed choices preserve the one-way plugin dependency.

## UI flows
N/A — the changed artifacts are skill and gate instructions plus internal dispatch tooling, not a GUI, TUI, CLI argument surface or external API.
