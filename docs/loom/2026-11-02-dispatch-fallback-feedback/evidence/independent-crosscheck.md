# Independent cross-check of the Claude consultation — 2026-11-02

## Assessment

The unknown-effective-profile feedback defect and the missing effort validation are independently reproducible. Claude's scope cautions are useful, but its recommendations are not all necessary repairs: the existing native attestation boundary already accepts explicitly inherited/unobservable model labels, while review-round identity and excluded-review classification remain contract questions. Do not automatically add a new retry category or attestation schema to make one fixture complete.

This check used current source and original fixture artifacts rather than treating Claude's report as authority. No new external review call, live agent trial, implementation or intent edit occurred. Source HEAD remained `55587449a0473697dee852f0dff69b240ef5d36e`.

## New executable evidence

`/tmp/loom-crosscheck-20261102/probe.py` made 50 real calls to the current packaged resolver CLI using synthetic state packets:

- Eight producer cases covered unknown main settings, unsupported known selections, host rejection, unsupported malformed-output retries, and an unsupported escalation target. Both inheritance settings were represented.
- Feeding each symbolic effective-profile result directly into successful or malformed-retry feedback produced 16 input rejections. These are protocol-shape checks, not 16 independent incidents or model/host executions.
- On successful feedback, null, integer, Boolean, object, list and empty-string effort values were accepted, as was an unverified string. Valid known-pair and verified host-native `ultra` controls also succeeded. Unknown model tiers were rejected. The confirmed defect is missing effort validation; do not “fix” it by rejecting every host-native string not in the portable effort list.
- Completed malformed output can retry, other tested failure kinds and incomplete attempts stop, and malformed retries stop at count 2. Success returns `routed` at counts 0 and 2. These controls describe current behavior, not proof of a future repair.

A symbolic output cannot directly round-trip under the current input schema. This does not mean every fallback necessarily leaves its actual settings unknowable: an adapter with a separately observed known inherited pair may truthfully report that pair. The confirmed problem is that an actually unknown/unverified effective state has no supported feedback representation.

The existing focused suites were rerun: 37 passed in 0.34 seconds. This is not the full package suite. Results: `/tmp/loom-crosscheck-20261102/probe-results.json` and `existing-tests.txt`.

## Claim-by-claim disposition

IDs below refer to the four `divergence_points` (D) and nine `findings` (F) in `claude-review-response.json`. “Confirmed” means supported within the stated source/input boundary, not general host certification.

| Claim | Disposition | Independent result |
|---|---|---|
| D1: excluded reviewer is not automatically malformed output | Supported, bounded | Raw `graduated-pytest-a/reviewer-two.yaml` is a structured PASS with scores, findings and execution disclosure. The stated exclusion concerns behavior, not absent output fields. `dispatch-profile.md:69-85` separates structural usability from capability-quality failure. Its exact retry classification needs design; do not assume an execution-boundary violation is `malformed-response`. This is not an exhaustive adjudication of the raw review's formatting. |
| D2: fix rounds differ from failed-attempt retries | Supported; earlier accusation withdrawn | `closing-review/SKILL.md:333-360` distinguishes three review rounds from one pre-verdict retry; `agents/reviewer.md:105-117` resumes the same reviewer over a changed digest. Same identity does not prove the same failed task. An initial profile calculation for Round 2 is not by itself proof of reset/bypass. |
| D3: final attestation alone cannot prove feedback/retry continuity | Confirmed | The resolver record stays in active context (`dispatch-profile.md:104-109`); a valid committed attestation does not encode a feedback receipt. Acceptance needs the rerun's command evidence and honest terminal status, not a new product ledger. |
| D4: other fallback sources are affected | Confirmed with a qualification | Multiple producer branches emit the same two symbolic states; all eight direct-feedback matrix cases reject them. Scope should include unverified effective state regardless of origin, but do not claim an actually known inherited pair cannot be reported truthfully. No extra host runtime test is implied. |
| F1: real resolver/contract representation gap | Confirmed | `_fallback` emits strings, `_after_execution` requires an object before inspecting the result (`dispatch_profile.py:62-64,170-178`). Actual CLI matrix reproduces rejection. |
| F2: successful no-retry feedback timing | Unresolved policy wording | `dispatch-profile.md:64-69` says every completed result and “before any redispatch”; `:205-208` requires successful routing. Replacement feedback is explicit; immediate feedback without a subsequent retry is not settled by executable behavior alone. Choose and document the interpretation during design. |
| F3: unknown settings do not justify arbitrary escalation/retry | Supported, bounded | Tier arithmetic requires a known profile. Current completed malformed-output retry and terminal guards were verified. Preserving an override-free policy does not prove that actual unknown model values stayed identical across attempts; keep the observation label truthful. Do not promise every failure recovers. |
| F4: resolver and station have different retry ceilings | Confirmed | Resolver permits dispatch at counts 0/1 and stops at 2; closing-review permits one retry before a conforming verdict. Preserve the stricter station limit and caller-carried count; normal fix rounds must not be silently treated as failed-attempt retries. |
| F5: station transient retry wording versus resolver stops | Source tension confirmed; runtime consequence unresolved | Closing-review allows retry for unavailable/transient executors; the resolver's tested incomplete/non-routing cases stop. The relationship between the station attempt and routing task is not fully defined. Do not silently reconcile this separate policy issue while claiming unchanged known-profile stops. |
| F6: incomplete/invalid effort can pass successful feedback | Confirmed | Real CLI calls accept null, 17, true, object, list and empty string with a known model. Verified host-native effort remains a valid control. Scope validation to complete, meaningful observed settings rather than a portable-only enum. |
| F7: unknown model might force a new attestation representation | Not reproduced; existing representation works | All four original committed records contain `inherited` or `inherited/unobservable`. Both the delivery witness shape and full final-HEAD validator accept them. `intent_state.py:168-170` requires nonblank text, not a concrete product model. Preserve truthful labeling and test it; no schema addition is justified by this concern. |
| F8: outside reviewers still require explicit verified settings | Confirmed existing boundary | `closing-review/SKILL.md:189-192` rejects using null overrides to select an outside profile. Native unknown-state support must not relax external selection or receipt requirements. |
| F9: bounded evidence and exclusions | Confirmed | Prior eight calls were four cases across identical runtime bundles. This check adds 50 synthetic CLI inputs, not 50 actual flows. Neither establishes whole-host coverage, operational frequency or a reason to add caching/modularization. |

## Correction to earlier interpretation

Withdraw the categorical statement that same-reviewer Round 2 initial dispatch itself proves a retry-budget bypass. A reviewer that correctly finds product defects has not necessarily failed its own review task. There is still no recorded result-feedback receipt in that run; whether the receipt was required at that point remains a separate contract/timing issue. Missing evidence is not proof of every asserted violation.

The actual failed replacement still demonstrates the unknown-profile schema gap. However, its failure-kind label was chosen by the experiment controller and is not established as the only legal classification. A repair must not expand retry policy merely to guarantee the fixture completes. Use an already-admissible malformed-response case to test lawful continuation, and adjudicate execution-boundary violations explicitly if they are retained as a promised outcome.

## Attestation countercheck

The four committed original fixture attestations were revalidated at their real HEADs and also passed `_delivery_witness_valid`. Their model labels were:

- missing-result-a: `inherited/unobservable` for both verdicts.
- missing-result-b, stale-new-program-a and stale-new-program-b: `inherited` for both verdicts.

No concrete model identity was needed for those native verdicts. This does not weaken outside-review explicit-profile requirements or certify that every other consumer accepts every possible unknown label. Raw local results: `/tmp/loom-crosscheck-20261102/attestation-checks.json`.

## Bounded repair direction

1. Repair unknown/unverified feedback representation and effort completeness validation in the current resolver/contract boundary; preserve valid known and verified host-native settings.
2. Clarify result-feedback timing and the distinction among a normal fix round, a failed-attempt retry and a reviewer excluded for behavior. Preserve existing limits; do not add a ledger or widen all failure-recovery policy.
3. Validate actual accepted feedback, count carry-forward, invalid-review exclusion and the honest terminal outcome in the rerun. Retain a controlled admissible continuation case that can complete; do not count a legal stop as completion.
4. Keep attestation schema changes, transient retry-policy redesign, collection optimization and module splitting outside this repair unless design produces separate concrete necessity.

The current intent is still open and unchanged. These are cross-check conclusions for refining it, not approval of implementation, publication or a technical encoding.

## Limits

This was the incumbent agent's source-and-execution recheck, not another fresh model opinion. No Claude/third-party call was added. No real host retry, new full-flow experiment, package installation or full package suite ran. Original generated fixture artifacts were inspected locally; historical user session logs were not analyzed or transmitted. No completeness or failure-rate claim is made.
