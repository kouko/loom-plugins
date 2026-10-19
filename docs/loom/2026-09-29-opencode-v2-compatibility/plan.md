# Make the loom plugins installable and usable under OpenCode v2 — plan
intent: 2026-09-29-opencode-v2-compatibility@64aa3fcd
spec: docs/loom/2026-09-29-opencode-v2-compatibility/spec.md
charter: 1.1

## Task DAG

### Wave 1

**W1-01 OpenCode packaging and shared loader for skills and agents**  after: —  acceptance: 1, 2, 4, 6
- Files: scripts/opencode/loader.js, scripts/sync_codex_manifests.py, loom-*/package.json, loom-*/index.js, loom-*/opencode/loader.js, tests/test_sync_codex_manifests.py, loom-code/tests/test_opencode_loader.py, .github/workflows/loom-code-ci.yml
- Test: A1 positive: package-json-derived-per-plugin; negative: drifted-loader-copy-fails-check. A2 positive: skills-registered-plugin-qualified; boundary: disable-model-invocation-skill-not-model-registered. A4 positive: agents-registered-plugin-qualified; negative: plugin-without-agents-registers-none. A6 positive: root-manifest-keys-unchanged; negative: sync-check-all-clean.
- Risk: agent-decided per spec REQ-1/2/4 decisions; test_sync_codex_manifests.py coverage widened, not narrowed; node required in CI.

**W1-02 OpenCode tool and agent mapping reference**  after: —  acceptance: 3, 4
- Files: loom-code/references/opencode-tools.md, loom-code/skills/write-plan/SKILL.md, loom-code/skills/build/SKILL.md, loom-code/skills/closing-review/SKILL.md, loom-code/tests/test_agy_tool_mapping.py
- Test: A3 positive: stations-link-opencode-reference; negative: write-plan-within-word-cap. A4 positive: reference-maps-subagent-agent-ids; negative: no-subagent-type-on-opencode.
- Risk: agent-decided per spec REQ-3/4; write-plan at 3750-word cap, extend the existing Antigravity line rather than adding one.

### Wave 2

**W2-01 Loader hook translation and loom-code OpenCode hooks**  after: W1-01  acceptance: 5
- Files: scripts/opencode/loader.js, loom-*/opencode/loader.js, loom-code/hooks/hooks-opencode.json, loom-workflow/hooks/hooks-opencode.json, loom-code/scripts/loom_checker/rule_checks/selection_guard.py, loom-code/tests/test_opencode_loader.py, loom-code/tests/test_selection_guard.py
- Test: A5 positive: shell-push-routed-to-push-hook; negative: subagent-prompt-entry-token-records-nothing; boundary: nested-opencode-run-refused; positive: nested-skill-folder-write-noted.
- Risk: agent-decided per spec REQ-5 event and tool tables; card root-session only; test_selection_guard.py coverage widened by one host program.

### Wave 3

**W3-01 Live OpenCode checks**  after: W2-01, W1-02  acceptance: 1, 5
- Files: docs/loom/2026-09-29-opencode-v2-compatibility/evidence/opencode-live-checks.md
- Test: A1 positive: git-file-install-lists-three-plugins; negative: none-installed-before-add. A5 positive: execute-tool-hook-result-recorded; boundary: expert-mode-command-text-reaches-prompt-hook.
- Risk: agent-decided per spec REQ-1/5: isolated XDG config only, never the user's; results decide W4-01 disclosures.

### Wave 4

**W4-01 Install docs and host principles**  after: W3-01  acceptance: 1, 7
- Files: README.md, loom-*/README.md, loom-*/README.ja.md, loom-*/README.zh-TW.md, PRINCIPLES.md, AGENTS.md, tests/test_agy_install_docs.py
- Test: A1 positive: every-readme-has-opencode-install-section; negative: install-spec-names-each-plugin. A7 positive: principles-name-opencode; boundary: principles-count-unchanged.
- Risk: agent-decided per spec REQ-5/7: disclosures follow W3-01 evidence, checked by review, not a test; reuse test_agy_install_docs.py helpers; PRINCIPLES amendment carries the ratified-by entry under intent Acceptance #7.

**W4-02 Mechanism census and release bump**  after: W4-01  acceptance: 5, 8
- Files: loom-code/scripts/check_mechanisms.py, docs/loom/evidence/mechanisms.yaml, loom-*/**/plugin.json, loom-*/package.json, loom-*/CHANGELOG.md, .claude-plugin/marketplace.json, *README*.md, loom-code/tests/test_*.py
- Test: A5 positive: opencode-hooks-counted-with-qualifier; negative: missing-budget-exception-blocks. A8 positive: current-release-metadata-synchronized; negative: pin-test-red-before-rewrite.
- Risk: agent-decided per spec: loom-code 3.24.0, loom-design 2.7.1, loom-workflow 5.5.6; budget-exception agent-decided under Acceptance #5.

## Simplicity check
- Replace new test_opencode_install_docs.py with two cases in test_agy_install_docs.py; drop duplicate ratified-by and live-result-dependent docs cases — taken
- Merge W2-02 (loom-workflow hook table) into W2-01 — taken
- Drop dispatch-profile.md edit; the generic non-Claude wording already covers OpenCode — taken
- Mapping reference needs no loader, moved to Wave 1 as W1-02 — taken

## Questions asked
① — what — 這次要讓三個 plugin 都能在 OpenCode 用，還是先只做 loom-code？／期望能做到什麼程度？／平常用哪個介面與 model？／希望怎麼安裝？／有沒有明確不做的？ → 「全部都要能在 opencode 用」「要能跟 claude code / codex / antigravity 一樣可以跑整個 loom 流程」「目前只用 CLI/TUI , 用 litellm 跑第三方雲端模型」「要能用 openCode v2 官方的指令 & 內建 TUI 介面 指定 repo 與 plugin 安裝」「暫時不追加特別針對 opencode 的新功能 先讓既有功能能正常運作」
① — consequence — hook 行為在 OpenCode v2 做不到時：A 列為不可用、流程照常出貨；B 五項全到才算完成 → 「對，選 A」
① — what — 覆述 intent（含自動發布授權） → 「對」

## Risks
1. A real `github:` fetch needs the change on GitHub; acceptance testing before Ship installs from a local `git+file` spec with the same `::path:` form, and the GitHub fetch is tried on the PR branch after publication, before decision point ③.
2. The TUI plugin dialog is interactive; the acceptance tester drives it through a terminal multiplexer, and states plainly if it could not.
3. Acceptance #3 needs a full loom run on a third-party model through litellm, which costs model usage and depends on that model following long skill prose.
4. user-decided — hook behaviours OpenCode v2 cannot provide are disclosed in the install instructions and the flow still ships (option A).
