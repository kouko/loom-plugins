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

### Wave 4 — fixes from the first blind run (intent re-confirmed 2026-09-14)

**W4-01 Language anchor looks back past tool results**  after: W3-02  acceptance: 6
- Files: loom-code/hooks/agy_adapter.py, loom-code/scripts/test_agy_adapter.py
- Test: A6 positive: skill-read-before-tool-result-injects-anchor; negative: skill-read-in-earlier-user-turn-silent.
- Risk: agent-decided — agy calls the model after the view_file result step lands, so match the latest skill read within the current user turn instead of only the newest model step; verified live on agy.

**W4-02 Absolute agy workspace path and dispatch wording**  after: W3-02  acceptance: 5
- Files: README.md, loom-code/README.md, loom-code/README.ja.md, loom-code/README.zh-TW.md, loom-design/README.md, loom-workflow/README.md, loom-code/references/antigravity-tools.md, scripts/test_agy_install_docs.py
- Test: A5 positive: readme-uses-absolute-add-dir; negative: readme-relative-add-dir-dot-rejected.
- Risk: agent-decided — agy 1.2.2 ignores a relative `--add-dir .`; document `--add-dir "$PWD"`, narrow the no-workspace claim to observed `agy -p`, and say one self invocation per dispatch.

**W4-03 Push gate names the missing attestation first**  after: W3-02  acceptance: 4, 8
- Files: loom-code/scripts/loom_checker/command_handlers/push.py, loom-code/scripts/loom_checker/rule_checks/push.py, loom-code/scripts/test_loom_publish.py, loom-code/scripts/test_publish_command_detection.py
- Test: A4 positive: plain-push-without-attestation-reason-names-attestation; negative: attested-noncanonical-push-still-blocked. A8 positive: blocked-push-set-unchanged; boundary: canonical-attested-push-allowed.
- Risk: user-decided — report the missing attestation before the canonical-rendering refusal on every host; the set of blocked commands must stay identical, pinned by existing publish tests.

**W4-04 Closing review commits the blind-run report**  after: W3-02  acceptance: 3
- Files: loom-code/skills/closing-review/SKILL.md, loom-code/scripts/test_review_convergence_contract.py
- Test: A3 positive: station-commits-report-before-finalize; negative: finalize-before-report-commit-not-instructed.
- Risk: agent-decided — finalize-review already requires a clean tree; state explicitly that the blind-run report is committed before finalize so agy runs do not leave it untracked.

### Wave 5 — closing-review findings after re-confirmation (intent re-confirmed again 2026-09-14)

**W5-01 Skill and docs findings**  after: W4-04  acceptance: 1, 3
- Files: loom-workflow/README.ja.md, loom-workflow/README.zh-TW.md, loom-code/skills/closing-review/SKILL.md, loom-code/references/antigravity-tools.md, loom-code/skills/write-plan/references/second-vendor-ask-and-docs-lint.md, loom-design/skills/capture-intent/references/second-vendor.md, scripts/test_agy_install_docs.py, loom-code/scripts/test_review_convergence_contract.py
- Test: A1 positive: loom-workflow-ja-zh-readmes-have-agy-section; negative: agy-section-missing-in-any-translation-fails. A3 positive: report-committed-before-reviewers-read-final-digest; negative: report-commit-after-verdicts-not-instructed.
- Risk: agent-decided — commit the blind-run report before reviewers read the final digest; agy offers no second-vendor runner yet, so both second-vendor references say so instead of probing; trim orientation-only hook section and duplicate wording.

**W5-02 Code findings**  after: W4-03  acceptance: 4, 8
- Files: loom-code/hooks/agy_adapter.py, loom-code/scripts/loom_checker/command_handlers/push.py, loom-code/scripts/test_loom_publish.py, loom-code/scripts/test_agy_adapter.py
- Test: A4 positive: attestation-reason-docstring-names-checked-head; boundary: case-folded-publishers-blocked-on-every-host. A8 positive: allow-set-parity-still-passes-after-split; negative: blocked-matrix-baseline-named.
- Risk: user-decided — keep case-insensitive publisher detection on every host; agent-decided — split `_closed_read_only` under 50 lines, name the matrix baseline commit, document that the reason reflects checked-out HEAD.

## Questions asked
① — what — 在 Antigravity 裡你希望做到多「能用」？（答：整條流程能走完）
① — what — 三個 plugin 都要支援 Antigravity 嗎？（答：三個都要）
① — what — 這次是給誰用？（答：也要讓別人能裝）
① — consequence — review 在 agy 撞名：只改 Antigravity 版（A）或三邊都保留 review（B）？（答：改為三邊都改名）
① — what — 提案 loom 專屬的審查站名字（答：closing-review）
① — consequence — 覆述 intent，含：舊名不留轉接、agy 上審查由 Gemini 執行、clone 後逐一安裝、原則加入 Antigravity、審查通過後自動 push 並開 PR（答：對）
① — what — 第 3 條驗收寫著「loom 的檢查程式接受盲跑報告」，但 loom 目前沒有任何規則在檢查盲跑報告，所以這半句永遠證明不了。你要怎麼處理？（答：改驗收說法）
① — consequence — 被 push 閘門擋下時，一般人打的 `git push` 看到的第一個理由是「指令必須用標準全引號寫法」，看不出真正缺的是審查紀錄。要改嗎？（這個訊息三個平台共用，擋不擋的判斷不會變，只改看到的文字）（答：改，三平台都先說缺審查）
① — consequence — 審查發現：第一輪對抗測試後，我們讓 push 閘門「不分大小寫」辨認 `git`／`gh`，所以現在 `GIT push`、`Gh pr create` 這類寫法在 Claude Code 和 Codex 上也會被擋（以前會放行）。這違反了你先前定的「哪些 push 會被擋不變」。在 macOS 上檔名不分大小寫，`GIT push` 其實真的會推送成功，所以舊行為是個漏洞。要怎麼處理？（答：保留，三平台都擋）

## Risks
1. user-decided — review station renamed closing-review on all hosts with no alias, because agy de-duplicates skills by short name and an alias would collide again.
2. Hooks fire only in the agy CLI; Antigravity desktop and IDE are out of scope, so gates there are unenforced and the README must say so.
3. Path resolution relies on the model deriving the plugin root; spike samples were small, so the blind run on agy exercises every station's checker command.
4. agy 1.2.2 behaviour (hook payloads, skill de-duplication) is undocumented and may change; adapters parse defensively and fail closed on the push gate.
