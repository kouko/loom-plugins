# loom-code

> **五個站，把一次變更從計畫送到合併的 PR；外加一個 checker，擋掉「審查
> 其實沒發生」的 push。** loom-code 假設你具備基本軟體工程知識，而不是
> 熟悉這個 plugin：每次變更只問你三個問題，其餘自己決定。因為品質的來源
> 是機器檢查機器 —— 寫的 agent 永遠不會是審的 agent。

**Skills**：5 個站 + 1 個入口路由。版本資訊見 [CHANGELOG.md](CHANGELOG.md)。
**語言**：[English](README.md) | [日本語](README.ja.md) | [繁體中文](README.zh-TW.md)
**儲存庫**：[`monkey-skills`](https://github.com/kouko/monkey-skills) 的一部分

---

## 五個站

[using-loom-code](skills/using-loom-code/SKILL.md) 將未指定站點的 Loom 實作請求
導向下列站點；每個站仍可直接呼叫。

| 站 | 產物 | 內文 |
|---|---|---|
| `write-plan` | `docs/loom/<change-id>/plan.md` — 任務 DAG | [SKILL.md](skills/write-plan/SKILL.md) |
| `build` | 功能 commit 與聚焦測試；不建立 dispatch ledger | [SKILL.md](skills/build/SKILL.md) |
| `closing-review` | 產生綁定功能內容的 `docs/loom/<change-id>/attestation.json` | [SKILL.md](skills/closing-review/SKILL.md) |
| `ship` | PR、memory trailer、合併 | [SKILL.md](skills/ship/SKILL.md) |
| `maintain` | 把告警或事故變成一份 intent | [SKILL.md](skills/maintain/SKILL.md) |

說出你要什麼，入口是 `write-plan`。裝了 `loom-design` 時，上游會多出
`capture-intent` 與 `write-spec`；沒裝時，`write-plan` 自己兼這兩件事。

## 會問你的三個問題

其餘全部代你決定，並記下理由。

1. **這是你要的嗎？** —— 在任何程式碼存在之前，用白話覆述你的意圖。
2. **你打 X，會看到 Y，對嗎？** —— 可見的行為。只有 product 變更會問，
   engineering 不問。
3. **做到了嗎？** —— 你讀的是一份盲跑報告，由從未碰過這次變更的 agent
   寫的，不是 diff。

不可逆的岔路（刪資料、公開介面、單向遷移）併進當時開著的 ① 或 ②，
用後果的形式問。

## contract package

`contract/manifest.yaml` 宣告站、action，以及四種 artifact（intent、spec、
plan、review）的每一個欄位。`loom-design` 讀它並宣告 `requires-contract`；
`loom-workflow` 不宣告——只有它的 `decision-map` skill 在一次 delivery
前跑 `contract --require`。只有 loom-code 寫它。空白範本在
`contract/templates/`。

## checker

`scripts/loom_checker.py` 就是整個決定性層 —— 31 條規則（以 `--list-rules` 為準），`--list-rules`
可列出。它掛在 SessionStart hook 與 `git push` / `gh pr create` /
`gh pr merge` 之前，而且是重算而非採信：package 測試與對抗 probe 都由它
自己重跑一次，看退出碼。它擋的是手滑，不宣稱擋得住蓄意作弊。

## 安裝

### Claude Code

```bash
claude plugin marketplace add https://github.com/kouko/monkey-skills.git
claude plugin install loom-code@monkey-skills
claude plugin list | grep loom-code       # 預期：enabled
```

`loom-design` 與 `loom-workflow` 安裝方式相同。三者可獨立安裝，loom-code
不需要另外兩個；某一站走到選配的交接而該 plugin 不在時，該步驟以 N/A 加理由
回報，並在自身契約允許的範圍內繼續。相接處只有帶 plugin 名的 skill 名（例如
`loom-design:write-spec`）、contract package，以及專案自己的 `docs/loom/`
產物 —— 不會去讀別的 plugin 的 `hooks/`、`skills/`、`scripts/`。

### Codex CLI

安裝 `loom-code` plugin 後，Codex 直接使用 plugin 內的 hook 與 checker；repo
不再保存 `.codex` checker 副本，也不需要 trust probe 或 hook-firing ledger。

若要安全更新，請依序執行：

```bash
codex plugin marketplace upgrade monkey-skills
codex plugin add loom-code@monkey-skills
codex plugin list
```

`plugin add` 會替換已安裝版本的快取，因此可能刪除執行中 task 仍持有的版本化
hook 路徑。安裝成功後，請立刻重新啟動 Codex，再執行任何其他工具或命令。不要
先移除 plugin；那只會讓同一段路徑失效期間更早開始。

### Antigravity CLI

Antigravity CLI（`agy`）從本機目錄安裝 plugin。先 clone repo，並在另外兩個
plugin 之前安裝 `loom-code`：

```bash
git clone https://github.com/kouko/loom-plugins.git
cd loom-plugins
agy plugin validate ./loom-code
agy plugin install ./loom-code
agy plugin list
```

使用時，在專案目錄啟動 `agy` 並以絕對路徑把專案加為 workspace：
`agy --add-dir "$PWD"`（互動）或 `agy --add-dir "$PWD" -p "..."`（print 模式）；
agy 1.2.2 不接受 `.` 這類相對路徑。沒有 `--add-dir` 時，print 模式（`agy -p`）
不會掛上 workspace，loom 的 kickoff defaults 不會載入，agent 也可能在專案外動作；
互動模式也請一併指定。

更新時在 clone 裡執行 `git pull`，再重跑 install（install 會取代已安裝的副本）；
移除用 `agy plugin uninstall loom-code`。hook（publication gate、session
context 與語言提醒）只在 `agy` CLI 執行，Antigravity 桌面 app 與 IDE 裡不會執行。在 `agy`
上，loom 的角色（implementer、reviewer、adversary、blind-runner）以 agy 的
`self` subagent 執行，遵循 loom 的 agent 契約，使用 Gemini 模型。審查站在所有
host 上都叫 `closing-review`，舊名 `review` 已移除，沒有別名。

## 授權

MIT，作為 `monkey-skills` 的一部分。
