# 讓各 plugin 的三語 README 重新一致 — 我試了什麼、結果如何

Tried on 2026-11-23, in a clean copy of the project at 954b0b390. How I tried
each line and what came back: `docs/loom/2026-11-20-readme-sync/evidence/acceptance-test-evidence.md`.

## What you asked for, one line at a time

| # | What you asked for | Verdict | What happened | Re-run |
|---|---|---|---|---|
| 1 | loom-code's README.ja.md and README.zh-TW.md carry every section and fact of README.md, translated. | works | 逐段對照三份 README：章節相同、順序相同，英文版 checker 章節的每一項事實（JSON 結果、建議下一步、delivery 欄位、退出碼等）在日文與繁中版都找得到；程式碼區塊與連結數量也一致。 | — |
| 2 | loom-workflow's three READMEs say what an "old map" is (a decision map from before roadmap replaced it) on first use. | works | 三份 README 第一次出現「old map／旧 map／舊 map」時，都緊接著括號說明它是 roadmap 取代前的 decision map。 | — |
| 3 | The complete package suite passes. | works | 在乾淨副本上跑完整測試套件，全部通過、沒有任何失敗（另有 5 項依設計略過）；在接受變更前會再跑一次的自動化測試套件，失敗時會擋下這次變更。 | — |

## 對你既有的資料做了什麼 (what this did to data you already had)

Nothing — it only touched files this change created. 這次只改了說明文件、版本號與變更紀錄，沒有讀寫你任何既有資料。

## I decided for you

- **翻譯版多出的補充說明** — 日文與繁中版在 checker 章節有幾處比英文版多講一點（例如舉了一個參數錯誤的例子、說明版本字串會去掉前後空白）。我判定這不違反「涵蓋英文版每項事實」，所以算 works。若你要求三語逐字等量，這幾處要回頭刪或補進英文版。

沒有被駁回的重要審查意見。

## Steps you told me to skip

- 寫設計規格（spec）這一步 — skipped on your instruction, 2026-11-23.
- 每個任務由獨立實作 agent 執行、並先寫會失敗的測試（implementer 與測試先行）— skipped on your instruction, 2026-11-23.

## Things I am not sure you want

- 翻譯版比英文版多出的那幾句補充說明，要保留，還是三語一律對齊英文版？
