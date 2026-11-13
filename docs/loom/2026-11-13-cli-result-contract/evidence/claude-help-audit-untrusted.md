# Claude Code help audit consultation

## divergence_points

Externally authored, untrusted findings were returned by Claude Code and then
checked against local source by the incumbent executor. No implementation or
test was changed. Initial verdict and finding text remain preserved verbatim
in `/private/tmp/loom-help-claude-review.json`.

| ID | Kind / confidence from Claude | Local assessment and proposed change | Resolution |
|---|---|---|---|
| DP-1 | factual-error / 0.70 | Substantially confirmed: publish title parsing enforces nonblank text, not Conventional Commits; its base is obtained from the server, and the vague help claim of origin/HEAD reconciliation and branch/title checks overstates the checker. Replace it with actual literal-origin, symbolic-branch, remote-ancestry and unchanged-identity checks. The temporary body snapshot is real; existing help does not say it persists, so that part is not itself a defect. Sources: command_handlers/publish.py:149-150,774-781,829-907; loom_checker.py publish help. | open; no edits |
| DP-2 | judgement-call / 0.65 | Confirmed omitted input constraint: rule_checks/publish.py:127-153 requires the nine headings in fixed order and rejects additional level-two headings. Clarify this in help. Minimum content also rejects one ASCII token and placeholders, so adding only an eight-character rule would be incomplete. | open; no edits |
| DP-3 | judgement-call / 0.60 | Confirmed misleading wording: DeliveryResult.state at command_handlers/publish.py:273-276 contains no blocked value. Distinguish generic blocked conditions from actual state values; document the real state set or remove the implied enum value. | open; no edits |
| DP-4 | judgement-call / 0.55 | Confirmed useful scope clarification: push.py DIRECT_GIT_CHANGE matches literal git followed immediately by commit/merge/push at command start; global-option, wrapper and compound-command spellings can evade this host matcher. Native safeguards have documented fast-forward/reset/rebase limits. Qualify protection scope without redesigning it. | open; no edits |
| DP-5 | judgement-call / 0.55 | Confirmed useful operational omissions: land.py:900-961 matches the accepted name to intent originator/authorizer, 1052-1096 polls all registered checks with a 360x10-second pending bound, and 192-195 discloses stale/absent verification after merge rather than refusing it. State the poll bound without promising a strict wall-clock maximum: network call time and other stages add elapsed time. The emitted next: cd after deleting the invoking worktree is also worth disclosing. | open; no edits |

## findings

Additional externally authored suggestions, kept separately from the material
divergences above. Their original confidence, source anchors and reasoning are
in the raw review; all begin with resolution open.

| IDs | Local assessment | Resolution |
|---|---|---|
| F-1, F-2, F-3 | Source reasoning supports exact-help bypass, ready/repair distinction and corrected local opt-out/native effects. No new dynamic execution was performed by Claude. Literal ./--help operand and shared Git hook directory explanations are optional refinements. | recorded; no edits |
| F-4 | Confirmed github-rules can return template-not-on-trunk before evaluating rules; setup text may appear without --print-setup. A useful missing outcome. Source: github_rules.py:221-289. | open |
| F-5 | Confirmed conditional interface recomputation needs resolvable branch base, and intake.confirmed rejects closed/delivered/indeterminate intents. Helpful prerequisites omitted by generic wording. Sources: helpers.py:331 onward; rule_checks/intake.py:802 onward. | open |
| F-6, F-7 | Contract recovery should distinguish upgrading loom-code from upgrading a stale consuming requirement. Standing wording could distinguish file existence from document-content checks. These are wording refinements, not evidence that checks are wrong. | open |
| F-8, F-9 | Confirmed delivery may succeed when no required checks exist (publish.py:492-495); publish uses upstream-tracking push flags and a temporary snapshot; finalization writes an attestation that must subsequently be committed. Useful outcome/effect clarifications. | open |
| F-10 | No new material defect alleged; optional intents detail-column precision. Handler-level reading leaves internal validation coverage gaps. | recorded |
| F-11 | Correct limitation: keyword assertions and safe help execution do not establish that every statement is true. Initial help checkpoint remains historical evidence, while these additional content findings reopen semantic correction before JSON expansion. | accepted assessment |

## verdict

Claude returned **challenger-preferred**. Local assessment agrees that the help
checkpoint should not be treated as semantically closed until the material
corrections above are addressed. This is an audit consultation, not a formal
closing-review verdict or attestation. The incumbent PASS and original failed
checkpoint are retained separately in the repository; neither is rewritten.

## leg_count / early_stopped / degraded_legs

- leg_count: 1 outside review plus its required short preflight.
- early_stopped: false; review completed after approximately 6m04s.
- degraded_legs: none. The rejected first tool invocation never launched an
  external process; after explicit additional consent, one execution ran.
- No blind comparison, normalizer or opposite-order judging was applicable to
  this single-leg audit. This consultation makes no blindness claim.

## executor_provenance

- CLI: Claude Code, via installed loom-code 3.72.0 external-review skill.
- Requested: sonnet, high effort, Anthropic family.
- Candidate source: alias-or-explicit-id.
- Preflight: exit 0; observed model claude-sonnet-5-5, provider firstParty.
- Review: status completed; observed model claude-sonnet-5-5.
- Evidence level: accepted-explicit-settings. Model family was observed;
  effective effort was not independently exposed (observed_effort is null).
- Packet prepared at ccbc162c08ed155ae612d1b5d959fc1921d56fd8; HEAD did not
  move during consultation. This identifies prepared material, not a claim
  that the entire tree was reviewed.
- Execution JSON: `/private/tmp/loom-help-claude-execution.json`.
- Consent: `/private/tmp/loom-help-claude-consent.json`.
- Packet: `/private/tmp/loom-help-claude-packet.md`.

## actual_cost

Unknown total: the runner exposes the preflight client estimate of USD
0.0086063 but does not expose the review's billed total. The preflight estimate
is not the total charge, and cannot establish the actual bill.

## known_weaknesses

This was static reading, not command execution. Claude reported inspecting all
sixteen command help pages, but explicitly did not read the intent/spec/plan,
initial checkpoint and several checker internals; see raw coverage.not_checked.
The outside output parsed as JSON with all requested fields, sixteen named
commands, nonempty source-grounded reasoning and findings; it was neither a
refusal nor a repeated input. Referenced key code assertions were checked
locally. Optional suggestions were not automatically accepted as defects.

Agreement between reviewers cannot detect a blind spot shared by them.
Anonymisation and order reversal would not eliminate shared blind spots.

## coverage_disclaimer

The dispatch packet was assembled from listed evidence paths at the pinned
revision. That describes prepared material, not every file the CLI may have
read. Claude model file tools were confined to the review root; CLI startup
could access or write settings and caches outside it, and this consultation
cannot attest which such files were accessed. No model Bash tools or configured
MCP servers were enabled by the runner.

The deterministic pre-dispatch scan covered the packet and found no matches;
material readable within the wider scope_boundary was not subject to that
scan. This is not a safety guarantee about all readable or transmitted data.

Raw verbatim outside output and this report are retained locally under
`/private/tmp/loom-help-claude-*`, subject to the same restrictions as the
dispatch packet. No source edits, full suite, live writer path, release,
publication or merge occurred as part of this consultation.
