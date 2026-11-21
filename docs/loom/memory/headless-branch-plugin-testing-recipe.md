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

**How to apply:** follow the three steps above, plus these run safeguards
before trusting any corpus result:

- give each run a max-turns floor of at least 4 — `--max-turns 1` makes
  orient-first queries hit the turn ceiling, which reads as a trigger miss;
- give each query enough context to route — a context-less query draws a
  clarifying question instead, which also reads as a false miss;
- exclude session-limit records and genuine execution failures from
  grading, and report how many were excluded rather than dropping them
  silently — but KEEP `error_max_turns` records and grade them normally:
  a session that fires a skill and keeps working past the turn cap can
  hold a valid skill invocation;
- grade EXACT and FAMILY separately: a fire of a sibling skill in the
  expected skill's family counts as FAMILY, never folded into EXACT;
  and for a query that expects no skill, count an over-trigger only when
  a skill of the family under test fires — a correct non-family routing
  is not an over-trigger;
- write the corpus as phrasings derived from each skill's description,
  seasoned with the few real natural triggers, rather than mining
  transcripts wholesale (they are mostly "go/OK" continuations);
- when invocation counts cannot show whether a recommendation appeared,
  read the transcripts — the fired-skill count does not grade text.

**Historical (note 2026-11-21):** until the Loom 1.0 cutover (commit
eae874c43, 2026-09-03) these safeguards were documented in
`loom-code/scripts/loom_firing_harness.py`, which enforced some of them:
its `run` mode refused fewer than 4 turns (#1), `filter_contaminated`
discarded contaminated records (#3) and the `grade` mode separated
EXACT / FAMILY / OVER (#4); `validate_corpus` only warned on short
queries (#2), corpus phrasing was a hand-authoring rule (#5), and
whether a recommendation surfaced needed manual transcript inspection
(#6). Its `parse_corpus` took file content rather than a path, its module
docstring held the authoritative trap list (#1–#6), and corpora lived under
`docs/loom/firing-corpus/`. That harness, its parser and its corpus are
removed; the safeguards above are kept from its docstring because they
still apply to any hand-run `claude -p` corpus.
