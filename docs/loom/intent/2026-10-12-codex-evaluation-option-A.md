# Codex evaluation of option A — 2026-10-12

Second-vendor evaluation requested by the user before decision point ① of
intent 2026-10-12-loom-evidence-drift-guards. Run with `codex exec` (codex-cli
0.162.1) on the draft proposal, fresh context, no prior verdicts supplied.

## Verdict (codex)

> A 的方向合理，但目前不能宣稱封住三個破口：它能抓漏列與版本不一致，
> 還不能證明真的測過，而且 commit 相等要求會與現行流程衝突。
> 保留單一 checker 入口，但先修正版本比較模型、驗收通過語意與 intent
> 修訂規則。否則 A 會同時漏掉假的覆蓋，又擋住正常的報告提交。

## Findings absorbed into the intent

| # | Codex finding | Fix in intent |
|---|---|---|
| 1 | 「證據 commit = 審查 commit」與 closing-review「先測試→提交報告→再審查」流程衝突 | Acceptance #2: 區分被測 commit 與被審查 commit 兩個身分；只對功能內容差異失效，允許證據檔案差異 |
| 2 | 「每條交代狀態」≠「每條通過」；重複條目可湊列數 | Acceptance #1: 核對條目身分與狀態，省略或重複皆失敗 |
| 3 | `intent@sha` pinning 非 loom-code 既有契約（是採用 repo 自己的實踐） | Acceptance #3: 基準改為 intent 確認 commit；失敗訊息含重新確認路徑 |
| 4 | 不該另建證據系統；digest.py 會把新增報告算進功能內容 | Constraint: 延伸既有 attestation，不另建平行證據系統 |
| 5 | 檢查只跑 review 入口一次不夠 | Acceptance #6: 接入發布前失效檢查 |
| 6 | 增量重測慣例會被全量重測取消 | Constraint: 保留增量重測，沿用需保留原始版本與理由 |
| 7 | 解析任意散文維護成本高、誤報多 | Constraint: 只解析少量穩定欄位 |
| 8 | verdict 歸檔未定義與 attestation 主從關係 | Acceptance #5: 主從關係在文件中明確 |

## Open risks for plan stage

- 缺憑證/外部服務時允許 `not verified` 記錄，但不能算驗收成功。
- 「僅新變更生效」的遷移基準要不可任意改寫；進行中的變更仍保留原漏洞。
- `<!-- gate: -->` 是規則標記，仍需實際 checker 規則與命令入口呼叫才有執行力。
