# Recovered retrospective review finalization — plan
intent: 2026-10-16-retro-review-finalization@7b8ac5b0
charter: 1.1

## Current State Evidence

- Forward: `loom-workflow/tests/skill-retro/test_propose.py:779,798` contains the two graduated regression cases.
- Reverse: `loom-workflow/skills/using-loom-workflow/SKILL.md:19,29` routes the two retrospective targets under their confirmed names.
- Error: `loom-code/scripts/loom_checker/probes.py:417` rejects a graduated program with no `concern:` in its first 20 lines.
- Data: `docs/loom/2026-10-14-project-and-skill-retro/acceptance-test-report.md` records earlier acceptance results against the lost review episode.
- Boundary: `loom-code/skills/closing-review/SKILL.md` limits one confirmed-intent episode to three functional digests and binds review evidence to content.

## Task DAG

**W1-01 Restore finalization readiness**  after: none  acceptance: 1, 2, 3
- Files: `loom-workflow/tests/skill-retro/test_propose.py`
- Test: A1 positive: both-retros-contract; boundary: no-old-alias. A2 positive: formal-suite-and-finalize; negative: missing-concern-rejected. A3 positive: ready-pr-verification; boundary: no-merge.
- Risk: agent-decided — add only the existing cases' concern metadata near the file start; Closing Review owns fresh verdicts and attestation, while Ship owns PR publication.

## Simplicity check

- none found

## Questions asked

- ① — what — `loom-design:capture-intent` 要求新的修復意圖先由你確認，因為原審查已達三輪上限。我的理解是：保留已確認的 `project-retro`／`skill-retro` 範圍，針對還原後的實際內容重新完成測試與獨立審查；通過後自動推送並建立 Ready PR，合併另行決定。這是你要的結果嗎？

## Risks

1. The recovered tree has no original reviewed Git object; fresh reviewers must inspect the cumulative change, and old verdicts cannot be reused.
2. The earlier acceptance report covers a lost digest; re-test affected acceptance on the new committed content before review.
