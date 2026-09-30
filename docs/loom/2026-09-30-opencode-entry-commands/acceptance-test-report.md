# 在 OpenCode 的指令清單啟動 loom — 我試了什麼、結果如何

2026-09-30 在專案的乾淨副本（433c2eb）上測試，使用真實的 OpenCode v2.0.20，裝在一個與你平常的 OpenCode 完全隔開的設定裡。每一條怎麼試、回來什麼：`docs/loom/2026-09-30-opencode-entry-commands/evidence/acceptance-test-evidence.md`。

## 你要的東西，一條一條看

| # | 你要的 | 結果 | 實際發生什麼 | Re-run |
|---|---|---|---|---|
| 1 | In OpenCode v2 with loom installed, the `/` command list offers loom-code:using-loom-code, loom-design:using-loom-design, loom-workflow:using-loom-workflow, loom-workflow:handoff, loom-workflow:recap-state and loom-workflow:goal-create, and running each one starts that skill's workflow. | works | 在 OpenCode 畫面打 `/loom`，清單正好列出這六個加上 expert-mode，每個只出現一次；六個我都實際執行過，各自都開始了該 skill 的流程（recap 給出回顧、handoff 寫出交接檔、goal-create 產出目標、三個入口開始分流或提問）。 | — |
| 2 | The same six remain available as skills the model can load in OpenCode, as before. | works | 這六個仍在 OpenCode 的 skill 清單裡，請模型用 skill 工具逐一載入，六個都成功，載入的內容與原始檔一致；loom 的 skill 總數跟 9/29 那次 OpenCode v2 驗收一樣是 24 個。 | — |
| 3 | loom-code:expert-mode is still offered as a command and is still not offered as a skill. | works | expert-mode 出現在 `/` 清單，但不在 skill 清單裡；模型試著把它當 skill 載入時被拒絕（「Unable to load skill」）。 | — |
| 4 | The README's OpenCode section tells a user how to start loom after installing it, including these commands. | works | 總 README 和三個 plugin 的英、日、繁中 README，在 OpenCode 安裝步驟後面都加了一句「用哪個指令開始 loom」，總 README 列出全部六個，名稱和 OpenCode 實際顯示的一字不差。 | — |
| 5 | The existing package test suite passes, and each plugin whose files change carries a new version consistent across manifests, CHANGELOGs and READMEs. | works | 跟這次改動相關的測試全數通過（31 個）；完整測試組由自動化測試負責——它會在變更被接受前執行，失敗就擋下。三個 plugin 都換了新版號（loom-code 3.26.0、loom-design 2.8.0、loom-workflow 5.6.0），各處設定檔、CHANGELOG、README 一致，沒有殘留舊版號。 | — |

另外兩件你交代要看的事：

- **中文對話跑完指令後，語言提醒還在嗎（實作階段自動對抗測試抓到、已經修掉的問題）**：還在。我先用中文說話、再執行 `/loom-code:using-loom-code`，之後模型載入 skill 時，拿到的提醒仍是「用繁體中文跟使用者說話」；loom 記錄的「使用者說過的話」只有你打的那行指令，沒有把英文的 skill 內文當成你說的話。
- **同一個名字會不會在清單裡同時出現「指令」和「skill」兩份**：不會。`/` 清單只列指令、不列 skill，所以每個名字只出現一次；兩份登記都存在，但只在後台看得到，這正是「既是指令也是 skill」的預期狀態。

## 對你既有的資料做了什麼

沒有——它只改了 loom 自己的檔案。這次改動只影響 OpenCode 啟動時怎麼登記 loom 的指令，不讀也不寫你任何既有的專案或設定。測試全程用隔離的 OpenCode 設定和一個臨時空專案，你平常的 OpenCode 設定與正在跑的兩個 OpenCode 服務都沒碰，結束時仍在運作。唯一留在測試區外面的，是 loom 在系統暫存資料夾裡為每個測試對話寫的一小份語言紀錄（7 個小檔，只含測試時打的句子）。

## 我替你決定的事

- **怎麼標記「這個 skill 也要當指令」** — 在那六個 skill 的開頭加一行 Claude Code 本來就有、意思相同的設定，而不是發明新欄位或在程式裡寫死名單。這一行在 Claude Code 上本來就是預設值，所以那邊行為不變。之後要改，只需調整這六個檔案和 OpenCode 的載入程式。
- **README 只加一句，不開新段落** — 每份 README 在原本「skill 如何提供」那一行後面接一句說明怎麼開始。之後想寫得更詳細，隨時可以再補。
- **三個 plugin 都升小版號（不是修補版號）** — 因為每個都多了新的 OpenCode 指令。這只影響版號字串，改回去成本很低。
- **把實作階段自動對抗測試裡抓到語言問題的那個案例，正式收進測試組** — 以後同樣的問題再出現會被自動擋下。
- **測試時從本機固定版本安裝，而不是從 GitHub 的 main 安裝** — 這個分支還沒進 main，README 寫的 GitHub 安裝路徑這次沒有實際走過；安裝方式本身上次已驗證過。

沒有任何會影響結果的審查意見被駁回。

## 我不確定你要不要的

沒有。
