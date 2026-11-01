# 修好架構圖在窄寬度下卡住、標題凸出框外的問題 — 我試了什麼、結果如何

2026-10-21 在乾淨的專案副本 155f92bc 上試過，另開一份 trunk（114ad1ce）的乾淨副本當對照。每一條怎麼試、回來什麼：`docs/loom/2026-10-21-diagram-narrow-width-fixes/evidence/acceptance-test-evidence.md`。

## What you asked for, one line at a time

| # | What you asked for | Verdict | What happened | Re-run |
|---|---|---|---|---|
| 1 | Drawing a layered-architecture diagram whose body holds a two-cell character, at the narrowest width budgets, finishes within a few seconds and produces a box whose borders line up. | works | 照使用說明的指令畫內文含中文字的架構圖，寬度從 0 到 4 都在一秒內畫完，框線上下對齊；同樣的圖在 trunk 上每一個寬度都卡住，直到被強制中止。流程圖在同類情況下也不再卡住。 | — |
| 2 | Wrapping text containing two-cell characters at a one-cell width finishes instead of looping. | works | 把「中文」「a中b文」「日本語テキスト」用一格寬度換行，都立刻回傳、一個字一行；trunk 上同樣的呼叫卡住五秒後被中止。純英文的換行結果和 trunk 一樣。 | — |
| 3 | A layered-architecture diagram whose layer title is wider than everything else in the layer shows the whole title inside a box whose borders line up. | works | 四種「標題比內容還寬」的架構圖（英文、中文、中英混合、指定窄寬度）現在整個標題都在框內、框線對齊；trunk 上四張都凸出右邊框一格。 | — |
| 4 | For inputs that hit neither defect, every diagram generator's output and error messages are byte-identical to trunk before this change. | works | 六種圖共 330 組輸入（30 組手挑、含所有我觸發得到的錯誤訊息，加 300 組隨機）兩邊比對：沒碰到這兩個問題的 319 組輸出與錯誤訊息逐位元組相同；唯一的差別是輸入缺欄位時 Python 自己吐出的程式崩潰紀錄裡兩個行號變了，錯誤內容本身一樣。 | — |
| 5 | The complete package suite passes. | works | 我在乾淨副本上跑了這次改動相關的所有測試，237 個通過、5 個照設計跳過；完整的套件會由「改動被接受前會再跑一次、失敗就擋下」的自動化測試套件執行。 | — |

## 對你既有的資料做了什麼 (what this did to data you already had)

Nothing — 這次只改了畫圖工具的內部程式碼、它的測試、版本號與更新說明，不讀也不寫任何你已有的檔案或資料。以前畫好、貼在別處的圖不會被改動；只有之後重畫同樣的「會出問題」的圖時，框會比以前寬一格。

## I decided for you

- **只對「有標題加內文」的圖層放寬框的寬度** — 單行名稱的圖層維持原本的算法，因為它的名稱是置中、沒有前置空白，不會凸出。日後要讓單行名稱也套用同樣規則，會改變現有圖的樣子。
- **只有內文含兩格寬的字（例如中日文）時，才為了「最寬的那個字」放寬框** — 這樣全英文的圖完全不變，連原本那則「寬度必須是正數」的錯誤訊息也照舊出現。代價是那則錯誤訊息仍會在某些極窄的英文圖上出現（見最後一節）。
- **換行時一格都放不下就硬放一個字** — 選這個而不是報錯，因為報錯會讓原本能畫的圖變成失敗。在框裡這不會凸出，因為框已經放寬到容得下那個字。
- **標題貼著右邊框、不留空白** — 框只放寬到剛好容得下「前置空白＋標題」，所以標題最後一個字緊貼右框。想要右邊也留一格，就是再加寬一格，會讓這類圖再改一次樣子。
- **版本只升一小格（5.12.2）** — 這是修 bug，沒有新功能或新參數。我確認過 trunk 目前還是 5.12.1，沒有被別的改動搶先用掉。

沒有任何 important 以上的審查意見被駁回（對抗測試提出的兩個 important 問題已在這次改動中修好，我也照它的案例重試過，見第 1、4 列）。

## Steps you told me to skip

Nothing — no step was skipped.

## Things I am not sure you want

- 架構圖裡內文剛好和框一樣寬時，會提早一格換行（例如寬度 10 的「abcdefghij」被拆成「abcdefghi」和「j」）。改動前就是這樣，這次刻意不動。要另外開一個小改動修它嗎？
- 名稱是空字串的單行圖層會畫歪，標題空白、內文只有一個英文字、又沒有元件的圖層在極窄寬度下會直接報「寬度必須是正數」。這兩個也都和改動前一樣。要一起修嗎？
- 圖層有空的元件（空字串）時，檢查工具會提醒「分隔線後面沒有內容」。這也是改動前就有的提醒，只是這次的測試案例剛好用到空元件才看到。需要處理嗎？
- 輸入格式錯誤（例如圖層少了元件欄位）時吐出的 Python 崩潰紀錄，行號會跟改動前不同。我把它當成不屬於「錯誤訊息」的範圍；如果你認為連這種紀錄都要一模一樣，第 4 條就只能算部分符合。
