# Name module entries in plans and review tests and splits against them — acceptance test evidence

Round 1: 2026-10-05, clean copy at b6dc33e9. Re-run after fix: 2026-10-05, clean copy at
5dd3f96d (`git worktree add --detach <scratchpad>/at-clean2 HEAD`; `git status --short` empty).
Fix range 211bad6a..5dd3f96d touched `loom-code/skills/write-plan/SKILL.md` (Task size),
`loom-code/skills/closing-review/references/lenses.md` (`tests` and `refactoring` rows only),
`loom-code/tests/test_write_plan_entry_definition.py` (docstring/message), and `loom-code/CHANGELOG.md`.

Rule text under test at 5dd3f96d (quoted):
- write-plan Task size (`SKILL.md:324-329`): "Tasks changing non-test code: Files marks the entry
  other modules call; case-ids name behaviour seen there; logic that entry cannot reach is its own
  module, tested at its entry."
- lenses.md `tests` row: "a module's entry is what other modules call, never whatever its tests call;
  a task changing non-test code whose plan Files line marks no entry is a finding; a new or changed
  test that calls an internal (non-entry) function is a finding when that behaviour is reachable from
  the module's entry, whether or not entry tests already cover it, and the fix moves the test to the
  entry, or deletes it when an entry test already covers that behaviour; a test through the entry is
  never asked to add internal tests, and logic the entry cannot reach that became its own module with
  its own entry, tested at that entry, is not a finding"
- lenses.md `refactoring` row: "… a split or extraction defaults to a non-exported function inside the
  module, and becomes its own module with an entry only when another module needs to call it or its
  behaviour is unreachable from the existing entry — wanting to test it alone is no reason for a new
  entry; a shared extraction across modules stays acceptable as its own module whose entry its callers import"

## Setup (clean copy, re-run at 5dd3f96d)

- README install path (`claude plugin marketplace add https://github.com/kouko/loom-plugins.git`
  then `claude plugin install loom-code@loom`) installs the published `main`, not this branch,
  and would modify the user's real install, so the branch copy was checked instead:
  - `claude plugin validate ./loom-code` -> `✔ Validation passed`
  - `claude plugin validate .` -> `✔ Validation passed with warnings` (pre-existing: marketplace
    has no description; `requires-contract` unknown field on plugins[2])
  - `python3 scripts/sync_codex_manifests.py --check --all` -> exit 0

## Method for lines 1, 2, 4 (re-run)

Case files in the scratchpad (not committed): `cases/review-cases.md` (12 cases),
`cases/plan-cases.md` (8 plan tasks), `cases/answer-key.md` written before dispatch and never
shown to an agent. Each agent read ONLY the named rule text in the clean copy:

| Agent | Model | Rule text it read | Input |
|---|---|---|---|
| Reviewer A | opus, fresh context | lenses.md Code rows naming, tests, refactoring, deletion-first, architecture | 12 review cases |
| Reviewer B | sonnet, fresh context | same rows | same 12 review cases |
| Plan checker | sonnet, fresh context | write-plan `SKILL.md:324-329` + lenses.md `tests` row | 8 plan cases |
| Planner | sonnet, fresh context | write-plan `SKILL.md:324-329` only | brief: toy shop, 4 Acceptance lines (code, test-only, docs, release metadata) |

Toy repo: `shop/pricing` exports only `compute_total`; private `_apply_discount`, `_add_tax`
in `shop/pricing/core.py` called only by it; `shop/checkout.place_order` calls `compute_total`;
`shop/reports`, `shop/invoices`, `shop/receipts` siblings; existing entry tests
`test_compute_total_percent_coupon_rounds_to_cents`, `test_compute_total_tax_rounds_half_up`.

Review cases: 01 internal test, no entry coverage | 02 internal test, entry test covers it |
03 entry-only test | 04 new `shop/fx` unreachable from pricing, own entry | 07 58-line cohesive fn |
08 46-line fn doing five unrelated jobs (control) | 09 coincidentally similar `_fmt_id` x3 |
10 shared money-format extracted to new `shop/money` entry | 11 `_apply_discount` exported "to unit-test alone" |
13 same-reason triplicate + fourth copy (control) | 14 NEW: `_add_tax` test beside entry test covering it |
15 NEW: shared money-format extracted as private `_format_money` in reports, imported by siblings.
(Cases 05, 06, 12 belong to line 3 and were not re-run.)

Plan cases: 01 code task, no entry | 02 entry = private `_apply_discount` | 03 entry ok, one internal
case | 04 correct | 05 docs-only | 06 NEW test-only task (`tests/test_checkout.py`), no entry |
07 NEW release metadata (`plugin.json`, `CHANGELOG.md`, `README.md`), no entry |
08 NEW production `shop/receipts/render.py`, no entry.

## 1. write-plan 產生的 plan 裡，每個會改程式碼的 task 都寫明它碰到的模組對外入口，而且它的測試案例以入口的行為命名。
- How I tried it (re-run): Planner wrote a Task DAG; Plan checker judged plan-01, 02, 04, 05, 06, 07, 08; ran
  `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest -q loom-code/tests/test_write_plan_entry_definition.py "loom-code/tests/test_write_plan_station_text.py::test_current_release_metadata_is_synchronized"`
- What came back:
  - Planner: Task 1 `Files: shop/pricing/__init__.py (entry, compute_total; marked), shop/pricing/core.py (… reached only through the entry), tests/test_pricing_coupon.py`, cases `percent-coupon-reduces-total`, `discount-rounds-to-cents`, `over-hundred-percent-coupon-clamps-to-zero`, …; Task 2 (test-only) `Files: tests/test_checkout_empty_cart.py`, no entry — "changes only test files … the rule for tasks changing non-test code does not apply"; Task 3 docs, no entry; Task 4 `plugin.json`, `CHANGELOG.md`, no entry — "only edits release metadata and changes no non-test code".
  - Plan checker: plan-01 VIOLATION ("a task changing non-test code whose plan Files line marks no entry is a finding"); plan-02 VIOLATION ("a module's entry is what other modules call, never whatever its tests call"); plan-04 COMPLIANT; plan-05 COMPLIANT; plan-06 COMPLIANT ("Tasks changing non-test code" — test-only); plan-07 COMPLIANT ("config, not code with an entry"); plan-08 VIOLATION.
  - Plan checker ambiguity note (verbatim): "the rule text does not say whether docs, JSON or Markdown count as 'non-test code'. I read them as prose or config. A strict reading would make plan-07 a violation."
  - pytest: `4 passed in 0.02s`.
- Evidence: replies transcribed above; 7/7 plan cases match the answer key.

## 2. 測試只需要涵蓋模組對外入口的介面：plan 裡每個測試案例都從入口測（必須測內部函式的案例不符合本條），不為內部函式另寫測試；closing review 把「直接測內部、而該行為從入口能觸及」的新增或修改測試當成問題回報，要求改從入口測。用刻意寫壞的範例改動試，這種測試會被抓到（不論入口是否已有測試涵蓋同樣行為），只從入口測的測試不會被要求補內部測試，而入口觸及不到、成為有自己入口的獨立模組並從該入口測的測試不會被抓。
- How I tried it (re-run): plan-03 to Plan checker; review cases 01-04 and 14 to Reviewers A and B.
- What came back:
  - plan-03 VIOLATION: "Drop `apply-discount-helper-quantizes-internally`. If an entry test already covers it, delete the case. If not, move it to `compute_total`."
  - case-01: A FINDING, B FINDING (tests) — fix: move the test to `compute_total`; no new entry.
  - case-02: A FINDING, B FINDING — "deletes it when an entry test already covers that behaviour"; fix: delete `tests/test_discount.py` (both).
  - case-03: A NO FINDING, B NO FINDING — "a test through the entry is never asked to add internal tests".
  - case-04: A NO FINDING, B NO FINDING — "logic the entry cannot reach that became its own module with its own entry, tested at that entry, is not a finding".
  - case-14: A FINDING, B FINDING — fix: delete `test_add_tax_rounds_half_up` (A also cites "duplicated cases"); neither asked for a further entry test.
- Evidence: 5/5 review cases match in both samples; 1/1 plan case matches.

## 3. closing review 的審查會把「只把呼叫轉給另一處、沒藏住任何邏輯」的新增模組或函式當成問題回報——只轉手指的是不做分支、轉換、驗證、錯誤處理、資源邊界處理或政策選擇，只呼叫另一處並回傳結果；用刻意寫壞的範例改動試，會被抓到，而真正藏住邏輯的模組不會被抓。
- Carried over from round 1 (b6dc33e9): the fix diff does not touch the `deletion-first` row or anything it cites; `git diff 211bad6a..5dd3f96d -- loom-code/skills/closing-review/references/lenses.md` changes only the `tests` and `refactoring` rows.
- Round 1 result: case-05 (forwarder) A FINDING, B FINDING (deletion-first: "A new module or function that only forwards … is a finding"; fix delete wrapper); case-06 (validates and raises) A/B NO FINDING; case-12 (re-export declaring entry) A/B NO FINDING. 3/3 match in both samples.

## 4. closing review 不單憑長度或重複次數要求拆分或抽出：長度只提示審查者去看，要求拆分時必須指出具體毛病（例如一個函式做了幾件不相干的事）；重複三次只在三處會因同一個理由一起改時才要求抽出。要求拆分或抽出時，修法預設是模組內部、不對外的函式；只有其他模組也需要呼叫它，或它的行為無法從既有模組的入口觸及時，才成為有自己入口的獨立模組；「想單獨測」本身不構成新增入口的理由。用刻意寫壞的範例改動試，只是長而沒有其他毛病的函式不會被要求拆分，三處碰巧相似但會各自改的程式不會被要求抽出，審查不會要求為拆分或抽出新增對外入口，而跨模組共用的抽出仍被接受。
- How I tried it (re-run): review cases 07-11, 13, 15 to Reviewers A and B.
- What came back:
  - case-07: A/B NO FINDING — "length alone is never the finding".
  - case-08 (control): A FINDING (naming, refactoring), B FINDING (naming) — "a function doing several unrelated things"; fix: private helpers inside `shop/checkout`; new entry: no (both).
  - case-09: A/B NO FINDING — "extracted only when the three change for the same reason".
  - case-10: A/B NO FINDING — "a shared extraction across modules stays acceptable as its own module whose entry its callers import".
  - case-11: A FINDING (refactoring, deletion-first), B FINDING (refactoring) — "wanting to test it alone is no reason for a new entry"; fix: return to private in pricing.
  - case-13 (control): A/B FINDING (refactoring) — extract one shared module whose entry all four import (the only entry-adding fix, tied to the shared-extraction clause).
  - case-15: A/B FINDING (refactoring, architecture) — fix: move to own module (e.g. `shop/money`, `format_money`) whose entry siblings import. Both noted no clause forbids cross-module private imports in plain words; finding inferred from "its own module whose entry its callers import".
  - Across all cases no reviewer asked for a new exported entry for a split or a single-module extraction.
- Evidence: 7/7 match in both samples.

## 5. 完整 package suite 全部通過；三份 manifest、README 的版號字串與 CHANGELOG 新區段一致。
- How I tried it (re-run at 5dd3f96d): `grep '"version"'` over manifests; `grep 3.34.0` over READMEs; CHANGELOG line 3; sync check; release-sync test in the pytest command under line 1.
- What came back: `loom-code/plugin.json:3`, `loom-code/.claude-plugin/plugin.json:3`, `loom-code/.codex-plugin/plugin.json:3`, `loom-code/package.json:3` all `"version": "3.34.0"`; `README.md:17`, `README.md:132`, `loom-code/README.md:11`, `loom-code/README.ja.md:11`, `loom-code/README.zh-TW.md:9` all 3.34.0; `loom-code/CHANGELOG.md:3` `## [3.34.0] — 2026-10-05 — …`; sync check exit 0; `test_current_release_metadata_is_synchronized` passed.
- Full package suite: NOT run here (left to finalize-review, which runs
  `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`
  and refuses the attestation on failure).

## Results — re-run reviewer tables (verdict columns)

| case | key | Reviewer A (opus) | Reviewer B (sonnet) |
|---|---|---|---|
| 01 | finding, move | FINDING, move | FINDING, move |
| 02 | finding, delete | FINDING, delete | FINDING, delete |
| 03 | none | NO FINDING | NO FINDING |
| 04 | none | NO FINDING | NO FINDING |
| 07 | none | NO FINDING | NO FINDING |
| 08 | finding, concrete problem, no new entry | FINDING, no new entry | FINDING, no new entry |
| 09 | none | NO FINDING | NO FINDING |
| 10 | accepted | NO FINDING | NO FINDING |
| 11 | finding, keep internal | FINDING | FINDING |
| 13 | extraction asked | FINDING, shared module entry | FINDING, shared module entry |
| 14 | finding, delete | FINDING, delete | FINDING, delete |
| 15 | finding, own module | FINDING, own module | FINDING, own module |

| plan case | key | Plan checker |
|---|---|---|
| plan-01 | violation | VIOLATION |
| plan-02 | violation | VIOLATION |
| plan-03 | violation | VIOLATION |
| plan-04 | compliant | COMPLIANT |
| plan-05 | compliant | COMPLIANT |
| plan-06 | compliant | COMPLIANT |
| plan-07 | compliant | COMPLIANT (ambiguity noted) |
| plan-08 | violation | VIOLATION |

Limitation: agents applied the rows in isolation on toy cases; this is not a full
closing-review round on a real diff.
