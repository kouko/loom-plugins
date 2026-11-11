# Quiet Stop feedback — plan
intent: 2026-11-11-stop-feedback-noise@57803f88
spec: docs/loom/2026-11-11-stop-feedback-noise/spec.md@05d800b1
charter: 1.1

## Task DAG
### Wave 1
**W1-01 Frame delivery feedback for each host and permit normal pauses** after: none acceptance: 1,2,3
- Files: loom-code/scripts/loom_checker/command_handlers/publish.py (entry: cmd_delivery), loom-code/hooks/hooks.json, loom-code/hooks/hooks-codex.json, loom-code/tests/test_delivery_stop.py, loom-code/tests/test_hooks_json.py, loom-code/tests/test_hook_recovery_literal_path.py, loom-code/skills/ship/SKILL.md
- Test: A1 positive: host-first-feedback; boundary: repeat-and-background-silence. A2 positive: explicit-delivery-preserved; boundary: unconfirmed-no-continuation. A3 positive: packaged-host-replay; boundary: invalid-host-and-literal-recovery.
- Risk: agent-decided — REQ-1/2/3 design; preserve test_delivery_stop.py and hook replay coverage except intentional repeated stderr removal. Keep observer behavior unchanged; repair both packaged recovery hints and execute the recovered invocation.

### Wave 2
**W2-01 Synchronize code release metadata** after: W1-01 acceptance: 1,2,3
- Files: loom-code/.claude-plugin/plugin.json, loom-code/CHANGELOG.md, loom-code/README*.md, README.md, loom-code/tests/test_write_plan_station_text.py, scripts/sync_codex_manifests.py (invoke only; generated manifests)
- Test: A1 positive: release-sync; boundary: stale-pin. A2 positive: release-sync; boundary: stale-pin. A3 positive: release-sync; boundary: stale-pin.
- Risk: agent-decided — minor 3.65.0 for changed hook invocation contract; CHANGELOG entry and current-version pin rewrite land before closing review.

### Wave 3
**W3-01 Restrict publication reminders to verified committed work** after: W2-01 acceptance: 1,2,3
- Files: loom-code/scripts/loom_checker/command_handlers/publish.py (entry: cmd_delivery; hook behavior only), loom-code/tests/test_delivery_stop.py, loom-code/skills/ship/SKILL.md, loom-code/CHANGELOG.md
- Test: A1 positive: eligible-reminder; boundary: absent-stale-pending-no-remote. A2 positive: explicit-delivery-and-skip-publication-preserved; boundary: changed-head-no-continuation. A3 positive: packaged-host-replay; boundary: human-wait-remains-conditional.
- Risk: agent-decided — reuse verification_status/local delivery; no workflow state. Preserve W1 response/recovery tests and explicit delivery/publication semantics. Exercise real valid/stale attestations with existing fixtures. Silent skip paths never refuse publication; retain 3.65.0 before review.

## Simplicity check
- none found

## Questions asked
① — what — 確認照此範圍進行嗎？
① — what — 反覆出現「Ran 1 stop hook／Stop hook error」的是哪個介面？我會用它驗證實際顯示與重複觸發情況。

## Risks
1. User confirmed Claude Code as affected and requested Codex testing. Native Codex framing was exercised; Claude account quota prevented Stop execution. Do not treat local JSON tests as proof of Claude UI behavior or automatically use another provider.
2. A normal first reminder may still ask the agent to stop and explain a pending human decision. The repeated event is silent; no language classifier guesses that the user has approved publication or merge.
3. No installed plugin/settings change and no merge of PR #140. Record source, native host support and installed adoption separately.
4. No outside review selected. Claude executor is installed but currently quota-blocked; availability does not authorize another review.
5. user-decided — proceed with evidence investigation and bounded revision (2026-11-11). [Research](research/01-stop-readiness-evidence.md) establishes conversational uncertainty. W3 preserves Acceptance, explicit commands and prior W1/W2 evidence. Closing review has not begun; budgets and retries are not reset.
