# CLI self-service — acceptance test evidence

Tried on 2026-11-12, in a clean copy of the project at b3204e76a99c2c2af4be8188706f6edab58c051b.

Checkout: `/private/tmp/loom-selfservice-candidate`. Independent acceptance tester; not an implementer. Resolver context: overrides null, inherited failure count 0; no subagents. No full suite run by this tester.

## Setup and identities

- `git status --porcelain` was empty before and after focused checks; `git rev-parse HEAD` returned the candidate SHA above. This disposable clean clone was supplied by the station, not the author's active tree.
- Followed README CLI conventions (lines 255–283): invoked the candidate `loom-code/scripts/loom-python --ready finalize-review --help`. Exit 0, stdout documentation, empty stderr; the existing cached runtime loaded the clean candidate. This is a CLI load/setup check, not a host installation or virgin-machine runtime provisioning test.
- Candidate launcher selected its sibling checker. Operator command metadata retains that absolute candidate launcher while cwd is the historical job checkout. The genuine historical job is fe64dfa7ef283be4becfa95f4b0a3c1fce542a10; diff base 70a05fd73b86c6629a89b816fc45a3ad14a509ed. Its resulting content digest is 58ad98b9d6a93338be10dc1c022a3767c47859e2. Its retained historical report has tested_commit 0dcaa4bda4bc2ed44e567e883ab0f357ed1c64b8. None of these is an attestation of candidate implementation b3204e76.
- Durable raw data: `acceptance-raw-commands.json` holds the 15 operator captured commands (argv, cwd, start, exit, stdout, stderr), original reviewer YAML and provenance, converted input, resulting artifact, liveness observations and explicit reconstruction limitations. Tester command captures are retained there separately. No executable probe or replay harness was added.
- The frozen expectations were read from `/private/tmp/loom-selfservice-acceptance-expectations.md` after the operator had completed. The operator reports receiving only allowed public guidance and authentic job material; no prebuilt input or implementation/tests/spec/plan were read. This is the observed bounded first-use exercise, not a claim that every future agent can succeed.

## 1. Independent discovery and preparation

- Evidence: raw `help-finalize`, `help-publish`, `help-delivery`, `reviewer-count`, `review-input.json`, `valid-finalize-escalated` and the retained operator report.
- The operator assembled two real reviewer records and the original executable adversarial declaration. The candidate finalized the historical job with exit 0 and announced its new attestation. Stderr showed package-tests started/passed and adversarial started/passed. The operator did not independently invoke the full package command.
- Independent authenticity checks compared SHA-256 of all four raw supplied files to the recorded hashes: all matched. Every original YAML key/value equals its corresponding converted verdict field, and both attestation verdicts equal the input verdicts. Attributed identities remain cli_code_review and cli_skill_review, vendor codex, model inherited. PASS_WITH_NOTES, the unresolved code-review nit, dimension scores, notes and both SHA fields were preserved. No outside-review receipt was invented.
- Candidate runtime and reviewer model/effort are not the same claim: supplied inherited model is retained, but concrete host model routing was not independently observable.

## 2. Recovery from caller-correctable errors

- Raw `broken-finalize`: exit 2, `cannot read review input: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)` followed by the finalize help hint. Input was the supplied incomplete JSON opening, not a hidden complete answer.
- Subsequent input was independently assembled from authentic YAML. System Python lacked PyYAML; first conversion failed and a subsequent finalize command saw a missing file (exit 2). Offline uv conversion then encountered cache permission denial before its approved retry succeeded. Valid finalization likewise first failed at collection (exit 1) before approved retry of the same command succeeded.
- Raw captures preserve the scenario failures and retries. `setup-failures.md`, embedded in the durable bundle, explicitly marks initial inline conversion traceback, setup reads and denied ps query as reconstructed from visible tool output, not raw subprocess captures. The retained conversion script is not a byte-for-byte recording of the original inline shell command.
- This proves eventual unaided command/input recovery with environment repair, not pristine first-attempt success. Parent's late evidence-recording reminder came after all scenarios and supplied no operational solution; its exact text is retained in the operator report.

## 3. Complete, waiting, blocked and unconfirmed

- `liveness.jsonl`: same exec session 34992 remained running without an exit file; stderr initially only said package-tests started. At 172 seconds it still ran; completion observation around 230 seconds found exit 0 and both final stage results. No heartbeat inside the child or live test count was claimed.
- `publish-no-authorization`: exit 2; `--intent or --confirm-authorized is required for publication authorization`. The historical intent has an automatic-publication line, but no authorization-bearing invocation argument was supplied. The task forbade all remote writes. This is missing invocation authorization, not a real run against an unauthorized intent.
- `delivery-published`: exit 1, state unconfirmed, complete false, reason trusted GitHub origin and gh are required. Operator did not turn this into permission to publish or invent a remote.
- `delivery-local-before-completion` and `delivery-local-after-finalize`: exit 0/local/complete true because work was committed locally. The first occurred during finalization; operator correctly distinguished local delivery from verification completion. The fresh attestation remained untracked in the disposable job.

## 4. Compatibility, evidence and authorization

- Independent focused invocation: `uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_loom_checker_cli.py loom-code/tests/test_loom_publish.py loom-code/tests/test_selection_finalize.py -q` in the clean candidate.
- The first attempt exited 2 due to uv cache lock/temp permission denial; its stdout/stderr are retained, followed by the approved retry result. No product repair was made.
- Approved retry exited 0: **180 passed in 79.83s (0:01:19)**, no skips. This result covers all three named focused modules and the spec-flow tests listed below. Candidate status remained clean afterward.
- Relevant checks exercise actual public entry, valid outputs and exit statuses, genuine authorization requirements, rejected evidence, stage progress, no-checks distinction and failed/partial publication observations. Remote responses are controlled in tests; no actual remote publish was executed.
- Full package command, reserved for formal finalization: `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`. That automated suite runs before acceptance and blocks on failure. Build's suite result is separate evidence and is not relabelled as this tester's run.

### Retained spec flow coverage

| Flow | Executed evidence |
|---|---|
| Discover | test_help_covers_commands_without_claiming_validation; test_covered_help_is_discoverable_and_explains_inputs |
| Command help | raw three command help calls; tester clean launcher help; outside-repo and exact short/long forms in test_covered_help_is_discoverable_and_explains_inputs; handler exclusion in test_exact_help_never_dispatches_handlers |
| Missing data | raw broken-finalize and corrected-finalize; test_usage_and_evidence_rejections_keep_diagnostics_and_add_one_hint |
| Rejected evidence | test_usage_and_evidence_rejections_keep_diagnostics_and_add_one_hint submits parseable empty evidence, expects BLOCK and exit 1; test_finalize_exit_zero_invalid_evidence |
| Refused publication | raw publish-no-authorization; test_publish_requires_authorization_and_absolute_body; test_unrelated_intent_cannot_authorize_attested_change; test_untracked_or_mutated_intent_cannot_authorize |
| Waiting | raw same-process liveness; test_finalize_progress_before_child_exit; test_publish_progress_before_wait |
| Partial or unknown | raw delivery-published; test_incomplete_delivery_keeps_json_stdout; test_retry_after_pr_creation_failure_does_not_repush |
| Empty CI | test_publish_reports_registration_grace_expiry_as_no_checks_registered; test_help_explains_outcomes_and_authority |
| Complete | raw valid-finalize-escalated and delivery-local-after-finalize; test_dispatch_preserves_success_internal_errors_and_hooks |
| Invalid help shape | test_nonexact_help_forms_retain_normal_rejection |
| Redirected streams | raw separately captured stdout/stderr; test_incomplete_delivery_keeps_json_stdout; test_dispatch_preserves_success_internal_errors_and_hooks |

## 5. Evidence integrity and boundaries

- Essential command streams and original review data are committed in the JSON bundle, rather than relying only on disposable absolute paths. The bundle copies actual retained data; it does not invent missing streams.
- Initial reads, first conversion traceback and ps denial were reconstructed; core help and scenario calls were captured directly. Setup repairs and the late parent evidence reminder are disclosed. No efficiency percentage, token saving, cross-host guarantee, installed-host routing, real remote publication or first-attempt success is inferred.
- No skip instruction was found in the intent/plan. The station reports no dismissed important findings. Candidate full package suite and formal finalization remain station responsibilities; historical artifact execution does not discharge them.
- No user data migration occurred. The operator wrote only disposable job artifacts; this tester wrote only acceptance publication metadata in the source checkout. No product/test edit or commit was performed.
