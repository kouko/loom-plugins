---
title: "為什麼聊天圖表預設不用 Mermaid"
type: loom-visualization
date: 2026-09-14
tags:
  - loom-visualization
  - blind-run
aliases: []
source: "/private/tmp/claude-501/-Users-kouko--herdr-worktrees-loom-plugins-loom-visualization/30f9cf4e-fddc-43dd-84bf-3c3c97261377/scratchpad/clean/docs/loom/2026-09-14-loom-visualization/spec.md"
source_mode: "file"
language: zh-TW
status: completed
processed_at: "2026-09-14T12:00:00+08:00"
timezone: Asia/Taipei
llm_provider: anthropic
llm_model: "claude-opus-5"
generator: "loom-workflow:loom-visualization"
arcs: 1
nodes: 6
layout: "rows 3/3"
verified: "pass --render @ 868b680416db"
fidelity_checked: ""
---

### 概述

在任何能被環境變數辨識出來的客戶端裡，聊天圖表一律用表格加 ASCII，Mermaid 只留給沒有 shell 的 claude.ai 或 Claude Desktop 對話。

### 推理鏈

#### 客戶端判斷規則怎麼來的

規格裡「客戶端判斷」這一條設計決定背後的推理。

```mermaid
graph TB
subgraph r1["問題與證據"]
direction LR
  A["<div style='text-align:left'>問題<br/>━━━━━━<br/>• Mermaid 原始碼常被原樣顯示<br/>• 讀者看到的是一堆語法</div>"]
  B["<div style='text-align:left'>客戶端證據<br/>━━━━━━<br/>• Claude Code 顯示原始碼<br/>• Codex 未驗證</div>"]
  C["<div style='text-align:left'>可偵測訊號<br/>━━━━━━<br/>• CLAUDECODE 環境變數<br/>• CODEX_THREAD_ID 等</div>"]
end
subgraph r2["取捨與結論"]
direction LR
  D["<div style='text-align:left'>錯誤代價不對稱<br/>━━━━━━<br/>• 選錯 Mermaid 讀者看原始碼<br/>• 選錯 ASCII 仍可讀</div>"]
  E["<div style='text-align:left'>否決工具名偵測<br/>━━━━━━<br/>• 只在單一宿主驗證過</div>"]
  F["<div style='text-align:left'>結論<br/>━━━━━━<br/>• 偵測到的客戶端一律 mermaid false<br/>• 無 shell 的對話才可用 Mermaid</div>"]
end
A -->|查各家實況| B
B -->|需要辨識手段| C
r1 -->|比較選錯的後果| r2
D -->|排除不穩訊號| E
E ==>|定案| F
style A fill:#f8f9fa,stroke:#868e96,stroke-width:2px
style B fill:#fff4e6,stroke:#e8590c,stroke-width:2px
style C fill:#fff4e6,stroke:#e8590c,stroke-width:2px
style D fill:#e5dbff,stroke:#7048e8,stroke-width:2px
style E fill:#ffe3e3,stroke:#e03131,stroke-width:2px
style F fill:#c5f6fa,stroke:#0c8599,stroke-width:2px
```

##### A — 問題

- **主張**：在程式助手的聊天裡，Mermaid 常常顯示成原始碼。
- **依據**：規格的現況描述指出終端機會原樣顯示 Mermaid。
- **這一步改變了什麼**：確定「看起來漂亮」不能當選擇依據。

##### B — 客戶端證據

- **主張**：Claude Code 各介面顯示原始碼，Codex 未經驗證。
- **依據**：規格引用的客戶端能力對照表。
- **這一步改變了什麼**：沒有一個可偵測的客戶端被確認能渲染。

##### C — 可偵測訊號

- **主張**：可以用環境變數分辨 Claude Code、Codex、Gemini CLI。
- **依據**：規格列出的偵測規則。
- **這一步改變了什麼**：判斷可以交給腳本，而不是模型的感覺。

##### D — 錯誤代價不對稱

- **主張**：選錯 Mermaid 的代價比選錯 ASCII 大。
- **依據**：規格原文的理由。
- **這一步改變了什麼**：預設往保守的一側倒。

> a wrong Mermaid choice shows the user raw source, a wrong ASCII choice still reads

##### E — 否決工具名偵測

- **主張**：不用可用工具名稱當主要訊號。
- **依據**：規格的替代方案一節：只在一個宿主上驗證過。
- **這一步改變了什麼**：只保留在無 shell 對話這一種情況。

##### F — 結論

- **主張**：偵測得到的客戶端一律不用 Mermaid。
- **依據**：前面五步合起來。
- **這一步改變了什麼**：技能的預設形式是表格加 ASCII。

> `mermaid` is `false` for every environment-detected client in this change, because each is documented or reported to show Mermaid source raw, or is unverified.

### 岔路

| 考慮過的選項 | 否決理由 |
|---|---|
| 從可用工具名稱判斷客戶端 | 只在一個宿主驗證過 |
| 允許 Codex IDE 擴充用 Mermaid | 只有一則使用者回報，且環境上分不出 CLI |

---

本頁是規格中一條設計決定的推理整理；要照做的人請以規格原文為準。
