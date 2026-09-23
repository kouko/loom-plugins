# 驗收測試減重 — 我試了什麼、結果如何

2026-09-23 在專案的乾淨副本（f834349e）上試過，這是修正後的重跑。每一條怎麼試、回來什麼：`docs/loom/2026-09-23-lighter-acceptance-testing/evidence/acceptance-test-evidence.md`。

## 你要的東西，一條一條看

| # | 你要的 | 結果 | 發生了什麼 | Re-run |
|---|---|---|---|---|
| 1 | The acceptance tester does not run the full package suite; a criterion the suite settles cites the finalize-review result instead. A setup check from a fresh clone still runs every time. | works | 這次重跑也是先從乾淨副本做安裝檢查，只跑了相關的 35 個測試（全過），完整測試套件沒跑；規則現在要報告用白話寫「自動測試套件會在接受改動前跑、失敗就擋下」，指令放證據檔，和範本不再打架。 | re-tested |
| 2 | The report the user reads holds one row per criterion (verdict and one plain sentence), the decisions made on the user's behalf, and the open questions; the evidence behind each row lives in a separate file under the change's evidence directory. | works | 報告的章節現在只照範本走，專案總規格也改成同樣四節，所以上次多補的三節都拿掉了；證據另放一個檔，檢查器照樣接受它，故意改成可執行檔時照樣擋下。 | re-tested |
| 3 | A re-run after a fix tests only the criteria the fix could affect, marks every other verdict as carried over from the earlier run, and gives a one-line reason for each carried-over verdict. A criterion that is re-tested is re-tested in full — every surface the Acceptance line names — never only the part the fix touched. | partly | 這次是真的修完再跑：規則讓我拿修正內容逐條判斷、並把要重測的整條重測，做起來順；但四條都可能被這次修正影響，「沿用上次結果並寫理由」那一半這次沒有實際用到。 | re-tested |
| 4 | These rules are carried by the acceptance tester's contract and the report template's own structure, and the checker's rule list does not grow. | works | 這次修正動到了檢查器會讀的總規格，所以重測：檢查器規則在改動前後仍是 26 條，檢查器本身沒改，也沒有新增閘門標記。 | re-tested |

## 對你既有的資料做了什麼 (what this did to data you already had)

沒有 — 它只改了這個工具自己的說明文件、範本、總規格和測試，外加這次新建的檔案；你專案裡既有的資料一個都沒碰。唯一的影響是：之後的驗收報告會變短，細節搬到另一個證據檔。

## 我替你決定的事

- **不在你電腦上真的安裝外掛** — 安裝會蓋掉你現在裝好的版本，所以我只從乾淨副本驗證外掛能被載入、檢查器能跑。之後想確認，就是實際裝一次。
- **安裝檢查用同一個 repo 的另一個乾淨工作目錄，不是重新 clone** — 你寫的是「fresh clone」，規則兩種都允許，這次派工也指定兩者皆可。差別只在於一個從網路重抓、一個從本機的 commit 展開；若你要求一定重新 clone，規則要改一句。
- **「直接引用最終結果」改成「引用最終會跑的檢查」** — 你寫的是引用 finalize-review 的結果，但報告要在它跑之前就提交，拿不到結果；規則改成報告用白話寫「最後那一步會跑、失敗就擋」，指令放證據檔。紅燈照樣會擋下，只是報告裡看不到那個結果。
- **四條全部重測，沒有沿用任何一條** — 這次修正動到第 1、2、4 條各自依賴的規則或總規格；第 3 條上次是「部分」，原因正是還沒真的重跑過，所以也重測。規則說有疑慮就整條重測，我照做。
- **最後的 finalize-review 和合併沒有實際跑** — 前者還要等 reviewer 的結果、也會跑完整測試套件；後者會真的合併 PR。我只實測了其中檢查證據檔的那一段。

## 我不確定你要不要的

- 規格若有畫面流程，修完重跑時畫面流程那幾行也要照「可能受影響就全測」的規則嗎？新規則只講了驗收條件。
- 「英文規則有沒有守住」的清單現在規定放證據檔，但範本給證據檔的格式裡沒有它的位置；我放在證據檔最後一節。要不要在範本裡替它留一節？
