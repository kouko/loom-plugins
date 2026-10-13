# 完成沒有測試 runner 的對抗測試轉正修正
originator: kouko
kind: engineering
needs-design: no — 補齊既有內部驗證的審查依據，不新增使用者介面或跨物件行為
evidence: [docs/loom/intent/2026-10-12-runnerless-probe-graduation.md, docs/loom/2026-10-12-runnerless-probe-graduation/acceptance-test-report.md, loom-code/scripts/loom_checker/probes.py, loom-code/skills/closing-review/references/lenses.md]
status: confirmed 2026-10-13
publication: automatic — authorized 2026-10-13 by kouko

## Problem
原本的對抗測試轉正修正已通過測試與獨立驗收，但終輪審查發現環境命令的辨識缺少可查核的官方依據，因此修正仍無法完成審查與交付。使用沒有特定測試 runner 的專案，仍拿不到能正式使用的修正版本。

## Proposed outcome
補齊既有修正的審查依據，重新驗證原本的轉正行為，讓符合要求的變更完成最終驗證並交付。

## Acceptance
1. 沒有特定測試 runner、直接宣告 pytest 套件指令的專案，將抓到缺陷的對抗測試移入正式套件後，能把該檔案記為對抗執行並完成 finalization。
2. 同樣的專案若將檔案移至正式套件未收集的位置，finalization 仍會拒絕該檔案。
3. 已有測試 runner 的專案，在 runner 指向專案根目錄或既有測試目錄時，能正確判定正式套件是否收集該檔案。
4. 透過既有 Conda 環境命令執行轉正測試的專案，能將實際執行該檔案的命令記為對抗執行；沒有執行該檔案的命令仍會被拒絕。
5. 環境命令的辨識依據可由官方文件查核，最終審查能對已驗證的修正產生與內容相符的證明。

## Constraints
- 保留原本四條驗收條件及對抗測試轉正要求。
- 保留直接以 `package-tests` 宣告正式測試指令的用法，不強制專案新增測試 runner。
- 不降低對抗測試執行、數量及 `concern:` 的驗證要求。

## Out of scope
- 改造 Claude Code 的非互動呼叫、用量管理或外部審查流程。
- 修正 Codex app-server 的模型探索失敗。
- 保證支援所有測試框架與環境命令。

## Open questions
- none
