# Stale monkey-skills references — plan
intent: 2026-09-14-stale-monkey-skills-refs@63d914b1
charter: 1.0

## Current State Evidence
- Forward: `loom-workflow/skills/distill-sessions/README.md:199` — "This skill is part of the [monkey-skills]" (ja:201, zh-TW:192 carry the same claim).
- Reverse: `loom-code/tests/integration/test-superpowers-mode-on.sh:119` — prints `claude plugin install loom-code@monkey-skills`; `loom-code/tests/integration/README.md:19` example path.
- Error: `loom-code/scripts/check_contract_citations.py:10` and `loom-workflow/skills/distill-sessions/scripts/main.py:77,89` — comments name this repository `monkey-skills`.
- Data: `PRINCIPLES.md:1` and `docs/loom/KICKOFF-DEFAULTS.md:1` — titles name `monkey-skills`; the checker reads their other lines.
- Boundary: `loom-workflow/skills/critique/NOTICE:24-26`, CHANGELOGs, fixtures — historical or attribution wording that must stay.

## Task DAG

### Wave 1

**W1-01 Reword stale present-tense references**  after: none  acceptance: 1, 2, 3, 5
- Files: loom-workflow/skills/distill-sessions/README.md, loom-workflow/skills/distill-sessions/README.ja.md, loom-workflow/skills/distill-sessions/README.zh-TW.md, loom-code/tests/integration/test-superpowers-mode-on.sh, loom-code/tests/integration/README.md, loom-code/scripts/check_contract_citations.py, loom-workflow/skills/distill-sessions/scripts/main.py
- Test: A1 positive: readme-says-developed-in; negative: readme-says-part-of. A2 positive: hint-uses-loom; negative: hint-uses-monkey. A3 positive: comments-name-loom-plugins; negative: comment-names-monkey. A5 positive: suite-green; negative: pinned-string-broken.
- Risk: agent-decided — one-line wording edits only; attribution files, CHANGELOGs and fixtures stay untouched.

**W1-02 Rename two repository document titles**  after: W1-01  acceptance: 4, 5
- Files: PRINCIPLES.md, docs/loom/KICKOFF-DEFAULTS.md
- Test: A4 positive: titles-renamed; boundary: other-lines-byte-identical. A5 positive: suite-green; negative: standing-docs-unparseable.
- Risk: agent-decided — change line 1 only; ratification and key lines are read by the checker and stay byte-identical.

## Questions asked
① — what — 你覺的剩下來有提到 monkeyskill 的部分要改嗎？（我建議改 4 處、保留歷史與授權文件，兩個標題由使用者決定；答：改吧，兩個標題也一起改）
① — what — 這次要改的 5 條驗收條件與不動的部分，並授權審查通過後自動 push、開 PR、CI 綠了合併；這樣對嗎？

## Risks
1. `check_contract_citations.py` scans prose for repository citations; its own docstring edit must not introduce a new citation violation — run it after the edit.
