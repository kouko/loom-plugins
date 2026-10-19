# Codex review can list the account's models
originator: kouko
kind: engineering
needs-design: no — repairs how the external-review script reads Codex's model list; its arguments, output shape, and every user-facing surface stay the same
status: confirmed 2026-10-17
publication: automatic — authorized 2026-10-17 by kouko

## Problem

A Codex cross-vendor review cannot start. Loom's external-review tool asks Codex which models the account may use, but always reports that no answer came back, so every Codex review stops at its first step. Today the only workaround is to run Codex by hand outside loom, which loses loom's consent checks and recorded review evidence. The failure happened during the 2026-10-17 closing review of the node-title change; no review data had been sent.

## Proposed outcome

When the user has consented to a Codex review, loom lists the models Codex currently offers on that account, so the user and agent can pick one and the review can proceed.

## Acceptance

1. With a working Codex login, loom's Codex candidate listing returns the account's current models (a non-empty list) instead of a "response missing" failure.
2. When Codex is reachable but never answers, the listing still ends within its time limit and reports a timeout or failure reason rather than hanging.
3. Candidate listing for Claude Code and Antigravity behaves as before, and the complete package suite passes.

## Constraints

- Listing still happens only after a valid consent record, and sends Codex nothing beyond the model-list request.
- The model-selection rules (explicit model and effort, matching vendor family) stay unchanged.

## Out of scope

- Choosing or hard-coding a default Codex model.
- The node-title change whose review was interrupted.

## Open questions
- none
