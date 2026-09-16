# Clean stale references — plan
intent: 2026-09-16-clean-stale-references@cb04eaea
charter: 1.0

## Current State Evidence
- Forward: `docs/loom/README.md` "Frozen stores" list links `specs/`, `backlog/`, `design/`, `archive/`, `BACKLOG.md` and two 2026-07 folders, none present.
- Reverse: `loom-workflow/skills/distill-sessions/references/codex-tools.md:8` cites loom-code's `codex-tools.md`, deleted in eae874c4.
- Error: `loom-code/docs/examples/README.md:31` links `skills/using-loom-code/references/codex-tools.md`, which does not exist.
- Data: N/A — prose only.
- Boundary: `docs/loom/plans/` exists and stays listed; write-spec's "ten completeness questions" matches `references/spec-forms.md:84`.

## Task DAG

**W1-01 Drop dead codex-tools pointers**  after: none  acceptance: 1, 3
- Files: loom-workflow/skills/distill-sessions/references/codex-tools.md, loom-code/docs/examples/README.md
- Test: A1 positive: no-missing-file-named; negative: grep-codex-tools-md-absent. A3 positive: examples-link-removed; negative: link-target-missing.
- Risk: Removing rather than repointing — no live successor document exists. agent-decided.

**W1-02 Frozen-store list matches the tree**  after: none  acceptance: 2
- Files: docs/loom/README.md
- Test: A2 positive: every-linked-path-exists; boundary: plans-still-listed.
- Risk: `plans/` has no ARCHIVED.md, so the sentence claiming one is removed. agent-decided.

## Questions asked
① — what — 你要的是把幾份文件裡指向不存在檔案的連結清掉，而且不能誤刪還存在的東西。這樣對嗎？

## Risks
1. First Acceptance set rested on unverified claims; re-confirmed after checking each path on disk.
