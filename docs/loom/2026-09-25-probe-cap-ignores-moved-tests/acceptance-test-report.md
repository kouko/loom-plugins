# probe 數量上限只算這次新增的 probe，不算搬家的測試 — 我試了什麼、結果如何

2026-09-25 在專案的乾淨副本（7a19c5a9）上試過；另開丟棄式的 repo 副本模擬各種改動，並把 PR #52 原樣重播一次。每一條怎麼試、回來什麼：`docs/loom/2026-09-25-probe-cap-ignores-moved-tests/evidence/acceptance-test-evidence.md`。

## 你要的東西，一條一條

| # | 你要的 | 結果 | 發生了什麼 | Re-run |
|---|---|---|---|---|
| 1 | A change that moves or renames test files carrying a `concern:` line, and adds no probe of its own, passes the probe-program cap in finalize-review. | works | 把五個帶 `concern:` 的測試搬進子資料夾或改名、不新增任何 probe，數到 0 個、上限檢查通過；重播 PR #52，現在數到 1 個（它真正新增的那一個）並通過，同一個 PR 用修正前的版本數到 9 個而被擋下。涵蓋這條的測試也全部通過。 | — |
| 2 | A change that adds a new probe program into the suite, including one copied from an existing probe under a new name, is still counted, and more than five still makes finalize-review refuse it. | works | 新增一個 probe、把既有 probe 複製成新檔名（原檔保留）、把一個原本沒有 `concern:` 的普通測試改名再加上 `concern:`，三種情況各數到 1 個；新增 6 個時被擋下（「6 個，最多 5 個」），剛好 5 個時通過。涵蓋這條的測試也全部通過。 | — |
| 3 | A program placed under a `tests/local/` folder is not counted as graduated into the package suite. | works | 在 `tests/local/` 放 1 個、再試放 6 個 probe，都數到 0 個、上限檢查通過；同一個 probe 放在一般 tests 資料夾則會被算進去。涵蓋這條的測試也通過。 | — |
| 4 | The repository memory store records that moving graduated probes used to trip the cap and why PR #52 shipped unattested. | works | 記憶條目存在、已列入索引、驗證工具回報 OK；內容寫明 PR #52 被數成 9 個（8 個只是改名的舊 probe、1 個新的），原因是數的時候把改名當成新增，而且 review 輪次已經用完，所以 PR 沒有 attestation 就出貨。 | — |
| 5 | The checker's rule list does not grow and no new step, reviewer or dispatch is added. | works | checker 規則仍是 26 條、與改動前一字不差；機制總數仍是 140、「all clear」；其他規則共用的那段讀取改動的程式完全沒動；這次改動沒有碰任何 skill、agent 或流程文字。 | — |

## 對你既有的資料做了什麼

沒有 — 這個變更只改了 checker 數 probe 的方式、它的測試、一則記憶條目和版號，不讀也不改你既有的任何檔案或資料。

## 我替你決定的事

- **用 symlink 放進 `tests/local/` 的 probe 不處理（已知限制）** — 這是你在 2026-09-25 決定的（「不想在這邊用 symlink 增加複雜度」）：若有人刻意把 symlink 提交進 `tests/local/`，suite 會跑到那些檔案、但上限不會算到它們。我照你的決定沒有把它當成需求來測，只確認記憶條目和程式註解都寫明了這個限制。
- **直接呼叫 finalize-review 用的那支上限檢查，而不是走完整個 finalize-review** — 這次改的是 checker 的計數邏輯，照派工要求在丟棄式 repo 裡直接跑那支檢查；完整的 finalize-review（含整套 test suite）會在變更被接受前實際執行，失敗就擋下。
- **完整 test suite 留給 finalize-review** — 我只跑了涵蓋這五條的測試（13 個全過）；整套 suite 是變更被接受前會跑、失敗就擋下的自動檢查。
- 沒有收到任何被駁回的 important 以上 finding。

## 我不確定你要不要的事

沒有。
