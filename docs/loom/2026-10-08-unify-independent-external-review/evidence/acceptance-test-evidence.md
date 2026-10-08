# Unified independent external review — acceptance test evidence

Tried on 2026-10-08 in a fresh local clone at `fdeafc46`.

## Clean setup

- Command: `git clone --no-hardlinks --single-branch /Users/kouko/GitHub/loom-plugins /private/tmp/loom-acceptance-20261008`
- Result: clone completed; `git rev-parse HEAD` returned `fdeafc461d885720cceae11c04a450c612c3c228`; `git status --short` was empty.
- README setup checks: `python3 scripts/sync_codex_manifests.py --check --all` exited 0; `python3 scripts/check_plugin_boundaries.py loom-code` returned `OK: loom-code is filesystem-boundary clean.`; the same command for `loom-workflow` returned `OK: loom-workflow is filesystem-boundary clean.`
- The README's full package command was reserved for `finalize-review`. Focused tests used its locked requirements offline. The first sandboxed `uv run` could not open the user's uv cache (`Operation not permitted`); the same offline command completed with narrowly scoped host approval. No package was installed into the base Python environment.
- No plugin was installed into the user's host. Actual host loading and authenticated CLI behavior were not established by these local checks.

## 1. Explicit code, plan, and decision review retains incumbent attribution

- How I tried it: inspected the installed-skill entry files in the clean clone; ran the focused command below and the four finalization cases below. No external CLI was launched.
- Focused command: `uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_external_review.py loom-code/tests/test_external_review_adversarial.py loom-code/tests/test_second_vendor_policy.py loom-code/tests/test_loom_attestation.py loom-workflow/tests/independent-advisor/test_independent_advisor_readmes.py loom-workflow/tests/scripts/test_independent_advisor_compaction.py -q`
- Result: `114 passed in 8.26s`.
- Additional command: `uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_selection_finalize.py::test_selected_outside_review_with_skipped_reviewers_stays_unattested loom-code/tests/test_selection_finalize.py::test_v2_without_selection_keeps_every_floor loom-code/tests/test_loom_attestation.py::test_selected_outside_review_raises_narrow_floor_and_requires_both_families loom-code/tests/test_loom_attestation.py::test_finalize_binds_selected_outside_runner_output_to_verdict -q`
- Result: `4 passed in 3.95s`.
- Named evidence: `test_named_external_review_handoff_preserves_owning_contract_and_consent`, `test_readmes_and_prompts_cover_outside_reviews`, `test_selected_outside_review_raises_narrow_floor_and_requires_both_families`, and `test_finalize_binds_selected_outside_runner_output_to_verdict`.
- Limitation: routing and attribution were exercised by tests and skill-contract checks, not by a real outside coding agent. No complete consent record was supplied for an authenticated dispatch.

## 2. Owning review criteria and verdict format remain binding

- How I tried it: used the same focused test commands above; checked the advisor and closing-review entry files in the clean clone.
- Result: the named handoff and finalization tests passed. `loom-workflow/skills/independent-advisor/SKILL.md:21-45` delegates the review packet and verdict checks to the owning skill. `loom-code/skills/closing-review/SKILL.md:153-196` retains the reviewer lens and YAML contract, and rejects an outside run that lacks a conforming verdict and runner receipt.
- Named evidence: `test_named_external_review_handoff_preserves_owning_contract_and_consent`, `test_finalize_binds_selected_outside_runner_output_to_verdict`, and the 114-test focused run.
- Limitation: no live outside output was available to inspect against the owner contract.

## 3. Nonblocking notice and no execution without opt-in

- How I tried it: `python3 loom-code/scripts/external_review.py --list-candidates --executor codex --scope /private/tmp/loom-acceptance-20261008 --consent-record /private/tmp/loom-acceptance-20261008/absent-consent.json`.
- Result: exit 1; `{"status": "failed", "reason": "consent-missing-or-stale", "executor": "codex", "candidates": []}`. This path rejected before model discovery.
- Named evidence: `test_consent_blocks_all_subprocesses`, `test_missing_host_read_disclosure_blocks_discovery`, `test_missing_host_write_disclosure_blocks_discovery`, `test_agy_candidate_uses_model_family_and_keeps_notice_nonblocking`, `test_resolve_available_returns_nonblocking_notice`, and `test_v2_without_selection_keeps_every_floor` passed in the focused runs.

## 4. Explicit model and effort on three CLIs, with pre-review evidence

- How I tried it: ran the focused command in section 1 against the real runner entry point with simulated subprocess responses for Codex, Claude Code, and Antigravity. The tests inspect the actual command arguments and discovery/preflight/review order.
- Result: all 114 focused tests passed. `test_codex_discovery_probe_and_review_observe_exact_profile` checks `model/list`, `-m`, `model_reasoning_effort`, and a shorter preflight before review. `test_claude_alias_uses_explicit_flags_and_reports_accepted_level` checks `--model`, `--effort`, and `modelUsage`. `test_agy_model_list_and_explicit_pair` checks `agy models`, `--model`, and `--effort`.
- Evidence limit: the Codex test verifies observable model and effort headers; the Claude Code test verifies accepted settings and a model-family usage record but not effective effort; the Antigravity test verifies a listed candidate and accepted settings but not independently observed effective model or effort. These distinctions are reported by the runner.
- Limitation: no network-backed discovery or authenticated CLI preflight was run. Installed binaries were present, but installation alone does not prove an active login or model entitlement.

## 5. Failed or unverifiable selection does not become a passed review

- How I tried it: used the direct missing-consent command in section 3 and the focused simulated failure tests in section 1.
- Result: the direct command failed before discovery. `test_codex_stdout_profile_claim_cannot_override_stderr_header`, `test_claude_json_null_is_structured_failure`, `test_agy_cross_family_selection_is_refused_before_probe`, `test_failed_selection_or_execution_never_falls_back`, `test_codex_spoof_rejected`, `test_consent_conflict_rejected`, `test_discovery_null_failed`, and `test_selected_outside_review_with_skipped_reviewers_stays_unattested` all passed.
- Limitation: stale candidates, exhausted credentials, rejected model/effort flags, and provider mismatches were exercised through simulated subprocesses, not live vendor services.

## Re-run on 2026-10-08, at `af34f30b`

- Clean setup: `git clone --no-hardlinks --single-branch /Users/kouko/GitHub/loom-plugins /private/tmp/loom-acceptance-af34f30b`; `git rev-parse HEAD` returned `af34f30b6bfb7b8f9dc2b02a467d5f936b53b0aa`; `git status --short` was empty. The README's `python3 scripts/sync_codex_manifests.py --check --all` exited 0. Both `python3 scripts/check_plugin_boundaries.py loom-code` and the same command for `loom-workflow` returned their filesystem-boundary `OK` messages.
- Focused command: `uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_external_review.py loom-code/tests/test_external_review_adversarial.py loom-code/tests/test_second_vendor_policy.py loom-code/tests/test_loom_attestation.py loom-code/tests/test_selection_finalize.py loom-code/tests/test_dispatch_profile_contract.py loom-workflow/tests/independent-advisor/test_independent_advisor_readmes.py loom-workflow/tests/scripts/test_independent_advisor_compaction.py -q`
- Result: `140 passed in 28.55s`. The full package suite remains for `finalize-review`; it was not run in this acceptance rerun.
- 1: re-tested code, plan, and decision owner routes with `test_explicit_review_selects_a_real_owner_before_external_execution`, and retained incumbent/outside attribution with `test_selected_outside_review_raises_narrow_floor_and_requires_both_families` and `test_external_dispatch_gate_integrates_runner_verdict_and_attestation`. All passed. No live outside review was dispatched.
- 2: re-tested the owner-format surface through `test_external_dispatch_gate_integrates_runner_verdict_and_attestation`. It now rejects the incomplete outside YAML `verdict: PASS / lens: docs / findings: []` with `required reviewer YAML`, accepts the version with `reviewed_sha` and all document-dimension scores, and rejects a missing score, invalid score, mismatched SHA, or malformed finding. `loom-code/agents/reviewer.md:124-149` defines the required reviewer output; `loom-code/scripts/loom_checker/reviewers.py:155-166` applies the gate. No live outside output was available.
- 3: re-tested `python3 loom-code/scripts/external_review.py --list-candidates --executor codex --scope /private/tmp/loom-acceptance-af34f30b --consent-record /private/tmp/loom-acceptance-af34f30b/absent-consent.json`; exit 1 with `{"status": "failed", "reason": "consent-missing-or-stale", "executor": "codex", "candidates": []}`. The notice and consent tests in the focused command passed. No model discovery ran.
- 4: re-tested Codex, Claude Code, and Antigravity simulated subprocess cases in the focused command. `test_agy_model_list_and_explicit_pair` now checks that `-p` receives the probe prompt and then the review prompt as separate argument values, with empty stdin and explicit `--model`/`--effort`. No authenticated CLI or network-backed probe was run, so real account entitlement and effective-model behavior remain unverified.
- 5: re-tested missing consent, model/family mismatch, explicit-selection failures, and the incomplete reviewer YAML path in the focused command. Each relevant case passed, including `test_failed_selection_or_execution_never_falls_back` and `test_external_dispatch_gate_integrates_runner_verdict_and_attestation`. Live stale-candidate and credential failures remain unverified.
