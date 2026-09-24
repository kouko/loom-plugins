# Acceptance testing 與第一輪 reviewer 在同一版本同時開跑 — 我試了什麼、結果如何

2026-09-24 在專案的乾淨副本（5263dc7a）上試過；對照組用改動前的版本（710814a9）。每一條怎麼試、回來什麼：`docs/loom/2026-09-24-parallel-acceptance-testing-and-review/evidence/acceptance-test-evidence.md`。

## 你要的東西，一條一條

| # | 你要的 | 結果 | 發生了什麼 | Re-run |
|---|---|---|---|---|
| 1 | In closing review, the acceptance tester and the first-round reviewers start on the same version, and the reviewers begin reading the change without waiting for the acceptance test report. | works | 新版兩次實際試跑，兩位 reviewer 和 acceptance tester 都在十幾秒內從同一個 commit 出發，reviewer 在 tester 還沒寫完報告時就看完了第一遍。舊版兩次都是 tester 先跑完、報告 commit 之後才派 reviewer。覆蓋這條的測試通過；完整的 automated test suite 會在變更被接受前執行，失敗就會擋下。 | — |
| 2 | The same reviewers read the committed acceptance test report and its evidence file before giving their verdict, in the same round, so the report is still reviewed and committing it causes no extra review round. | works | 報告 commit 後，兩次都是把「原本那兩位」reviewer 叫回來（不是新開），並告訴他們從出發的 commit 到報告 commit 多了什麼。他們讀完報告和 evidence 才給正式結論，而且真的有拿報告內容去對照。第一次回來時兩位都自己註明「這不是結論」，整個過程只算一輪。小提醒：第二次試跑時，這個「暫定」回覆裡已經寫了和正式結論一樣格式的 NEEDS_REVISION 欄位，主流程有忽略它，但光看格式分不出哪個才是正式的。 | — |
| 3 | Findings from acceptance testing and from the reviewers on that version reach the fix round as one list. | works | 新版兩次都把 tester 和兩位 reviewer 的問題合成一張修正清單、一份交接。不過這個案例三方找到的是同一個 bug，舊版也一樣合成一張，所以這次沒能證明「只有 tester 找到的問題」也會被收進來。 | — |
| 4 | The acceptance test report the user reads at acceptance still states, one row per Acceptance line, what was tried and the result. | works | 報告範本和 tester 的工作說明都沒改；檢查報告格式的測試通過；新版試跑產出的報告每條 Acceptance 各一列，寫了怎麼試、結果如何。完整 automated test suite 會在接受前執行並在失敗時擋下。 | — |
| 5 | Given a trial change run through closing review with both steps, the time from the start of closing review to the reviewers' verdicts is shorter than running acceptance testing and then the reviewers one after the other, shown by a trial run. | partly | 兩組對照都是新版比較快：第一組 3 分 00 秒對 4 分 42 秒，第二組 2 分 38 秒對 2 分 42 秒。但第一組差距主要是舊版 tester 花了兩分鐘在整台電腦上找範本檔，跟這次改動無關；條件乾淨的第二組只差 4 秒，在誤差範圍內。原因是這個改動很小，reviewer 看完整份改動只要半分鐘左右，被叫回來讀報告也要差不多的時間，所以省不下來。 | — |
| 6 | The checker's rule list does not grow and no new step, reviewer or dispatch is added. | works | 規則數仍是 26 條，閘門計數仍是 140，新增文字裡沒有新閘門或派工字眼；每次試跑都只派了 3 個 agent（1 位 tester、2 位 reviewer），新版多的是把原本兩位 reviewer 叫回來，不是新派人。相關測試通過，完整 automated test suite 會在接受前執行並在失敗時擋下。 | — |

**試跑細節**：我做了一個很小的專案（算字數的指令），故意埋一個 bug：只把空白當分隔，tab 和換行不算，所以「one two↵three⇥four」會算成 2。之後請 Claude 在新版和舊版上各跑兩次 closing review，跑到第一輪結論出來、修正清單列好就停。

- 每次都確認載入的是對應版本的 closing-review（新版 3.14.0、舊版 3.13.0），而且只有新版載入的說明文字裡有「同時開跑」這句新規則。
- 四次都抓到那個 bug，也都得到 NEEDS_REVISION。
- 第一輪嘗試時，我的測試專案設定錯了：遠端的預設分支設成功能分支。兩個版本都照規則在派人之前就停下，我修好專案後重跑，那兩次不算進結果。
- 「叫回同一個 agent」在這種非互動模式下做得到，新版兩次都成功叫回。

**成本**：六次試跑共約 9.09 美元（含設定錯誤的兩次約 1.09 美元）。新版每次比對照組多花約 0.3–0.6 美元，多出來的是把 reviewer 叫回來讀報告的那幾輪。

## 對你既有的資料做了什麼

沒有 — 這個變更只改了工具遵循的說明文字、reviewer 的工作說明、幾支測試和版號，不讀也不改你既有的任何檔案或資料。

## 我替你決定的事

- **怎麼載入尚未發布的分支版本** — README 的安裝方式只會裝到已發布的 main，所以我改用 Claude Code 從本機資料夾載入 plugin，並確認每次都載入正確的版本。改用正式安裝方式時結果應相同，但這次沒有驗證。
- **每邊多跑一次** — 第一組的時間差被一個無關的延遲放大，看不出結論，所以照你的指示每邊加跑一次，約 3.77 美元。
- **試跑時略過 adversarial、跑到第一輪就停** — 為了省成本並把量測集中在第一輪。副作用是試跑裡最後的簽核檢查也跟著略過，所以試跑沒有涵蓋那一段。
- **新段落怎麼寫、叫回前的回覆不算結論、無法叫回的外部 reviewer 照舊等報告出來再開始** — 計畫裡標為 agent 自行決定。之後要改，就是改那段說明文字和它的測試。
- 沒有收到任何被駁回的 important 以上 finding。

## 我不確定你要不要的事

- 第 5 條在這麼小的案例上幾乎省不到時間。要不要我用一個比較大的改動（reviewer 看完要好幾分鐘的那種）再跑一組，確認實際能省多少？還是依你 session 記錄裡平均約 12 分鐘的等待，這次看到的運作方式就夠了？
