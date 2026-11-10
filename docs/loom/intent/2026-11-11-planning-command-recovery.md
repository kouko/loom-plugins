# 讓規劃工具的呼叫錯誤可以直接修正並繼續工作
originator: kouko
kind: engineering
needs-design: yes — 調整工具的命令說明與錯誤輸出，目前沒有涵蓋此修復行為的介面規格。
evidence: [docs/loom/research/2026-11-11-planning-launcher-argument-mismatch.md]
intent_confirmed_sha: bcc06047c47a839f2a2c5b719c1cac436834c346
status: confirmed 2026-11-11
publication: automatic — authorized 2026-11-11 by kouko

## Problem
使用者遇到 Codex 已保存意圖，卻因規劃工具的參數格式不符而停在規劃前的情況。本機 Codex 與歷史 Claude Code 記錄亦有呼叫失敗、必須額外查找用法才能繼續的現象，增加等待與重試成本。

## Proposed outcome
代理能辨認並修正已觀察到的規劃工具呼叫錯誤，取得足夠且一致的用法資訊後繼續規劃。

## Acceptance
1. 對已觀察到的錯誤呼叫，工具提供的資訊足以讓未參與修改的代理修正命令並成功完成規劃檢查。
2. 工具的使用說明能查到有效的規劃檢查呼叫方式，且範例與實際支援的格式一致。
3. 原有正確呼叫仍正常運作，錯誤呼叫不會被誤報成檢查成功。

## Constraints
- 優先處理此問題；前一項技能審查適用範圍修正保留，分開交付。
- 注意複雜度，採取能處理已證實問題的最小修正。
- 區分已重現的本機原因與另一台 Codex 尚未取得原始錯誤的情況，不宣稱後者已確診。

## Out of scope
- 技能審查適用範圍、回顧統計與其他已列出的改善項目。
- 另一台機器的直接操作、安裝或設定變更。

## Open questions
- none
