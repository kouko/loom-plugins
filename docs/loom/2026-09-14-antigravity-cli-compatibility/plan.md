# Antigravity CLI compatibility — plan
intent: 2026-09-14-antigravity-cli-compatibility@e9584c45
charter: 1.0

## Current State Evidence
- Forward: `loom-code/.claude-plugin/plugin.json` and `.codex-plugin/plugin.json` exist per plugin; agy 1.2.2 `plugin validate` requires a root `plugin.json`, which no plugin has.
- Reverse: `loom-code/contract/manifest.yaml:17` station `review` must equal a skill folder per `loom-code/scripts/test_contract_manifest.py:63-68`; session-start derives station order from it.
- Error: `loom-workflow/skills/decision-map/SKILL.md:66-223` and `loom-memory/SKILL.md:15` use bare `${CLAUDE_PLUGIN_ROOT}`, which Codex and agy leave unsubstituted (path-lab spike 0/3).
- Data: `loom-code/hooks/hooks.json:3-35` reads Claude payloads (`tool_input.command`, `transcript_path`); agy sends camelCase `toolCall.args.CommandLine` and `transcriptPath`, and has no SessionStart event.
- Boundary: `scripts/sync_codex_manifests.py:38-53` mirrors only Codex manifests; `loom-code-ci.yml:127` checks drift; `scripts/test_loom_plugin_install_layout.py:342-360` pins per-host hook selection.

## Task DAG

### Wave 1

**W1-01 Rename review station to closing-review**  after: none  acceptance: 10, 8
- Files: loom-code/skills/closing-review/, loom-code/contract/manifest.yaml, loom-code/agents/, loom-code/scripts/, loom-design/skills/, loom-workflow/skills/loom-memory/scripts/test_skill_contract.py, docs/loom/evidence/mechanisms.yaml, README*.md
- Test: A10 positive: manifest-station-equals-closing-review-folder; negative: no-loom-code-review-invocation-remains. A8 positive: package-suite-passes-after-rename; boundary: finalize-review-command-and-gate-ids-unchanged.
- Risk: agent-decided — rename station id with skill so manifest-folder parity holds; keep `finalize-review` command, rule areas and gate-marker ids as internal ids; plugin READMEs in three languages updated together.

**W1-02 Host-neutral plugin-root wording and lint**  after: W1-01  acceptance: 3, 8
- Files: loom-code/skills/, loom-code/references/dispatch-profile.md, loom-design/skills/, loom-workflow/skills/decision-map/, loom-workflow/skills/loom-memory/, loom-code/scripts/check_contract_citations.py, scripts/test_loom_plugin_install_layout.py
- Test: A3 positive: skill-root-phrase-has-other-host-fallback; negative: bare-claude-plugin-root-without-fallback-rejected. A8 positive: pinned-doc-tests-updated-pass; boundary: sibling-lookup-allows-version-subdirectory.
- Risk: agent-decided — hybrid phrase (Claude variable, else two levels above SKILL.md) ran 6/6 across hosts in spike; bare relative `scripts/` paths rejected as unreliable; lint extends existing citation scanner rather than a new tool.

### Wave 2

**W2-01 Generate and check Antigravity manifests**  after: W1-01  acceptance: 1, 2, 8
- Files: scripts/sync_codex_manifests.py, scripts/test_sync_codex_manifests.py, loom-code/plugin.json, loom-design/plugin.json, loom-workflow/plugin.json, .github/workflows/loom-code-ci.yml, scripts/test_loom_plugin_install_layout.py
- Test: A1 positive: root-manifest-generated-and-validates; negative: drifted-root-manifest-fails-check. A2 positive: every-skill-folder-discoverable; boundary: closing-review-visible-beside-foreign-review-skill. A8 positive: codex-manifests-unchanged; negative: claude-ignores-root-manifest.
- Risk: agent-decided — extend the existing Codex sync script instead of a second generator; agy-dependent checks skip cleanly when `agy` is absent so CI stays host-agnostic.

**W2-02 Antigravity hooks for loom-code**  after: W1-01  acceptance: 4, 5, 6
- Files: loom-code/hooks.json, loom-code/hooks/agy_adapter.py, loom-code/scripts/test_agy_adapter.py, loom-code/scripts/test_hooks_json.py
- Test: A4 positive: unattested-push-returns-deny-with-reason; negative: non-push-command-returns-allow. A5 positive: invocation-zero-injects-station-order; boundary: later-invocations-inject-nothing. A6 positive: ja-skill-read-injects-anchor; negative: english-session-silent.
- Risk: agent-decided — one adapter translates agy payloads to existing handlers; session context and language anchor use PreInvocation because agy lacks SessionStart and PostToolUse cannot inject; adapter fails closed on push.

**W2-03 Antigravity folder-structure hook for loom-workflow**  after: none  acceptance: 7
- Files: loom-workflow/hooks.json, loom-workflow/scripts/agy-validate-skill-folder.sh, loom-workflow/tests/test-agy-validate-skill-folder.sh
- Test: A7 positive: nested-skill-subfolder-write-denied; negative: flat-skill-file-write-allowed.
- Risk: agent-decided — agy PostToolUse cannot block, so the rule moves to PreToolUse on file-write tools and checks the target path before writing; Claude hook stays unchanged.

**W2-04 Antigravity dispatch and tool mapping**  after: W1-02  acceptance: 3
- Files: loom-code/references/antigravity-tools.md, loom-code/skills/build/SKILL.md, loom-code/skills/closing-review/SKILL.md, loom-code/skills/write-plan/SKILL.md, loom-code/scripts/test_agy_tool_mapping.py
- Test: A3 positive: stations-reference-agy-tool-mapping; negative: mapping-names-no-claude-only-tool.
- Risk: agent-decided — one per-host mapping reference (superpowers pattern) instead of per-host skill copies; reviewers on agy dispatch loom agents via invoke_subagent; second-vendor policy unchanged.

### Wave 3

**W3-01 Install docs and host principles**  after: W1-01, W2-01, W2-02, W2-03  acceptance: 1, 9
- Files: README.md, loom-code/README.md, loom-code/README.ja.md, loom-code/README.zh-TW.md, loom-design/README.md, loom-workflow/README.md, PRINCIPLES.md, AGENTS.md
- Test: A1 positive: readme-agy-install-steps-from-clone; negative: readme-claims-agy-marketplace. A9 positive: principles-name-antigravity-cli; boundary: principles-non-negotiables-count-unchanged.
- Risk: agent-decided — clone plus `agy plugin install <dir>` per plugin, loom-code first; Japanese and Traditional Chinese READMEs get the same section; PRINCIPLES amendment line records the user-confirmed host addition.

**W3-02 Antigravity host lines in loom-design and drift hook**  after: W2-01, W2-04  acceptance: 3, 8
- Files: loom-design/skills/capture-intent/references/second-vendor.md, loom-design/scripts/spec/test_capture_intent_contract.py, .claude/hooks/check-codex-manifest-drift.sh, .claude/hooks/test_check_codex_manifest_drift.py
- Test: A3 positive: capture-intent-names-agy-probe-order; negative: capture-intent-offers-host-vendor. A8 positive: drift-hook-message-names-both-manifests; boundary: codex-drift-block-unchanged.
- Risk: agent-decided — added after W2-04 found loom-design's second-vendor copy lists only Codex and Claude hosts and W2-01 found the drift hook message Codex-only; wording mirrors the loom-code reference.

## Questions asked
① — what — 在 Antigravity 裡你希望做到多「能用」？（答：整條流程能走完）
① — what — 三個 plugin 都要支援 Antigravity 嗎？（答：三個都要）
① — what — 這次是給誰用？（答：也要讓別人能裝）
① — consequence — review 在 agy 撞名：只改 Antigravity 版（A）或三邊都保留 review（B）？（答：改為三邊都改名）
① — what — 提案 loom 專屬的審查站名字（答：closing-review）
① — consequence — 覆述 intent，含：舊名不留轉接、agy 上審查由 Gemini 執行、clone 後逐一安裝、原則加入 Antigravity、審查通過後自動 push 並開 PR（答：對）

## Risks
1. user-decided — review station renamed closing-review on all hosts with no alias, because agy de-duplicates skills by short name and an alias would collide again.
2. Hooks fire only in the agy CLI; Antigravity desktop and IDE are out of scope, so gates there are unenforced and the README must say so.
3. Path resolution relies on the model deriving the plugin root; spike samples were small, so the blind run on agy exercises every station's checker command.
4. agy 1.2.2 behaviour (hook payloads, skill de-duplication) is undocumented and may change; adapters parse defensively and fail closed on the push gate.
