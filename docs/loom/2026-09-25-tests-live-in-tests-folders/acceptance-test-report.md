# 每個測試都住進 tests 資料夾 — 我試了什麼、結果如何

2026-09-25 在專案的乾淨副本（b560fb23）上試過，另開一份改動前（23dad634）的乾淨副本當對照組，再開第三份副本專門放丟棄式的測試。每一條怎麼試、回來什麼：`docs/loom/2026-09-25-tests-live-in-tests-folders/evidence/acceptance-test-evidence.md`。

## 你要的東西，一條一條

| # | 你要的 | 結果 | 發生了什麼 | Re-run |
|---|---|---|---|---|
| 1 | Outside `docs/loom/`, every test file in the repository is under a plugin's `tests/` folder (that plugin's tests) or the root `tests/` folder (repository-level tests); none remains beside production code or inside a skill folder. | works | 現在 242 個測試檔全部在某個 tests 資料夾裡，一個都不在工具程式旁邊或 skill 資料夾裡；改動前有 216 個散在外面，每一個都找得到搬去的新位置，多出的 4 個是新加的防回歸測試。 | — |
| 2 | The package suite collects and passes the same tests it collected before the move, plus the skill probe tests it did not collect before, with none lost; the before and after counts per plugin are recorded. | works | 我用改動前後各自的測試清單逐一比對：改動前 3574 個、改動後 3627 個，一個都沒少；多出的 53 個正好是以前沒被跑到的 24 個（23 個 skill 探針加 1 個 manifest 測試）和 29 個新的防回歸測試，和記錄的前後數字一致。完整 test suite 在乾淨副本跑一次全過；其中 5 個畫圖檢查在全新副本裡會「跳過」而不是「通過」，因為它需要的套件在同一輪稍後才安裝——改動前也一模一樣，不是這次造成的。這份完整 suite 也會在變更被接受前再跑一次，失敗就擋下。 | — |
| 3 | A test added later anywhere under a `tests/` folder is run by the package suite without editing the suite command, and CI runs the same tests; the one exception is a `tests/local/` folder, which holds tests that need a locally installed CLI and is named as local-only. | partly | Python 測試做到了：我在各個 tests 資料夾底下新開子資料夾放測試，沒改指令就被跑到；放在四個 `tests/local/` 的都被跳過；CI 的三個 workflow 合起來涵蓋全部五組測試，改到任何 tests 資料夾都會觸發。但 shell 測試沒做到：只有放在 loom-workflow tests 資料夾最上層的才會跑，放在 loom-code 的 tests 資料夾或 loom-workflow tests 的子資料夾就靜靜地不跑——這正是這次要消除的「測試悄悄沒在跑」，而且 repo 自己的規則檢查還明說那種位置是允許的。 | — |
| 4 | The repository's contributor guidance states where tests go, and every document an agent reads at run time names the new locations. | works | 貢獻指南新增了一節，寫明測試放哪、`tests/local/` 會被跳過、新增測試不用改指令；agent 執行時會讀的文件裡，搜尋所有舊測試路徑（434 種寫法）一筆都沒有，同樣的搜尋在改動前的副本有 467 筆，證明搜尋本身有效。 | — |
| 5 | The checker's rule list does not grow and no new step, reviewer or dispatch is added. | works | checker 規則仍是 26 條、清單和改動前一字不差；機制總數仍是 140、檢查結果「all clear」；流程文字的改動只有路徑替換，沒有新步驟、reviewer 或派工。 | — |

## 對你既有的資料做了什麼

沒有 — 這個變更只搬動了 repo 裡的測試檔、更新了測試清單、CI 設定和文件，不讀也不改你既有的任何檔案或資料。

## 我替你決定的事

- **用 clean clone 驗證，而不是實際啟動 Claude 試跑** — 這次只搬測試、不改任何 skill 的行為，所以照派工要求直接在乾淨副本跑測試清單和完整 suite。
- **「一樣的測試」用「檔名＋測試名稱」比對** — 搬家會改資料夾、不會改檔名和測試名稱，所以用這組當身分證比對前後；若同名檔在兩個 plugin 間互換，這個比法看不出來（這次沒有這種情形的跡象）。
- **skill 的 test-prompts.json 不算測試檔** — 它們是 skill 觸發測試用的提示詞資料，不是可執行的測試，所以留在 skill 資料夾裡我沒算成違規。
- **一支既有測試的比對被放寬了** — 檢查「畢業探針和原始證據逐字相同」的那支測試，現在會跳過比對自己，並容許一行路徑設定不同；實作方記錄這是搬家必須的決定（2026-09-25）。你的限制是「不改任何測試的判斷」，這一處嚴格說是例外；要收回就得另找方式讓搬過去的那份仍能逐字比對。
- 沒有收到任何被駁回的 important 以上 finding。

## 我不確定你要不要的事

- shell 測試目前只在 loom-workflow tests 資料夾最上層才會被自動跑到。要把自動探索也擴到其他 tests 資料夾的 shell 測試，還是在指南裡明寫「shell 測試只能放那裡」並讓規則檢查擋掉其他位置？
- 將來若新增第四個 plugin，它的 tests 資料夾不會自動被跑，要加一組才會。這樣可以接受嗎？
- 那 5 個畫圖檢查在全新環境會跳過而不是真的跑。要不要讓安裝步驟排在它們之前，讓它們在 CI 上真的執行？
