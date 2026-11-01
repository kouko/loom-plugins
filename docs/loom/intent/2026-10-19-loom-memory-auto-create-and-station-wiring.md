# Auto-create store and station wiring for loom-memory
originator: kouko
kind: engineering
needs-design: no — engineering changes to skill files and scripts, no declared interface surface
status: confirmed 2026-10-20
publication: automatic — authorized 2026-10-20 by kouko

## Problem
loom-memory 的 Record 操作在新 repo 裡從未觸發。原因是沒有「初始化記憶庫」的操作——Record 需要先讀 `index.md`，但如果記憶庫根本不存在，就沒有任何路徑讓它發生。加上沒有站位呼叫 loom-memory（closing-review 只做散文提醒，ship 只呼叫 git-memory），持久教訓只存在於 agent 的內建記憶裡，從不寫入 repo。

## Proposed outcome
1. Record 操作自動偵測記憶庫是否存在：若不存在，從 template 建立 `docs/loom/memory/` 目錄（含 README.md 和 index.md），然後繼續記錄。
2. ship 站在整理 commit 時一併分流持久教訓到 loom-memory，與 git-memory 的分流對稱。

## Acceptance
1. 在一個沒有 `docs/loom/memory/` 的 repo，執行 Record 時，store 被自動建立（含 README.md 和 index.md），概念檔寫入，index 重建，`validate` 通過。
2. ship 站在 git-memory 分流之後，也分流持久教訓到 loom-memory（概念檔存在）。
3. Recall 行為不變：absent store 仍是正常 no-memory result，不會觸發建立。
4. Retire 行為不變：需要使用者明確同意才刪。
5. 對新自動建立的 store 跑 `validate` 過得過。
6. 對已存在的 store，現有行為不變（回歸）。

## Constraints
- git-memory 與 loom-memory 的邊界不變。
- 沒有新增 checker gate。
- Record 的分類過濾規則不變（0–1 durable lesson per change 是正常）。

## Out of scope
- 匯入舊格式 store（migrate_legacy_store.py 仍為明確操作）。
- 新增任何 checker gate。
- 讓任何站位硬呼叫 loom-memory（四個操作仍是被動的）。
- 結案報告的教訓判斷行（選項 B，使用者 2026-10-20 決定選 A）——若 A 上線後觀察到教訓仍常被漏掉，再開新 change 加回。

## Open questions
- none