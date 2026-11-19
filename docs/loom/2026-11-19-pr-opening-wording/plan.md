# The PR-opening step is no longer called publish — plan
intent: 2026-11-19-pr-opening-wording@fbff7a163
spec: docs/loom/2026-11-19-pr-opening-wording/spec.md@6599f4462
charter: 1.1

## Task DAG

Wave 1 — checker code (W1-01 then W1-02, shared test modules); Wave 2 — prose and release.

**W1-01 Rename the dispatch key to open-pr**  after: none  acceptance: 1, 2
- Files: `loom-code/scripts/loom_checker.py`, `loom-code/scripts/loom_checker/cli_advice.py`, `loom-code/tests/test_loom_checker_cli.py`, `loom-code/tests/test_loom_checker_modules.py`, `loom-code/tests/test_loom_python_runtime.py`, `loom-code/tests/test_adversarial_blocked_publish_routes.py`
- Test: A1 positive: open-pr-dispatches-to-cmd_publish-with-same-args; boundary: open-pr-help-lists-same-usage. A2 positive: publish-returns-unknown-sub-command-nonzero-no-push; boundary: publish-help-and-loom-python-repair-publish-unknown.
- Risk: REQ-1/REQ-2; existing tests calling `publish` are rewritten to `open-pr`, coverage preserved; no alias entry (user-decided).

**W1-02 Reword printed lines and hook messages**  after: W1-01  acceptance: 3, 4, 7
- Files: `loom-code/scripts/loom_checker/command_handlers/publish.py`, `loom-code/scripts/loom_checker/command_handlers/land.py`, `loom-code/scripts/loom_checker/command_handlers/push.py`, `loom-code/scripts/loom_checker.py`, `loom-code/tests/test_loom_publish.py`, `loom-code/tests/test_loom_checker_cli.py`
- Test: A3 positive: open-pr-output-has-no-publish-word; negative: land-advice-says-run-open-pr-again. A4 positive: push-reminder-has-no-publishing; boundary: pretooluse-message-188-reworded. A7 positive: native-hook-bytes-unchanged; boundary: installed-hook-still-recognized.
- Risk: REQ-3/4/7; NATIVE_HOOK bytes must not change (existing byte-compare tests preserved); machine ids stay (spec Design decision).

**W2-01 Reword station prose and docs**  after: W1-01  acceptance: 5, 6
- Files: `loom-code/skills/ship/SKILL.md`, `loom-code/skills/ship/README.md`, `loom-code/skills/using-loom-code/SKILL.md`, `loom-code/skills/write-plan/references/confirm-intent.md`, `loom-design/skills/capture-intent/SKILL.md`, `loom-code/references/cli-results.md`, `README.md`, `loom-code/tests/test_ship_station_text.py`
- Test: A5 positive: ship-text-calls-open-pr; negative: no-station-text-runs-publish-subcommand. A6 positive: readme-and-cli-results-name-open-pr; boundary: history-under-docs-loom-untouched.
- Risk: REQ-5/6; existing `test_ship_station_text.py` assertions widened, not dropped.

**W2-02 Version bump and full suite**  after: W1-02, W2-01  acceptance: 8
- Files: `loom-code/.claude-plugin/plugin.json`, `loom-design/.claude-plugin/plugin.json`, `loom-code/CHANGELOG.md`, `loom-design/CHANGELOG.md`, `loom-code/tests/test_write_plan_station_text.py`, `loom-design/tests/spec/test_capture_intent_contract.py`, `loom-code/README*.md`, `loom-design/README*.md`
- Test: A8 positive: complete-package-suite-passes; boundary: version-metadata-sync-tests-pass.
- Risk: minor bumps via SSOT plus `scripts/sync_codex_manifests.py --all`; check origin/main version first (agent-decided).

## Simplicity check
- merge W1-01 and W1-02 into one checker task — declined: combined Files list is 10 entries, over the 8-entry cap; W1-02 stays sequential after W1-01
- drop the localized-README clause — taken
- add missing files (`test_ship_station_text.py`, plugin README variants) — taken

## Questions asked
① — what — 「直接移除」指移除開 PR 前的授權確認，還是移除 publish 這個字？
① — consequence — 授權欄位、狀態值、rule id、hook 腳本保留不改的代價說明
① — consequence — 舊命令只回 unknown sub-command 的代價
① — what — 這樣是你要的嗎？

## Risks
1. External scripts calling `publish` fail with unknown sub-command; disclosed and accepted at ① (user-decided).
2. Ship text and CLI must land in the same release, else agents on mixed versions call a missing command.
