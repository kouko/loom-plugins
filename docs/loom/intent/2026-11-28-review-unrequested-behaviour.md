# 最後審查要抓出「做了沒人要求的事」
originator: kouko
kind: engineering
needs-design: no — internal reviewer guidance and its tests; no user-facing surface, single rule
evidence: [docs/loom/research/2026-11-28-mattpocock-skills.md]
status: confirmed 2026-11-28
intent_confirmed_sha: 86d3e7d5d6d04b5d2d3d5894a04e35f0bd2193ed
publication: automatic — authorized 2026-11-28 by kouko

## Problem

loom 的最後審查會檢查「該做的沒做」「說做了卻沒做」「兩份文件互相矛盾」，但沒有任何一步專門檢查「改動做了 intent 沒要求的事」，或做了 intent 的 Out of scope 明確排除的事。只有寫了 spec 的改動，spec 審查會抓這件事；不需要 spec 的改動（loom 多數的改動）沒人看。驗收測試員只試 Acceptance 條件，也不會去找多出來的行為。結果是：多做的行為可能一路通過審查、合併，使用者在驗收報告上也看不到它。目前沒有發現實際發生過，這是預防性補強；來源是研究紀錄第 4 項（mattpocock `code-review` 的 Spec 軸）。

## Proposed outcome

最後審查的 reviewer 不論用哪一份審查清單，都會把「交付了 intent 沒要求、或 intent 的 Out of scope 排除的行為」當成問題提出，沒有 spec 的改動也一樣。

## Acceptance

1. 最後審查的 reviewer 共用指引寫明：交付了 intent 沒要求的行為，或 intent 的 Out of scope 排除的行為，必須當作 finding 提出；沒有 spec 的改動同樣適用。
2. 把這條規則刪掉、或改成可以略過時，package suite 會有測試失敗。
3. loom-code 發布新版號，CHANGELOG 寫明這條規則。

## Constraints

- 只補這一項缺口；不採用 mattpocock 的兩軸分工，兩位 reviewer 仍用同一份審查清單。
- spec 審查既有的檢查（spec 沒要求的行為算缺陷）維持不變。

## Out of scope

- 讓兩位 reviewer 各看不同的審查面向（兩軸分工）。
- 驗收測試員的工作方式。
- 回頭審查已經合併的改動。

## Open questions
- none
