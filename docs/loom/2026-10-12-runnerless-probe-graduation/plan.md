# Runnerless probe graduation — plan
intent: 2026-10-12-runnerless-probe-graduation@666fbbe302697982aaaa9a6f66b7bbf9a9e23751
charter: 1.1

## Current State Evidence
- Forward: `probes.py:suite_collects` reads only `scripts/run_package_tests.py`; a repository without it has no recognized suite paths.
- Reverse: `finalize.py:_finalize` accepts a graduated artifact only when `suite_collects` recognizes it, then counts and executes it.
- Error: `probes.py:command_executes_artifact` unwraps `uv run` but rejects a `conda run` command even when it names the test.
- Data: `probes.py:declared_test_command` separately reads `package-tests` from `KICKOFF-DEFAULTS.md`, while `_declared_suite_commands` does not.
- Boundary: `test_selection_finalize.py` covers runner-backed graduation and uncollected neighbors, but no runnerless pytest fixture.

## Task DAG

**W1-01 Recognize tests collected by package suites**  after: none  acceptance: 1,2,3
- Files: `loom-code/scripts/loom_checker/probes.py`, `loom-code/tests/test_selection_finalize.py`, `loom-code/tests/test_adversarial_probe_cap_coverage.py`
- Test: A1 positive: runnerless-collected-finalizes; negative: collection-error-refused. A2 positive: ignored-or-unselected-refused; negative: selected-file-accepted. A3 positive: runner-root-collected; negative: runner-root-ignored.
- Risk: agent-decided — use bounded pytest collection for direct commands to respect repo configuration; retain the runner inventory when present and refuse unsupported command shapes.

**W1-02 Accept a bounded Conda test command**  after: W1-01  acceptance: 4
- Files: `loom-code/scripts/loom_checker/probes.py`, `loom-code/tests/test_selection_finalize.py`, `loom-code/tests/test_loom_attestation.py`
- Test: A4 positive: conda-runs-artifact; negative: conda-does-not-run-artifact.
- Risk: agent-decided — recognize only an explicit `conda run` Python pytest argv; refuse ambiguous options and preserve attestation revalidation.

**W2-01 Synchronize the patch release**  after: W1-01,W1-02  acceptance: 1,2,3,4
- Files: `loom-code/plugin.json`, `loom-code/.claude-plugin/plugin.json`, `loom-code/.codex-plugin/plugin.json`, `loom-code/package.json`, `loom-code/CHANGELOG.md`, `loom-code/README*.md`, `README.md`, `loom-code/tests/test_write_plan_station_text.py`
- Test: A1 positive: packaged-runnerless-finalizes; negative: packaged-uncollected-refused. A2 positive: packaged-ignored-refused; negative: packaged-selected-accepted. A3 positive: packaged-dot-accepted; negative: packaged-dot-ignored. A4 positive: packaged-conda-accepted; negative: packaged-noop-rejected.
- Risk: agent-decided — bump the patch version after functional work and before finalization, so its content-bound review remains valid.

## Simplicity check
- none found

## Questions asked
① — what — 你要修的是：沒有額外測試腳本的專案，將抓到缺陷的測試移進正式測試後，也能完成 Loom 的最終驗證；正式測試收不到的檔案或沒有真的執行檔案的命令仍須被拒絕。這次也涵蓋既有測試腳本指向專案根目錄、以及透過 Conda 執行該檔案；Codex 模型探索問題先不納入。這個範圍與驗收結果符合你的意思嗎？回答「是」後，我會在驗證通過時非強制推送分支並建立 Ready PR；合併另行決定。你也可以在發布前取消自動發布。

## Risks
1. Running collection adds startup and import work before finalization; a bounded timeout and a failed-closed result must protect the gate.
2. The reported iCHEF repository and its Conda environment are unavailable here; clean fixture repositories must cover its command shape without claiming a live-host run.
user-decided — second-vendor selection-confirmed: claude
