# 恢復 skill 資料夾檢查並清理 AGENTS.md — 我試了什麼、結果如何

Tried on 2026-11-18 at 9552e1de1. 在專案的乾淨副本上試過。每一條怎麼試、回來什麼：`docs/loom/2026-11-18-skill-folder-check-and-agents-cleanup/evidence/acceptance-test-evidence.md`。

## 你要的東西，逐條對照

| # | 你要的 | 結果 | 實際發生的事 | 重跑 |
|---|---|---|---|---|
| 1 | 在任一 skill 的子資料夾內加入含檔案的巢狀資料夾後，不論是否已 commit，完整 package suite 都會失敗並指出該路徑；移除後恢復通過。 | partly | 涵蓋這條的測試（屬於自動化測試套件，該套件會在變更被接受前執行，失敗就會擋下）在這些情況都失敗並指出路徑，移除後恢復通過：一般巢狀資料夾未 commit、已 staged、已 commit；放在 skill 子資料夾、skill 資料夾或再深一層的 git repository，不論未追蹤或以 gitlink commit；以 gitlink commit 在 plugin 資料夾、plugin 的 skills 資料夾、skill 資料夾或 skill 子資料夾時，沒抓內容的新 clone 也會失敗（這時只指得出資料夾本身）。**會通過的界線**：未 commit 且名稱被 git 忽略的資料夾（包括放在這種名稱底下的 repository）；指向資料夾的 symlink，不論是否 commit；已 commit 的檔案從磁碟刪除、但刪除還沒 commit 時（同一個 commit 的新 clone 仍會失敗）；不在 plugin 清單上的頂層資料夾；plugin 裡 skills 以外資料夾的 gitlink。**會失敗但指不出路徑的界線**：gitlink 放在 loom-code 這個 plugin 資料夾時，測試程式啟動不了，所以失敗訊息沒有路徑。**比你要求更嚴的界線**：內容扁平的 repository 一旦以 gitlink commit 也會失敗；巢狀 repository 裡被忽略的快取檔（例如 `__pycache__/x.pyc`）也會失敗。各界線的原因見下面「我替你決定的事」。 | re-tested |
| 2 | `AGENTS.md` 不再提及不在這個 repo 的 plugin，也不再指向不存在的檔案或測試。 | works | 文件裡找不到其他 plugin 的名稱，實際指向的檔案和測試全部存在；找不到對應檔案的只剩寫法示範、檔名樣式、文字格式和指令。 | carried over — 這次修正只改了測試檔，`AGENTS.md` 沒有變，它指向的測試檔也還在。 |
| 3 | `AGENTS.md` 對 skill 資料夾檢查、審查鏡頭與人數、版號及 changelog 的描述，都與 repo 現行的檢查和檔案一致。 | works | `AGENTS.md` 的描述都與實際相符，它指向的測試檔開頭所列的規則和例外，也和我試到的結果一致。 | re-tested |
| 4 | `AGENTS.md` 仍保留 skill 資料夾扁平與版號 bump 的 MUST 規則，完整 package suite 通過。 | works | 兩條 MUST 規則都還在，與這份文件和版號相關的 278 個測試全部通過；完整的自動化測試套件會在變更被接受前執行，失敗就會擋下，這次驗收沒有另外跑完整套件。 | re-tested |

## 對你既有的資料做了什麼

這個變更改寫了你既有的 `AGENTS.md`：新增 18 行、刪除 57 行，包括你同意移除的跨 plugin 委派規則。舊內容仍可從 git 歷史讀回，不需要另外備份。其餘改動都是這個變更新增的測試和紀錄，沒有動到任何 plugin 的內容。我的試驗都在另外複製的副本裡進行，沒有碰你的工作目錄。

## 我替你決定的事

前八項是檢查的界線，請逐項決定接受或退回。

- **未 commit 且被 git 忽略的路徑不算違規** — 實作選擇放行，因為這些內容不會進 repo，而本機快取不該讓測試失敗。我試過 `node_modules`、`__pycache__`、`.venv`、`.pytest_cache`、被忽略的 `.pyc` 檔，以及放在 `node_modules` 名稱底下的 repository，都通過；強制加入 git 後就失敗。要改成也擋，本機快取就可能讓測試失敗。
- **指向資料夾的 symlink 不算違規** — 實作選擇放行，因為 git 只存連結本身。代價是規則可以被繞過：我試過連結後面有巢狀檔案，未 commit、已 commit、新 clone 都通過，而且都能透過連結讀到那個檔案。要改成也擋，只需調整檢查，但所有指向資料夾的連結都會被擋。
- **已 commit 的檔案從磁碟刪除後，即使刪除還沒 commit 也算通過** — 實作把刪除視為修正，因為檢查看的是目前磁碟上還有什麼。代價是本機通過時，同一個 commit 的新 clone 仍會失敗，要等刪除 commit 後才全部通過。
- **只檢查 plugin 清單上的頂層資料夾** — 實作選擇這樣，避免把測試資料或紀錄裡的 `skills` 資料夾當成 plugin。代價是新 plugin 在加入清單前，裡面的巢狀資料夾不會被擋，我試過未 commit 和已 commit 都通過。
- **plugin 資料夾、skills 資料夾和其下的 gitlink 一律失敗，即使內容是扁平的** — gitlink 是外層 repo 只記下內層 commit 的指標，不存檔案；新 clone 沒有內容可查，所以實作直接擋下。這比你的要求嚴：同樣的扁平 repository 未追蹤時會通過，commit 成 gitlink 就失敗。plugin 裡 skills 以外資料夾的 gitlink 不在檢查範圍，我試過裡面有巢狀檔案也通過，因為那裡不是 skill。
- **gitlink 放在 loom-code 資料夾時，失敗訊息沒有路徑** — 測試程式啟動時要讀 loom-code 裡的程式，這個資料夾被換掉就直接報錯結束。套件仍然失敗，所以不會放行，但你看不到是哪個路徑；單獨跑這支檢查才看得到。移除 gitlink 後還要把 plugin 檔案還原，才會恢復通過。放在 loom-design 資料夾則正常指出路徑。
- **移除 gitlink 的方式** — 失敗訊息現在寫明用 `git rm --cached <路徑>` 再 commit，我在每一層都試過可行。如果內層 repository 還留在磁碟上、裡面又有巢狀檔案，檢查會繼續失敗並指出那個檔案，要把資料夾移走才通過；內容扁平就直接通過。`git rm -r -f` 只有在資料夾裡還有內層 repository 時會被 git 拒絕；新 clone 的空資料夾、資料夾不存在、或資料夾裡只有一般檔案時都成功。
- **巢狀 repository 裡被忽略的檔案也算數** — 外層 git 看不進巢狀 repository，所以實作直接掃磁碟，不套用忽略規則。結果是本來扁平的 repository 只要多了 `__pycache__` 這類快取，檢查就失敗，清掉後恢復通過。代價是偶爾誤報，好處是不會漏掉真正的巢狀內容。
- **審查細節改為指向現有來源** — `AGENTS.md` 不再自己列出審查鏡頭和人數，改指向鏡頭說明文件與計算人數的自動檢查工具，避免兩邊內容不一致。代價是讀者要多開一個地方才看得到細節。
- **這次不 bump plugin 版號** — 變更沒有動到任何 plugin 內容，已安裝的副本不受影響。若日後認為文件變更也要發版，需要另開變更。
- **把抓到問題的對抗測試留進常設測試** — 這樣之後每次變更都會跑到，代價是多了四個測試檔。

沒有任何嚴重程度 important 以上的審查意見被駁回。

## 你要我跳過的步驟

沒有 — 沒有跳過任何步驟。

## 我不確定你是否想要的事

- 指向資料夾的 symlink 能讓巢狀內容通過檢查，而且 commit 後仍然通過。你接受，還是要擋下？
- 未 commit 且名稱被忽略的資料夾會通過。你接受嗎？
- 刪除還沒 commit 時本機會通過、新 clone 仍失敗。你接受嗎？
- 還沒列進 plugin 清單的新 plugin 不受檢查。你接受嗎？
- 扁平的 gitlink 會失敗，巢狀 repository 裡被忽略的快取檔也會失敗，這兩項比你的要求嚴。你接受嗎？
- gitlink 放在 loom-code 資料夾時，套件會失敗但指不出路徑。你接受，還是要讓它也指出路徑？
