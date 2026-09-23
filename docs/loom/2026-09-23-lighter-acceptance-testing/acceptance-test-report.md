# 驗收測試減重 — 我試了什麼、結果如何

2026-09-23 在專案的乾淨副本（e43b6b11）上試過。每一條怎麼試、回來什麼：`docs/loom/2026-09-23-lighter-acceptance-testing/evidence/acceptance-test-evidence.md`。

## 你要的東西，一條一條看

| # | 你要的 | 結果 | 發生了什麼 | Re-run |
|---|---|---|---|---|
| 1 | The acceptance tester does not run the full package suite; a criterion the suite settles cites the finalize-review result instead. A setup check from a fresh clone still runs every time. | works | 這份報告就是照新規則跑的：從乾淨副本做了安裝檢查，只跑了這次改動相關的 24 個測試（全過），完整測試套件留給最後的 finalize-review。 | — |
| 2 | The report the user reads holds one row per criterion (verdict and one plain sentence), the decisions made on the user's behalf, and the open questions; the evidence behind each row lives in a separate file under the change's evidence directory. | works | 照新範本寫出的這份報告一條一行、證據另放一個檔；那個證據檔不會被檢查器誤當成程式，而故意改成可執行檔時會被擋下。 | — |
| 3 | A re-run after a fix tests only the criteria the fix could affect, marks every other verdict as carried over from the earlier run, and gives a one-line reason for each carried-over verdict. A criterion that is re-tested is re-tested in full — every surface the Acceptance line names — never only the part the fix touched. | partly | 規則讀起來清楚、也有測試守著，但這是第一次跑，還沒有真的「修完再跑一次」可以驗證。 | — |
| 4 | These rules are carried by the acceptance tester's contract and the report template's own structure, and the checker's rule list does not grow. | works | 檢查器的規則在改動前後都是 26 條，檢查器本身沒改，也沒有新增任何閘門標記。 | — |

## 審查摘要

Closing review 的 reviewer 還沒交回結果給我，所以這裡沒有可以摘要的審查意見。

## 我問過你的問題

- 要不要先核實數字再開 intent — 你說好，先核實。
- 「部分重跑漏掉其他地方」這條要不要加進來 — 你說加進 intent，然後跑完。

## 對你既有的資料做了什麼 (what this did to data you already had)

沒有 — 它只改了這個工具自己的說明文件、範本和測試，外加這次新建的檔案；你專案裡既有的資料一個都沒碰。唯一的影響是：之後的驗收報告會變短，細節搬到另一個證據檔。

## 英文規則有沒有守住

- 計畫：守住，只有兩句照錄你原話的中文回答。
- 規格：這次沒有規格（不需要設計）。
- 審查意見：還沒有，無從檢查。
- 證據檔：英文，守住。
- 測試說明文字：英文，守住。
- 測試名稱：部分守住 — 後加的 10 個對抗測試照「對象_狀態_預期」命名，原本的 13 個是整句式命名。
- Commit 訊息：9 個都是英文，守住。

## 我替你決定的事

- **不在你電腦上真的安裝外掛** — 安裝會蓋掉你現在裝好的版本，所以我只從乾淨副本驗證外掛能被載入、檢查器能跑。之後想確認，就是實際裝一次。
- **完整測試那一行，指令只放證據檔** — 新規則一邊說「完整測試那一行要引用測試指令」，一邊說「報告裡不能出現指令」。我把指令放證據檔，報告只寫白話。若你要的是報告裡看得到指令，範本要改一句。
- **範本缺的兩節我補上了** — 專案的總規格要求報告有「審查摘要」和「我問過你的問題」，新範本沒有；另外新規則要求列出英文規則是否守住，範本也沒留位置。三節我都補了，範本本身沒改。
- **「直接引用最終結果」改成「引用最終會跑的檢查」** — 你寫的是引用 finalize-review 的結果，但報告要在它跑之前就提交，拿不到結果；實作選擇寫明「最後那一步會跑、失敗就擋」。紅燈照樣會擋下，只是報告裡看不到那個結果。
- **最後的 finalize-review 和合併沒有實際跑** — 前者要等 reviewer 的結果還會跑完整測試套件，後者會真的合併 PR；我只讀了程式並實測其中讀證據檔的那一段。

## 我不確定你要不要的

- 規格若有畫面流程，修完重跑時畫面流程那幾行也要照「可能受影響就全測」的規則嗎？新規則只講了驗收條件。
- 安裝檢查用「同一個 repo 的另一個乾淨工作目錄」算不算數？你寫的是「fresh clone」，規則兩種都允許。
