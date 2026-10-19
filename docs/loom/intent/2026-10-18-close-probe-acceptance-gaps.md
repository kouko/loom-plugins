# 補上找漏洞測試接受判斷剩下的缺口
originator: kouko
kind: engineering
needs-design: no — 只改 checker 內部對已記錄找漏洞測試指令的接受判斷，沒有使用者輸入的介面，每支測試仍是單一接受／拒收決定
status: confirmed 2026-10-18
publication: automatic — authorized 2026-10-18 by kouko

## Problem
PR #94 讓審查證明工具（`finalize-review` 與 attestation validator）接受各語言的找漏洞測試，合併時還留著幾個已知缺口：

| 缺口 | 後果 |
|---|---|
| pytest 指令加上 `-k`（或 `-m`、`--deselect`，或寫在設定檔、外掛裡的過濾），或同時列多個檔，可以讓該測試檔的測試一支都沒跑，工具仍接受 | 沒跑到的找漏洞測試被當成跑過，審查證明不實 |
| 測試檔路徑含 `../`（例如從 store 資料夾往外跳）能通過「必須放在這次變更的 store」的檢查；`finalize-review` 另一步目前看來會擋下，validator 端沒有確認 | 放在別處、不屬於這次變更的檔案可能被算成這次的找漏洞測試 |
| `env go test …`、`npx --yes jest …`、`pnpm jest …` 這類常見寫法不在清單上，只能靠 reviewer 確認 | 多花一次 reviewer 確認，且確認只看輸出、不讀結果 |
| Rust：需要的 feature 預設就開啟的測試目標、放在 `tests/<資料夾>/main.rs` 的測試，被誤判成沒收進測試套件 | 正確的 Rust 找漏洞測試被拒收，變更卡在 closing-review |
| PR #94 最後兩次修正（Bun 只收 `./` 寫法、Rust 測試目標判讀）之後沒有重跑驗收 | 這兩處只有 LLM reviewer 審查與自動測試在保證，沒有在乾淨範例 repo 實際試過 |

## Proposed outcome
上面每個缺口都關閉：會排除測試檔的過濾一律拒收、路徑跳出 store 一律拒收、常見的包裝寫法直接讀結果判斷、cargo 實際會跑的 Rust 測試不再被拒收，並在乾淨範例 repo 重新驗收 Bun 與 Rust。

## Acceptance
1. pytest 找漏洞測試的指令只能列這一支檔；執行後 pytest 的總結若顯示有測試被略過（deselected），或沒有任何測試通過，`finalize-review` 一律拒收，不論過濾來自指令、設定檔還是外掛；不帶過濾、只列這支檔的指令照舊接受。判斷畢業測試是否收進測試套件時，套件指令本身帶的過濾照舊允許。
2. 找漏洞測試的檔案路徑含 `..` 或其他寫法、實際上不在這次變更的 store 也不在測試套件裡時，`finalize-review` 與 validator 都拒收。
3. 在乾淨範例 repo 裡，`env go test -json …`（含 `env 變數=值 go test -json …`）、`npx --yes jest …`、`pnpm jest …`（pnpm 直接接工具名）這幾種寫法，與原本清單寫法一樣，不需 reviewer 確認就讀結果產生審查證明；讀到零支通過時一樣拒收。
4. 在乾淨 Rust 範例 repo 裡，`required-features` 每一項都直接列在 `[features] default` 裡的測試目標，以及 `tests/<資料夾>/main.rs`，畢業成測試後被判定為已收進測試套件；`cargo test` 不會跑的目標仍被拒收。
5. 在乾淨範例 repo 用真的工具重試：Bun 的 `bun test ./<檔案>` 寫法產生有效審查證明、其他 Bun 路徑寫法被拒收；Rust 畢業測試的接受與拒收結果符合 cargo 實際行為。
6. repo 的完整 package suite 通過。

## Constraints
- 功能內容摘要的計算方式與三輪審查上限不變。
- PR #94 定下的接受規則（讀結果、至少一支非跳過測試通過、清單外走 reviewer 確認）不變，只補缺口。
- 已產生的有效審查證明仍驗證有效。

## Out of scope
- 新增其他語言或測試框架。
- 防止測試程式蓄意印出假結果，或偽造 reviewer 確認。
- 要求使用者的專案另外安裝測試報告外掛。
- Rust feature 的間接開啟（預設 feature 再開啟其他 feature）；這種測試目標仍被拒收，不會被誤接受。

## Open questions
- none
