# 修好五處技能文件與檢查程式互相矛盾的地方 — 我試了什麼、結果如何

2026-10-27 在乾淨的專案副本（`02c51607`）上逐條試過。每一條怎麼試、回來什麼：`docs/loom/2026-10-26-five-skill-consistency-defects/evidence/acceptance-test-evidence.md`。

## 你要求的每一項

| # | 你要求的結果 | 判定 | 實際發生的事 | 重測 |
|---|---|---|---|---|
| 1 | A change that survives every adversarial attack and has no covering repository test can complete finalize-review without the user skipping the adversarial step, and the recorded adversarial evidence names the no-program outcome and its reason. | works | 在拋棄式專案上用真正的收尾檢查跑：只附一筆「沒有程式、理由是…」的紀錄就完成收尾，產出的驗證紀錄寫明這個結果與理由，之後重讀也判為有效；理由空白、和程式並列、兩筆、或專案裡其實存著攻擊程式時，全部被拒。 | — |
| 2 | The adversarial ceiling stated in the skill prose and the ceiling enforced by finalize-review count the same set of programs, so reusing an existing program never overflows the five-program ceiling and never produces a refusal the prose says cannot happen. | works | 文件現在說「上限按不重複的程式路徑算，重跑已算過的不加」，和檢查程式的算法一致；實測五支程式全部重跑、或同一支跑兩次都通過，第六支新的才被拒，正是文件說會被拒的情況。 | — |
| 3 | Recording a lesson that an existing memory entry already states produces exactly one defined outcome and never a second entry for the same subject, and the skill and its operations reference name that outcome identically. | works | 兩份文件用一字不差的同一句話定義結果：保留原條目、只把新來源加上去，並都禁止為同一主題建第二筆；在拋棄式記憶庫照做一遍，工具驗證通過，仍只有一筆條目。 | — |
| 4 | Every loom-visualization chat template that draws a node-label separator uses exactly six U+2501 characters, and the page verifier accepts a page built from each changed template. | partly | 三個有分隔線的範本現在每條都是六個字元，逐個標籤送進頁面檢查器都通過（改成七個就被擋）；但把整個範本做成一頁送檢時仍被拒，原因都與分隔線無關（範本本來就不是完整頁面格式）。 | — |
| 5 | A pytest-style adversarial probe recorded with any supported Python invocation (for example `python3 -m pytest`) is accepted by finalize-review, and one recorded as a direct `python3 <artifact>` run is still refused; the adversarial protocol states that acceptance instead of one literal spelling. | works | `python3 -m pytest`、`python3.12 -m pytest`、完整路徑的 Python、包在 `uv run` 裡的寫法都被收尾檢查接受；直接 `python3 檔案` 仍被拒；文件改寫成「任何支援的 Python 呼叫方式」並列出例子。 | — |
| 6 | The complete package suite passes, and both affected plugins land synchronized minor version bumps with CHANGELOG entries. | works | 在乾淨副本上跑完整的自動測試，全部通過、沒有任何失敗（約兩分鐘）；兩個 plugin 的版號在所有清單檔與 README 都一致（loom-code 3.50.0、loom-workflow 5.16.0），CHANGELOG 都有對應段落。 | — |

## 對你既有的資料做了什麼

這次修改只動 plugin 自己的文件、檢查程式與範本，不讀也不改你專案裡既有的資料。對已經存在的驗證紀錄：舊格式照樣有效，新增的「沒有程式」寫法只是多一種被接受的形式；記憶庫的規則變更只影響之後新記錄的課題，不會改寫已存的條目。我的測試全在暫存目錄的拋棄式專案裡進行，沒有碰你的工作樹（除了提交這份報告與證據檔）。

## 我替你決定的事

- **範本只做到「逐個標籤」通過檢查，不做成能整頁通過** — 規劃階段（plan）就決定這樣做：要整頁通過得替範本加上標題、連線說明、分組等原本沒有的東西，而你在 intent 裡把「擴大範本必須遵守頁面規則的範圍」列為不做。所以第 4 條後半只在標籤層級成立。若你要的是整頁可過，那是另一個變更，成本是改寫三個範本的圖。
- **「沒有程式」的紀錄放在既有欄位裡，不升版驗證紀錄格式** — 規劃階段決定：在原本的執行紀錄清單裡多一種寫法，不另開新版本格式。好處是舊紀錄、樣板都不用動；之後若要更嚴格的結構，得再改一次格式。
- **沒有被主流程駁回的重大問題。** 另有兩個攻擊測試留下的小問題，你在 intent 裡已列為不處理：沒有東西能證明「沒有程式」的紀錄背後真的跑過攻擊；記憶庫對「新課題擴大原條目或新增相關規則」的情況仍沒有定義結果。
- **我用了哪種方式「安裝」** — 我直接從乾淨副本執行 plugin，沒有用 README 的 `claude plugin install`，因為那會改到你電腦上真實的 plugin 設定。所以「從市集安裝」這一步沒有實際試。

## 你要求略過的步驟

沒有 — 計畫與 intent 都沒有記載你要求略過的步驟。

## 我不確定你是否想要的

- 第 4 條：只要求「範本裡的分隔線本身合格」就夠了嗎？還是你原本期待每個範本整頁都能通過頁面檢查？
