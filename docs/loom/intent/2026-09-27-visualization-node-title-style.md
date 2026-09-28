# 統一 loom-visualization 框狀節點的文字結構：標題／分隔線／內文
originator: kouko
kind: engineering
needs-design: yes — the diff covers the declared `**/templates/**` interface surface, and node text behaviour is multi-object (11 information shapes × ASCII/Mermaid × 6 generators) with no spec covering it
status: confirmed 2026-09-27

## Problem
loom-visualization 畫出的節點沒有統一的內部結構。產生器把節點文字當單一 label 字串渲染：`gen_flow.py`、`gen_tree.py`、`gen_arch.py` 支援以 `\n` 分行的標籤，`gen_seq.py` 與 `gen_bar.py` 直接拒絕多行；聊天用 Mermaid template 只寫一個純字串標籤。整個 skill 只有 page-mode 推理頁（`references/mermaid-cot-spec.md`）定義過「標題＋分隔線＋條列」的節點結構。結果是：kouko 在 coding chat 看到的每個框只有一行無錨點的字串，分不出「這個節點是什麼」與「它說了什麼」；節點需要放多於幾個字時，skill 沒有規定的位置放細節，長標籤折行難讀，或內容直接掉出圖外。

## Proposed outcome
skill 的 ASCII 產生器與聊天用 Mermaid template，凡畫成「框」的節點一律呈現三段結構：標題列、框內分隔線、內文；內文是可換行的長文，或以固定記號開頭的條列。長內文在框內換行而非無限加寬；對齊檢查（`scripts/align.py`）與 Mermaid 解析器檢查持續作為閘。

節點結構是容器而非字數要求：只有一個詞可寫的節點不畫空分隔線——它應擴寫成帶資訊的片語，或自圖中移除。配對的內容規則（何時節點有話說、何時刪節點）與容器格式一起寫入 skill 文件，避免 agent 為湊滿格式灌水。

## Acceptance
1. 用產生器輸出流程／層級／架構圖（樣本含中日文標籤與長內文）時，有內文的框狀節點顯示標題、框內分隔線、內文三段；長內文在框內換行；輸出通過 `scripts/align.py`。
2. 分支決策、狀態生命週期、推理鏈三個 template 的 ASCII 與 Mermaid 形式採用相同節點結構；所有更新過的 Mermaid 範例通過 Mermaid 解析器檢查。
3. 節點結構規範（兩種內文形式、分隔線記號、條列記號）與內容規則（只寫得出一個詞的節點應擴寫成帶資訊的片語，或自圖中移除；不畫空分隔線）寫入 skill 文件；verify 流程能標記偏離該結構的輸出。
4. 非框狀文字槽——箭頭／邊標籤、表格儲存格、數值標籤、sequence 參與者與訊息——維持單行；`seq` 與 `bar` 產生器對多行輸入的既有行為不變。
5. 套件測試全數通過。

## Constraints
- 產生器維持僅用 Python 標準庫；skill 資料夾扁平、SKILL.md token 上限、runtime contract citations 等 repo 慣例照舊。
- 對齊閘不變：含 CJK 的輸出必須通過 `scripts/align.py`，不得目測。
- 節點樣式以使用者 2026-09-27 提供的 mock 為準：標題列靠左、框內水平分隔線、以 `*` 開頭的條列或可換行長文（標題與內文皆靠左，使用者 2026-09-27 選定）。

## Out of scope
- 非框狀文字槽（箭頭／邊標籤、表格儲存格、數值標籤、sequence 參與者名與訊息標籤）——維持單行（使用者 2026-09-27 選定範圍 A）。
- page-mode 推理頁（`references/mermaid-cot-spec.md`）的節點結構——已是標題／分隔線／條列，不在此變更內調整。
- Obsidian vault 圖表，以及 commit／PR／repo 文件的圖表規則——既有 boundary 不變。
- 表格類輸出（option comparison、data model）與數值圖（quantity bar）的呈現形式。

## Open questions
- none
