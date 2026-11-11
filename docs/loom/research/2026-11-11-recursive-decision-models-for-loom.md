---
title: "Applying recursive decision model ideas to Loom"
type: loom-research
status: concluded
created: 2026-11-11
updated: 2026-11-11
tags:
  - loom/research
---

# Applying recursive decision model ideas to Loom

## Question and scope

Can Loom benefit from Raymond Weitekamp's proposal to reserve generation for work that needs it, while bounded decisions use classifiers and executable control logic?

Assessment of checkout `91ee36100708f73af5d1df33107dbf98b91ac44f`, loom-code 3.65.0, on 2026-11-11. The worktree was initially clean. This is standalone research, not an implementation, installation, release, or authorization to introduce a hosted model. This document is the only intentional repository change.

Starting material: the user-provided summary titled `2026-11-11 Your Agent Doesnt Need an LLM for Every Decision Raymond Weitekamp OpenProse`, associated with [the AI Engineer video](https://www.youtube.com/watch?v=hFNbPmzzcEs). Its metadata identifies automatic subtitles and an LLM-generated summary. The video could not be fetched in this run; this assessment does not claim transcript-level verification. The private source location is intentionally not published.

## Method and rationale

Use local implementation inspection, two bounded existing test modules, primary-source documentation, and a qualitative trade study. Criteria: preserve authorization and verification, avoid duplicating policy, reduce actual orchestration work, maintain host portability, and justify dependency/operational cost. Search began with English and Japanese queries; accepted external evidence below is primary material. No private repository contents were sent to an external model or search service.

Stop when architectural fit and a bounded next experiment are supported. No performance comparison is possible without representative Loom traces and a candidate implementation. Do not infer savings from game or audio demonstrations.

## Findings

### Distinguish three mechanisms

| Mechanism | Appropriate input and output | Limit |
|---|---|---|
| Fixed code rules | Observed fields, paths and hashes produce allowed outcomes | Correct policy execution does not establish the truth of model-supplied fields |
| Decision model | Unstructured input produces a label, score or option probabilities | Bounded output can still be semantically wrong |
| Generative model | Produces code, explanations, hypotheses and new plans | More flexible; needs verification and bounded authority |

The author's RDM proposal concerns external context, recursive composition and optional generation, not merely replacing all model calls with if-statements. His published DSPy examples were inspected: `RDM.forward` predicts, conditionally calls registered tools below a depth limit, and returns observations. The outline example stores content outside the model and exposes selected headings. These are illustrative source examples, not an executed library evaluation. The author explicitly calls the first recursive handbook search a poor practical solution; recursion alone is not evidence of efficiency. [Author article](https://raw.works/recursive-decision-models/).

Jev's documented API returns typed judgments. Its `confidence` summarizes the answer distribution and is distinct from empirical correctness on Loom tasks. A threshold requires local evaluation; high confidence must never substitute for user authorization. [Introduction](https://docs.typesafe.ai/introduction), [confidence definition](https://docs.typesafe.ai/confidence).

### Existing Loom already implements part of the idea

| Surface inspected | Observed behavior | Incremental implication |
|---|---|---|
| [Dispatch resolver](../../../loom-code/scripts/dispatch_profile.py), `_classify`, `_initial`, `_after_execution`; [caller contract](../../../loom-code/references/dispatch-profile.md) | Typed task evidence selects portable model/effort; failure feedback and capability constraints govern retries/fallback | Reuse this oracle. Replacing it with a classifier would add uncertainty to an already mechanical operation |
| [Intake command](../../../loom-code/scripts/loom_checker/command_handlers/intake.py), `cmd_intake` | Reads manifest/artifacts and recomputes prerequisites for write-spec/write-plan | Expose its factual blockers rather than ask an LLM to recreate them; this is not a complete all-station scheduler |
| [Delivery observer](../../../loom-code/scripts/loom_checker/command_handlers/publish.py), `observe_delivery` | Produces state, reason, next action and evidence; checks committed intent, scoped dirty files and external delivery identity | The proposed structured status interface already exists for delivery; extend only after finding a real uncovered decision |
| [Reviewer floor](../../../loom-code/scripts/loom_checker/reviewers.py), `reviewer_floor_for_paths` | Positive allowlist for narrow deltas; otherwise retains two-reviewer floor | Do not let probabilistic routing waive required review |
| [Manifest](../../../loom-code/contract/manifest.yaml) and [session-start](../../../loom-code/hooks/session-start) | Station/decision-point names derive from shared contract, then enter model context as guidance | Externalized policy exists, but injected prose is not an autonomous execution controller |
| [Skill router](../../../loom-code/skills/using-loom-code/SKILL.md) | Agent selects a skill using request meaning and existing artifacts | A possible advisory classifier experiment, provided mixed requests and uncertainty retain generative judgment |

The dispatch input boundary matters: the caller supplies predicates such as `trust_boundary`, `inconsistent_evidence`, and whether work met acceptance. Code deterministically processing those fields does not prove they were accurately observed. Likewise, a passing checker cannot establish every semantic product obligation.

The host owns the surrounding agent loop. A plugin adding a classifier tool may add a model call without removing any parent-model turn. Actual orchestration savings require a verified host hook/adapter or an execution path that bypasses the redundant parent decision. Current [OpenCode](../../../loom-code/references/opencode-tools.md) and [Antigravity](../../../loom-code/references/antigravity-tools.md) reference contracts already describe limits on applying model-and-effort overrides. These are repository-documented constraints, not fresh runtime measurements of those hosts.

### Best and worst transfer candidates

| Candidate | Assessment | Why |
|---|---|---|
| Consolidated read-only status/eligible-action output using existing checker functions | Best first candidate, conditional on measured duplication | Finite states, inspectable evidence, no new inference service; avoid a second policy source |
| Select relevant references by explicit station/artifact metadata | Worth a bounded experiment | Can reduce irrelevant context, but mandatory contracts must remain available; retrieval misses need fallback |
| Classify ambiguous natural-language requests or findings | Optional later experiment | Semantic work that cannot simply be replaced by file checks; needs multilingual/mixed-intent evaluation |
| Replace substantive review, acceptance, root-cause analysis, or authorization | Not recommended | Finite verdict labels do not make the reasoning behind them mechanical |
| Recursive classifier hierarchy across seven stations | No present justification | Small action space; branching can multiply calls and an early false negative can exclude the correct branch |
| Speculative parallel writes and automatic policy learning | Not recommended for initial adoption | Require stale-state rejection, isolation, conflict handling and explicit authority, not just model confidence |

The video's arbitrator idea transfers as a separation between proposing and executing actions. Loom's checker/publication paths are useful foundations, but this is not proof of universal interception: hook configurations contain availability fail-open paths, and host enforcement differs. A future executor should recheck relevant state/content and authority at execution time; merely adding a classifier does not establish this property. [Hook configuration](../../../loom-code/hooks/hooks-codex.json), [publication implementation](../../../loom-code/scripts/loom_checker/command_handlers/publish.py).

## Evidence and verification

- `python3 -m pytest -q loom-code/tests/test_dispatch_profile_resolver.py`: **153 passed in 0.26s**. Tests exercise resolver rules and fallback behavior, not real model accuracy or every host adapter.
- `python3 -m pytest -q loom-code/tests/test_delivery.py`: **9 passed in 5.53s**. Tests use controlled Git fixtures and mocked external calls; they do not prove actual GitHub publication or host termination enforcement.
- Installed launcher: `/Users/kouko/.codex/plugins/cache/loom/loom-code/3.65.0/scripts/loom-python --ready delivery --json`: exit 1, `state: unconfirmed`, reason `cannot identify a committed change`. This standalone research has no committed change intent; no software-delivery claim is made.
- [Anthropic's workflow/agent distinction](https://www.anthropic.com/research/building-effective-agents) supports separating predefined control from dynamic work. It is architectural guidance originally published in 2024, not a current Loom benchmark.
- [Pydantic AI decision-model documentation](https://pydantic.dev/docs/ai/models/decision/) documents classification with fallback to a language model when generation or uncertain choices require it. Documentation-only evidence: no Pydantic runtime or implementation was tested here, and adopting its framework is not necessary for the recommendation.
- The author's Rust RDM package, hosted Jev service and demonstrations were not installed or executed. No claim about their production suitability, license compatibility, local hardware support, exact price or Loom latency is established.

## Decision impact

| Option | User-visible consequence | Assessment |
|---|---|---|
| Keep current behavior and measure first | No new dependency or workflow change | Valid when repeated orchestration cost is not yet demonstrated |
| Smaller deterministic improvement using existing checker outputs | Agent receives current blockers and permitted next actions with evidence | Recommended first experiment; actual benefit remains unmeasured |
| Combine fixed controls with an advisory decision model | Faster classification may be possible; uncertain cases retain existing judgment | Consider only after an offline comparison shows incremental value |
| Replace the controller with a general recursive decision runtime | Larger integration and maintenance surface across hosts | Not justified by present evidence |

For a subsequent authorized experiment, choose one recurring, read-only decision and compare the current path against reuse of existing deterministic outputs. Only then add a classifier arm if the decision genuinely needs semantics. Reuse the manifest/checker functions instead of copying their rules. Suggested output fields are observed state, eligible actions, blocking reasons, evidence paths/content identity and unresolved facts; these are a proposal, not an existing universal API.

Evaluation should separate request interpretation, legal-action selection and execution. Use held-out English/Japanese/Traditional Chinese cases, ambiguous mixed requests, missing/stale artifacts, unavailable host capabilities and interrupted work. Measure incorrect routes, missed mandatory checks, fallback frequency, total parent-model turns, tokens/cost and end-to-end latency including fallback. Include adversarial instructions in analyzed content. Preserve required user decisions, substantive independent review and acceptance testing.

Adopt only if correctness and authority boundaries remain intact and the measured benefit exceeds implementation and operating cost. Zero observed boundary violations in a finite test set is a release criterion, not a mathematical guarantee. No numeric confidence threshold or savings percentage is justified yet.

## Limitations and open questions

No representative trace dataset, classifier benchmark, cross-host end-to-end run, new scheduler prototype, independent reviewer assessment, or complete package suite was performed. This is an architectural feasibility assessment with focused local tests. It cannot establish that orchestration is Loom's dominant cost; code generation, review or tests may dominate instead. The practical conclusion is to apply bounded decisions and external evidence selectively, while preserving semantic judgment and authority checks.
