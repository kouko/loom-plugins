# 驗收測試減重 — 我試了什麼、結果如何

2026-09-23 在專案的乾淨副本（19025419）上試過，這是第二次修正後的重跑。每一條怎麼試、回來什麼：`docs/loom/2026-09-23-lighter-acceptance-testing/evidence/acceptance-test-evidence.md`。

## 你要的東西，一條一條看

| # | 你要的 | 結果 | 發生了什麼 | Re-run |
|---|---|---|---|---|
| 1 | The acceptance tester does not run the full package suite; a criterion the suite settles cites the finalize-review result instead. A setup check from a fresh clone still runs every time. | works | 這次同樣先從乾淨副本做安裝檢查、只跑了相關的 28 個測試（全過）、完整測試套件沒跑；規則現在由派工的一方明說完整測試有沒有被跳過，這次沒跳過，所以報告照規則寫「自動測試套件會在接受改動前跑、失敗就擋下」。 | re-tested |
| 2 | The report the user reads holds one row per criterion (verdict and one plain sentence), the decisions made on the user's behalf, and the open questions; the evidence behind each row lives in a separate file under the change's evidence directory. | works | 報告仍照範本的四節寫，證據另放一個檔，系統照樣接受純文字的證據檔、擋下被改成可執行檔的那份；「每份文件有沒有守英文規則」的清單已從測試者的工作拿掉，證據檔不再需要替它留位置。 | re-tested |
| 3 | A re-run after a fix tests only the criteria the fix could affect, marks every other verdict as carried over from the earlier run, and gives a one-line reason for each carried-over verdict. A criterion that is re-tested is re-tested in full — every surface the Acceptance line names — never only the part the fix touched. | partly | 我拿這次修正的內容逐條判斷，四條都依賴這次被改的規則，所以四條都整條重測；規則現在也涵蓋畫面流程，但「沿用上次結果並寫一行理由」那一半，兩次重跑都沒有實際用到。 | re-tested |
| 4 | These rules are carried by the acceptance tester's contract and the report template's own structure, and the checker's rule list does not grow. | works | 這次修正把幾條規則從流程說明搬進測試者自己的規則，沒碰檢查工具也沒碰總規格；檢查規則在改動前後都是 26 條，也沒有新增強制檢查點（原本一起數檢查點的那段測試被拿掉了，我直接數過，仍是原本的四個）。 | re-tested |

## 對你既有的資料做了什麼 (what this did to data you already had)

沒有 — 它只改了這個工具自己的說明文件、範本、總規格和測試，外加這次新建的檔案；你專案裡既有的資料一個都沒碰。唯一的影響是：之後的驗收報告會變短，細節搬到另一個證據檔。

## 我替你決定的事

- **不在你電腦上真的安裝外掛** — 安裝會蓋掉你現在裝好的版本，所以我只從乾淨副本驗證外掛能被載入、檢查工具能跑。之後想確認，就是實際裝一次。
- **安裝檢查用同一個 repo 的另一個乾淨工作目錄，不是重新 clone** — 你寫的是「fresh clone」，規則兩種都允許，這次派工也指定兩者皆可。差別只在於一個從網路重抓、一個從本機的 commit 展開；若你要求一定重新 clone，規則要改一句。
- **「引用最終結果」改成「引用最後會跑的檢查」** — 你要的是報告直接引用最後那道自動檢查的結果，但報告必須在那道檢查跑之前就提交，拿不到結果；所以報告用白話寫「自動測試套件會在接受改動前跑、失敗就擋下」，指令放證據檔。紅燈照樣會擋下改動，只是報告裡看不到那個結果。
- **四條又全部重測，沒有沿用任何一條** — 這次修正改了測試者的規則本身（誰告訴它測試有沒有跳過、測試失敗時怎麼判、重跑範圍擴到畫面流程、拿掉英文清單），四條都建立在這些規則上；規則說有疑慮就整條重測，我照做。
- **表格第一欄照抄你的驗收條件原文** — 第 1 條原文裡有一個內部步驟名稱，範本要求原文照抄，所以我沒改寫它；白話說明放在「發生了什麼」那一欄。
- **最後那道自動檢查和合併沒有實際跑** — 前者要等 reviewer 的結果、也會跑完整測試套件；後者會真的合併 PR。我只實測了其中檢查證據檔的那一段。
- **被駁回的重要審查意見** — 沒有收到任何一條，所以這裡沒有可列的。

## 我不確定你要不要的

- 第 3 條「沿用上次結果」那一半，在這個改動上兩次都用不到：每次修正都改到四條共同依賴的規則，所以每次都得全測。你接受它以「部分」結案、留待下一個真的只碰到一兩條的修正再驗證嗎？
