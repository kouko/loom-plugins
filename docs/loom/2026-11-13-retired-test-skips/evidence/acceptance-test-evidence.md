# Retired historical skips — acceptance test evidence

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
