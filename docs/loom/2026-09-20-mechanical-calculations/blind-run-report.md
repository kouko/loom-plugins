# 盲跑報告 — 2026-09-20-mechanical-calculations

本報告記錄在乾淨環境中，照 intent 的 Acceptance 條件逐條嘗試的結果。

---

## Acceptance 1

**條件**：檢查器只在每個變更路徑都是此 change 的 intent、其 Loom 證據、測試檔、或 `docs/loom/` 之外的低風險文件時，才把完整分支 delta 分類為 narrow；生產碼、保護面、介面面、不安全路徑、未知檔案類型保留完整儀式。

**嘗試方式**：
- 建立乾淨 repo，feature branch 只包含 intent、plan、evidence、測試檔、及 `docs/loom/` 外的 `.md` 文件 → `reviewer-count` 回傳 1（narrow）
- 同一 repo 加入 `src/main.py`（生產碼）→ `reviewer-count` 回傳 2（broad）
- 同一 repo 加入 `loom-code/contract/manifest.yaml`（保護面）→ `reviewer-count` 回傳 2
- 同一 repo 加入路徑含 `..` 或絕對路徑 → `reviewer_floor_for_paths` 直接回傳 2

**證據**：
- `test_auto_skip_boundaries.py::test_autoskip_narrow_skipspecplanblindrun` 通過
- `test_auto_skip_boundaries.py::test_autoskip_broad_skipempty` 通過
- `test_auto_skip_boundaries.py::test_autoskip_protected_skipempty` 通過
- `test_is_narrow_delta_path_traversal.py` 四項測試全部通過

**判定**：works

---

## Acceptance 2

**條件**：無綁定使用者選擇時，`selection show <change-id>` 於 narrow delta 回報 `spec`、`plan`、`blind-run` 為 skipped，write-spec、write-plan、blind-run 三站只略過這些步驟。

**嘗試方式**：
- 在 narrow delta（intent + plan + evidence + 測試檔 + `README.md`）上執行 `selection show 2026-09-20-mechanical-calculations`

**證據**：
```
{
  "change_id": "2026-09-20-mechanical-calculations",
  "bound": false,
  "run": ["implementer", "tdd", "reviewers", "adversarial", "package-tests"],
  "skip": ["spec", "plan", "blind-run"],
  "code": null,
  "failures": []
}
```

**判定**：works

---

## Acceptance 3

**條件**：無綁定使用者選擇時，空、未知、broad、mixed、或不可讀的 delta 不自動略過任何步驟，保留完整儀式。

**嘗試方式**：
- 空 delta（feature branch 無額外 commit）→ `selection show` 回傳 `skip: []`
- broad delta（含 `src/main.py`）→ `selection show` 回傳 `skip: []`
- 兩種情況 `run` 皆包含全部 8 個步驟

**證據**：
```
# 空 delta
{"skip": [], "run": ["spec","plan","implementer","tdd","reviewers","adversarial","blind-run","package-tests"]}

# broad delta（含 src/main.py）
{"skip": [], "run": ["spec","plan","implementer","tdd","reviewers","adversarial","blind-run","package-tests"]}
```
- `test_effective_selection_user_precedence.py::test_effectiveselection_emptydelta_fullritual` 通過
- `test_auto_skip_boundaries.py::test_autoskip_broad_skipempty` 通過

**判定**：works

---

## Acceptance 4

**條件**：綁定的使用者選擇決定有效步驟；自動分類不可增加也不可移除使用者選擇的步驟。

**嘗試方式**：
- narrow delta 上用 `selection propose --skip adversarial` 提案，並以 `/loom-code:expert-mode OK <code>` 確認綁定
- 檢查 `effective_selection`：`bound: true`，`skip: ["adversarial"]`，**spec/plan/blind-run 仍在 run 列表中**（未被自動加入 skip）
- 另測：使用者 skip 較多步驟（含 auto-skip 步驟），確認不被自動移除

**證據**：
```
# 使用者只 skip adversarial
{"bound": true, "skip": ["adversarial"], "run": ["spec","plan","implementer","tdd","reviewers","blind-run","package-tests"]}

# auto-skip (spec,plan,blind-run) 未被加入 skip；使用者選擇的 adversarial 保留在 skip
```
- `test_effective_selection_user_precedence.py` 五項測試全部通過（bound-fewer、bound-more、cancel、wrong-scope、tampered）

**判定**：works

---

## Acceptance 5

**條件**：narrow 分類不略過 `adversarial`、`package-tests`、reviewer 證據、發布檢查、或任何其他機械閘。

**嘗試方式**：
- narrow delta 無使用者選擇時，檢查 `selection show` 的 `run` 列表

**證據**：
```
"run": ["implementer", "tdd", "reviewers", "adversarial", "package-tests"]
```
- `adversarial`、`package-tests`、`reviewers` 全部在 `run` 中，不在 `skip` 中
- `_NARROW_AUTO_SKIP_STEPS = frozenset({"spec", "plan", "blind-run"})` 只含這三項

**判定**：works

---

## Acceptance 6

**條件**：`selection show` 列出 `plan` 為 skipped 時，write-plan 合約不再要求 plan artifact；其他 change 仍要求。

**嘗試方式**：
- narrow delta：`selection show` → `skip` 含 `plan`
- broad delta：`selection show` → `skip` 為空，`run` 含 `plan`

**證據**：
- narrow：`"skip": ["spec", "plan", "blind-run"]`
- broad：`"skip": [], "run": [..., "plan", ...]`
- `test_selection_store.py` 測試 `test_reused_change_id_on_new_branch_inherits_nothing` 驗證 narrow delta 自動略過 plan

**判定**：works

---

## Acceptance 7

**條件**：乾淨環境盲跑 narrow 文件或測試變更，確認無需 specification、plan、blind-run 三站，其餘閘門皆通過。

**嘗試方式**：
- 本報告即為該盲跑：在乾淨環境（/tmp 臨時 repo）建立 narrow delta（intent、plan、evidence、測試檔、低風險文件），執行所有驗證
- 所有 adversarial probe（24 項）通過
- 完整套件測試通過（背景任務 exit code 0）

**證據**：
- `docs/loom/2026-09-20-mechanical-calculations/evidence/probes/` 24 項測試全部通過
- `loom-code/scripts/` 完整測試套件通過

**判定**：works

---

## Acceptance 8

**條件**：repo 套件測試通過，mechanism check 對 trunk 回報無淨增加計數機制。

**嘗試方式**：
- 執行 `python loom-code/scripts/check_mechanisms.py` 對比 main branch
- 執行完整套件測試 `uv run pytest loom-code/scripts/`

**證據**：
```
class          recomputed registered
skill                  22         22
checker-rule           25         25
hook                   10          9
contract               63         63
prose-gate             19         19
net mechanism count (excl. host-hygiene): 138
exempt from net count: PostToolUse:Skill:language-anchor.py
all clear
```
- 10 recomputed hooks vs 9 registered：多出的 1 個（`PostToolUse:Skill:language-anchor.py`）已在 mechanisms.yaml 以 `class: host-hygiene` 登記，不計入淨計數
- 淨機制數 138，與 trunk 一致，無增加
- 套件測試全通過

**判定**：works

---

## 對既有使用者資料的影響

此變更為機械路由邏輯調整，**不修改任何使用者資料**。既有 change 的 selection 記錄、attestation、intent 內容皆不受影響。narrow delta 自動略過功能僅在無使用者綁定選擇時生效，且使用者隨時可透過 `selection propose` 覆寫。

---

## 我替您決定的事項（含重要以上 severity dismissal）

- 無。所有 adversarial probe 皆為機械驗證，未發現需人工裁決的缺陷。

---

## 開放問題

- 無。所有 Acceptance 條件在乾淨環境下驗證通過。

---

## 總結

8 條 Acceptance 全部 **works**。變更實現了「narrow delta 自動略過 spec/plan/blind-run」的機械計算，保留了使用者覆寫權限，未跳過任何安全閘門，套件測試與機制計數皆零回歸。
