# Prerequisite probe attribution — spec
intent: 2026-11-17-probe-prerequisite-attribution@335042b4
pre-build-review: required — evidence attribution changes a verification boundary

## Requirements
REQ-1 — Proven unchanged prerequisites
  WHEN a graduated probe has valid prerequisite execution evidence and unchanged identity, the counter shall exclude it from automatic graduation counting → Acceptance #1
REQ-2 — Explicit reuse and union
  The counter shall include explicitly supplied prerequisites and count each path once across stored, graduated and supplied programs → Acceptance #2
REQ-3 — Fail closed
  IF prerequisite evidence or identity cannot be established THEN the counter shall retain the program, including new, copied and substantively modified programs → Acceptance #3
REQ-4 — Preserve cap
  The counter shall retain the five-program ceiling and ordinary-test distinction → Acceptance #4
REQ-5 — Preserve verification scope
  The checker shall preserve branch-wide reviewer requirements, automatic skips and full package execution independently of prerequisite attribution → Acceptance #5
REQ-6 — Preserve evidence
  The checker shall leave historical evidence unchanged and shall not reuse it as the current change's passing attestation → Acceptance #6

## Design decision
- agent-decided (REQ-1/3): Derive prerequisite evidence from Git ancestry, not an editable base or exclusion field. Only canonical attestations of other changes committed before the first introduction of the current intent qualify. Missing/ambiguous history grants no exclusion. This frozen horizon prevents current work from manufacturing a later prerequisite boundary.
- agent-decided (REQ-1/3): Validate each candidate attestation against its historical committed tree using existing attestation validation and evidence checks; its digest must cover that tree. Enumerate the canonical attestation's historical revisions before the horizon when later metadata commits no longer match the old digest. Only passing, artifact-bound adversarial executions justify individual exclusions, not an assertion that the entire earlier product was accepted.
- agent-decided (REQ-1/3): Require the same path, blob and mode at the validated tree and selected HEAD, and no intervening alteration after that evidence. Copies and changes are counted. Existing pure-rename treatment is retained separately; this change must not silently broaden its exclusions.
- agent-decided (REQ-2): Subtract proven prerequisite paths only from automatic graduated discovery. Never subtract from the current store or supplied executions. Maintain set-union deduplication.
- agent-decided (REQ-3/5): Implement attribution as a dedicated probe capability, called by graduated discovery. Keep committed_branch_delta, branch_base, reviewer floor and auto-skip logic unchanged. Avoid recursion when validating historical no-program records; records without a program execution cannot justify an exclusion.
- user-decided (REQ-4/6): Keep five programs, local-only delivery, and the finance terminal episode; do not add higher-cap exceptions or alter installed cache.

- agent-decided (REQ-1/3), Round 1 clarification: History queries naming one intent, canonical record or program must treat that name literally; only the query enumerating all canonical attestations intentionally uses a glob. Git's pathspec interpretation cannot establish uninterrupted identity for a different file. Requirements and review-episode continuity are unchanged.

## Alternatives considered
- A configurable later branch base: rejected because it can hide unreviewed content and affects unrelated reviewer/skip calculations.
- Only count supplied programs: rejected because programs committed or graduated but not supplied would escape the ceiling.
- Raise the cap: rejected because incorrect attribution remains and the user explicitly excluded that work.
- A new prerequisite manifest: rejected initially because committed history and existing attestations already identify evidence; add no new user-maintained schema without demonstrated necessity.

## Current state evidence
- Forward: loom-code/scripts/loom_checker/probes.py::graduated_probe_programs uses branch-added concern-bearing suite programs.
- Reverse: loom-code/scripts/loom_checker/command_handlers/finalize.py::_finalize calls check_adversarial_proportionate before execution.
- Error: loom-code/scripts/loom_checker/probes.py::check_adversarial_proportionate rejects a union larger than MAX_PROBE_PROGRAMS.
- Data: loom-code/scripts/loom_checker/attestation.py::validate_attestation and check_attestation_evidence bind existing execution records to historical functional content.
- Boundary: loom-code/scripts/loom_checker/reviewers.py::committed_branch_delta remains branch-wide; old finance records are read-only.

## UI flows
N/A — no new CLI arguments, editable fields or user interface; the existing cap check stops falsely attributing proven prerequisite programs.
