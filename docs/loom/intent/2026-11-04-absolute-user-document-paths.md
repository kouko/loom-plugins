# 對話中的文件位置統一使用絕對路徑
originator: kouko
kind: engineering
needs-design: no — engineering guidance for conversation output in skills and hooks; no new interface surface or multi-state behaviour
status: confirmed 2026-11-04
intent_confirmed_sha: 96a898be40d0129814e931b9090c718d9c740d3e
publication: automatic — authorized 2026-11-04 by kouko

## Problem
使用者指出，Loom 在對話中給文件位置時使用相對路徑，並希望統一為絕對路徑。目前檢視的共用開場提示與站點指引沒有統一要求將交給使用者的本機文件位置轉為絕對路徑。

## Proposed outcome
Loom 在對話中提供本機文件位置時，一律提供符合當下工作目錄與檔案實際位置的絕對路徑。

## Acceptance
1. Loom 對話中提供給使用者的本機文件位置皆為絕對路徑，涵蓋 loom-code、loom-design 與 loom-workflow 的文件交付。
2. 支援本機文件連結的對話環境使用絕對路徑作為連結目標；顯示名稱可保留簡短檔名。
3. 在不同專案目錄與 worktree 中交付文件時，路徑均指向該次工作的實際文件位置，不固定使用開發者的電腦路徑。
4. 插件內部資源引用、版本控制內的文件連結與結構化資料中的相對路徑契約保持可攜性。

## Constraints
- 修改範圍為 Loom 家族在對話中交給使用者的本機文件位置。
- 遵守既有 skill bundled file 相對路徑規約。

## Out of scope
- 將儲存庫文件內的連結或插件內部資源引用全面改為絕對路徑。
- 更改遠端網址。
- 更新已安裝的插件副本或合併至 main。

## Open questions
- none
