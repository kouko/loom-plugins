---
name: headless-branch-plugin-testing-recipe
description: Recipe for behaviorally testing an unpushed branch's Claude Code plugins headlessly — --plugin-dir wrapper, neutral empty cwd, probe hook injection first
type: process
sources:
  - resource: PR #488 (loom family connective tissue, firing tests 2026-07-04)
  - resource: docs/loom/2026-09-15-mechanical-checks-before-review/evidence/plugin-dir-reviewer-probe.md (2026-09-15) — --plugin-dir reached a dispatched subagent's role contract; --allowedTools swallowed the trailing prompt
---

To behaviorally test Claude Code plugins from an UNPUSHED branch
(e.g. with `claude -p` firing or refusal runs): installed plugins track
GitHub main, so a normal session exercises stale code — the cache's
version directories are the tell. Recipe:

1. **Wrapper script per plugin** overriding the installed copy:
   `exec claude "$@" --plugin-dir <repo>/<plugin>` — invoke the
   wrapper wherever your runner would invoke `claude`. The override
   also reaches subagents that session dispatches: their role
   contracts load from the branch, not the installed cache. Pass the
   prompt on stdin (or write `--allowedTools=Agent`): `--allowedTools`
   takes every following argument, so a trailing prompt is swallowed
   and `-p` fails with "Input must be provided either through stdin or
   as a prompt argument".
2. **Run from a neutral EMPTY directory** — leftover artifacts in a
   working/scratchpad directory contaminated 3 test records by
   giving the model unintended context.
3. **Probe that the hook injects BEFORE burning corpus runs** — one
   cheap probe session to confirm the branch's hook content actually
   loads, before spending tokens on the full corpus.

**Why:** without the wrapper you silently test main instead of your
branch; without the empty directory and the probe, failed records
look like routing bugs when they are setup bugs.

**How to apply:** follow the three steps above.
