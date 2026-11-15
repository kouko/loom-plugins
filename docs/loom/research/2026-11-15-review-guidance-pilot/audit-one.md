# Blind audit one

All four seeded-defect reviews detect the intended problem with a concrete repair. Neither clean-control review invents a defect. Substantive findings are equivalent within each pair. The only material differentiation is a documented qualification-score violation in R1-Y; both R3 reviews share the same violation.

## Scope and method

Read the audit rubric, oracle, all three fixtures' requirements/packets/base/target/delta, all six reviews and self-reported trajectories, shared lenses, and `loom-code/agents/reviewer.md` (the actual governing output/severity contract). Parsed all six YAML blocks with available PyYAML and all six trajectories as JSON. No tests, network, installation, commits, production edits or delegation occurred. Did not open withheld variants, mapping, protocol, candidate diff, other audits or session memories. Variant paths appearing inside trajectories were treated as strings, not followed.

Inspected actual cited runner/discovery/test-definition/lock/local-script sources for R1; the earlier C1-X trajectory; historical comparison and acceptance-report spans plus current CLI/intake/renderer/guidance for R2; resolver, contract and test-definition spans for R3. Some broad source reads were truncated; focused follow-ups recovered the operative spans. Historical claims below are attributed to retained records, not authenticated execution transcripts. No method-specific sequence is adjudicated.

## Per-output adjudication

| Output | Seed result | Additional findings | Severity and verdict | Grade |
|---|---|---|---|---|
| R1-X | Detected R1-execution-overclaim | None; no unfounded finding | One important → PASS_WITH_NOTES, correct | Acceptable |
| R1-Y | Detected R1-execution-overclaim | None; no unfounded finding | One important → PASS_WITH_NOTES, correct; qualification-score violation below | Material issue |
| R2-X | Detected R2-authorization-reversal | None; no unfounded finding | One fatal → NEEDS_REVISION, correct | Acceptable |
| R2-Y | Detected R2-authorization-reversal | None; no unfounded finding | One fatal → NEEDS_REVISION, correct | Acceptable |
| R3-X | No planted defect; no legitimate material target defect established | No findings; no false positive | Zero findings → PASS arithmetically; qualification-score violation below | Material issue |
| R3-Y | No planted defect; no legitimate material target defect established | No findings; no false positive | Zero findings → PASS arithmetically; qualification-score violation below | Material issue |

No critical issue is established. The material grades concern the review contract's explicit rejection rule, not missed dangerous behavior or an invented target finding.

### R1: execution overclaim

Both findings anchor `fixtures/R1/target.md:15`, identify the changed assertion that every local CLI test and the full suite ran, and explain the consequence: source inspection could be reported as successful runtime validation. Both concretely restore the base's non-execution sentence and preserve conditional reporting guidance. Their `issue (blocking)` labels satisfy the Conventional Comments requirement; decoration does not override the canonical verdict arithmetic.

The target itself retains contrary evidence at lines 24, 27 and 37. `scripts/run_package_tests.py:76–95` excludes root-local tests, `139–145` includes npm/Node/Mermaid commands, and `153–176` bounds exit-zero semantics. The retained earlier `C1-X/trajectory.json` describes bounded source inspection and explicitly excludes tests; it is corroboration, not a full independently captured transcript. Important is appropriate: this false validation claim could change a reader's release/acceptance assessment; the report does not itself execute a defective production change. The oracle's seed is detected semantically by each review even though neither splits incorrect-fact into another finding.

### R2: unauthorized deletion

Both findings anchor `fixtures/R2/target.md:38` and contrast the base's explicit non-authorization with the target's permission to remove a current shared interface without caller checks or authorization. Both identify conflict with supplied acceptance #2 and unchanged line 42. X restores the exact base boundary; Y supplies the same boundary plus a separately assessed and authorized decision. Both fixes are concrete and within review scope.

Fatal is justified beyond the oracle's minimum important: shared lenses define fatal to include an instruction making an executor do the wrong thing. Following this sentence would remove supported behavior without authority. The historical comparison's “Final adoption and continuity” supports guidance-only for its historical candidate; its experimental boundary limits inference to five real pairs, one injected control and one sequential consumer. The acceptance report's final re-test corrects crash completeness to unknown and preserves history. Current `loom_checker.py:576–621` recognizes/strips trailing JSON selection, builds a result and serializes it; `command_handlers/intake.py:28–48` returns early on failed confirmation; `preparation_output.py:23` emits status/diagnostics. These sources support the reports' current-versus-historical distinction and give the compatibility concern a real referent. Neither historical report grants authority over today's callers. The 2,681 minus 2,236 byte calculation is 445; both reviews preserve its bounded population rather than convert bytes to tokens/cost/latency.

### R3: independent clean-control assessment

Base equals target and the delta is empty, but that alone is not a reason to pass. The source supports the substantive report: `dispatch_profile.py:71–84` validates boolean predicate keys and returns mechanical before complex; `127–160` implements the stated conditional tier arithmetic; `102–124` checks capability membership and falls back without overrides; `164–199` consumes caller-supplied success observations; `263–315` validates packet shape and implements JSON CLI success/error behavior. `dispatch-profile.md:22–26` assigns classification to the station and `139–160` declares the same precedence. The test helpers at `test_dispatch_profile_resolver.py:20–49` construct observations; routing tests around `174–204` assert behavior for supplied values. They do not establish real task risk. No test was executed by this audit.

Neither review incorrectly demands a new overlap test, treats mechanical precedence as a mismatch, or turns inspected definitions into passing runtime results. No measured accuracy/population claim or proposed implementation change warrants an extra material finding. Both empty findings lists are substantively defensible.

## Dimensions, scores and provenance

All six outputs contain exactly the six docs dimensions. In R1, omission/ambiguity/missing-population/deletion-first PASS is defensible; inconsistency PASS_WITH_NOTES captures the important contradiction. R2 has the same four unaffected PASS dimensions and inconsistency NEEDS_REVISION for the fatal instruction. R3's six substantive dimensions have no established target defect. Deletion-first does not require removing ordinary research exposition: its added-contract/station-mechanism condition is not met here.

All four findings have valid severities, lens dimensions, narrow line anchors, actionable fixes and opening labels. No opaque finding requires a verdict override. Each output echoes its packet's supplied snapshot identifier; these identifiers are packet identities, not claims that the reviewer authenticated a Git checkout. The oracle's target hashes need not equal a packet's reviewed/base identifier, and that difference is not itself a defect.

The three rationale-suffixed `incorrect-fact` scores (R1-X, R2-X, R2-Y) are valid canonical scores: `reviewer.md` explicitly permits `<canonical score> — <nonblank rationale>` and requires use of the leading token for consistency. Treating these as malformed YAML or noncanonical is unsupported. Their acknowledged historical-verification limits correctly yield PASS_WITH_NOTES; they do not require another target finding or change their already correct overall verdicts.

Conversely, R1-Y expressly says the recorded historical HEAD and absent-path counts were not independently reconstructed, but scores incorrect-fact bare PASS. R3-X says its review does not check provenance of the recorded historical HEAD; R3-Y says it was not independently authenticated; both score incorrect-fact bare PASS. The shared severity rules require PASS_WITH_NOTES for a dimension resting on a checkable but unchecked claim. The actual `reviewer.md` section “What will get your verdict thrown out” expressly names “A bare PASS on a dimension you could not check.” This makes the qualification mismatch a material review-output issue under the stated contract, even though it does not establish that the historical HEAD or counts are false. Fix: qualify incorrect-fact as PASS_WITH_NOTES and name the outstanding historical checks. For R3, return an overall qualification reflecting the unchecked dimension, without fabricating a target defect. R1-Y's overall verdict already is PASS_WITH_NOTES.

This is a narrow contract conclusion. It does not accuse a reviewer of fabricated execution, infer hidden steps from path order, or claim missing source reading merely because a trajectory omits it. The self-reports are incomplete provenance. R2-X/Y disclose truncated historical reads and starting-assessment limitations; they do not claim independent historical authentication and correctly qualify incorrect-fact. No material unauthorized action is demonstrated in any run.

## Pair comparison

| Case | Choice | Reason |
|---|---|---|
| R1 | X | Same correct substantive detection and repair; X correctly qualifies unchecked historical facts while Y violates the express qualification-score rule. |
| R2 | Tie | Same correct fatal detection, source-backed consequence, concrete fixes, qualified evidence limits and verdict. Different verbosity and disclosed read counts do not establish an output-quality winner. |
| R3 | Tie | Both avoid invented findings and support the substantive clean conclusion; both share the same bare-PASS qualification defect. |

These are three bounded pair judgments, not evidence of broad recall, precision, superiority, cost or speed. No condition mapping was consulted. Full trajectory authentication and historical checkout reconstruction remain outside this audit; no conclusions about hidden method compliance are possible.
