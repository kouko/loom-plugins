# Planning command recovery — plan
intent: 2026-11-11-planning-command-recovery@c4f03ba9
spec: docs/loom/2026-11-11-planning-command-recovery/spec.md
charter: 1.1

## Task DAG
### Wave 1
**W1-01 Repair launcher and checker discovery** after: none acceptance: 1, 2, 3
- Files: loom-code/scripts/loom-python (entry), loom-code/scripts/loom_checker.py (entry), loom-code/tests/test_loom_python_runtime.py, loom-code/tests/test_loom_checker_cli.py
- Test: A1 positive: corrected-plan; negative: redundant-script. A2 positive: complete-help; boundary: no-runtime-help. A3 positive: existing-script-forwarding; negative: invalid-plan.
- Risk: agent-decided — follow spec REQ-1/2/3 decisions; preserve existing runtime/CLI tests and custom-script coverage; add no parser framework or implicit correction.

### Wave 2
**W2-01 Correct same-class hook recovery hints** after: W1-01 acceptance: 1, 3
- Files: loom-code/hooks/hooks*.json, loom-code/hooks.json, loom-code/tests/test_hooks_json.py, docs/loom/research/2026-11-11-planning-launcher-argument-mismatch.md
- Test: A1 positive: valid-recovery-hint; negative: missing-mode-hint. A3 positive: existing-hook-policy; negative: runtime-unavailable.
- Risk: agent-decided — spec REQ-1/3; preserve test_hooks_json.py coverage and failure policy; exercise emitted hints without real publication or installing hooks.

### Wave 3
**W3-01 Release recovery guidance** after: W2-01 acceptance: 1, 2, 3
- Files: loom-code/.claude-plugin/plugin.json, loom-code/CHANGELOG.md, README.md, loom-code/README*.md, loom-code/.codex-plugin/plugin.json, loom-code/plugin.json, loom-code/package.json, loom-code/tests/test_write_plan_station_text.py
- Test: A1 positive: release-parity; negative: stale-manifest. A2 positive: release-parity; negative: stale-pin. A3 positive: package-suite; negative: invalid-release.
- Risk: agent-decided — minor release 3.63.0 for shared command guidance, CHANGELOG entry and release-pin rewrite; synchronize existing derived manifests.

## Simplicity check
- none found

## Questions asked
- 1 — what — 另一台機器當時失敗的完整命令與原始錯誤訊息是什麼？若方便，請一併提供使用的工具（Codex／Claude Code／OpenCode）與 Loom 版本；我正在用本機重現結果核對。
- 1 — what — 是否確認先處理這項？確認後，驗證通過會推送分支並建立 Ready PR；合併另行確認，可在發布前取消。

## Risks
- agent-decided — semantic recovery needs a cold-agent trial; unit tests alone prove output and exit behavior, not successful agent recovery.
- agent-decided — the user added a same-pattern audit after confirmation; it preserves the confirmed recovery outcome and maps hook hints to the same defect class. No review round or retry counter is reset.
- agent-decided — engineering change skips product behavior confirmation; no one-way door identified.
- agent-decided — separate pending skill-lens branch also reserves 3.63.0; whichever lands second must resync and resolve its release metadata before review.
