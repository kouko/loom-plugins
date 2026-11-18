# Loom Plugins

## Skill Development Conventions

### File Paths
- SKILL.md 內引用 bundled files 時使用相對路徑（相對於 skill 目錄）
- Good: `references/lenses.md`
- Bad: `loom-code/skills/closing-review/references/lenses.md`
- 原因：Claude Code 提供 Base Path，bundled files 從 skill 目錄相對解析

### 兩份文件：intent.md 與 spec.md（loom 1.0）
- `docs/loom/intent/<change-id>.md`（capture-intent／write-plan 擁有）— 使用者語言：Problem、Proposed outcome、Acceptance（每條可被 independent acceptance testing 證明）、Constraints、Out of scope、Open questions
- `docs/loom/<change-id>/spec.md`（write-spec 擁有）— 工程語言：`REQ-<n> — <name>` 每條對回 intent 的 Acceptance 編號、Design decision（標 agent-decided／user-decided）、Current state evidence、UI flows
- spec.md 只在 `needs-design: yes` 時存在；spec 一律 reference 它的 intent，不重述

### Skill Structure（CRITICAL — Anthropic 規範）

**MUST：skill 資料夾扁平 — subfolder 內不可再嵌 subfolder。**

```
✅ OK（subfolder 是單層）:
skills/init/SKILL.md
skills/init/assets/SCHEMA.md
skills/init/assets/extract_lineage.py
skills/init/scripts/build.py
skills/init/agents/worker.md
skills/init/references/spec.md
skills/init/protocols/code-review.md
skills/init/checklists/security.md

❌ NOT OK（subfolder 內又開 subfolder）:
skills/init/assets/scripts/foo.py     ← assets/ 下開 scripts/
skills/init/agents/sub/worker.md      ← agents/ 下開 sub/
skills/init/references/v1/spec.md     ← references/ 下開 v1/
```

- 每個 skill 是自包含目錄：SKILL.md + 任意數量的**單層** subfolder（assets/、protocols/、agents/、scripts/、references/、checklists/、rubrics/、standards/ 等）
- 任一 subfolder 內**不可再開 subfolder**（這是 Anthropic 官方 skill convention）
- SKILL.md body 硬上限 ~6,000 tokens（約 4,500 words）；軟目標 ~5,000 tokens（約 3,750 words，對齊官方建議）；超過軟目標需在 PR 註明一行理由。Anthropic 官方建議 <500 lines，本 repo 改用 token 計量因為行數密度差異大
- Domain knowledge 用目錄慣例 + 描述性檔名路由，不用靜態清單
- Reference files 從 SKILL.md 直接引用，路徑都是 `<subfolder>/<file>` 一層 deep
- **違規會讓 package suite 的 `tests/test_skill_folder_flatness.py` 失敗（例外與原因見該測試檔開頭）**；本 repo 寫入時不會回報，因為未註冊的 `.claude/hooks/validate-skill-folder-structure.sh` 會讓 loom-workflow 的 hook 跳過

### Module Criteria

**MUST：一個 skill 拆成 per-capability 檔案後，用四條判準衡量 —— change、add、remove、locate。**

- **change** — Editing one capability touches that capability's file and its own test, where it has one, and nothing else.
- **add** — Adding a capability is a new file plus one routing entry, and every existing capability file stays untouched.
- **remove** — Removing a capability deletes its file, its routing entry and its own test where it has one, and leaves nothing behind that still names it.
- **locate** — A rule that belongs to one capability lives in that capability's file, while the shared part carries only what every capability shares and a sibling file carries only its own.
- A capability's own test module is optional: `add` stays one file plus one routing entry, and `change` reads as its own test where it has one. Written without one, a capability gives up the guarantee that a failure names the capability that broke, and its removal is one deletion fewer.
- 四條各自要有一支可執行的 check 擋著，散文不算：只寫在這裡而沒有 check 重算的判準就是缺陷。
  `loom-code/tests/test_module_criteria_text.py` 記著每一條由哪支 check 執行
- 範例是 `loom-code/skills/closing-review/references/` 底下的 adversary recipe 拆分

### Test Location

**MUST：測試住在 `tests/` 資料夾，和它測的 code 分開。**

- 每個 plugin 的測試放在 `<plugin>/tests/`；loom-workflow 的 skill 測試放在 `loom-workflow/tests/<skill>/`
- Repository-level 測試（root `scripts/`、`.claude/hooks/` 的測試）放在 root `tests/`
- 不可把測試放在 production code 旁邊（`scripts/` 內）或 skill 資料夾內（含 `probes/`）
- `tests/local/` 放需要本機安裝 CLI 的測試，package suite 和 CI 都會跳過它
- Package suite（`scripts/run_package_tests.py --loom-family`）只跑四個 test root：root `tests/`、`loom-code/tests/`、`loom-design/tests/`、`loom-workflow/tests/`，含它們的子資料夾，pytest 檔（`test_*.py`、`*_test.py`）和 shell 測試（`test-*.sh`）都自動探索，新增測試不用改 suite command；CI 也跑同一份 inventory
- Package suite 需要本機有 `node`（OpenCode plugin 的 loader 測試會執行它）；使用者安裝 plugin 不需要 node
- 四個 root 定義在 `scripts/run_package_tests.py` 的 `TEST_ROOTS` 常數；新增 plugin 時要把它的 `<plugin>/tests/` 加進這個常數，否則它的測試不會跑，repo-wide guard 也會擋下
- 例外：`docs/loom/` 底下的 evidence probe 程式留在原處
- 移除一個 skill 時一併刪掉它的測試（Module Criteria 的 **remove**）：loom-workflow 刪 `tests/<skill>/` 資料夾；loom-code 刪 `loom-code/tests/` 裡以該 skill 命名的檔案

### Contract Citations

**MUST：執行期散文契約不得引用本 repo 的開發紀錄** — a runtime prose
contract under the loom skill and agent trees must not cite one of this
repository's development records under `docs/`.

- 原因：派出去的 agent 讀的是**它當下所在的 repo**，所以這種引用只在本
  repo 解得開。這是可攜性缺陷，不是風格偏好
- 豁免一 **loom-scaffolded store directories**：loom 為任何 adopting repo 定義
  的協定路徑（store 目錄、協定檔名、文法佔位符）——那是 schema，不是引用
- 豁免二 **`.py`/`.sh` provenance comments**：出處註解沒有 model 會讀到，
  除非它主動開檔
- 用 `loom-code/scripts/check_contract_citations.py` 檢查；違規的完整定義在
  該腳本裡，這裡不重複（重複＝第二個漂移面）
- **既有債務是分階段清的**：腳本裡的 `DEBT_LIST` 記著規則上線時就已違規的
  檔案，清單只能變短。在清單上的檔案仍算違規，只是尚未清理——新的違規
  在任何地方都會即刻被擋。看到一個 on-list 檔案裡還有引用，那是待辦，
  不是規則的例外

### Quality Gates

**loom 家族（loom-code／loom-design／loom-workflow）**：品質只有三種驗證動作，
其餘都是形式。

- 三種動作：**讀**（fresh-context reviewer 按 lens 審查）、**acceptance testing**（乾淨環境照 intent 的 Acceptance 逐條試）、**對抗**（mutation／fuzz，或 adversary 自寫可執行的 abuse／邊界案例）
- 對抗跑在 Build 結尾；讀與 acceptance testing 跑在 closing-review；寫的人不能自己驗
- Lens 定義見 `loom-code/skills/closing-review/references/lenses.md`；reviewer 人數來自 checker 的 review policy（`python3 loom-code/scripts/loom_checker.py reviewer-count <change-id>`）
- 決定性的閘只有一支 **checker**：`python3 loom-code/scripts/loom_checker.py --list-rules`
  是規則清單的 SSOT（規則全部是「重算」，不是宣稱）；這裡不重列規則 id，重列＝第二個漂移面
- 散文不當閘：只有 SKILL.md／reference 內以 `<!-- gate: <id> -->` 標記的段落算閘，
  沒標記的散文不得當閘用

### Versioning & Release

**MUST：每個合併至 main 且動到 plugin 的 PR，必須 bump 該 plugin 的版號**（預設 patch；有 station guidance、field、rule id 或 contract manifest 變更時為 minor）。

- 每個 plugin 一份 SSOT：`<plugin>/.claude-plugin/plugin.json` 是單一來源真相；`<plugin>/.codex-plugin/plugin.json`、`<plugin>/plugin.json`、`<plugin>/package.json` 皆經 `python3 scripts/sync_codex_manifests.py --all` 衍生而來；勿手動改導出檔以免版本衝突
- `<plugin>/CHANGELOG.md` 必須在同一 commit 加入新區段 `## [X.Y.Z] — <date> — <summary>`
- README 版號字串同步更新：`<plugin>/README.md`、`<plugin>/README.ja.md`、`<plugin>/README.zh-TW.md`，以及 root `README.md` 的 plugin 表格列與該 plugin 章節的版本行
- 版號在最後一輪 fix 就 bump，要在 closing-review 的 finalize-review 產生 attestation 之前；在它之後才 bump 會讓 attestation 失效（stale）
- 理由：`claude plugin update` 只比對版本字串；未 bump 的變更永遠不會發到已安裝副本
- 機制化：各 plugin 的 pin test 斷言版號一致——`loom-code/tests/test_write_plan_station_text.py::test_current_release_metadata_is_synchronized`、`loom-design/tests/spec/test_capture_intent_contract.py`、`loom-workflow/tests/scripts/test_release_metadata.py`；bump packet 必須列出 CHANGELOG entry、pin test rewrite 為交付項
- 參考記憶：`docs/loom/memory/version-bump-through-claude-ssot-and-sync-script.md`、`docs/loom/memory/version-bump-packets-must-name-changelog-entry.md`

### loom 1.0 flow
- 七站：capture-intent → write-spec →（write-plan → build → review → ship），maintain 回頭開 intent
- 三個人類決策點：①覆述並確認 intent（含 engineering 單向門；不寫 spec 的 product 單向門也在此問）②product 的可見行為與單向門確認（spec）③acceptance test report 驗收
- 入口與完整站序：`docs/loom/README.md`

### Agent Conventions
- **writer ≠ judge 由流程保證**：closing review 使用 fresh-context reviewer；
  產生的 attestation 綁定功能內容與 reviewer identity，不維護 dispatch ledger
- 傳遞 **檔案路徑** 給 agent（不是檔案內容）；路徑在 SKILL.md 中用相對路徑定義，launch 時解析為絕對路徑
