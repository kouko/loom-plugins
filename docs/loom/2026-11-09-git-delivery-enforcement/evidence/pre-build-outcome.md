# Pre-build outcome

Status: NON_CONVERGENT — implementation has not started.

The confirmed intent remains confirmed and its requirements are unchanged. The feature branch contains the intent, spec, plan and review/research evidence only. No Git hooks were installed and no adopting repository or GitHub protection was modified.

## External review

One authorized Claude Code opus/high execution completed successfully. The observed model was claude-opus-5-5; effective effort was not independently observable (accepted-explicit-settings). The review returned RESHAPE, not an implementation PASS. Its externally authored output and provenance are in claude-complexity-review.md.

Accepted changes: dependency-free static shell Git hooks, shared single-shot CI classification instead of hook polling, reuse of the existing plan-field parser, neutral startup capability disclosure, non-bypass next actions, and a bounded hook deadline. Publication withdrawal was resolved by one shared authorization helper: committed intent grants; working intent can only revoke. Commit-only withdrawal was declined because a failed commit must not restore a withdrawn grant.

## Terminal internal spec finding

The required internal pre-build review ran three times. Round 1 identified shared-hook enrollment and local-only target discovery; both were resolved in round 2. Following the externally requested reshape, round 3 found that the proposed native hook can miss a custom default branch when local origin/HEAD is missing. This contradicts REQ-3. The finding is accepted, not dismissed.

The concrete correction would require installation to establish the intended default-branch identity and validate it before certifying protection; later inability to resolve that identity must refuse with an actionable recovery instruction. Main/master fallbacks alone cannot certify protection of an unknown default. This is a proposed correction, not an implemented or reviewed fix.

The reviewer contract (loom-code/agents/reviewer.md, Fix rounds) requires NON_CONVERGENT after a blocking third round and prohibits a fourth round, identity changes to reset the episode, or asking the user whether to continue. This record preserves the failure rather than starting Build from a spec with a known protection gap. No implementation, acceptance report, final attestation, publication or merge is claimed.

## Validation actually performed

- Intent and plan checks passed at their recorded pre-build commits; these are artifact checks, not executable feature tests.
- Independent plan-lens reviewer returned PASS/no simpler shape before the external reshape. The task boundaries did not expand.
- Locked isolated test dependencies were prepared successfully in a temporary UV_CACHE_DIR. No feature or complete package suite was run because implementation never began.
- Raw external execution and consent remain in /private/tmp/loom-git-delivery-claude-review/; no unapproved second external execution ran.

## OpenCode boundary

OpenCode compatibility remains a required Acceptance obligation. The planned validation is packaged context/execute-before invocation of the shared command plus actual Git-native hook behavior. The documented absence of a Stop event is retained as a limitation. No claim is made that the unimplemented feature already works in OpenCode.
