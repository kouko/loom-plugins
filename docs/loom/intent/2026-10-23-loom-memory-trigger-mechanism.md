# agent 存自己的記憶時，同時判斷這筆是不是 repo 的教訓並寫進 repo
originator: kouko
kind: engineering
needs-design: no — 調整 loom-memory 的觸發說明與分類規則，並把既有的記憶提醒 hook 移進 loom-workflow；沒有新的使用者介面、欄位或多狀態行為
status: confirmed 2026-10-24
publication: automatic — authorized 2026-10-24 by kouko

## Problem
repo 的長期教訓幾乎不再寫進 `docs/loom/memory/`：2026-07～08 每月約 70 筆，2026-10 至今 1 筆。同一段時間，agent 內建的記憶（Claude Code auto-memory，存在使用者本機）照常在存：本 repo 本機就有約 25 筆，其中至少 5 筆是任何人跑這個 repo 都會遇到的教訓（FORCE_COLOR 讓巢狀 pytest 解析失敗、sync-trunk 衝突的處理方式、CLAUDE_CODE_SESSION_ID 漏進巢狀 pytest 等），在 repo 的記憶庫裡一筆都找不到。這些知識只留在一台機器上，其他貢獻者、其他機器、其他 agent 都看不到。

現況的原因：

| 現況 | 位置 | 效果 |
|---|---|---|
| loom-memory 的 description 只寫「被要求時記錄」與「需要時回想」 | `loom-workflow/skills/loom-memory/SKILL.md` frontmatter | agent 自己判斷值得記的時候不會打開它 |
| loom-memory 本文規定「只有兩種被動觸發，走到流程某一步不算理由」（#821 為了讓 loom-memory 可選裝而寫，不是為了減少記錄） | 同檔〈When this skill activates〉 | Ship §2 的路由句被它否定 |
| 內建記憶寫入時提醒同步的 hook 還在 repo，但沒有任何設定接上它；當初也只對 `type: project` 的筆記提醒，而 repo 教訓多半存成 `type: feedback` | `.claude/hooks/remind-memory-mirror.sh`、`tests/hooks/test_remind_memory_mirror.py` | 孤兒檔案；就算接上也抓不到大多數 repo 教訓 |
| 分類規則只排除「個人偏好」，沒有排除「只在某台機器或某個工具上成立」的事 | Record 步驟 1 | 即使觸發，也沒有清楚標準區分 repo 與個人／全域記憶 |

## Proposed outcome
agent 準備把一筆教訓存進自己的內建記憶時，也會用 loom-memory 判斷這筆是不是屬於這個 repo：換一個人、換一台機器、換一套工具 clone 這個 repo 仍然成立且有用的，寫進 repo 的記憶庫；只跟使用者本人、本機或某個 agent 工具有關的，留在內建記憶，不寫進 repo。這個觸發同時寫在 loom-memory 的 description（所有平台都看得到），並由 loom-workflow plugin 內的 hook 在 Claude Code 寫入內建記憶時一定提醒一次，不論筆記類型。

## Acceptance
1. 在乾淨環境、裝了 loom-workflow 的 Claude Code session 裡，agent 把一條「任何人跑這個 repo 都會遇到」的教訓存進內建記憶後，同一個 session 內 `docs/loom/memory/` 多出對應的教訓檔，`index.md` 已重建且 `validate` 通過。
2. 同樣的環境裡，agent 存一條使用者個人偏好、和一條只在使用者本機成立的事（例如本機某個指令指向特定環境），兩者都不會在 `docs/loom/memory/` 產生或修改任何檔案。
3. 裝了 loom-workflow 的 Claude Code 中，寫入內建記憶資料夾內任何筆記（不論 `type` 為何）都會出現一次提醒；寫入其他路徑、或 hook 收到格式異常的資料時，不出現提醒也不會讓 session 出錯。
4. 在沒有這類 hook 事件的平台（例如 Codex 的檔案編輯），不出現錯誤，行為與現在相同；loom-memory 的 description 仍描述這個觸發時機。
5. loom-memory 的規則文字與各 station 的規則文字裡，沒有任何一句話否定這個觸發；沒裝 loom-workflow 時，loom-code 的各站照常運作。
6. 在 finalize-review 產生審查證明之後才發現的 repo 教訓，不會在同一個 branch 寫進 `docs/loom/memory/`（#109 的規則照舊），它留在內建記憶裡。
7. repo 內原本那支沒接上的 hook 與它的測試已移除，repo 裡沒有檔案再引用它。
8. 套件測試（package suite）全部通過。

## Constraints
- 不能靠使用者每次手動提醒。
- hook 放在 loom-workflow plugin 內，使用 loom-workflow 的每個 repo 都會生效（user-decided 2026-10-24）。
- hook 只提醒、不自己寫教訓；寫不寫、寫什麼由 agent 依 loom-memory 的分類判斷（#821 的原則：hook 可以提醒或驗證，不能自行產生教訓）。
- loom-code 不得因此依賴 loom-workflow；沒裝 loom-workflow 時 loom-code 照常運作。
- finalize-review 之後不寫 memory 的規則（#109）不變。
- 「每次變更零到一條教訓是正常結果」的篩選標準不放寬。
- commit／PR 的 `Decision:`／`Learning:`／`Gotcha:` trailer 屬於 git-memory，本變更不改 git-memory 的規則。
- 執行期規則文字不得引用本 repo `docs/` 下的開發紀錄（Contract Citations 規則）。

## Out of scope
- 在 loom 流程站加固定的記憶檢查點。
- 把使用者本機既有的內建記憶回頭搬進 repo。
- 修改 agent 內建記憶本身的行為（例如阻止它存 repo 教訓）。
- 讓 Codex／OpenCode 的檔案編輯送出 hook 事件。
- 把 `docs/loom/memory/**` 排除在審查證明的內容摘要之外。

## Open questions
- none
