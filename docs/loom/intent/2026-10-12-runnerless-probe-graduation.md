# 讓沒有測試 runner 的專案也能完成對抗測試轉正
originator: kouko
kind: engineering
needs-design: no — 修正既有內部驗證行為，不新增使用者介面或跨物件流程
evidence: [loom-code/scripts/loom_checker/probes.py, loom-code/scripts/loom_checker/command_handlers/finalize.py, loom-code/tests/test_selection_finalize.py, loom-code/skills/closing-review/references/adversarial.md]
status: confirmed 2026-10-12
publication: automatic — authorized 2026-10-12 by kouko

## Problem
使用 Loom 的專案即使已將抓到缺陷的對抗測試移入每次都會執行的正式測試，若該專案直接以測試指令執行套件、沒有特定的測試 runner，finalize-review 仍會拒絕該測試。使用者必須保留不合理的暫存位置或額外建立 runner，才能繼續交付；使用環境命令執行單一測試時也可能遭到拒絕。

## Proposed outcome
Loom 能依專案既有的正式測試指令辨認已轉正的對抗測試，讓符合轉正要求的變更完成 finalization，並持續拒絕正式套件未收集的檔案與未真正執行測試的命令。

## Acceptance
1. 沒有特定測試 runner、直接宣告 pytest 套件指令的專案，將抓到缺陷的對抗測試移入正式套件後，能把該檔案記為對抗執行並完成 finalization。
2. 同樣的專案若將檔案移至正式套件未收集的位置，finalization 仍會拒絕該檔案。
3. 已有測試 runner 的專案，在 runner 指向專案根目錄或既有測試目錄時，能正確判定正式套件是否收集該檔案。
4. 透過既有 Conda 環境命令執行轉正測試的專案，能將實際執行該檔案的命令記為對抗執行；沒有執行該檔案的命令仍會被拒絕。

## Constraints
- 保留「抓到缺陷的對抗測試要移入之後每次改動都會執行的套件」的既有要求。
- 保留直接以 `package-tests` 宣告正式測試指令的既有用法，不強制專案新增測試 runner。
- 不降低現有對抗測試執行、數量及 `concern:` 的驗證要求。

## Out of scope
- 修正 Codex app-server 的模型探索失敗。
- 保證支援所有測試框架與環境命令。

## Open questions
- none
