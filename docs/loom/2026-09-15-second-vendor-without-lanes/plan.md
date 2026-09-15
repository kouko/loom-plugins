# Second-vendor suggestion without lanes — plan
intent: 2026-09-15-second-vendor-without-lanes@17c592ff
charter: 1.0

## Current State Evidence
- Forward: `loom-code/scripts/second_vendor_policy.py:110` — `lane = _require_string(packet.get("lane"), "lane", LANES)`; a missing lane exits 2.
- Reverse: `loom-code/skills/write-plan/SKILL.md:467` — tells the agent to pass "the observed mode, lane, host" to the policy; no rule defines lane.
- Error: `loom-code/scripts/second_vendor_policy.py:138-153` — `small` returns `opt_in_eligible: false`, `full` returns `true` for the same packet.
- Data: `docs/loom/KICKOFF-DEFAULTS.md:14` — lanes were removed by expert-mode; `loom-code/contract/manifest.yaml:258` still says `ask` blocks "once per full-lane change".
- Boundary: `loom-design/skills/capture-intent/SKILL.md:44,252` and `references/second-vendor.md:29,50` — the same lane wording in the upstream station.

## Task DAG

### Wave 1

**W1-01 Remove the lane input from the second-vendor policy**  after: none  acceptance: 1, 3
- Files: loom-code/scripts/second_vendor_policy.py, loom-code/scripts/test_second_vendor_policy.py
- Test: A1 positive: same-packet-same-result-without-lane; negative: lane-field-rejected-as-unknown. A3 positive: narrow-change-gets-opt-in; boundary: accept-after-review-started-is-next-change-only.
- Risk: agent-decided — every change follows today's full-lane branch (user-decided B); reason codes drop the lane prefix; a caller still sending `lane` fails loudly as an unknown field.

**W1-02 Remove lane wording from station text and contract**  after: W1-01  acceptance: 2, 4
- Files: loom-code/skills/write-plan/SKILL.md, loom-code/skills/write-plan/references/second-vendor-ask-and-docs-lint.md, loom-code/contract/manifest.yaml, loom-code/scripts/test_write_plan_station_text.py, loom-design/skills/capture-intent/SKILL.md, loom-design/skills/capture-intent/references/second-vendor.md, loom-design/scripts/spec/test_capture_intent_contract.py
- Test: A2 positive: no-lane-word-in-loom-code-loom-design-station-text; negative: small-lane-branch-still-described. A4 positive: suite-green; negative: station-text-pin-still-expects-full-lane.
- Risk: agent-decided — the `ask` question and suggest notice apply to every change; pins asserting "every full-lane change" move to "every change".

### Wave 2

**W2-01 Record the probe-maintenance gotcha**  after: W1-02  acceptance: 4
- Files: docs/loom/memory/a-probe-outpaced-by-scope-growth-needs-a-maintainer.md, docs/loom/memory/index.md
- Test: A4 positive: memory-store-integrity-hook-passes; negative: contradicting-entry-left-unreconciled.
- Risk: agent-decided — the charter's harness-friction home `environment-gotchas.md` no longer exists, so the lesson lands in this store; one fact, no new intent.

## Questions asked
① — what — 修掉「要不要建議找其他公司的 AI 再審查」這一步對已刪除的「大／小改動」設定的依賴，同一個改動每次結果一樣，所有改動都會問，並授權自動 push 開 PR、合併前回「接受」；這樣對嗎？
① — what — 只改文件或測試的小改動，要不要也問你要不要找其他公司的 AI 再審查？（答：B 我覺得還是問 因為當前不卡流程繼續進行 而且問的時候我記得也會給建議是要用還是不要用）
① — what — 可以用更白話的方式說明嗎？ 但是不要用比喻（使用者要求改寫說明）

## Risks
1. user-decided — every change, including a narrow low-risk one, is offered the second-vendor opt-in (2026-09-15); suggest mode never waits, and a recommendation appears only with risk evidence.
2. The memory charter names a harness-friction file that no longer exists; W2-01 records in `docs/loom/memory/` and notes that gap.
