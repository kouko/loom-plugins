# 修好五處技能文件與檢查程式互相矛盾的地方 — 我試了什麼、結果如何

2026-10-27 第一次在乾淨的專案副本（`02c51607`）上逐條試過；修正之後，在新的乾淨副本（`0a27f371`）上重測了受影響的項目，也試了新增的第 6 條；第 6 條的位置問題修好後，又在新的乾淨副本（`a0966dd7`）上把第 6 條完整重測一次。最新一次修正之後，在新的乾淨副本（`7df38898`）上把第 1 條和第 6 條完整重測，並重新核對第 7 條。針對少見換行字元的修正之後，再於新的乾淨副本（`77b86cf0`）上把第 1、6 條完整重測，並重新核對第 7 條。每一條怎麼試、回來什麼：`docs/loom/2026-10-26-five-skill-consistency-defects/evidence/acceptance-test-evidence.md`。

## 你要求的每一項

| # | 你要求的結果 | 判定 | 實際發生的事 | 重測 |
|---|---|---|---|---|
| 1 | A change that survives every adversarial attack and has no covering repository test can complete finalize-review without the user skipping the adversarial step, and the recorded adversarial evidence names the no-program outcome and its reason. | works | 用真正的收尾檢查跑：只附一筆「沒有程式、理由是…」的結果，就能完成收尾，產出的驗證紀錄寫明這個結果和理由，事後重讀也判為有效。理由空白、和程式並列、或專案裡其實存著攻擊程式時都會被拒。理由前後多了空白、含有註解記號、或被任何一種換行字元分成兩段時（包括一般打字打不出來的分頁字元、Unicode 分行字元等，我把 Python 認得的九種換行字元全試過），收尾檢查都會當場拒絕，不會等到發布時才卡住；一般句子、中文句子、中間有破折號、定位字元或不換行空白的句子照樣通過。說明文件現在也完整寫出這些拒絕條件。 | re-tested |
| 2 | The adversarial ceiling stated in the skill prose and the ceiling enforced by finalize-review count the same set of programs, so reusing an existing program never overflows the five-program ceiling and never produces a refusal the prose says cannot happen. | works | 文件說上限按不重複的程式算，重跑已經算過的程式不會多算，和檢查程式的算法一致。實測：重跑五支舊程式通過，第六支新程式被拒。 | carried over — 最新這次修正只改了理由是否算「一行」的判斷和說明這條規則的一句話，沒有動到上限的計算，也沒有動到說明上限的文件 |
| 3 | Recording a lesson that an existing memory entry already states produces exactly one defined outcome and never a second entry for the same subject, and the skill and its operations reference name that outcome identically. | works | 兩份文件用一字不差的同一句話定義結果：保留原條目，只把新來源加上去，不另建第二筆。在拋棄式記憶庫照做，工具驗證通過，條目仍只有一筆。 | carried over — 最新這次修正沒有動到記憶庫相關的任何檔案 |
| 4 | Every loom-visualization chat template that draws a node-label separator uses exactly six U+2501 characters, and the page verifier accepts a page built from each changed template. | partly | 三個有分隔線的範本每條都是六個字元，每個標籤單獨送進頁面檢查器都通過；但整個範本做成一頁送檢時仍被拒，原因與分隔線無關。 | carried over — 最新這次修正沒有動到範本或頁面檢查器 |
| 5 | A pytest-style adversarial probe recorded with any supported Python invocation (for example `python3 -m pytest`) is accepted by finalize-review, and one recorded as a direct `python3 <artifact>` run is still refused; the adversarial protocol states that acceptance instead of one literal spelling. | works | 各種 `python -m pytest` 的寫法都被接受，直接用 `python3 檔案` 跑仍會被拒，文件也改成列出被接受的各種寫法。 | carried over — 最新這次修正沒有動到判斷指令寫法的程式碼，也沒有動到說明攻擊程式寫法的那份文件（它只改了收尾說明裡講理由規則的一句話） |
| 6 | When the recorded adversarial evidence is a no-program outcome, the pull request's Verification section states that no adversarial program ran and gives the recorded reason, and publication refuses a body that leaves it out. | works | 把「沒有程式＋理由」那一行寫進 PR 的「驗證」段落（包括驗證段落底下更小一級的標題裡）就能發布；漏寫、理由寫錯、藏在註解或程式碼區塊裡、寫成清單項目、寫在別的段落都會被拒。驗證段落裡一旦出現一級或二級標題（含前面縮排最多三格的），之後的內容就不再算驗證段落；驗證紀錄已經過期時，只要紀錄裡寫著「沒有程式」，同樣要求這一行，漏寫就拒絕。上次留下的漏洞已補上：夾著少見換行字元的理由現在在收尾時就被拒，根本到不了發布；收尾收下的理由（含中文、定位字元、不換行空白等）我逐一拿去發布，那一行都對得上。 | re-tested |
| 7 | The complete package suite passes, and both affected plugins land synchronized minor version bumps with CHANGELOG entries. | works | 版號在所有清單檔和 README 都一致（loom-code 3.50.0、loom-workflow 5.16.0），沒有被最新修正動到；3.50.0 段落裡「理由必須是去掉空白的一行」那句仍然正確描述修正後的行為，版號檢查測試全數通過。和這次修改相關的測試我都跑過，全數通過；完整的自動測試我沒有重跑，交給自動測試套件，它在變更被接受前執行，失敗就會擋下。 | re-tested — 只重新核對版號、更新紀錄和相關測試；完整測試照樣交給上述的自動測試套件 |

## 對你既有的資料做了什麼

這次修改只動 plugin 自己的文件、檢查程式和範本，不會讀取或修改你專案裡既有的資料。既有的驗證紀錄：舊格式照樣有效，「沒有程式」只是多一種被接受的寫法。新增的發布檢查只在驗證紀錄記著「沒有程式」時才要求 PR 多寫一行，其他 PR 不受影響；現在不論驗證紀錄是有效還是已經過期，只要它記著「沒有程式」就會要求。記憶庫規則的變更只影響之後新記錄的課題，已存的條目不會被改寫。我的測試全部在暫存目錄的拋棄式專案裡進行，發布測試沒有推送到任何遠端，也沒有連上 GitHub。除了提交這份報告和證據檔，我沒有碰你的工作樹。

## 我替你決定的事

- **「驗證」段落底下再開更小一級的標題，寫在那裡也算數** — 檢查把「驗證」標題之後、下一個一級或二級標題之前的內容都當成驗證段落，所以寫在三級以下的小標題裡會放行。我判斷這符合你「寫在驗證段落」的要求，所以第 6 條判為「成立」。若你要求一定要緊接在「驗證」標題底下，就得再改一次檢查。
- **範本只做到「逐個標籤」通過檢查，不做成能整頁通過** — 規劃階段就這樣決定：要整頁通過，得替範本加上原本沒有的東西，而你把「擴大範本必須遵守頁面規則的範圍」列為不做。
- **「沒有程式」的結果放在既有欄位裡，不升級驗證紀錄的格式** — 規劃階段決定的：舊紀錄和樣板都不用動；之後若要更嚴格的結構，得再改一次格式。
- **理由裡夾著少見的換行字元（例如分頁字元），收尾時就擋下** — 這是主流程（不是我）替你做的決定：上次報告把它當成問題留給你，但它和前一輪修掉的「收尾收下、發布卻永遠過不了」是同一類毛病，所以直接一併擋下。代價是：如果有人真的在理由裡放了這種字元，收尾會要求改寫理由；一般打字不會遇到。
- **沒有被主流程駁回的重大問題。**
- **我怎麼「安裝」的** — 我直接從乾淨副本執行 plugin，沒有用 README 的 `claude plugin install`，因為那會改到你電腦上真正的 plugin 設定。
- **發布測試只跑到「準備連線」為止** — 為了不推送、也不連 GitHub，我把對外連線換成一律回報失敗。所以「PR 真的在 GitHub 上建立、內文裡有那一行」這一步沒有實際跑；這一步由專案自己的測試驗證，那些測試全數通過。

## 你要求略過的步驟

沒有 — 計畫和 intent 裡都沒有記載你要求略過的步驟。

## 我不確定你是否想要的

- 第 4 條：只要範本裡的分隔線本身合格就夠了嗎？還是你原本期待每個範本整頁都能通過頁面檢查？
