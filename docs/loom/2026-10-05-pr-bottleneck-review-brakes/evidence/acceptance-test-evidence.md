# Name lying tests in review and state merge risk in PR bodies — acceptance test evidence

Tried on 2026-10-05, in a clean copy of the project at 30642536.

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
