# 發布前檢查 PR 說明寫的驗證狀態，並整理 OpenCode 說明文字 — 我試了什麼、結果如何

2026-09-30 在專案的乾淨副本上試，之後每輪修正都在新的乾淨副本上重試受影響的各條；完整的重試紀錄和每一條怎麼試、回來什麼：`docs/loom/2026-09-30-publish-checks-stated-verification-status/evidence/acceptance-test-evidence.md`。

各條結果來自哪個版本：

- 第 1、2、3、6 條：f7a5bd7c（目前最新）
- 第 4 條：cf17c38e（之後的修正沒再動說明文件）
- 第 5 條：2c6c419e（之後的修正沒碰記憶庫）

## 你要的，一條一條看

| # | 你要的 | 結果 | 發生了什麼 | 重跑 |
|---|---|---|---|---|
| 1 | Publishing a change whose PR body states a verification status different from the one loom computes for that branch is refused before anything is pushed, and the refusal names the status the body must carry. | partly | 我在拋棄式 repo 裡用 PR 說明謊報「valid」，只要標籤後面有冒號（半形或全形），一般寫法、項目符號、編號清單、縮排清單、勾選清單、粗體、只有標籤加粗、引用、標題、表格一格，以及標籤裡混了合字（例如「ﬆ」）的寫法，全部被擋下，什麼都沒推出去，錯誤訊息直接給出該寫的那一行；同樣的說明在這次修改之前會被照推。但有四種寫錯的方式仍會照樣發布：標籤和值分在表格不同格、中間沒有冒號；狀態寫在表格第二格；用破折號代替冒號；標籤包在 HTML 標籤裡（例如 `<b>…</b>`）。實作者決定把它們列為已知限制，但你還沒同意這個較窄的範圍，所以只算部分達成（見最後一節）。 | re-tested |
| 2 | Publishing a change whose generated attestation exists in the working tree but is not committed is refused before anything is pushed, and the refusal says to commit it. | works | 驗證紀錄檔「建立了但沒 commit」和「commit 後又被改過」兩種都被擋下，沒有推出去，訊息寫「還沒 commit，commit 後再發布」；照做之後就能繼續。 | re-tested |
| 3 | Publishing a change whose PR body states the computed status, with no uncommitted attestation, behaves as before, including when the status is `absent` or `stale`. | works | 照原樣寫一行 `Verification status: absent` 或 `stale (...)`、完全不寫、一般句子或表格某一列只是提到驗證狀態、以及各種寫對但有裝飾的寫法（粗體、項目符號、編號、勾選清單、引用、標題、程式碼標記、全形冒號、各種表格），發布都照常推出分支，和修改前一樣。唯一例外是標籤裡混了合字的寫法：就算狀態寫對也會被擋，錯誤訊息給出照貼就能過的那一行。 | re-tested |
| 4 | The three OpenCode wording defects named in the Problem are fixed where they appear. | works | 十份 README 都寫明「TUI 在 2.0.18–2.0.20 沒有安裝選項」、不再把資料夾叫成檔案，開頭那句也改成「從 CLI 安裝的 plugin 在 TUI 裡也會載入」，不再暗示 TUI 能安裝；設計文件的第一條需求和設計決定都加上了版本範圍；上次的驗收報告保留當時「說明沒寫設定檔位置」的觀察，但在旁邊加了日期註記，說明之後的版本已經寫明位置。 | carried over — 之後的修正只改發布檢查的程式和測試，沒動任何說明文件 |
| 5 | The repository's memory store holds the lesson that a host's interface or install claim is checked against the host's official documentation before it is written into install docs. | works | 記憶庫多了一條教訓：寫任何主機的安裝或介面步驟前，先引用官方文件、並在標明的版本上實際試過；記憶庫的格式檢查通過。 | carried over — 之後的修正完全沒碰記憶庫 |
| 6 | The existing package test suite passes, and each plugin whose files change carries a new version consistent across manifests, CHANGELOGs and READMEs. | works | 在 f7a5bd7c 的乾淨副本上跑整套自動測試，全部通過、沒有失敗；另外，接受這次修改前還會再跑一次同一套自動測試，失敗就會擋下。三個有改到的 plugin 版本號（3.25.0、2.7.2、5.5.7）在所有 manifest、CHANGELOG、README 裡都一致，之後的修正沒動版本號。 | re-tested |

## 對你既有的資料做了什麼

沒有動到 — 這次修改只改了發布指令的檢查、說明文件和測試；你已經有的分支、PR 和設定檔都不會被讀寫。唯一的差別是：以後若 PR 說明寫錯驗證狀態，或驗證紀錄檔忘了 commit，發布會停下來，請你改一行或 commit 後再發布。

## 我替你決定的事

- **怎麼證明「在推出去之前就擋下」而不碰 GitHub**：我讓拋棄式 repo 的遠端指向一個保證不存在的網址，並攔下發布指令對外的每一個動作、逐一列出；推送改送到本機的空白遠端。被擋的情況對外動作是 0 個、本機遠端保持空白；照常發布的情況則真的推到本機遠端。改用這個方法，代價是沒有實際開出 PR，但開 PR 這一步這次沒有改動。
- **`valid` 狀態沒有實際試**：要做出一份真正有效的驗證紀錄，得在拋棄式 repo 跑完整套審查流程，我沒有這樣做，改看既有的自動測試（通過）。
- **設計文件第一條需求是加註、不是改寫**（實作時由 agent 決定）：原本使用者的那句話和「或 TUI 對話框」仍在條文裡，後面補了一句說明它不存在。這樣保留了原話的來龍去脈；如果你希望條文本身就不再提 TUI 對話框，需要再改一行。
- **上次驗收報告採「保留原觀察＋加日期註記」**（修正時由 agent 決定）：當時說明確實沒寫設定檔位置，所以原句留著，旁邊註明之後已寫明。這樣報告仍是當時的真實紀錄。
- **狀態寫對但有裝飾時要不要擋**：已由你的 intent 決定，不是我替你決定的 —— intent 的限制條件和第 3 條都寫「只擋寫錯的狀態」。上一輪的版本連寫對的也擋，第二次修正後已照 intent 改成只比對狀態值（見第 3 條）。
- **四種寫法刻意不檢查，列為已知限制**（實作者決定，會寫進 PR）：標籤和值分在表格不同格、中間沒有冒號（例如「Verification status｜valid」，或只有一欄的表頭、值寫在下一列）——因為只看一行分不出那是表頭還是資料；驗證狀態寫在表格的第二格（例如「狀態列｜Verification status: valid」）；用破折號代替冒號（「Verification status - valid」）；標籤包在 HTML 標籤裡（例如「`<b>Verification status:</b> valid`」，這一種在這次修改之前就存在）。這些寫錯也會照樣發布。其中「分在不同格」的寫法在前兩次修正的版本裡曾被擋下，後來為了不誤擋寫對的表頭而放掉。
- **標籤看得出來、但值讀不出來時一律擋下**（實作者決定）：例如標籤裡混了合字「ﬆ」。以前這種寫法會讓發布指令直接出錯中斷，現在改成擋下並給出該寫的那一行；代價是就算狀態寫對，這種寫法也要照貼改掉。
- 沒有任何重要以上的審查意見被駁回。

## 我不確定你要不要的

- 設計文件第一條需求：現在是「保留原話＋加註說 TUI 沒有對話框」，你可以接受，還是要把「或 TUI 對話框」從條文裡拿掉？
- 四種寫錯的方式（表格不同格沒冒號、狀態寫在第二格、用破折號、標籤包在 HTML 標籤裡）仍會照樣發布——你接受把它們列為已知限制，還是要這次一起擋？
