---
title: "Industry approaches to external research and repository investigation"
type: loom-research
status: concluded
created: 2026-11-14
updated: 2026-11-14
tags:
  - loom/research
---

# Industry approaches to external research and repository investigation

## Question and scope

Are there more capable tools or concepts for engineering-research, given that it
currently handles both external practice research and internal implementation investigation?
What division would fit Loom without unnecessary orchestration or dependencies?

This follows the [SourceAtlas assessment](2026-11-14-sourceatlas-engineering-research.md),
but broadens the question beyond that project's design. It is a separate assessment;
no runtime skill change, installation, paid experiment or publication is authorized
or performed. Local baseline is `3b1a9972644517911454530dc1876f88525b1f37`.
External documentation was inspected on 2026-11-14. Source snapshots are recorded below.

## Method and rationale

Use a purposive primary-source survey and lightweight trade study. Compare tools
by the evidence they provide, applicable task, maintenance/integration burden,
limitations and verification status. Search English and Japanese in the initial
discovery batch, then follow first-party documentation and selected upstream code.
Japanese queries supplied leads, not independent corroboration of English sources.
Do not rank products by popularity, feature count or unrelated vendor benchmarks.

Inspect implementation paths for the open-source examples used to support specific
mechanism claims. Proprietary services are documentation-level candidates, not
locally verified integrations. Stop after identifying distinct evidence capabilities,
current support boundaries and a proportionate Loom proposal. No tool installation,
API research task or actor comparison is needed to establish this conceptual boundary.

## Findings

### The user's distinction is real, but source location is not the best sole boundary

| Evidence question | Suitable method | What a successful answer establishes |
|---|---|---|
| What do other projects or practitioners recommend, and under which conditions? | External discovery, full-source reading, comparison and counterevidence | Attributed practices and applicable tradeoffs; not industry prevalence without representative evidence |
| What does this specific implementation do? | Text/structural/symbol search, connected source inspection, configuration and history | Source-supported behavior at an identified revision; not proof that it ran |
| Does it actually work in the target environment? | Bounded execution, reproduction, traces or representative measurement | Observed behavior for the tested input/environment; not universal correctness |

An upstream open-source repository is external to Loom but calls for the same
source-investigation methods as a local repository. Conversely, internal design
documents can contain unverified proposals. Therefore classify by the claim and
evidence needed, while separately recording location, authorization and revision.

The current [research contract](../../../loom-code/skills/engineering-research/SKILL.md)
already includes all three methods. Its [source policy](../../../loom-code/skills/engineering-research/references/source-policy.md)
already requires connected implementation inspection. The missing opportunity is
more concrete tool selection and evidence handling, not discovering that code and
web sources differ for the first time.

### External research: stronger retrieval and inspectable attribution

| Candidate / concept | Inspected capability | Fit and limitation |
|---|---|---|
| [Exa Deep Search](https://exa.ai/docs/search/deep-search) | Iterative search/refinement; structured results can associate each output field with citations in `output.grounding` | Useful candidate for broad external comparisons; inspect cited sources and conditions independently. Documentation only; no API execution or measured advantage over native browsing |
| [Tavily Research](https://docs.tavily.com/documentation/api-reference/endpoint/research) | Research task API exposes output schema, citation format and domain controls | Another hosted research candidate; not interchangeable with a local code analyzer. Documentation only, with no local pricing/quality comparison |
| [LangChain Deep Agents research guide](https://docs.langchain.com/oss/python/deepagents/deep-research) | Focused delegated tasks, isolated context and cited synthesis; its shown search implementation fetches full pages after URL discovery | Useful orchestration reference when independent questions exceed one context; a new runtime/provider/trace surface would be unnecessary for simple lookups |
| [Anthropic production account](https://www.anthropic.com/research/multi-agent-research-system) | Reports separate research and citation work, bounded delegation and substantial coordination/token costs | Supports selective parallel research as an architectural option, not universal superiority or a requirement to delegate every question |

The most relevant concept is claim-level attribution: retain which observation
supports which material conclusion, instead of attaching a general bibliography
to a synthesized answer. An API-produced citation/confidence value remains a
claim to inspect, not an independent proof. Existing host browsing remains a viable
baseline; these sources do not establish that purchasing another API improves Loom.

Current-version traps were checked. [Exa's current guide](https://exa.ai/docs/search/quickstart)
marks `deep-reasoning` as legacy and directs new work to `deep` or Agent. The
[Open Deep Research repository](https://github.com/langchain-ai/open_deep_research)
was confirmed `archived: true` through GitHub repository metadata. It remains an
inspectable historical example, not a default recommendation for a new dependency.

At `1b7d2e80db9faa586165c60e09096dbbfd483a64`, its
[researcher implementation](https://github.com/langchain-ai/open_deep_research/blob/1b7d2e80db9faa586165c60e09096dbbfd483a64/src/open_deep_research/deep_researcher.py#L225-L345)
dispatches bounded research calls, gathers results and retains raw notes. The
exception branch at lines 332–342 ends research on errors (`or True` broadens the
condition); successful report generation should not be interpreted as all research
branches succeeding. Do not copy an example's completion semantics uncritically.

### Repository investigation: precise navigation, compact context and targeted analysis

| Candidate / concept | Inspected capability | Fit and limitation |
|---|---|---|
| [Serena](https://oraios.github.io/serena/01-about/000_intro.html) | Symbol definitions/references through language-aware tooling; selected implementation traced below | Strong local candidate when identical names, large files or cross-file references make text search ambiguous. Language backend/setup quality matters; symbol references do not prove runtime reachability |
| [Sourcegraph Deep Search](https://sourcegraph.com/docs/deep-search) | Agent uses code search/navigation and reports searches/files consulted; documented sandbox aggregation can compute inventories | Candidate for multiple repositories and large inventories. Product-plan and indexing burden apply; no instance was deployed or tested |
| [Sourcegraph precise navigation](https://sourcegraph.com/docs/code-navigation/precise-code-navigation) | Language-specific SCIP indexes supply definition/reference navigation; search-based navigation is a fallback | Structural identity is stronger than matching text for supported indexed symbols. Requires applicable indexes; query revision, coverage and freshness remain important |
| [Aider repository map](https://aider.chat/docs/repomap.html) | Compact definitions/signatures, selected through dependency-graph ranking within a token budget | Useful orientation concept beyond filename sampling. A map helps choose what to read; it is not evidence for omitted behavior. Documentation-level assessment |
| [CodeQL data-flow analysis](https://codeql.github.com/docs/writing-codeql-queries/about-data-flow-analysis/) | Queryable local/global propagation and taint models, with documented modeling/computation limits | Relevant for a specific security or propagation question. Too much setup for ordinary project orientation; static paths are not observed execution |

Serena source at `6e5c3776d4e67befaab7c290bc29b0279c98d1ed` was traced from
[FindReferencingSymbolsTool](https://github.com/oraios/serena/blob/6e5c3776d4e67befaab7c290bc29b0279c98d1ed/src/serena/tools/symbol_tools.py#L158-L194)
through [LspApi](https://github.com/oraios/serena/blob/6e5c3776d4e67befaab7c290bc29b0279c98d1ed/src/serena/repl/api/lsp_api.py#L537-L576)
to the [symbol retriever](https://github.com/oraios/serena/blob/6e5c3776d4e67befaab7c290bc29b0279c98d1ed/src/serena/symbol.py#L812-L880),
which resolves a symbol and calls the language server's reference operation with
its file/line/column. This verifies a language-aware query path, not complete
language coverage, successful installation or all dynamic references.

For Loom specifically, Markdown contracts, shell hooks, manifests and generated
files matter alongside Python. Symbol tooling must be combined with ordinary text,
configuration and command-dispatch inspection; a Python-only graph would miss
important relationships. Existing `rg`, Git and bounded tests remain the default
until an actual navigation failure justifies an additional tool.

### Documentation-to-implementation applicability is a separate responsibility

[Context7](https://context7.com/docs/overview) supplies version-specific library
documentation. Its current [research preview](https://context7.com/docs/howto/research-preview)
adds source lookup and upgrade guidance; preview is off by default and may change.
Source lookup is available for eligible Git-backed libraries, not every website
documentation entry. This is a relevant attempt to connect documentation and
the source revision it describes, rather than treating all external evidence as web prose.

At Context7 `5c4a4b43cd5010f5678c6fceac3dd16865112e67`, the
[server](https://github.com/upstash/context7/blob/5c4a4b43cd5010f5678c6fceac3dd16865112e67/packages/mcp/src/index.ts#L402-L468)
registers documentation lookup and conditionally registers preview tools.
[Preview registration](https://github.com/upstash/context7/blob/5c4a4b43cd5010f5678c6fceac3dd16865112e67/packages/mcp/src/lib/research-preview-tools.ts)
connects to [query-code](https://github.com/upstash/context7/blob/5c4a4b43cd5010f5678c6fceac3dd16865112e67/packages/mcp/src/lib/query-code-tool.ts#L89-L178),
whose versioned request goes through
[fetchLibraryCode](https://github.com/upstash/context7/blob/5c4a4b43cd5010f5678c6fceac3dd16865112e67/packages/mcp/src/lib/api.ts#L303-L365)
to `/v2/code`. The client transmits library/version/operation parameters; server-side
index correctness, account eligibility and query quality were not verified here.
The preview also registers outbound documentation feedback, so it should not be
treated as a purely read-only addition when considering future integration.

No upstream tool establishes that the target project has installed that version,
enabled the feature, selected the same implementation or successfully exercised
it. The owning researcher must connect external support to the actual lockfile,
configuration, call path and, where necessary, observed execution. This can be a
small table in the existing record, not another database or compulsory document.

### Evaluate support, coverage and evidence freshness separately

The [ALCE paper abstract](https://arxiv.org/abs/2305.14627) distinguishes answer
correctness and citation quality. Only the abstract was inspected here; this study
does not claim to reproduce its metrics or transfer its historical error rates
to modern tools. For Loom, derive concrete checks from the actual failure modes:

| Evaluation target | Useful check | Inadequate proxy |
|---|---|---|
| External claim support | Does the actual cited passage support the bounded claim under the stated conditions? | URL exists; report includes citations |
| Repository evidence | Does the identified definition/configuration/path support the claim at the inspected revision? | Symbol name appears; graph looks complete |
| Runtime statement | Is there an actual receipt/output for the tested input and environment? | Tests exist; code appears executable |
| Recommendation maintenance | Does a changed recommendation have new support, and does the retained conclusion match? | Agent agreed with a follow-up challenge |
| Proportionality | Same questions, supported decisions, time/tool/context costs and simple-question controls | More sources, agents or retrieved chunks |

The [ZIP diagnosis](2026-11-12-recommendation-evidence-gap.md) and
[code-owned dogfood](../../skill-dogfood/2026-11-08-code-owned-engineering-research/report.md)
already demonstrate why retrieval and record-verification failures must be measured
separately. The current [framework comparison](../../skill-dogfood/2026-11-08-engineering-research-frameworks/report.md)
does not establish that more research instructions improve outcomes.

## Decision impact

**Recommended trial shape: retain one engineering-research entry, use separate
question-selected methods for external evidence, repository evidence and execution,
and share a small claim/evidence/applicability/unknown record.** This is an
agent-proposed direction, not a ratified specification or demonstrated improvement.

Follow-up clarification: the user confirmed the single-entry preference. The
[question-classification study](2026-11-14-engineering-research-question-taxonomy.md)
clarifies that the three activities above are not an exhaustive question taxonomy:
choose evidence methods by the question's purpose, including diagnosis, selection,
feasibility, impact/risk, measurement, causal effect and conformance checks. This
refines the classification without claiming a new implementation or trial result.

| Alternative | Capability / historical-fit benefit | Cost and decision |
|---|---|---|
| Keep current skill unchanged / defer | Existing general rules already cover all evidence types | Zero added maintenance; retain as the comparison baseline |
| One entry with small specialized methods and optional tools | Preserves mixed-question handling while making evidence/tool selection concrete | Recommended first experiment; avoid new station, service or mandatory index |
| Split external research and code investigation into independent skills | More specialized descriptions, tools and prompts | Potential routing overlap, duplicate evidence policy and handoff loss; justify with measured selection/context problems first |
| Combine a hosted research API with local symbol tooling | Stronger external discovery and code navigation where each is needed | Candidate only after task-specific trials; two dependencies do not automatically improve decision quality |
| Always use multi-agent research plus a persistent code/knowledge graph | Supports some broad or cross-repository workloads | Not justified for present evidence; coordination, index maintenance, freshness and operating costs are real |

For a first tool shortlist, consider Context7 for versioned dependency questions,
Serena for demonstrated symbol-navigation problems, and Exa/Tavily as competing
external retrieval/research candidates. Sourcegraph fits a concrete multi-repository
need; CodeQL fits a concrete data-flow/security need. This is task-fit guidance,
not a procurement ranking. No evidence currently chooses Exa over Tavily or either
over the host's existing search for the user's workload.

A bounded follow-up could compare unchanged guidance with the small method split
on an external-practice comparison, a misleading documentation/source mismatch,
duplicate symbol names, a feature disabled by local configuration, a missing runtime
receipt and the ZIP follow-up reversal. Hold model, inputs and allowed tools constant
when testing instruction effects; evaluate added tools separately so tool effects
are not confused with wording effects. A mandatory graph or delegation step should
fail the simple-question overhead control unless its value is demonstrated.

## Evidence and verification status

Primary sources above were opened or fetched; upstream source links are pinned.
GitHub repository metadata confirmed Open Deep Research archived and Serena/Context7
not archived at inspection. Selected source paths were traced, not whole projects
audited. No private project/session material was sent to external searches.

Documented product support and previews may change. No subscription, API credential,
pricing comparison, installed host support, native-tool overlap benchmark or local
performance was verified. Search snippets and vendor percentages were not treated
as tool-selection evidence. The obsolete Exa documentation URL failed and was replaced
with current first-party documentation; no unsupported deprecation date is asserted.

This is a bounded survey of relevant approaches, not a representative industry
adoption study, universal state-of-the-art ranking or proof that splitting a skill
will improve execution. Full current-session history was not reread; prior local
reports supply bounded historical evidence. Runtime skills and the earlier research
record remain unchanged.
