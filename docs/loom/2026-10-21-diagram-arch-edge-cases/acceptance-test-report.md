# 修正分層架構圖提早換行與空名稱的邊界問題 — 我試了什麼、結果如何

2026-10-21 在專案的乾淨副本（3f44b26f）上試，並和改動前的主線（5e850c70）逐一對照。每一條怎麼試、回來什麼：`docs/loom/2026-10-21-diagram-arch-edge-cases/evidence/acceptance-test-evidence.md`。

## 你要的，逐條對照

| # | 你要的 | 結果 | 實際發生 | Re-run |
|---|---|---|---|---|
| 1 | A layered-architecture layer whose description line is its widest line shows that line unbroken, in a box whose borders line up, whenever no width budget forces it narrower. | works | 「handles requests」和一行中文說明現在都留在同一行、框線對齊；主線會把它們拆成兩行；寬度上限比說明還窄時仍照常換行。 | — |
| 2 | A layer with an empty single-line name and no components draws a box whose borders line up. | works | 空名稱、無元件的層畫出三格寬、每行等寬的框；主線最後一行會多一格。 | — |
| 3 | A layer with an empty title and at least one description line draws a box whose borders line up instead of raising an error, at any width budget. | works | 主線會報錯不出圖的五種寫法（含寬度 1、寬度 0、空說明行）現在都畫出對齊的框；原本就能畫的寬度輸出完全沒變。 | — |
| 4 | For inputs that hit none of the three defects, every diagram generator's output and error messages are byte-identical to trunk before this change. | works | 6,000 筆隨機輸入對照主線：表格、流程、樹、長條、時序圖全部一字不差；架構圖有差的 327 筆全都屬於這三個缺陷，錯誤訊息也都和主線相同。 | — |
| 5 | The package suite pins the exact trunk output of unaffected inputs for every diagram generator, and the hang-guarded rendering in the generator tests goes through one shared helper. | works | 六種圖各有兩筆主線輸出被測試釘住，拿去跑主線程式也全部通過；原本兩個幾乎重複的防卡死輔助函式已合成一個。 | — |
| 6 | The complete package suite passes. | works | 這次改動相關的 79 項測試都通過；完整測試套件會在接受改動前自動執行，失敗就會擋下。 | — |

## 對你既有的資料做了什麼

沒有——這個改動只改變畫圖時輸出的文字，不讀也不寫你已有的任何檔案或資料。

## 我替你決定的

- **說明行剛好最寬時，文字貼齊右框** — 我（實作端）讓框的寬度剛好容納「前導空格＋說明文字」，所以最寬那行右邊沒有留白（例如 `│ handles requests│`）。原因是這樣不改變其他輸入的輸出。日後想在右邊留一格空白，所有含說明行的架構圖寬度都會變，要重寫一批測試。
- **寬度上限比說明還窄時仍換行；用換行字串寫的名稱則不受寬度上限限制** — 這跟主線行為一致，只修你點名的問題。日後若要讓字串名稱也受寬度上限，是另一個改動。
- **只有「零寬度記號」（例如單獨一個重音符號）的名稱或標題，視同空的** — 所以它也照第 2、3 條畫出對齊的框，而主線是歪的或報錯。如果你希望它被當成有內容的名稱處理，要再調整。
- **把對抗測試留下的一支「行尾空格說明行」檢查併入正式測試** — 讓它以後每次都跑；不影響你看到的行為。
- **版號只升小修（5.12.3）** — 這是錯誤修正，沒有新增參數或規則。

（「空標題在任何寬度都要畫出來」是你在 2026-10-21 選的 A 方案，不列在這裡。沒有任何 important 以上的審查意見被駁回。）

## 你要我跳過的步驟

沒有——沒有步驟被跳過。

## 我不確定你要不要的

- 說明行最寬時文字緊貼右框、沒有留白（見上），你覺得可以接受嗎？
- 標題為空、而且一行說明都沒有的層，現在和主線一樣仍會報錯「Body cannot be empty」；這不在這次範圍內，要不要另開一件處理？
