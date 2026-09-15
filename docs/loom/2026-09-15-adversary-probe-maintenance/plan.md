# Adversary probe maintenance and reuse-first — plan
intent: 2026-09-15-adversary-probe-maintenance@98222a44
charter: 1.0

## Current State Evidence
- Forward: `loom-code/skills/build/SKILL.md:98-113` — the adversary never fixes what it breaks; after a fix Build re-runs existing programs and does not dispatch the adversary again.
- Reverse: `loom-code/agents/adversary.md:9-11,59-60` — "You do not fix what you break"; "Amend an unseen probe fix into that probe's original commit" is the only probe-edit rule.
- Error: `loom-code/skills/closing-review/references/adversarial.md:15-17` — "write at least three" cases with no instruction to check existing probes or tests first.
- Data: `docs/loom/*/evidence/probes/` — 37 files and 250 test functions on 2026-09-15; never collected by `scripts/run_package_tests.py`.
- Boundary: `loom-code/scripts/test_build_mechanical_checks.py` pins the end-of-Build sentences that W1-01 rewrites.

## Task DAG

### Wave 1

**W1-01 Let Build re-dispatch the adversary for stale probes**  after: none  acceptance: 1, 3
- Files: loom-code/skills/build/SKILL.md, loom-code/scripts/test_build_mechanical_checks.py
- Test: A1 positive: build-names-probe-update-exception; negative: implementer-may-edit-adversarial-program. A3 positive: trial-widened-scope-updates-probe-without-maintainer; negative: trial-needs-manual-probe-commit.
- Risk: agent-decided — one exception to "do not dispatch the adversary again", limited to programs that no longer fit a widened scope; keep the no-retry-loop rule for ordinary fixes.

**W1-02 Give the adversary update evidence and reuse-first rules**  after: W1-01  acceptance: 2, 4, 5
- Files: loom-code/agents/adversary.md, loom-code/skills/closing-review/references/adversarial.md, loom-code/scripts/test_build_mechanical_checks.py
- Test: A2 positive: update-requires-per-kind-mutation-on-committed-probe; negative: single-mutation-or-copy-accepted. A4 positive: report-marks-reused-modified-new; negative: new-probe-without-reason. A5 positive: suite-green; negative: prose-pin-negation-accepted.
- Risk: agent-decided — sequential after W1-01 because both files restate the same hand-off; pins follow the prose-pin rule (affirmative verb, negation rejected, self-tests).

### Wave 2

**W2-01 Close adversary findings on the probe-update exception**  after: W1-02  acceptance: 1, 2, 4, 5
- Files: loom-code/skills/build/SKILL.md, loom-code/agents/adversary.md, loom-code/skills/closing-review/references/adversarial.md, loom-code/scripts/test_build_mechanical_checks.py
- Test: A1 positive: sync-trunk-staleness-covered; negative: defect-guard-mutant-survives-pins. A2 positive: restore-original-rejection-mutation-required; negative: loosening-by-modify-accepted. A4 positive: branch-tests-excluded-from-reuse-floor; negative: implementer-pins-count-as-reuse. A5 positive: adversary-abuse-program-green; negative: rerun-sentence-deletion-survives.
- Risk: agent-decided — defect stays failing and returns a finding; exception extends to sync-trunk staleness; adversary program is read-only for the implementer.

**W2-02 Make mutation evidence runnable without discard commands**  after: W2-01  acceptance: 2, 3, 4
- Files: loom-code/agents/adversary.md, loom-code/skills/closing-review/references/adversarial.md, loom-code/scripts/test_build_mechanical_checks.py
- Test: A2 positive: mutation-applied-in-throwaway-copy-or-edit-tool; negative: git-checkout-discard-named-as-revert. A3 positive: rerun-trial-adversary-runs-own-mutations; negative: trial-blocked-by-discard-guard. A4 positive: flipped-case-marked-modified; negative: rewritten-case-marked-new.
- Risk: agent-decided — blind run found `git checkout --` refused by the host guard; mutations run on a throwaway copy of the committed probe; blind run re-runs Acceptance 3 afterwards.

## Questions asked
① — what — 對抗 agent 的兩個問題：範圍擴大後由對抗 agent 自己更新檢查並附正式突變證據；寫之前先查既有檢查與測試、逐項標沿用／修改／新增；本機暫存 repo 實跑驗證；授權自動 push 開 PR、合併前回「接受」；這樣對嗎？
① — what — 所以 A+ 實際上的修改有哪些？另外當前業界似乎有一派認為當前最新的模型其實少寫 prompt 指示效果更好，對此你的看法是？（使用者追問）
① — what — 要不要加「規則文件總字數不增加」與「新句子不用強烈字眼」兩條限制？（答：先不用 我們先做完 A+ 再一次整理所有的實作）

## Risks
1. user-decided — no word-budget or emphatic-wording constraint for this change (2026-09-16); consolidation of all rule text is a later change.
2. Acceptance 3 depends on the host safety check allowing the adversary to run and commit its own updated probe; untested, so the blind run reports the outcome either way.
