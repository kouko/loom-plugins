# 清掉 OpenCode 啟動指令那次改動留下的審查小意見 — 我試了什麼、結果如何

2026-09-30 在專案的乾淨副本上試的：第一輪在版本 41121f04，修正後第二輪在版本 b4b6fa5b。每一條怎麼試、得到什麼回應：`docs/loom/2026-09-30-opencode-entry-commands-review-nits/evidence/acceptance-test-evidence.md`。

名詞說明：「transcript（對話紀錄）」是 loom 在 OpenCode 上替每個對話另存的一份「使用者說過的話」，用來判斷你用哪種語言說話；「skill 內文」是執行指令時 OpenCode 自動接在你打的字後面、給模型看的那一大段說明；「分隔句」指內文開頭那句 "Base directory for this skill:"。

## 你要的，一條一條看

| # | 你要的 | 結果 | 實際發生什麼 | Re-run |
|---|---|---|---|---|
| 1 | The loom-code, loom-design and loom-workflow changelogs state that on OpenCode a command's skill body is no longer recorded as the user's words. | works | 三個 plugin 的更新紀錄最上面都新增一段，寫明在 OpenCode 上執行指令時，skill 內文不會被當成你說的話；已發布的舊段落一字未動。 | carried over — 這次修正沒有碰任何更新紀錄 |
| 2 | On OpenCode, a message the user types that contains "Base directory for this skill:" is recorded in full, while a loom command's prompt is still recorded as only the typed command text. | works | 修正後在真的 OpenCode（v2.0.20）裡重新走一遍，結果跟 9/30 第一輪一樣：執行 loom-code 與 loom-workflow 的指令時，模型收到完整 skill 內文，但對話紀錄只留下你打的那行；貼上一段含分隔句的文字（包括一段以斜線開頭的），對話紀錄整段保留、跟模型收到的一模一樣。 | re-tested |
| 3 | The loom-code README (en, ja, zh-TW) no longer labels expert-mode "user-invoked" in a way that clashes with the entry skills now also runnable as commands. | works | 英、日、繁中三份說明文件都改稱 expert-mode 為「僅限指令」（command-only／コマンド専用），舊的「使用者呼叫」字樣全部不見了。 | carried over — 這次修正沒有碰任何說明文件 |
| 4 | The 2026-09-30-opencode-entry-commands acceptance report explains or replaces "important", "Build 階段" and "上次測試" in plain words, and that change's plan gives the correct edited test line range and the full W2-01 file list. | works | 舊報告裡三個詞都換成白話（例如「上次測試」改成「9/29 那次 OpenCode v2 驗收」），驗收結果欄沒動；第一輪指出的那句「安裝方式本身上次已驗證過」也改成「在 9/29 那次 OpenCode v2 驗收已驗證過」，整份舊報告不再有沒說明是哪次的「上次」；舊計畫的行號範圍與檔案清單仍然正確。 | re-tested |
| 5 | The loader keeps the skill-body separator in one place, its header comment says a skill with both keys stays command-only, and the renamed loader test says what it checks. | works | 分隔句在載入程式裡仍只寫一次、兩處共用，它的名字改得更貼切；檔頭說明寫著「兩個設定都開時只當指令」；改名後的測試名稱說出它真的在檢查的兩件事；三個 plugin 各自的載入程式副本和主檔完全相同。 | re-tested |
| 6 | The existing package test suite passes, and each plugin whose files change carries a new version consistent across manifests, CHANGELOGs and READMEs. | works | 跟這次改動相關的測試全數通過（60 個，比第一輪多了修正新增的 2 個）；完整測試組由自動化測試負責——它會在變更被接受前執行，失敗就擋下。版號仍是 loom-code 3.26.1、loom-design 2.8.1、loom-workflow 5.6.1，各處一致。 | re-tested |

## 對你既有的資料做了什麼

沒有。這次只改了程式、說明文件和先前那次改動的報告與計畫的用字；你電腦上 OpenCode 的設定和正在執行的 OpenCode 都沒碰。唯一的行為差別是：之後在 OpenCode 上，你自己打（或貼上）的訊息即使含有分隔句，也會完整記進對話紀錄，不再被截斷。

## 我替你決定的

- **第 2 條用假的模型測，而不是真的 AI 模型** — 我在隔離環境裡放了一個只會回「ok」的本機假模型。這條要看的是「記下來的是什麼」，這在送給模型之前就決定了，跟模型怎麼回答無關；好處是完全不用任何 API 金鑰、不花錢。代價是這次沒有看到模型實際跑完 skill 流程，但那部分 9/30 那次 OpenCode 啟動指令驗收已經看過，這次也沒改。
- **從本機固定版本安裝，而不是從 GitHub 的 main 安裝** — 這個分支還沒進 main。安裝步驟本身跟 9/30 那次驗收一樣走得通。
- **修正後第 2 條仍在真的 OpenCode 裡重跑一次** — 修正只改了一個名字和測試，照理不影響行為；但它改到的正是負責記錄的那個程式檔，只看測試不算數，所以整條重新實際操作。
- **一種刻意湊出來的訊息仍會被截斷** — 如果有人故意打一段「以 `/某某:名字` 開頭，後面接分隔句，再接一個以 `skills/名字` 結尾的路徑」的訊息，它會被當成指令而截斷。這只可能是刻意模仿，我沒有把它算成失敗；實作時也是刻意這樣取捨的（為了讓其他 loom plugin 的指令也能正確截斷）。

沒有任何會影響結果的審查意見被駁回。

## 我不確定你要不要的

沒有。（第一輪問的「舊報告那句『安裝方式本身上次已驗證過』要不要改成白話」，已在修正中改好。）
