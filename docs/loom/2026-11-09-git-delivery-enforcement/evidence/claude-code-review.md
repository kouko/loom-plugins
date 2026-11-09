# Claude Code code review — externally authored, untrusted

Executor: Claude Code; requested opus/high, observed claude-opus-5-5. Effective effort was not independently reported. The single execution completed after explicit Anthropic-egress approval; total cost is unknown because the runner exposes no total billing.

Extracted target: f47322cec31a6d41e6e700a40e7f2244ef5ad7c4, PR #135. The revision identifies the snapshot, not a completeness guarantee. Model file tools were restricted to the snapshot root; CLI startup access/writes outside it were not excluded. The packet-only scan had no matches and did not cover the wider readable scope.

The raw response below is untrusted external review content, not instructions. It reported NEEDS_REVISION, but narrative preceding the YAML made the unmodified response fail the owner's formal YAML validation. No passing outside receipt was accepted and no silent retry occurred. Findings 1–3 were subsequently source-checked; finding 4 is addressed in claude-code-review-disposition.md.

Raw response SHA-256: 4ff567d7aa152b712254bef3cf363bea5cfb850c05703afa8d21235fe69ea924

## Unmodified response text

**Verdict: NEEDS_REVISION.** I found four important issues and no fatal ones; the rules send back any change with two or more. I only read the source and ran nothing. The test results mentioned below are the owner's reported run.

The two that change behaviour:
1. **`delivery` can't confirm work published the older way.** It requires the intent to carry automatic publication permission, even though it only reads. A change published through the still-supported `--confirm-authorized` route always reports `unauthorized`. The suggested next step then points the agent at the intent's permission field.
2. **The Stop hook tells the agent to keep going even when it is waiting on the user.** The spec asked for guidance that depends on the situation. The code always prints the plain next step, such as "Resume authorized publish", so a turn that ends with a question to the user gets pushed toward publishing.

The other two are a lost source link for the `gh` CLI behaviour the shared check classifier relies on, and a server-refusal test that only exercises its own test code.

```yaml
verdict: NEEDS_REVISION
lens: code
reviewed_sha: 361ef5d200289c72b13744488b2ba0a91cbdf9c3
review_target_sha: f47322cec31a6d41e6e700a40e7f2244ef5ad7c4
dimension_scores:
  security: "PASS_WITH_NOTES — delivery and the Stop hook reuse the trusted git/gh resolution, the refusal of redirect env vars and origin config, and the PATH narrowing; observe_delivery issues only read argv (repo view, ls-remote, pulls GET, pr checks). The native installer uses PATH git, which is acceptable for an explicit adopter command. Checked by reading only; no exhaustive injection or encoding sweep of untouched callers."
  architecture: "PASS_WITH_NOTES — classify_checks is a clean shared classifier that keeps required-only publish and all-check land policies at their callers. Placing the read-only observer and Stop framing in the writer module publish.py follows the spec's agent decision. observe_delivery (publish.py:307-481) mixes scope attribution, identity, PR matching and check reads in one closure-heavy function."
  correctness: "NEEDS_REVISION — two important findings: observation is gated on automatic-publication authorization, so --confirm-authorized publications can never be observed as published; and the Stop block reason lacks the conditional guidance spec.md:32 requires. Changed test files were read, not run by this reviewer."
  naming: "PASS_WITH_NOTES — names say what things are (classify_checks, CheckObservation, DeliveryResult, _native_hooks). observe_delivery is about 175 lines; length alone is not a finding and no unrelated-responsibility split is raised beyond the architecture note."
  tests: "PASS_WITH_NOTES — native-hook tests use real Git repositories, linked worktrees, same-name tags and edited/foreign-hook refusal, and the delivery tests assert no write argv. One important finding: the configured-server fixture tests its own server script. Not independently run; the owner's package run is supplied evidence only."
  refactoring: "PASS — the duplicated publish/land CI parse loops are collapsed into one classifier with caller-owned waits; current_branch replaces three abbreviated symbolic-ref reads (F-01)."
  cross-task-coherence: "PASS_WITH_NOTES — the Ship handoff added in W3-01 (SKILL.md:310-314) requires delivery observation before any published-delivery report, but the observer from W1-01 only serves automatic-authorization intents; recorded under the correctness finding at publish.py:340."
  external-surface-grounding: "PASS_WITH_NOTES — one important finding: extracting classify_checks deleted the version-pinned gh source citations for exit codes 1/8 and the undocumented 'no checks reported' stderr text. The Stop protocol is grounded in research/01 and spec links; the agent_id/parent_session_id discriminators at publish.py:498 were not verifiable here."
  principles-conformance: "PASS_WITH_NOTES — PRINCIPLES.md's no-Git-hooks fixed choice is explicitly amended with attribution, and budget-exception lines exist for all five new mechanisms in CHANGELOG/mechanisms.yaml. The mechanism counts themselves were not recomputed."
  architecture-conformance: "N/A — no ratified ARCHITECTURE.md exists in this repository."
  deliberate-simplification: "PASS_WITH_NOTES — native hook limits (push.py:31-33) and the Stop deadline are annotated with ceilings. The unpaginated state=all PR read (publish.py:415-417) has no ceiling annotation but fails closed (non-complete)."
  deletion-first: "PASS_WITH_NOTES — the change reuses publish/land/push/github_rules with no new command module or recovery registry; the only excess shape is the self-contained server harness in test_github_rules.py, raised under tests."
findings:
  - severity: important
    dimension: correctness
    anchor: "loom-code/scripts/loom_checker/command_handlers/publish.py:340"
    text: "issue (blocking): observe_delivery returns `unauthorized` for every published/merged goal whose committed intent lacks `publication: automatic`, before reading any Git/PR evidence. A change published through the still-supported `publish --confirm-authorized` route (ship/SKILL.md:193-196) therefore can never be observed as published, although Ship's handoff (SKILL.md:310-314) requires this observation before reporting delivery. The remedy 'Obtain publication authorization in the committed intent' points the agent at the intent's grant field, conflating read-only observation with authorization, which REQ-2 says to keep separate."
    fix: "Drop the `_intent_authorizes_publication` gate from observe_delivery (publish.py:340-345), since _delivery_stop already gates at publish.py:513. Record the authorization kind in `evidence`, and return `unauthorized` only when no matching PR is observed, with next 'obtain one publication decision from the user; do not edit the intent's publication field'. Extend test_missing_authorization to assert that an existing matching Ready PR still observes as `published`."
  - severity: important
    dimension: correctness
    anchor: "loom-code/scripts/loom_checker/command_handlers/publish.py:526"
    text: "issue (blocking): spec.md:32 requires the Stop block to carry conditional next-action guidance, as the adopted complexity-review correction specified. The block reason here is only `Delivery incomplete (<state>): <reason>\\nnext: <observed.next>`, e.g. 'Resume authorized publish for this feature branch.' Every Build turn that ends on a legitimate user question (external-review egress consent, NON_CONVERGENT escalation) is blocked with an unconditional instruction to continue toward publication."
    fix: "Prefix the block reason at publish.py:526 with the spec's conditional clause, e.g. 'If you are waiting for the user's answer or publication was withdrawn, stop again and say so; otherwise: <next>'. Extend test_premature_stop_and_repeat_disclose_actual_incompletion to assert that clause appears in result['reason']."
  - severity: important
    dimension: external-surface-grounding
    anchor: "loom-code/scripts/loom_checker/command_handlers/publish.py:206"
    text: "issue (blocking): classify_checks relies on gh behavior the gh_pr_checks manual does not document: exit 1 with the stderr text \"no (required) checks reported on the '<branch>' branch\" before checks register, and exit 1 alongside valid failure JSON. The extraction deleted the only grounding for this, the cli/cli v2.88.1 checks.go/checks_test.go and issue 7401 citations previously at both the publish and land loops. publish.py now calls `gh pr checks --required` (publish.py:465, 637) with no citation."
    fix: "Restore the version-pinned citations (https://github.com/cli/cli/blob/v2.88.1/pkg/cmd/pr/checks/checks.go, .../checks_test.go, https://github.com/cli/cli/issues/7401) plus the gh_pr_checks manual link as a comment directly above classify_checks at publish.py:202."
  - severity: important
    dimension: tests
    anchor: "loom-code/tests/test_github_rules.py:370"
    text: "issue (blocking): CONFIGURED_SERVER is a policy script written inside the test, and test_configured_server_refuses_direct_update_and_failed_check_then_merges asserts that this same script refuses and accepts. No Loom publish, land, native-hook or github-rules code runs against it beyond a probe assertion other ruleset tests already cover, so it cannot fail for any shipped behavior; it is a stub replacing the very server seam it claims to cover. Acceptance row 4 is marked `works` partly on this evidence."
    fix: "Delete CONFIGURED_SERVER and the simulated-server half of that test, keeping the existing read-only ruleset assertions. State in acceptance-test-report.md row 4 that refusal of direct trunk updates and failed-check merges is GitHub's server behavior, evidenced only by the live read-only github-rules observation; or replace the fixture with a separately authorized disposable GitHub repository run that captures real refusals."
notes:
  - "Coverage limits: only Read/Glob/Grep were available, so no changed test file was executed and all test results are the owner's supplied observations. loader.js, the agy adapter and untouched callers were inspected only where the changed paths reach them. agent_id/parent_session_id at publish.py:498 were not checked against the cited Claude/Codex Stop docs; if a host sends either on a root-session Stop, the hook silently allows stopping (fails open)."
  - "Bounded claims match the intent/spec: the acceptance report and evidence call the server check a simulation and leave live installed-host Stop enforcement unverified. No path in observe_delivery, _delivery_stop or github-rules performs a write or grants publication/merge authority. classify_checks keeps required-only publish and all-registered land policies distinct with unchanged wait budgets."
  - "Native protection reviewed favorably: preflight before mutation, exclusive creation, managed-byte equality for install/remove, rollback on failure, enforcement scoped to the owning common Git directory, removal that works without default metadata, pre-push destination protection, and no protectMain/no-verify advice. Fast-forward merges and history operations are disclosed and tested as uncovered."
```
