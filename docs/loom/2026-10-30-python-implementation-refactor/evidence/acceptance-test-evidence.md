# Decision Map Python boundaries — acceptance test evidence

Tried on 2026-10-30 in a fresh local clone at `04529711853cd25af8a09fa6ae2c631836604697`, detached HEAD, with no uncommitted files. The clone was `/private/tmp/loom-plugins-python-acceptance-clean`. The README development setup names `uv run --isolated --with-requirements requirements-package-tests.lock`; the sandbox denied writing to the default uv cache, and an empty writable cache could not resolve the offline lock. I used the already installed `/Users/kouko/.conda/envs/dbt-redshift/bin/python` and its pytest in the clean source copy. No package was installed, and no product files were modified.

## 1. Decision Map 的讀取、驗證及交易能力各有可辨認的負責模組與入口；修改、加入或移除其中一項能力時，不必同步修改無關能力的實作。

- How I tried it: Ran the focused Decision Map tests shown in section 3, including `test_map_module_boundaries.py`. Inspected `git diff --name-status 45c94746..HEAD -- loom-workflow/skills/decision-map/scripts` in the clean clone.
- What came back: The module boundary tests passed. The changed script files were `map_close_transaction.py`, `map_store.py`, `map_ticket_mutations.py`, and `start_delivery.py`; no script file was added. The change added the shared `map_store.append_section_fields` entry and preserved `_append_section_fields` as an alias, replacing a duplicate Notes editor in `start_delivery.py`. The boundary tests check validation-owner imports, the existing facade identity, transaction owners, and this single shared Notes editor.
- Evidence: `loom-workflow/skills/decision-map/scripts/map_store.py:225`, `:243`; `loom-workflow/tests/decision-map/test_map_module_boundaries.py:20`, `:79`, `:157`, `:178`, `:219`; focused pytest output in section 3.

## 2. 重構前後，Decision Map 工具對相同有效與無效輸入的結果、退出狀態及既有資料處理結果維持一致。

- How I tried it: Ran all Decision Map tests in the clean clone; in particular, the existing valid and invalid map, delivery, and transaction tests. Also invoked `map_store.py --help` and `start_delivery.py --help` with the same Python interpreter.
- What came back: All Decision Map tests passed. `map_store.py --help` exited 0 and listed `{validate}`. `start_delivery.py --help` exited 0 and retained positional `map_dir da_id change_id` plus `--title` and `--repo-root`. Tests assert valid and invalid returns, refusal before writes, idempotent delivery binding, unchanged MAP bytes after an injected writer failure, and atomic compare-and-swap behavior. This is regression-test evidence rather than a byte-for-byte replay of every historical user map.
- Evidence: `loom-workflow/tests/decision-map/test_start_delivery.py:57`, `:87`, `:109`, `:198`; `loom-workflow/tests/decision-map/test_map_module_boundaries.py:136`, `:240`; `loom-workflow/tests/decision-map/test_map_store.py:1114`, `:1220`; focused pytest output in section 3.

## 3. Decision Map 的既有測試與完整 Loom 套件測試通過，且沒有因重構而增加只轉手的模組或不必要的對外入口。

- How I tried it: In the clean clone, ran `/Users/kouko/.conda/envs/dbt-redshift/bin/python -m pytest -q loom-workflow/tests/decision-map loom-workflow/tests/scripts/test_release_metadata.py`. Ran `python3 scripts/sync_codex_manifests.py --check --all`. Inspected changed scripts as in section 1.
- What came back: `279 passed in 8.73s` (exit 0). Manifest synchronization check exited 0 with no output. No new Decision Map script file was present. One shared Notes editor entry was added to `map_store.py` to remove duplicate implementation, while the old name remains an alias. The full package suite was not run here; `finalize-review` is scheduled to run it and block attestation on failure.
- Evidence: Captured pytest output:

  ```text
  ........................................................................ [ 25%]
  ........................................................................ [ 51%]
  ........................................................................ [ 77%]
  ...............................................................          [100%]
  279 passed in 8.73s
  ```

- Full-suite command reserved for `finalize-review`: `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`.
