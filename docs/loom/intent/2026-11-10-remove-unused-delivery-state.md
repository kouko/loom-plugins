# 清除未使用的交付狀態
originator: kouko
kind: engineering
needs-design: no — 僅清除內部未使用的型別值，不改變介面或執行行為
intent_confirmed_sha: e54af2333b133f8145819697c2890f4fc0c8e611
status: confirmed 2026-11-10
publication: automatic — authorized 2026-11-10 by kouko

## Problem
交付檢查的型別宣告仍包含實際不會產生的未授權狀態，讓維護者誤判可能收到的結果。

## Proposed outcome
交付結果的型別宣告與現有實作一致。

## Acceptance
1. 交付結果的型別宣告不再列出未使用的 unauthorized 狀態。
2. 既有交付檢查與發布授權檢查維持原有行為，相關測試通過。

## Constraints
- 僅針對 Claude Code 提出的未使用狀態問題做小修正。
- 遵循專案既有分支、審查與版本發布規定。

## Out of scope
- 新增交付狀態、修改發布授權政策或其他功能。
- 清理其他既有程式碼。

## Open questions
- none
