# 專案可以有一份 agent 必須遵守的 ARCHITECTURE.md — 我試了什麼、結果如何

2026-09-25 在專案的乾淨副本上測試：第一輪在 8b80c9ce，修正後的重測在 21289e5d。每一條怎麼試、回來什麼：`docs/loom/2026-09-25-standing-architecture-doc/evidence/acceptance-test-evidence.md`。

我另外建了用完即丟的小 Python 專案（一個記筆記的 CLI），自己扮演 agent 照新工具的說明一步步做，同時扮演使用者，每一題都選 agent 推薦的選項。重測時沿用同一批專案，另外多建一個「完全沒有設定過測試指令」的專案。

## 你要的東西，一條一條看

| # | 你要的 | 結果 | 發生了什麼 | Re-run |
|---|---|---|---|---|
| 1 | In a repository without ARCHITECTURE.md, a loom-design tool reads the project's requirements and existing code and proposes an architecture covering module split and dependency direction, main technology choices, folder structure and required CI stages, giving at least two options with their trade-offs for each open choice, and the user picks. | works | 照說明先讀 README、intent 和程式碼，四個面向都提了；程式碼已定案的（Python、資料夾佈局）直接說明不重問，其餘每題兩個選項各附優缺點和推薦，由使用者選。 | carried over — 修正只改了參考資料裡 Pylint 預設值的出處說明和「安全掃描費用」的措辭，提案用到的選項和數字都沒變 |
| 2 | The chosen design is written as a user-ratified ARCHITECTURE.md at the repository root holding the design decisions with their reasons and the structural rules, with no project overview and no data models or API interfaces. | works | 檢查工具在使用者同意前拒收、同意後通過；加上「概述」「資料模型」、API 段落、標題下方的說明文字、第二行「同意」紀錄、或空的決策段落，都會被拒收。 | 重測，works |
| 3 | Every rule in that file that can be checked mechanically comes with a guard test that the repository's package suite runs. | works | 在一個原本沒有記錄測試指令的專案裡，照說明先把測試指令記下來、再寫守護測試，並把這份設定和架構文件一起 commit；用記下的指令跑，守護測試有跑到，故意放錯檔案時就失敗。 | 重測，works |
| 4 | When a change breaks a checkable rule, the package suite fails with a message that names the rule, the offending file, and the two ways out: conform to the rule, or change the rule and its guard together. | works | 故意放錯一個檔案、加一個禁止的 import，測試失敗，訊息寫出規則編號、出事的檔案，以及「照規則改」或「規則和守護測試一起改」兩條路。 | carried over — 修正只把失敗訊息的寫法改成指向格式說明裡的同一段，那一段文字沒變；重測第 3 條時也順便再看到同樣的訊息 |
| 5 | When ARCHITECTURE.md exists, the plan for a change that adds or moves files places them by its rules and names the rule it followed. | works | 以 planner 身分讀新的規劃說明：先讀 ARCHITECTURE.md、照規則放新檔、在任務的風險欄寫規則編號；需要破例時由 planner 在開工前和你一起改規則，並把架構文件和守護測試列進該任務要動的檔案，實作者不能自己改規則。我沒有跑一次完整的規劃流程。 | 重測，works |
| 6 | When ARCHITECTURE.md exists, closing review reports whether the change conforms to it, and a violation is a finding that sends the change back; this uses the existing reviewers, with no reviewer added. | works | 審查清單的這一項現在寫明「違反規則至少算重要」，而審查流程會把每一個「重要」以上的問題送回實作階段修；reviewer 數量的程式完全沒動。我沒有真的跑一次含違規的審查。 | 重測，works（上次 partly） |
| 7 | When ARCHITECTURE.md is absent, every change shows a warning line alongside the existing standing-document warnings, never blocks, and the existing waiver silences it; review scores that conformance check as not applicable. | works | 沒有這份檔案時警告會點名它、不擋；第二行警告改成中性的「沒有它就無法拿它來檢查變更」；寫上既有的豁免設定就安靜；三份都在時不出聲；審查說明寫明此時該項記為不適用。 | 重測，works |
| 8 | When a change alters the structure, the same tool re-designs the affected part and updates its design decisions, rules and guards together. | works | 第一輪已模擬新增模組：同一個 commit 裡新增決策、規則和守護測試。重測時確認重新同意是「換掉原本那一行」會通過，留下兩行則被拒收；專案的測試仍全數通過。 | 重測，works |

這幾條相關的自動測試我在乾淨副本上跑過，全數通過。整套自動測試會在變更被接受前再跑一次，失敗就會擋下。

## 對你既有的資料做了什麼

沒有——它只動到這次變更自己建立的檔案。這次的測試全在暫存資料夾裡的丟棄專案中進行。

## 我替你決定的事

- **扮演使用者時，每一題都選 agent 推薦的選項** —— 這樣才能在沒有你的情況下走完整個流程。代價：沒有測到「使用者選了非推薦選項」的路徑。
- **第 6 條這次判為 works** —— 說明現在明訂違規至少算「重要」，而「重要」一定會被送回修。不過主流程仍可以帶理由駁回一個「重要」問題（駁回會公開列出），這是所有審查項目共用的規則，不是這次新增的。
- **另一位審查者提出、被主流程駁回的兩點**（照規定記在這裡）：
  - 檢查工具把 ARCHITECTURE.md 所在的資料夾當成專案根目錄，所以放在 `docs/` 底下的檔案也能通過檢查。駁回理由：工具說明規定寫在根目錄，而且只要根目錄沒有這份檔案，每次變更的警告仍會點名它。
  - 規則段落可以是空的也能通過。駁回理由：不是每個專案四類規則都用得到；空的「決策」段落則已改成會被拒收。我重測時確認兩者都是這樣運作。

## 我不確定你要不要的地方

- 重新設計後如果忘了重新取得你的同意（例如改了規則卻沒換掉同意那一行的日期），目前仍沒有機制會發現，只靠 agent 照說明做。這樣可以嗎？
- 檢查工具只確認守護測試的檔案存在，不確認記下的測試指令真的會跑到它；這一點靠 agent 照說明做。
