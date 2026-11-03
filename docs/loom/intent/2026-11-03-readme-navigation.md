# README 詳細說明與三層導覽
originator: kouko
kind: engineering
needs-design: no — human-facing documentation and navigation, without runtime behavior changes
status: confirmed 2026-11-03
intent_confirmed_sha: 3ac2263726848082ed5d04066cc1d465bd005fc7
publication: automatic — authorized 2026-11-03 by kouko

## Problem

使用者從專案清單無法直接找到各 plugin 與 skill 的詳細說明，許多 skill 尚無 README；現有大圖也混合主要流程與依需要使用的工具。

## Proposed outcome

使用者能從專案、plugin、skill 三層 README 找到詳細使用說明並返回上層；主要流程與工具清單分開呈現。

## Acceptance

1. 所有目前的 27 個 skill 都有給使用者閱讀的 README，說明用途、使用方式、產出與限制。
2. 專案 README 的 plugin 與 skill 清單，以及各 plugin 的 skill 清單，都直接連到對應的 README。
3. 各 skill README 能返回專案與 plugin，並連到相關技能與自身執行規則；導覽中的本機相對連結都有有效目的地。
4. 主要流程與工具清單分開；三語圖保留需要設計、審查退回、探索與交付的正確條件。

## Constraints

- 使用既有分支 docs/readme-flow-tool-separation；保留先前已提交的流程圖調整 4088c3c4。
- 新增詳細頁以英文撰寫；既有日文、繁中版同步連結，有同語言頁時優先使用，否則連到英文。
- 不改動 SKILL.md、執行程式、hook 或工作流程契約。
- 本 intent 補記已獲授權的文件工作，不宣稱在實作前已執行 Loom 入口站。
- 範圍依據：使用者先要求拆開流程與工具清單，後要求先 commit，再為每個 skill 撰寫 README 並做三層互連。
- 發布依據：使用者要求「可以幫我再獨立review一次嗎？ 沒問題的話就開始走合併流程」。合併仍待最終驗收報告呈現後的明確接受。
- agent-decided: release patch versions, synchronized manifests, changelog entries and version-pin checks are included before final review.

## Out of scope

- 為所有新增 skill 頁補上日文、繁中翻譯。
- 執行功能變更、重新設計 skill 或修復無關文件債務。
- 自動安裝或更新使用者已安裝的 plugin。

## Open questions

- none
