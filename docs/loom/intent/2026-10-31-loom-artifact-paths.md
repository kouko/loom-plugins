# 將 Loom 產生的檔案收在 docs/loom
originator: kouko
kind: engineering
needs-design: yes — 圖檔目的地是使用者直接存取的檔案介面，目前缺少從錯誤執行目錄呼叫時的行為規格
status: confirmed 2026-10-31
publication: automatic — authorized 2026-10-31 by kouko

## Problem
Loom 的圖表工具若從專案根目錄執行，會在根目錄建立 `diagrams/`；使用者因而無法確信 Loom 產生的相關檔案都在 `docs/loom` 內，合併後清理工作樹也可能被這些未追蹤檔案擋住。

## Proposed outcome
Loom 為每次變更產生的持久檔案可預期地收在 `docs/loom` 內，不會因呼叫工具時所在的目錄不同而散落到專案根目錄；專案共用文件維持現有位置。

## Acceptance
1. 已指定這次變更時，從專案根目錄建立 draw.io 圖，圖檔與文字投影都位於該變更的 `docs/loom` 目錄內，根目錄不新增 `diagrams/`。
2. 從該次變更目錄建立同一類圖，圖檔與文字投影仍位於相同的預期位置。
3. 無法確定這次變更的目錄、或要求更新 `docs/loom` 外的圖檔時，工具清楚拒絕寫入，且不會在 `docs/loom` 外產生或修改檔案。
4. 這項變更不移動或修改使用者原有的圖檔；原有的 Loom 變更紀錄仍可從原位置讀取。

## Constraints
- 範圍是每次變更產生的持久檔案，包含圖檔與文字投影；既有 intent、spec、plan、驗收報告等已在 `docs/loom` 的位置不改變。
- 專案共用的 `PRINCIPLES.md`、`DESIGN.md`、`ARCHITECTURE.md` 維持現有位置。
- 不改動既有未追蹤的根目錄 `diagrams/`。

## Out of scope
- 建置快取與作業系統暫存檔。
- 搬移既有圖檔及專案共用文件。
- 改變對既有外部圖檔的唯讀檢查能力。
- 跨工作階段的交接筆記（HANDOFF）與正常的程式碼、測試檔案。

## Open questions
- none
