# Uninterrupted external review — independent acceptance evidence

Tried on 2026-11-13, exact HEAD 862088abdf7c4187b090f1622af5f12776df7e16.

## Environment and setup/load

- Created a new local clone with `git clone --local --no-hardlinks . /private/tmp/loom-acceptance-862088a`; `git rev-parse HEAD` matched the exact SHA above and initial/final pre-test `git status --porcelain` was empty.
- Followed README validation instructions: `python3 scripts/sync_codex_manifests.py --check --all`, `python3 scripts/check_plugin_boundaries.py loom-code`, `python3 scripts/check_plugin_boundaries.py loom-design`, `python3 loom-code/scripts/check-skill-crossrefs.py`; all exited successfully. Boundaries and cross-references explicitly reported OK.
- README Codex marketplace installation would change global installed state and require network access. It was not executed. The clean-copy OpenCode loader tests provide local load evidence, not proof of Codex marketplace installation or fresh-session routing.
- System `python3 -m pytest` failed because pytest was absent. README's isolated uv invocation first hit a read-only default cache; a cache under `/private/tmp` avoided that issue, but dependency download failed with DNS resolution for pypi.org. Used an existing cached Python/pytest environment read-only instead; no production/test repair or dependency installation occurred.
- Focused command: `/Users/kouko/.cache/uv/archive-v0/-9lbSe78TDsFC1yAizQye/bin/python -m pytest -q loom-code/tests/test_external_review.py loom-code/tests/test_external_review_adversarial.py loom-code/tests/test_review_convergence_contract.py loom-workflow/tests/independent-advisor/test_independent_advisor_readmes.py loom-code/tests/test_opencode_loader.py`.
- Observed result: `192 passed in 49.71s`, exit 0, including clean-copy loader execution. These tests ran against the clean clone, not the shared working tree.
- Full package suite deliberately belongs to finalize-review, not this agent: `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`. No full suite result is asserted here.

## 1. A single explicit request continues to a valid review

- Inspected raw controlled actor report, consent and receipt at `/private/tmp/loom-continuation-behavior/named-request-after/` and the cancellation record in its sibling `cancelled-request/`.
- Positive actor receipt identifies claude/sonnet/medium, direct-user-request, the active target and `simulated: true`; report says `early_stopped: false`, one leg, `inconclusive`, and explicitly disclaims live execution. Cancellation records simulator_calls 0, outside_calls 0 and data_transmitted false.
- This independently corroborates the retained behavior record at `caller-behavior-after-fix.md:3-9`. It is inspection of prior raw behavioral evidence, not a newly run fresh-context actor or a live host test. The fixture's inconclusive review does not demonstrate a valid real external verdict.
- Focused contract/runner tests exercise the executable boundary and preserved guidance; they cannot prove model obedience across all supported callers and external services.
- Result: partly. Important evidence gap: final-tree live continuation is absent, anchored at `caller-behavior-after-fix.md:9`.

## 2. Disclosure does not require another answer

- Same controlled actor evidence reaches its adapter without a second answer. Existing live metadata records additional_user_answers_during_execution 0.
- Read final caller contract at `loom-code/skills/external-review/SKILL.md:95-103` and `loom-workflow/skills/independent-advisor/SKILL.md:164-172`: direct consent is distinct from host approval; required second answers fail uninterrupted acceptance. Reading is supporting context only.
- The live call used explicitly approved test scope and destination. Neither it nor the simulator establishes how host approval handles a future terse request. Result: partly.

## 3. Real review in the previously blocking environment

- Independently loaded `/private/tmp/loom-uninterrupted-live-result.json` and hashed its exact `review_output` bytes with SHA-256. Hash `b30352cd9de052b0f2c2a05bbb66ce53ef6736f025a7a878af16c7083008274b` exactly matches `live-execution.json`.
- Raw JSON reports status completed, executor claude, observed_model claude-sonnet-5-5. It contains substantive YAML review output with PASS_WITH_NOTES and actual findings; it is not only a successful preflight. Observed effort remains null.
- Existing execution evidence `implementation-test-evidence.md:14-20` describes Codex host execution and zero additional answers, but the raw provider result cannot independently attest all surrounding user turns. The execution predates the final packet clarification (`caller-behavior-after-fix.md:9`). No repeat real call was authorized or attempted.
- Result: partly; a real prior scoped call exists, while this exact clean tested revision has no end-to-end live evidence. Do not claim host-wide policy change or final semantic completion.

## 4. Failures remain incomplete

- Focused runner and adversarial tests cover missing/stale authorization, discovery/review timeout, failed selections and non-substitution. Named examples: `test_failed_selection_or_execution_never_falls_back`, `test_missing_authorization_source_blocks_discovery`, `test_review_stage_times_out_when_descendant_holds_stdout`.
- No real login/quota/platform refusal was induced; the live call succeeded. Works is bounded to executed deterministic failure-path tests, not a claim of observing every vendor failure live.
- The automated full package suite runs before acceptance and blocks on failure; finalize-review owns that check. No dismissed important findings were supplied.

## Re-run on 2026-11-13, at 712196710c54e3c7a5dc5b7beb436403ccd63772

### Clean setup and observed execution

- Created `/private/tmp/loom-acceptance-7121967` using `git clone --local --no-hardlinks .`; exact HEAD is 712196710c54e3c7a5dc5b7beb436403ccd63772. No source or tests were repaired.
- Re-ran `python3 scripts/sync_codex_manifests.py --check --all`, `python3 scripts/check_plugin_boundaries.py loom-code`, and `python3 loom-code/scripts/check-skill-crossrefs.py` in that clone: all exited 0.
- Local load check: `/Users/kouko/.cache/uv/archive-v0/-9lbSe78TDsFC1yAizQye/bin/python -m pytest -q loom-code/tests/test_opencode_loader.py`: 18 passed in 6.47s. Global installation/fresh host session still not exercised.
- Independently inspected committed final-live packet, consent, result, manifest, caller report, trajectory and validation. Exact source bytes hash to `66490ab8c9ea6d7a496b4660d46b867a768daa6063471cbde8d5ee0c10c57487`, matching the manifest. Raw review_output SHA-256 is `b1006c5c7e38c680186946d248a6f1cbd7bde051de66ab229c8045658db9680a`.
- Trajectory records one 2-second preflight, one 94-second real review, no retries/provider substitution and no further user answer. Actual authorization is the user's explicit accepted-selection, not the natural testcase quoted in mode_basis. These are retained execution records, not an additional call by this witness.
- Result status completed, observed model claude-sonnet-5-5, requested Sonnet/medium; observed_effort null. Medium was accepted explicitly, not independently measured. Actual total cost remains unknown.

### Independent output assessment; original rejection preserved

- Inspected raw output against `loom-workflow/skills/independent-advisor/references/report-contract.md` and binding SKILL report rules, then checked source, rather than accepting the separate adjudication by authority.
- Nonempty output includes all four required card fields, source anchors, distinct mechanisms and reasoning. Mechanically confirmed: Popen lacks env filtering; consent has no expiry or packet digest; agy prompt is in argv; output lists have no byte cap; Claude candidate acceptance lacks a pre-probe executor/family compatibility check. This is substantive audit analysis, not merely input restatement.
- Original caller validation rejected the entire leg as unbacked-claim; its report labels the external text a high-confidence assertion of an actual secret incident. Preserve that rejection and all raw text. This witness disagrees with that stated rationale: the review explicitly presents a read-only source analysis, labels the environment item judgement-call/medium, and lists secret exposure under Failure modes. It does not claim to have observed actual secrets or a remote transmission in this execution.
- Nonetheless, “Other vendors' API keys and tokens reach every CLI” is too categorical in isolation. Only exported variables already present in the parent process can be inherited; whether credentials exist, were accessed, or left the machine is unverified. “Anyone on the host” reading argv is also OS/process-visibility dependent and unverified. No incident or universal privacy guarantee is accepted here.
- Other explicitly speculative scenarios (helper model metadata, prompt echo, PID reuse) remain unverified conditional risks; mitigation cost estimates are external judgement. The authorization discussion omits the selected_executor equality and must not be read as saying that regex alone is the whole authorization check.
- Under the unchanged rejection key, source-supported mechanisms and attributed conditional risks can support a bounded audit; unsupported categorical incident assertions cannot. Witness assessment is evidence only, not an edited replacement for the vendor text or caller report. A delivered usable caller result requires its own explicit reconciliation and limitations.

### Per-row retest scope

- 1: re-tested against final live artifacts and exact source. Single scoped Claude execution now observed; all supported reviewers and natural-request-only host approval remain unverified. Final usable delivery assessed separately from subprocess success.
- 2: re-tested. Recorded disclosures and accepted-selection proceeded without another user answer; this proves the authorized scoped run, not a platform-wide approval policy.
- 3: re-tested. A real final-source Claude review completed in Codex without another answer; output validation disagreement remains explicitly separate from observed execution.
- 4: carried over — source failure-path implementation and tests unchanged; new evidence is successful execution and output assessment, not a changed failure path. No fresh vendor failure was induced. Full package suite remains owned by finalize-review.

### Caller reconciliation independently checked

- Inspected `final-live/reconciliation.md`, `reconciled-validation.json`, and `reconciled-audit-report.md`. The caller withdraws its incident-fabrication interpretation under the unchanged rubric and accepts an explicitly qualified audit, without another external call. It preserves the raw categorical sentence as a warning rather than incident evidence.
- Independently recomputed SHA-256 of original report.md, validation.json, trajectory.json and result.json. All four exactly match `original_observation_files_unchanged` in reconciled-validation.json. Initial rejection remains available, not overwritten or hidden.
- Reconciled report supplies the required fields, attribution of external passages, confidence, concrete proposals, open resolutions, model/effort distinction, unknown actual cost, unavailable history, coverage disclaimer and packet-boundary qualification. It limits delivered findings to source-backed mechanisms and explicit design judgements, and does not turn hypothetical secret presence/remote transmission, OS visibility or speculative CLI behavior into observed incidents.
- Independent assessment: this is an attributable usable qualified audit under the unchanged rubric, not acceptance of every raw vendor sentence or a formal owner verdict. A1 remains partly for cross-service and bare-request host-approval coverage; A2 works for this scoped authorized run; A3 works for final-source real execution plus usable qualified result; A4 remains carried over. No additional test or external execution was necessary for this document-only reconciliation.
