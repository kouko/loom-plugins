# Relay results in the user's conversation language — plan
intent: 2026-10-04-relay-results-in-user-language@69405c71
charter: 1.1

## Current State Evidence
- Forward: `loom-code/hooks/language-anchor.py` emits a zh/ja directive only on PostToolUse with tool_name `Skill`; its zh text hardcodes 繁體中文.
- Reverse: `loom-code/tests/test_language_anchor_hook.py` pins ZH_FRAGMENT "會話語言（繁體中文）"; `loom-code/tests/test_hooks_json.py` pins one SessionStart command and the PostToolUse matcher set {Skill}.
- Error: build/SKILL.md:90 and closing-review/SKILL.md:10 name only English artifacts; ship/SKILL.md:12 covers only the PR body.
- Data: `agy_adapter.py` and `opencode/loader.js` reuse `_ANCHOR_TEXT` keyed by detected language; keys must stay `zh`/`ja`.
- Boundary: Claude Code docs confirm SessionStart `compact|resume` accepts additionalContext; no documented hook fires on a background-agent completion turn.

## Task DAG
Wave 1 changes station prose and the existing anchor independently; wave 2 releases.

**W1-01 Stations say agent results reach the user in the user's language**  after: none  acceptance: 1, 2, 5
- Files: loom-code/skills/build/SKILL.md, loom-code/skills/closing-review/SKILL.md, loom-code/skills/ship/SKILL.md, loom-code/tests/test_simplified_station_text.py
- Test: A1 positive: build-and-closing-review-relay-sentence-pinned; boundary: no-user-message-turn-clause-pinned. A2 positive: ship-sentence-covers-every-user-message; boundary: decision-point-3-named. A5 positive: english-artifact-sentences-unchanged; negative: pr-body-language-clause-kept.
- Risk: agent-decided — one sentence beside each existing English-artifact sentence; ship's line 12 widened, not duplicated; exact-sentence pins.

**W1-02 Language anchor fires on resume and agent results with neutral wording**  after: none  acceptance: 3, 4
- Files: loom-code/hooks/language-anchor.py, loom-code/hooks/hooks.json, docs/loom/evidence/mechanisms.yaml, loom-code/tests/test_language_anchor_hook.py, loom-code/tests/test_hooks_json.py, loom-code/tests/test_agy_adapter.py, loom-code/tests/test_opencode_loader.py, loom-code/tests/test_adversarial_opencode_command_language.py
- Test: A3 positive: compact-resume-and-agent-result-emit-anchor; negative: bash-tool-stays-silent. A4 positive: zh-anchor-names-conversation-language; negative: en-majority-stays-silent.
- Risk: agent-decided — separate SessionStart compact|resume entry; hook_event_name echoed, PostToolUse when absent; `_ANCHOR_TEXT` keys kept; new ids registered host-hygiene; tests widened, ZH_FRAGMENT changed; SubagentStop skipped.

**W1-03 Language detection ignores harness-written user turns**  after: W1-02  acceptance: 3
- Files: loom-code/hooks/lang_detect.py, loom-code/hooks/language-anchor.py, loom-code/tests/test_lang_detect.py, loom-code/tests/test_language_anchor_hook.py
- Test: A3 positive: zh-turns-plus-compact-summary-still-zh; negative: genuine-english-user-turn-still-counts. A3 boundary: skill-reinvocation-echo-not-counted.
- Risk: agent-decided — adversary found English compaction summaries outvote the user; skip isCompactSummary and isMeta turns plus the re-invocation prefix; reject non-string hook_event_name; detector coverage widened only.

**W2-01 Release metadata for loom-code 3.31.0**  after: W1-01, W1-02  acceptance: 6
- Files: loom-code/CHANGELOG.md, loom-code/plugin.json, loom-code/.claude-plugin/plugin.json, loom-code/.codex-plugin/plugin.json, loom-code/package.json, README.md, loom-code/README*.md, loom-code/tests/test_write_plan_station_text.py
- Test: A6 positive: release-metadata-sync-test-passes-at-3.31.0; negative: sync-codex-manifests-check-exits-0.
- Risk: agent-decided — minor bump because station guidance and a hook trigger change; loom-design and loom-workflow untouched.

**W2-02 Graduate the compact-summary probe**  after: W1-03  acceptance: 3
- Files: docs/loom/2026-10-04-relay-results-in-user-language/evidence/probes/test_language_anchor_compact_summary.py, loom-code/tests/test_adversarial_language_anchor_compact_summary.py
- Test: A3 positive: graduated-probe-passes-in-suite; negative: compact-summary-vote-regression-fails-probe.
- Risk: agent-decided — the probe caught the compact-summary vote defect, so review.probe-graduation moves it into loom-code/tests unchanged apart from the path.

## Simplicity check
- Reuse the existing anchor and its detector instead of a new reminder hook — taken
- Widen ship's existing PR-body sentence instead of adding a new one — taken

## Questions asked
① — what — 只改說明／加在每次載入的說明／只靠 memory（A/B/C） → 「A」
① — what — codex review 後：A／A+（擴大既有語言提醒）／只擴大提醒 → 「A+，但提醒用使用者對話使用的語言，不固定繁體中文」
① — what — 覆述 intent（含自動發布授權） → 「對」

## Risks
1. PostToolUse(Agent) covers foreground agents only; a background agent's completion turn has no documented hook and SubagentStop is skipped, so acceptance testing reports both as uncovered.
2. Prose and reminders already failed once on a turn that carried a reminder; this change raises the odds, it does not prove the drift is gone.
3. Codex and OpenCode hook files are not rewired; Claude Code only.
