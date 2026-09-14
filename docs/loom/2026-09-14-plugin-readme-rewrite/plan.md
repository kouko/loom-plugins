# Plugin README rewrite — plan
intent: 2026-09-14-plugin-readme-rewrite@d8207795
charter: 1.0

## Current State Evidence
- Forward: `loom-*/README{,.ja,.zh-TW}.md` — nine READMEs, no Mermaid block, 4-8 `monkey-skills` mentions each, including install commands.
- Reverse: `.claude-plugin/marketplace.json` — marketplace `"name": "loom"`; root `README.md` "## Install" already targets `kouko/loom-plugins`.
- Error: `loom-code/scripts/test_sync_codex_manifest.py:59-67` — pins `independently installable`, `plugin-qualified skill names`, `docs/loom/`, `N/A with the reason` in loom-code README.md.
- Data: `loom-workflow/scripts/test_independent_advisor_plugin_readmes.py:37-46` — each loom-workflow README keeps the `independent-advisor` table row and `│   ├── independent-advisor/` tree line.
- Boundary: `loom-workflow/skills/goal-create/scripts/test_readmes.py:45-49,93-96` — goal-create row keeps localized accepted/recovery tokens; loom-design READMEs are unpinned.

## Task DAG

### Wave 1

**W1-01 Rewrite loom-design READMEs**  after: none  acceptance: 1, 2, 3, 4, 5
- Files: loom-design/README.md, loom-design/README.ja.md, loom-design/README.zh-TW.md
- Test: A1 positive: design-skills-match-dir; negative: design-version-mismatch. A2 positive: design-mermaid-parses; negative: design-mermaid-missing. A3 positive: design-lang-structure-equal; negative: design-lang-fact-drift. A4 positive: design-install-loom; negative: design-install-monkey. A5 positive: suite-green; negative: design-pin-broken.
- Risk: agent-decided — station diagram capture-intent → write-spec → loom-code handoff, tools shown as on-demand; no README pins exist, so rely on reviewer fact checks.

**W1-02 Rewrite loom-code READMEs**  after: none  acceptance: 1, 2, 3, 4, 5
- Files: loom-code/README.md, loom-code/README.ja.md, loom-code/README.zh-TW.md
- Test: A1 positive: code-skills-match-dir; negative: code-version-mismatch. A2 positive: code-mermaid-parses; negative: code-mermaid-missing. A3 positive: code-lang-structure-equal; negative: code-lang-fact-drift. A4 positive: code-install-loom; negative: code-install-monkey. A5 positive: suite-green; negative: code-four-phrases-missing.
- Risk: agent-decided — station diagram with ①②③ and maintain → write-plan; keep the four pinned English phrases verbatim.

**W1-03 Rewrite loom-workflow READMEs**  after: none  acceptance: 1, 2, 3, 4, 5
- Files: loom-workflow/README.md, loom-workflow/README.ja.md, loom-workflow/README.zh-TW.md
- Test: A1 positive: workflow-skills-match-dir; negative: workflow-version-mismatch. A2 positive: workflow-mermaid-parses; negative: workflow-mermaid-missing. A3 positive: workflow-lang-structure-equal; negative: workflow-lang-fact-drift. A4 positive: workflow-install-loom; negative: workflow-install-monkey. A5 positive: suite-green; negative: workflow-pinned-rows-missing.
- Risk: agent-decided — timing-grouped diagram, not a sequential flow; keep independent-advisor row and tree line plus goal-create localized tokens.

## Questions asked
① — what — 三種語言的 README 都要改嗎？（答：三種語言都改）
① — what — 每份 README 要改到什麼程度？（答：整份重寫）
① — what — 安裝指令和 repo 連結要從 monkey-skills 改成這個 repo（loom-plugins）嗎？（答：改成 loom-plugins）
① — what — 你要把三個 plugin 各自的 README 整份重寫（三種語言、Mermaid 流程圖、安裝指向 loom、測試全過），流程圖畫法如表，並授權自動 push 開 PR、檢查綠了合併；這樣對嗎？

## Risks
1. Three language versions can drift; each task writes English first, then translates facts and diagram structure, and reviewers compare the trio.
2. Mermaid labels in Japanese and Chinese may wrap poorly; each task renders all three diagrams locally before commit.
