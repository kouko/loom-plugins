# Small actual-flow validation — 2026-11-02

## Result

Six fresh-context native Codex executor trials exercised three cases against original and candidate rule bundles. Four trials produced committed attestations that root independently validated at their final HEADs. Two trials stopped at a newly exposed dispatch-profile feedback limitation. This is not six clean full-process passes: one earlier completed run also has a recorded dispatch-feedback deviation, and a later reviewer output was excluded after an execution-scope violation.

The original suspected deletion and store-placement operational failures were not reproduced in the tested cases. Both variants preserved pre-existing permanent tests and current suite paths; both deleted only the deliberately stale new program. The candidate wording is therefore not demonstrated to improve these actual file outcomes.

A separate, concrete protocol defect is confirmed: initial dispatch accepts an unobservable profile and returns `effective_profile: inherited`, but after-execution feedback requires a portable model/effort pair and cannot represent that actual unknown state. Required reviewer replacement is blocked without fabricating settings or evading feedback. Independent CLI reproduction confirms the same gap in both bundles.

## Scope and fidelity

- Boundary: supplied Build hand-off → actual closing-review, real fresh reviewers, actual checker execution, generated/committed attestation and post-commit validation where reachable. Stop before Ship, publication or merge. Capture-intent, write-plan and Build were fixture setup rather than newly evaluated stations.
- Source checkout and local origin/main: `55587449a0473697dee852f0dff69b240ef5d36e`. Source repo remains unchanged. Copied bundle hashes and the two prose-only differences are in `bundle-diff.json`.
- Runtime code is identical between original (A) and candidate (B). No concern-filter optimization is included in these bundles; its earlier performance evidence is a separate experiment.
- Fixture adapts the real `split_groups` function from `scripts/run_package_tests.py`, with an intentionally seeded missing empty-group filter. Actual failing executions precede restoration of the source function. Each trial has a separate repo and local bare origin; no network or package installation was used.
- Graduated trials include an actual committed store probe, actual RED execution, corrected implementation and real Git move to the suite. Earlier direct-suite preparation remains retained as explicitly superseded `setup-v0-repo`, outside active trials.
- That graduation move was fixture preparation before the executor entered closing-review. The executors tested acceptance and preservation of an already graduated suite path; they did not independently choose or perform the graduation move. No end-to-end graduation-decision claim is made.
- Native subagent model/effort identity is unobservable. Dispatch uses the actual packaged oracle's inherited, override-free fallback. This is not a pinned-model or cross-vendor benchmark, not a complete skill activation/cold-reader evaluation, and not a Claude Code/OpenCode runtime validation.
- One execution per variant/case. Trial ordering was not randomized; fixture and protocol clarifications were applied during exploration. Completion counts are not causal A/B rates or population failure rates.

## Actual outcomes

| Case | Original A | Candidate B | Supported conclusion |
|---|---|---|---|
| Existing permanent test; hand-off omits observed result | Inspected base history, retained exact test bytes, ran suite/program, committed valid attestation; one fixture-plan fix and same-reviewer second round | Retained exact test bytes, recovered result by actual run, committed valid attestation | Earlier decision-only deletion was not reproduced with real history and full prerequisite ordering. |
| New stale store program explicitly caught nothing | Deleted only stale program, retained permanent tests, committed valid attestation | Same actual file outcome and valid committed attestation | Candidate preservation wording did not suppress this cleanup case. |
| Defect-catching pytest already graduated | Kept suite path, suite/program passed; actual finalizer accepted path, but its output was not committed after a disallowed reviewer was excluded and replacement feedback failed | Kept suite path, suite/program and both reviewers passed; stopped on unknown-profile feedback before finalization | Placement did not force a move back. Full completion is blocked by feedback, not artifact location. |

Exact Git state and file hashes are in every trial's `independent-state.json`. Aggregation: `results.json`; initial/active fixture provenance: `manifest.json`, `current-manifest.json`, and trial packets. All permanent test files remained byte-identical to their active trial initial HEAD. Only stale cases removed a test program. No trial changed the source plugin or published anything.

## Confirmed finding: unknown fallback cannot feed execution feedback

Severity: Medium workflow continuation defect. Surface: shared dispatch-profile contract and bundled resolver, independent of the two candidate wording edits.

### Source evidence

- `loom-code/scripts/dispatch_profile.py:62-63` represents fallback effective profiles as symbolic `inherited` or `host-default/unverified` values.
- `loom-code/scripts/dispatch_profile.py:134-138` allows an unobservable initial main profile to take that fallback rather than inventing settings.
- `loom-code/scripts/dispatch_profile.py:170-172` requires `last_attempt.profile` to be an object whose model is a portable tier, before it evaluates successful or failed execution.
- `loom-code/references/dispatch-profile.md:64-69` requires after-execution feedback and its effective profile before redispatch. Its success handling also requires a routed outcome for successful execution.

### Actual reproduction

`reproduce_dispatch_gap.py` calls the real copied `loom-python --ready --script dispatch_profile.py` in both bundles. Eight actual CLI calls are retained in `dispatch-gap-reproduction.json`:

| Input condition, per bundle | Result |
|---|---|
| Initial main model/effort unknown, inheritance guaranteed | exit 0; overrides null; effective profile inherited |
| Completed successful feedback carrying that effective value | exit 2; last_attempt.profile must be an object |
| Replacement feedback carrying that effective value | exit 2; same error |
| Schema-only known portable pair control | exit 0; routed |

The executors also tried the truthful unknown-components representation `{model: null, effort: null}`; it is rejected with `last_attempt.profile is not a portable model-effort pair`. Unknown values are not missing observations the host can truthfully replace with an invented portable pair.

### Workflow evidence and strongest counterargument

The graduated baseline needs a replacement after reviewer two self-disclosed historical probe replay outside its assigned scope. The output was excluded, and replacement stopped at the feedback schema error. This is an unambiguous continuation failure under the contract: relabeling replacement as new initial work would evade the feedback requirement.

The graduated candidate applied the stronger reading that every completed result requires feedback even without a retry; both successful reviewers then hit the same representation gap. The phrase “before any redispatch” permits a narrower reading under which a successful no-retry result need not block finalization. Therefore this second stop is policy-sensitive and must not be presented as independent proof that every ordinary successful run necessarily fails. The initial-output/feedback-input mismatch and actual replacement failure remain under either reading.

The four committed records do not eliminate this issue. In particular, missing-result-a used same-reviewer Round 2 after its plan repair, but its logged resolver calls are all new `initial` events: no after-execution receipt is recorded before that redispatch. Its committed attestation validates mechanically, while full shared-dispatch conformance is not established. This is a distinct observed process deviation, not a workaround to endorse.

### Why earlier green tests were insufficient

The existing resolver/contract test modules passed: 37 tests in 0.35 seconds (`dispatch-existing-tests.txt`). The real fallback-to-feedback reproduction still fails. The earlier rule-interpretation pilot did not exercise actual reviewer replacement or the resolver transition. No source repair or new source test has been applied in this validation task.

## Other observations and experimental corrections

- The first missing-result baseline fixture lacked the plan's module-entry marker. Two real reviewers found it; a genuine implementer repaired only that plan line, Build reran mechanical checks, and the same reviewers verified Round 2. This fixture deficiency is not attributed to either rule hypothesis. Unstarted fixtures were corrected before execution.
- Reviewer/environment differences exposed a Python without pytest; an existing verified interpreter was used, with no installation.
- Stale-program baseline hit a local guard during a targeted deletion attempt, then used the safe targeted edit tool. A later report-writing command also hit the guard while quoting the first rejection. The executor stopped tools; root preserved its final return as clearly labeled `executor-return.json`, not a fabricated executor-written `result.json`.
- That executor's final prose understated privacy-scan evidence. Independent auditors/root verified actual scan exit 0 at command-log line 26 before final evidence commit at line 28. The raw log resolves this reporting inconsistency; no missing scan is alleged.
- The graduated baseline's initially generated attestation is untracked, explicitly excluded and non-deliverable because it includes a disallowed reviewer. Structural `validate_attestation` on its bytes can return no errors, but that does not establish committed or semantically conforming evidence. The summary deliberately does not count it among the four validated committed records.
- Controller interventions, scheduling, changed reminders and limitations are preserved in `CONTROLLER-NOTES.md`; these are material limits on causal comparison.

## Revised recommendation

1. Prioritize a separately scoped repair to dispatch fallback/feedback continuity. Preserve unknown state, atomic no-override behavior, reviewer independence and retry limits; do not invent model settings or avoid feedback by renaming a retry. Add actual initial-fallback → feedback/continuation checks, including success, malformed output and exhausted retry budget. Clarify the no-retry success feedback requirement in the same contract.
2. The concern-first filtering optimization retains its separate measured evidence and remains a bounded implementation candidate. This flow study does not measure its end-to-end speedup.
3. Downgrade the original deletion/placement claims to clarity opportunities for the tested situations. Do not describe candidate wording as a demonstrated fix to actual permanent-test deletion or move-back failure.
4. No broad sample expansion, caching or module split is justified by this study. After a targeted repair exists, rerun the failed feedback transition and one complete affected workflow. Expand only if outcomes disagree or a new failure appears.

This small fixture does not cover every definition of “existing” test, every prior-history shape, another language runner or another host. Absence of a targeted incident in these six runs is not proof of universal safety.

## Raw evidence index

- `PROTOCOL.md`, `CONTROLLER-NOTES.md`: scope, oracle, interventions and fidelity limits.
- `current-manifest.json`, `bundle-diff.json`: active fixture and source provenance.
- `results.json`: aggregate executor returns plus independent state.
- `<trial>/packet.json`, `<trial>/handoff.json`: exact input paths and hand-off state.
- `<trial>/command-log.jsonl`, reviewer YAML/JSON and reviewer command logs: actual commands, exits, tests and verdicts.
- `<trial>/result.json` or clearly labeled `<trial>/executor-return.json`: actor report.
- `<trial>/independent-state.json`: root's actual final Git/file/committed-attestation inspection.
- `dispatch-gap-reproduction.json`, `reproduce_dispatch_gap.py`, `dispatch-existing-tests.txt`: independent schema reproduction and existing-test result.
- `audit1.md`, `audit2.md`: independent final evidence challenges; read alongside this report.

No `dogfood-pass` or full-process certification is issued. No production implementation, publication or merge was performed.
