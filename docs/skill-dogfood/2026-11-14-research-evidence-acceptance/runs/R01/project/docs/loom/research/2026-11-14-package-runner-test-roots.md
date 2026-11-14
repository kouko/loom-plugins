---
title: "Package runner 的 TEST_ROOTS"
type: loom-research
status: concluded
created: 2026-11-14
updated: 2026-11-14
tags:
  - loom/research
---

# Package runner 的 TEST_ROOTS

## 問題與範圍

確認提供的 project/src/scripts/run_package_tests.py 中 TEST_ROOTS 的精確目錄；只讀來源，不執行 runner、suite 或實驗，不評估修改。

## 方法與理由

直接檢視常數定義即可回答此事實問題；以 `nl -ba src/scripts/run_package_tests.py` 讀取提供的來源，不需外部搜尋或比較框架。

## 發現

實際讀到第 53 行定義：

```python
TEST_ROOTS = ("tests", "loom-code/tests", "loom-design/tests", "loom-workflow/tests")
```

精確包含四個目錄，依原順序為 `tests`、`loom-code/tests`、`loom-design/tests`、`loom-workflow/tests`。

## 證據

來源檢視：[run_package_tests.py](../../../src/scripts/run_package_tests.py)，第 53 行。適用於本次提供的來源快照；未提供 commit 或版本資訊。

## 決策影響

此常數的內容已可確認，無需實驗。

## 限制與未驗證事項

未執行 runner 或測試，不宣稱測試執行成功，也未驗證這些目錄是否實際存在。來源未修改。
