# 把 loom-code 升版到 3.7.2,讓 #30 與 #31 真正發到已安裝的副本

originator: kouko
kind: engineering
needs-design: no — 只動版本字串、changelog 與 README,不是宣告的介面表面(`**/cli/**`、`**/api/**`、`**/commands/**`、`**/*.tsx`、`**/templates/**`)
evidence: [loom-code/plugin.json, loom-code/.claude-plugin/plugin.json, loom-code/.codex-plugin/plugin.json, loom-code/CHANGELOG.md]
status: confirmed 2026-09-19
publication: automatic — authorized 2026-09-19 by kouko

## Problem

`plugin.json` 的版本從 2026-09-16 起停在 `3.7.1`。#30(「發佈被擋時指出合法路徑」)在 2026-09-18 合併時沒有跟著升版,#31 隔天合併也一樣。`claude plugin update` 只比對版本字串,版本沒動就回報「已是最新版」,什麼都不刷新——任何用這個指令裝 loom-code 的人永遠拿不到這兩個修正。

這件事有獨立證據:2026-09-19 凌晨,一個跟本次工作無關的 session,在 #30 合併七小時後,用已安裝的 `3.7.1` 撞到 #30 修正前的原始拒絕文字(只有「找到 0 份」和格式問題,沒有 #30 新增的路徑說明),接下來三小時嘗試沒有文件記載的繞路方法。

## Proposed outcome

`claude plugin update loom-code@loom` 能讓使用者拿到 #30 與 #31 的內容。

## Acceptance

1. `loom-code/plugin.json`、`.claude-plugin/plugin.json`、`.codex-plugin/plugin.json` 三份版本字串一致,且高於 `3.7.1`。
2. `CHANGELOG.md` 有一則新版本條目,說明這是純升版且原因是什麼。
3. 三語 README 與根目錄 README 的版本字串與上述三份 manifest 一致。
4. 既有測試全部通過,包含釘住版本字串的測試。

## Constraints

- 不改任何站別說明、規則、契約 manifest 版本。
- 機器面輸出(commit、測試、changelog)維持英文。

## Out of scope

- 對 #30 本身的範圍或降級討論——那是另一件事,這裡只處理「發不出去」的問題。

## Open questions

- none
