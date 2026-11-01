# 清掉 structured-node 改動留下的八個小意見 — 我試了什麼、結果如何

2026-10-20 第一次在乾淨的專案副本 a57a5769 上試過；同一天因為版本號被另一個已合併的改動先用掉而重新整理版本，於是在新的乾淨副本 0a1641b2 上重試受影響的幾條，並改拿最新的 trunk（76919786）當對照。每一條怎麼試、回來什麼：`docs/loom/2026-10-19-structured-node-nit-cleanup/evidence/acceptance-test-evidence.md`。

## What you asked for, one line at a time

| # | What you asked for | Verdict | What happened | Re-run |
|---|---|---|---|---|
| 1 | For the same inputs, including every error path, all five diagram generators produce output and error messages byte-identical to trunk before this change. | works | 拿最新的 trunk 和這次的改動各畫同樣 31 張圖（含中文、標籤比框還寬、所有錯誤訊息），輸出與錯誤文字全部逐位元組相同；直接呼叫共用函式的 11 個極端寬度案例也全相同。 | re-tested |
| 2 | The structured-node wrapping test fails when the width the body wraps at is changed. | works | 我在拋棄式副本裡把換行寬度故意改小一格、再改大一格，這支測試兩次都失敗；舊版的測試面對同樣的錯誤卻照樣通過，所以新測試確實補上了這個洞。 | carried over — 這次重整版本沒有動到畫圖程式或它的測試 |
| 3 | No test only restates a constant's literal text; the empty-body error text stays checked through the generator entry points. | works | 只抄寫常數文字的那支測試已刪掉，找不到其他同類測試；「body 不可為空」的錯誤文字改由流程圖、架構圖、樹狀圖三個入口實際觸發來檢查，測試通過。 | carried over — 這次重整版本沒有動到畫圖程式或它的測試 |
| 4 | The shared helper file carries no plan-only labels and no branch that cannot change its output, and `gen_arch.py` has no run of more than two blank lines. | works | 共用檔裡已沒有計畫編號標籤，三處對輸出沒影響的判斷已拿掉（拿掉後輸出完全一樣），架構圖產生器最長只剩兩行空行（原本是四行）。 | carried over — 這次重整版本沒有動到畫圖程式 |
| 5 | The 5.11.1 release note lists every helper that release added, and the structured-node change's golden-diff evidence and intent each carry a note pointing to what finally shipped (the 26-sample comparison; five sites derived from one error constant), with their original text kept. | works | 重新套上後，5.11.1 的更新說明仍列齊當時新增的五個共用項目（補上原本漏的一個），這次的變動另寫在新的 5.12.1 段落；舊改動的比對紀錄與 intent 跟最新 trunk 相比各只多了附註，原文一字未刪。 | re-tested |
| 6 | The complete package suite passes. | works | 在這次改動的工作副本（0a1641b2）上重跑完整的自動化測試套件，全部通過；正式收尾前還會由「改動被接受前會再跑一次、失敗就擋下」的自動化測試套件再檢查一次。 | re-tested |

## 對你既有的資料做了什麼 (what this did to data you already had)

Nothing — 這次只改了畫圖工具的內部程式碼、它的測試、版本號與更新說明；兩份已合併改動的舊紀錄只在結尾多加一行附註，原文沒有被改寫或刪除，不碰任何你自己的檔案或資料。

## I decided for you

- **舊紀錄只加附註、不改寫** — 我選擇在已合併改動的比對紀錄和 intent 後面各追加一行附註，而不是直接修正原文，因為你在 intent 裡要求舊紀錄只能追加。日後要改成直接修正原文，就得重寫已經審查過的歷史紀錄。
- **版本只升一小格（5.12.1）** — 因為使用者看得到的行為完全沒變，只升最小的一格。原本預定的 5.11.2 已經過時：另一個改動先合併並用掉了 5.12.0，所以這次改接在它後面。日後若有人認為該升更大一格，要重新改版本號、更新說明，並重跑收尾審查。
- **拿掉「寬度不夠時補零格空白」的判斷** — 因為 Python 本來就把負數個空白當成零個，拿掉後輸出一樣（我實測了比框還寬的中英文標籤）。日後若改用別的語言或寫法重做這段，要記得把這個保護加回來。
- **刪掉只抄寫常數文字的測試** — 改由三個產生器入口實際觸發錯誤來檢查同樣的文字，涵蓋範圍沒有變少。若想恢復，只是加回一支測試。

沒有任何 important 以上的審查意見被駁回。

## Steps you told me to skip

Nothing — no step was skipped.

## Things I am not sure you want

- 架構圖在你指定的寬度比圖層標題還窄時，標題那一行會凸出框外一格。改動前就是這樣（這次沒有改變它，也不在這次範圍內）。要另外開一個小改動修它嗎？
