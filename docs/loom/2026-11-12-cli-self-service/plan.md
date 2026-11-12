# Self-service CLI discovery and recovery — plan
intent: 2026-11-12-cli-self-service@4eebeb0f
spec: docs/loom/2026-11-12-cli-self-service/spec.md@b4f4b8bf
charter: 1.1

## Task DAG

### Wave 1 — Public command entry

**W1-01 Expose bounded help and recovery guidance** after: none acceptance: 1, 2, 3, 4
- Files: loom-code/scripts/loom_checker.py (public entry: main), loom-code/tests/test_loom_checker_cli.py
- Test: A1 positive: discover-input; boundary: help-outside-repo. A2 positive: usage-recovery; negative: preserve-rejection. A3 positive: outcome-guidance; boundary: incomplete-json. A4 positive: unchanged-success; negative: invalid-help-shape; architecture: loom-code/tests/test_loom_checker_modules.py::test_entry_point_owns_only_cli_dispatch.
- Risk: agent-decided — REQ-1/2/3/4 use dispatch-local help without handler rewrites. Preserve and widen existing coverage in loom-code/tests/test_loom_checker_cli.py; retain the main-only callable boundary checked by test_loom_checker_modules.py::test_entry_point_owns_only_cli_dispatch. Original diagnostics and hook behavior remain authoritative.

### Wave 2 — Release and reproducible first-use evidence

**W2-01 Document and package the bounded interface** after: W1-01 acceptance: 5
- Files: loom-code/.claude-plugin/plugin.json, loom-code/.codex-plugin/plugin.json, loom-code/plugin.json and loom-code/package.json (generated), loom-code/CHANGELOG.md, README.md, loom-code/README*.md, loom-code/tests/test_write_plan_station_text.py, docs/loom/2026-11-12-cli-self-service/evidence/
- Test: A5 positive: retained-first-attempts; boundary: untested-host-disclosure. Run synchronized-release metadata test and package suite; independent acceptance owns actual operator evidence.
- Risk: agent-decided — REQ-5 retain raw attempts and limits without measuring unsupported efficiency gains. Bump code minor to 3.68.0; synchronize generated manifests, README and CHANGELOG entry; rewrite existing version pins only where needed.

## Simplicity check
- none found

## Questions asked
① — what — 是否確認這個範圍？
① — consequence — 確認也會授權在審查與檢查通過後，推送至 kouko/loom-plugins 並建立 Ready PR；你可在發布前撤回，合併仍另行確認。

## Risks
1. Authentic review judgments cannot be synthesized for convenience. The independent operator receives raw evidence and public documentation, not completed JSON or implementation answers; isolated acceptance excludes remote writes.
2. Progress and partial success do not establish delivery. Preserve exit status and result fields; use existing observation before any repeat publication. Help has no validation or authorization effect.
3. Preserve the current worktree. Publication is authorized; merge remains a separate user action. Independent acceptance and review follow completed implementation, with exact tested source and failed attempts retained.
4. The spec review passed with notes: installed-version help failures were source-supported but not independently replayed. Retain executable pre-change failures during test-first implementation rather than claiming prior raw evidence exists.
