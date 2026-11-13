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
