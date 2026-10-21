# 讓 Loom agent 自行修復檢查環境
originator: kouko
kind: engineering
needs-design: no — 修復既有技能與 hook 的執行環境，不新增使用者輸入介面或跨物件流程
status: confirmed 2026-10-21
publication: automatic — authorized 2026-10-21 by kouko

## Problem
新機器上的 Python 可能缺少 Loom 檢查所需的版本或套件，導致使用者在流程入口看到套件匯入錯誤，無法繼續工作。不同入口選用的 Python 也可能不同，使用者即使修好其中一處，仍可能在另一處遇到相同問題。

## Proposed outcome
Loom agent 在主機具備可用安裝工具、網路或所需快取，以及必要寫入權限時，能自行修復 Loom 的檢查環境並重新執行原有檢查；條件不足時明確指出未完成的原因，而不改變使用者專案自己的測試環境。

## Acceptance
1. 在有可用安裝工具、網路或所需快取，以及必要寫入權限的乾淨環境中，遇到缺少 Python、Python 過舊或缺少必要套件時，Loom agent 能自行修復並重新執行檢查，使用者不必手動安裝這些 Python 元件。
2. 修復後，即使主機預設的 Python 仍不符合需求，現有技能與各主機 hook 都能使用可工作的環境執行原有檢查。
3. 缺少安裝工具、網路／快取或寫入權限而無法修復時，使用者能看到具體障礙與可執行的處理方法；環境故障不會被誤報為合約過舊或檢查通過。
4. 環境已備妥而網路不可用時，Loom 仍能執行檢查。
5. 由 Loom 執行使用者專案的測試時，測試所用的 Python、套件與結果和專案直接執行時一致。
6. 原有合約檢查、規則與各 hook 對成功、失敗及無效輸入的處理仍可用。

## Constraints
- 保留 Loom 現有檢查與審查規則，不因執行環境故障略過必要檢查。
- 保留使用者專案原有的測試執行環境。

## Out of scope
- 更動使用者專案本身的語言或工具鏈。
- 為讓使用者直接使用舊版 Python 而降低 Loom 的 Python 版本需求。
- 自行重寫 TOML／YAML 解析器，或把第三方套件直接加進使用者專案。
- 本次改寫 Loom checker 為 Go；在本次修復完成後另行深入研究。

## Open questions
- none
