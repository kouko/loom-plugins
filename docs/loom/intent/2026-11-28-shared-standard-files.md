# 寫的人與審的人共讀同一份標準
originator: kouko
kind: engineering
needs-design: no — internal reference files read by loom agents; no CLI, API, UI or user-facing file surface changes
evidence: [docs/loom/research/2026-11-28-mattpocock-skills.md]
status: confirmed 2026-11-28
intent_confirmed_sha: 93f7ee80ca777f16e857a42ab5865ff3d7bd0a41
publication: automatic — authorized 2026-11-28 by kouko

## Problem

loom-code 裡同一條品質規則寫在兩個地方：寫程式的 implementer 讀
`loom-code/references/engineering-baseline.md`，審查的 reviewer 讀
`loom-code/skills/closing-review/references/lenses.md`，兩邊措辭不同，已經出現標準不一致：

| 規則 | 寫的人讀到 | 審的人讀到 |
|---|---|---|
| 抽象層 | 只有一個用途就不准抽象 | 兩個使用者、明確要求或看得見的動機，三者之一就可以 |
| 測試 | 邏輯改了也不會失敗的測試不算測試 | 只要求有 RED→GREEN 證據 |
| 只轉呼叫的模組 | 沒寫 | 算 finding |

結果是寫的人照自己的標準寫，到 closing-review 才被另一套標準挑出來，多一輪修正；或寫的人被禁止的寫法，審的人反而放行。文件／skill 文字的品質判準（遺漏、歧義、否定詞被改掉）目前只有審的人讀得到。另外兩個已知缺口沒有任何一邊寫：測試的期望值用和程式相同的算法算出來（必然通過的測試），以及介面幾乎和它做的事一樣複雜的模組（shallow module）。

## Proposed outcome

測試、程式碼設計、文件／skill 文字三個主題，各有一份寫的人和審的人共讀的標準；每條規則只在一個地方寫，兩邊引用同一段文字。

## Acceptance

1. `loom-code/references/` 下有三份標準檔，各自涵蓋測試、程式碼設計、文件／skill 文字。
2. 這三個主題的每條規則只寫在一份標準檔裡：implementer 讀的基準文件和 reviewer 讀的判準文件都指向標準檔，不再各自重述同一條規則。
3. 抽象層門檻只有一種寫法，寫的人和審的人讀到的是同一句。
4. 測試標準禁止「期望值用和程式相同的方式算出來」的斷言，並要求期望值來自獨立來源（已知正確的字面值、手算範例或規格）。
5. 程式碼設計標準含 shallow module 判準（介面幾乎和它做的事一樣複雜）和刪除測試（刪掉這個模組後，複雜度是消失還是散到各呼叫者）。
6. 測試標準禁止綁實作的測試：mock 內部元件、測私有方法、繞過公開介面去驗證結果；判斷依據是「沒改行為的重構會讓它失敗」。
7. 程式碼設計標準含可測試的設計：依賴由外部傳入而不是在內部建立，優先回傳結果而不是直接產生副作用。
8. write-plan 為每個 task 切模組邊界時，指向程式碼設計標準。
9. 搬移前 engineering-baseline 與 lenses 裡屬於這三個主題的每條規則，搬移後仍存在且意思不變（禁止沒有變成允許，門檻沒有放寬或收緊，除第 3 條統一的那一處）。紅 → 綠 → 重構的循環維持不變。
10. 完整 package suite 通過，loom-code 以新版號釋出。

## Constraints

- 不新增 skill；標準檔放在 loom-code 自己的 `references/`，用路徑讀取。
- 標準檔是執行期文字，不得引用本 repo `docs/` 下的開發紀錄（Contract Citations 規則）。

## Out of scope

- 獨立的參考用 skill（`user-invocable: false`）。
- 定期掃描既有程式找 shallow module 的入口。
- security、architecture-conformance、principles-conformance 等引用外部標準或使用者自有文件的審查維度。
- reviewer 的維度名稱與判決格式。
- loom-design、loom-workflow 的 skill。
- 研究紀錄中尚未討論的第 3、4 項（mutation-diff 驗證、兩軸審查分工）。
- 把重構移出 TDD 循環（研究紀錄已記為待議）。
- 寫測試前和使用者確認測試位置；強制使用 mattpocock 的專有名詞。

## Open questions
- none
