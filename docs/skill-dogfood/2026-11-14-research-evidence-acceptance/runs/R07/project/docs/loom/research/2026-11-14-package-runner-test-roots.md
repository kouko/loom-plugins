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

## 問題與條件

確認提供的 project 原始碼中，package runner 的 TEST_ROOTS 精確包含哪些目錄；直接讀取常數定義即足以回答，不討論修改。

## 方法

只讀原始碼：這是常數內容的事實核對，無須執行 runner、suite 或實驗。

## 發現

TEST_ROOTS 按定義順序精確包含四個字串：

- `tests`
- `loom-code/tests`
- `loom-design/tests`
- `loom-workflow/tests`

## 證據

已讀取提供快照的 [src/scripts/run_package_tests.py](../../../src/scripts/run_package_tests.py)，第 53 行定義：

```python
TEST_ROOTS = ("tests", "loom-code/tests", "loom-design/tests", "loom-workflow/tests")
```

證據種類為原始碼觀察；使用 `nl -ba` 讀取，未執行該檔案。

## 決策影響與限制

這足以確認此快照的常數內容。未取得 commit 版本識別，亦未驗證各目錄存在或測試執行情況；這些不影響本次常數核對，原始碼變更後須重新核對。
