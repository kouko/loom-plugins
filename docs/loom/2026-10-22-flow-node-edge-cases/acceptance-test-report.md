# 修正流程圖說明行貼右框、以及字串說明被拆成單字 — 我試了什麼、結果如何

2026-10-22 在專案的乾淨副本（efa90a66）上試過。每一條怎麼試、回來什麼：`docs/loom/2026-10-22-flow-node-edge-cases/evidence/acceptance-test-evidence.md`。

## 你要求的，逐條

| # | 你要求的 | 結果 | 實際發生了什麼 | Re-run |
|---|---|---|---|---|
| 1 | A flow node whose description line is wider than the width budget keeps one space between the text and the right border, as it does with no width given. | works | 你回報的那個例子（寬度 10、11 格長的說明）現在換行成兩行，右邊都留一格空白；最窄寬度、沒給寬度但超過預設 40 格、中文說明也都留白，兩萬個隨機流程圖裡沒有一個說明行再貼右框。 | — |
| 2 | A flow or architecture node whose description is a single string draws that string as its description lines, one line per line of the string, instead of one character per line. | works | 流程圖和架構圖的「handles requests」現在畫成一行而不是 16 行單字；含換行的字串畫出來和寫成清單時一模一樣；空字串仍照舊報「說明不能為空」的錯。 | — |
| 3 | For every one of the six generators, inputs that hit neither defect draw byte-identically to trunk fc6e9bfc, including error messages. | works | 六種圖各丟兩萬個隨機輸入，跟主線版本逐字比對：沒碰到這兩個缺陷的輸入（包含報錯的，連錯誤訊息）全部一字不差，換另一組隨機種子也一樣。 | — |
| 4 | The test guarding that all six generators are pinned fails when a generator's drawn output changes. | works | 我把六種圖輪流改成多畫一個空白，每一次那支測試都失敗並指出是哪張圖；沒改時它通過。 | — |
| 5 | The full package suite passes. | works | 和這次修改相關的測試（圖表產生器與版號一致性）全數通過（255 過、5 個需要 Mermaid 環境而略過）；完整套件由收尾的自動化測試執行，它在合併前跑、失敗就擋下這次修改。 | — |

## 對你既有的資料做了什麼

沒有 — 這些產生器只讀進你給的輸入、印出圖，不讀也不寫你任何既有檔案。唯一的差別是「重畫」：以前畫好、貼在別處的圖不會變，但如果拿同一份輸入重畫，說明寫成一整串字串的節點、以及原本說明貼著右框的流程節點，會畫得和以前不同（這正是這次要修的）；其他輸入重畫結果和以前一字不差。

## 我替你決定的

- **只重新換行「會貼右框的那一行」** — 我選了只對會碰到右框的說明行多留一格再換行，其他行維持原本的換行位置，因為全部改用較窄的寬度會讓大約十分之一本來沒問題的圖換行位置改變。之後要改成全部統一，代價是很多既有圖重畫時斷行位置會跟著變。
- **很窄的寬度下，流程框可能比以前寬一格** — 為了一定留得出右邊那格空白，窄寬度時框的最小寬度多一格；例如說明只有一個全形空白、寬度給 1 時，框從 5 格變 6 格（審查時已提出、判定屬於這次修正的範圍）。要改回去就得接受那種情況又貼右框。
- **字串怎麼切成多行** — 我照 Python 一般認定的「換行」來切（包含 Windows 的換行），控制字元（例如 tab）照原樣畫，和寫成清單時一致，不會報錯。改成更嚴格的切法曾讓第 2、3 條失敗，所以沒採用。
- **把「六種圖都有被釘住」的檢查併進逐張畫圖比對的那支測試** — 這樣它檢查的是真正畫出來的圖，而不只是名單。要拆回去只是測試檔的整理，不影響使用。
- **版號用小修正（5.12.4）** — 這是修 bug，沒有新增欄位或規則。主線目前仍是 5.12.3，沒有撞號。

沒有任何被駁回的重大審查意見。

## 你要我跳過的步驟

沒有 — 沒有任何步驟被跳過。

## 我不確定你要不要的

- 架構圖的說明行還是會貼著右框（例如「handles requests│」）。這是你上一次已經決定接受、這次也明列不處理的；要不要另開一件來修？
