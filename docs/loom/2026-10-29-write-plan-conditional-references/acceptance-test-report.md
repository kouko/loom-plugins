# write-plan 的必讀本文不再夾帶條件性段落 — 我試了什麼、結果如何

2026-10-29 在專案的乾淨副本（3eb08254）上試。每一條怎麼試、拿到什麼結果：`docs/loom/2026-10-29-write-plan-conditional-references/evidence/acceptance-test-evidence.md`。

## 你要的東西，一條一條看

| # | 你要的 | 結果 | 實際發生什麼 | Re-run |
|---|---|---|---|---|
| 1 | write-plan's SKILL.md body is at most 2800 words, under an unchanged 3750-word cap. | works | 本文從 3749 字降到 2780 字（離 2800 只剩 20 字），3750 的上限檢查一字未改。 | — |
| 2 | A run without loom-design still reaches the no-intent interview and the self-written minimal spec path, and each rule those paths state today is still stated, with the same meaning, in the file the run is sent to. | works | 沒裝 loom-design 的四條路（沒有需求單、手寫未確認的需求單、需要自己寫規格、規格寫到一半續做）都會被指到正確的檔案；原本 312 句裡 311 句逐字搬過去，唯一改動的一句是補上「去讀哪個檔」的指引。 | — |
| 3 | A run with loom-design installed is never told to read the no-intent interview file, and is told to read the self-written spec file only when it writes a spec itself. | works | 裝了 loom-design 的各條路都不會被叫去讀「訪談」檔；只有在它自己要寫規格時（任務理由塞不進一行風險說明，或有待記錄的細節）才會被叫去讀「自寫規格」檔，交給規格工具的那條路沒有指引。 | — |
| 4 | Every existing check that pins those rules still runs and passes against the file that now holds them. | works | 鎖住這些規則的檢查都已改成讀新檔案，相關的 11 個測試檔共 234 個測試全部通過；完整測試組會在變更被接受前由自動測試再跑一次，失敗就會擋下。 | — |

## 對你既有的資料做了什麼

沒有 — 這次只搬動外掛自己的說明文字與測試，沒有讀寫任何你原本擁有的資料或設定檔。

## 我替你決定的事

- **怎麼「試」第 2、3 條** — 這兩條講的是 agent 在每條路上會讀到什麼，所以我以第一次讀的人的角度，逐條路順著文字指引走，並用腳本逐句比對搬動前後的文字；我沒有真的把這個版本裝進你的 Claude Code 去跑一次完整流程，因為那會改動你的外掛設定。若你要真實執行的證據，得另外在一個拋棄式環境裡跑。
- **「被指到的檔案」包含接力的檔案** — 沒有需求單時，訪談檔會再把你指向「確認需求」那份說明，寫需求單的規則在那裡；我把這種一跳再一跳的指引算成「被指到」。
- **已確認的需求單少讀一段規則，我判斷意思沒變** — 需求單已經確認時，現在不會再讀到「寫需求單」那段規則（包括「看得到的影響但介面未定時要標成需要設計」那一句）。這種情況下判斷要不要設計的主規則仍在本文裡，loom-design 那邊負責擷取需求的工具也有同一句，所以我判斷沒有改變意思。如果你認為已確認的流程也該讀到那句，這裡就是會出問題的地方。

## 你叫我跳過的步驟

沒有 — 沒有跳過任何步驟。

## 我不確定你要不要的事

- 版本說明寫「降到 2763 字」，但後來的修正加了 17 字，實際是 2780 字。要更正那個數字嗎？
- 本文離 2800 字只剩 20 字的空間，而且沒有任何檢查會守住 2800 這條線（只守 3750）。要另外加一個 2800 的檢查，還是維持現狀？
