# Reviewer floor and process notes — plan
intent: 2026-09-19-reviewer-floor-and-process-notes@df28d293
charter: 1.0

## Current State Evidence

- Forward: `loom-code/scripts/loom_checker/reviewers.py:24` `reviewer_floor_for_paths`
  — a positive allowlist that recognises only `.md/.mdx/.rst/.txt` as low-risk;
  a `.json` manifest touch falls through to the default floor of 2 regardless
  of how narrow its actual diff is.
- Reverse: `loom-code/scripts/test_loom_attestation.py:155`
  `test_reviewer_floor_is_one_only_for_narrow_low_risk_paths` is the existing
  contract for this function; no case in it covers a JSON file at all.
- Error: no test anywhere asserted that removing an existing recognizer must
  preserve its prior test coverage; the removal that motivated this intent
  (a separate, since-abandoned branch) shipped a coverage gap that only
  surfaced across three later verification passes.
- Data: `docs/loom/memory/index.md` and its gotcha section had no entry
  recording that a Loom memory commit must land before `finalize-review`,
  though `loom-code:closing-review`'s own SKILL.md already states the
  underlying rule ("A recorded lesson is functional content like anything
  else committed").
- Boundary: `heading_window.py` and `sibling_import.py` had zero references
  from live code, skill, or agent text anywhere in the tracked tree (verified
  with `git grep`, not only `loom-code/scripts`' own import graph, which
  falsely cleared two OTHER files as dead earlier in the same investigation).
  Both names still appear in `loom-code/CHANGELOG.md` and
  `loom-design/CHANGELOG.md` as history, which this removal does not touch.

## Task DAG

**W0-01 Recognize a version-only JSON bump as low risk**  after: —  acceptance: 1
- Files: `loom-code/scripts/loom_checker/reviewers.py`, `loom-code/scripts/test_loom_attestation.py`
- Test: A1 positive: version-only change on both sides of a `.json` file yields floor 1; negative: a second field changed, a newly added file, or malformed JSON each still yield floor 2.
- Risk: recomputes structural equality from git blobs, not the filename (NN3); widens an existing checker rule, no new mechanism. See W0-05 for gaps this first cut left open. agent-decided.

**W0-05 Close five adversarial gaps in the version-only JSON check**  after: W0-01  acceptance: 1, 5
- Files: `loom-code/scripts/loom_checker/reviewers.py`, `loom-code/scripts/test_loom_attestation.py`, `loom-code/scripts/test_adversarial_reviewer_floor_json.py`
- Test: A1 positive: a real bump (incl. NaN) yields floor 1; negative: `0`→`false`, `3`→`3.0`, a duplicate key, `version` retyped, and a 3000-deep file each yield floor 2. A5 positive: suite green; boundary: `xfail(strict=True)` on the blind spot.
- Risk: fixing bool/int equality broke a held NaN case (two parses share one interned object); restored with an identity check first. agent-decided.

**W0-02 Require existing test coverage to be named before removing a protected function**  after: —  acceptance: 2
- Files: `loom-code/skills/write-plan/SKILL.md`
- Test: A2 positive: word count stays under the skill's soft cap; boundary: `check-skill-crossrefs.py` still resolves.
- Risk: prose-only, not a checker rule; a task can slip past it. A review found it could collide with the Risk line's own 40-word cap; now points at the existing spec-escape for that case. agent-decided.

**W0-03 Warn that a memory entry must precede finalize-review**  after: —  acceptance: 3
- Files: `loom-workflow/skills/git-memory/SKILL.md`
- Test: A3 positive: word count stays well under cap; boundary: `check-skill-crossrefs.py` on loom-workflow still resolves.
- Risk: prose-only; the mechanical guard (content_digest mismatch) already existed and caught the incident that motivated this note. agent-decided.

**W0-04 Remove two modules with zero live references**  after: —  acceptance: 4, 5
- Files: `loom-code/scripts/heading_window.py`, `loom-code/scripts/sibling_import.py`, `loom-code/scripts/test_heading_window.py`, `loom-code/scripts/test_sibling_import.py`
- Test: A4 positive: package suite green after removal; negative: repo-wide `git grep` finds only history prose (memory, CHANGELOG). A5 positive: `pytest loom-code/scripts -q` zero failures; boundary: collected count matches pre-removal minus four.
- Risk: their own tests (`test_heading_window.py`, `test_sibling_import.py`) exercised only these two modules, so removal narrows coverage to nothing rather than dropping a shared case; an import-graph-only check had falsely cleared two unrelated live files earlier this session. agent-decided.

## Questions asked

① — consequence — 啟動 closing-review 把這條分支推上去 — 「啟動 closing-review 把這條分支推上去」(使用者已在稍早的對話裡看過完整的四項改動內容並個別確認,此為最終發佈確認)

## Risks

1. W0-01 changes checker code the gate itself protects, so this branch computes reviewer floor 2 for itself regardless of W0-01's own fix — expected and correct, not a defect.
2. The first four commits landed before this intent/plan existed (implement directly, formalize after, as asked). Content changed twice more since: an adversarial round (`ba2c3f0a`, now W0-05) and reviewer-response fixes reflected in W0-01/W0-02's own lines.
