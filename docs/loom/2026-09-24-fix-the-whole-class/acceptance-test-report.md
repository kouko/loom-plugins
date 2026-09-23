# 修正一次補齊同類缺陷 — 我試了什麼、結果如何

2026-09-24 在專案的乾淨副本（706ea36b）上試過。每一條怎麼試、回來什麼：`docs/loom/2026-09-24-fix-the-whole-class/evidence/acceptance-test-evidence.md`。

## 你要的東西，一條一條

| # | 你要的 | 結果 | 發生了什麼 | Re-run |
|---|---|---|---|---|
| 1 | Before a fix is handed to an implementer, the orchestrator names the defect's class and searches the whole change for other instances of it — including every surface named by the Acceptance line the finding maps to — and the fix hand-off lists every instance found, the flagged one included. | works | 覆蓋這條的測試全數通過；四次實際試跑中，交給 implementer 的交接內容每次都寫出缺陷類別、找過哪些地方，並列出所有同類位置（含被點名的那一處）。完整的 automated test suite 會在變更被接受前執行，失敗就會擋下。 | — |
| 2 | The fix's record (its hand-off and commit message) states the class and the places searched, so a reader can see siblings were looked for even when none were found. | works | 覆蓋這條的測試全數通過（含「只找到被點名那一處時也要寫」）；四次試跑的交接都寫了類別與搜尋範圍，也都要求 commit message 照寫。沒有實際做出 commit，也沒有試「一個兄弟都沒有」的案例，這兩點只靠規則文字與測試。完整 automated test suite 會在接受前執行並在失敗時擋下。 | — |
| 3 | Given a finding that names one instance while siblings of the same defect exist elsewhere in the change, an agent following the station text produces a fix hand-off that covers the siblings, shown by a trial run on such a case. | works | 用新版規則跑兩個案例、各兩次，四次都把三處同類缺陷全部納入交接；在舊版（main）上跑的對照組，較難的案例兩次都只修被點名的一處，另外兩處被明講「留著、另外處理」。 | — |
| 4 | The rule is carried by station prose; the checker's rule list does not grow and no new step, reviewer or dispatch is added. | works | checker 規則仍是 26 條，與 main 相同；閘門計數與 main 一樣、沒有增加；新增的文字裡沒有閘門標記，也沒有新的步驟、reviewer 或派工。相關測試通過，完整 automated test suite 會在接受前執行並在失敗時擋下。 | — |

**試跑細節（第 3 條）**：我做了兩個小專案，每個都有一個分支在三個地方犯了同一種錯（把使用者輸入直接拼進資料庫查詢，也就是 SQL injection），而 review 意見只點名其中一處。

- 簡單案例：三處都在被點名那條 Acceptance 講到的功能裡。新版兩次都涵蓋三處，舊版兩次**也**涵蓋三處；差別在新版有明寫「缺陷類別」與「找過哪些地方」，舊版沒有。
- 困難案例：另外兩處屬於別的 Acceptance（稽核紀錄、商品搜尋）。新版兩次都涵蓋三處；舊版兩次都只交接一處。這個案例才真正看得出規則的作用。
- 八次試跑都沒有去動變更範圍外、既有的舊程式碼，也都沒有修改任何檔案。

## 對你既有的資料做了什麼

沒有 — 這個變更只改了工具遵循的說明文字、一支測試和版號，不讀也不改你既有的任何檔案或資料。

## 我替你決定的事

- **怎麼載入尚未發布的分支版本** — README 的安裝方式只會裝到已發布的 main，所以我改用 Claude Code 從本機資料夾載入 plugin 的方式，並確認實際載入的是分支版（3.12.0）。之後改用正式安裝方式時結果應相同，但這次沒有驗證。
- **多加了一個較難的案例和對照組** — 你只要求跑兩次；因為簡單案例裡新舊版表現一樣，我加跑困難案例、新舊版各兩次，才能看出差異。多花大約 2 美元。
- **規則只寫在一個地方，其他站只放一句指引**，以及**版號升 minor** — 計畫裡標為 agent 自行決定。之後要改成各站各寫一份，就得維護多份一致的文字。
- 沒有收到任何被駁回的 important 以上 finding。

## 我不確定你要不要的事

沒有。
