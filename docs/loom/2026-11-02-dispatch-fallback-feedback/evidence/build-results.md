# Build results

## W1-01 — fallback feedback
- Implementer: `/root/dispatch_resolver_build`; task commit `185d7fd5`.
- Defect-class search: resolver, shared dispatch contract and resolver tests, including all fallback producers and feedback branches. Both object-only feedback and missing effort validation were repaired.
- RED before production edit: root ran the locked isolated uv focused test command; 74 failed, 73 passed. Complete short-trace output: `/tmp/loom-dispatch-w1-red.txt` (local diagnostic).
- GREEN after implementation: 151 passed. Raw output: `/tmp/dispatch-w1-green.log` (local diagnostic). The six added parameterized test functions map to one positive and one negative/boundary test for each of Acceptance 1–3; net test lines +132.
- All pre-existing tests remain. Five fallback origins are covered: unknown main, unverified native effort, unsupported initial target, unsupported redispatch target, and pre-execution host rejection, with both labels and count boundaries.
- Existing symbolic labels are reused; no production module, function, persistent state or record field was added. Resolver net line growth is 15; tests and shared contract add maintenance surface for the previously missing roundtrip and malformed-data guarantees.
- Native task invocation used null overrides and `host-default/unverified`, count 0. After receiving the completed conforming implementation report, root actually fed that symbolic profile to the repaired resolver: `routed/execution-succeeded`, count 0, null requested/override fields. This is genuine feedback on the implementation task, distinct from synthetic profile matrix tests.

## W2-01 — continuation boundaries
- Implementer: `/root/dispatch_continuation_build`; task commit `54bbcaf3`.
- RED: four added contract tests failed while 46 existing tests passed; GREEN: all 50 passed. Raw local diagnostics: `/tmp/dispatch-w2-red.log` and `/tmp/dispatch-w2-green.log`.
- Five planned files changed; convergence tests and intent pin checker unchanged. Net test lines +52, one positive and one negative/boundary test for each of Acceptance 4 and 6. Affirmative prose-pin checks include synthetic negation controls; these are contract checks, not evidence of agent behavior.
- Defect class searched: both intent confirmation paths, Build entry, Closing Review episode/retry passage and station tests. Substantive requirements change, wording-only reconfirmation, same failed task continuity and successful defect-finding reviews now have separate stated handling.
- Root received the completed conforming implementation report and actually fed back `host-default/unverified`, count 0. The repaired resolver returned `routed/execution-succeeded`, count 0 and null overrides.

## Release packet and word-cap repair
- W3-01 implementer `/root/dispatch_release_build`, commit `89acd8f7`: loom-code 3.57.0 and loom-design 2.20.0, six translated plugin READMEs, root README, changelogs, derived manifests and existing version assertions.
- Code release-focused tests: 43 passed. Design-focused tests initially found a genuine integration failure: the W2 capture-intent addition made its body 3,534 words, exceeding the existing 3,500-word cap.
- The W2 implementer shortened only its newly added repeated paragraphs; no test was weakened. Repair commit `9b7d0140`: design-focused tests 27 passed, station/convergence tests 50 passed, capture-intent body 3,500 words. The release worker did not repair runtime source itself.

## Adversarial execution and W4-01
- Independent adversary `/root/dispatch_adversary` tried 11 attack points, one earned a new RED program. Synthetic executions covered 348 symbolic states, 216 malformed-pair states, six native-effort bindings and a three-step exhaustion chain. These are stateless program cases, not live sessions. Six temptation checks were textual only; agent behavior remains for independent acceptance testing.
- Important finding: old `inherited` feedback combined with current `inheritance_guaranteed=false` caused a new malformed-response retry to claim inheritance. The initial design incorrectly preserved a historical label as a new guarantee.
- Actual RED: `test_retry_inheritance_truth.py`, 1 failed; raw local outputs `/tmp/dispatch-adversary-red.txt` and `/tmp/dispatch-w4-red.log`. The adversary authored the program, root committed its exact bytes in `a37d7bb9`, and the implementer never edited it.
- Agent-decided correction: spec commit `a4136c8a`, independently re-reviewed PASS. Completed success and terminal outcomes retain their past label; a new fallback dispatch uses the current guarantee. Requirements, override omission and retry limits did not change.
- W4-01 implementer `/root/dispatch_resolver_build`, commit `4123ff56`: searched fallback calls, shared retry wording and profile tests. Existing retry test gained both lost/restored-guarantee cases; net test lines +6, no new implementer test function. Resolver tests plus unchanged earned program: 154 passed.
- Native feedback for the adversary and each completed implementation task returned `routed`, count 0, with unknown effective settings and no invented overrides. Finding a product defect was successful adversarial work, not a failed agent attempt.

## Graduation and integration hand-off
- W4-02 moved the adversary's program byte-identically to `loom-code/tests/test_dispatch_fallback_inheritance.py` in commit `c9dfca15`; old store path absent. SHA256 before and after: `0d021ba8578de873670ad9efc4163e21b0374d8f7e182f93eb70eed60d033aae`. Actual suite-path execution: 1 passed.
- Initial complete package run found the existing early-Build one-home reference check rejecting the added redundant station name. The W2 implementer cited the unique `review.bounded-episode` rule directly and clarified the new-task subject; commit `7f79a0d4`, relevant checks 52 passed, existing test unchanged.
- Final Build source: `7f79a0d4e4345de027bc51171438b8d7ecaba0fe`; sync-trunk up to date with `origin/main` at `55587449a0473697dee852f0dff69b240ef5d36e`.
- Complete locked isolated package suite exited 0: 4,107 pytest passes and six skips, plus all discovered shell checks. Raw local output `/tmp/loom-dispatch-build-suite-final.log`. Skips are the suite's existing conditions, not user-requested omissions.
- After the suite, the committed permanent adversarial program ran again: 1 passed, `/tmp/loom-dispatch-build-adversarial.log`. The adversary was not dispatched again: the same earned program still catches the same product defect, and subsequent prose fixes did not change its scope.
- Build hand-off: `/tmp/loom-dispatch-build-handoff.json`; no unresolved adversarial findings, no steps skipped. Closing Review computed reviewer floor 2 and began independent acceptance testing only after these checks passed.

## Verification boundaries
Focused tests prove resolver decisions and validation. They do not establish fresh-agent interpretation, complete closing-review behavior, installed cache loading, or Claude Code/OpenCode runtime behavior. Independent isolated acceptance testing and closing review follow Build; historical evidence is not substituted for those checks.
