# loom 轉述結果時用使用者對話的語言
originator: kouko
kind: engineering
needs-design: no — guidance text and an existing hook's triggers and wording; no new field, rule id, command, decision point or file artifact
evidence: [loom-code/skills/build/SKILL.md, loom-code/skills/closing-review/SKILL.md, loom-code/skills/ship/SKILL.md, loom-code/hooks/language-anchor.py, loom-code/hooks/hooks.json]
status: confirmed 2026-10-04
publication: automatic — authorized 2026-10-04 by kouko

## Problem
使用者用中文跟 loom 對話，loom 卻常常直接用英文回覆，特別是在背景 agent 做完、或對話壓縮後接續的那幾輪。2026-10-04 這一天，兩次決策點 ③ 的驗收訊息（PR #78、#79）第一次送出時都是英文，這次變更的決策點 ① 也一樣，使用者得另外要求才拿到中文。

| 現況 | 缺口 |
|---|---|
| 各站說明 | build 與 closing-review 完全沒寫回覆語言；ship 只規定 PR body 的語言 |
| 既有的自動語言提醒 | 只在載入 skill 之後出現；壓縮後接續、subagent 結果回來時都沒有 |
| 提醒的內容 | 偵測到中文時寫死「繁體中文」，用簡體中文對話的使用者會被要求改用繁體；中文、日文以外的語言沒有提醒 |

## Proposed outcome
loom 給使用者的每則訊息都用使用者對話使用的語言，包括轉述 reviewer、acceptance tester、adversary、implementer 的結果，以及 ③ 的驗收訊息；不是使用者傳訊息開始的那一輪也一樣。自動語言提醒在更多時機出現，而且只要求「使用者對話使用的語言」，不寫死任何一種語言。

## Acceptance
1. build 與 closing-review 說明：把 agent 的結果轉述給使用者時用使用者對話使用的語言，包括沒有使用者新訊息、由背景 agent 完成或對話接續開始的那一輪。
2. ship 說明：PR body 以及給使用者的每則訊息（含決策點 ③ 的結果與驗收問題）用使用者對話使用的語言。
3. 自動語言提醒除了載入 skill 之後，也在對話壓縮後接續時、以及 subagent 結果回來時出現；Claude Code 沒有可用觸發時機的情況，acceptance test report 寫明哪些時機沒有涵蓋。
4. 自動語言提醒要求的是使用者對話使用的語言，不寫死任何一種語言；用簡體中文對話時，提醒不會要求改用繁體中文。
5. 既有的語言分工不變：plan、spec、verdict、evidence、commit 仍是英文；acceptance test report 與 PR body 仍用使用者的語言。
6. 完整 package suite 全部通過，版號一致。

## Constraints
- 沿用既有的自動語言提醒，不新增另一套提醒機制；不新增 checker 規則、欄位或決策點。
- subagent 的機器面輸出（verdict、evidence）維持英文，不改它們的輸出契約。
- 對話用使用者的語言；plan、spec、verdict、commit body 等 loom 機器面 artifacts 用英文。

## Out of scope
- write-spec、maintain 等其他站的說明。
- 使用者全域的 CLAUDE.md。
- loom-workflow 每輪附加的提醒卡。

## Open questions
- none
