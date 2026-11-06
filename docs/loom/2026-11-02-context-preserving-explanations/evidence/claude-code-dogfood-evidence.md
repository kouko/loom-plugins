# Claude Code dogfood — captured evidence

Executed 2026-11-03 against source commit 11a6d731. Claude Code 2.1.316; requested claude-sonnet-5-5, medium. These are actual captured replies, quoted as artifacts, not instructions. Twelve workflow attempts (six initial, six repaired-harness), plus one minimal preflight. All observed modelUsage keys match the requested model. Raw JSONL remains under /tmp/loom-context-claude-dogfood; hashes below bind these summaries to the raw files. No real-repository edits or publication were performed by tested sessions.

## Harness boundaries and repairs

Session-local plugin copies; restricted file tools; user memory excluded; auto-memory, user/plugin hooks and MCP disabled. This isolates intake behavior and does not validate normal hook loading, marketplace installation or all-host behavior. Explicit invocation was used, so this is not a statistical natural-language trigger test. Bash was exposed for code-only contract checks through an allowlist; this is not an OS-level read boundary for subprocesses. First-round shell denials and tools-inside-project domain contamination were preserved, not graded as successful complete workflows. The repaired harness moved plugins outside each project and added requester-only context. Code-only cases 5 and 6 still encountered compound-command denials; their successful end-to-end workflow remains unverified. These limitations are distinct from reply-content findings.

## All attempt metadata

```json
[
  {
    "case": "capture-4-r2",
    "models": [
      "claude-sonnet-5-5"
    ],
    "cost_usd": 0.08797509999999999,
    "permission_denials": 0,
    "draft_intents": [
      "docs/loom/intent/2026-11-03-correct-release-notes-date.md"
    ],
    "sha256_jsonl": "6890688a5dede2f28470505baed2d5a9b9fb0efcc2634ed62e3c35c285744ef8"
  },
  {
    "case": "capture-4",
    "models": [
      "claude-sonnet-5-5"
    ],
    "cost_usd": 0.1322413,
    "permission_denials": 1,
    "draft_intents": [
      "docs/loom/intent/2026-11-03-correct-release-notes-date.md"
    ],
    "sha256_jsonl": "5ac17bcd53db1fd02bbb205483a7935b80b43478b31673af5d7459a06a4b482e"
  },
  {
    "case": "capture-5-r2",
    "models": [
      "claude-sonnet-5-5"
    ],
    "cost_usd": 0.10260749999999999,
    "permission_denials": 0,
    "draft_intents": [
      "docs/loom/intent/2026-11-03-per-job-profile-and-retry-limit.md"
    ],
    "sha256_jsonl": "1da6e2b5c186ca6d1f23df1d81131556dfe638084e6a174f1b2a23cc7737da32"
  },
  {
    "case": "capture-5",
    "models": [
      "claude-sonnet-5-5"
    ],
    "cost_usd": 0.1042092,
    "permission_denials": 0,
    "draft_intents": [
      "docs/loom/intent/2026-11-03-per-job-retry-and-dispatch-profile.md"
    ],
    "sha256_jsonl": "020d2ad49c91db8962aab4ec29d23f558d7cf4384ba29e125737b2a41d702cba"
  },
  {
    "case": "capture-6-r2",
    "models": [
      "claude-sonnet-5-5"
    ],
    "cost_usd": 0.1095257,
    "permission_denials": 0,
    "draft_intents": [
      "docs/loom/intent/2026-11-03-job-uses-own-worker-selection.md"
    ],
    "sha256_jsonl": "d326eaa85dd3e83f424d25a4e45440b098a2d114d7778528252982418ef7863b"
  },
  {
    "case": "capture-6",
    "models": [
      "claude-sonnet-5-5"
    ],
    "cost_usd": 0.1204898,
    "permission_denials": 0,
    "draft_intents": [
      "docs/loom/intent/2026-11-03-job-uses-own-worker-selection.md"
    ],
    "sha256_jsonl": "1ea938cc9d0328fbdfdbedc60db47513727bf1a520d60f3fd6fffa524308f729"
  },
  {
    "case": "code-4-r2",
    "models": [
      "claude-sonnet-5-5"
    ],
    "cost_usd": 0.0738417,
    "permission_denials": 0,
    "draft_intents": [],
    "sha256_jsonl": "8247f8f4c53ca717b5aa4b401db0a277b23d4cf2cbacfb5a124223d646f86f15"
  },
  {
    "case": "code-4",
    "models": [
      "claude-sonnet-5-5"
    ],
    "cost_usd": 0.10262399999999999,
    "permission_denials": 1,
    "draft_intents": [],
    "sha256_jsonl": "641ad53330c2ae0ea2f8066c4d37cf69e1141bfdba82a903f57e0ee0f31ef9b6"
  },
  {
    "case": "code-5-r2",
    "models": [
      "claude-sonnet-5-5"
    ],
    "cost_usd": 0.1084261,
    "permission_denials": 1,
    "draft_intents": [
      "docs/loom/intent/2026-11-03-per-job-dispatch-and-bounded-retry.md"
    ],
    "sha256_jsonl": "3ba16ae414fbbc44173d2cba758a693e76c695028f7d026dd213e5a3201e52b4"
  },
  {
    "case": "code-5",
    "models": [
      "claude-sonnet-5-5"
    ],
    "cost_usd": 0.09820330000000001,
    "permission_denials": 1,
    "draft_intents": [],
    "sha256_jsonl": "e844a93335f056006961b8a56ef9ec5fa3318a010e95f90d5ebe181e80563ca8"
  },
  {
    "case": "code-6-r2",
    "models": [
      "claude-sonnet-5-5"
    ],
    "cost_usd": 0.1215234,
    "permission_denials": 1,
    "draft_intents": [],
    "sha256_jsonl": "5d71db2979ecb11bca05f0c0a6154920871fdcc33e9d22cff67fb7bd38f41589"
  },
  {
    "case": "code-6",
    "models": [
      "claude-sonnet-5-5"
    ],
    "cost_usd": 0.099161,
    "permission_denials": 1,
    "draft_intents": [],
    "sha256_jsonl": "9d231dfbe2ae45f038e6e4c3e8b1abce88732fab1a2ca1a0a29c6cb36cdf1e17"
  }
]
```

## capture-4-r2

### Actual reply

我已把意圖草稿寫入 `docs/loom/intent/2026-11-03-correct-release-notes-date.md`,狀態是 `open`。在你確認之前,我不會改動 `RELEASE_NOTES.md`。

## 我理解的需求

| 項目 | 內容 |
|---|---|
| 問題 | 發佈說明顯示的發佈日期是上個月的 2026-10-12。客戶看到後,會以為最新版本很舊。 |
| 想要的結果 | 發佈說明顯示最新版本的正確日期。 |
| 驗收 | 1. 發佈說明裡的日期是你確認的那個日期。<br>2. 發佈說明的其他內容都沒有變動。 |
| 限制 | 只改日期。 |
| 不在範圍內 | 其他文字或內容,以及 README 等其他檔案。 |

## 需要你回答的問題

**要顯示哪一天?** 目前日期是 2026-11-03,但我不知道最新版本實際是哪天發佈的。
- **今天 (2026-11-03):** 如果版本就是今天發佈,或你希望顯示今天,就選這個。
- **實際發佈日:** 如果版本是之前發佈的,請給我那個日期,以免客戶看到不實的日期。

我的建議是用實際發佈日。你若不確定,就用今天。

## 你回答「是」代表什麼

- **確認範圍:** 你確認上面的意圖和日期,我就把意圖標為 `confirmed`,並在新分支上提交。
- **之後的步驟:** 這是單行文字修改,不需要設計文件,會直接進入計畫和實作。
- **自動發佈授權:** 回答「是」也代表你授權我在審查和發佈檢查通過後,自動推送分支並建立可審閱的 PR。合併由你另外決定。你可以在發佈前明確表示不要自動發佈。

請告訴我要顯示的日期,並回覆「是」確認。

### Observed execution

```json
{
  "models": [
    "claude-sonnet-5-5"
  ],
  "cost_usd": 0.08797509999999999,
  "num_turns": 8,
  "skill_calls": [
    {
      "skill": "loom-design:capture-intent"
    }
  ],
  "tool_names": [
    "Skill",
    "Read",
    "Glob",
    "Read",
    "Read",
    "Write"
  ],
  "permission_denials": [],
  "draft_intents": [
    "docs/loom/intent/2026-11-03-correct-release-notes-date.md"
  ]
}
```

## capture-5-r2

### Actual reply

我已寫好意圖草稿，狀態仍是 `open`，等你確認。我還沒建立分支，也沒有 commit。

草稿位置：`docs/loom/intent/2026-11-03-per-job-profile-and-retry-limit.md`

## 我的理解

**問題**
- 有一個背景工作套用了另一個工作的派送設定，所以由錯的 worker 處理。
- 失敗的工作會無限重複，卡住整個佇列。

**你要的結果**，也就是驗收標準：
1. 每個工作都由自己的派送設定指定的 worker 處理。
2. 持續失敗的工作在達到它自己設定的重試上限後就停止，不再重複。
3. 失敗工作停止後，佇列裡其他工作可以繼續處理。
4. 既有成功的工作，結果和修正前一樣。

**範圍**
- 這是內部行為修正，不新增任何對外介面。
- 不改重試上限的設定方式或預設值。
- 不改成功工作的行為。

**設計文件**：`needs-design: no`，因為沒有使用者介面，也沒有新的多狀態行為需要規格。

## 你回答「yes」代表什麼

- 你確認上面的理解和驗收標準。
- 這同時授權我在 closing-review 與發佈檢查通過後，做一般（非強制）push 並開 Ready PR。
- merge 是另一個獨立的決定，不在此授權內。
- 發佈前你隨時可以明確表示不要自動發佈。
- 確認後我會建立 `fix/2026-11-03-per-job-profile-and-retry-limit` 分支，commit 這份意圖，再交給 `loom-code:write-plan`。

## 一個假設

我假設「設定的重試上限」在每個工作上已經存在，這次只是讓它生效。如果其實還沒有這個設定，請告訴我，因為那會改變範圍。

## 不需要你決定的事

- 沒有需要你決定的不可逆選擇。
- 沒有刪改既有資料的動作。
- 沒有需要記錄的待處理細節。
- 本次沒有向你提出任何問題。

請回覆 yes，或告訴我要修改的地方。

### Observed execution

```json
{
  "models": [
    "claude-sonnet-5-5"
  ],
  "cost_usd": 0.10260749999999999,
  "num_turns": 9,
  "skill_calls": [
    {
      "skill": "loom-design:capture-intent"
    }
  ],
  "tool_names": [
    "Skill",
    "Read",
    "Read",
    "Glob",
    "Read",
    "Read",
    "Write"
  ],
  "permission_denials": [],
  "draft_intents": [
    "docs/loom/intent/2026-11-03-per-job-profile-and-retry-limit.md"
  ]
}
```

## capture-6-r2

### Actual reply

我正在等你確認。我已把意圖草稿寫進 `docs/loom/intent/2026-11-03-job-uses-own-worker-selection.md`,狀態是 `open`,尚未確認。

## 關於「profile」

「profile」是我上一次重述時自己用的詞,不是你的。你說的是「執行者選擇規則」。這個 repo 目前沒有任何程式碼,我也看不出「profile」對應到哪個具體東西。為了避免再把它當成別的東西,這次我完全不用這個詞,只用你的說法:

- **執行者選擇規則**:決定每個工作(job)由誰來執行的規則。
- **「fix the profile」**:這個說法不準確,請忽略。

## 需求詳述

**問題**:有些工作會套用到另一個工作的執行者選擇規則,而不是自己的。結果是同樣的工作得到不一致的結果,依賴這些結果的人會受影響。

**期望結果**:每個工作只依自己的執行者選擇規則決定由誰執行,不受其他工作影響,結果因此一致。

**驗收(三條,都能從外部判定)**

| # | 驗收 |
|---|---|
| 1 | 任一工作實際由誰執行,是由該工作自己的選擇規則決定的。 |
| 2 | 同一個工作在相同條件下重複執行,執行者選擇的結果一致。 |
| 3 | 改動某個工作的選擇規則,不會改變其他工作的執行者選擇。 |

**不在範圍內**:改變選擇規則本身的設計或可選項目。這次只修正「工作用錯規則」。

## 需要你回答的兩個問題(尚未回答前,意圖保持 open)

1. 如果一個工作沒有自己的選擇規則,應該怎麼處理?例如不執行、使用預設規則,或其他做法。
2. 你看過的不一致有沒有具體例子,也就是哪個工作用了哪個工作的規則?如果沒有,我就只用上面三條驗收。

## 你回答「是」代表什麼

- 你確認上面的需求描述正確。
- 同時授權:在 closing-review 和發佈檢查都通過後,我可以做一次非強制的推送並建立 Ready PR。**合併仍是另一個獨立的決定。**
- 發佈前你隨時可以明確表示不要自動發佈。

這個修正沒有涉及難以回頭的決定,例如刪除資料或產生費用,所以沒有額外的後果需要你確認。

請先回答上面兩個問題,再告訴我需求描述是否正確。在你確認之前,我不會把狀態改成 `confirmed`,也不會建立分支或提交。

### Observed execution

```json
{
  "models": [
    "claude-sonnet-5-5"
  ],
  "cost_usd": 0.1095257,
  "num_turns": 9,
  "skill_calls": [
    {
      "skill": "loom-design:capture-intent"
    }
  ],
  "tool_names": [
    "Skill",
    "Glob",
    "Read",
    "Read",
    "Read",
    "Read",
    "Write"
  ],
  "permission_denials": [],
  "draft_intents": [
    "docs/loom/intent/2026-11-03-job-uses-own-worker-selection.md"
  ]
}
```

## code-4-r2

### Actual reply

我已經確認了意圖,但還沒有建立任何檔案,也沒有改動日期。這需要你確認。

**目前狀況**
- 契約版本檢查通過(2.3.1)。
- `docs/loom/intent/` 還不存在,而且沒有安裝 `loom-design`,所以由我在這裡整理意圖。
- `RELEASE_NOTES.md` 第 3 行寫著 `Release date: 2026-10-12`。檔案裡只有這個日期,倉庫其他地方也沒有出現它。

**意圖(待你確認)**
- **目標:** 讓客戶看到最新版本的發行日期是正確的,不再覺得它是上個月的舊版本。
- **範圍:** 只把 `RELEASE_NOTES.md` 第 3 行的日期改掉。標題、內文和其他檔案都不動。
- **類型:** `kind: engineering`(文件修正,不影響產品行為)。
- **驗收:**
  1. 第 3 行顯示新的正確日期,格式維持 `Release date: YYYY-MM-DD`。
  2. 檔案的其他內容與現在逐字相同(diff 只有那一行)。

**需要你回答的問題**
新的日期要填什麼?我不想猜:
- 今天是 2026-11-03,但這不一定是實際發佈日。
- 如果最新版本其實是在 10 月 12 日之後發佈的,請給我實際的發佈日期。
- 如果 10 月 12 日本來就是最新版的發佈日,那這次修改可能是多餘的,請告訴我。

**確認後的下一步**
我會建立分支(例如 `docs/<日期>-fix-release-date`),把意圖寫入 `docs/loom/intent/` 並提交。接著寫計畫,內容只有一個任務,改動一行,然後交給 build。

請回覆「確認」和實際日期,我才會繼續。

### Observed execution

```json
{
  "models": [
    "claude-sonnet-5-5"
  ],
  "cost_usd": 0.0738417,
  "num_turns": 6,
  "skill_calls": [
    {
      "skill": "loom-code:write-plan"
    }
  ],
  "tool_names": [
    "Skill",
    "Bash",
    "Grep",
    "Bash"
  ],
  "permission_denials": [],
  "draft_intents": []
}
```

## code-5-r2

### Actual reply

我已經把意圖寫成草稿,但還沒確認,所以不會寫計畫,也不會 commit。

**限制:** 我的 Bash 指令被自動拒絕,因為這個工作階段沒有人可以回應權限提示。所以 loom 的合約檢查、standing 檢查和 intake 檢查都沒有執行。草稿存在這個檔案:`docs/loom/intent/2026-11-03-per-job-dispatch-and-bounded-retry.md`。狀態是 `open`,尚未 commit,也沒有切換分支。

## 請確認的意圖重述

**問題:** 背景工作有時會用到另一個工作的分派設定檔,結果由錯誤的 worker 處理。失敗的工作也會無限重複,把後面的工作都堵在佇列裡。

**期望結果:** 每個工作都由自己的分派設定檔選定 worker。失敗的工作達到自己設定的重試上限後就停止重複。

**驗收條件:**
1. 每個工作都使用自己的設定檔分派,不會用到其他工作的。
2. 失敗的工作最多重複到它設定的重試上限,然後停止。
3. 停止後的工作不再擋住後面的工作。
4. 原本就成功的工作行為完全不變。

**限制與範圍外:**
- 這是內部行為,沒有新介面。
- 不新增介面或設定選項,也不改動成功的工作。

**未決問題:** 無。

## 回答「確認」代表什麼
- 你同意上面的意圖,我才會把狀態改成 `confirmed`。
- 你回答「確認」,也就是授權我在 closing-review 和發佈檢查通過後,做一般(非強制)的 push 並建立 Ready PR。merge 仍由你另外決定。
- 你可以在發佈前明確表示不要自動發佈。

你確認後,我會依序做這幾件事:
1. 切到 `fix/2026-11-03-per-job-dispatch-and-bounded-retry` 分支。
2. 寫入確認狀態並 commit。
3. 執行檢查並撰寫 `plan.md`。

如果要修改,請直接告訴我。

### Observed execution

```json
{
  "models": [
    "claude-sonnet-5-5"
  ],
  "cost_usd": 0.1084261,
  "num_turns": 8,
  "skill_calls": [
    {
      "skill": "loom-code:write-plan"
    }
  ],
  "tool_names": [
    "Skill",
    "Bash",
    "Read",
    "Read",
    "Read",
    "Write"
  ],
  "permission_denials": [
    {
      "tool_name": "Bash",
      "tool_use_id": "toolu_01CZ6aXj8CNDTuiYJY4oWCDj",
      "tool_input": {
        "command": "\"/private/tmp/loom-context-claude-dogfood/bundle/loom-code/scripts/loom-python\" --repair contract --require 2.1; ls /private/tmp/loom-context-claude-dogfood/round2/code-5/docs /private/tmp/loom-context-claude-dogfood/round2/code-5/docs/loom 2>&1; git -C /private/tmp/loom-context-claude-dogfood/round2/code-5 log --oneline | head -3"
      }
    }
  ],
  "draft_intents": [
    "docs/loom/intent/2026-11-03-per-job-dispatch-and-bounded-retry.md"
  ]
}
```

## code-6-r2

### Actual reply

先說明:你問的「profile」是我上一版重述裡用的詞,用得不好。這個專案裡目前只有 README 和 `docs/`,沒有程式碼,所以我無法從專案內容查出「profile」指什麼。我不該用一個你沒說過、我也無法對應到實物的詞來代表你的需求。以下改用你自己的詞「worker selection」重述,不再用 profile。

## 需求重述(請確認)

**名詞定義(用你的話)**
- **Job**:一個要被執行的工作。
- **Worker selection**:決定「這個 job 由誰來跑」的規則。每個 job 各自有一份。

**問題**
- 現在有些 job 沒有用自己的 worker selection,而是用了另一個 job 的。
- 結果是同樣的 job 可能由不該跑它的人執行,輸出的結果前後不一致。
- 受影響的是依賴這些 job 結果的人,他們無法信任結果。

**我說的「fix the profile」,依你的意思應該改成這句**
- 修好後,每個 job 都只使用自己的 worker selection,不會借用別的 job 的。

**驗收條件(擬寫入意圖檔)**
1. 每個 job 執行時,由它自己的 worker selection 決定誰來跑。
2. 兩個 job 的 worker selection 不同時,各自依自己的規則選人,互不影響。
3. 同一個 job 重複執行,選人的結果一致,不再因為別的 job 而變動。

**不在範圍內**:重新設計 worker selection 的規則本身。這次只處理「用錯對象」的問題。

**我需要你回答的一個問題(結果取向)**
- 已經因為這個問題產生的不一致結果,要不要重新跑或修正?
  - 預設是**不動**。這次只修正之後的行為,不會改寫你現有的任何結果。
  - 如果你要處理舊結果,請明確說明。這會動到你現有的資料,我需要你的同意。

**確認「yes」代表什麼**
- 這是工程性質的變更,我判斷不需要另外寫規格文件。
- 回答 yes 即授權我:寫計畫、實作、做審查。審查和發布檢查通過後,我會做一次一般(非強制)的 push,並開一個 Ready 狀態的 PR。
- **合併 PR 是另一個獨立的決定,我不會替你合併。**
- 你可以在發布前明確選擇不要自動發布。

**目前狀態**:意圖尚未確認,所以我沒有寫任何計畫,也沒有提交任何檔案。請告訴我:
1. 以上重述是否正確(特別是 worker selection 和 job 的說法)?
2. 舊結果要不要處理?

你確認後,我才會寫入意圖檔並繼續做計畫。

### Observed execution

```json
{
  "models": [
    "claude-sonnet-5-5"
  ],
  "cost_usd": 0.1215234,
  "num_turns": 10,
  "skill_calls": [
    {
      "skill": "loom-code:write-plan"
    }
  ],
  "tool_names": [
    "Skill",
    "Bash",
    "Grep",
    "Bash",
    "Bash",
    "Bash",
    "Read",
    "Read"
  ],
  "permission_denials": [
    {
      "tool_name": "Bash",
      "tool_use_id": "toolu_018jsS2PNzce1rBL3qqGQKoV",
      "tool_input": {
        "command": "cd /private/tmp/loom-context-claude-dogfood/bundle/loom-code/skills/write-plan/references; cat confirm-intent.md; cat ../../../contract/templates/intent.md",
        "description": "Read confirm-intent reference and intent template"
      }
    }
  ],
  "draft_intents": []
}
```
