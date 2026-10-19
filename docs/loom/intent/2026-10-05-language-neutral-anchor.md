# 語言提醒不再由程式判斷語言
originator: kouko
kind: engineering
needs-design: no — an existing hook's reminder text and its language-detection step; no new field, rule id, command, decision point or file artifact
evidence: [loom-code/hooks/language-anchor.py, loom-code/hooks/lang_detect.py, loom-code/hooks/agy_adapter.py, loom-code/opencode/loader.js]
status: confirmed 2026-10-05
publication: automatic — authorized 2026-10-05 by kouko

## Problem
自動語言提醒要先由程式數字元判斷使用者的語言，才決定送不送、用哪種語言寫。這個判斷把每個英文字母算一票，使用者用中文夾很多英文術語時常被判成英文，提醒就不出現；2026-10-04 實測的 51 段壓縮過的真實對話中有 4 段整段沒有提醒，acceptance testing 也碰到一次。中文、日文以外的語言完全沒有提醒。

| 現況 | 後果 |
|---|---|
| 中文夾英文術語被判成英文 | 最需要提醒的輪次反而沒有提醒 |
| 只認得中文與日文 | 韓文、俄文、法文等使用者沒有提醒 |

## Proposed outcome
自動語言提醒不再判斷使用者用什麼語言：每次觸發都送出同一句不指定語言的提醒，要求用使用者在對話中所用的語言與文字回覆，由回覆的 model 自己從對話認出語言。

## Acceptance
1. 中文夾大量英文術語的對話，在每個既有觸發時機都會收到語言提醒。
2. 任何語言的對話（含英文、韓文、法文）都會收到同一句提醒；提醒不指定、也不偏向任何一種語言或字體。
3. 實際用繁體中文、簡體中文、日文、韓文各開一段對話，在背景 agent 做完的那一輪，回覆維持該對話的語言與字體。
4. 目前顯示語言提醒的每個工具（Claude Code、Antigravity、OpenCode）都改送同一句提醒。
5. 既有的語言分工與各站說明不變。
6. 完整 package suite 全部通過，版號一致。

## Constraints
- 沿用既有提醒與既有觸發時機，不新增時機、checker 規則、欄位或決策點。
- 不另外呼叫 model 判斷語言。
- 提醒那一句用英文寫（使用者決定），不寫成中文或中英並列。
- 對話用使用者的語言；plan、spec、verdict、commit 等 loom 機器面 artifacts 用英文。

## Out of scope
- 新增觸發時機或替 Codex 加上語言提醒。
- 使用者全域的 CLAUDE.md 與 loom-workflow 每輪提醒卡。
- 各站說明文字的語言規定。

## Open questions
- none
