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

## Re-run on 2026-11-12, at 96a577c8a51ce5a07dda6e508a753b9e295d622b

Independent tester: `selfservice_acceptance_followup`, not an implementer. The earlier tester was unavailable in the live agent inventory; this is a fix verification in the existing episode, not a new first-use experiment. The historical evidence above remains attributed to its original candidate and operator.

### Clean setup and diff boundary

- Created `/private/tmp/loom-selfservice-followup-candidate` with `git clone --no-hardlinks /private/tmp/loom-agent-tool-efficiency /private/tmp/loom-selfservice-followup-candidate`. Its HEAD was exactly `96a577c8a51ce5a07dda6e508a753b9e295d622b`; `git status --porcelain` was empty before and after testing.
- Followed the current README launcher convention. All three `loom-code/scripts/loom-python --ready <command> --help` invocations (`finalize-review`, `publish`, `delivery`) returned 0 with documentation on stdout and zero-byte stderr. This checks loading from the clean copy using the existing cached runtime; it does not test a fresh host installation.
- Read the full fix range `16d5f2f213b451c3a1e03f7f6a116a5756ee375b..96a577c8a51ce5a07dda6e508a753b9e295d622b`, including upstream `781fc1cbf49bd0f30b3b93b1156f110a75eeeb72`. The CLI implementation delta changes only the publish exit-2 explanation and local-delivery meaning. The finalize/publish handlers and the three CLI/publish/finalize test modules have no delta. Upstream adds optional research routing, without changing the tested command-input protocol or supplying missing execution evidence. Release metadata advances to 3.69.0.
- Package tests and formal finalization were not skipped. No dismissed important finding was supplied. This tester did not execute the full suite or formal finalization.

### 1. Discovery and preparation — carried over

The command names, input schema, actual preparation instructions and handler behavior are unchanged in this fix range. The new outcome descriptions do not replace any discovery or preparation step; upstream research guidance explicitly reuses adequate evidence and cannot supply missing execution proof. Original first-use evidence therefore remains applicable. This tester did not claim to be a new blind operator.

### 2. Caller-error recovery — carried over

The malformed-input diagnostics, help hint and correction requirements are unchanged. The new authorization explanation does not change the refusal or tell the caller to repair authorization by inventing it. Original unaided recovery evidence is retained, including failed setup attempts; no reconstructed history was rewritten.

### 3. Outcome interpretation — re-tested

The tester read actual help and interpreted the real results below. Focused executions also covered all original outcome surfaces: waiting (`test_finalize_progress_before_child_exit`, `test_publish_progress_before_wait`), stage versus overall completion (`test_finalize_exit_zero_invalid_evidence`), refused authorization, incomplete JSON, no registered checks, and partial remote-write observations. Remote cases in those tests are controlled; they are not live GitHub publication.

Candidate `publish --help` stdout now includes:

```text
exit 1 means blocked or unconfirmed; exit 2 means invocation or authorization
errors, or internal failures. Read the diagnostic to determine the next action;
the exit code alone is not a reason to retry.
```

Candidate command, in the candidate checkout:

```text
loom-code/scripts/loom-python --ready publish --title 'acceptance refusal only' --body-file /private/tmp/loom-selfservice-pr-body.md
exit: 2
stdout: empty
stderr:
publish: --intent or --confirm-authorized is required for publication authorization
Help: "<loom-code>/scripts/loom-python" --ready publish --help (replace <loom-code> with the installed loom-code plugin directory).
```

This is missing authorization in the invocation, not proof that the committed intent lacks authorization. No publication was attempted after the refusal.

Candidate `delivery --help` stdout now includes:

```text
--goal defaults to published. local checks that attributable paths are committed;
it does not check finalization, attestation or verification. published checks the
matching Ready PR and required CI; merged checks merged delivery evidence.
```

To check the exclusion directly, created a fresh clone of the authentic historical job with `git clone --no-hardlinks /private/tmp/loom-selfservice-job /private/tmp/loom-selfservice-followup-job`. Its HEAD was `fe64dfa7ef283be4becfa95f4b0a3c1fce542a10`, status was clean, and `test ! -e docs/loom/2026-11-11-agent-tool-efficiency/attestation.json` returned 0. No test fixture or fabricated review was added. From that historical checkout:

```text
/private/tmp/loom-selfservice-followup-candidate/loom-code/scripts/loom-python --ready delivery --goal local --json
exit: 0
stderr: empty
stdout fields:
state: local
reason: attributable work is committed locally
next: Report the explicit local goal; publication needs separate authorization.
complete: true
evidence.change_id: 2026-11-11-agent-tool-efficiency
evidence.head: fe64dfa7ef283be4becfa95f4b0a3c1fce542a10
```

The absence of an attestation and `complete: true` coexist exactly as the clarified help says. The tester did not interpret this as verification or remote completion. The candidate's own local observation also returned local/true at candidate HEAD despite its old attestation; that is not the evidence used to claim verification passed.

From the clean candidate, whose clone origin is local:

```text
loom-code/scripts/loom-python --ready delivery --goal published --json
exit: 1
stdout fields:
state: unconfirmed
reason: trusted GitHub origin and gh are required
complete: false
evidence.head: 96a577c8a51ce5a07dda6e508a753b9e295d622b
stderr:
Help: "<loom-code>/scripts/loom-python" --ready delivery --help (replace <loom-code> with the installed loom-code plugin directory).
```

This is unavailable remote evidence, not a successful publication and not authorization to write remotely. Raw separated streams remain in `/private/tmp/loom-followup-{local,publish,published,unattested-local}.{stdout,stderr}` and `/private/tmp/loom-followup-help-{publish,delivery,finalize}.{stdout,stderr}`; the relevant observations above are retained in this committed evidence file.

### 4. Compatibility and authority — re-tested

Executed in the clean candidate:

```text
uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_loom_checker_cli.py loom-code/tests/test_loom_publish.py loom-code/tests/test_selection_finalize.py loom-code/tests/test_write_plan_station_text.py -q
exit: 0
223 passed in 80.11s (0:01:20)
```

The raw combined output is `/private/tmp/loom-selfservice-followup-focused.txt`. All four modules passed with no skips; this covers legal calls, output/exit compatibility, authorization and evidence rejection, progress, the three covered command help surfaces and synchronized release metadata. The real refusal and observation calls above complement these controlled tests. Neither the full suite nor formal finalization was rerun by this tester. The existing full-suite command in section 4 remains the formal acceptance-blocking check; Build's separate integrated results are retained in `followup-package.txt` and `followup-adversarial.txt` and are not attributed to this tester.

### 5. Evidence and scope boundaries — re-tested

- `git diff 16d5f2f213b451c3a1e03f7f6a116a5756ee375b..HEAD -- docs/loom/2026-11-12-cli-self-service/evidence/acceptance-raw-commands.json` was empty (0 bytes). The complete original operator bundle, authentic review inputs, failures and reconstruction disclosures remain unchanged.
- This re-run records exact candidate/job identities, raw-output locations and retained excerpts. The report distinguishes carried-over first use from this informed fix verification. Original live waiting evidence is not claimed to have been reproduced; waiting and finalization distinctions were re-exercised through the focused tests.
- No live remote writes, cross-host routing, fresh-machine installation, time reduction or token reduction were tested or inferred. No user working data, implementation, tests or attestation were edited. Both disposable clones remained clean; only this report and its evidence were updated in the active worktree.
- Findings: none.
