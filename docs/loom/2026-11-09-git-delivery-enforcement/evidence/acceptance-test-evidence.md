# Git delivery enforcement — acceptance test evidence

Tried on 2026-11-09, in a clean detached worktree at cdae36b6eb85eb98f59836ff5ba1253428e60a7b.

## Setup and execution

- Created with `git worktree add --detach /private/tmp/loom-acceptance-independent cdae36b6eb85eb98f59836ff5ba1253428e60a7b`; initial `git status --porcelain` was empty.
- Read root AGENTS.md, README Install, intent, spec, acceptance tester contract and report template. README describes host plugin installation; avoided overwriting existing host installations. Loaded the clean checkout's packaged OpenCode entry through its executable Node loader harness and ran the resulting shell command. This verifies packaged loading, not installation into an actual running host.
- Focused command: `UV_OFFLINE=1 UV_CACHE_DIR=/private/tmp/loom-delivery-uv-cache uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_delivery.py loom-code/tests/test_delivery_stop.py loom-code/tests/test_native_git_protection.py loom-code/tests/test_native_ambiguous_branch.py loom-code/tests/test_github_rules.py loom-code/tests/test_adversarial_blocked_publish_routes.py loom-code/tests/test_land_merge.py loom-code/tests/test_loom_publish.py loom-code/tests/test_opencode_loader.py -q`.
- Captured result: `175 passed in 60.51s`. No full suite was run by this tester. Required later suite: `python3 scripts/run_package_tests.py --loom-family`, owned by finalize-review.
- Independent supplemental probes at `/private/tmp/test_acceptance_delivery_extra.py` reused isolated repository setup, then supplied empty PR responses, mismatched identity, pending, cancelled and unknown check states. These are simulated remote responses, not live GitHub actions. The initial empty-PR probe incorrectly supplied `[{}]`, which correctly produced unconfirmed; corrected the probe to supply `[]`, without changing product code.
- Supplemental command: `PYTHONPATH=loom-code/tests:loom-code/scripts UV_OFFLINE=1 UV_CACHE_DIR=/private/tmp/loom-delivery-uv-cache uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest /private/tmp/test_acceptance_delivery_extra.py -q -s`; corrected probe result: `5 passed in 2.85s`.

## 1. Observed delivery

- Executed test_delivery: exact PR/HEAD yields published and merged; newer local HEAD yields unpublished; staged, deleted and untracked attributable paths yield uncommitted; remote timeout yields unconfirmed.
- Supplemental probes: empty PR list -> missing_pr; foreign branch -> mismatched_pr; pending checks -> pending; cancelled -> cancelled; unknown -> unconfirmed. Each returned exit 1 and complete false, with reason and next action. Published/merged cases returned exit 0.
- Direct CLI in the detached clean checkout: `python3 loom-code/scripts/loom_checker.py delivery --goal local --json` returned exit 1, state unconfirmed, complete false, reason `a safe symbolic feature branch is required`, with preserve-work guidance.

## 2. Authorization

- test_local_without_network asserted no external calls for explicit local completion and retained unrelated untracked work.
- test_missing_authorization asserted unauthorized, incomplete and no external calls after working-copy withdrawal.
- test_loom_publish authorization tests exercised committed, foreign, missing and modified intents before network writes. Delivery fixture asserts no push/create/edit/merge/fetch calls for every observation.

## 3. Native Git protection

- Executed real git init/clone/commit/push/merge/worktree actions in temporary repositories through test_native_git_protection and test_native_ambiguous_branch.
- Verified compound shell main commit refusal, trunk-destination push refusal, no-ff merge commit refusal, feature commits/push, linked worktrees, foreign hooks unchanged, conflict refusal, edited-hook removal refusal, and ordinary fast-forward synchronization.
- Same-name tag regression passed. Fast-forward local history updates remain outside selected hook coverage, as explicitly demonstrated by the test. No hook was installed in a real user repository.

## 4. Remote rules

- Independent read-only live command: `python3 loom-code/scripts/loom_checker.py github-rules`, using existing gh authentication, exit 0.
- Exact output: `loom: main requires a pull request (administrators included) and the check "loom-pr-floor / PR floor"`.
- test_github_rules executed setup output and classification with missing, malformed, inaccessible and bypass-enabled rule responses; all passed.
- Did not attempt live direct-main push or merge with failing checks, and did not change server rules. No server-refusal fixture was executed as a substitute. Therefore the configured-server refusal portion remains unverified; the live rule read alone does not establish that attempted operations were refused.

## 5. Publication and merge outcomes

- test_loom_publish and test_land_merge executed isolated command handlers with captured external-call responses for success, terminal failure, pending polling, malformed/inaccessible diagnostics, timeout and changing identities.
- Supplemental observations captured pending/cancelled/unknown results without completion. Existing failed-json test exercised gh exit 1 with a valid failed-check JSON response.
- Passing tests verify no unsafe fallback in refusal paths; no real publication or merge occurred.

## 6. Reasons and remedies

- test_actionable_result returned uncommitted paths and commit guidance; test_protection_remedy required remote-set-head repair advice and excluded no-verify advice.
- Supplemental missing/mismatched PR output: `Inspect the PR identity and resume authorized publish; preserve the feature branch.` Pending output: `Continue bounded check observation; wait for a terminal result before proceeding.` Unknown output: `Inspect gh authentication, permissions and response diagnostics; retry the same route.`
- Detached CLI preserved work instead of treating missing branch evidence as completion.

## 7. Host and policy integration

- test_packaged_opencode_delivery_executes_without_claiming_stop loaded root index.js, fired context, extracted its packaged delivery command, fired execute.before, and executed the shell command. It returned unconfirmed/incomplete with next action and explicitly disclosed unverified OpenCode/Antigravity termination enforcement.
- test_delivery_stop executed hook JSON handling for premature stop, repeat, user confirmation boundaries, irrelevant child hooks and total deadline. This tests actual hook handler behavior, not an installed host's termination trigger.
- Native Git behavior is independent of model, host and change size; the same hooks ran actual Git actions. No live Claude/Codex/Antigravity Stop event was exercised. Loader/API test fixtures are not a live host claim.

## Finding

- important, Acceptance 4 / REQ-4: live protection configuration was observed, but refusal of a direct trunk update and a merge with failed required checks was not exercised. Close with a separately authorized disposable configured server environment and captured refusal output. Do not label this requirement fully verified from configuration or simulated CLI responses.

## Re-run on 2026-11-09, at 025f2f7726dbfc73dd357eae73464138dea81047

- Created new clean detached worktree `/private/tmp/loom-acceptance-independent-r2` at the exact tested commit; initial `git status --porcelain` was empty. Re-read README installation instructions and exercised packaged loading again through the actual OpenCode context -> execute.before -> shell command harness. No installed host settings were changed.
- Reviewed full fix diff `bbdfd022..025f2f77`: only plan F06 documentation and 94 added lines in test_github_rules.py; no runtime code, prior tests, manifest or host definitions changed.
- Command: `UV_OFFLINE=1 UV_CACHE_DIR=/private/tmp/loom-delivery-uv-cache uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_github_rules.py loom-code/tests/test_opencode_loader.py::test_packaged_opencode_delivery_executes_without_claiming_stop -q`.
- Captured result: `20 passed in 8.43s`. This includes every remote-rules classification/setup/bypass/unknown case and the newly configured-server refusal case. No full package suite was run by this tester; finalize-review still owns its mandatory run.
- Independent live read-only command `python3 loom-code/scripts/loom_checker.py github-rules` returned exit 0: `loom: main requires a pull request (administrators included) and the check "loom-pr-floor / PR floor"`.
- 1: carried over — diff adds only the remote-rules fixture and plan entry; delivery observer and existing state tests are unchanged.
- 2: carried over — no authorization, local-goal or publication implementation/test changes.
- 3: carried over — no native hook implementation/test changes; added simulated remote does not install protecting client hooks.
- 4: re-tested — complete remote-rules module covers read/setup, absent, bypassed, unreadable and malformed rules. New `test_configured_server_refuses_direct_update_and_failed_check_then_merges` runs a separate policy-deciding subprocess against the identical responses.json used by production observation. Its unprotected client prepares actual Git objects in a temporary bare remote. A direct request is rejected because PR is required; a merge request is rejected because the configured required check fails; each refusal asserts trunk unchanged and PR unmerged. Changing that check to success allows the merge request, updates trunk and marks PR merged. Thus the fixture is configuration-driven with negative and positive controls, not a canned rejection or a client-side precheck.
- 5: carried over — publication/land runtime, checks and existing tests unchanged; added server test does not change these paths.
- 6: carried over — reason/remedy runtime and existing coverage unchanged; new server fixture has no effect on production output.
- 7: carried over — host definitions, loader and policy unchanged; packaged loader setup was nevertheless repeated successfully. Actual installed-host stop enforcement remains unverified.

### Finding resolution and limits

- Earlier important Acceptance 4 finding is resolved by the allowed configured-server simulation, not dismissed. Spec explicitly permits a configured fixture; live GitHub refusal is not required to satisfy this chosen verification boundary.
- The fixture requests go to a local Python subprocess that applies policy then calls update-ref; they are not Git receive-pack transport requests or GitHub API calls. It proves the simulated server decision contract and stable refs on refusal, not GitHub implementation, transport-level interception, credentials or enforcement against a client that directly modifies the fixture's filesystem. No real server write was attempted.
- Live GitHub configuration was independently read; actual live direct-push rejection and failed-check merge rejection remain untested, as do installed-host Stop triggers. These limitations are retained rather than conflated with the configured simulation result.
- No remaining important finding in the scoped Acceptance 4 simulation obligation.

## Re-run on 2026-11-09, at b16dd51c945dee7f59a8ff689ceebdf26881e8c6

- Created fresh detached worktree `/private/tmp/loom-acceptance-independent-r3` at the exact tested commit. Initial and final `git status --porcelain` were empty. Re-read README Install and repeated the packaged loader's context -> execute.before -> actual shell execution setup, without modifying installed hosts.
- Inspected the entire `53e54d48..b16dd51c` diff. Runtime change is limited to shared mixed-terminal-check remedy text; category, issue selection and wait behavior are retained. Other changes add the mixed-case assertion, remove a redundant capture prose assertion, add an official Git hook source comment outside NATIVE_HOOK bytes, and record plan fixes.
- Re-ran all seven Acceptance surfaces rather than carrying any row over. Focused command: `UV_OFFLINE=1 UV_CACHE_DIR=/private/tmp/loom-delivery-uv-cache uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_delivery.py loom-code/tests/test_delivery_stop.py loom-code/tests/test_native_git_protection.py loom-code/tests/test_native_ambiguous_branch.py loom-code/tests/test_github_rules.py loom-code/tests/test_adversarial_blocked_publish_routes.py loom-code/tests/test_land_merge.py loom-code/tests/test_loom_publish.py loom-code/tests/test_opencode_loader.py -q`.
- Captured focused result: `176 passed in 63.11s`.
- Repeated independent supplemental missing/mismatched PR and pending/cancelled/unknown-check probes: `PYTHONPATH=loom-code/tests:loom-code/scripts UV_OFFLINE=1 UV_CACHE_DIR=/private/tmp/loom-delivery-uv-cache uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest /private/tmp/test_acceptance_delivery_extra.py -q`; result `5 passed in 3.20s`.
- Capture contract regression command: `UV_OFFLINE=1 UV_CACHE_DIR=/private/tmp/loom-delivery-uv-cache uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-design/tests/spec/test_capture_intent_contract.py -q`; result `27 passed in 0.03s`.
- 1: re-tested — delivery state/identity tests and independent missing/mismatched/incomplete-state probes passed, including non-success for unavailable evidence.
- 2: re-tested — explicit local-goal/no-network and missing/changed publication authorization tests passed; observation assertions prohibit external writes.
- 3: re-tested — actual temporary Git/native hook tests, ordinary sync, hook-conflict preservation and same-name-tag regression passed. Citation-only hook change does not alter emitted hook bytes.
- 4: re-tested — full remote-rules classification/setup tests and configured-server refusal/green-control fixture passed. Read-only live `python3 loom-code/scripts/loom_checker.py github-rules` again returned exit 0 with `loom: main requires a pull request (administrators included) and the check "loom-pr-floor / PR floor"`.
- 5: re-tested — publication/land success, failure, pending, unknown/inaccessible, timeout and identity cases passed. Existing mixed refusal now includes failure, cancellation and action-required checks; all remain refused without a merge request.
- 6: re-tested — delivery/native/publish/land actionable errors passed. `test_failing_nonrequired_check_blocks` asserts the full remedy for each named FAILURE, CANCELLED and ACTION_REQUIRED issue: inspect/fix failures, diagnose cancellation, obtain required approval and rerun only appropriate checks using the existing route. It still excludes passed checks and asserts no merge call.
- 7: re-tested — executable packaged OpenCode loader, Stop handler framing and native Git operations passed; retained capture structural checks passed after the redundant prose assertion was removed.
- No important finding remains from this acceptance run; none was dismissed. Earlier configured-server limitations remain: local subprocess simulation is not live GitHub or Git transport enforcement, and installed-host Stop enforcement remains untested. No real server write or real-project hook installation occurred.
- Full package suite was not run by this tester. Package tests remain mandatory and finalize-review will execute the complete suite and block on failure.

## Re-run on 2026-11-10, at 9b522d3a7035d7a6375bb00a23ebb71ba6a40750

- Created fresh detached worktree `/private/tmp/loom-acceptance-independent-r4` at the exact tested commit; initial and final status checks were empty. Re-read README Install and repeated the executable packaged OpenCode loader setup through context -> execute.before -> shell execution. Existing host installations were not modified.
- Read current intent/spec, F10–F12 plan, earlier acceptance records and the complete untrusted external review plus owner disposition. Inspected `f47322ce..9b522d3a`: read-only observation no longer requires the automatic publication grant; grant evidence and conditional write guidance are separate; first Stop refusal has human-wait/withdrawal conditions; shared-check source citations are restored without classifier behavior changes. No native/server enforcement changes.
- Re-tested every Acceptance row in full using the same nine focused files, rather than carrying changed observer or host behavior over. Command: `UV_OFFLINE=1 UV_CACHE_DIR=/private/tmp/loom-delivery-uv-cache uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_delivery.py loom-code/tests/test_delivery_stop.py loom-code/tests/test_native_git_protection.py loom-code/tests/test_native_ambiguous_branch.py loom-code/tests/test_github_rules.py loom-code/tests/test_adversarial_blocked_publish_routes.py loom-code/tests/test_land_merge.py loom-code/tests/test_loom_publish.py loom-code/tests/test_opencode_loader.py -q`.
- Captured result: `177 passed in 63.92s`.
- Repeated independent missing/mismatched PR and pending/cancelled/unknown-state probes: `PYTHONPATH=loom-code/tests:loom-code/scripts UV_OFFLINE=1 UV_CACHE_DIR=/private/tmp/loom-delivery-uv-cache uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest /private/tmp/test_acceptance_delivery_extra.py -q`; captured `5 passed in 3.02s`.
- 1: re-tested — every prior delivery state/identity case passed. Revised test_missing_authorization first observed uncommitted after working withdrawal; after committing the legacy intent and matching remote/PR HEAD, it observed published and merged with automatic_publication_authorized false. Pending intent changes do not become delivered merely because read authorization was separated.
- 2: re-tested — local goal still makes no external calls. Every delivery fixture observation asserts no push/create/edit/merge/fetch calls. Ready/merged legacy facts are observable without changing intent or creating write authorization. Existing publisher tests refuse legacy publication without an explicit decision and refuse untracked, modified and working-revoked grants before external calls. Stop user-boundary test verifies working-copy withdrawal permits stopping immediately. Thus read-only observation remains available while automatic writer/Stop applicability is revoked.
- 3: re-tested — actual isolated native Git commit/merge/push/worktree/conflict/sync and same-name-tag cases passed; no real repository hook installation.
- 4: re-tested — remote rule read/setup/unknown/bypass cases and configured simulation negative/positive controls passed. No new live read or write was attempted in this rerun. Earlier live read-only configuration evidence remains dated 2026-11-09; no server/native implementation or rule-observation changes invalidate it. The simulation does not establish live GitHub or Git transport enforcement.
- 5: re-tested — publish/land success, terminal failure, pending, malformed/inaccessible and timeout cases passed, including mixed-terminal remedy behavior. Source-grounding repair is comment-only and does not change category or wait policies.
- 6: re-tested — all delivery/native/publication/merge reason/remedy cases passed. New missing_pr_without_automatic_grant case requires an existing explicit decision or a new user decision before writing; it does not advise editing intent to self-grant. First Stop block explicitly says `If you are waiting for the user's answer or publication was withdrawn, stop again and say so; otherwise:` before existing next-action guidance.
- 7: re-tested — packaged OpenCode command actually executed; Stop handler first/repeat, withdrawal/user-boundary, irrelevant-child and total-deadline cases passed. Repeated Stop does not block again; deadline remains 20 seconds, yields unconfirmed and permits stopping. Actual installed-host termination triggers remain untested.

### External important finding disposition received for this run

- The external author rated the configured-server self-testing objection important. The owner did not adopt it as a product defect: retained spec explicitly permits configured simulation, and the user chose the bounded repair-and-review scope retaining that simulation. This is disclosed in the report's decisions section, not silently discarded.
- Independently retain the limitation: the fixture proves its configuration-driven simulated decision contract, with production rule observation sharing that input; it does not prove GitHub implementation or receive-pack enforcement. No inference of live rejection is drawn from its PASS. A stronger live requirement would need separately authorized real-service testing.
- External findings about observation authorization, first Stop feedback and missing source grounding were repaired and independently exercised as above. No new important finding arose from these acceptance executions. The earlier external response did not satisfy the formal output format; this acceptance record is not a formal external PASS receipt and no follow-up external outcome is claimed.
- This rerun is the user's one additional bounded repair/review pass; earlier evidence remains intact. Package tests were not skipped, finalize-review will run, and this tester did not execute the full suite.
