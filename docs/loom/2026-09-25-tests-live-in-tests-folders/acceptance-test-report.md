# 每個測試都住進 tests 資料夾 — 我試了什麼、結果如何

第一輪 2026-09-25 在專案的乾淨副本（b560fb23）上試過，另開一份改動前（23dad634）的乾淨副本當對照組，再開一份副本專門放丟棄式的測試；修正（讓 shell 測試在每個 test root 都會跑、規則檢查只允許這四個 root）後，在新的乾淨副本（277a1c0f）上把五條全部重試一次；第二次修正（shell 測試不再跑到 tests 資料夾裡另一份 repo 副本的測試）後，在乾淨副本（fdddb2ca）上重試第 2、3 條。每一條怎麼試、回來什麼：`docs/loom/2026-09-25-tests-live-in-tests-folders/evidence/acceptance-test-evidence.md`。

## 你要的東西，一條一條

| # | 你要的 | 結果 | 發生了什麼 | Re-run |
|---|---|---|---|---|
| 1 | Outside `docs/loom/`, every test file in the repository is under a plugin's `tests/` folder (that plugin's tests) or the root `tests/` folder (repository-level tests); none remains beside production code or inside a skill folder. | works | 修正後重數：239 個測試檔全部在四個 tests 資料夾（root 和三個 plugin 各一）裡，沒有一個在工具程式旁邊或 skill 資料夾裡；改動前散在外面的 216 個都找得到新位置，只多出 1 個新的防回歸測試檔（修正時刪掉了 3 個重複的）。 | carried over — 第二次修正沒有搬動或新增任何測試檔，只在既有的測試檔裡加了一個測試 |
| 2 | The package suite collects and passes the same tests it collected before the move, plus the skill probe tests it did not collect before, with none lost; the before and after counts per plugin are recorded. | works | 第二次修正後重新逐一比對：改動前 3574 個、現在 3639 個，一個都沒少；多出的 65 個是以前沒被跑到的 24 個（23 個 skill 探針加 1 個 manifest 測試）和 41 個新的防回歸測試，和更新後的前後數字記錄完全一致。完整 test suite 在乾淨副本跑一次全過；5 個畫圖檢查在全新副本裡仍是「跳過」，原因和改動前一樣是它需要的套件在同一輪稍後才裝，不是這次造成的。這份完整 suite 也會在變更被接受前再跑一次，失敗就擋下。 | re-tested |
| 3 | A test added later anywhere under a `tests/` folder is run by the package suite without editing the suite command, and CI runs the same tests; the one exception is a `tests/local/` folder, which holds tests that need a locally installed CLI and is named as local-only. | works | 第二次修正後重試：在 tests 資料夾裡放了三份另一個 repo 的副本（兩個 git worktree，其中一個被 ignore 隱藏，加一個獨立的 clone），裡面的 shell 測試一個都沒被跑到；同一棵樹用修正前的版本會誤跑 46 個。一般位置新放的 shell 測試照樣會跑；上一輪確認過的 Python 測試、`tests/local/` 跳過、放錯位置被規則檢查擋下和 CI 設定，這次修正都沒動到。 | re-tested |
| 4 | The repository's contributor guidance states where tests go, and every document an agent reads at run time names the new locations. | works | 貢獻指南現在寫明：suite 只跑四個 test root 和它們的子資料夾，Python 和 shell 測試都自動找到，新增測試不用改指令，`tests/local/` 會被跳過；新增一個 plugin 則要把它的 tests 資料夾加進清單才會跑——我重試時實際看到的行為就是這樣。agent 執行時會讀的文件裡，搜尋所有舊測試路徑一筆都沒有（同樣的搜尋在改動前有 467 筆）；修正也把記憶條目裡舊的測試指令改成新的。 | carried over — 第二次修正沒有改貢獻指南或任何 agent 會讀的文件；指南說的「四個 root 裡的 shell 測試會自動跑」仍與第 3 條重試所見一致 |
| 5 | The checker's rule list does not grow and no new step, reviewer or dispatch is added. | works | 修正後重跑：checker 規則仍是 26 條、清單和改動前一字不差；機制總數仍是 140、「all clear」；修正沒有動到任何 skill、agent 或流程文字。 | carried over — 第二次修正只改測試清單程式、一支測試、數字記錄和 CHANGELOG，沒有動 checker 規則或任何流程文字 |

## 對你既有的資料做了什麼

沒有 — 這個變更只搬動了 repo 裡的測試檔、更新了測試清單、CI 設定、文件和幾則記憶條目，不讀也不改你既有的任何檔案或資料。

## 我替你決定的事

- **用 clean clone 驗證，而不是實際啟動 Claude 試跑** — 這次只搬測試、不改任何 skill 的行為，所以照派工要求直接在乾淨副本跑測試清單和完整 suite。
- **「一樣的測試」用「檔名＋測試名稱」比對** — 搬家會改資料夾、不會改檔名和測試名稱，所以用這組當身分證比對前後；若同名檔在兩個 plugin 間互換，這個比法看不出來（這次沒有這種情形的跡象）。
- **skill 的 test-prompts.json 不算測試檔** — 它們是 skill 觸發測試用的提示詞資料，不是可執行的測試，所以留在 skill 資料夾裡我沒算成違規。
- **修正後五條全部重試** — 這次修正動到測試清單、規則檢查、指南和 CI，五條都可能受影響，所以沒有沿用任何上一輪的結果。
- **一支既有測試仍跳過比對自己** — 檢查「畢業探針和原始證據逐字相同」的那支測試，修正後對其他檔案恢復逐字比對，但仍跳過它自己（它搬家時必須改一行路徑）。實作方記錄這是搬家必須的決定（2026-09-25）。你的限制是「不改任何測試的判斷」，這一處嚴格說仍是小例外。
- 沒有收到任何被駁回的 important 以上 finding。

## 我不確定你要不要的事

- 將來新增第四個 plugin 時，要記得把它的 tests 資料夾加進清單，否則它的測試不會跑（規則檢查會擋下提醒）。這樣可以接受嗎？
- 那 5 個畫圖檢查在全新環境會跳過而不是真的跑。要不要讓安裝步驟排在它們之前，讓它們在 CI 上真的執行？
