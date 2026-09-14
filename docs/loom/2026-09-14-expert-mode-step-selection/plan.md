# Let the user choose which Loom steps a single change runs — plan
intent: 2026-09-14-expert-mode-step-selection@17aaaa83
spec: docs/loom/2026-09-14-expert-mode-step-selection/spec.md@c143ac7a
charter: 1.0

## Task DAG
<!-- When a spec requirement changes after this commit, the un-landed
     tasks it touches are replaced and the reason is named in the commit
     message. Landed tasks stay as they are. -->

### Wave 1 — record store and lane removal

**W1-01 Selection store, vocabulary and lifetimes**  after: none  acceptance: 1, 6, 7
- Files: `loom-code/contract/manifest.yaml`, `loom-code/scripts/loom_checker/selection.py`, `loom-code/scripts/loom_checker/command_handlers/selection.py`, `loom-code/scripts/loom_checker.py`, `loom-code/scripts/test_selection_store.py`
- Test: A1 positive: propose-prints-table-code-and-cancel-restores-full; negative: unknown-step-or-unmet-dependency-refused. A6 positive: same-branch-and-base-applies; boundary: reused-change-id-on-new-branch-inherits-nothing. A7 positive: failure-survives-rebase; boundary: selection-lapses-after-rebase.
- Risk: store lives under the git common dir, shared by worktrees; branch plus merge-base scoping per spec decisions 2 and 6. agent-decided.

**W1-02 Remove lane grammar from the intent checker**  after: none  acceptance: 10
- Files: `loom-code/scripts/loom_checker/rule_checks/intent.py`, `loom-code/scripts/loom_checker/command_handlers/intent.py`, `loom-code/scripts/loom_checker/rules.py`, `loom-code/scripts/test_loom_checker_intent.py`, `loom-code/skills/review/references/lenses.md`
- Test: A10 positive: intent-with-leftover-lane-line-passes-schema; negative: no-lane-grammar-symbol-left-in-checker.
- Risk: removing check_lane_reason may break the shared deciding-commit helper; keep the helper, drop only lane prefixes per spec decision 15. agent-decided.

**W1-03 Remove lane settings from contract and templates**  after: W1-01  acceptance: 10
- Files: `loom-code/contract/manifest.yaml`, `loom-code/contract/templates/intent.md`, `loom-code/contract/templates/KICKOFF-DEFAULTS.md`, `docs/loom/evidence/mechanisms.yaml`, `docs/loom/KICKOFF-DEFAULTS.md`, `loom-code/scripts/test_contract_manifest.py`
- Test: A10 positive: manifest-templates-and-mechanisms-agree-without-lane; negative: reintroduced-default-lane-key-fails-manifest-test.
- Risk: shares the manifest with W1-01, so it runs after it; the KICKOFF line removal carries a dated reason line per charter. agent-decided.

### Wave 2 — capture, guard and gates

**W2-01 Prompt capture hook on both hosts**  after: W1-01  acceptance: 1, 2, 9
- Files: `loom-code/hooks/hooks.json`, `loom-code/hooks/hooks-codex.json`, `loom-code/scripts/loom_checker/command_handlers/selection.py`, `loom-code/scripts/test_selection_capture.py`, `loom-code/scripts/test_hooks_json.py`
- Test: A1 positive: user-prompt-with-code-binds-and-returns-system-message; negative: withdraw-token-records-cancel-not-binding. A2 positive: payload-without-prompt-ref-refused; boundary: plain-yes-binds-nothing. A9 positive: codex-turn-id-payload-binds-same-record; boundary: bare-expert-mode-token-matches.
- Risk: Codex literal for a plugin skill is unconfirmed; match both `$expert-mode` and `$loom-code:expert-mode` prefixes per spec decision 13 (codex PR #31348). agent-decided.

**W2-02 PreToolUse guard over the record store**  after: W2-01  acceptance: 2
- Files: `loom-code/hooks/hooks.json`, `loom-code/hooks/hooks-codex.json`, `loom-code/scripts/loom_checker/rule_checks/selection_guard.py`, `loom-code/scripts/loom_checker/command_handlers/push.py`, `loom-code/scripts/test_selection_guard.py`
- Test: A2 positive: relative-path-and-rev-parse-record-writes-denied; negative: ls-models-selections-and-selection-cancel-pass.
- Risk: Codex fires PreToolUse for apply_patch since codex PR #18391 (0.154.0 installed); older Codex misses file-edit guarding, disclosed per spec decision 3. agent-decided.

**W2-03 Finalization and attestation v2**  after: W1-01, W1-03  acceptance: 3, 7
- Files: `loom-code/scripts/loom_checker/command_handlers/finalize.py`, `loom-code/scripts/loom_checker/attestation.py`, `loom-code/contract/manifest.yaml`, `loom-code/contract/templates/attestation.json`, `loom-code/scripts/test_loom_attestation.py`, `loom-code/scripts/test_selection_finalize.py`
- Test: A3 positive: bound-skip-of-reviewers-and-adversarial-validates; negative: unbound-skip-refused-and-digest-mismatch-blocks. A7 positive: finalize-failure-recorded-and-listed-as-prior; boundary: failure-after-confirmation-not-listed-as-prior.
- Risk: v1 attestations must keep validating; waivers apply only to steps in selection.skip per spec decision 9. agent-decided.

**W2-04 Publish disclosure and skipped-review ledger**  after: W2-03  acceptance: 5, 8
- Files: `loom-code/scripts/loom_checker/rule_checks/publish.py`, `loom-code/scripts/loom_checker/command_handlers/publish.py`, `loom-code/scripts/loom_checker/command_handlers/selection.py`, `loom-code/scripts/test_loom_publish.py`, `loom-code/scripts/test_selection_ledger.py`
- Test: A5 positive: matching-skipped-and-prior-failure-lines-publish; negative: missing-authority-or-failure-line-refused. A8 positive: merged-change-skipping-reviewers-listed; boundary: none-prints-no-merged-change-skipped-review.
- Risk: nine-heading validator must stay exact; disclosure lives under Verification per spec decision 10. agent-decided.

### Wave 3 — skill surface and accounting

**W3-01 expert-mode skill and station reads**  after: W2-01, W2-02, W2-03, W2-04  acceptance: 1, 4
- Files: `loom-code/skills/expert-mode/SKILL.md`, `loom-code/skills/expert-mode/agents/openai.yaml`, `loom-code/skills/build/SKILL.md`, `loom-code/skills/review/SKILL.md`, `loom-code/skills/ship/SKILL.md`, `loom-code/skills/write-plan/SKILL.md`, `loom-code/scripts/test_expert_mode_skill.py`, `loom-code/scripts/test_simplified_station_text.py`
- Test: A1 positive: frontmatter-disables-model-invocation-and-openai-yaml-blocks-implicit; negative: skill-text-evaluates-no-gate. A4 positive: suggestion-then-plain-yes-skips-nothing; boundary: station-text-suggests-once-without-waiting.
- Risk: station prose grows past token caps; each station gains one read-selection sentence only per spec decision 7. agent-decided.

**W3-02 Principles amendment, mechanisms and release**  after: W1-02, W1-03, W3-01  acceptance: 9, 10
- Files: `PRINCIPLES.md`, `docs/loom/evidence/mechanisms.yaml`, `loom-code/CHANGELOG.md`, `loom-code/.claude-plugin/plugin.json`, `loom-code/.codex-plugin/plugin.json`, `loom-code/contract/manifest.yaml`, `loom-code/scripts/test_check_mechanisms.py`
- Test: A10 positive: check-mechanisms-and-package-suite-green; negative: unregistered-selection-mechanism-red. A9 positive: codex-manifest-sync-check-passes; boundary: claude-codex-version-mismatch-fails.
- Risk: PRINCIPLES signature is the user's; amendment text lands with ratified-by pending until kouko signs at acceptance. agent-decided.

## Questions asked
① — consequence — Package tests as a fixed floor; user: "測試不一定要跑"
① — what — Agent-opened entry point, three options; user: "用方案3 但我希望如果是agent自己觸發的時候 能不要擋住當前的執行流程 避免流程被頻繁中斷"
① — what — Restated intent plus automatic publication; user: "對"
① — consequence — Guard excludes disguised commands, reviewer rejection recorded only when handed over, withdraw added; user: "接受 另外我想確認 /loom-code:expert-mode 取消 <- 這應該是用語意判定的 不是固定用中文「取消」 兩個字對嗎？"

## Risks
1. Codex measured: PreToolUse covers apply_patch after PR #18391; the plugin-skill mention literal stays unconfirmed, so capture matches both forms and the blind run checks the real Codex prompt.
2. A text-matching guard cannot recognise every shell write; REQ-2 is bound to recognised forms, the boundary kouko accepted in the intent.
3. The PRINCIPLES.md non-negotiable 2 amendment needs kouko's own ratified-by line; it is presented with the acceptance report, never signed by an agent.
4. Protected paths (skills, hooks, contract) make the computed reviewer floor two; the adversary must attack capture forgery, table swap and failure erasure.
5. The branch is named KICKOFF-DEFAULTS-redesign, not the change-id; publication derives the change-id from the attestation path, so no rename is required.
