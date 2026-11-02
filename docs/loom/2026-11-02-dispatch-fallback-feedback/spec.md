# Dispatch fallback feedback — spec
intent: 2026-11-02-dispatch-fallback-feedback@80861e57
pre-build-review: required — shared dispatch contract and materially ambiguous review/reconfirmation boundaries

## Requirements
REQ-1 — Truthful fallback completion
  WHEN a completed attempt used an override-free fallback, the resolver shall accept its retained symbolic effective profile and return routed for successful conforming work without inventing a model or effort → Acceptance #1
REQ-2 — Valid invocation data and partial observation
  The resolver shall reject malformed explicit profile pairs while preserving portable efforts and verified native efforts; the review contract shall distinguish requested settings, accepted invocation settings and independently observed settings without requiring unavailable observations → Acceptance #2
REQ-3 — Bounded feedback and redispatch
  WHEN a completed attempt is fed back, the resolver shall preserve its completed-redispatch count, permit only existing legal transitions and stop without escalation when an unknown baseline cannot justify one → Acceptance #3
REQ-4 — Review work versus reviewed work
  The review station shall distinguish a conforming verdict that identifies artifact defects from an unusable reviewer execution, retaining the existing review-round and failure-retry bounds → Acceptance #4
REQ-5 — End-to-end evidence
  The isolated workflow validation shall retain actual resolver inputs and outputs, count continuity, excluded results and legal terminal outcomes, obtaining committed validated records only for completed admissible workflows → Acceptance #5
REQ-6 — Changed intent during implementation
  WHEN the user changes confirmed requirements during implementation, the main agent shall obtain renewed confirmation, reassess affected design, plan and evidence, preserve applicable work and start a new review episode only for a substantive requirements change; wording-only reconfirmation shall preserve the episode and retries of the same failed task shall retain their count → Acceptance #6

## Design decision
- agent-decided — Extend `last_attempt.profile` to accept exactly the existing output labels `inherited` and `host-default/unverified`, as well as the existing explicit model/effort object. Feed back the dispatched effective profile, not an unsupported requested target. No new record schema, ledger, adapter or production module is needed.
- agent-decided — Validate explicit profile keys, portable model tier and nonempty string effort before every result branch. Accept portable efforts or a host-native effort verified for that exact model in capabilities; reject nulls, scalar/list objects, incomplete pairs and unverified native names. An invalid supplied pair is not a fallback label.
- agent-decided — A successful conforming symbolic attempt returns `routed`, null requested/override fields and the exact retained symbolic label. Legal malformed-response redispatch omits both overrides, retains the label and sets `next_redispatch = count + 1`. Replaying an override-free invocation does not claim the same unknown backend model.
- agent-decided — Symbolic capability-quality or reasoning-depth failure cannot justify arithmetic escalation and returns `execution-failed/no-legal-escalation`. Existing incomplete, exhausted-budget and non-routing terminal branches remain terminal. No new failure kinds or transient-retry policy is introduced. A valid success still routes at count 2.
- agent-decided — Require feedback for every completed host-native execution, including a successful final attempt. The main agent checks output structure and evidence; a conforming review that finds a product defect succeeded at its review assignment even when its verdict is NEEDS_REVISION. Artifact fix rounds are distinct from failed reviewer retries. Execution-boundary violations stay excluded and do not automatically become malformed-response.
- agent-decided — Preserve external-review explicit invocation validation and execution receipts; partial observed model/effort data is allowed by the existing evidence levels. This native fallback repair does not waive outside-execution authorization or preflight.
- user-decided — Mid-implementation substantive requirements changes require renewed intent confirmation, affected downstream work and renewed evidence. Retain usable implementation rather than restarting all work. Wording-only confirmation does not restart the review episode; changing technical repair or reviewer identity also does not reset it. The main agent records the substantive difference, affected obligations, retained/replaced evidence and task-continuity reason in existing spec/plan/evidence artifacts, not a new state store.
- agent-decided — Keep the byte-based intent pin checker unchanged. It can prove that confirmation matches file content, not that requirements changed semantically. Reconfirmation validity and eligibility for a new review episode are separate decisions. A new episode remains bounded to three functional digests. Repeating the same failed task retains its retry count even after substantive intent change; changed task obligations require a recorded reason before treating it as new work.
- agent-decided — Clarify the existing owning station contracts and test their consistency; use isolated fresh-agent exercises to verify semantic decisions rather than pretend a text assertion or hash check proves agent behavior. Preserve the no-review-ledger rule.
- agent-decided — Bump affected plugin minor versions, update changelogs and README release metadata, and derive host manifests before closing review. No installed-plugin update is part of this change.

## Alternatives considered
- Require a fully observed pair after every execution: rejected because some native and external hosts cannot supply it.
- Accept arbitrary partial objects as unknown: rejected because malformed explicit settings could bypass validation.
- Introduce a unified requested/applied/observed schema across adapters: rejected because the existing labels, invocation records and evidence levels cover this repair.
- Automatically reset all counters on a confirmation commit: rejected because a wording-only edit or unchanged failed task does not create new work.
- Add a semantic intent classifier or persistent counter ledger: rejected because neither is necessary and semantic equivalence cannot be established by a hash.
- Change transient failure policy to force blocked fixtures to finish: rejected; lawful stopping is an expected result.

## Current state evidence
- Forward: `loom-code/references/dispatch-profile.md` :: “Before every host-native dispatch” requires the resolver.
- Reverse: `loom-code/skills/closing-review/SKILL.md` :: “A closing Review episode starts” owns bounded review episodes; Build and Closing Review both reference the shared dispatch contract.
- Error: `loom-code/scripts/dispatch_profile.py` :: `_after_execution` requires an object profile although `_fallback` emits symbolic labels; its success branch previously accepted an unchecked effort value.
- Data: `loom-code/scripts/dispatch_profile.py` :: `_fallback` emits null overrides and an inherited/unverified effective profile; `_decision` can also retain an unsupported requested pair that must not be replayed as applied settings.
- Boundary: `loom-code/scripts/loom_checker/rule_checks/intent_version.py` :: `_content_identity` excludes only status/pin lines; `loom-code/skills/external-review/SKILL.md` retains outside explicit-setting and receipt requirements.

## UI flows
N/A — Internal resolver and agent workflow contracts; no new user interface, command-line arguments or external service operations.
