# 修正前先把所有阻擋問題收齊、依缺陷類別分組 — 我試了什麼、結果如何

2026-09-24 在專案的乾淨副本（3e03f4e7）上試過。每一條怎麼試、回來什麼：`docs/loom/2026-09-24-fix-closing-review-handoff/evidence/acceptance-test-evidence.md`。

## 你要的東西，一條一條

| # | 你要的 | 結果 | 發生了什麼 | Re-run |
|---|---|---|---|---|
| 1 | Before a fix round starts, every fatal or important finding from the reviewers and from independent acceptance testing on the current version is collected into one list, and no fix begins from a subset of it. | works | 覆蓋這條的測試全數通過；五次實際試跑都把兩位 reviewer 和 acceptance tester 的 important 問題收進同一張清單（nit 排除），並說明所有交接都在同一輪修正裡送出、reviewer 回來之前送完。完整的 automated test suite 會在變更被接受前執行，失敗就會擋下。 | — |
| 2 | Findings in that list that share a defect class, named in words from the findings themselves and not from the recorded verdict label, reach Build as one hand-off that names all of their instances. | works | 覆蓋這條的測試全數通過；五次試跑都把「使用者給的檔名沒檢查就接到資料夾路徑上」這兩處合成一份交接、兩處都列出，類別名稱取自問題描述本身，沒有人拿 `NEEDS_REVISION` 當類別。完整 automated test suite 會在接受前執行並在失敗時擋下。 | — |
| 3 | The station text states that the per-verdict failure record kept for the pull request is disclosure only and is not the input a fix is scoped from. | works | 規則文字明寫「逐一記錄的 verdict 失敗只是給 pull request 的揭露，修正範圍從清單來」，原本那句記錄指令一字未改，對應測試通過；五次新版試跑都照這樣說，舊版五次都沒有。 | — |
| 4 | Given a seeded case with two reviewer findings and one acceptance-testing finding, two of which share a defect class, an agent following the station text produces one hand-off for the shared class and a separate one for the other, shown by a trial run. | works | 用新版跑了五次（兩種案例），五次都是「同類的一份、另一個單獨一份」共兩份交接；舊版對照組五次裡四次也這樣做，一次把三個問題併成一份。 | — |
| 5 | The rule is carried by station prose; the checker's rule list does not grow and no new step, reviewer or dispatch is added. | works | checker 規則仍是 26 條，與改動前相同；閘門計數與改動前一樣是 140；新增的只是一段沒有閘門標記的說明文字，沒有新步驟、reviewer 或派工。相關測試通過，完整 automated test suite 會在接受前執行並在失敗時擋下。 | — |

**試跑細節（第 1–4 條）**：我做了一個小專案，分支加了三個功能（匯出筆記、下載附件、分頁）。兩位 reviewer 都回 `NEEDS_REVISION`：一位指出匯出檔名可以跳出使用者的資料夾，另一位指出分頁少算最後一頁；acceptance tester 指出附件名稱可以讀到資料夾外的檔案。其中「跳出資料夾」兩則是同一類、來源不同，分頁是另一類；兩位 reviewer 的標籤相同，按標籤分組就會分錯。

- 案例 A：三方結果一起給。新版三次、舊版三次。
- 案例 B：acceptance tester 的結果「稍早」先到、用不同編號，reviewer 的結果後到。新版兩次、舊版兩次。
- 每一次都確認真的載入了負責收尾審查的那個 skill，且載入的是對應版本（新版 3.13.0、舊版 3.12.0）。
- 十次都沒有改任何檔案，範圍外那支既有的舊程式（有同樣的寫法）也都被明確排除、沒有動到。

**老實說**：這個案例對舊版也不難——舊版五次裡四次自己就分對了、五次都有收進 tester 的問題。新版看得出的差別是：分組五次全對（舊版漏一次），以及每次都講明「失敗記錄只是揭露、不決定修什麼」（舊版一次都沒講）。它證明 agent 會照新規則做，但沒能證明在這種案例下它大幅改變結果。

## 對你既有的資料做了什麼

沒有 — 這個變更只改了工具遵循的說明文字、一支測試和版號，不讀也不改你既有的任何檔案或資料。

## 我替你決定的事

- **怎麼載入尚未發布的分支版本** — README 的安裝方式只會裝到已發布的 main，所以我改用 Claude Code 從本機資料夾載入 plugin 的方式，並確認載入的是分支版（3.13.0）。改用正式安裝方式時結果應相同，但這次沒有驗證。
- **多加一個較難的案例、每邊多跑一次** — 你要求每邊至少兩次；第一個案例新舊版差不多，我加了「tester 結果先到、編號不同」的案例，總共新舊版各五次，約 4.6 美元。
- **新段落不再重複指向修正站的搜尋規則**、**對抗測試的探針併入正式測試**、**版號升 minor** — 計畫裡標為 agent 自行決定。之後若要改，就是改那段文字和那支測試。
- 沒有收到任何被駁回的 important 以上 finding。

## 我不確定你要不要的事

- 舊版在這個案例上大多也能分對。你要不要我再設計一個更難的案例（例如 tester 和 reviewer 的結果分兩輪送達、或同類問題描述用詞差很多），來看新規則是否真的改變結果？還是這次的證明就夠了？
