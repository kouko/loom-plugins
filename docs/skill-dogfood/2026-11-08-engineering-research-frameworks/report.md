# Dogfood report — engineering evaluation selection

## Result

The revision-5 prototype selected proportionate approaches for the six sampled
questions. Its selection reference was actually read in all five evaluation
cases and omitted for the simple fact case. Two independent auditors supported
the substantive method/domain outcomes for all twelve old/new executions.
The revision-4 comparator achieved the same main outcomes: this run does not
establish an incremental quality benefit from the added selection rules.

Native discovery selected the target in 40/40 positive trials and did not select
it in 10/10 negatives. Description text did not change. A procedural reading-order
observation remains in both versions; do not collapse that into a global PASS.

## Metadata

| Field | Value |
|---|---|
| Date | 2026-11-08 |
| Target | Uninstalled revision 5, `input/new/engineering-research/` |
| Comparator | Frozen revision 4, `input/old/engineering-research/` |
| Model request | gpt-6.1-sol / first-party OpenAI / medium for native actors and independent auditors |
| Immutable backend revision | Not independently returned or verified; fixed request name does not prove immutable weights |
| Activation | Native Codex raw-skill discovery, actual body reads, 20 positives + 5 negatives repeated twice |
| Explicit execution | Six genuine-source cases, old/new once each, twelve fresh actors in one randomized masked batch; baseline launched before/with candidate |
| Independent review | Two fresh auditors, twelve actors and nine criteria each; raw per-criterion judgments retained |
| Installation | None; no production plugin, release, commit or merge changed |

[Protocol](protocol.md) · [authorization](authorization.json) ·
[environment](environment.json) · [frozen inputs](input-hashes.json) ·
[recomputed integrity checks](verification.json).

## Prototype changes under test

The [revision-5 main instruction](../../loom/2026-11-07-engineering-research-trial/revision-5-framework-selection/candidate/engineering-research/SKILL.md)
adds a conditional link to [evaluation selection](../../loom/2026-11-07-engineering-research-trial/revision-5-framework-selection/candidate/engineering-research/references/evaluation-selection.md).
The template adds fit/criteria, tradeoff and recommendation-condition prompts.
The description, five checks, previous method/source rules and optional graph
policy are preserved. The [research proposal](../../loom/research/2026-11-08-engineering-evaluation-framework-selection.md)
remains a development record, not a runtime dependency.

This is a one-off prototype with documented criteria, using the quick development
evaluation path plus the three dogfood probes. Old/new same-case runs are retained;
no unsupported 15-percent improvement gate or automatic-fix loop was imposed.

## Same-case substantive results

Arm mapping was withheld until both independent audits were complete. Auditors
saw each actual raw contract, so richer content could still suggest a version;
masking hid preferred-version labels, not all possible content-based inference.

| Case | Revision 4 | Revision 5 | Main evidence-supported outcome |
|---|---|---|---|
| C01 — Exact TEST_ROOTS fact | [X009](execution/X009/answer.txt) | [X008](execution/X008/answer.txt) | Both: correct four roots; short note; no experiment, diagram or matrix. New selection reference not loaded. |
| C02 — Preview commands: reuse versus rewrite, bounded probe | [X001](execution/X001/answer.txt) | [X004](execution/X004/answer.txt) | Both: reuse the real command builder with conditions; one allowed construction-only probe; no returned suite commands executed. |
| C03 — Foreign-code trust + unavailable-Git resilience | [X005](execution/X005/answer.txt) | [X003](execution/X003/answer.txt) | Both: separate trust and dependency-failure questions into linked records; preserve fail-open and unverified isolation boundaries. |
| C04 — Confounded prior timing/token observations | [X012](execution/X012/answer.txt) | [X011](execution/X011/answer.txt) | Both: retain real receipts, reject quality/cost/causal superiority from unmatched work; propose a bounded matched comparison. |
| C05 — Markdown migration and evidence traceability | [X006](execution/X006/answer.txt) | [X007](execution/X007/answer.txt) | Both: calculate changed relative paths, preserve provenance, adapt migration to Markdown; no actual migration or database workflow. |
| C06 — Unsupported full-CI/release approval | [X010](execution/X010/answer.txt) | [X002](execution/X002/answer.txt) | Both: source/test definitions do not prove full current-HEAD CI success or authorize release. |

Both reviewers found no substantiated material functional defect. Auditor 1
recorded 104 supported and four not-applicable judgments. Auditor 2 supported
all substantive method/domain criteria while recording R9 ordering observations
separately. This is not unanimous procedural compliance or proof of equivalence
outside these tasks.

The simple fact notes contained 199 words (old) and 208 words (new), including
metadata/headings. The new extra reference was not read for that case. Both
mixed-risk actors produced two records for independently answerable questions.
No actor generated a Mermaid block in this round, so no new rendering claim is
made. The previous round's render evidence is not relabeled as this run's result.

## Severity summary and advisory observations

| Classification | Count | Interpretation |
|---|---|---|
| Critical / High / Medium substantive findings | 0 | No substantiated defect in completed scope |
| Low advisory workflow observation | 1 theme | Literal resource-read ordering differs in six actors across both revisions; no demonstrated decision harm |
| Uncertain boundary cases | 2 actors | Provenance orientation before reference loading may be allowed by premise checking |
| Informational readability suggestion | 1 | Optional acronym expansion; not a practical blocker |

### OBS-001 — Source evidence sometimes precedes the required reference reads

- **Severity / category / pass:** Low advisory / Workflow-drift / informed;
  confirmed command order, disputed procedural classification, no demonstrated
  functional harm.
- **Probe prompts:** C01, C02, C04 and C05 in [frozen cases](execution/cases.json).
- **Expected:** The shared main contract says, “Before gathering evidence, read
  [research methods] and [source policy]”. Step 1 also asks for premise/context
  verification against available artifacts.
- **Actual:** Six actors read substantive tests/source, timing receipts or a
  migration excerpt first, and later read the method/source references. After
  unblinding: old X001/X009/X012 and new X007/X008/X011. The two provenance-only
  cases X002/X003 remain uncertain rather than confirmed substantive violations.
- **Transcript evidence:** [X001 events](execution/X001/events.jsonl), item at
  line 12 reads `nl -ba src/tests/test_run_package_tests.py`; line 13 loads the
  required references. [X008 events](execution/X008/events.jsonl), line 7 reads
  the full runner alongside SKILL/provenance; line 10 loads the references.
  Exact commands and all eight dispositions appear under R9 in
  [auditor 2 structured judgments](audits/audit-2.json).
- **Root cause:** The literal before-evidence wording is clear for substantive
  reads, but the boundary between prerequisite premise orientation and evidence
  gathering is not fully explicit. Causal impact of order is not established.
- **Reviewer difference:** Auditor 1 acknowledges ordering as a limitation and
  supports R9's overall outcome; auditor 2 uses six partial/two uncertain R9
  votes. Both support the substantive results. Preserve the disagreement.
- **Why structural checks miss it:** Required files and correct final notes do
  not establish when resources were read.
- **Location:** Both packages' `SKILL.md`, numbered step 1 and “Research method
  and source selection”; this clause predates revision 5.
- **Suggested fix direction:** In a later revision, clarify permitted initial
  orientation versus substantive evidence reads, or make the intended early
  reference-loading point explicit. No target was edited after this finding.
- **Repro:** Repeat the frozen prompts using the isolated execution harness;
  inspect actual command order, not just final answers.

### INFO-001 — Optional method-acronym expansion

The cold reader could execute the bounded procedure and interpret simple/mixed
questions without author clarification, but suggested expanding ATAM on first
use. The row already gives an actionable scenario recipe. This is an
informational accessibility suggestion, not a confirmed procedural failure.
See [raw questions, interpretations and file receipt](cold-reader/probe-c-framework-reading.md).
The earlier routine-lookup/stage-boundary observations have not been marked
resolved; the description was unchanged and this round does not settle them.

## Raw outputs appendix

### A. Activation

[Corpus](activation/corpus.json) · [predeclared ambiguity/design](activation/design.md)
· [summary](activation/summary.json) · [findings and limits](activation/findings.md)
· [activation integrity](activation/verification.json).

All 50 runs were fresh, valid and timeout-free, with real target-body output
rather than self-reported selection. Excluding predeclared ambiguous P10/P18/P20
still gives 34/34 positives and 10/10 negatives. No labels were changed from
observed outputs. The designer accidentally saw the previous runner's embedded
corpus; new queries differed and no target body was read by the designer. Actors
remained blind. This is a designer-familiarity limitation, not eliminated bias.
No project fixture was provided for routing; missing evidence remained missing.
Native catalogs and filtered events are retained beside each answer. Codex raw
skill reads are not Claude Skill() events, installed-plugin behavior or full
Loom-hook parity. The unchanged description precludes a trigger-improvement
claim from a body-only change.

| Case | Query | Should select target | Run 1 | Run 2 |
|---|---|---|---|---|
| P01 | We are drafting the intent for offline sign-in. Whether the chosen identity SDK supports token refresh without a network could overturn the design. Establish what evidence we need before committing. | yes | [receipt](activation/runs/P01-r1/receipt.json) / [answer](activation/runs/P01-r1/answer.txt) | [receipt](activation/runs/P01-r2/receipt.json) / [answer](activation/runs/P01-r2/answer.txt) |
| P02 | Our spec assumes Python 3.13 can load this native extension. The vendor support table is missing. Investigate compatibility before we approve that runtime. | yes | [receipt](activation/runs/P02-r1/receipt.json) / [answer](activation/runs/P02-r1/answer.txt) | [receipt](activation/runs/P02-r2/receipt.json) / [answer](activation/runs/P02-r2/answer.txt) |
| P03 | The implementation plan relies on a browser API working in Safari. We have only seen Chrome behavior; resolve that uncertainty before scheduling work. | yes | [receipt](activation/runs/P03-r1/receipt.json) / [answer](activation/runs/P03-r1/answer.txt) | [receipt](activation/runs/P03-r2/receipt.json) / [answer](activation/runs/P03-r2/answer.txt) |
| P04 | Build keeps failing at the same cross-compilation step. Before we attempt another fix, investigate whether our dependency even supports the target architecture. | yes | [receipt](activation/runs/P04-r1/receipt.json) / [answer](activation/runs/P04-r1/answer.txt) | [receipt](activation/runs/P04-r2/receipt.json) / [answer](activation/runs/P04-r2/answer.txt) |
| P05 | Two sources disagree about whether the database driver retries non-idempotent writes. That changes the data-loss risk in our proposed design. Resolve the conflict. | yes | [receipt](activation/runs/P05-r1/receipt.json) / [answer](activation/runs/P05-r1/answer.txt) | [receipt](activation/runs/P05-r2/receipt.json) / [answer](activation/runs/P05-r2/answer.txt) |
| P06 | Loom intent 還沒確認：我們假設套件可在沒有 Node 的使用者環境載入。請查證這個前提，因為不成立就得換方案。 | yes | [receipt](activation/runs/P06-r1/receipt.json) / [answer](activation/runs/P06-r1/answer.txt) | [receipt](activation/runs/P06-r2/receipt.json) / [answer](activation/runs/P06-r2/answer.txt) |
| P07 | 正在寫 spec。舊文件說 webhook 保證順序，新文件只保證至少一次，這會改變去重設計，先解開矛盾。 | yes | [receipt](activation/runs/P07-r1/receipt.json) / [answer](activation/runs/P07-r1/answer.txt) | [receipt](activation/runs/P07-r2/receipt.json) / [answer](activation/runs/P07-r2/answer.txt) |
| P08 | 規劃資料庫升級前，請確認目前版號能不能直接升到目標版；不支援就要安排中繼升級。 | yes | [receipt](activation/runs/P08-r1/receipt.json) / [answer](activation/runs/P08-r1/answer.txt) | [receipt](activation/runs/P08-r2/receipt.json) / [answer](activation/runs/P08-r2/answer.txt) |
| P09 | build 已在權限設定上失敗好幾輪；先研究 macOS sandbox 是否容許這項操作，再決定怎麼修。 | yes | [receipt](activation/runs/P09-r1/receipt.json) / [answer](activation/runs/P09-r1/answer.txt) | [receipt](activation/runs/P09-r2/receipt.json) / [answer](activation/runs/P09-r2/answer.txt) |
| P10 | 這個儲存方案是否可行，取決於服務端能不能做原子條件寫入。現在沒有可靠證據，請先調查。 | yes | [receipt](activation/runs/P10-r1/receipt.json) / [answer](activation/runs/P10-r1/answer.txt) | [receipt](activation/runs/P10-r2/receipt.json) / [answer](activation/runs/P10-r2/answer.txt) |
| P11 | Loom の intent を詰めています。選定 SDK のライセンスが再配布を許すか不明で、採用可否が変わります。根拠を確認してください。 | yes | [receipt](activation/runs/P11-r1/receipt.json) / [answer](activation/runs/P11-r1/answer.txt) | [receipt](activation/runs/P11-r2/receipt.json) / [answer](activation/runs/P11-r2/answer.txt) |
| P12 | spec の前提である HTTP クライアントのプロキシ対応が現行版にもあるか、確かな資料で確認してから設計を進めたいです。 | yes | [receipt](activation/runs/P12-r1/receipt.json) / [answer](activation/runs/P12-r1/answer.txt) | [receipt](activation/runs/P12-r2/receipt.json) / [answer](activation/runs/P12-r2/answer.txt) |
| P13 | 計画に入る前に、このキャッシュが複数プロセスで安全に使えるか確認したいです。仕様の説明が食い違い、方式の選択に影響します。 | yes | [receipt](activation/runs/P13-r1/receipt.json) / [answer](activation/runs/P13-r1/answer.txt) | [receipt](activation/runs/P13-r2/receipt.json) / [answer](activation/runs/P13-r2/answer.txt) |
| P14 | ビルド中、同じ ABI エラーが続きます。対応バージョンの組合せそのものが間違っていないか調べてください。 | yes | [receipt](activation/runs/P14-r1/receipt.json) / [answer](activation/runs/P14-r1/answer.txt) | [receipt](activation/runs/P14-r2/receipt.json) / [answer](activation/runs/P14-r2/answer.txt) |
| P15 | The intent compares local versus hosted parsing. We have no measured latency under the deployment constraints; determine what evidence would justify either choice. | yes | [receipt](activation/runs/P15-r1/receipt.json) / [answer](activation/runs/P15-r1/answer.txt) | [receipt](activation/runs/P15-r2/receipt.json) / [answer](activation/runs/P15-r2/answer.txt) |
| P16 | A benchmark claims the new dependency is faster, but it used different hardware. Before changing our plan, assess whether that evidence supports the migration decision. | yes | [receipt](activation/runs/P16-r1/receipt.json) / [answer](activation/runs/P16-r1/answer.txt) | [receipt](activation/runs/P16-r2/receipt.json) / [answer](activation/runs/P16-r2/answer.txt) |
| P17 | Our design depends on the current API retaining deleted records for thirty days. Verify that capability and identify what remains unknown before we lock the spec. | yes | [receipt](activation/runs/P17-r1/receipt.json) / [answer](activation/runs/P17-r1/answer.txt) | [receipt](activation/runs/P17-r2/receipt.json) / [answer](activation/runs/P17-r2/answer.txt) |
| P18 | We are deciding whether to migrate authentication providers. Check whether the required passkey flow exists at the versions we can deploy; do not implement the migration. | yes | [receipt](activation/runs/P18-r1/receipt.json) / [answer](activation/runs/P18-r1/answer.txt) | [receipt](activation/runs/P18-r2/receipt.json) / [answer](activation/runs/P18-r2/answer.txt) |
| P19 | One test says the plugin loader handles ESM, another says it only accepts CommonJS. Build is blocked until we resolve which claim applies to our supported host. | yes | [receipt](activation/runs/P19-r1/receipt.json) / [answer](activation/runs/P19-r1/answer.txt) | [receipt](activation/runs/P19-r2/receipt.json) / [answer](activation/runs/P19-r2/answer.txt) |
| P20 | Repeated attempts to enable streaming have failed. Before another retry, establish whether our account tier and API version support it at all. | yes | [receipt](activation/runs/P20-r1/receipt.json) / [answer](activation/runs/P20-r1/answer.txt) | [receipt](activation/runs/P20-r2/receipt.json) / [answer](activation/runs/P20-r2/answer.txt) |
| N01 | Critique the value and complexity of adding a dashboard export button. Technical feasibility is settled; focus on whether this product idea earns its maintenance cost. | no | [receipt](activation/runs/N01-r1/receipt.json) / [answer](activation/runs/N01-r1/answer.txt) | [receipt](activation/runs/N01-r2/receipt.json) / [answer](activation/runs/N01-r2/answer.txt) |
| N02 | Get an independent coding-agent opinion on our architecture trade-off. The evidence is collected already; I want a second reviewer, not another investigation. | no | [receipt](activation/runs/N02-r1/receipt.json) / [answer](activation/runs/N02-r1/answer.txt) | [receipt](activation/runs/N02-r2/receipt.json) / [answer](activation/runs/N02-r2/answer.txt) |
| N03 | Review this development session for process improvements: we skipped the kickoff, implemented the agreed tiny change, and ran tests late. No technical issue remains open. | no | [receipt](activation/runs/N03-r1/receipt.json) / [answer](activation/runs/N03-r1/answer.txt) | [receipt](activation/runs/N03-r2/receipt.json) / [answer](activation/runs/N03-r2/answer.txt) |
| N04 | The intent and feasibility are approved. Turn the agreed addition of a keyboard shortcut into implementation tasks with acceptance checks. | no | [receipt](activation/runs/N04-r1/receipt.json) / [answer](activation/runs/N04-r1/answer.txt) | [receipt](activation/runs/N04-r2/receipt.json) / [answer](activation/runs/N04-r2/answer.txt) |
| N05 | I want an undo button for deleted drafts. Help capture the user problem, intended outcome and acceptance criteria; there is no known engineering uncertainty yet. | no | [receipt](activation/runs/N05-r1/receipt.json) / [answer](activation/runs/N05-r1/answer.txt) | [receipt](activation/runs/N05-r2/receipt.json) / [answer](activation/runs/N05-r2/answer.txt) |

### B. Cold reader

[Complete raw response and files-read receipt](cold-reader/probe-c-framework-reading.md).
This is one fresh reading assessment, not runtime evidence. It did not inspect
old versions, prior results, the research author's explanation or external URLs.

### C. Executor artifacts and D. actual operations

| Actor / case / unblinded version | Actual generated research records | Raw operations |
|---|---|---|
| X001 / C02 / old | [2026-11-08-package-suite-command-preview.md](execution/X001/artifacts/docs/loom/research/2026-11-08-package-suite-command-preview.md) | [events](execution/X001/events.jsonl) / [receipt](execution/X001/receipt.json) / [prompt](execution/X001/prompt.txt) |
| X002 / C06 / new | [2026-11-08-head-ci-release-evidence.md](execution/X002/artifacts/docs/loom/research/2026-11-08-head-ci-release-evidence.md) | [events](execution/X002/events.jsonl) / [receipt](execution/X002/receipt.json) / [prompt](execution/X002/prompt.txt) |
| X003 / C03 / new | [2026-11-08-package-runner-foreign-tests.md](execution/X003/artifacts/docs/loom/research/2026-11-08-package-runner-foreign-tests.md); [2026-11-08-package-runner-git-failures.md](execution/X003/artifacts/docs/loom/research/2026-11-08-package-runner-git-failures.md) | [events](execution/X003/events.jsonl) / [receipt](execution/X003/receipt.json) / [prompt](execution/X003/prompt.txt) |
| X004 / C02 / new | [2026-11-08-package-suite-command-preview.md](execution/X004/artifacts/docs/loom/research/2026-11-08-package-suite-command-preview.md) | [events](execution/X004/events.jsonl) / [receipt](execution/X004/receipt.json) / [prompt](execution/X004/prompt.txt) |
| X005 / C03 / old | [2026-11-08-package-runner-foreign-tests.md](execution/X005/artifacts/docs/loom/research/2026-11-08-package-runner-foreign-tests.md); [2026-11-08-package-runner-git-failures.md](execution/X005/artifacts/docs/loom/research/2026-11-08-package-runner-git-failures.md) | [events](execution/X005/events.jsonl) / [receipt](execution/X005/receipt.json) / [prompt](execution/X005/prompt.txt) |
| X006 / C05 / old | [2026-11-08-research-note-migration-traceability.md](execution/X006/artifacts/docs/loom/research/2026-11-08-research-note-migration-traceability.md) | [events](execution/X006/events.jsonl) / [receipt](execution/X006/receipt.json) / [prompt](execution/X006/prompt.txt) |
| X007 / C05 / new | [2026-11-08-research-note-migration.md](execution/X007/artifacts/docs/loom/research/2026-11-08-research-note-migration.md) | [events](execution/X007/events.jsonl) / [receipt](execution/X007/receipt.json) / [prompt](execution/X007/prompt.txt) |
| X008 / C01 / new | [2026-11-08-package-runner-test-roots.md](execution/X008/artifacts/docs/loom/research/2026-11-08-package-runner-test-roots.md) | [events](execution/X008/events.jsonl) / [receipt](execution/X008/receipt.json) / [prompt](execution/X008/prompt.txt) |
| X009 / C01 / old | [2026-11-08-package-runner-test-roots.md](execution/X009/artifacts/docs/loom/research/2026-11-08-package-runner-test-roots.md) | [events](execution/X009/events.jsonl) / [receipt](execution/X009/receipt.json) / [prompt](execution/X009/prompt.txt) |
| X010 / C06 / old | [2026-11-08-head-ci-release-evidence.md](execution/X010/artifacts/docs/loom/research/2026-11-08-head-ci-release-evidence.md) | [events](execution/X010/events.jsonl) / [receipt](execution/X010/receipt.json) / [prompt](execution/X010/prompt.txt) |
| X011 / C04 / new | [2026-11-08-research-workflow-timing-evidence.md](execution/X011/artifacts/docs/loom/research/2026-11-08-research-workflow-timing-evidence.md) | [events](execution/X011/events.jsonl) / [receipt](execution/X011/receipt.json) / [prompt](execution/X011/prompt.txt) |
| X012 / C04 / old | [2026-11-08-research-workflow-timing-evidence.md](execution/X012/artifacts/docs/loom/research/2026-11-08-research-workflow-timing-evidence.md) | [events](execution/X012/events.jsonl) / [receipt](execution/X012/receipt.json) / [prompt](execution/X012/prompt.txt) |

[Cases](execution/cases.json) · [predeclared domain expectations](execution/rubric.md)
· [source/sample provenance](execution/fixtures/provenance.json) ·
[sealed blinded packet](execution/packet-seal.json) ·
[process/token totals](execution/completion.json) ·
[cleanup](execution/cleanup.json) · [post-audit arm mapping](execution/arm-map-private.json).

Six tasks used identical prompts/resources/permissions across versions. The
sources are genuine current repository files; prior timing receipts contain
actual observations, not fabricated benchmark results. The migration fixture
preserves a verbatim metadata/evidence excerpt at its original relative location,
with the full-original and excerpt identities distinguished. It is not a full
project or production service. Actors were told the plugin was uninstalled and
explicitly invoked, with no active change or config.

All twelve processes exited 0 without timeout or harness error; source/skill/sample
inputs stayed unchanged. Total actor time was 1,203.785 seconds, input tokens
1,949,021 (cached 1,608,192) and output tokens 44,706. Activation usage is reported
separately. Receipts do not supply currency pricing; no monetary cost is invented.
Time/token values are descriptive single-run observations, not causal speed or
cost comparisons. All auth symlinks were removed; temporary evidence was retained.
Hidden reasoning text was filtered, while aggregate usage counters were kept.

### E. Independent auditor judgments

[Auditor 1 raw report](audits/audit-1.md) · [structured votes](audits/audit-1.json).
[Auditor 2 raw report](audits/audit-2.md) · [structured votes](audits/audit-2.json).

Both auditors began fresh, reviewed completed actors as receipts appeared,
and ultimately covered all twelve. They inspected source, actual operations and
artifacts against each raw contract plus [common criteria](audit-rubric.json).
They did not receive variant mapping, author predictions, previous grader
results, cold-reader findings or one another's judgments. Equivalent adequate
methods were accepted; matching framework names alone was not a success measure.
The raw votes and ordering disagreement remain available for human calibration.

## Interpretation and limits

The new rules are executable as conditional guidance in these sampled tasks,
including skipping the extra reference for a simple fact and combining methods
for a mixed question. The comparator already achieved the same main decisions.
This run therefore supports retaining the new material as optional reference
if its explanatory value is desired, but does not show an incremental quality
improvement or justify making every framework a mandatory workflow.

There is one execution per case/version, one requested model/effort, a small
set of mostly related source files, and two judges sharing a model family.
The tasks explicitly bound experiments and sometimes prohibited diagrams;
observed restraint is not general unprompted restraint. Further generalization
would require different repositories and less constrained tasks. Full ATAM,
real performance bottleneck diagnosis, randomized live experiments/SRM,
production migration, service SLO/canary evaluation and specialist security
coverage were not executed. The 13-row proposal is not fully validated by six
samples. A correct threat-model-style discussion is not a verified vulnerability
or security certification.

This round did not test installed hosts, publish anything, or modify frozen
prior notes/skills. All 2,557 prior artifacts and both frozen inputs are checked
by [the recomputing verifier](verify.py). No fixes were applied after results.
