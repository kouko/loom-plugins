---
name: execute-cheap-loom-simplify-upgrades-at-review
description: When review finds a LOOM-SIMPLIFY marker whose recorded upgrade is one-line-cheap, the reviewer reports the upgrade as a finding and the implementer executes it in the fix round instead of leaving the marker (on 2026-07-04 the upgrades were executed at review time)
type: practice
sources:
  - resource: PR #479 (loom-pipeline conductor v0.1, 2026-07-04)
---

`LOOM-SIMPLIFY:` is loom-code's in-code marker for a deliberate,
scope-bounded shortcut; each marker records the shortcut, a
checkable ceiling, the upgrade path, and a reference
(`loom-code/skills/subagent-driven-development/standards/deliberate-simplification.md`).
When review reaches such a marker and the recorded upgrade turns out
to be one-line-cheap, execute the upgrade right there instead of
leaving the marker for later. On PR #479 three such upgrades were
executed at review time — a hardcoded personal checkout path became
a `skillsRoot` argument, hardcoded station names were generalized,
and a probe budget was parameterized — and all three paid off
immediately.

Note 2026-11-21: the `deliberate-simplification.md` reference was
removed with the subagent-driven-development skill; today no plugin
document defines the marker (its original definition is the
loom-code 0.19.0 entry in `loom-code/CHANGELOG.md`), and markers remain
in code, e.g. `loom-workflow/skills/git-memory/scripts/privacy-scan.py`.
Today's reviewer never edits what it reviews
(`loom-code/agents/reviewer.md`), so "execute it right there" now means
the upgrade is applied by the implementer in the fix round.

**Why:** a marker whose upgrade costs less than re-reading the
marker later is pure debt; deferring it buys nothing and risks the
shortcut outliving its ceiling unnoticed.

**How to apply:** at review time, the reviewer prices each
LOOM-SIMPLIFY upgrade it encounters; if it is roughly one line (or
comparably trivial), it reports the upgrade as a finding, with the
justification, and the implementer applies it and deletes the marker
in the fix round. Keep the marker only when the upgrade is genuinely
non-trivial.
