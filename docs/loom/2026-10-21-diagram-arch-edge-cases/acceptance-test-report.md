# 修正分層架構圖提早換行與空名稱的邊界問題 — 我試了什麼、結果如何

2026-10-21 在專案的乾淨副本（3f44b26f）上試，並和改動前的主線（5e850c70）逐一對照；審查意見後，同日在新的乾淨副本（0fd51596）上重測第 1、6 條。這段期間的修正只改了計畫文件的一句話，沒有動程式或測試，所以第 2–5 條沿用前次結果。每一條怎麼試、回來什麼：`docs/loom/2026-10-21-diagram-arch-edge-cases/evidence/acceptance-test-evidence.md`。

## 你要的，逐條對照

| # | 你要的 | 結果 | 實際發生 | Re-run |
|---|---|---|---|---|
| 1 | A layered-architecture layer whose description line is its widest line shows that line unbroken, in a box whose borders line up, whenever no width budget forces it narrower. | works | 「handles requests」和一行中文說明現在都留在同一行、框線對齊；主線會把它們拆成兩行；寬度上限比說明還窄時仍照常換行。注意：你沒有指定寬度時，程式會自動套用 40 格的預設上限，所以一行 40 格以上的說明照樣會被拆開（例如 40 個字母會變成 39 個加上單獨一個掉到下一行），這和主線一樣；39 格以內的說明現在不再被拆，主線在 39 格時就會拆。要畫更長的說明行不斷行，得自己指定更大的寬度。 | 重測：同上各例重跑，另加 39 格、40 格說明行和寬度 60 的例子 |
| 2 | A layer with an empty single-line name and no components draws a box whose borders line up. | works | 空名稱、無元件的層畫出三格寬、每行等寬的框；主線最後一行會多一格。 | carried over — 修正只改計畫文件，沒動程式或測試 |
| 3 | A layer with an empty title and at least one description line draws a box whose borders line up instead of raising an error, at any width budget. | works | 主線會報錯不出圖的五種寫法（含寬度 1、寬度 0、空說明行）現在都畫出對齊的框；原本就能畫的寬度輸出完全沒變。 | carried over — 修正只改計畫文件，沒動程式或測試 |
| 4 | For inputs that hit none of the three defects, every diagram generator's output and error messages are byte-identical to trunk before this change. | works | 6,000 筆隨機輸入對照主線：表格、流程、樹、長條、時序圖全部一字不差；架構圖有差的 327 筆全都屬於這三個缺陷，錯誤訊息也都和主線相同。 | carried over — 修正只改計畫文件，沒動程式或測試 |
| 5 | The package suite pins the exact trunk output of unaffected inputs for every diagram generator, and the hang-guarded rendering in the generator tests goes through one shared helper. | works | 六種圖各有兩筆主線輸出被測試釘住，拿去跑主線程式也全部通過；原本兩個幾乎重複的防卡死輔助函式已合成一個。 | carried over — 修正只改計畫文件，沒動程式或測試 |
| 6 | The complete package suite passes. | works | 依流程紀錄，完整測試套件在 Build 階段（3f44b26f）已全部通過（這次我沒有親自跑完整套件）；接受改動前它會再自動跑一次，失敗就會擋下。這份報告自己跑的是涵蓋這次改動的 79 項測試，全部通過。 | 重測：79 項測試在 0fd51596 上重跑，全部通過 |

## 對你既有的資料做了什麼

沒有——這個改動只改變畫圖時輸出的文字，不讀也不寫你已有的任何檔案或資料。

## 我替你決定的

- **說明行剛好最寬時，文字貼齊右框** — 我（實作端）讓框的寬度剛好容納「前導空格＋說明文字」，所以最寬那行右邊沒有留白（例如 `│ handles requests│`）。原因是這樣不改變其他輸入的輸出。日後想在右邊留一格空白，所有含說明行的架構圖寬度都會變，要重寫一批測試。
- **寬度上限比說明還窄時仍換行；用換行字串寫的名稱則不受寬度上限限制** — 這跟主線行為一致，只修你點名的問題。日後若要讓字串名稱也受寬度上限，是另一個改動。
- **沒指定寬度時，仍沿用 40 格的預設上限** — 所以「沒有寬度限制」其實是「上限 40 格」：40 格以上的說明行照樣換行，和主線一樣；只有 39 格以內的說明行這次不再被拆。我沒有拿掉這個預設，因為拿掉會讓所有沒指定寬度的長說明圖變寬、輸出和主線不同。如果你要「沒指定寬度就完全不換行」，那是另一個改動。
- **同一張圖裡所有層共用同一個框寬** — 所以某一層的說明行不再被拆、框變寬時，其他沒受影響的層也會跟著變寬一格以上（例如和「API／handles requests」放在同一張圖的「Web」層，框從 18 格變 19 格）。這是原本就有的「各層對齊」設計，不是新行為，但你會看到沒問題的層也變寬了。
- **只有「零寬度記號」（例如單獨一個重音符號）的名稱或標題，視同空的** — 所以它也照第 2、3 條畫出對齊的框，而主線是歪的或報錯。如果你希望它被當成有內容的名稱處理，要再調整。
- **把對抗測試留下的一支「行尾空格說明行」檢查併入正式測試** — 讓它以後每次都跑；不影響你看到的行為。
- **版號只升小修（5.12.3）** — 這是錯誤修正，沒有新增參數或規則。

（「空標題在任何寬度都要畫出來」是你在 2026-10-21 選的 A 方案，不列在這裡。沒有任何 important 以上的審查意見被駁回。）

## 你要我跳過的步驟

沒有——沒有步驟被跳過。

## 我不確定你要不要的

- 說明行最寬時文字緊貼右框、沒有留白（見上），你覺得可以接受嗎？
- 標題為空、而且一行說明都沒有的層，現在和主線一樣仍會報錯「Body cannot be empty」；這不在這次範圍內，要不要另開一件處理？
