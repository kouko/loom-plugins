# 發布前檢查 PR 說明寫的驗證狀態，並整理 OpenCode 說明文字 — 我試了什麼、結果如何

2026-09-30 在專案的乾淨副本（2c6c419e）上試；第一輪審查修正後，同日在乾淨副本（cf17c38e）上重試受影響的各條；第二次修正後，同日在乾淨副本（df8feb8c）上再重試第 1、3 條；第三次修正後，同日在乾淨副本（f93e1ea6）上又重試第 1、3 條，這兩條現在的結果來自 f93e1ea6。第 2、4、6 條的結果來自 cf17c38e，第 5 條來自 2c6c419e。每一條怎麼試、回來什麼：`docs/loom/2026-09-30-publish-checks-stated-verification-status/evidence/acceptance-test-evidence.md`。

## 你要的，一條一條看

| # | 你要的 | 結果 | 發生了什麼 | 重跑 |
|---|---|---|---|---|
| 1 | Publishing a change whose PR body states a verification status different from the one loom computes for that branch is refused before anything is pushed, and the refusal names the status the body must carry. | partly | （f93e1ea6）我在拋棄式 repo 裡用 PR 說明謊報「valid」，一般寫法、項目符號、編號清單、縮排清單、粗體、引用、標題、全形冒號、表格一格，以及上次沒擋到的表格兩格（含無空格、加粗、三格、沒有開頭直線的寫法），全部被擋下，什麼都沒推出去，錯誤訊息直接給出該寫的那一行；同樣的說明在這次修改之前會被照推。但還有三種寫法錯了也照樣推出去：勾選清單「- [x] Verification status: valid」、表格裡第二格才寫「Verification status: valid」、以及用破折號代替冒號。 | re-tested |
| 2 | Publishing a change whose generated attestation exists in the working tree but is not committed is refused before anything is pushed, and the refusal says to commit it. | works | 驗證紀錄檔「建立了但沒 commit」和「commit 後又被改過」兩種都被擋下，沒有推出去，訊息寫「還沒 commit，commit 後再發布」；照做之後就能繼續。 | re-tested |
| 3 | Publishing a change whose PR body states the computed status, with no uncommitted attestation, behaves as before, including when the status is `absent` or `stale`. | partly | （f93e1ea6）照原樣寫一行 `Verification status: absent` 或 `stale (...)`、完全不寫、一般句子或表格某一列只是提到驗證狀態、以及各種寫對但有裝飾的寫法（粗體、項目符號、編號、引用、標題、程式碼標記、全形冒號、表格一格或兩格），發布都照常推出分支，和修改前一樣。但有兩種寫對的表格現在會被擋下，而修改前會照常發布：表格三格「Verification status｜absent｜from CI」（多一格備註），以及表頭寫「Verification status｜Reviewer」、狀態寫在下一列的表格。 | re-tested |
| 4 | The three OpenCode wording defects named in the Problem are fixed where they appear. | works | 十份 README 都寫明「TUI 在 2.0.18–2.0.20 沒有安裝選項」、不再把資料夾叫成檔案，開頭那句也改成「從 CLI 安裝的 plugin 在 TUI 裡也會載入」，不再暗示 TUI 能安裝；設計文件的第一條需求和設計決定都加上了版本範圍；上次的驗收報告保留當時「說明沒寫設定檔位置」的觀察，但在旁邊加了日期註記，說明之後的版本已經寫明位置。 | re-tested |
| 5 | The repository's memory store holds the lesson that a host's interface or install claim is checked against the host's official documentation before it is written into install docs. | works | 記憶庫多了一條教訓：寫任何主機的安裝或介面步驟前，先引用官方文件、並在標明的版本上實際試過；記憶庫的格式檢查通過。 | carried over — 這次修正完全沒碰記憶庫 |
| 6 | The existing package test suite passes, and each plugin whose files change carries a new version consistent across manifests, CHANGELOGs and READMEs. | works | 修正後在乾淨副本重跑整套自動測試，全部通過、沒有失敗；另外，接受這次修改前還會再跑一次同一套自動測試，失敗就會擋下。這次修正沒動版本號，三個 plugin 的版本號（3.25.0、2.7.2、5.5.7）在所有 manifest、CHANGELOG、README 裡仍然一致。 | re-tested |

## 對你既有的資料做了什麼

沒有動到 — 這次修改只改了發布指令的檢查、說明文件和測試；你已經有的分支、PR 和設定檔都不會被讀寫。唯一的差別是：以後若 PR 說明寫錯驗證狀態，或驗證紀錄檔忘了 commit，發布會停下來，請你改一行或 commit 後再發布。

## 我替你決定的事

- **怎麼證明「在推出去之前就擋下」而不碰 GitHub**：我讓拋棄式 repo 的遠端指向一個保證不存在的網址，並攔下發布指令對外的每一個動作、逐一列出；推送改送到本機的空白遠端。被擋的情況對外動作是 0 個、本機遠端保持空白；照常發布的情況則真的推到本機遠端。改用這個方法，代價是沒有實際開出 PR，但開 PR 這一步這次沒有改動。
- **`valid` 狀態沒有實際試**：要做出一份真正有效的驗證紀錄，得在拋棄式 repo 跑完整套審查流程，我沒有這樣做，改看既有的自動測試（通過）。
- **設計文件第一條需求是加註、不是改寫**（實作時由 agent 決定）：原本使用者的那句話和「或 TUI 對話框」仍在條文裡，後面補了一句說明它不存在。這樣保留了原話的來龍去脈；如果你希望條文本身就不再提 TUI 對話框，需要再改一行。
- **上次驗收報告採「保留原觀察＋加日期註記」**（修正時由 agent 決定）：當時說明確實沒寫設定檔位置，所以原句留著，旁邊註明之後已寫明。這樣報告仍是當時的真實紀錄。
- **狀態寫對但有裝飾時要不要擋**：已由你的 intent 決定，不是我替你決定的 —— intent 的限制條件和第 3 條都寫「只擋寫錯的狀態」。上一輪的版本連寫對的也擋，第二次修正後已照 intent 改成只比對狀態值（見第 3 條）。
- 沒有任何重要以上的審查意見被駁回。

## 我不確定你要不要的

- 設計文件第一條需求：現在是「保留原話＋加註說 TUI 沒有對話框」，你可以接受，還是要把「或 TUI 對話框」從條文裡拿掉？
- 寫錯也不會被擋的三種寫法：勾選清單「- [x] Verification status: valid」、狀態寫在表格第二格、用破折號代替冒號。要把哪些納入檢查，還是接受它們不在檢查範圍內？（勾選清單在 PR 說明裡很常見，我認為最可能真的遇到。）
- 寫對卻被擋的兩種表格：多一格備註的三格表格，以及表頭寫「Verification status」、值寫在下一列的表格。依 intent 這兩種不該被擋；錯誤訊息會給出照貼就能過的那一行，所以代價只是多改一次，但它和 intent 有出入。
