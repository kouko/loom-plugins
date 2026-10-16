# skill-retro

[English](README.md) | [日本語](README.ja.md) | **繁體中文**

分析多次 Claude Code 與 Codex 開發紀錄，找出已安裝 skill 的反覆問題。提案可以針對其指示，或與該 skill 直接相關的 plugin 註冊、載入、hook、附帶腳本及相依 connector。回顧只產出審閱資料；選定的變更交由獨立實作流程處理。

舊呼叫名稱 `distill-sessions` 已改為 `skill-retro`。操作規則見 [SKILL.md](SKILL.md)。

## 運作方式

1. `scripts/main.py` 讀取支援的本機紀錄並依可觀察的摩擦訊號排序；JSON 寫到 `top.json`，預覽摘要寫到 stderr。
2. 使用者明確同意外送選定的紀錄內容後，逐筆分析 agent 產出已分類的 Memory Item。收集至 `merged.json` 時保留來源 session 與目標 skill。
3. `scripts/propose.py` 產出各目標的提案。至少兩個不同 session 才升格為反覆問題；單次觀察維持待補證。指示問題需要真實的 SKILL.md 章節；整合問題需要直接相關的原始碼位置，不虛構章節錨點。
4. 審閱提案後，將選定變更交給獨立實作流程。回顧本身不套用修改。

收集格式與宿主派遣方式見 [執行協定](references/runtime-protocol.md)。

## Installation

此 skill 隨 `loom-workflow` plugin 提供。透過 `loom` marketplace 安裝：

```sh
# Claude Code
claude plugin marketplace add https://github.com/kouko/loom-plugins.git
claude plugin install loom-workflow@loom

# Codex
codex plugin marketplace add https://github.com/kouko/loom-plugins.git
codex plugin add loom-workflow@loom
```

安裝包含本次改名的版本後，於 Claude Code 呼叫 `loom-workflow:skill-retro`，或請 Codex 使用 `skill-retro`。舊名稱不是可呼叫別名。Python 腳本只用標準函式庫，需 Python 3.11 以上。

## Quick start

從 repository 根目錄執行本機預覽；此步驟不外送 session 資料：

```sh
python3 loom-workflow/skills/skill-retro/scripts/main.py \
  --target-skill-pattern 'loom-code:*' > top.json
```

排序摘要會出現在 stderr。檢視目標後，明確同意要交給分析 agent 的紀錄範圍。依[執行協定](references/runtime-protocol.md)收集各分析結果至 `merged.json`，再產生審閱檔：

```sh
python3 loom-workflow/skills/skill-retro/scripts/propose.py \
  --input merged.json \
  --target-skill /path/to/target/SKILL.md \
  --output proposals.md
```

`propose.py` 讀取目標 SKILL.md，只寫入 `proposals.md`。缺少整合來源的觀察另列為待調查候選，不放入 `merged.json`；單次觀察仍待補證。

## Configuration

`main.py` 可用 `--config /path/to/thresholds.json` 載入部分 JSON 門檻設定。六個門檻與含義見[執行協定](references/runtime-protocol.md#configuration-meanings)。常用參數如下：

- `--target-skill-pattern`（預設 `loom-code:*`）
- `--top-n`（預設 `5`）
- `--max-trajectories-per-skill`（預設 `5`，計算派遣次數）
- `--project-root`（覆寫 Claude 專案紀錄目錄，主要供測試）
- `--facets-root`（覆寫 Claude `/insights` facet 目錄，主要供測試）

## 授權

此 skill 屬於 [loom-plugins](https://github.com/kouko/loom-plugins) repository，採用其中的 [MIT 授權](https://github.com/kouko/loom-plugins/blob/main/LICENSE)。

### 第三方歸屬

`agents/` 中的失敗與成功分析 prompt 改作自 Apache 2.0 授權的 [Trace2Skill](https://github.com/Qwen-Applications/Trace2Skill)（[論文](https://arxiv.org/abs/2603.25158)）。轉載這些改作內容時應保留上游歸屬。
