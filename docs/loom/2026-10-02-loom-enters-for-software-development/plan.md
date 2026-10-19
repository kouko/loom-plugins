# Loom enters for software development without outside rules — plan
intent: 2026-10-02-loom-enters-for-software-development@7122ccd3
charter: 1.1

## Current State Evidence
- Forward: `loom-code/hooks/session-start` body names stations and decision points but never says which requests enter loom; `hooks/hooks.json` and `hooks-opencode.json` run it at SessionStart.
- Reverse: `loom-code/hooks/hooks-codex.json` has only PreToolUse, so Codex gets no session-start text; agy gets it through `agy_adapter.py` pre-invocation.
- Error: session-start prints two defensive keys; loom-workflow commit 6603aca8 saw Codex 0.154 mark such a hook Failed and drop the text.
- Data: capture-intent, maintain and write-plan descriptions claim only named or existing-intent work; `tests/test_loom_skill_description_catalog.py` caps all descriptions at 4,047 chars (3,370 used).
- Boundary: `loom-code/tests/test_session_start_words.py` caps the empty-repo output at 2,639 words (258 now); `LOOM_CODE_MODE=off` stays the only opt-out.

## Task DAG
Wave 1 changes the entry surfaces and fixes the #74 leftovers independently; wave 2 bumps versions.

**W1-01 Session-start text routes software-development requests into loom on all hosts**  after: none  acceptance: 4, 5
- Files: loom-code/hooks/session-start, loom-code/hooks/hooks-codex.json, loom-code/tests/test_session_start_words.py, loom-code/tests/test_hooks_json.py, loom-code/tests/local/test-superpowers-mode-off.sh, tests/test_loom_plugin_install_layout.py
- Test: A4 positive: agy-and-opencode-get-routing-line; negative: mode-off-prints-nothing. A5 positive: codex-hook-prints-only-hookSpecificOutput; boundary: mode-off-empty-output-has-same-shape.
- Risk: agent-decided — one routing paragraph, no repo-detection branch; every host prints only hookSpecificOutput, no host flag; narrows test_session_start_words.py three-key assertion to one key.

**W1-02 Entry skill descriptions claim unnamed feature and bug-fix requests**  after: none  acceptance: 1, 2, 3
- Files: loom-design/skills/capture-intent/SKILL.md, loom-code/skills/write-plan/SKILL.md, tests/test_loom_skill_description_catalog.py
- Test: A1 positive: unbranded-feature-request-enters-capture-intent; negative: write-plan-not-claimed-without-intent. A2 positive: loom-asked-small-edit-enters; boundary: typo-or-rename-goes-direct. A3 positive: code-change-claimed; negative: research-or-notes-not-claimed.
- Risk: agent-decided — reword two descriptions inside the 4,047-char budget, no new skill; maintain already claims bug reports and stays unchanged.

**W1-03 Remove the three leftovers from PR #74**  after: none  acceptance: 6
- Files: loom-code/skills/ship/SKILL.md, loom-code/scripts/loom_checker/verification.py, loom-code/scripts/loom_checker/command_handlers/*.py, loom-code/tests/test_verification_status.py, loom-code/tests/test_pr_floor.py, loom-code/tests/test_selection_finalize.py
- Test: A6 positive: narrow-change-sentence-gone, depth-parameter-gone, trailing-blank-line-gone-from-test_selection_finalize; negative: existing-verification-statuses-unchanged.
- Risk: agent-decided — drop depth from verification_status and its callers; test_verification_status.py and pr-floor tests narrow only the depth argument, coverage of statuses preserved.

**W2-01 Version bump**  after: W1-01, W1-02, W1-03  acceptance: 7
- Files: loom-*/**/plugin.json, loom-*/package.json, loom-*/CHANGELOG.md, README.md, loom-*/README*.md, loom-*/tests/**/test_*.py
- Test: A7 positive: release-metadata sync tests pass at the new versions; negative: `sync_codex_manifests.py --check --all` exits 0.
- Risk: agent-decided — minor for loom-code and loom-design (station guidance and hook change); loom-workflow untouched unless a synced file changes.

**W3-01 Graduate the loom-code-only entry probe into the suite**  after: W2-01  acceptance: 1
- Files: docs/loom/2026-10-02-loom-enters-for-software-development/evidence/probes/test_abuse_loom_code_only_entry.py, loom-code/tests/test_session_start_loom_code_only_entry.py
- Test: A1 positive: loom-code-only-session-start-names-write-plan-fallback; negative: write-plan-description-keeps-loom-code-only-entry-role.
- Risk: agent-decided — move the adversary's red probe into loom-code/tests after the routing fix makes it green; the probe file leaves the change store.

## Simplicity check
- W1-03 Files name test_selection_finalize.py so A6's blank-line part has an owner — taken
- Drop the --host=codex flag; every host prints only hookSpecificOutput — taken
- Remove cases.md from W1-02; descriptions are not in its frozen hash — taken
- Leave maintain's description unchanged; it already claims bug reports — taken

## Questions asked
① — what — 在有用 loom 的 repo 裡，哪些請求要自動走 loom 流程 → 「功能與修 bug（推薦）」
① — what — 在沒有用 loom 的資料夾開 session 時，loom 要不要出現（A 安靜／B 一行提示／C 現狀／D 軟體開發一律用） → 「Ｄ」
① — what — 存放暫時不做的點子的地方要放進這次嗎 → 「不放，之後再說（推薦）」
① — what — 驗收時要在哪些工具上實際試 → 「Claude Code + Codex（推薦）」
① — consequence — 覆述 intent，含所有安裝者預設改變與自動發布授權 → 「對」

## Risks
1. user-decided — every loom install now routes feature and bug-fix work into loom in any folder; the only opt-out is LOOM_CODE_MODE=off.
2. Codex runs the new SessionStart hook only after the user trusts the plugin's hooks once.
3. The agent must judge "software development"; misjudged notes or research sessions are caught by acceptance line 3's live trial.
