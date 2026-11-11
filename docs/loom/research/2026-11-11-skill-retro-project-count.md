---
title: "Skill-retro project identity and sampling reliability"
type: loom-research
status: concluded
created: 2026-11-11
updated: 2026-11-11
tags:
  - loom/research
---

# Skill-retro project identity and sampling reliability

## Question and scope

At repository commit `a8ec84e02740b58820055249e40e186d63233fbd`, determine whether the project-count finding remains actionable, its downstream effects, and the smallest defensible repair boundary. This is analysis, not authorization to implement or release a fix. Production files and historical evidence remain unchanged.

The earlier local retrospective is `/private/tmp/loom-retro-20261110/report.zh-TW.md`. Its P1-B identified sessions being counted as projects. This investigation focuses on that item, not a renewed whole-project audit or the other proposed host-behavior experiments.

## Method and rationale

Trace the current CLI, adapters, aggregation, selection and proposal grouping; inspect the corresponding tests; then compare identical synthetic inputs with omitted versus explicitly correct project mappings. CLI probes use isolated temporary transcript roots and an empty facets directory, never the operator's live history. This combination distinguishes a display-only issue from selection changes without modifying production code or invoking paid model analysis. Local source and execution resolve this question; external search is unnecessary.

## Findings

### 1. The production integration loses information before counting

The [Event model](../../../loom-workflow/skills/skill-retro/scripts/event.py) has source file and line fields, but no working directory or project identity. The Claude adapter's `_record_to_event` does not retain the transcript's `cwd`. The [Codex adapter](../../../loom-workflow/skills/skill-retro/scripts/ingest.py) assigns `path.stem` as session identity and processes `response_item` records, without deriving identity or cwd from `session_meta`.

The [CLI](../../../loom-workflow/skills/skill-retro/scripts/main.py) calls `aggregate_by_skill` without `session_to_project`. The [aggregator](../../../loom-workflow/skills/skill-retro/scripts/aggregate.py) substitutes session IDs for project paths. A partial mapping also substitutes the session ID for every missing entry. Consequently, merely adding a mapping argument is insufficient unless metadata reaches that argument and unknown entries stop inventing projects.

### 2. This changes ranking, not just confidence labels

`cross_project_norm` contributes 0.25 of the weighted score. Confidence becomes high at two reported projects. The number of projects is normalized against the largest count among candidates, so one inflated candidate can also change another candidate's score. Ranking chooses the top candidates sent for analysis; the default minimum is three sessions.

Controlled experiment: A has 12 invocation events across four sessions in one project; B has 12 across three sessions in three projects. Timestamps are identical and there are no friction signals. The current CLI selects A before B. Supplying the correct project mapping to the existing aggregator reverses the order:

| Condition | A score / confidence | B score / confidence | Order |
| --- | --- | --- | --- |
| Current omitted mapping | 0.7500 / high | 0.6875 / high | A, B |
| Known correct mapping | 0.5833 / low | 0.7500 / high | B, A |

Scores are rounded to four decimals. This is a controlled sensitivity demonstration, not evidence that a particular historical proposal was wrongly selected.

### 3. Duplicate sessions are a related but separate defect

A second CLI probe stores one Codex `session_meta.id` and one synthetic explicit Skill call under three filenames. The current CLI reports three sessions, three projects and high confidence, crossing the three-session selection threshold. The explicit Skill call isolates identity handling; it does not claim that native Codex normally invokes skills with this tool shape.

Fixing project identity alone cannot prevent duplicate transcripts from inflating session counts or event-frequency scores. Identical source sessions must be recognized without concatenating overlapping histories and counting events twice. Differing copies may contain unique events; blindly dropping all but the first file is not established as safe. Forked conversations require provenance about shared history before claiming independent support.

### 4. Raw working-directory strings are not canonical project identities

Supplying four different worktree paths to the current aggregator produces four projects. It treats supplied values as identities; it performs no repository canonicalization.

Read-only Git inspection of this checkout and its existing `memory-pointer-on-disk-state` worktree returned the same absolute common Git directory, `/Users/kouko/GitHub/loom-plugins/.git`. That is usable evidence for grouping existing local linked worktrees. A repository subdirectory should resolve to the same project as its root.

This does not settle historical deleted worktrees, moved directories, separate clones, or non-Git projects. Unknown provenance must remain unknown rather than becoming a new project. Do not group solely by basename or remote URL: neither has been established as the intended project boundary here. Current filesystem resolution also does not prove historical identity when a path has been reused.

### 5. Project confidence is not the proposal-promotion gate

The [proposal grouping code](../../../loom-workflow/skills/skill-retro/scripts/cluster.py) promotes matching observations using distinct session IDs, not `confidence` or project count. The [proposal renderer](../../../loom-workflow/skills/skill-retro/scripts/propose.py) remains proposal-only. Therefore the confirmed project-count bug directly affects selection and displayed confidence; it does not itself bypass an implementation or publication approval.

Duplicate session identities can plausibly inflate the grouping support count if duplicate analyses produce matching observations. That propagation is supported by source inspection, but no full model-analysis-to-proposal run was performed here. Project independence and session independence must remain separate concepts; replacing every session threshold with a project threshold would change the product contract rather than simply fix this bug.

### 6. Existing green tests do not exercise the missing connection

The focused suite returned **136 passed**. `test_confidence_tagging_uses_cross_project_count` supplies a correct mapping manually and verifies that two sessions in one project remain low confidence. The principal CLI payload test checks keys, sessions and dispatch data, but does not verify source cwd through to canonical project count. Thus the correct aggregation capability and the broken default integration coexist.

## Evidence and reproduction

- Current source: [main.py](../../../loom-workflow/skills/skill-retro/scripts/main.py), [ingest.py](../../../loom-workflow/skills/skill-retro/scripts/ingest.py), [event.py](../../../loom-workflow/skills/skill-retro/scripts/event.py), [aggregate.py](../../../loom-workflow/skills/skill-retro/scripts/aggregate.py), [cluster.py](../../../loom-workflow/skills/skill-retro/scripts/cluster.py), [propose.py](../../../loom-workflow/skills/skill-retro/scripts/propose.py).
- Tests inspected: [test_aggregate.py](../../../loom-workflow/tests/skill-retro/test_aggregate.py), [test_main.py](../../../loom-workflow/tests/skill-retro/test_main.py).
- Temporary executable probe: `/private/tmp/loom-retro-count-analysis-20261111/probe.py`; run with `PYTHONDONTWRITEBYTECODE=1 python3 /private/tmp/loom-retro-count-analysis-20261111/probe.py`.
- Actual probe results: `/private/tmp/loom-retro-count-analysis-20261111/results.json`; generated CLI payload and fixtures are in the `fixture_directory` named there. The script imports current production code; a future run needs revision pinning to compare with this observation.
- Focused tests: `uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-workflow/tests/skill-retro/ -q` returned `136 passed in 0.24s`. Existing cache access required sandbox escalation; no package change was made.
- Worktree inspection: `git -C <path> rev-parse --path-format=absolute --git-common-dir`, run for this checkout and `/Users/kouko/GitHub/loom-plugins/.claude/worktrees/memory-pointer-on-disk-state`, returned the same common directory, exit 0 for each.

## Decision impact

Prioritize identity correctness over more transcript adapters or ranking changes.

1. A bounded first repair can retain observed cwd/project metadata, resolve existing linked worktrees consistently, propagate actual identity to aggregation, and prevent missing identity from counting as a distinct project. Keep current ranking weights and the separate session-support policy. Include CLI-level regression coverage, not just manually mapped aggregate tests.
2. Follow with session identity and duplicate-history handling, or include it in the same change only if the promised outcome is trustworthy automatic ranking. Otherwise disclose that the first repair corrects project counts but does not make the entire sampler reliable.
3. Defer OpenCode support, compressed archives, date filtering, and broader analysis-prompt changes. They expand coverage but cannot repair false counts in data already read.

Acceptance targets for a future repair: multiple sessions in one repo count as one project; linked worktrees and repo subdirectories do not multiply projects; genuinely separate known repositories stay separate; missing or partial metadata cannot manufacture high cross-project confidence; source provenance remains inspectable; the actual CLI produces the expected candidate order. Session-dedup work additionally needs same-ID copies, overlapping-but-divergent copies and forks, with shared events not counted as independent evidence and unique events not silently lost.

Keeping the current implementation is acceptable only for explicitly selected, manually checked investigations that do not rely on automatic cross-project scores. Merely renaming the confidence label or passing raw cwd strings leaves the demonstrated ranking or worktree problem unresolved. Rewriting all adapters and ranking together adds unrelated scope.

## Limitations and open questions

No production repair, formal closing review, fresh independent review, installed-host test or full model-analysis-to-proposal replay was performed. The controlled probes demonstrate current implementation behavior, not population error rates. Historical non-Git/deleted/moved locations and fork independence remain design questions for an authorized repair. Temporary probe artifacts may be cleaned by the OS; the durable record preserves inputs, observations, scope and source links. The other priorities from the earlier retrospective were not re-executed in this investigation.
