# Root README public overview — plan
intent: 2026-09-14-root-readme-overview@90c77745
charter: 1.0

## Current State Evidence
- Forward: `README.md` — "# Loom" plugin table is the only overview; no flow diagram exists at the root.
- Reverse: `.claude-plugin/marketplace.json` — marketplace `"name": "loom"` lists the three plugin roots that install instructions must target.
- Error: `README.md` — "The extraction does not configure a publishing remote" becomes false once the repository is published.
- Data: `loom-*/.claude-plugin/plugin.json` — `version` fields are the source for the plugin table.
- Boundary: `loom-code/README.md` "## Install" — plugin-level install URLs name monkey-skills and stay unchanged.

## Task DAG

### Wave 1

**W1-01 Rewrite root README**  after: none  acceptance: 1, 2, 3, 4, 5, 6
- Files: README.md
- Test: A1 positive: readme-names-three-plugins; negative: readme-version-mismatch. A2 positive: mermaid-block-parses; boundary: mermaid-shows-three-decision-points. A3 positive: install-targets-loom-marketplace; negative: install-names-monkey-skills. A4 positive: dev-and-provenance-kept; negative: unpublished-claim-absent. A5 positive: every-node-names-a-skill; boundary: loom-workflow-nodes-only-in-dm. A6 positive: workflow-subsection-names-tools; negative: loom-memory-row-not-review-convergence.
- Risk: agent-decided — English only, mirroring existing root README; plugin READMEs untouched per Constraints; Mermaid kept to GitHub-supported flowchart syntax.

### Wave 2

**W2-01 Keep root README row test-compatible**  after: W1-01  acceptance: 7
- Files: README.md
- Test: A7 positive: package-suite-passes; negative: workflow-row-omits-independent-advisor.
- Risk: agent-decided — fix the README row, never the test; the existing test pins `independent-advisor` in the root loom-workflow row.

## Questions asked
① — what — 你要把 repo 首頁的 README 重寫成給第一次來的人看的入口（三個 plugin 說明、Mermaid 流程圖、可從此 repo 安裝、保留開發與來源說明）；回答「對」即授權審查通過後自動 push 並開 PR。對嗎？
① — consequence — 公開後完整 git 歷史（含從 monkey-skills 帶來的歷史與證據標籤）所有人可見，改回私人也收不回 fork 與快取；建議 README 合併後最後一步再公開。

① — what — 照這個方式改嗎（主流程圖＋loom-workflow 對照表）？
① — what — 你比較想要哪一種？簡化版圖＋兩三句補充／第四版詳細圖／不畫圖只用三句話說明
① — what — 這樣可以就回我「可以」（合併 decision-map 進主流程圖並修正兩個小問題）
① — what — 需求新增三條驗收條件（節點標 skill 與 decision-map 入口、支援工具說明、套件測試通過）並授權審查通過後自動 push 開 PR；這樣對嗎？

## Risks
1. Mermaid syntax GitHub cannot render would silently show a code block; verify by parsing with a Mermaid CLI when available, else a strict syntax read.
