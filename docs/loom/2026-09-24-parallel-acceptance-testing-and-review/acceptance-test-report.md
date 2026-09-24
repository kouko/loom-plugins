# Acceptance testing 與第一輪 reviewer 在同一版本同時開跑 — 我試了什麼、結果如何

2026-09-24 在專案的乾淨副本上試過：第一次在 5263dc7a，修正後在 ee26369c 重測第 1、2、3、5、6 條；對照組用改動前的版本（710814a9）。每一條怎麼試、回來什麼：`docs/loom/2026-09-24-parallel-acceptance-testing-and-review/evidence/acceptance-test-evidence.md`。

## 你要的東西，一條一條

| # | 你要的 | 結果 | 發生了什麼 | Re-run |
|---|---|---|---|---|
| 1 | In closing review, the acceptance tester and the first-round reviewers start on the same version, and the reviewers begin reading the change without waiting for the acceptance test report. | works | 修正後的版本再試一次：兩位 reviewer 和 tester 在 34 到 46 秒之間都從同一個 commit 出發，派 reviewer 時明確告訴他們 acceptance testing 同時在跑；tester 還沒寫完報告，兩位 reviewer 就交回了第一遍。覆蓋這條的測試通過；完整的 automated test suite 會在變更被接受前執行，失敗就會擋下。 | re-tested |
| 2 | The same reviewers read the committed acceptance test report and its evidence file before giving their verdict, in the same round, so the report is still reviewed and committing it causes no extra review round. | works | 報告 commit 後，叫回的是原本那兩位 reviewer，他們讀了報告和 evidence、拿裡面的數字自己重算過，才給正式結論，整個過程仍只算一輪。上次提醒的問題已經修好：第一次的回覆現在標成「暫定」、沒有正式結論那一欄，光看格式就分得出哪個才算數；對報告本身的意見也歸到最接近的評分項（正確性）。另外，「修正後重測時，要先把新報告 commit 才叫回 reviewer」這條新規則，這次試跑停在第一輪、沒走到，只由測試確認文字在。 | re-tested |
| 3 | Findings from acceptance testing and from the reviewers on that version reach the fix round as one list. | works | 三方的問題合成一張修正清單、一份交接，包括 tester 找到的「只有空白時算成 1」和一位 reviewer 對報告的意見。不過三方找到的仍是同一個 bug，所以還是沒能證明「只有 tester 找到的問題」也會被收進來。 | re-tested |
| 4 | The acceptance test report the user reads at acceptance still states, one row per Acceptance line, what was tried and the result. | works | 報告範本和 tester 的工作說明都沒改；檢查報告格式的測試通過；新版試跑產出的報告每條 Acceptance 各一列，寫了怎麼試、結果如何。完整 automated test suite 會在接受前執行並在失敗時擋下。 | carried over — 這次修正沒有動報告範本或 tester 的工作說明（已比對確認），只改了 reviewer 收到的說明和叫回的順序 |
| 5 | Given a trial change run through closing review with both steps, the time from the start of closing review to the reviewers' verdicts is shorter than running acceptance testing and then the reviewers one after the other, shown by a trial run. | partly | 修正後這一次，從開始到兩位 reviewer 的結論是 2 分 16 秒，比上次條件乾淨的舊版對照（2 分 42 秒）快 26 秒。但這次的 tester 本身就快了約 19 秒（58 秒對 77 秒），又不是同時段的配對，扣掉之後差距仍在誤差範圍內。結論和上次一樣：兩件事確實重疊了，但在這麼小的改動上省不了多少時間。 | re-tested |
| 6 | The checker's rule list does not grow and no new step, reviewer or dispatch is added. | works | 規則數仍是 26 條；自動檢查算出的機制淨數仍是 140，其中寫在說明文字裡的閘門是 20 個，也沒變；新增文字裡沒有新閘門或派工字眼。這次試跑仍只派了 3 個 agent，多的只是兩次把原本的 reviewer 叫回來。相關測試通過，完整 automated test suite 會在接受前執行並在失敗時擋下。 | re-tested |

**試跑細節**：我做了一個很小的專案（算字數的指令），故意埋一個 bug：只把空白當分隔，tab 和換行不算，所以「one two↵three⇥four」會算成 2。之後請 Claude 在新版和舊版上各跑兩次 closing review，跑到第一輪結論出來、修正清單列好就停。

- 每次都確認載入的是對應版本的 closing-review（新版 3.14.0、舊版 3.13.0），而且只有新版載入的說明文字裡有「同時開跑」這句新規則。
- 四次都抓到那個 bug，也都得到 NEEDS_REVISION。
- 第一輪嘗試時，我的測試專案設定錯了：遠端的預設分支設成功能分支。兩個版本都照規則在派人之前就停下，我修好專案後重跑，那兩次不算進結果。
- 「叫回同一個 agent」在這種非互動模式下做得到，新版兩次都成功叫回。

**成本**：六次試跑共約 9.09 美元（含設定錯誤的兩次約 1.09 美元）。新版每次比對照組多花約 0.3–0.6 美元，多出來的是把 reviewer 叫回來讀報告的那幾輪。 修正後的重測只跑了一次新版，約 2.05 美元，所以總共約 11.14 美元。

## 對你既有的資料做了什麼

沒有 — 這個變更只改了工具遵循的說明文字、reviewer 的工作說明、幾支測試和版號，不讀也不改你既有的任何檔案或資料。

## 我替你決定的事

- **怎麼載入尚未發布的分支版本** — README 的安裝方式只會裝到已發布的 main，所以我改用 Claude Code 從本機資料夾載入 plugin，並確認每次都載入正確的版本。改用正式安裝方式時結果應相同，但這次沒有驗證。
- **每邊多跑一次** — 第一組的時間差被一個無關的延遲放大，看不出結論，所以照你的指示每邊加跑一次，約 3.77 美元。
- **試跑時略過 adversarial、跑到第一輪就停** — 為了省成本並把量測集中在第一輪。副作用是試跑裡最後的簽核檢查也跟著略過，所以試跑沒有涵蓋那一段。
- **重測只跑一次新版，沿用上次的舊版對照** — 舊版的內容沒有變，所以沒有再跑對照組，省下約 1.8 美元。代價是這次的比較不是同時段的配對，時間差比較不可靠。
- **新段落怎麼寫、叫回前的回覆不算結論、無法叫回的外部 reviewer 照舊等報告出來再開始** — 計畫裡標為 agent 自行決定。之後要改，就是改那段說明文字和它的測試。
- 沒有收到任何被駁回的 important 以上 finding。

## 我不確定你要不要的事

- 第 5 條在這麼小的案例上幾乎省不到時間。要不要我用一個比較大的改動（reviewer 看完要好幾分鐘的那種）再跑一組，確認實際能省多少？還是依你 session 記錄裡平均約 12 分鐘的等待，這次看到的運作方式就夠了？
