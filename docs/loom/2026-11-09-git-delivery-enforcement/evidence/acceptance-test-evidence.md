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
