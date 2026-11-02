# Loom evidence drift guards — acceptance test evidence

Tried on 2026-11-02, in a clean copy of the project at 2938a3bedddae6d53146f6a7e0c97db65237b3db.

## Setup and actual commands

- `git clone --no-hardlinks . /private/tmp/loom-acceptance-2938a3b`: exit 0, full history retained. `git rev-parse HEAD` returned the exact commit above. Final clean-clone `git status --short` was empty.
- Read README Development instructions and confirmed intent/spec/plan. Used its isolated locked environment with focused pytest inventory, as required by the acceptance-tester contract.
- `python3 loom-code/scripts/loom_checker.py --list-rules`: exit 0, including all four evidence rules. `python3 scripts/sync_codex_manifests.py --check --all`: exit 0. Local checker and manifests load; this does not claim a new global plugin installation.
- Initial sandboxed uv failed to create a cache lock. Approved cache access resolved that. An initial mixed code/design-root command then failed collection with `ModuleNotFoundError: test_verification_status` (zero tests executed); reran separately, consistent with the package inventory's isolated roots. No repairs were made.
- Code command: `uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_evidence_drift_guards.py loom-code/tests/test_adversarial_evidence_drift.py loom-code/tests/test_verification_status.py loom-code/tests/test_selection_finalize.py loom-code/tests/test_contract_manifest.py loom-code/tests/test_review_json_template.py loom-code/tests/test_write_plan_station_text.py -q -n 0`. Exit 0, **164 passed in 75.16s**. Log `/private/tmp/loom-acceptance-code.log`.
- Design command: `uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-design/tests/spec/test_capture_intent_contract.py -q -n 0`. Exit 0, **27 passed in 0.02s**. Log `/private/tmp/loom-acceptance-design.log`.
- Boundary command: `uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_loom_checker_intake.py -k 'named_boundary_file or plan_boundary_tests' -q -n 0`. Exit 0, **11 passed, 137 deselected in 2.97s**. Log `/private/tmp/loom-acceptance-boundary.log`.
- **202 focused tests passed**. Full package suite left to finalization, not run by this witness. Its command is `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`; no future result is claimed.
- Additional witness-owned temporary programs: `python3 /private/tmp/loom-acceptance-lifecycle.py` and `python3 /private/tmp/loom-acceptance-defaults.py`, both exit 0. They used temporary Git repositories, existing source helpers, and actual checker CLI execution. Relevant captured outputs are preserved below; fixture reviewer identities are test data only.

## 1. Complete, uniquely identified acceptance results

Passed tests: `test_coverage_fails_and_names_a_missing_line`, `test_coverage_fails_and_names_an_extra_line`, `test_coverage_fails_and_names_a_duplicated_line`, `test_coverage_fails_and_names_an_unreadable_verdict`, and complete-report cases, including escaped content pipes. `test_acceptance_status_records_not_verified_for_a_missing_row` verifies omission is not passing.

Witness lifecycle trial committed each report mutation and ran actual finalization:

```text
missing 1 BLOCK intake.attestation-coverage: acceptance test report has no row for Acceptance lines: 1
duplicate 1 BLOCK intake.attestation-coverage: acceptance test report carries duplicate rows for Acceptance lines: 1
unreadable 1 BLOCK intake.attestation-coverage: acceptance test report states no Verdict in (works / partly / not verified / fails) for Acceptance lines: 1
```

These cover spec Empty evidence and Invalid coverage flows. Complete evidence reached execution and output generation in section 5. Failed attempts did not produce a replacement record.

## 2. Tested and reviewed commit identity

Passed `test_commit_identity_fails_when_a_v2_field_is_missing`, `test_commit_identity_fails_on_functional_drift`, `test_commit_identity_ignores_evidence_only_drift`, and `test_commit_identity_passes_identical_functional_content`. Functional-drift assertions require both commit abbreviations in the diagnostic. Publication attacks include null and unresolved tested identities; selected-tree tests include unrelated functional content and invalid provenance.

Actual lifecycle success output contained `tested_commit: db41300`, `reviewed_commit: d389aa66aa43583df4e8da40527b60da4f89323b`, and `acceptance_status: [{acceptance: 1, status: works}]`. After functional plan content changed, actual finalization returned:

```text
BLOCK intake.commit-identity: functional content differs between the tested commit db41300 and the reviewed commit 90ca987; the acceptance evidence was produced on other code than what is being reviewed
```

This and section 3 cover spec Mismatched content. Evidence-only changes pass; executable probes retain functional binding.

## 3. Confirmed intent, rollback and recovery

All five cases of `test_finalizer_anchors_the_latest_confirmed_intent` passed. Actual finalization succeeds for unchanged newly confirmed content and rejects restoring the entire older unpinned file, restoring an older pinned file, and a merge carrying the older intent. Explicit historical and confirmation commits remain readable despite newer checkout history.

Matching/abbreviated pins, post-confirmation editing, recovery and POSIX-shell recipe tests passed. An additional direct mutation trial printed:

```text
intake.intent-version: the intent has changed since the attestation pinned its confirmation (recorded 98dbcf1, current 0ad4a49); every Acceptance line of the intent may be affected. recompute it with `grep -v -e '^status:' -e '^intent_confirmed_sha:' docs/loom/intent/2026-10-12-drift.md | git hash-object --stdin` and re-confirm the intent before closing review
```

The diagnostic conservatively identifies every Acceptance line as potentially affected, rather than pretending to determine semantic impact precisely. Both entry recipes were executed and matched checker identity (section 7).

## 4. Concrete named boundary programs

Eleven focused intake/boundary cases passed. `test_named_boundary_file_uses_the_implemented_tree` exercises Files/Test/Risk carriers, planning with `require_files=False`, file presence, and selected committed tree versus mutable checkout. Missing task references are independently rejected; historical charter handling is retained. Both absent-program adversarial cases passed, including `.pY` spelling.

Actual finalization of a plan naming an absent program returned exit 1:

```text
BLOCK intake.plan-boundary-tests: Named boundary/probe test files do not exist: tests/test_missing.py
```

This covers spec Missing boundary program. That trial also correctly reported functional drift because its plan changed after testing; the independent missing-program diagnostic was present.

## 5. Persisted verdict and authoritative output

Witness trial finalized a temporary adopting repository using fixture package command `python3 -c pass` and review input outside the repository. Actual CLI exit 0:

```text
wrote docs/loom/2026-09-14-example/attestation.json for 6dadf6a4c5f1127fdb8e2d460ee35461bf256ce9
```

Parsed output retained `verdicts: [{reviewer: r1, vendor: openai, model: m, lens: code, verdict: PASS, findings: []}]`, both commit identities, per-line acceptance, and successful package execution. Fixture identities are not actual reviewer claims. `test_finalize_binds_the_report_verdicts_into_acceptance_status` independently passed. These cover spec In progress and Success with real subprocess execution before output generation.

`loom-code/skills/closing-review/SKILL.md:270` explicitly assigns authoritative verdicts to the change directory's attestation and defines outside review input as temporary. This branch's real attestation has NOT been regenerated by this witness; closing-review must generate it after report commitment and fresh review.

## 6. Publication checks selected committed artifacts again

Lifecycle trial committed its generated record: verification returned `valid`. A committed report-only observational note remained `valid`. Subsequent damage returned:

```text
missing publication stale (acceptance test report has no row for Acceptance lines: 1)
duplicate publication stale (acceptance test report carries duplicate rows for Acceptance lines: 1)
unreadable publication stale (acceptance test report states no Verdict in (works / partly / not verified / fails) for Acceptance lines: 1)
```

All six `test_evidence_revalidation_reads_the_selected_tree` cases passed: status mismatch, intent pin, reviewed content, boundary file, provenance, and valid report edit. They recheck an earlier valid commit while HEAD is damaged, then repair mutable files and still reject the selected damaged commit. Five publication-damage attacks passed too. Full-history rollback/merge checks are recorded in section 3.

This covers spec Publication. Verification discloses `stale`; existing publication authorization may still publish while disclosing it. No network publication or merge was attempted.

## 7. Defaults, old shapes and mechanical verification

Witness default-check output:

```text
attestation default fields ['acceptance_status', 'intent_confirmed_sha', 'reviewed_commit', 'tested_commit']
confirmation ordering and executable hash recipe loom-design/skills/capture-intent/SKILL.md
confirmation ordering and executable hash recipe loom-code/skills/write-plan/references/confirm-intent.md
both recipes match checker intent identity 19673070d78e30519d42bffadc486b6eb49b5db9
report defaults canonical provenance and per-line verdict/re-run
```

Assertions loaded the actual JSON/report templates and both instruction artifacts. Both entry paths require replacing the placeholder after writing all confirmed frontmatter, including publication authorization. Their literal hash recipe was run under `sh` and matched checker identity. Successful finalization also exercised report provenance/default record population. Manifest/template declaration consistency tests passed.

`test_historical_v2_and_complete_extension_keep_exact_shapes` passed for six-key v1, seven-key v2 and complete extended v2, using their respective digest policies; incomplete extensions and unknown keys were rejected. `test_compatibility_existingv2_accepted` passed. Report-free mechanical finalization passed, records actual tested/reviewed HEAD, leaves acceptance status empty and claims no independent acceptance testing. These cover spec Historical evidence and Mechanical verification.

## Re-run on 2026-11-02, at 2938a3bedddae6d53146f6a7e0c97db65237b3db

- 1–7: re-tested in full; no old verdicts or reviewer identities carried over. All nine confirmed spec UI cases map to the seven rows above.
- No important/fatal dismissals supplied. Only the report and this evidence file were edited in the original repository by this witness.
- Limits: structured checks cannot prove the truth of a prose claim. Historical exemptions do not manufacture missing evidence. No claim is made that this branch's final whole-repository suite or real finalization has already completed.
