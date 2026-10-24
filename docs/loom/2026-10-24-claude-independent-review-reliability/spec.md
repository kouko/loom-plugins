# Reliable Claude Code independent review — spec
intent: 2026-10-24-claude-independent-review-reliability@0743260432a8ecdfc4dd392b5bf236aeb050c1d0
pre-build-review: required — external data transfer, filesystem access, and the public failure contract change

## Requirements

REQ-1 — Complete the full review
  WHEN an authorized Claude Code review receives the full-size fixture identified below through Loom's external-review entry, the entry shall return a completed, model-attributed review body consumable by the owning review flow → Acceptance #1

REQ-2 — Bound review access and writes
  WHILE a Claude Code review runs, the entry shall expose only the authorized review root and its explicitly supplied packet to model file tools, prevent model writes to the reviewed worktree, and leave the user's global Claude Code settings unchanged → Acceptance #2

REQ-3 — Identify incomplete compaction failures
  IF Claude Code ends a probe or review with a structured rapid-refill/compaction failure, including a zero-exit `is_error: true` result, THEN Loom shall report that stage as failed with a stable, recognizable reason and a private-diagnostics recovery action, without including the prompt, review body, or raw CLI error text in the public result → Acceptance #3

REQ-4 — Preserve authorization and other paths
  WHEN authorization is missing or stale, the entry shall start no external process; with valid authorization, Codex, Antigravity, and ordinary Claude success and error results shall retain their existing behavior → Acceptance #4

REQ-5 — Accept harmless review formatting
  WHEN a completed outside reviewer returns one YAML document in a single whole-output YAML fence or omits only a Conventional Comments label from otherwise complete findings, the owning flow shall accept the unchanged review fields and bind a receipt to the raw output; findings without a nonempty path plus a positive line number or nonblank verbatim quote, missing required fields, dimension scores weaker than their findings require, or contradictory overall scores and verdicts shall remain rejected → Acceptance #5

## Design decision

- agent-decided — Invoke Claude in single-run safe and restricted modes, reset its auto-compaction window for the invocation, disable configured MCP servers, and retain the existing explicit Read/Glob/Grep allowlist; this is the CLI profile that completed the measured full-size review while avoiding local customizations and command execution.
- agent-decided — Treat the review root as Claude's model-tool read boundary; keep required review evidence inside that root or explicitly include it in the submitted packet, since automatically granting outside paths would defeat the bounded read requirement. Update the Claude-specific disclosure and result description to match the actual boundary while retaining disclosure of possible CLI startup writes outside the worktree.
- agent-decided — Recognize only Claude's exact structured `rapid_refill_breaker` terminal reason as compaction failure and emit fixed public text; arbitrary CLI content remains private because it may contain review material.
- agent-decided — Expose an optional per-invocation Claude budget cap to the entry so the authorized live acceptance run can enforce USD 6 without changing ordinary review limits or user settings.
- agent-decided — Do not add retry, fallback model, or global user-settings mutation; a failed review stays failed and needs a newly authorized execution.
- agent-decided — Strip only a single whole-output YAML fence for parsing, preserve the raw output digest, and allow a nonempty finding text without its classification label. Require an anchor with a nonempty path and a positive line number or nonblank quote; this checks syntax, not whether the target content exists. In each dimension, a fatal finding or at least two important findings requires NEEDS_REVISION, and one important finding requires at least PASS_WITH_NOTES. Do not infer an anchor, severity, score, verdict, or fix.

## Alternatives considered

- Keep `--permission-mode plan` with the tool allowlist alone: the prior full-size invocation using this profile failed, and project/user customizations could still influence the reviewer.
- Change the user's global `autoCompactWindow`: persistent state would affect unrelated Claude sessions and could not be attributed to this review alone.
- Retry automatically after rapid refill: another transmission and charge would occur without a fresh bounded review request.
- Add every path mentioned in the packet with `--add-dir`: free-text paths are not a trustworthy authorization list and may expose unrelated local files.
- Replace the review carrier with free-form Markdown: the owner still needs a deterministic structure for scores, findings, and target binding, so this would add a second parser without fixing missing evidence.

## Current state evidence

- Forward: `loom-code/scripts/external_review.py::_command` builds Claude's current plan-mode invocation; `execute` runs preflight then review.
- Reverse: `loom-code/skills/external-review/SKILL.md::Execute` supplies the owning skill's packet to `external_review.py`; `loom-code/skills/closing-review/SKILL.md::Outside review` consumes this boundary.
- Error: `loom-code/scripts/external_review.py::_execution_failure_reason` recognizes structured `api_error` only and falls back to `unknown error` for `rapid_refill_breaker`.
- Data: `loom-code/scripts/external_review.py::_claude_observation` extracts `result` and `modelUsage`; `execute` returns `status`, `reason`, `observed_model`, `evidence_level`, and `review_output`.
- Boundary: `loom-code/skills/external-review/SKILL.md::Before discovery` currently says the root is not a filesystem read boundary; `loom-code/scripts/external_review.py::_consent_valid` requires explicit filesystem and vendor disclosures.
- Full-size fixture: local private archive `/private/tmp/loom-claude-full-review.ZgD0qz` is the git archive of target `3286f76d1e677f45e006ca14f61de887fad98dc3`; its private `.review-material/packet.txt` is 3,981 bytes, SHA-256 `09fdc408acd490545941424fbeeb98a266300e4b65f9ba3970376c53d8cb1257`, and `delta.patch` is 239,215 bytes, SHA-256 `f3e14f2379fcc830a08f3c71268de696f2c106ae24a0347cdd2f80bbeeb93f91` (base `4c889e23a67257a7a625842a143e7f2a93b1f5f0`). Keep packet and patch out of commits and public results.
- Measured baseline: `/private/tmp/loom-claude-full-size-qcxbg5rk/summary.json` (CLI 2.1.310, 36 turns, completed) and `/private/tmp/loom-claude-full-size-repeat-glr7k7fq/summary.json` (CLI 2.1.309, 35 turns, completed) used direct Claude calls with the proposed profile; these are local private evidence, not Loom entry results.
- Acceptance procedure: the independent tester invokes `loom-code/scripts/external_review.py` via `loom-code/scripts/loom-python --repair --script external_review.py` with `--executor claude --model opus --effort high --family anthropic --scope /private/tmp/loom-claude-full-review.ZgD0qz --consent-record <private authorized JSON> --max-budget-usd 6`; feed the exact private `packet.txt` on stdin, verify the public JSON fields and pass its `review_output` to the existing reviewer parser. The root contains the private packet and patch so restricted file tools need no outside grant.
- Later authorized Haiku/low evidence: the same full-size packet produced a completed, model-attributed review body, but its whole-output YAML fence and four missing classification labels prevented current acceptance; two of six findings also lack line-or-quote anchors. This result supports a bounded parser test but does not satisfy the original Opus/high live acceptance procedure or justify accepting the unlocated findings.

## UI flows

| Case | Review operation | Public result and owner reaction |
|---|---|---|
| Authorized completion | Run Claude review through Loom | `status: completed`, observed model, and nonempty review body; the owning flow validates the body before accepting any verdict. |
| Rapid-refill stop, nonzero or zero exit | Run Claude probe or review through Loom | `status: failed`, stage-specific reason containing a stable compaction category, `review_output: null`, and a fixed `next_action` to inspect private diagnostics before requesting another authorized review; the owning flow records no reviewer pass. |
| Other Claude execution failure | Run Claude probe or review through Loom | `status: failed` with the existing bounded reason/action and no raw prompt, review, or CLI error text; the owning flow records no reviewer pass. |
| Missing or stale consent | Request a Claude review | `status: failed`, `reason: consent-missing-or-stale`; no external process starts. |
| Completed review with harmless formatting | Submit a fenced YAML response or a finding missing only its classification label | The owning flow validates the parsed fields and keeps the raw-output digest in its receipt; it still refuses an anchor with only whitespace or line zero, or a dimension score weaker than its findings require. |
