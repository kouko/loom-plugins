# Reliable Claude Code independent review — spec
intent: 2026-10-24-claude-independent-review-reliability@43470b27e359b7c87173a2cac28f8e302d76eb2d
pre-build-review: required — external data transfer, filesystem access, and the public failure contract change

## Requirements

REQ-1 — Complete the full review
  WHEN an authorized Claude Code review receives the previously failing full-size material through Loom's external-review entry, the entry shall return a completed, model-attributed review body consumable by the owning review flow → Acceptance #1

REQ-2 — Bound review access and writes
  WHILE a Claude Code review runs, the entry shall expose only the authorized review root and its explicitly supplied packet to model file tools, prevent model writes to the reviewed worktree, and leave the user's global Claude Code settings unchanged → Acceptance #2

REQ-3 — Identify incomplete compaction failures
  IF Claude Code ends a probe or review with a structured rapid-refill/compaction failure, THEN Loom shall report that stage as failed with a stable, recognizable reason and a private-diagnostics recovery action, without including the prompt, review body, or raw CLI error text in the public result → Acceptance #3

REQ-4 — Preserve authorization and other paths
  WHEN authorization is missing or stale, the entry shall start no external process; with valid authorization, Codex, Antigravity, and ordinary Claude success and error results shall retain their existing behavior → Acceptance #4

## Design decision

- agent-decided — Invoke Claude in single-run safe and restricted modes, reset its auto-compaction window for the invocation, disable configured MCP servers, and retain the existing explicit Read/Glob/Grep allowlist; this is the CLI profile that completed the measured full-size review while avoiding local customizations and command execution.
- agent-decided — Treat the review root as Claude's model-tool read boundary; keep required review evidence inside that root or explicitly include it in the submitted packet, since automatically granting outside paths would defeat the bounded read requirement. Update the Claude-specific disclosure and result description to match the actual boundary while retaining disclosure of possible CLI startup writes outside the worktree.
- agent-decided — Recognize only Claude's exact structured `rapid_refill_breaker` terminal reason as compaction failure and emit fixed public text; arbitrary CLI content remains private because it may contain review material.
- agent-decided — Do not add retry, fallback model, or global user-settings mutation; a failed review stays failed and needs a newly authorized execution.

## Alternatives considered

- Keep `--permission-mode plan` with the tool allowlist alone: the prior full-size invocation using this profile failed, and project/user customizations could still influence the reviewer.
- Change the user's global `autoCompactWindow`: persistent state would affect unrelated Claude sessions and could not be attributed to this review alone.
- Retry automatically after rapid refill: another transmission and charge would occur without a fresh bounded review request.
- Add every path mentioned in the packet with `--add-dir`: free-text paths are not a trustworthy authorization list and may expose unrelated local files.

## Current state evidence

- Forward: `loom-code/scripts/external_review.py::_command` builds Claude's current plan-mode invocation; `execute` runs preflight then review.
- Reverse: `loom-code/skills/external-review/SKILL.md::Execute` supplies the owning skill's packet to `external_review.py`; `loom-code/skills/closing-review/SKILL.md::Outside review` consumes this boundary.
- Error: `loom-code/scripts/external_review.py::_execution_failure_reason` recognizes structured `api_error` only and falls back to `unknown error` for `rapid_refill_breaker`.
- Data: `loom-code/scripts/external_review.py::_claude_observation` extracts `result` and `modelUsage`; `execute` returns `status`, `reason`, `observed_model`, `evidence_level`, and `review_output`.
- Boundary: `loom-code/skills/external-review/SKILL.md::Before discovery` currently says the root is not a filesystem read boundary; `loom-code/scripts/external_review.py::_consent_valid` requires explicit filesystem and vendor disclosures.

## UI flows

N/A — this engineering change has no new product interface; the existing external-review result and owning review flow report completion or a bounded failure.
