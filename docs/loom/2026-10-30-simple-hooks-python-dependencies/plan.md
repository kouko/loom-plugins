# Simple hooks without checker package checks — plan
intent: 2026-10-30-simple-hooks-python-dependencies@1d611ac171d0a4c0ada9fe85bbcd39ebd5a72120
charter: 1.1

## Current State Evidence
- Forward: `loom-code/hooks/hooks.json:19,41,51` launches the standard-library language hook through `loom-python --ready`.
- Reverse: `loom-code/tests/test_hooks_json.py:155-158` pins the current launcher and fallback command.
- Error: `loom-code/scripts/loom-python:40-47` rejects a cold cache before starting any `--script` target.
- Data: `loom-code/hooks/language-anchor.py:16-17` imports only `json` and `sys`; `agy_adapter.py:19-29` imports standard-library modules.
- Boundary: `loom-code/hooks.json:9,18` routes both the checker-backed publication gate and simple pre-invocation through the launcher.

## Task DAG

### Wave 0 — simple hook routing

**W0-01 Run standard-library hooks directly**  after: none  acceptance: 1, 2, 3
- Files: `loom-code/hooks/hooks.json`, `loom-code/hooks/hooks-opencode.json`, `loom-code/hooks.json`, `loom-code/tests/test_hooks_json.py`
- Test: A1 positive: cold-cache anchor and pre-invocation; negative: no checker-package warning. A2 positive: publication gate retains ready check; boundary: cold-cache policy. A3 positive: host outputs; boundary: malformed payloads.
- Risk: agent-decided — prefer host Python for five simple hooks, retain cached-runtime fallback when host Python is unavailable; leave launcher and checker untouched. Existing host tests cover both paths.

### Wave 1 — integration and release

**W1-01 Verify host wiring and release metadata**  after: W0-01  acceptance: 1, 2, 3
- Files: `loom-code/.claude-plugin/plugin.json`, `loom-code/CHANGELOG.md`, `loom-code/README.md`, `loom-code/README.ja.md`, `loom-code/README.zh-TW.md`, `README.md`, `loom-code/tests/test_write_plan_station_text.py`
- Test: A1 positive: cold-cache host commands; boundary: no cache repair. A2 positive: checker gate unchanged; negative: bypass attempt. A3 positive: package suite; boundary: manifest synchronization.
- Risk: agent-decided — bump patch version for installed clients after behavior verification; generated manifests follow the canonical release metadata.

## Simplicity check
- Prefer direct `python3` when present, retaining the ready-cache fallback when absent — taken
- Keep adapter and launcher tests as verification, not edits — taken

## Questions asked
① — what — 你要的是：有可用系統 Python 時，簡單 hook 即使沒有 Loom 專用環境也能照常執行、不顯示不相關的套件缺失訊息；發布檢查仍維持原本的環境要求與失敗處理。對嗎？

## Risks
1. Host hook commands differ by plugin root syntax; only standard-library paths may bypass the checker runtime. Ready-cache operation without host Python remains supported.
2. Current tests assert the old launcher command and must be updated with execution evidence, not only string comparisons.
