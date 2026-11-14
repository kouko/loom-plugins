---
title: "Applying SourceAtlas concepts to engineering-research"
type: loom-research
status: concluded
created: 2026-11-14
updated: 2026-11-14
tags:
  - loom/research
---

# Applying SourceAtlas concepts to engineering-research

## Question and scope

Which SourceAtlas concepts or implementations could improve engineering-research,
given its actual historical uses and failures?

This is an assessment, not authorization to change/install a skill. Local baseline:
`3b1a9972644517911454530dc1876f88525b1f37`; local engineering-research main text
matches installed loom-code 3.79.0. SourceAtlas snapshot:
`e3c7d6cf92f9e477f328b20b9b1d8a107d3ffd87`, manifest version 2.13.1.
No actual active implementation change was established from the branch name.

## Method and rationale

Use a lightweight trade study: compare historical failure coverage, correctness,
portability, operating burden and proportionality. Inspect retained local execution
reports and incident research, then trace upstream skill wrappers to command
instructions and the relevant helper/test code. Inspect counterexamples to the
initial hypothesis that another analysis workflow would solve the observed gaps.

The identified public upstream is sufficient for this bounded question; no extra
English/Japanese discovery searches or private-session uploads were necessary.
Historical reports are attributed observations, not newly repeated experiments.
No upstream setup, package installation, model trial or performance benchmark ran.

## Findings

### Historical need, rather than a feature-count comparison

| Historical evidence | Observed result | Relevance |
|---|---|---|
| [Code-owned dogfood](../../skill-dogfood/2026-11-08-code-owned-engineering-research/report.md), DF-003–005 | Some actors omitted substantive saved-content readback, overstated link verification, or exceeded a discovery boundary despite explicit rules | More prose alone has no demonstrated corrective effect; final-file correctness does not prove the claimed verification occurred |
| [RAR-to-ZIP diagnosis](2026-11-12-recommendation-evidence-gap.md), historical observations | A nested ZIP implementation choice lacked comparison; a user challenge reversed the recommendation without new evidence; the retained note kept the old choice | Need claim-specific support and synchronized conclusions, not just repository orientation |
| [Framework trial](../../skill-dogfood/2026-11-08-engineering-research-frameworks/report.md), same-case results | Old/new versions reached the same main substantive outcomes in six paired cases | A larger method catalog is not established improvement |
| [CLI guidance research](2026-11-13-cli-agent-design-guidelines.md), source-traced examples and probes | Research already traced upstream dispatch/executor/error paths and used eight bounded local probes | SourceAtlas-style path tracing is partly existing practice; an added helper needs incremental benefit |

These are selected engineering-research records from November 8–13, not an
exhaustive cross-host history review. The November 7 evaluation memory was used
to locate context; its obsolete round-3 report path was unavailable in this
checkout, so remembered counts are not used as newly verified results here.

### What SourceAtlas actually implements

The six `plugin/skills/*/SKILL.md` wrappers primarily route natural questions to
commands. For example, codebase-overview invokes overview, and code-flow-tracer
invokes flow. The analysis is largely model-executed instructions, complemented
by local shell tools; it is not an independently verified semantic code graph.

| Mechanism | Source observation | Possible application |
|---|---|---|
| Prioritize informative files | [Scanner](https://github.com/lis186/SourceAtlas/blob/e3c7d6cf92f9e477f328b20b9b1d8a107d3ffd87/scripts/atlas/scan-entropy.sh#L18-L101) lists conventional documentation/configuration paths and line counts | A bounded orientation aid for an unfamiliar repository; choose by the actual research question |
| Explicit hypotheses | [Constitution, Article III](https://github.com/lis186/SourceAtlas/blob/e3c7d6cf92f9e477f328b20b9b1d8a107d3ffd87/ANALYSIS_CONSTITUTION.md) associates a hypothesis with evidence and a validation method | For consequential unknowns, retain claim, supporting observation and the observation that would refute it; avoid mandatory hypothesis quotas |
| Trace actual paths | [Flow command, steps 2–3](https://github.com/lis186/SourceAtlas/blob/e3c7d6cf92f9e477f328b20b9b1d8a107d3ffd87/plugin/commands/flow/SKILL.md) reads functions, follows calls, records locations and stops at boundaries | Make selected entry/configuration/failure paths explicit in repository research; source tracing remains distinct from observed runtime behavior |
| Structure-aware search with fallback | [Pattern workflow](https://github.com/lis186/SourceAtlas/blob/e3c7d6cf92f9e477f328b20b9b1d8a107d3ffd87/plugin/commands/pattern/workflow.md), step 1.5, selects ast-grep for content patterns; [call helper](https://github.com/lis186/SourceAtlas/blob/e3c7d6cf92f9e477f328b20b9b1d8a107d3ffd87/scripts/atlas/ast-grep-search.sh#L264-L335) has AST and text alternatives | Optional existing tooling when text search produces consequential ambiguity; no default new dependency |
| Recompute simple report claims | [Fact checker](https://github.com/lis186/SourceAtlas/blob/e3c7d6cf92f9e477f328b20b9b1d8a107d3ffd87/tests/evals/fact-check.sh#L128-L157) checks path existence and line bounds, plus selected counts/configuration | Best concrete implementation idea: recompute reference validity and compare reported quantities with observations |
| Inspect co-change history | [History workflow](https://github.com/lis186/SourceAtlas/blob/e3c7d6cf92f9e477f328b20b9b1d8a107d3ffd87/plugin/commands/history/workflow.md) prepares git logs and invokes code-maat for coupling/ownership | Useful only when evolution or co-change could alter the decision; ordinary git history remains the smaller default |

The scanner does not calculate information-theoretic entropy: the inspected
implementation uses filename/directory heuristics. Likewise, pattern ranking
uses filename match scores and directory bonuses ([ranking implementation](https://github.com/lis186/SourceAtlas/blob/e3c7d6cf92f9e477f328b20b9b1d8a107d3ffd87/scripts/atlas/find-patterns.sh#L1850-L1946)).
These are useful discovery heuristics, not proof of representative sampling or
the best implementation. Calling them "information theory" adds no validation.

### What should not transfer unchanged

1. **Fixed scan ratios and hypothesis/confidence targets.** Overview prohibits
   deep inspection and requests high-confidence hypotheses. Research must instead
   inspect as far as a consequential claim requires, including failure paths.
   The [constitution](https://github.com/lis186/SourceAtlas/blob/e3c7d6cf92f9e477f328b20b9b1d8a107d3ffd87/ANALYSIS_CONSTITUTION.md),
   [overview](https://github.com/lis186/SourceAtlas/blob/e3c7d6cf92f9e477f328b20b9b1d8a107d3ffd87/plugin/commands/overview/SKILL.md)
   and [detector](https://github.com/lis186/SourceAtlas/blob/e3c7d6cf92f9e477f328b20b9b1d8a107d3ffd87/scripts/atlas/detect-project.sh)
   also encode different scale thresholds. No calibrated probability or
   "75% understanding" measure was established by this assessment.
2. **Automatic cache reuse.** Overview returns an existing cache and ends analysis,
   with an age warning after 30 days; flow similarly reuses a name-based cache.
   Neither inspected cache branch validates source revision or relevant file
   changes. Loom must recheck applicability to the current question and conditions;
   recent modification time is insufficient.
3. **Existence equals correctness.** Fact-check checks references, not whether
   their content entails the claim; a file listed as scanned is not proof it was
   read. Flow's self-check is path existence plus method-name grep. These cannot
   solve unsupported recommendations or prove complete call-graph coverage.
4. **A universal source hierarchy.** Constitution Article IV ranks configuration
   and documentation above code. Applicable evidence depends on the claim: an
   installed dependency declaration does not establish execution or runtime success.
5. **Unqualified quality/benchmark transfer.** The [overview verification report](https://github.com/lis186/SourceAtlas/blob/e3c7d6cf92f9e477f328b20b9b1d8a107d3ffd87/dev-notes/2025-12/2025-12-21-overview-e2e-verification.md)
   checks five projects' configurations/structure. Its reported 93% score does
   not establish better engineering decisions, causality or performance in Loom.
   The inspected [CI workflow](https://github.com/lis186/SourceAtlas/blob/e3c7d6cf92f9e477f328b20b9b1d8a107d3ffd87/.github/workflows/verify.yml)
   runs frontmatter lint, not this fact-checker or a research-quality evaluation.

The AST helper also converts some execution errors into empty arrays
(`run_inline_rule`, lines 254–260). Any adapted helper must distinguish tool
failure from a valid search with zero matches.

## Evidence

Upstream links above are pinned source observations fetched through the GitHub
connector. The recursive tree was inspected to find the live plugin command
surfaces rather than assuming `.claude/commands` was the only implementation.
Connected wrappers, overview/flow commands, pattern/history workflows, scanner,
detector, selected AST/search implementations, fact checker, output template,
verification guide, manifest, CI and license were inspected. Large search helpers
were read in selected relevant sections, not exhaustively audited.

Local evidence consists of the linked historical reports and current
[main contract](../../../loom-code/skills/engineering-research/SKILL.md),
[methods](../../../loom-code/skills/engineering-research/references/research-methods.md),
[source policy](../../../loom-code/skills/engineering-research/references/source-policy.md)
and [evaluation guidance](../../../loom-code/skills/engineering-research/references/evaluation-selection.md).
The existing source policy already requires connected execution-path inspection;
the retained-record rules already require substantive readback and update consistency.

## Decision impact

**Recommend adapting the evidence-checking concept and making targeted repository
tracing easier to execute; do not integrate the whole SourceAtlas workflow.**

| Alternative | Historical gap coverage | Burden / decision |
|---|---|---|
| Keep current guidance / defer | Existing tracing/comparison rules remain available; demonstrated application gaps remain | Zero new maintenance; valid baseline |
| Add a short repository-investigation recipe only | Makes orientation and connected tracing concrete; little direct help for stale recommendations | Small; optional when unfamiliar-repo navigation is a demonstrated cost |
| Combine the small recipe with bounded evidence checks | Reference/count defects become reproducible; semantic checks still needed for recommendations and saved conclusions | Recommended trial candidate; no new mandatory station, store or installation |
| Integrate SourceAtlas as a required tool | Adds pattern/history capabilities, but does not establish a fix for observed recommendation/readback failures | Command/host/path assumptions, extra dependencies and duplicate record/cache rules; not justified now |

The smallest useful candidate would keep the existing Markdown research record.
For each decision-changing claim, retain the evidence location, evidence kind
(declaration/source observation/runtime result), applicability and unresolved
test. A helper could check paths/anchors and recomputable quantities within
authorized roots. Actual saved-content reading and a claim-to-evidence assessment
must still verify meaning, recommendation changes and final-record consistency.
This is a proposed adaptation, not a capability SourceAtlas's fact checker already has.

Before claiming improvement, compare unchanged guidance with that small candidate
on matched cases: a simple fact negative, a misleading README with a gated failure
path, a valid reference that does not support the claim, an obsolete cache, and
the nested ZIP recommendation plus follow-up challenge. Measure supported
decisions, updated saved conclusions, actual readback and operating cost separately.
Do not use activation rate, diagram count or valid links as research-quality proxies.

The recommendation would change if a bounded trial showed no improvement, excessive
overhead on simple questions, or a real target repository required specialist
AST/history support that existing tools could not supply adequately. Direct
SourceAtlas use can then be reconsidered for that bounded question.

## Limitations and open questions

- Static implementation assessment only; no SourceAtlas command, helper suite or
  host installation was exercised. Performance and cross-host portability remain unverified.
- Historical fixtures concern older skill revisions; they identify failure classes,
  not current failure rates. Current guidance includes later repairs.
- Reports were read as historical evidence; this was not a complete reread of all
  Codex/Claude sessions and does not isolate a model's internal cause.
- No new independent review or paid actor comparison was dispatched.
- SourceAtlas is MIT licensed; copied substantial code/text requires preserving
  its copyright/license notice. No upstream implementation was copied into runtime files.
