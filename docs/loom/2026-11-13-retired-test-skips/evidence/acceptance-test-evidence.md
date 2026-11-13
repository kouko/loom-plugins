# Retired historical skips — acceptance test evidence

Historical observations below are preserved at their original revision. Current cumulative acceptance is recorded in the final dated re-run section; it supersedes the old report verdicts without rewriting those observations.

Tried on 2026-11-13, in a clean copy of the project at fca52f217b451b28313f24f1eb9bcb4f544e9645.

## Setup and scope

Fresh clone: `git clone --no-hardlinks /private/tmp/loom-retired-test-skips /private/tmp/retired-acceptance-20261113`, followed by detached checkout of the tested SHA. Initial and restored final `git status --porcelain` were empty. All mutations were confined to this disposable clone; no parent source, archive, real user data, other worktree or installed plugin changed.

Read README's isolated dependency setup and used its locked requirements for targeted tests, never the full package suite. README checks `python3 scripts/sync_codex_manifests.py --check --all`, `python3 scripts/check_plugin_boundaries.py loom-code`, the same boundary command for loom-design, and `python3 loom-code/scripts/check-skill-crossrefs.py` each exited 0. Boundary output: `OK: loom-code is filesystem-boundary clean.`, `OK: loom-design is filesystem-boundary clean.` Cross-reference output: `OK: all relative skill cross-references resolve.` This establishes repository test setup/loadability, not installation into a live coding-agent host.

Initial uv attempts exited 2 before collection because `/Users/kouko/.cache/uv` could not create a lock temporary file (`Operation not permitted`). Approved existing-cache access then succeeded. No dependency was installed into conda base. No skipped workflow steps or important dismissed findings were supplied or found in intent/plan. No spec applies.

## 1. 六項歷史測試各自的移除、取代或保留處置皆有可核對的理由，仍適用的驗證責任有明確去向。

Read each disposition against base `fbdc29af358413bc9d55b599231b2a6cbcb4524d` and actual test diff, then exercised its continuing owners:

| Retired proof | Verified continuing owner and limit |
|---|---|
| Historical 1.5.1 manifest pin | Existing current-release metadata test preserves the unconditional `## [1.5.1]` heading assertion and current manifest/readme consistency. Archive unchanged; graduated-copy comparison executable logic unchanged, with no new exception. |
| Retired integrity CLI | Current-store validation/idempotent regeneration and explicit retired-validator absence tests run in migration module. No retired executable restored. |
| Winner of removed basename collision | All three unified-root tests pass: full collection, station pythonpath membership and empty duplicate-basename allowance. Removed winner test had no remaining pair. |
| Historical 293 lesson / one guide snapshot | Public-entry synthetic migration now checks exact two-lesson inventory and separate single guide. Historical 293 count is retired, not independently replayed or claimed passed. |
| Historical lesson fidelity comparison | Fixture independently captures metadata/body inputs before migrate, including two descriptions/types/bodies, existing origin and missing origin's introducing SHA; later unrelated Git commit prevents accidentally accepting latest SHA. |
| Historical charter comparison | Same public-entry fixture verifies guide identity/type/description, exact introducing SHA, complete charter bytes after documented separator normalization, old index removal and regenerated validity. |

No docs archive or real memory-store path occurs in the base-to-tested changed-file inventory. The migration diff retains all 17 formerly active test names, removes only three historical comparisons and their unused helpers, and strengthens the existing public-entry test. Expected fixture values do not call migration transformation helpers. This evidence is ownership plus executed checks, not an absent-skip-text scan.

## 2. 保留或替代的檢查能在乾淨環境實際執行，不依賴已退役工具、固定舊版本或當前分支恰有特定歷史資料。

Each invocation ran separately from fresh clone root with its plugin configuration. Prefix: `uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest`.

| Arguments after prefix | Exit / captured output | Raw output |
|---|---|---|
| `loom-code/tests/test_probes_coldread_abuse_coldread_branch_end.py loom-code/tests/test_write_plan_station_text.py -q -rs` | 0; `59 passed in 0.20s` | `/private/tmp/retired-acceptance-code.txt` |
| `loom-design/tests/test_unified_pytest_root.py -q -rs` | 0; `3 passed in 0.22s` | `/private/tmp/retired-acceptance-design.txt` |
| `loom-workflow/tests/loom-memory/test_migrate_legacy_store.py -q -rs` | 0; `17 passed in 0.96s` | `/private/tmp/retired-acceptance-workflow.txt` |

Total: 79 actually passed, zero skips/xfails. The six retired historical cases are not six newly passing cases. Migration fixture initializes its own Git repository, not an enclosing trunk baseline. Existing coldread historical evidence checks still use retained repository history, transported by the fresh clone.

## 3. 既有版本一致性、模組收集與衝突防護、記憶庫遷移資料保留及失敗保護等仍適用的保障不因整理而喪失。

The runs above execute current release guards (including historical heading), graduated-copy identity, all unified-root collection/conflict checks, and all 17 migration/validator cases. Read their diff to confirm no new skip/xfail, relaxed conflict set or exception; invalid metadata/name, already-migrated shape, batch failure and retry guards remain active.

Independent negative probe `test_migration_corrupt_description_rejected`: in the disposable clone only, changed production `_migrate_concept_frontmatter` assignment from `"description": legacy_fm["description"]` to the valid string `"Independent acceptance corruption."`. Ran the unchanged `test_migrate_transforms_a_legacy_store_into_a_valid_okf_profile -q -rs` with the same prefix. Exit 1, `1 failed in 0.22s`, exact assertion: `AssertionError: ('a-fact.md', 'description')`, actual corrupted string versus `First distinct description.` Raw output `/private/tmp/retired-acceptance-negative.txt`. This is an independent production-seam mutation, not the implementer/adversary's claimed mutation result and not a test-oracle edit.

Restored the assignment using apply_patch and reran the identical test: exit 0, `1 passed in 0.20s` (`/private/tmp/retired-acceptance-restored.txt`); final clone status empty. No executable acceptance program committed.

## 4. 完整套件通過，這六項既有原因不再造成跳過；若有其他合理跳過，能逐項說明而不計為通過。

Did not independently rerun the full package suite, as required by the acceptance-tester contract. The targeted owners above actually passed with zero skips. The automated full test suite runs before acceptance and blocks on failure through finalize-review; package-tests and finalize-review are not skipped.

Configured command: `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`.

Independently read `/private/tmp/loom-retired-skips-package-tests.txt` and summed its fifteen pytest summary counts: 2837 + 211 + 53 + 264 + 64 + 22 + 13 + 12 + 58 + 125 + 253 + 12 + 19 + 163 + 162 = 4268. No skipped summaries. Shell groups report pass, Mermaid reports `13/13 mermaid blocks parsed` and its negative validator exit check passes. Build-verification records runner exit 0; this tester verified the retained output, not the past process exit independently. The log contains npm audit's dependency vulnerability notice; no package upgrade was attempted in this test-only scope.

`git diff 00c41f4bc774dc71dd66d0f96ae8db23db11ecf4 HEAD --stat` shows only the Build evidence markdown added after the recorded candidate; tested functional code is unchanged. This main-based branch excludes PR #150's additional help test, so 4268 versus that branch's 4269 is not a regression comparison. Historical skip records remain intact and are not live collection. Finalize-review's new full-suite result is still pending this committed acceptance report.

## Re-run on 2026-11-13, at daf2adf33a68d06fd7b1bde17e962e01c9d67224

### Setup and limits

Fresh independent tester; no implementation changes. `git clone --no-hardlinks /private/tmp/loom-retired-test-skips /private/tmp/loom-ci-acceptance-clean` succeeded; exact HEAD above and initial/final `git status --porcelain` were empty. Initial `git clone --local` failed because hardlinks were forbidden; the fallback retained a fresh clone and history. README's locked isolated dependency command was used for focused checks only. Initial uv execution failed before collection because its cache lock was not writable; approved existing-cache access succeeded, without installing into conda base.

README setup checks `python3 scripts/sync_codex_manifests.py --check --all`, `python3 scripts/check_plugin_boundaries.py loom-code`, the corresponding loom-design command, and `python3 loom-code/scripts/check-skill-crossrefs.py` all exited 0. Boundaries and relative cross-reference outputs were OK. This proves repository readiness, not live host installation. No containers/VMs installed, credentials provided, or model requests made. No important dismissed findings or user-instructed skips were supplied or found. No spec applies. Package-tests and finalize-review will run and are not skipped.

All pytest commands below use `uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest` in the clean clone. Results are direct tool-captured stdout/exit statuses from this independent run, not inferred from source.

### 1. Six dispositions and continuing owners — re-tested

Read all six disposition rows against the actual retained tests and earlier evidence. The current release owner keeps the historical 1.5.1 heading; retired integrity CLI responsibility is current-store validity and retirement checks; removed collision has no winner to preserve but collection/pythonpath/empty-conflict checks remain; three historical corpus checks are replaced by independent synthetic inventory, exact metadata/body/provenance and full charter fidelity. The historical 293-file proof remains retired, not counted as passing. Executed continuing owners under rows 2/3. The fca52f217..daf2adf33 diff does not alter these three focused test modules.

### 2. Clean execution — re-tested

| Arguments | Exit and actual result |
|---|---|
| `loom-code/tests/test_probes_coldread_abuse_coldread_branch_end.py loom-code/tests/test_write_plan_station_text.py -q -rs` | 0; 59 passed in 0.21s |
| `loom-design/tests/test_unified_pytest_root.py -q -rs` | 0; 3 passed in 0.20s |
| `loom-workflow/tests/loom-memory/test_migrate_legacy_store.py -q -rs` | 0; 17 passed in 1.21s |

79 actually passed, zero skips. Fixture migration owns a temporary Git repo; no historical corpus or retired CLI was supplied.

### 3. Preserved safeguards — re-tested

The 79 checks above cover release metadata, complete module collection/conflict protection and all 17 migration/validation cases, including failed migration no-write boundaries and metadata/body/guide preservation. Read the fix range to establish unchanged assertions; the earlier independent description-corruption failure/restoration remains historical sensitivity evidence, not a mutation repeated by this tester. No production/test repair or real-store operation was performed.

### 4. Full suite and skips — re-tested

Did not run the full package suite, as required by the tester contract. Independently inspected `/private/tmp/loom-ci-environment-package-tests.txt`: fifteen actual pytest summaries sum to 2842 + 211 + 53 + 264 + 64 + 22 + 13 + 12 + 58 + 125 + 253 + 12 + 19 + 163 + 162 = 4273; zero skipped summaries. Shell groups pass; Mermaid reports `13/13 mermaid blocks parsed` and intentional invalid input exits 1. Parent recorded exit 0; this tester witnessed the retained log, not that earlier process. The automated full suite runs before acceptance and blocks on failure through finalize-review. Configured command remains `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`. Linux results are pending and are not represented by these macOS results.

### 5. Per-job preparation and real external tool — re-tested, partly

`tests/test_ci_environment_preparation.py -q -rs`: exit 0, `5 passed in 0.72s`. This executes parsed job ordering/dependency/trigger checks and actual corrupt-download shell; it is not Linux execution. Read all three consuming workflows and the retained official-installation research. Python jobs install the hash-verified lock before their runner; code prepares zsh, uv, Python 3.11 and official pinned agy; workflow Python prepares Node/Mermaid inside its own job. Existing shell/Mermaid jobs retain their setup and suite inventory. Path filters include both requirements sources.

`agy --version`: exit 0, `1.3.3`. `tests/test_sync_codex_manifests.py -k agy_plugin_validate -q -rs`: exit 0, `3 passed, 32 deselected in 0.19s`. These use real local agy to validate all three plugins without credentials or model calls; they do not establish the pinned Linux 1.5.8 payload's success. No real Linux runner is available before publication. AC5 remains partly until actual GitHub logs show installation, readiness, and formerly skipped checks executing.

### 6. Failure boundaries and explicit limits — re-tested, partly

The executed named check `test_ci_agy_corrupt_download_stops_before_extraction` runs the workflow's actual install script under `bash --noprofile --norc -eo pipefail` with corrupt download bytes and an extraction trap. Passing means checksum rejects it, extraction never occurs, and GITHUB_PATH is not published. Other four checks verify dependencies precede suites, no continue-on-error/if override, and trigger coverage. This establishes local step failure and the configured native Actions success dependency; it does not simulate or observe the GitHub scheduler. There is no claim of Linux success or a failed real GitHub job.

Actual current execution: 79 historical-owner checks + 5 CI checks + 3 real local validator checks = 87 passed, zero skips; 32 deselected are selection exclusions, not passes. External full-suite log: 4273 passed, zero skips, plus shell and Mermaid passes. Linux actual executions/skips: not yet observed. Retained Ubuntu restrictions cover case-insensitive paths and macOS /var-alias behavior; only actual Linux -rs output can establish their final counts/reasons. AC6 remains partly until those logs identify the actual executed/skipped inventory and job outcome. Old failures/skips above remain historical facts.
