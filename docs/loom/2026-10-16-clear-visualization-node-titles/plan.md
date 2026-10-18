# Independent node titles in loom-visualization — plan
intent: 2026-10-16-clear-visualization-node-titles@70ebf14
spec: docs/loom/2026-10-16-clear-visualization-node-titles/spec.md@43397ef
charter: 1.1

## Task DAG

Wave 1 — wording and representative examples

**W1-01 State and demonstrate the title rule**  after: none  acceptance: 1, 2, 3
- Files: loom-workflow/skills/loom-visualization/references/node-structure.md, loom-workflow/skills/loom-visualization/templates/{02,03,04,05,07,08}*.md
- Test: A1 positive: title-stands-alone; negative: body-restates-title. A2 positive: mixed-existing-samples; negative: duplicate-branch-label. A3 positive: examples-align-and-parse; boundary: single-line-unchanged.
- Risk: agent-decided — preserve each template's shape and existing structured-node coverage; REQ-1–3 constrain a wording-only change without generator edits.

Wave 2 — release metadata after examples settle

**W2-01 Publish synchronized minor metadata**  after: W1-01  acceptance: 3
- Files: loom-workflow/plugin.json, loom-workflow/.claude-plugin/plugin.json, loom-workflow/.codex-plugin/plugin.json, loom-workflow/CHANGELOG.md, loom-workflow/README.md, loom-workflow/README.ja.md, loom-workflow/README.zh-TW.md
- Test: A3 positive: synchronized-release-version; negative: stale-manifest-or-readme-pin.
- Risk: agent-decided — bump to 5.11.0 after the final wording fix (5.10.0 was taken on trunk by #93 before ship); guidance changes require a minor release, and metadata must precede attestation.

## Simplicity check
- Existing template tests plus independent semantic review instead of new wording-pin tests — taken

## Questions asked
① — what — 你要的是：讓節點的短標題單獨就能說明功能或行為，內文只補充新資訊；精準修改工程與流程範例，並補一個可驗證對齊的簡單 ASCII UI 線框圖範例。做完後，你能從指引判斷何時用單行標題、何時加內文，以及何時用 ASCII 畫位置、用 Mermaid 畫流程。這是你要的範圍嗎？
① — what — 修正後的目標是：讓節點的短標題單獨就能說明功能或行為，內文只補充新資訊；精準調整現有工程規劃與流程設計範例。完成後，你能從指引判斷何時保留單行節點、何時加內文，更新的範例也會通過圖表檢查。這個範圍對嗎？
① — what — 寫清楚短標題與內文的分工，精準改善現有工程及流程範例；這次不新增複雜圖型範本，也不做 wireframe。做完後，使用者只看標題就能辨認節點的功能或行為，內文只在提供新資訊時出現，更新的圖也通過現有檢查。這個範圍對嗎？

## Risks
1. A title can be terse yet unclear; check examples semantically, not by counting words or structured nodes.
2. Keep current format and renderer behavior; the existing template tests cover structured examples, parser compatibility, and alignment.
