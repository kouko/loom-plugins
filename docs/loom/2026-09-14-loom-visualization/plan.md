# Add a loom-visualization skill for coding-harness conversations — plan
intent: 2026-09-14-loom-visualization@c1b76092
spec: docs/loom/2026-09-14-loom-visualization/spec.md@ab7ffe0a
charter: 1.0

## Task DAG
<!-- When a spec requirement changes after this commit, the un-landed
     tasks it touches are replaced and the reason is named in the commit
     message. Landed tasks stay as they are. -->

### Wave 1 — independent engines

**W1-01 Port the stdlib ASCII engine**  after: none  acceptance: 4
- Files: `loom-workflow/skills/loom-visualization/scripts/{width,glyphs,align,generate}.py`, `loom-workflow/skills/loom-visualization/scripts/checks_{seam,table,kink}.py`, `loom-workflow/skills/loom-visualization/scripts/gen_{table,flow,tree,bar,arch,seq}.py`, `loom-workflow/skills/loom-visualization/scripts/test_ascii_{width,generators,checks,cli}.py`
- Test: A4 positive: cjk-labelled-flow-passes-checks-under-python-I; boundary: control-and-combining-chars-width-zero.
- Risk: stdlib width diverges from wcwidth on symbols; tests pin CJK, kana, punctuation and box glyphs per spec REQ-4 decision. agent-decided.

**W1-02 Client check and capability matrix**  after: none  acceptance: 3, 7
- Files: `loom-workflow/skills/loom-visualization/scripts/detect_client.py`, `loom-workflow/skills/loom-visualization/scripts/test_detect_client.py`, `loom-workflow/skills/loom-visualization/references/client-matrix.md`
- Test: A3 positive: claude-code-cli-env-mermaid-false; negative: unrecognised-env-falls-back-table-ascii. A7 positive: target-under-dot-obsidian-reports-vault; negative: plain-repo-path-not-vault.
- Risk: env markers drift between host versions; matrix carries sources and verified date, unknown stays conservative per spec REQ-3 decision. agent-decided.

**W1-03 Move page mode onto a stdlib renderer**  after: none  acceptance: 6
- Files: `loom-workflow/skills/loom-visualization/scripts/{render_cot_html,verify_cot_html}.py`, `loom-workflow/skills/loom-visualization/references/{mermaid-cot-spec,fidelity-check}.md`, `loom-workflow/skills/loom-visualization/assets/cot-report-template.md`, `loom-workflow/tests/test_loom_visualization_page_scripts.py`, `scripts/run_package_tests.py`, `scripts/test_run_package_tests.py`, `.github/workflows/loom-workflow-ci.yml`
- Test: A6 positive: template-report-renders-standalone-page-with-loom-visualization-stamp; negative: leftover-markdown-in-output-fails-verify.
- Risk: stdlib renderer may miss a CommonMark construct the template uses; renamed existing tests are the oracle per spec REQ-6 decision. agent-decided.

### Wave 2 — skill surface

**W2-01 Templates, SKILL.md and boundary tests**  after: W1-01, W1-02, W1-03  acceptance: 2, 7
- Files: `loom-workflow/skills/loom-visualization/SKILL.md`, `loom-workflow/skills/loom-visualization/templates/*.md`, `loom-workflow/skills/loom-visualization/NOTICE.md`, `loom-workflow/skills/loom-visualization/scripts/test_templates.py`, `loom-workflow/scripts/test_loom_visualization_compaction.py`
- Test: A2 positive: eleven-shapes-each-have-table-ascii-mermaid; negative: template-missing-mermaid-section-fails. A7 positive: skill-declines-vault-target; negative: template-with-wikilink-fails.
- Risk: SKILL.md may exceed token cap after absorbing page mode; long procedure moves to references per spec folder-shape decision. agent-decided.

**W2-02 Mermaid validator project and CI job**  after: W2-01  acceptance: 5
- Files: `loom-workflow/tests/mermaid/package.json`, `loom-workflow/tests/mermaid/package-lock.json`, `loom-workflow/tests/mermaid/validate_mermaid.mjs`, `scripts/run_package_tests.py`, `scripts/test_run_package_tests.py`, `.gitignore`, `.github/workflows/loom-workflow-ci.yml`
- Test: A5 positive: all-template-blocks-parse; negative: known-bad-arrow-block-rejected.
- Risk: npm install needs network; lockfile pins versions and the separate workflow-mermaid group has no skip path per spec REQ-5 decision. agent-decided.

**W2-03 Rename wiring in contract, counts and catalog**  after: W2-01  acceptance: 1
- Files: `loom-code/contract/manifest.yaml`, `docs/loom/evidence/mechanisms.yaml`, `loom-workflow/scripts/test_skill_count.py`, `scripts/test_loom_skill_description_catalog.py`, `loom-workflow/skills/using-loom-workflow/SKILL.md`, `loom-workflow/scripts/test_cot_explain_compaction.py`, `loom-workflow/skills/cot-explain/`
- Test: A1 positive: skill-sets-and-manifest-name-loom-visualization; negative: leftover-cot-explain-reference-grep-fails.
- Risk: hash-pinned description baseline; a rename map keeps the historical record intact per spec REQ-1 decision. agent-decided.

**W2-04 Manifests, READMEs and CHANGELOG 5.0.0**  after: W2-03  acceptance: 1
- Files: `loom-workflow/.claude-plugin/plugin.json`, `loom-workflow/.codex-plugin/plugin.json`, `README.md`, `loom-workflow/README.md`, `loom-workflow/README.ja.md`, `loom-workflow/README.zh-TW.md`, `loom-workflow/CHANGELOG.md`
- Test: A1 positive: codex-manifest-sync-check-passes-at-5-0-0; negative: claude-codex-version-mismatch-fails.
- Risk: Codex manifest drift; regenerate with the sync script rather than hand-editing, per spec REQ-1 decision. agent-decided.

**W2-05 SessionStart trigger cards**  after: W2-01  acceptance: 8, 9
- Files: `loom-workflow/hooks/hooks.json`, `loom-workflow/hooks/visualization-card`, `loom-workflow/skills/loom-visualization/assets/trigger-card.md`, `loom-workflow/skills/loom-visualization/assets/trigger-card-coexist.md`, `loom-workflow/scripts/test_visualization_card_hook.py`, `loom-workflow/scripts/fixtures_ascii_graph_trigger_card.md`
- Test: A8 positive: comparison-prompt-stream-shows-skill-call-and-table; negative: trivial-control-no-skill-call-no-diagram. A9 positive: enabled-toolkit-prints-coexist-card; boundary: disabled-or-other-project-prints-full-card.
- Risk: plugin activity misread yields two or zero cards; unreadable state prints the full card per spec trigger-card decision. agent-decided.

### Wave 3 — mechanism accounting

**W3-01 Register loom-workflow hooks and loom-visualization gates as mechanisms**  after: W2-01, W2-05  acceptance: 10
- Files: `loom-code/scripts/check_mechanisms.py`, `loom-code/scripts/test_check_mechanisms.py`, `docs/loom/evidence/mechanisms.yaml`, `loom-workflow/scripts/test_validate_skill_folder_structure_hook.py`, `loom-code/CHANGELOG.md`, `loom-code/.claude-plugin/plugin.json`, `loom-code/.codex-plugin/plugin.json`
- Test: A10 positive: package-suite-and-check-mechanisms-green; negative: unregistered-workflow-hook-is-red.
- Risk: net count rises by two hooks plus W2-01's two prose gates; loom-code minor bump carries four budget-exception lines. agent-decided.

## Questions asked
① — what — 你要的是：在 loom-workflow 裡新增一個 loom-visualization skill，專門處理 coding harness 對話裡的視覺化呈現，並把 cot-explain 併進來（覆述 10 條驗收與不做的範圍）。對嗎？
① — consequence — 移除 cot-explain 名稱：直接移除（建議），或保留舊名轉址一段時間？
① — consequence — 回答「對」也代表授權自動發布：review 與發布檢查通過後自動 push 並開 Ready PR，merge 仍需你另外決定。

## Risks
1. user-decided — `cot-explain` removed without alias; recorded as a breaking change (intent Constraints).
2. The ported ASCII engine becomes a second copy of ascii-graph-toolkit; each file header records source commit e5b978e0 so later divergence is traceable.
3. Acceptance 8 is behavioural and model-dependent; the fixed seven-prompt protocol with a control keeps the blind run decidable.
4. Removing the markdown-it-py CI pin could hide another consumer; W1-03 checks the repository for remaining imports before dropping it.
5. user-decided — 2026-09-14 kouko authorized merging origin/main into this branch to resolve README conflicts and re-confirmed the intent, starting a new review episode scoped to that resolution.
