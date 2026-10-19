# Remove expert-mode and its typed skip confirmation — plan
intent: 2026-10-01-remove-expert-mode@d66a74d1
charter: 1.1

## Current State Evidence
- Forward: `loom-code/hooks/hooks.json:31` and `hooks-codex.json:8` run `loom_checker.py selection capture --hook` on every prompt; `finalize.py` writes `attestation.selection` from `attestation.py:35` `selection_evidence`.
- Reverse: `verification.py:139` prints `valid (skipped: …)` only from `attestation.selection`; `command_handlers/publish.py:438` checks `Skipped steps:` only when a selection is bound.
- Error: `rule_checks/selection_guard.py` blocks commands naming the record store; the missing-checker fallbacks in `hooks.json:21` and `hooks-codex.json:19,28` repeat that guard inline.
- Data: `attestation.py:24` makes `selection` a required v2 key; `command_handlers/intake.py:60` reads `skipped-by-instruction: (spec|plan) <date>` records.
- Boundary: `loom-code/tests/test_selection_finalize.py` also covers probe caps and narrow-change skipping; `docs/loom/evidence/mechanisms.yaml` cites it as proof for surviving mechanisms.

## Task DAG
Wave 1 removes the hooks; wave 2 removes the checker, then the skill and prose, then adds the report section; wave 3 bumps versions.

**W1-01 Hooks stop capturing prompts and guarding the record store**  after: none  acceptance: 3
- Files: loom-code/hooks/hooks.json, loom-code/hooks/hooks-codex.json, loom-code/hooks/agy_adapter.py, scripts/opencode/loader.js, loom-*/opencode/loader.js, loom-code/tests/test_hooks_json.py, loom-code/tests/test_*agy_adapter.py, loom-code/tests/test_*opencode*.py
- Test: A3 positive: no hook on any host runs `selection capture` or guards the record store; negative: publish reminder and OpenCode language transcript still fire.
- Risk: agent-decided — missing-checker fallback keeps only its allow line; narrows test_hooks_json.py, test_agy_adapter.py, test_adversarial_agy_adapter.py, test_opencode_loader.py, test_adversarial_opencode_nested_prompt.py to surviving hooks.

**W2-01 Checker drops selection records and the selection command**  after: W1-01  acceptance: 2, 4, 5
- Files: loom-code/scripts/loom_checker.py, loom-code/scripts/loom_checker/*.py, loom-code/scripts/loom_checker/command_handlers/*.py, loom-code/scripts/loom_checker/rule_checks/*.py, loom-code/tests/test_*.py, loom-code/contract/manifest.yaml, docs/loom/evidence/mechanisms.yaml
- Test: A2 positive: plain-words reviewers skip discloses `absent`; negative: non-null `selection` refused. A4 positive: unbound runs keep `valid`/`stale`/`absent`; boundary: narrow-change auto-skip unchanged. A5 positive: dated spec record waives; negative: undated does not.
- Risk: agent-decided — keep schema v2, `selection` always null (no v3); delete selection modules, push.py helpers only they import, test_selection_{capture,store,ledger,guard}.py; test_selection_finalize.py loses only its selection cases, other coverage kept in place.

**W2-02 Delete the expert-mode skill and every offer of it**  after: W2-01  acceptance: 1, 3
- Files: loom-code/skills/**, loom-code/references/*.md, loom-design/skills/**, README.md, loom-code/README*.md, loom-code/tests/test_*.py, loom-code/scripts/check_mechanisms.py, tests/test_loom_skill_description_catalog.py
- Test: A1 positive: skill and command absent on all four hosts; negative: plain-words skip rule remains in each station. A3 positive: no expert-mode outside dated docs and released CHANGELOG sections; boundary: dated folders untouched.
- Risk: agent-decided — stations drop `selection show` and `record-failure` steps but keep the plain-words skip rule and record line; deletes test_expert_mode_skill.py; narrows test_simplified_station_text.py pins accordingly.

**W2-03 Acceptance report lists the steps the user skipped**  after: W2-02  acceptance: 6
- Files: loom-code/skills/closing-review/references/acceptance-test-report.md, loom-code/skills/closing-review/SKILL.md, loom-code/contract/manifest.yaml, loom-code/tests/test_*.py
- Test: A6 positive: report template and charter `must` list require a skipped-steps section; negative: when acceptance-test is skipped, closing-review tells the user the skipped steps in chat.
- Risk: agent-decided — one report section fed from the committed `skipped-by-instruction:` lines, no new checker rule; extends the existing charter `must` list and its charter test.

**W3-01 Version bump**  after: W2-03  acceptance: 7
- Files: loom-*/**/plugin.json, loom-*/package.json, loom-*/CHANGELOG.md, README.md, loom-*/README*.md, loom-*/tests/**/test_*.py
- Test: A7 positive: release-metadata sync test passes at the new versions; negative: `sync_codex_manifests.py --check --all` exits 0.
- Risk: agent-decided — minor for loom-code and loom-design (station guidance and a checker command change), patch for loom-workflow (synced loader only); every sync output committed.

## Simplicity check
- Keep test_selection_finalize.py's non-selection cases in place instead of moving them — taken
- Drop the acceptance-tester contract edit; the report template already sets its sections — taken

## Questions asked
① — what — 評估移除 expert-mode 是否合理；建議選項 A（完整移除） → 「開 change 做選項 A」
① — what — 移除後如何保留跳過紀錄（做法 1–5） → 「做 1＋3」
① — consequence — 紀錄附上使用者原話會永久公開 → 「不要留原話 只要留使用者指示跳過的記錄」
① — what — 覆述 intent（含自動發布授權） → 「對」

## Risks
1. Removing the selection guard makes the old record store writable again; it holds only stale local records and nothing reads it after this change.
2. Attestations already generated with a non-null `selection` become stale; none exist on open branches today.
3. user-decided — second-vendor selection-confirmed: codex
