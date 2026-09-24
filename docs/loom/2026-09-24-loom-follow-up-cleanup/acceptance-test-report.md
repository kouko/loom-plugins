# 收掉前四個 loom 變更留下的待辦 — 我試了什麼、結果如何

2026-09-24 在專案的乾淨副本（84f546dc）上試過，另開一份改動前（710814a9）的乾淨副本當對照組。每一條怎麼試、回來什麼：`docs/loom/2026-09-24-loom-follow-up-cleanup/evidence/acceptance-test-evidence.md`。

## 你要的東西，一條一條

| # | 你要的 | 結果 | 發生了什麼 | Re-run |
|---|---|---|---|---|
| 1 | The fix-round paragraph in closing review names the acceptance-testing findings on the content the reviewers just read, including the committed acceptance test report, so no reading of it leaves them out. | works | 規則文字現在明寫「包含已 commit 的 acceptance test report」；新版試跑時 agent 把 tester 的 important 問題和 reviewer 的一起列進修正清單，並引用了這句新文字；覆蓋這條的測試通過，完整的 automated test suite 會在變更被接受前執行，失敗就會擋下。老實說：舊版對照組在同一個案例也沒漏掉，所以這次看不出行為差異。 | — |
| 2 | Closing review lists, among what it hands the acceptance tester, every important-or-worse finding it decided not to act on. | works | 新版寫出的派工內容把「被駁回的 important 問題和駁回理由」交給 tester，並提醒它若駁回理由和某條驗收條件衝突要寫進報告；舊版對照組的派工內容完全沒提那個被駁回的問題。 | — |
| 3 | The implementer contract states that a fix hand-off listing several instances of one defect class is one task, not a reason to return `BLOCKED`. | works | 規則已寫明「同一類問題的多處實例算一個任務」；新版 implementer 收到「兩個檔案、三處同類問題」的修正交接後直接先寫失敗測試、三處一起修好、一次 commit、回報 DONE，沒有退回。舊版對照組這次也做完了，看不出差異。 | — |
| 4 | No test outside the checker's own tests pins the checker's rule count as a literal. | works | 我自己搜尋整個 repo 的測試，除了 checker 自己的測試以外已找不到寫死「26 條規則」的地方（改動前有三處）；新加的防回歸測試也通過。 | — |
| 5 | The recovery-rule probe that is red on main passes, with the cause recorded as either wrong station prose or a wrong probe expectation. | works | 那組恢復規則探針從 repo 根目錄和從 plugin 目錄跑都是 13 個全過；改動前那一個確實是紅的；commit 說明和 CHANGELOG 都記下原因是「探針的預期過時」，不是規則文字錯。 | — |
| 6 | The repository memory store holds the PR #50 lesson — the measured time saving, the cost increase and why reviewers must keep reading the report — with its index entry. | works | 記憶條目寫了省下約一分鐘、成本多約 30%、以及 reviewer 曾在報告裡抓到 8 個重要錯誤（7 個光讀報告看不出來）所以必須繼續讀報告；索引多了一行，記憶庫驗證通過，重新產生的索引和 commit 的一字不差。 | — |
| 7 | The checker's rule list does not grow and no new step, reviewer or dispatch is added. | works | checker 規則仍是 26 條、清單和改動前完全相同；閘門計數仍是 140、與改動前輸出一致；改動只是在既有段落裡加一句、換一個片語，沒有新步驟、reviewer 或派工；相關測試通過，完整 automated test suite 會在接受前執行並在失敗時擋下。 | — |

**試跑細節（第 1–3 條）**：每條新舊版各跑一次，每次都確認真的載入了對應版本的說明文字（新版 3.14.0、舊版 3.13.0；implementer 另外讓它逐字唸出自己的規則，兩版各唸出各自的句子）。九次試跑總花費約 1.52 美元。第 2 條新舊版差異清楚；第 1、3 條舊版也做對了，證明新版會照新規則做，但沒證明這些案例下它改變了結果。

## 對你既有的資料做了什麼

沒有 — 這個變更只改了工具遵循的說明文字、測試、一個記憶條目和版號，不讀也不改你既有的任何檔案或資料。

## 我替你決定的事

- **怎麼載入尚未發布的分支版本** — README 的安裝方式只會裝到已發布版本，所以我用 Claude Code 從本機資料夾載入 plugin，並確認它蓋過了你機器上已裝的 3.13.0。改用正式安裝時結果應相同，但這次沒有驗證。
- **第 1 條的案例改用正常順序** — 派工建議「報告在 reviewer 開始後才 commit」；我改成規則要求、也是問題描述裡的順序（先 commit 報告、reviewer 再讀），因為那才是「字面讀法會漏掉」的情境。若你要的是那個亂序情境，這次沒測。
- **試跑用 sonnet、每邊一次** — 為了省成本；較弱的 model 對字面讀法反而更敏感。
- **計畫裡標為 agent 自行決定的幾項**（移除重複的規則數測試、探針修正原因判為「預期過時」、記憶條目寫法、版號升 minor）— 之後若要改，就是改那段文字和那支測試。
- 沒有收到任何被駁回的 important 以上 finding。

## 我不確定你要不要的事

- 那組恢復規則探針仍然不在正式測試套件裡跑，所以同樣的「紅了沒人發現」還可能再發生。要不要另開一個變更把它收進去？
- 第 1、3 條舊版在這些案例上也做對了。要不要再設計更刁的案例，看新文字是否真的改變結果？還是現在的證明就夠了？
