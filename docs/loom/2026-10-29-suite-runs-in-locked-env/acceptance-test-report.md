# uv 專案的完整測試改在鎖定環境裡跑 — 我試了什麼、結果如何

2026-10-29 在專案的乾淨副本（edc30a0b）上試；修正後同日在新的乾淨副本（0ffd76e6）上重跑第 1 條。每一條怎麼試、回來什麼：`docs/loom/2026-10-29-suite-runs-in-locked-env/evidence/acceptance-test-evidence.md`。

重跑時另外確認了：新的乾淨副本照專案說明能正常載入使用。

試驗場：把範例 uv 專案（tasknote）clone 一份到暫存區操作，原本那份沒動；整個過程中這台機器上排第一的 `python3` 都是沒裝 tasknote 的 conda 環境，PATH 一次都沒改。

## 你要的，一條一條看

| # | 你要的 | 結果 | 實際發生什麼 | 重跑 |
|---|---|---|---|---|
| 1 | In a uv-managed Python repository with no declared package-tests command, the end-of-Build suite and finalize-review's suite pass on a machine where the first `python3` on PATH is an interpreter without the project's dependencies, with no PATH change by the agent. | works | finalize-review 那一次改用鎖定環境跑、測試全過並寫出驗收紀錄。修正後 Build 的說明直接指向檢查工具裡那張「依哪個專案檔案選哪條指令」的表；我照說明在範例專案的全新副本裡走一遍，選到的就是鎖定環境那條指令，和 finalize-review 用的一字不差，31 個測試全過，鎖檔沒動。同一台機器直接用排第一的 `python3` 跑則在收集階段 4 個錯誤。另外，「Build 說明確實指向那張表、且沒有抄一份指令進去」這兩個測試也跑過、通過；整套測試會在改動被接受前執行，沒過就擋下。我沒有開一整輪 Build 流程，是照 Build 的那一步說明手動執行。 | 重測 |
| 2 | A Python repository without a uv lockfile, and any repository that declares a package-tests command, gets the same suite command as before. | works | 沒有鎖檔的專案、鎖檔被 git 忽略的專案、以及有自己宣告測試指令的 uv 專案，拿到的指令都和改動前一字不差。 | carried over — 這次修正只改了 Build 的說明文字、說明測試和更新紀錄，判斷指令的程式沒動 |
| 3 | In such a repository whose committed lockfile no longer matches its declared dependencies, the suite stops with a message naming how to update the lockfile, and the lockfile is left unchanged. | works | 改了相依套件卻沒更新鎖檔時，測試立刻停下，訊息直接寫「要更新鎖檔請跑 `uv lock`」，finalize-review 也照樣擋下；鎖檔前後內容完全相同。 | carried over — 修正沒碰執行測試或 finalize-review 的程式 |
| 4 | In such a repository, an adversarial program graduated into the package suite is recognized at finalize-review as collected by that suite. | works | 放進正式測試資料夾的對抗測試被認得、通過；放在測試資料夾以外的則被 finalize-review 拒絕（改動前連前者都認不出來）。 | carried over — 修正沒碰判斷「測試有沒有被收進來」的程式 |

另外第一輪時依指示把這個 repo 自己的完整測試跑了一次：全部通過（重跑這一輪沒有再跑整套）。

## 對你既有的資料做了什麼

已提交的檔案一個都沒被改（每次跑完 git 狀態都是乾淨的，鎖檔內容前後一致）。但測試現在會用專案自己的虛擬環境（`.venv`）：沒有就自動建一個；已經有的話，鎖檔裡列的套件會被調回鎖檔的版本（實測：手動裝的 pytest 8.3.5 被換回鎖檔的 9.1.1），你另外自己裝的、鎖檔沒列的套件則保留不動。這個虛擬環境本來就不進版本控制，要回復只能自己重裝原本的版本。

## 我替你決定的

- **用假的審查結果去跑 finalize-review** — 為了在範例專案裡真的走到「跑完整測試」那一步，我餵了兩份寫好的通過結論；它們只是讓流程走下去，不代表有人審查過。這只發生在暫存區的副本，不影響這次改動。
- **在範例專案的 main 分支上試** — clone 下來預設停在另一個分支，我改用最新的 main，因為它才有完整的測試與先前的對抗測試。結果不受影響，兩邊都有鎖檔且沒宣告測試指令。
- **鎖定方式選「鎖檔不符就停」而不是「照舊跑」或「自動改寫鎖檔」**（這次改動本身替你做的決定）— 規劃時試過：不加限制會偷偷改寫鎖檔，「照舊跑」會用到過期的套件。之後若想改，只是換一個參數。
- **鎖檔優先於一般 Python 專案判斷**（同上）— 有鎖檔的 uv 專案一律走新指令。代價：已經在進行中、沒宣告測試指令的 uv 專案分支，升級後偵測到的指令會變，先前的驗收紀錄會過期、要重跑一次收尾審查。
- 沒有任何嚴重度 important 以上的發現被主流程駁回。

## 你叫我跳過的步驟

沒有 — 沒有任何步驟被跳過。

## 我不確定你要不要的

- 上一輪的疑問（Build 結尾要不要和 finalize-review 用同一條指令）已由這次修正解決，見第 1 條。
- 一個小缺口（和 uv 無關、改動前就存在）：專案裡完全沒有那張表列的任何檔案、只有測試檔時，檢查工具會改用 `python3` 直接跑；Build 的說明沒提到這種情況。要不要補一句？
