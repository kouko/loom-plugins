# Language-neutral anchor — plan
intent: 2026-10-05-language-neutral-anchor@e585694d
charter: 1.1

## Current State Evidence
- Forward: `loom-code/hooks/language-anchor.py` calls `lang_detect.conversation_language()` and emits `_ANCHOR_TEXT[zh|ja]`; any other result prints nothing.
- Reverse: `loom-code/tests/test_language_anchor_hook.py`, `test_lang_detect.py` and three graduated adversarial tests pin per-language output and detector votes.
- Error: `lang_detect.detect_script` counts each ASCII letter as one vote, so zh dense with English terms resolves `en` and the anchor stays silent.
- Data: `loom-code/hooks/agy_adapter.py:254-263` reuses `_ANCHOR_TEXT` and `lang_detect.majority_language`; OpenCode runs `language-anchor.py` through `hooks-opencode.json`.
- Boundary: `lang_detect.py` has no runtime consumer outside `language-anchor.py` and `agy_adapter.py`; `transcript_path` is read only by them, the OpenCode prompt file existing for them alone; Codex wires no anchor.

## Task DAG
Wave 1 replaces detection with one fixed reminder per host, then deletes what only detection used; wave 2 releases.

**W1-01 Claude Code and OpenCode anchor emits one fixed English reminder**  after: none  acceptance: 1, 2, 3, 4, 5
- Files: loom-code/hooks/language-anchor.py, loom-code/tests/test_language_anchor_hook.py, loom-code/tests/test_adversarial_language_anchor_compact_summary.py, loom-code/tests/test_opencode_loader.py, loom-code/tests/test_adversarial_opencode_command_language.py
- Test: A1 positive: zh-with-english-terms-gets-anchor; boundary: compact-summary-transcript-gets-anchor. A2 positive: en-ko-fr-transcripts-get-same-text; negative: text-names-no-language-or-script. A3 positive: text-asks-for-user-language-and-script; boundary: missing-transcript-still-emits. A4 positive: opencode-skill-result-gets-same-text; negative: bash-tool-stays-silent. A5 positive: machine-artifact-clause-kept; negative: unknown-event-stays-silent.
- Risk: agent-decided — detector-vote cases and the two probes guarding misreads are deleted, their failure gone; event, tool and malformed-input gates narrowed to one text; English text per user.

**W1-02 Antigravity anchor uses the same text**  after: W1-01  acceptance: 4
- Files: loom-code/hooks/agy_adapter.py, loom-code/tests/test_agy_adapter.py, loom-code/tests/test_adversarial_agy_anchor_turns.py, loom-code/tests/test_adversarial_agy_adapter.py
- Test: A4 positive: agy-skill-read-gets-same-text; negative: agy-second-invocation-same-read-stays-silent.
- Risk: agent-decided — once-per-skill-read gate kept; English-turn cases (anchor_turns :95, :104) flip from silence to the anchor; '日本語' asserts (agy_adapter :264, :293) rewritten to the fixed text.

**W1-03 OpenCode loader stops recording user prompts**  after: W1-01  acceptance: 4
- Files: scripts/opencode/loader.js, loom-code/opencode/loader.js, loom-design/opencode/loader.js, loom-workflow/opencode/loader.js, loom-code/tests/test_opencode_loader.py
- Test: A4 positive: opencode-skill-result-still-gets-anchor-without-prompt-file; negative: prompt-file-never-written.
- Risk: agent-decided — delete transcript(), spoken(), the keepsTranscript append and transcript_path payload fields (no reader left, verified by git grep); copies synced by sync_codex_manifests.py; loader test narrowed.

**W1-04 Delete the language detector**  after: W1-02, W1-03  acceptance: 6
- Files: loom-code/hooks/lang_detect.py, loom-code/tests/test_lang_detect.py, loom-code/tests/test_hooks_json.py, loom-code/scripts/check_mechanisms.py, loom-code/tests/test_check_mechanisms.py
- Test: A6 positive: package-suite-passes-without-detector; negative: no-runtime-file-names-lang-detect.
- Risk: agent-decided — test_lang_detect.py deleted with its module; KEPT_HOOK_FILES and HOST_HYGIENE_ALLOWLIST drop lang_detect; the synthetic allowlist case renamed or deleted.

**W2-01 Release metadata for loom-code 3.32.0**  after: W1-04  acceptance: 6
- Files: loom-code/CHANGELOG.md, loom-code/plugin.json, loom-code/.claude-plugin/plugin.json, loom-code/.codex-plugin/plugin.json, loom-code/package.json, README.md, loom-code/README*.md, loom-code/tests/test_write_plan_station_text.py
- Test: A6 positive: release-metadata-sync-test-passes-at-3.32.0; negative: sync-codex-manifests-check-exits-0.
- Risk: agent-decided — minor bump because a hook's emitted text and trigger condition change.

**W2-02 Patch releases for loom-design and loom-workflow loader copies**  after: W1-03  acceptance: 6
- Files: loom-design/CHANGELOG.md, loom-design/plugin.json, loom-design/.claude-plugin/plugin.json, loom-design/.codex-plugin/plugin.json, loom-workflow/CHANGELOG.md, loom-workflow/plugin.json, loom-workflow/.claude-plugin/plugin.json, loom-workflow/.codex-plugin/plugin.json
- Test: A6 positive: each-plugin-version-test-passes; negative: sync-codex-manifests-check-exits-0.
- Risk: agent-decided — patch bumps so installed copies receive the synced loader; also update each plugin's package.json, README and version-pin test the sync or version tests name.

## Simplicity check
- Delete the detector and its tests rather than keep it unused — taken
- Stop OpenCode's loader writing its per-session prompt file — taken

## Questions asked
① — what — 語言判斷：A 改計分方式／E 不判斷、每次送同一句中性提醒 → 「走 E 吧」
① — what — 覆述 intent（含自動發布授權） → 「對」
① — consequence — 提醒用英文／中文／中英各一句 → 「英文」

## Risks
1. user-decided — reminder written in English: neutral across languages; its pull on a non-English conversation is weaker than a native-language reminder, which acceptance testing measures live.
2. English conversations now also receive one reminder line per trigger.
3. The model, not a program, identifies the language; a reply can still drift, and this change cannot prove it never does.
