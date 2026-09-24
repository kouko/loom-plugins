# 收掉前四個 loom 變更留下的待辦 — 我試了什麼、結果如何

第一輪 2026-09-24 在專案的乾淨副本（84f546dc）上試過，另開一份改動前（710814a9）的乾淨副本當對照組；第一次修正後在新的乾淨副本（3bb4a226）上重試了修正可能影響的幾條；第二次修正（讓 Ship 列出晚到的駁回）後在乾淨副本（1ee91bb0）上重試第 5、7 條。每一條怎麼試、回來什麼：`docs/loom/2026-09-24-loom-follow-up-cleanup/evidence/acceptance-test-evidence.md`。

## 你要的東西，一條一條

| # | 你要的 | 結果 | 發生了什麼 | Re-run |
|---|---|---|---|---|
| 1 | The fix-round paragraph in closing review names the acceptance-testing findings on the content the reviewers just read, including the committed acceptance test report, so no reading of it leaves them out. | works | 規則文字現在明寫「包含已 commit 的 acceptance test report」；新版試跑時 agent 把 tester 的 important 問題和 reviewer 的一起列進修正清單，並引用了這句新文字；覆蓋這條的測試通過，完整的 automated test suite 會在變更被接受前執行，失敗就會擋下。老實說：舊版對照組在同一個案例也沒漏掉，所以這次看不出行為差異。 | carried over — 這次修正沒有動到修正清單那段文字，也沒動它的測試 |
| 2 | Closing review lists, among what it hands the acceptance tester, every important-or-worse finding it decided not to act on. | works | 修正後重跑同一個案例：新版寫出的派工內容仍把「被駁回的 important 問題和駁回理由」交給 tester，還要求它核對駁回理由、若和某條驗收條件衝突就寫進報告。新加的那句只處理「tester 最後一次派出之後才駁回」的問題（改列進 PR 的驗證段落），那時已不會再派 tester，所以不影響這條；舊版對照組（第一輪）完全沒提被駁回的問題。覆蓋這條的測試通過，完整 automated test suite 會在接受前執行並在失敗時擋下。 | carried over — 第二次修正只改 Ship 寫 PR 的說明，交給 tester 的內容沒變；第一次修正後已重試 |
| 3 | The implementer contract states that a fix hand-off listing several instances of one defect class is one task, not a reason to return `BLOCKED`. | works | 規則已寫明「同一類問題的多處實例算一個任務」；新版 implementer 收到「兩個檔案、三處同類問題」的修正交接後直接先寫失敗測試、三處一起修好、一次 commit、回報 DONE，沒有退回。舊版對照組這次也做完了，看不出差異。 | carried over — 這次修正沒有動到 implementer 的規則 |
| 4 | No test outside the checker's own tests pins the checker's rule count as a literal. | works | 修正放寬了防回歸測試（不再把名為 RULES 的清單當成 checker 規則），所以我重新搜尋整個 repo 的測試：除了 checker 自己的測試以外，仍找不到寫死「26 條規則」的地方，也找不到用那個名字寫死數量的地方；防回歸測試（含新加的反例）通過。 | carried over — 第二次修正沒動測試裡的規則數或防回歸測試；第一次修正後已重試 |
| 5 | The recovery-rule probe that is red on main passes, with the cause recorded as either wrong station prose or a wrong probe expectation. | works | 修正改了這些探針會讀的那份規則文字，所以重跑：從 repo 根目錄和從 plugin 目錄跑都是 13 個全過；原因記錄（探針的預期過時）沒變。第二次修正後再跑一次，仍 13 個全過。 | 重試 |
| 6 | The repository memory store holds the PR #50 lesson — the measured time saving, the cost increase and why reviewers must keep reading the report — with its index entry. | works | 記憶條目現在多說明那些成對數字是每邊 3 次的平均；仍寫著省下約一分鐘、成本多約 30%、以及 reviewer 曾在報告裡抓到 8 個重要錯誤（7 個光讀報告看不出來）所以必須繼續讀報告；索引那一行還在，記憶庫驗證通過，重新產生的索引和 commit 的一字不差。 | carried over — 第二次修正沒動記憶庫；第一次修正後已重試 |
| 7 | The checker's rule list does not grow and no new step, reviewer or dispatch is added. | works | checker 規則仍是 26 條、清單和改動前完全相同；閘門計數仍是 140、與改動前輸出一致。兩次修正加的句子只是把晚到的駁回寫進 PR 既有的驗證段落（Ship 那一站現在也照寫），沒有新步驟、reviewer、閘門或派工；第二次修正後重跑，規則數與閘門計數仍和改動前相同；相關測試通過，完整 automated test suite 會在接受前執行並在失敗時擋下。 | 重試 |

**試跑細節**：第一輪第 1–3 條新舊版各跑一次，共九次約 1.52 美元；第 2 條新舊版差異清楚，第 1、3 條舊版也做對了。修正後只重跑第 2 條的新版一次，外加一次確認載入的是分支版本（3.14.0），共約 0.29 美元。第二次修正沒有試跑，只確認 Ship 那一站載入後念得出新句子，約 0.06 美元。

## 對你既有的資料做了什麼

沒有 — 這個變更只改了工具遵循的說明文字、測試、一個記憶條目和版號，不讀也不改你既有的任何檔案或資料。

## 我替你決定的事

- **怎麼載入尚未發布的分支版本** — README 的安裝方式只會裝到已發布版本，所以我用 Claude Code 從本機資料夾載入 plugin，並確認它蓋過了你機器上已裝的 3.13.0。改用正式安裝時結果應相同，但這次沒有驗證。
- **第 1 條的案例改用正常順序** — 派工建議「報告在 reviewer 開始後才 commit」；我改成規則要求、也是問題描述裡的順序（先 commit 報告、reviewer 再讀），因為那才是「字面讀法會漏掉」的情境。若你要的是那個亂序情境，這次沒測。
- **試跑用 sonnet、每邊一次** — 為了省成本；較弱的 model 對字面讀法反而更敏感。
- **修正後第 2 條不重跑舊版對照組** — 舊版文字沒變，第一輪的對照結果仍然適用。
- **計畫裡標為 agent 自行決定的幾項**（移除重複的規則數測試、探針修正原因判為「預期過時」、記憶條目寫法、版號升 minor）— 之後若要改，就是改那段文字和那支測試。
- 沒有收到任何被駁回的 important 以上 finding。

## 我不確定你要不要的事

- 那組恢復規則探針仍然不在正式測試套件裡跑，所以同樣的「紅了沒人發現」還可能再發生。要不要另開一個變更把它收進去？
- 第 1、3 條舊版在這些案例上也做對了。要不要再設計更刁的案例，看新文字是否真的改變結果？還是現在的證明就夠了？
