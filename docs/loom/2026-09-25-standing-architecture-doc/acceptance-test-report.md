# 專案可以有一份 agent 必須遵守的 ARCHITECTURE.md — 我試了什麼、結果如何

2026-09-25 在專案的乾淨副本（8b80c9ce）上測試。每一條怎麼試、回來什麼：`docs/loom/2026-09-25-standing-architecture-doc/evidence/acceptance-test-evidence.md`。

我另外建了一個用完即丟的小 Python 專案（一個記筆記的 CLI），自己扮演 agent 照新工具的說明一步步做，同時扮演使用者，每一題都選 agent 推薦的選項。

## 你要的東西，一條一條看

| # | 你要的 | 結果 | 發生了什麼 | Re-run |
|---|---|---|---|---|
| 1 | In a repository without ARCHITECTURE.md, a loom-design tool reads the project's requirements and existing code and proposes an architecture covering module split and dependency direction, main technology choices, folder structure and required CI stages, giving at least two options with their trade-offs for each open choice, and the user picks. | works | 照說明先讀 README、intent 和程式碼，四個面向都提了；程式碼已定案的（Python、資料夾佈局）直接說明不重問，其餘每題兩個選項各附優缺點和推薦，由使用者選。 | — |
| 2 | The chosen design is written as a user-ratified ARCHITECTURE.md at the repository root holding the design decisions with their reasons and the structural rules, with no project overview and no data models or API interfaces. | works | 寫出的檔案只有決策（含理由）和四類規則；檢查工具在使用者同意前拒收，同意後通過，加上「概述」「資料模型」或 API 段落都會被拒收。 | — |
| 3 | Every rule in that file that can be checked mechanically comes with a guard test that the repository's package suite runs. | works | 三條可機械檢查的規則各有一支守護測試，專案本來的測試指令就會跑到；需要判斷的那條標為交給 reviewer。 | — |
| 4 | When a change breaks a checkable rule, the package suite fails with a message that names the rule, the offending file, and the two ways out: conform to the rule, or change the rule and its guard together. | works | 故意放錯一個檔案、加一個禁止的 import，測試失敗，訊息寫出規則編號、出事的檔案，以及「照規則改」或「規則和守護測試一起改」兩條路。 | — |
| 5 | When ARCHITECTURE.md exists, the plan for a change that adds or moves files places them by its rules and names the rule it followed. | works | 以 planner 身分讀新的規劃說明：它要求先讀 ARCHITECTURE.md，照規則放新檔，並在該任務的風險欄寫上規則編號；我沒有跑一次完整的規劃流程。 | — |
| 6 | When ARCHITECTURE.md exists, closing review reports whether the change conforms to it, and a violation is a finding that sends the change back; this uses the existing reviewers, with no reviewer added. | partly | 審查清單多了「是否符合 ARCHITECTURE.md」這一項，reviewer 數量的程式完全沒動；但說明沒有規定違規至少算「重要」，reviewer 若判成小問題，變更就會直接通過、不會被退回。 | — |
| 7 | When ARCHITECTURE.md is absent, every change shows a warning line alongside the existing standing-document warnings, never blocks, and the existing waiver silences it; review scores that conformance check as not applicable. | works | 沒有這份檔案時警告會點名它、不擋；寫上既有的豁免設定就安靜；檔案放在根目錄就不再點名；審查說明寫明此時該項記為不適用。 | — |
| 8 | When a change alters the structure, the same tool re-designs the affected part and updates its design decisions, rules and guards together. | works | 模擬新增一個模組：同一個 commit 裡新增一條決策、一條規則和對應的守護測試，檢查工具通過，故意違反新規則時測試會失敗。 | — |

Package suite 的相關測試我跑過且全數通過；整套自動測試我也照站方要求跑了一次，全數通過。整套測試在變更被接受前還會再跑一次，失敗就會擋下。

## 對你既有的資料做了什麼

沒有——它只動到這次變更自己建立的檔案。這次的測試全在暫存資料夾裡的丟棄專案中進行。

## 我替你決定的事

- **扮演使用者時，每一題都選 agent 推薦的選項** —— 這樣才能在沒有你的情況下走完整個流程。代價：沒有測到「使用者選了非推薦選項」的路徑。
- **第 6 條判為 partly 而非 works** —— 你的原意是「違規就退回」，但目前的說明把輕重交給 reviewer 判斷。如果你接受「輕微的違規可以只記下不退回」，這條可以視為 works。

## 我不確定你要不要的地方

- 違反 ARCHITECTURE.md 的規則，是不是一律要退回重改？如果是，審查說明要補一句「違規至少算重要」。
- 只缺 ARCHITECTURE.md 時，警告的第二行寫的是「無法檢查變更是否符合這個產品應有的樣子」，用在架構文件上有點不貼切，要不要改寫？
- 重新設計後如果忘了重新取得你的同意，目前沒有任何機制會發現，只靠 agent 照說明做。這樣可以嗎？
