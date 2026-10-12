# Loom evidence drift guards
originator: kouko
kind: product
needs-design: no — internal checker, attestation and station-text changes to loom-code; no user-facing interface surface per the repo's interface-surfaces default
evidence: [docs/loom/intent/2026-10-12-codex-evaluation-option-A.md]
status: confirmed 2026-10-12
publication: automatic — authorized 2026-10-12 by kouko

## Problem

在實際採用 loom 的 repo（youtube-summarize-scraper 的 2026-10-10-tui-display-fixes）觀察到：一個帶著 fatal bug 的變更一路走到 closing review 才被人肉攔下，loom 流程本身沒有擋住任何一次。三個具體破口：

1. **驗收覆蓋缺口** — acceptance test report 只驗證了 intent 10 條 Acceptance 中的 3 條，卻宣稱「全部逐條驗證通過」；fatal bug 正好在沒測的 7 條裡。
2. **證據基準漂移** — acceptance testing 跑在 intent 確認點的 commit，review 看的是 20+ commits 之後的 HEAD；中間的新功能零驗收。
3. **Intent 版本漂移無偵測** — intent 檔案在變更進行中被還原（10 條版 → 3 條版），git status 看不出異動，導致 build 依 A 版 intent 實作、review 依 B 版 intent 誤判範圍蔓延。

次要破口：plan 的 Risk 欄位精準預言了 fatal bug 但沒有對應測試；plan 的散文承諾無人檢查而洩漏進生產路徑；review verdict 產物落在 repo root 而非 change 目錄。

受影響的是所有 loom 採用 repo 的 closing review 品質；目前的替代方案是依賴 reviewer 的警覺性，本次案例證明這不夠。

## Proposed outcome

loom 流程機械化地偵測證據覆蓋缺口、證據過時與 intent 漂移，不再依賴 reviewer 的警覺。機制落點是**延伸既有 attestation**（它已綁定功能內容摘要）：補上確認時的 intent 版本、實際被測 commit、逐條驗收狀態與證據定位，由既有的 finalize 與發布前檢查核對；acceptance report 模板對每一條 Acceptance 交代覆蓋狀態（完整報告與驗收通過是兩個保證，not verified 是合法狀態但不計通過）。偵測到漂移時指出哪些驗收失效、走重新確認的恢復路徑，而不是只要求改 pin。review verdict 歸檔進 change 目錄並定義與 attestation 的主從關係。

## Acceptance

1. 對一份 acceptance report 未逐條交代 intent 每條 Acceptance 身分與狀態（含省略或重複條目）的變更執行檢查，檢查失敗並指出有問題的條號。
2. 對一份 attestation 未記錄被測 commit 與被審查 commit 兩個身分的變更執行檢查，檢查失敗；兩者之間存在功能內容差異（非證據檔案差異）時，檢查失敗。
3. 對一份 attestation 所記錄的 intent 確認版本與 intent 檔案當前內容不符的變更執行檢查，檢查失敗，且失敗訊息指出受影響的驗收條目與重新確認路徑。
4. 對一份 plan 具名的 boundary/probe test 在變更中不存在的變更執行檢查，檢查失敗。
5. closing review 完成後，verdict 產物存在於該 change 目錄內，且其與 attestation 的主從關係在文件中明確。
6. 檢查在 closing review 之後的發布前失效檢查中再次執行，不只 review 入口一次。
7. 本變更之後新建立的 loom 變更，其 attestation 與 acceptance report 模板預設帶有上述欄位。

## Constraints

- 規則必須是 loom_checker.py 可重算的 check，不是散文宣稱。
- 機制延伸既有 attestation 與 digest 綁定，不另建平行的證據系統。
- 證據比較允許證據檔案差異、只對功能內容差異失效；保留 acceptance-tester 既有的增量重測慣例（沿用未受影響的列需保留原始版本與理由）。
- 解析格式要窄：只解析少量穩定欄位（attestation JSON、模板欄位），不解析任意散文。
- 既有 loom 1.0 站別產物與 schema 不破壞；新規則對新建立的變更生效，「新」的基準由 intent 確認 commit 定義，缺欄位的處理明確定義。
- 遵守 Module Criteria：新規則各自有測試；add = 一個新檔 + 一個 routing entry。
- 遵守版本政策：新 rule ids 為 minor bump；三份 manifest、CHANGELOG、README 同步。

## Out of scope

- 重設計 review lens 或 reviewer dispatch 機制。
- 為採用 repo 的歷史 loom 產物做回溯遷移。
- youtube-summarize-scraper 那個變更本身的修復（另一個 repo、另一個 intent）。
- 從 plan 散文自動生成測試程式碼。
- 取代 acceptance test report 的使用者可讀格式（它維持現狀，機制欄位進 attestation）。

## Open questions

- none

## Decisions
- **intent_confirmed_sha**: In capture-intent station, after confirming intent, compute blob SHA of intent file (without status line) and add `intent_confirmed_sha: <sha>` to intent frontmatter. This matches spec's confirmed-behavior approach.
- **tested_commit parsing**: Extract from acceptance test report's "Tried on ... at <short sha>" line using regex `r'at ([0-9a-f]{7,40})'`. If not found, fall back to first 7 chars of HEAD at acceptance-test time.
- **Evidence file diff whitelist**: Extend manifest.yaml publication_only_paths to include `docs/loom/<change-id>/evidence/**` and `docs/loom/<change-id>/acceptance-test-report.md`.
- **Checker modularization**: Split 4 new rules into separate files under loom-checker/rule_checks/ (evidence_coverage.py, commit_identity.py, intent_version.py, plan_boundary_tests.py) and register in rules.py.