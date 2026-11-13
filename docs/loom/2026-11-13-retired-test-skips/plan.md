# Retired historical test skips — plan
intent: 2026-11-13-retired-test-skips@b2ecdfa81756606b098ae92c6c8adf2b0621a3e6
charter: 1.1

## Current State Evidence
- Forward: `loom-workflow/tests/loom-memory/test_migrate_legacy_store.py::test_migrate_transforms_a_legacy_store_into_a_valid_okf_profile` executes migration against a temporary Git repository.
- Reverse: `loom-code/tests/test_write_plan_station_text.py::test_current_release_metadata_is_synchronized` owns current release consistency; `test_probes_coldread_changelog_carries_1_5_1.py` mixes historical heading preservation with an expired version precondition.
- Error: `loom-workflow/tests/loom-memory/test_migrate_legacy_store.py::test_name_stem_mismatch_aborts_before_any_file_is_written` and adjacent invalid-description tests enforce failed migrations writing nothing.
- Data: `loom-workflow/tests/loom-memory/test_migrate_legacy_store.py::_require_pre_migration_ref` skips three historical real-store comparisons after the trunk baseline migrates.
- Boundary: `loom-design/tests/test_unified_pytest_root.py::test_duplicated_non_test_basenames_are_only_the_known_shadowed_pair` enforces an empty conflict set; the winner test has no remaining pair.

## Task DAG

### Wave 1 — Test maintenance

**W1-01 Retire expired proofs and preserve live coverage** after: none acceptance: 1, 2, 3, 4
- Files: `loom-code/tests/test_probes_coldread_changelog_carries_1_5_1.py`, `loom-code/tests/test_probes_coldread_abuse_coldread_branch_end.py`, `loom-code/tests/test_write_plan_station_text.py`, `loom-design/tests/test_unified_pytest_root.py`, `loom-workflow/tests/loom-memory/test_migrate_legacy_store.py`, `docs/loom/2026-11-13-retired-test-skips/disposition.md`
- Test: A1 positive: six-dispositions; boundary: historical-proof-limits. A2 positive: temp-git-migration; negative: invalid-migration-no-writes. A3 positive: preserved-metadata-body-charter; boundary: empty-conflicts-current-release. A4 positive: focused-pytest-rs; boundary: remaining-skips-explained.
- Risk: agent-decided — Listed test files preserve applicable coverage through current guards and strengthened synthetic migration; retire only obsolete proof, retain the historical changelog assertion, and remove helpers made unused by these deletions.

### Wave 2 — One coherent patch release packet

**W2-01 Synchronize release manifests and changelog** after: W1-01 acceptance: 3
- Files: `loom-code/.claude-plugin/plugin.json`, `loom-code/.codex-plugin/plugin.json`, `loom-code/plugin.json`, `loom-code/package.json`, `loom-code/CHANGELOG.md`
- Test: A3 positive: generated-manifest-parity; boundary: unchanged-other-plugin-versions; run aggregate release checks after W2-02.
- Risk: agent-decided — Patch 3.72.1 changes internal tests only; edit the SSOT, derive mirrors with scripts/sync_codex_manifests.py --all, and commit this packet together with W2-02 before review finalization.

**W2-02 Complete release documentation and verify Build** after: W2-01 acceptance: 3, 4
- Files: `loom-code/README.md`, `loom-code/README.ja.md`, `loom-code/README.zh-TW.md`, `README.md`, `loom-code/tests/test_write_plan_station_text.py`, `docs/loom/2026-11-13-retired-test-skips/disposition.md`
- Test: A3 positive: current-release-synchronized; negative: release-drift-rejected. A4 positive: full-package-suite; boundary: independently-accounted-skips; execute the configured complete package suite after both release tasks and retain real pytest -rs evidence.
- Risk: agent-decided — test_write_plan_station_text.py preserves coverage, changing only CURRENT_VERSION. Recheck fresh main before final version selection because unmerged help PR #150 independently proposes 3.73; do not modify its branch or evidence.

Build verification uses the configured `package-tests` command in `docs/loom/KICKOFF-DEFAULTS.md`, the relevant focused pytest invocations with `-rs`, and the mandatory independent adversarial pass. Keep positive runs distinct from skipped cases. Record outputs and any remaining skip explanations in the disposition evidence before closing review; no production tool changes are authorized.

## Simplicity check
- none found

## Questions asked
① — what — 按這個範圍進行嗎？

## Risks
1. agent-decided — The six-row disposition records proof ownership and historical limits; synthetic migration checks preserve supported transformations, not a claim that the past 293-file migration has been rerun.
2. user-decided — Confirmed scope preserves all worktrees and delivers independently of help PR #150; canonical intent authorizes automatic publication. Merge remains a separate decision.
3. agent-decided — No workflow steps are skipped, no second-vendor consent is inherited from PR #150, and no spec is needed for internal test maintenance with empty carried details.
