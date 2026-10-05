# Name lying tests in review and state merge risk in PR bodies — acceptance test evidence

Tried on 2026-10-05, in a clean copy of the project at 30642536; re-tested after the fix at e237802e (see "Re-run at e237802e" at the end).

Scratch root below: `$S` = the session scratchpad
(`/private/tmp/claude-501/-Users-kouko--herdr-worktrees-loom-plugins-fix-pr-bottleneck/6cf584c4-39cf-4288-bff2-5a30741c2ae7/scratchpad`).

## 0. Setup (clean copy)
- How I tried it: `git worktree add --detach $S/clean HEAD` (HEAD 30642536, nobody had worked in it). README `## Install` uses `claude plugin marketplace add https://github.com/kouko/loom-plugins.git`, which installs the published main branch, not this branch, and would change the user's real install; so I validated the local copy instead: `claude plugin validate loom-code`, `claude plugin validate .`, `python3 scripts/sync_codex_manifests.py --check --all`, and parsed the three loom-code manifests with `json.load`.
- What came back: `loom-code` → `✔ Validation passed`; marketplace `.` → `✔ Validation passed with warnings` (warning: `plugins[2] plugin.json → requires-contract: Unknown field 'requires-contract'. Claude Code ignores it at load time.` — the field is not touched by this change); sync check exit 0; manifests parse.
- Evidence: commands above; not an actual `claude plugin install` from the branch.

## 1. closing review 的審查會把三種會騙人的測試（把實作原樣再寫一遍、讀原始碼文字判斷程式結構、mock 掉自己聲稱要測的那一段）各自當成問題回報；用一個刻意寫壞的範例改動試，三種都會被抓到。
- How I tried it: wrote a seeded change as a one-commit git repo at `$S/seeded` (not committed here): `shop/pricing.py` (`member_price`, `price_in`, `checkout_total`), `shop/rates.py` (`fetch_rate`, remote seam), `tests/test_pricing.py` with four tests:
  - `test_member_discount_applied` — expected value is `round(price * (1 - pricing.MEMBER_DISCOUNT), 2)` (restates the implementation)
  - `test_price_in_uses_rate_service` — `inspect.getsource` / `read_text` substring asserts on code (source text for code structure)
  - `test_fetch_rate_parses_service_response` — `mock.patch("shop.rates.fetch_rate")` then calls the mock (mocks the seam it claims to cover)
  - `test_checkout_total_member_cart` — honest behaviour test through `checkout_total` with literal expectations
  `uv run --isolated --with pytest python -m pytest -q tests` → `4 passed` (the three bad tests are green).
  Then dispatched a fresh `loom-code:reviewer` given only the clean copy's `loom-code/skills/closing-review/references/lenses.md` (`tests` row) and the seeded repo, without telling it which tests were seeded bad.
- What came back: `tests: NEEDS_REVISION`.
  - `test_member_discount_applied`: finding (important, tests/test_pricing.py:11) — "restating a constant or the implementation".
  - `test_price_in_uses_rate_service`: finding (important, tests/test_pricing.py:16-19) — "reading source text to assert code structure"; reviewer noted the prose-pin exception covers prose, not code source.
  - `test_fetch_rate_parses_service_response`: finding (important, tests/test_pricing.py:24) — "a mock or stub replacing the very seam it claims to cover".
  - `test_checkout_total_member_cart`: no finding.
- Evidence: reviewer verdict text above; seeded files under `$S/seeded` (scratch, not committed).

## 2. loom 自己用來釘住散文規則的測試，不會因為第 1 條被當成問題。
- How I tried it: dispatched a second fresh `loom-code:reviewer` with only `lenses.md` (`tests` row), `loom-code/tests/test_ship_risk_section_agent_decided_door.py` (an affirmative prose-pin test that reads SKILL.md text) treated as a changed test file, and `loom-code/skills/ship/SKILL.md`. Boundary (code-structure source-text test still flagged) is the A1 run: `test_price_in_uses_rate_service` was flagged by the same row.
- What came back: `tests: PASS`. All three test functions "no finding": the two self-tests are the ones engineering-baseline §5 item 8 requires; `test_ship_risk_placeholder_cites_agent_decided_doors` reads prose, not code layout, and meets item 8 (affirmative verb before the literal, negation rejects, self-tests present). No other findings.
- Evidence: reviewer verdict text above; A1 reviewer line for `test_price_in_uses_rate_service`.

## 3. ship 產生的 PR 說明，「風險與回滾」段落寫明：能否撤回（one-way／two-way door）、出事的影響範圍、回滾方式。
- How I tried it: dispatched a fresh `general-purpose` (sonnet) drafter with only `loom-code/skills/ship/SKILL.md` and (A) this change's plan + intent, (B) a hypothetical plan at `$S/hypo/plan.md` whose task W1-01 Risk line records `agent-decided: one-way door (published format) — the exported field is named timestamp, not the old ts`, and whose plan `## Risks` says nothing about doors. Also ran the criterion's own test: `uv run --isolated --with pytest python -m pytest -q loom-code/tests/test_ship_risk_section_agent_decided_door.py` in the clean copy, and the same test against the pre-change `ship/SKILL.md` (`git show b53adac2:loom-code/skills/ship/SKILL.md` copied into `$S/oldtree`).
- What came back:
  - Draft A: "Two-way door: no one-way door is recorded. The plan's Risks section states "No one-way door in this change", no task Risk line is marked as one, and the acceptance test report's "I decided for you" section holds none." Blast radius: closing reviewers may flag more tests; ship writers get a fuller risk section; loom-code users and maintainers; no runtime, no checker rule. Rollback: `git revert` the squash commit; installed copies see it only after the next version bump. Remaining risks: plan Risks 1 and 2.
  - Draft B: "One-way door: the plan's W1-01 Risk line records an agent-decided one-way door (published format). The exported field is named `timestamp`, not the old `ts`." Blast radius: downstream readers parsing `ts`, users with exported files. Rollback: reverting code does not change files already written; re-export or have readers accept both.
  - Pin test: clean copy `3 passed`; pre-change text `1 failed, 2 passed` (`test_ship_risk_placeholder_cites_agent_decided_doors` fails), so the test can fail.
- Evidence: drafts above (drafter cited ship/SKILL.md lines 69-75); `loom-code/tests/test_ship_risk_section_agent_decided_door.py`. Not tried: an actual `ship` run opening a real PR (outward-facing; not in scope of this test).

## 4. 完整 package suite 全部通過，版號與 CHANGELOG 一致。
- How I tried it: in the clean copy, `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`; then `grep '"version"'` on `loom-code/plugin.json`, `loom-code/.claude-plugin/plugin.json`, `loom-code/.codex-plugin/plugin.json`, `loom-code/package.json`; first `## [` heading of `loom-code/CHANGELOG.md`; version strings in `README.md`, `loom-code/README.md`, `loom-code/README.ja.md`, `loom-code/README.zh-TW.md`; `CURRENT_VERSION` in `loom-code/tests/test_write_plan_station_text.py`; `grep -rln 3.32.0` outside docs/.git (excluding CHANGELOG).
- What came back: suite exit 0; pytest summaries 1900 passed/2 skipped, 190/1, 53, 260, 121, 64, 22, 13, 1, 71/3, 201/5, 12, 155 → 3063 passed, 11 skipped, 0 failed; shell checks all PASS. All four manifests `"version": "3.33.0"`; CHANGELOG top `## [3.33.0] — 2026-10-05 — the tests lens names tests that cannot fail, and the ship PR risk section states door, blast radius and rollback`; README.md:17 and :132, loom-code/README.md:11, README.ja.md:11, README.zh-TW.md:9 all 3.33.0; `CURRENT_VERSION = "3.33.0"`; no stray 3.32.0 outside docs and CHANGELOG history.
- Evidence: suite log `$S/suite.log` (536 lines, scratch); grep output above. `finalize-review` reruns the same suite before the change is accepted and blocks it on failure.

## Re-run at e237802e (fix range 4c5b383f..e237802e)

Fix diff touched `loom-code/skills/ship/SKILL.md` (risk placeholder: agent-decided lines checked against the five classes of `../write-plan/references/one-way-door.md`; spec added to PR-body sources), `loom-code/skills/closing-review/references/lenses.md` (tests row: "prose-pin tests that meet ... §5 item 8 excepted"), `loom-code/tests/test_ship_risk_section_agent_decided_door.py` (wider NEGATION, second assert on `one-way-door.md`), `loom-code/CHANGELOG.md`. These reach A1, A2 (lenses row), A3 (ship placeholder + pin test) and A4 (suite), so all four were re-tested in full; nothing carried over.

### 0. Setup (re-run)
- How I tried it: `git worktree add --detach $S/clean3 HEAD` (e237802e, `git status --short` empty); `claude plugin validate loom-code`, `claude plugin validate .`, `python3 scripts/sync_codex_manifests.py --check --all`.
- What came back: `✔ Validation passed`; `✔ Validation passed with warnings` (same pre-existing `requires-contract` warning); sync exit 0.

### 1 + 2. tests lens: three lying shapes flagged; item-8 prose pin excepted (re-run)
- How I tried it: one fresh `loom-code:reviewer`, given only `$S/clean3/loom-code/skills/closing-review/references/lenses.md` (`tests` row) and two artifacts treated as changed test files, told nothing about which tests were seeded bad: (A) `$S/clean3/loom-code/tests/test_ship_risk_section_agent_decided_door.py` reading `$S/clean3/loom-code/skills/ship/SKILL.md`; (B) the A1 seeded repo `$S/seeded/tests/test_pricing.py` (unchanged from the first run). Reviewer ran both: A `3 passed`, B `4 passed`.
- What came back:
  - A: `tests: PASS`, findings `[]`. `test_ship_risk_placeholder_cites_agent_decided_doors` (:49) — "a prose-pin test that meets engineering-baseline §5 item 8, so it is covered by the row's carve-out" (affirmative verb before literal :33, negation rejected :31, self-tests present). Both self-tests "no finding".
  - B: `tests: NEEDS_REVISION`. important `test_pricing.py:11` — "restating a constant or the implementation"; important `test_pricing.py:16` — "reading source text to assert code structure (not a prose-pin test)"; important `test_pricing.py:24` — "a mock or stub replacing the very seam it claims to cover"; `test_checkout_total_member_cart` (:30) "no finding".

### 3. ship risk section (re-run)
- How I tried it: two fresh `general-purpose` (sonnet) drafters, each given only `$S/clean3/loom-code/skills/ship/SKILL.md` §2 (told to follow files it points to) plus inputs:
  - (i) this change: intent, plan, and the first-run acceptance test report from `$S/clean3`; no spec.
  - (ii) made-up plan `$S/hypo2/plan.md` + `$S/hypo2/intent.md`: W1-01 Risk `agent-decided — wrote the export as CSV with columns when,event,count rather than JSON, because the user's spreadsheet already opens CSV.` (no one-way label); W1-02 Risk `agent-decided — named the flag --out rather than --output`; plan Risks item 2 `No one-way door in this change.`; no spec, no report.
- What came back:
  - (i): "這次改動是 two-way door：沒有任何已記錄的 one-way door（plan 的 Risks 寫明「No one-way door in this change」；plan 裡 … task Risk 的 agent-decided 項目與驗收報告「我替你決定的事」3 項，逐條對照 one-way-door.md 的五類（a）到（e），都不落在其中任何一類）". Per-line table: W1-01, W1-02, W3-01 Risk lines and the three report items each `none` with a reason. Blast radius (closing-review reviewers, ship agents; no user data), rollback (revert + new patch version reaches installed copies), remaining risks present. Followed SKILL.md lines 41-45, 69-78, 83; read one-way-door.md lines 10-32, 66-76.
  - (ii): "One-way door. … Its Risks section says "No one-way door in this change", but checking the agent-decided lines one by one finds one that falls in class (c) of `one-way-door.md`" — W1-01 CSV `(c) limits what the user can do in future: it fixes the export data format` → Yes; W1-02 `--out` → None. Blast radius (users consuming exported files), rollback (revert the commits; already-exported CSV files stay; later format change needs a new flag or migration), remaining risks present. Followed SKILL.md lines 43-45, 69-78, 83.
  - Pin test: `uv run --isolated --with pytest python -m pytest -q loom-code/tests/test_ship_risk_section_agent_decided_door.py` in `$S/clean3` → `3 passed`; same test against pre-fix `git show 4c5b383f:loom-code/skills/ship/SKILL.md` in `$S/oldtree3` → `1 failed, 2 passed` (`test_ship_risk_placeholder_cites_agent_decided_doors` fails: the old placeholder has no `one-way-door.md`).
- Not tried: an actual `ship` run opening a real PR.

### 4. Package suite and version (re-run)
- How I tried it: in `$S/clean3`, `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q > $S/suite3.log`; then the same version greps as the first run.
- What came back: exit 0; pytest summaries 1900/2 skipped, 190/1, 53, 260, 121, 64, 22, 13, 1, 71/3, 201/5, 12, 155 → 3063 passed, 11 skipped, 0 failed; no `FAIL`/`failed` line in the log (535 lines). Four manifests `"version": "3.33.0"`; CHANGELOG top `## [3.33.0] — 2026-10-05 — …`; README.md:17, :132, loom-code/README.md:11, README.ja.md:11, README.zh-TW.md:9 all 3.33.0; `CURRENT_VERSION = "3.33.0"`; no `3.32.0` outside docs/.git/CHANGELOG.
- Evidence: `$S/suite3.log` (scratch). `finalize-review` reruns the same suite before the change is accepted and blocks it on failure.
