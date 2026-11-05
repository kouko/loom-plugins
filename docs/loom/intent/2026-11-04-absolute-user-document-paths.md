# 簡短的文件交付規則
originator: kouko
kind: engineering
needs-design: no — engineering guidance for conversation output in skills and hooks; no new interface surface or multi-state behaviour
status: confirmed 2026-11-05
intent_confirmed_sha: 96a898be40d0129814e931b9090c718d9c740d3e
publication: automatic — authorized 2026-11-04 by kouko

scope-revision: 2026-11-05 — 使用者以「那就改定位實作吧」確認實作縮小後的文件交付規則；延續同一變更，既有程序採用率與審查結果不代表修訂版已通過。

## Problem
使用者收到文件位置時，需要能找到該次專案或 worktree 中的正確文件。原方案把所有對話中的文件位置都納入規範，後續又探索強制 realpath 與跨終端點擊；這些要求超出文件交付本身的需要。使用者回報 Ghostty＋herdr 可用 Cmd＋Shift 點擊，但換行會截斷目標；此問題尚未由本方案解決。

## Proposed outcome
用一條簡短規則規範文件交付：交付本機文件時提供它的實際絕對位置；已確認支援本機 Markdown 連結時，以相對路徑為連結文字、絕對路徑為目標，外部文件可用檔名；不支援或支援情況未知時，顯示完整絕對路徑。檔案內的可攜式引用保持不變。

## Acceptance
1. loom-code、loom-design 與 loom-workflow 交付本機文件時，提供該文件的實際絕對位置；一般敘述中的檔名、引用的原文與範例不必全部轉換。
2. 已確認支援本機 Markdown 連結的環境使用相對路徑文字與絕對路徑目標，外部文件可用檔名；不支援或支援情況未知時顯示完整絕對路徑，不承諾可以點擊。
3. 交付位置指向當次專案、worktree 或專案外的實際文件；不寫死開發者目錄，不指定必須使用 realpath 或逐字比對程序。
4. 插件內部資源引用、版本控制內的文件連結與結構化資料中的相對路徑契約保持可攜性。

## Constraints
- 修改範圍為 Loom 家族的文件交付指引與直接相關測試；規則保持簡短，不新增攔截器、路徑服務或相容性設定。
- 支援情況採用已知的介面契約；不為每次交付探測環境，未知時直接採用完整路徑。
- 遵守既有 skill bundled file 相對路徑規約。
- 本輪實作縮小後的交付規則，重新取得驗收與審查證據；不更新已安裝插件或合併 PR。

## Out of scope
- 將所有對話中的路徑字串或儲存庫文件內的連結全面改成絕對路徑。
- 強制 realpath、shell 產生 Markdown、逐字比對或新增輸出攔截器。
- 保證所有 agent、terminal 或編輯器都能點擊，或修復終端換行截斷。
- 全域禁止所有介面使用 file URI；輸出格式遵守已知介面契約。
- 更改遠端網址、終端設定、更新已安裝插件或合併至 main。

## Open questions
- none
