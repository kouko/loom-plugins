# Root README public overview — plan
intent: 2026-09-14-root-readme-overview@39496355
charter: 1.0

## Current State Evidence
- Forward: `README.md` — "# Loom" plugin table is the only overview; no flow diagram exists at the root.
- Reverse: `.claude-plugin/marketplace.json` — marketplace `"name": "loom"` lists the three plugin roots that install instructions must target.
- Error: `README.md` — "The extraction does not configure a publishing remote" becomes false once the repository is published.
- Data: `loom-*/.claude-plugin/plugin.json` — `version` fields are the source for the plugin table.
- Boundary: `loom-code/README.md` "## Install" — plugin-level install URLs name monkey-skills and stay unchanged.

## Task DAG

### Wave 1

**W1-01 Rewrite root README**  after: none  acceptance: 1, 2, 3, 4
- Files: README.md
- Test: A1 positive: readme-names-three-plugins; negative: readme-version-mismatch. A2 positive: mermaid-block-parses; boundary: mermaid-shows-three-decision-points. A3 positive: install-targets-loom-marketplace; negative: install-names-monkey-skills. A4 positive: dev-and-provenance-kept; negative: unpublished-claim-absent.
- Risk: agent-decided — English only, mirroring existing root README; plugin READMEs untouched per Constraints; Mermaid kept to GitHub-supported flowchart syntax.

## Questions asked
① — what — 你要把 repo 首頁的 README 重寫成給第一次來的人看的入口（三個 plugin 說明、Mermaid 流程圖、可從此 repo 安裝、保留開發與來源說明）；回答「對」即授權審查通過後自動 push 並開 PR。對嗎？
① — consequence — 公開後完整 git 歷史（含從 monkey-skills 帶來的歷史與證據標籤）所有人可見，改回私人也收不回 fork 與快取；建議 README 合併後最後一步再公開。

## Risks
1. Mermaid syntax GitHub cannot render would silently show a code block; verify by parsing with a Mermaid CLI when available, else a strict syntax read.
