# Loom evidence drift guards — acceptance test evidence

Tried on 2026-11-02, in a clean copy of the project at 31d0c73ed27f8a6aa77425fbf115f3cfa3ed3a69. Original numbered sections retain their historical observations. The final re-run section is authoritative for current results: rows 1, 2, 3, 5, 6 and 7 were re-tested in full at this HEAD; row 4 retains original provenance at 2938a3bedddae6d53146f6a7e0c97db65237b3db with an explicit unchanged-surface reason.

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

## Re-run on 2026-11-02, at d7d23e19659088a36a6e6f61d3cf9ea6f06f2b0d

### Clean setup and actual delta

- `git clone --no-hardlinks . /private/tmp/loom-acceptance-d7d23e1` succeeded with full history. `git rev-parse HEAD` returned the exact commit above. Read the same README setup instructions; used the declared isolated locked environment again.
- `python3 loom-code/scripts/loom_checker.py --list-rules` and `python3 scripts/sync_codex_manifests.py --check --all` both exited 0. The actual checker loads after the three unused intake imports were removed.
- Examined `git diff 2938a3be..d7d23e19`: only runtime changes are the probe cap restored from six to five and deletion of three unused imports. The associated reference changes six to five and the cap test now explicitly tries five/six. Remaining changes are report/evidence and plan records. All four evidence-check implementations, both confirmation instructions, templates, finalizer, publication revalidation and digest behavior are unchanged.

### Per-row carry-over decision

- 1: carried over from 2938a3bedddae6d53146f6a7e0c97db65237b3db — coverage implementation and report parser unchanged; report-only changes do not change tested parser behavior.
- 2: carried over from that exact original commit — commit identity, digest classification and bookkeeping generation unchanged.
- 3: carried over from that exact original commit — canonical confirmation ancestry, rollback detection, pin comparison and recovery text unchanged.
- 4: carried over from that exact original commit — concrete boundary-file and planning-reference checks unchanged; the cap counts adversarial programs and does not alter boundary-file existence semantics.
- 5: carried over from that exact original commit — output location, authoritative verdict storage and finalization generation unchanged; previous success used zero adversarial programs and remains below either cap.
- 6: carried over from that exact original commit — selected-tree publication evidence revalidation unchanged, including coverage, identities, intent and boundary presence; all recorded cases remain unaffected by a five/six program ceiling.
- 7: re-tested in full — cap affects supported workflow eligibility, so rechecked new defaults, both entry instructions/hash recipes, historical shapes, report-free mechanical verification and actual-finalizer five/six boundary.

### Commands and observed results

- In the new clean clone: `uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_selection_finalize.py loom-code/tests/test_verification_status.py loom-code/tests/test_adversarial_evidence_drift.py loom-code/tests/test_contract_manifest.py loom-code/tests/test_review_json_template.py loom-code/tests/test_write_plan_station_text.py loom-code/tests/test_loom_checker_modules.py -k 'cap_probe_programs or narrow_delta_finalizes or finalization_mechanical or compatibility_existingv2 or historical_v2_and_complete_extension or attestation_has_only or markdown_templates_carry or artifact_schemas or decision or current_release_metadata or module' -q -n 0`: exit 0, **17 passed, 124 deselected in 6.70s**. Log `/private/tmp/loom-acceptance-d7d-code.log`.
- `test_cap_probe_programs_pass_and_one_more_is_refused` invokes the real finalizer, observes five programs exit 0, then a sixth exit 1 with `BLOCK adversarial.proportionate` and `6 probe programs`. Module loading, default schema/template assertions, old six/seven-key records and both report-free mechanical cases passed in that run.
- `uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-design/tests/spec/test_capture_intent_contract.py -q -n 0`: exit 0, **27 passed in 0.03s**. Log `/private/tmp/loom-acceptance-d7d-design.log`.
- Updated only the temporary witness defaults program's root to the new clean clone and ran `python3 /private/tmp/loom-acceptance-defaults.py`: exit 0. It again loaded all four default evidence fields, canonical report provenance and per-line result/re-run columns, asserted both confirmation entry paths order publication before hashing, and executed their shell recipe; checker and shell again agreed on `19673070d78e30519d42bffadc486b6eb49b5db9`. Log `/private/tmp/loom-acceptance-d7d-defaults.log`.
- This incremental run: **44 focused tests passed**, plus executable default/recipe checks. No full suite or unaffected 202-case rerun. Package-tests remain required and finalization will run; supplied Build logs are not independent witness results and are not represented as such.
- Results remain 1–7 `works`. No new findings or important/fatal dismissals. Real branch attestation remains outside this witness's edits and claims.

## Re-run on 2026-11-02, at 31d0c73ed27f8a6aa77425fbf115f3cfa3ed3a69

### Clean setup, actual delta and scope

- `git clone --no-hardlinks . /private/tmp/loom-acceptance-31d0c73` succeeded, preserving complete history. `git rev-parse HEAD` returned the exact target above. Re-read README Development setup, then reused its declared isolated locked environment.
- `python3 loom-code/scripts/loom_checker.py --list-rules` and `python3 scripts/sync_codex_manifests.py --check --all` exited 0. Final `git status --short` in the clean clone was empty.
- Examined `git diff b0673ad0..31d0c73e` including production, tests, contract, registry, station prose and release notes. New confirmation lookup is shared with identity validation and delivered-state checking; old six/seven-key evidence is rejected for selected pinned canonical confirmations, while pre-pin history remains compatible. Invalid status arrays/objects now produce a validation failure rather than an unhashable-value exception. Report-free mechanical verification is supported beyond narrow changes; a present report still must be valid, and absent reports cannot claim independent results. Three evidence citations and recovery-command testing were corrected.
- Rows 1, 2, 3, 5, 6 and 7: re-tested in full because shared validation/finalization, confirmation lookup and mechanical compatibility changed.
- Row 4: carried over from 2938a3bedddae6d53146f6a7e0c97db65237b3db. Boundary-file presence, task/reference parsing and planning-versus-implemented stages are unchanged; neither the report-absence branch nor confirmation lookup changes their semantics. The actual lifecycle trial incidentally reconfirmed its missing-file diagnostic, but is not substituted for the full original row.

### Exact commands and totals

In the clean clone:

```text
uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_evidence_drift_guards.py loom-code/tests/test_adversarial_evidence_drift.py loom-code/tests/test_verification_status.py loom-code/tests/test_selection_finalize.py loom-code/tests/test_contract_manifest.py loom-code/tests/test_review_json_template.py loom-code/tests/test_write_plan_station_text.py loom-code/tests/test_loom_checker_modules.py -k 'not runner and not conda and not uv_pytest and not graduated and not probe_program and not extension_less and not spends and not executed_artifact and not ordinary_new and not file_the_suite and not selected_outside and not reviewers_skipped and not shell_probe and not program_in_the_store and not adversarial_artifact and not cap_probe and not usage_error and not wide_delta and not no_program' -q -n 0
```

Exit 0: **139 passed, 33 deselected in 49.43s**. Log `/private/tmp/loom-acceptance-31d-code.log`. The filter excludes unrelated runner/probe-cap/dispatch cases, retaining every coverage, identity, confirmation, publication, compatibility and mechanical-evidence case.

`uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-design/tests/spec/test_capture_intent_contract.py -q -n 0`: exit 0, **27 passed in 0.03s**. Log `/private/tmp/loom-acceptance-31d-design.log`.

Total: **166 focused tests passed**. No complete package suite executed by this witness. Finalization remains required and will execute that suite; supplied Build logs are not claimed as witness-run results.

Updated only temporary witness programs' source-root pointer and ran `python3 /private/tmp/loom-acceptance-defaults.py` and `python3 /private/tmp/loom-acceptance-lifecycle.py`; both exit 0. Logs `/private/tmp/loom-acceptance-31d-defaults.log` and `/private/tmp/loom-acceptance-31d-lifecycle.log`.

### Re-tested outcomes and UI flows

- **1 — works.** Complete reports, escaped separators and valid statuses pass; missing, duplicate, extra and unreadable rows fail with numbers. Actual CLI returned exit 1 for missing/duplicate/unknown status on Acceptance 1. These cover Empty evidence and Invalid coverage. Mechanical omission is distinct from a present malformed report: all three `test_mechanical_verification_without_a_report_keeps_evidence_boundaries` cases passed, including rejection of claimed statuses without a report and invalid present reports.
- **2 — works.** All commit-identity tests passed: missing identities and functional changes fail, direct evidence-only changes pass. Six/seven-key downgrade is now blocked for a selected pinned canonical confirmation, including the direct identity rule and full validator. Actual lifecycle finalization recorded tested `ffd05d2` and reviewed `6cfe5542eef6d05087df18c5e5faaba0b7b18fdc`; changing functional plan content emitted `functional content differs between the tested commit ffd05d2 and the reviewed commit 7095335`. This covers commit-side Mismatched content.
- **3 — works.** All five actual-finalizer canonical-confirmation cases passed, including complete old-file restoration with/without an old pin, merge-hidden restoration and explicitly selected historical commits. All intent-version cases passed. `test_intent_version_fails_after_a_post_confirmation_edit` now extracts and runs the exact shell command from the public rule diagnostic, proving recovery output at its entry point rather than calling its formatting helper. The diagnostic states every Acceptance may be affected and requires reconfirmation. This covers intent-side Mismatched content.
- **5 — works.** Actual lifecycle CLI exited 0 and wrote `docs/loom/2026-09-14-example/attestation.json`; parsed record retained fixture reviewer r1's PASS, both identities, per-line result and completed package execution. `test_finalize_binds_the_report_verdicts_into_acceptance_status` passed. Station documentation still defines this record as authoritative and external input as temporary. These cover In progress and Success. Fixture reviewer identity is test data, not this branch's reviewer evidence; its real attestation has not been regenerated by this witness.
- **6 — works.** All eight selected-tree revalidation cases passed, including new `status-list` and `status-object`: malformed values produce stale verification rather than raising TypeError. Earlier valid selected commits remain valid despite a damaged checkout; repairing mutable files cannot hide damaged selected evidence. Actual lifecycle publication was valid after record commitment and a report-only note; missing, duplicate and unknown-result mutations each returned stale with the affected number. Canonical pinned evidence cannot downgrade to old shapes to bypass these checks. This covers Publication.
- **7 — works.** Templates and declared field consistency passed, as did both entry contracts. Executed both entry recipes against finalized sample frontmatter; checker and shell again agree on `19673070d78e30519d42bffadc486b6eb49b5db9`. Both recipes require publication fields before hashing. Parameterized legacy validation tests passed both branches: pre-pin six/seven-key records remain valid/delivered; after a selected canonical pinned confirmation those shapes fail and remain active, while the complete extension passes. Incomplete extensions and unknown fields fail. Actual report-free mechanical cases pass for no-intent, narrow and executable changes; executable case runs functional package and adversarial commands with required reviewer input, records actual HEAD and empty statuses, and claims no independent acceptance testing. These cover Historical evidence and Mechanical verification.

### Limits and current verdict

All seven rows remain `works`; row 4 is the only carried-over row. No new findings and no important/fatal dismissals. Report absence cannot mechanically establish whether independent acceptance was semantically needed: the station and reviewers retain that decision, now explicitly documented in the report. Existing publication still discloses stale verification rather than universally blocking publication. No production, test, intent, spec, plan or attestation edits; only the two witness artifacts changed. No claim that this branch's real finalization or final whole-repository suite has already completed.
