# Name module entries in plans and review tests and splits against them — acceptance test evidence

Tried on 2026-10-05, in a clean copy of the project at b6dc33e9
(`git worktree add --detach <scratchpad>/at-clean HEAD`; `git status --short` empty).

## Setup (clean copy)

- README install path (`claude plugin marketplace add https://github.com/kouko/loom-plugins.git`
  then `claude plugin install loom-code@loom`) installs the published `main`, not
  this branch, and would modify the user's real install, so the branch copy was
  checked instead:
  - `claude plugin validate ./loom-code` -> `✔ Validation passed`
  - `claude plugin validate .` -> `✔ Validation passed with warnings` (pre-existing:
    marketplace has no description; `requires-contract` unknown field on plugins[2])
  - `python3 scripts/sync_codex_manifests.py --check --all` -> exit 0

## Method for lines 1-4

Seeded example changes were written in the scratchpad (not committed); an answer
key was written before any agent result arrived and never shown to an agent.
Each agent was told to read ONLY the named rule text in the clean copy:

| Agent | Model | Rule text it read | Input |
|---|---|---|---|
| Reviewer A | opus, fresh context | `loom-code/skills/closing-review/references/lenses.md` Code rows naming, tests, refactoring, deletion-first, architecture | 13 review cases |
| Reviewer B | sonnet, fresh context | same rows | same 13 review cases |
| Plan checker | sonnet, fresh context | `loom-code/skills/write-plan/SKILL.md` Task size paragraph (lines 324-329) + lenses.md `tests` row | 5 plan-task cases |
| Planner | sonnet, fresh context | `loom-code/skills/write-plan/SKILL.md` Task size paragraph only | brief: toy shop + 3 Acceptance lines (2 code, 1 docs) |

Toy repo in every case: `shop/pricing` exports only `compute_total` (in `__init__.py`);
private `_apply_discount`, `_add_tax` are called only by `compute_total`;
`shop/checkout.place_order` calls `pricing.compute_total`; `shop/reports`,
`shop/invoices`, `shop/receipts` are sibling modules.

Review cases (one-line summary each):

| case | seeded change | expected |
|---|---|---|
| 01 | new test imports internal `_apply_discount`; no entry test | finding, move to entry |
| 02 | same internal test; entry test already covers the behaviour | finding |
| 03 | only new test goes through `compute_total` | no finding, no internal test asked |
| 04 | new `shop/fx` module (`convert`), unreachable from pricing, called by reports + invoices, tested at `convert` | no finding |
| 05 | `get_order_total(cart): return compute_total(cart)` | finding (forwarder) |
| 06 | same wrapper but validates empty cart / qty and raises | no finding |
| 07 | 58-line cohesive invoice-body renderer | no split asked |
| 08 | 46-line `finalize` doing pricing, DB write, SMTP, loyalty, audit log (control) | split only with concrete problem; no new entry |
| 09 | three `_fmt_id` helpers alike but owned by three different change reasons | no extraction asked |
| 10 | identical money-format block in 3 modules extracted to new `shop/money` | accepted |
| 11 | `_apply_discount` moved to new exported `shop/discounts` "so it can be unit-tested on its own"; only caller is `compute_total` | finding, keep internal |
| 12 | `pricing/__init__.py` re-exports new `add_tax` because reports calls it | no finding |
| 13 | three same-reason copies left in place, a fourth added (control) | extraction asked |

Plan cases: plan-01 code task, Files names no entry; plan-02 entry marked as the
private `_apply_discount`, cases named after it; plan-03 entry correct but one case
`apply-discount-helper-quantizes-internally`; plan-04 entry `pricing.compute_total`,
cases all at entry; plan-05 docs-only task, no entry.

## 1. write-plan 產生的 plan 裡，每個會改程式碼的 task 都寫明它碰到的模組對外入口，而且它的測試案例以入口的行為命名。
- How I tried it: Planner agent wrote a Task DAG from the brief using only the Task size paragraph; Plan checker judged plan-01, plan-02, plan-04, plan-05; ran the graduated entry-definition program:
  `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest -q loom-code/tests/test_write_plan_entry_definition.py "loom-code/tests/test_write_plan_station_text.py::test_current_release_metadata_is_synchronized"`
- What came back:
  - Planner output, code tasks: `Files: shop/pricing/__init__.py (entry: compute_total), ...` with cases `compute_total_33_percent_coupon_on_10_00_returns_6_70`, `compute_total_percent_coupon_half_cent_boundary_rounds_to_cents`, `compute_total_without_coupon_unchanged`; `Files: shop/checkout/__init__.py (entry: place_order)` with cases `place_order_empty_cart_raises_clear_error`, `place_order_empty_cart_creates_no_order`, `place_order_single_item_cart_succeeds`; Risk line: "_apply_discount and _add_tax are tested at that entry, not directly". Docs task: no entry (correct).
  - Plan checker: plan-01 VIOLATION ("Any task touching code: Files marks the entry other modules call"; tests row "a code task whose plan Files line marks no entry is a finding"); plan-02 VIOLATION ("a module's entry is what other modules call, never whatever its tests call"); plan-04 COMPLIANT; plan-05 COMPLIANT (clause covers only tasks touching code).
  - pytest: `4 passed in 0.02s`.
- Evidence: planner and checker replies transcribed above; `loom-code/tests/test_write_plan_entry_definition.py` (3 tests) green.

## 2. 測試只需要涵蓋模組對外入口的介面：plan 裡每個測試案例都從入口測（必須測內部函式的案例不符合本條），不為內部函式另寫測試；closing review 把「直接測內部、而該行為從入口能觸及」的新增或修改測試當成問題回報，要求改從入口測。用刻意寫壞的範例改動試，這種測試會被抓到（不論入口是否已有測試涵蓋同樣行為），只從入口測的測試不會被要求補內部測試，而入口觸及不到、成為有自己入口的獨立模組並從該入口測的測試不會被抓。
- How I tried it: plan-03 to Plan checker; review cases 01-04 to Reviewers A and B.
- What came back:
  - plan-03 VIOLATION: drop `apply-discount-helper-quantizes-internally`, entry case already covers rounding.
  - case-01: A FINDING, B FINDING — tests row "a new or changed test that calls an internal (non-entry) function is a finding when that behaviour is reachable from the module's entry"; fix: move to `compute_total`.
  - case-02: A FINDING, B FINDING — "whether or not entry tests already cover it"; fix: drop internal test, extend existing entry test.
  - case-03: A NO FINDING, B NO FINDING — "a test through the entry is never asked to add internal tests".
  - case-04: A NO FINDING, B NO FINDING — own module, two callers, unreachable from pricing, tested at its entry.
- Evidence: reviewer tables (transcribed in the Results section below). 4/4 cases and 1/1 plan case match the answer key in both samples.

## 3. closing review 的審查會把「只把呼叫轉給另一處、沒藏住任何邏輯」的新增模組或函式當成問題回報——只轉手指的是不做分支、轉換、驗證、錯誤處理、資源邊界處理或政策選擇，只呼叫另一處並回傳結果；用刻意寫壞的範例改動試，會被抓到，而真正藏住邏輯的模組不會被抓。
- How I tried it: review cases 05, 06, 12 to Reviewers A and B.
- What came back:
  - case-05: A FINDING, B FINDING — deletion-first "A new module or function that only forwards … just a call elsewhere returning its result — is a finding"; fix: delete the wrapper, call directly.
  - case-06: A NO FINDING, B NO FINDING — "one hiding any of those [validation, error handling] is not".
  - case-12: A NO FINDING, B NO FINDING — "a re-export that declares the module's entry" / another module needs to call it.
- Evidence: reviewer tables below; 3/3 match in both samples.

## 4. closing review 不單憑長度或重複次數要求拆分或抽出：長度只提示審查者去看，要求拆分時必須指出具體毛病（例如一個函式做了幾件不相干的事）；重複三次只在三處會因同一個理由一起改時才要求抽出。要求拆分或抽出時，修法預設是模組內部、不對外的函式；只有其他模組也需要呼叫它，或它的行為無法從既有模組的入口觸及時，才成為有自己入口的獨立模組；「想單獨測」本身不構成新增入口的理由。用刻意寫壞的範例改動試，只是長而沒有其他毛病的函式不會被要求拆分，三處碰巧相似但會各自改的程式不會被要求抽出，審查不會要求為拆分或抽出新增對外入口，而跨模組共用的抽出仍被接受。
- How I tried it: review cases 07-11 and 13 to Reviewers A and B.
- What came back:
  - case-07 (long, cohesive): A NO FINDING, B NO FINDING — "a prompt to look, never itself a finding".
  - case-08 (control, five unrelated jobs): A FINDING, B FINDING — "a function doing several unrelated things"; fix: non-exported functions inside the module; new entry: no (both).
  - case-09 (coincidental similarity): A NO FINDING, B NO FINDING — "extracted only when the three change for the same reason".
  - case-10 (cross-module shared extraction): A NO FINDING, B NO FINDING — "a shared extraction across modules stays acceptable".
  - case-11 ("so it can be tested alone"): A FINDING, B FINDING — "wanting to test it alone is no reason for a new entry"; fix: keep it non-exported, test through the entry.
  - case-13 (control, same-reason duplication + fourth copy): A FINDING, B FINDING — extraction requested; the only fix adding an entry, and both reviewers tied it to "a shared extraction across modules stays acceptable" (it is called by four modules).
  - Across all 13 cases no reviewer asked for a new exported entry for a split or a single-module extraction.
- Evidence: reviewer tables below; 6/6 match in both samples. Reviewer A noted the rule text does not say where a cross-module extraction should live (case-13) — either placement adds an entry, which the rule accepts.

## 5. 完整 package suite 全部通過；三份 manifest、README 的版號字串與 CHANGELOG 新區段一致。
- How I tried it: `grep '"version"'` over the manifests; `grep 3.34.0` over READMEs; CHANGELOG head; `sync_codex_manifests.py --check --all`; the release-sync test in the pytest command under line 1.
- What came back: `loom-code/plugin.json`, `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, `package.json` all `"version": "3.34.0"`; `README.md:17`, `README.md:132`, `loom-code/README.md:11`, `README.ja.md:11`, `README.zh-TW.md:9` all 3.34.0; `CHANGELOG.md:3` `## [3.34.0] — 2026-10-05 — …`; sync check exit 0; `test_current_release_metadata_is_synchronized` passed.
- Full package suite: NOT run here (left to finalize-review, which runs
  `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`
  and refuses the attestation on failure).
- Evidence: commands and outputs above.

## Results — reviewer tables (verbatim verdict columns)

| case | key | Reviewer A (opus) | Reviewer B (sonnet) |
|---|---|---|---|
| 01 | finding | FINDING (tests) | FINDING (tests) |
| 02 | finding | FINDING (tests) | FINDING (tests) |
| 03 | none | NO FINDING | NO FINDING |
| 04 | none | NO FINDING | NO FINDING |
| 05 | finding | FINDING (deletion-first) | FINDING (deletion-first) |
| 06 | none | NO FINDING | NO FINDING |
| 07 | none | NO FINDING | NO FINDING |
| 08 | finding w/ concrete problem, no new entry | FINDING (naming, architecture), no new entry | FINDING (naming), no new entry |
| 09 | none | NO FINDING | NO FINDING |
| 10 | accepted | NO FINDING | NO FINDING |
| 11 | finding, keep internal | FINDING (refactoring, deletion-first, tests) | FINDING (refactoring, tests) |
| 12 | none | NO FINDING | NO FINDING |
| 13 | extraction asked | FINDING (refactoring), shared entry | FINDING (refactoring), shared entry |

| plan case | key | Plan checker |
|---|---|---|
| plan-01 | violation | VIOLATION |
| plan-02 | violation | VIOLATION |
| plan-03 | violation | VIOLATION |
| plan-04 | compliant | COMPLIANT |
| plan-05 | compliant | COMPLIANT |

Limitation: agents applied the rows in isolation on toy cases; this is not a full
closing-review round on a real diff.
