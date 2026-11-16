# Expanded planning judgment — Build checks

2026-11-17. Production candidate first committed at 562ad5dc; final source and
research-snapshot clarification at 30cc3125. Skill/README bytes are identical
between those commits. Complete source frontmatter matches the 087f5057 baseline.
Candidate SKILL.md SHA256: 5724fefe4e85e7ff8fe024f66aab2a920bb0d46017d57a23cce5bfa28e22d4c5.

`sync-trunk` reported up to date at 562ad5dc against origin/main 9bbab926.
No trunk content was added. Fresh scoped adversary observations and limitations
are retained in planning-knowledge-adversarial.md; no new program was earned.

Executed the complete KICKOFF-DEFAULTS locked package command:

```text
uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q
exit 0
4,036 pytest cases across 16 runner groups, plus discovered shell inventory
```

The first candidate run passed, then the same complete suite passed again on
the final committed source after clarifying historical research status. Both
logs remain local rather than conflating the earlier run with the final tree.
After the final suite, executed the retained adversarial program unchanged:

```text
python3 -m pytest loom-code/tests/test_loom_checker_intent.py -q
65 passed in 19.57s
exit 0
```

No new retained executable attack or prose-presence regression was added.
The existing program measures preserved gate behavior, not the new planning
semantics. Focused packaging/catalog tests separately passed 11 cases.

At this record's creation, matched native comparisons were still running.
They use four frozen cases, three independent native contexts per arm/case,
the old skill baseline and frozen candidate, with evaluator criteria withheld
from executors. No semantic pass, relative improvement, installed-host activation
or universal domain coverage follows from this mechanical report. Independent
grading and clean acceptance remain required before closing review.
