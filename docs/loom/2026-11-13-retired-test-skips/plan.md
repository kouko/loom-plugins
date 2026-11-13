# Historical test maintenance and complete CI preparation — plan
intent: 2026-11-13-retired-test-skips@ecddb23b175a133fc0d904aa8b557c844ba36d0a
charter: 1.1

## Current State Evidence
- Forward: `loom-workflow/tests/loom-memory/test_migrate_legacy_store.py::test_migrate_transforms_a_legacy_store_into_a_valid_okf_profile` executes migration against a temporary Git repository.
- Reverse: `loom-code/tests/test_write_plan_station_text.py::test_current_release_metadata_is_synchronized` owns current release consistency; `test_probes_coldread_changelog_carries_1_5_1.py` mixes historical heading preservation with an expired version precondition.
- Error: `loom-workflow/tests/loom-memory/test_migrate_legacy_store.py::test_name_stem_mismatch_aborts_before_any_file_is_written` and adjacent invalid-description tests enforce failed migrations writing nothing.
- Data: `loom-workflow/tests/loom-memory/test_migrate_legacy_store.py::_require_pre_migration_ref` skips three historical real-store comparisons after the trunk baseline migrates.
- Boundary: `loom-design/tests/test_unified_pytest_root.py::test_duplicated_non_test_basenames_are_only_the_known_shadowed_pair` enforces an empty conflict set; the winner test has no remaining pair.

- Forward: `.github/workflows/loom-workflow-ci.yml` job `loom-visualization-page-pytest` selects every workflow Python session but installs only pytest.
- Error: `loom-code/tests/test_rehearse_probes.py::test_rehearseProbes_underPython311_doesNotRaiseTypeErrorOnTheTempfileDeleteKeyword` skips when Python 3.11 or uv is absent.
- Data: `requirements-package-tests.lock` pins the complete Python test environment; existing CI jobs use three differing dependency lists.
- Boundary: `tests/test_sync_codex_manifests.py::test_agy_plugin_validate_accepts_committed_plugin` requires the real agy executable; official installation evidence is retained in `research/01-agy-ci-installation.md`.

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

### Wave 3 — Prepare each CI job before its tests

**W3-01 Prepare CI dependencies and verify failure ordering** after: W2-02 acceptance: 5, 6
- Files: `.github/workflows/loom-code-ci.yml`, `.github/workflows/loom-design-ci.yml`, `.github/workflows/loom-workflow-ci.yml`, `tests/test_ci_environment_preparation.py`, `loom-code/tests/test_package_tests_command.py`, `requirements-dev.txt`
- Test: A5 positive: per-job-dependencies-before-suite; boundary: dependency-path-triggers. A6 positive: setup-failure-blocks-suite; negative: missing-dependency-rejected. Run parsed-workflow checks, controlled failed-install execution and -rs skip reporting before full integration.
- Risk: agent-decided — Install the hash-verified Python lock, zsh, uv, Node and Mermaid where consumed; install the official agy 1.5.8 Linux payload with fixed SHA512. Preserve runner inventory, display names and coverage while updating the superseded dependency-source assertion.

**W3-02 Record CI coverage and complete the existing release packet** after: W3-01 acceptance: 3, 4, 5, 6
- Files: `loom-code/CHANGELOG.md`, `docs/loom/2026-11-13-retired-test-skips/disposition.md`, `docs/loom/2026-11-13-retired-test-skips/evidence/ci-environment-verification.md`
- Test: A3 positive: synchronized-existing-patch-release; boundary: other-branches-unchanged. A4 positive: complete-package-suite; boundary: platform-skips-accounted. A5 positive: github-live-dependency-checks; boundary: real-agy-validation. A6 positive: failed-setup-rejects-tests; boundary: unsupported-platforms-disclosed.
- Risk: agent-decided — Extend the existing 3.72.1 changelog packet without another bump unless fresh main requires it. Preserve earlier evidence, add actual Linux results, and retain OS-specific skips without adding a platform matrix.

## Simplicity check
- none found

## Questions asked
① — what — 按這個範圍進行嗎？
① — what — 確認依此擴充 PR #151 嗎？

## Risks
1. agent-decided — The six-row disposition records proof ownership and historical limits; synthetic migration checks preserve supported transformations, not a claim that the past 293-file migration has been rerun.
2. user-decided — Confirmed scope preserves all worktrees and delivers independently of help PR #150; canonical intent authorizes automatic publication. Merge remains a separate decision.
3. agent-decided — No workflow steps are skipped, no second-vendor consent is inherited from PR #150, and no spec is needed for internal test maintenance with empty carried details.
4. user-decided — On 2026-11-13, “對” confirmed additional AC5/6: prepare each CI job before testing and expose setup failure. Preserve worktrees and keep PR #150 untouched; no OS matrix expansion.
5. agent-decided — Earlier acceptance and attestation prove only AC1–4 at their recorded revisions. New CI setup/failure obligations require fresh adversary, full-suite execution, independent acceptance and closing review; retain old results as historical evidence, not current verification.
6. agent-decided — W3 is substantive new work, not a retry of the completed historical-test review. Start a new closing-review episode covering the cumulative tree and AC1–6; preserve prior episode outcomes and same-task failure history.
7. agent-decided — Add requirements-dev.txt and requirements-package-tests.lock to both events of each consuming workflow. Keep PR-floor’s trusted sparse checkout and pinned checker dependency unchanged; its existing installation already precedes its check.
8. agent-decided — Keep Ubuntu-only coverage. Case-insensitive-path and macOS /var-alias tests remain explicit platform skips. Record observed agy version and real validator results; never supply model credentials or count an unexecuted validator as passed.
