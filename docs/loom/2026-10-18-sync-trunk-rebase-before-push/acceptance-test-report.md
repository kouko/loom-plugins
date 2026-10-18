# 還沒 push 的分支同步 trunk 時改用 rebase — 我試了什麼、結果如何

2026-10-19 在專案的乾淨副本（50799c24）上試的。每一條怎麼試、輸出是什麼：`docs/loom/2026-10-18-sync-trunk-rebase-before-push/evidence/acceptance-test-evidence.md`。

所有情境都是在暫存目錄裡新建的真實 git repo：一個充當遠端的 bare repo、一個當作你的工作副本的 clone、另一個 clone 扮演別人往 trunk 推新 commit。你自己的全域 git 設定（例如 rebase 時自動合併 fixup commit、第一次 push 自動設定 upstream）全程保持生效。

## 你要的，逐條對照

| # | 你要的 | 結果 | 實際發生的事 | Re-run |
|---|---|---|---|---|
| 1 | 在一條從沒 push 過、落後 trunk 且不衝突的分支上，`sync-trunk` 讓分支自己的 commit 直接接在 trunk 最新的 commit 後面、沒有 merge commit，並回報內容有變動。 | works | 兩種開分支的方式都一樣：兩個自己的 commit 被接到 trunk 最新 commit 之後，歷史是一條直線、merge commit 數為 0，指令回報 rebased 和 content changed；你設定的 autosquash 也沒有偷偷把 fixup commit 合併掉。 | — |
| 2 | 在一條已經 push 過、落後 trunk 的分支上，`sync-trunk` 照舊 merge：已 push 的 commit 原封不動留在分支裡，下一次不加 force 的 push 會被遠端接受。 | works | 已 push 的 commit 編號都沒變，多了一個 merge commit；接著普通的 `git push` 直接成功。分支是從另一個 clone push 上去、這邊根本沒看過遠端分支時，也一樣走 merge 並 push 成功。 | — |
| 3 | 從沒 push 過的分支在 rebase 時會衝突的話，`sync-trunk` 列出衝突的檔案，並讓分支、它的 commit 和工作目錄完全維持指令執行前的樣子。 | works | 兩種衝突（整條分支和 trunk 改同一行、只有逐個 commit 重放時才撞到）都正確列出衝突的那個檔案，執行前後的 HEAD、每個 commit 編號、工作目錄狀態、被忽略的私人檔案內容和 stash 清單完全一致，也沒有留下進行中的 rebase。 | — |
| 4 | 其他所有 `sync-trunk` 結果（已是最新、警告、拒絕）都不變，且完整的 package suite 通過。 | works | 12 種情境（已是最新、只領先不落後、有未提交的修改、有未追蹤檔案、detached HEAD、在 trunk 上執行、抓不到遠端、被忽略的檔案會被 trunk 蓋掉、衝突、多給參數）新舊版本的輸出、結束碼、HEAD 和工作目錄逐字相同；涵蓋這個改動的 33 個測試全數通過；完整的 package suite 由正式接受前的自動測試把關，失敗就擋下這次改動。 | — |

## 對你既有的資料做了什麼

這次驗收只在暫存目錄裡新建的 repo 上操作，沒有碰你任何既有的 repo 或檔案。改動本身會碰到你既有的東西：對一條從沒 push 過的分支，`sync-trunk` 現在會改寫那些本機 commit，讓它們換上新的 commit 編號；舊的 commit 不會立刻消失，仍可從 git 的 reflog 找回（這類已不在分支上的 commit，git 預設保留約 30 天）。已經 push 過的 commit 一律不會被改寫。遇到衝突時什麼都不動。

## 我替你決定的事

- **「算 push 過」的判斷方式** — 實作選擇：遠端 origin 上有同名分支、這條分支設定了 push 目標、或分支裡任何一個自己的 commit 出現在任一遠端上，就算 push 過；只要查詢失敗就當作 push 過、改走 merge。偏保守，代價是少數其實沒 push 的情況也會留下 merge commit。日後要改只需調整這個判斷。
- **分支裡已經有 merge commit 時一律 merge** — 實作選擇，避免 rebase 把舊的 merge commit 攤平。代價：曾經 merge 過 trunk 的未 push 分支，之後也不會變回直線。
- **rebase 失敗但不是衝突時改走 merge** — 實作選擇（例如較舊的 git 或某些被忽略檔案的情況）：確認分支已完全還原後才改用 merge，所以這種情況下仍會出現 merge commit，而不是直接停下。
- **版號定為 3.42.1（patch）** — 實作選擇，理由是沒有改動任何對外的欄位或規則。
- **驗收時把 trunk 取名為 `trunk` 而不是 `main`** — 我的選擇：這台機器的指令防護會擋下任何往 `main` push 的指令，而模擬別人更新 trunk 必須 push。指令判斷 trunk 名稱的方式對兩者相同，所以不影響結果。
- **沒有自己跑完整的 package suite** — 依驗收流程，完整 suite 留給接受前的自動檢查執行；我只跑了涵蓋這四條的測試。
- 沒有被駁回的重要審查意見。

## 你要我略過的步驟

沒有 — 沒有任何步驟被略過。

## 我不確定你是否想要的事

- 有一種情況以前會成功、現在會停下：分支裡某個 commit 改了一行、後面的 commit 又改回來，而 trunk 同時也改了那一行。以前的 merge 會順利完成（整體來看分支沒動那一行），現在逐個 commit 重放時會撞到，於是列出衝突並停下，要你手動處理。這符合第 3 條的寫法，但你要不要這種情況改成退回 merge、而不是停下？
- 衝突在動手前就被偵測到時，訊息寫的是「the merge was not attempted」，即使這條分支原本會走 rebase。只是字面問題，要不要順手改成中性的說法？
