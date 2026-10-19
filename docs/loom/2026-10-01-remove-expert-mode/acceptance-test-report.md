# 移除 expert-mode 與輸入確認碼的跳過方式 — 我試了什麼、結果如何

2026-10-01 在專案的乾淨副本（51ca2e87）上試過。每一條怎麼試、回來什麼：`docs/loom/2026-10-01-remove-expert-mode/evidence/acceptance-test-evidence.md`。

## 你要的東西，一條一條

| # | 你要的 | 結果 | 實際情況 | 重跑 |
|---|---|---|---|---|
| 1 | expert-mode is no longer offered on Claude Code, Codex, Antigravity CLI or OpenCode, as a skill or as a command. | works | 在 Claude Code 實際輸入那個指令，回答是「這個指令不存在」，而舊版同一句話會跑出跳過表和確認碼；OpenCode 的載入程式實際跑過，指令清單裡已經沒有它；Codex 和 Antigravity CLI 無法在這裡啟動，只從它們讀取的安裝檔確認那個 skill 和相關 hook 都不在了。 | — |
| 2 | A user can still skip any of the eight steps in plain words with the same outcome as before: reviewers, package suite and adversarial skips leave the change unattested and disclosed as `absent`; the other five lose nothing. | works | 跳過 LLM reviewer、完整測試或刻意破壞測試時，變更拿不到驗證證明，PR 上顯示 `absent` 而且不擋合併；跳過 spec 和 plan 實際試過仍然放行；其餘三步本來就只靠站內說明，說明沒變。 | — |
| 3 | No loom skill, hook, checker command or rule, README, CHANGELOG-current section or standing loom doc still offers expert-mode or a typed skip confirmation code. | works | 全面搜尋之後，除了帶日期的舊變更資料夾以外，只剩「已移除」的歷史說明和測試內部的文字，沒有任何地方還在提供它或確認碼；檢查工具也已經不認得舊指令。 | — |
| 4 | Pull requests and merges of changes made after the removal show the same verification statuses as today for runs without a typed confirmation. | works | 用新舊兩版檢查工具對同樣的四段歷史各算一次，`valid`、`stale`、`absent` 三種結果完全一致；唯一的差別是「帶著確認碼跳過」的舊情況，正是這條排除的。合併本身走 GitHub，沒有實際合併，用的是同一個 PR 檢查。 | — |
| 5 | Every step skipped in plain words before Ship is recorded on the change's branch as skipped by the user's instruction, with its date, and a spec or plan skip recorded that way still waives the spec or plan. | works | 在一個練習用的 repo 裡實際試過：沒有紀錄或紀錄沒寫日期時會被擋，補上有日期的紀錄就放行，紀錄寫在 intent 或 plan 都有效；「每站跳過時寫下紀錄」是各站的指示，和改之前一樣，沒有跑完整的 agent 流程去看它真的寫下。 | — |
| 6 | When the user is asked to accept a change, the acceptance test report lists every step skipped by the user's instruction; when acceptance testing itself was skipped, the user is told the skipped steps in the conversation instead. | partly | 報告範本和規格都要求這一節，這份報告本身就照它寫了（這次沒有跳過任何步驟）；但「acceptance testing 被跳過時改在對話裡告訴你」只在站的指示裡看到，沒有實際跑一次來證明。 | — |
| 7 | The existing package test suite passes, and each plugin whose files change carries a new version consistent across manifests, CHANGELOGs and READMEs. | works | 三個有改動的 plugin 都升了版（loom-code 3.27.0、loom-design 2.9.0、loom-workflow 5.6.2），各處的版號一致，版號相關的測試都通過；完整的測試套件不在這裡跑，由驗收前會執行、失敗就擋下的自動測試套件負責。 | — |

## 對你既有的資料做了什麼

這個變更不碰你已經有的資料：舊的 expert-mode 跳過紀錄留在你電腦上原地，不會被刪除，只是之後再也沒有東西讀它。唯一的影響是，如果有哪個還沒合併的分支是用舊確認碼跳過步驟後產生驗證證明的，那份證明現在會變成 `stale`（需要重新跑 closing review）；依計畫記載，目前沒有這樣的分支。

## 我替你決定的事

- **驗證證明的格式不升版** — 保留現有格式，「跳過紀錄」欄位一律留空，填了東西就視為無效，因為這樣舊的證明不用重做。日後要改格式得另開一個變更。
- **hook 失效時的退路只保留「放行」那一句** — 檢查工具找不到時不再另外擋舊紀錄存放處，因為那個存放處已經沒有人讀。之後要再擋就得把規則加回去。
- **各站只刪掉舊指令的步驟，保留「用一般說法跳過」的規則和寫紀錄那一行** — 這樣跳過方式只剩一種，行為和以前的一般說法一樣。
- **報告新增一節「你叫我跳過的步驟」，資料直接讀分支上已提交的紀錄，不加新的檢查規則** — 比較簡單；代價是如果紀錄漏寫，沒有機器會擋下，只能靠讀報告的人發現。
- **版號：loom-code 和 loom-design 升次版號，loom-workflow 只升修補版號** — 前兩個的站內指示和檢查指令有變，後者只是同步了載入程式。
- **Codex、Antigravity CLI、OpenCode 的判斷方式（這是我做驗收時的決定）** — 這三個無法在這裡互動啟動，我改成讀它們各自載入的安裝檔，OpenCode 則直接執行它的載入程式來確認；如果你要百分之百確定，需要在那幾個工具裡實際打一次那個指令。

沒有任何嚴重度 important 以上的意見被駁回。

## 你叫我跳過的步驟

沒有 — 這次沒有跳過任何步驟。

## 我不確定你是否想要的事

- 驗收測試 agent 自己的工作說明在列舉報告內容時只列了四部分，沒提到新的「你叫我跳過的步驟」這一節（它是以範本為準，所以這次照樣寫了）。要不要順手把那份說明補上這一節？
