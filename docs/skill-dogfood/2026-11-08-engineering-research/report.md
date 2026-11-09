# Dogfood report — engineering-research revision 4

## Result and metadata

The uninstalled prototype was selected in all 40 positive trials and none of
10 adjacent negative trials in this fixed corpus. Three genuine-source tasks
completed; two independent auditors found no substantiated material functional
defect in their outputs or operations. The optional graph rendered in local
Obsidian. One cold reader identified two low-severity routing-boundary ambiguities.
These bounded observations are not a global dogfood-pass, a baseline comparison,
or evidence that Mermaid improves agent comprehension.

| Field | Value |
|---|---|
| Tested skill | `input/engineering-research/`, frozen copy of prototype revision 4 |
| Original | `docs/loom/2026-11-07-engineering-research-trial/revision-4-structured-relations/candidate/engineering-research/` |
| Date | 2026-11-08 |
| Native model request | gpt-6.1-sol / first-party OpenAI / medium, fixed across A/B; both independent auditors use the same requested model/effort |
| Immutable server version | Not independently returned or verified; fixed request name is not proof of immutable weights |
| Cold reader | Fresh inherited host model; no independently recorded immutable model version |
| Activation fidelity | Native Codex raw-skill discovery and actual body-read evidence, not Claude Skill() telemetry |
| Environment | Locally recorded HEAD equals origin/main at `d5a7f0da247214bdb9c61fe90c550256432e5f76`; remote freshness not fetched |
| Installation | Raw prototype only; no production plugin, prototype source, prior records, commits or releases changed |

See [protocol](protocol.md), [environment](environment.json),
[explicit transfer authorization](authorization-resume.json), and
[recomputed evidence integrity](final-verification.json).

## Observed behavior

| Probe | Completed evidence | What remains unproven |
|---|---|---|
| A — activation | 20 positive + 5 negative prompts, twice each: 40/40 target reads and 10/10 correct non-reads | Production frequency, installed hooks, other hosts/models, more difficult ordinary-lookup boundaries |
| B01 — relationships | One source-grounded note and Mermaid flowchart; source exclusions and fail-fast order checked by two fresh auditors | Runtime Git/pytest behavior; universal foreign-tree isolation |
| B02 — simple question | One concise source note, no graph or unused structural section | Unprompted graph restraint across general tasks; this prompt explicitly said no graph needed |
| B03 — missing CI evidence/no-write | Unsaved draft, no new project files, no claim that CI passed | Actual historical CI outcome |
| C — first reading | Reader could carry out the main procedure, with two routing-boundary uncertainties | Actual routing failure on those exact uncertain requests |
| Parent render check | Saved B01 graph renders locally; valid and invalid controls distinguish successful render from an error SVG | Visual layout quality, GitHub compatibility, factual/causal validity, agent understanding gains |

The explicit-stage positive subset was 26/26; the preidentified boundary-sensitive
positive subset was 14/14. Do not relabel cases from their observed answers.
The one approved preflight used full adjacent bundles; the remaining 49 used
only genuine adjacent frontmatter stubs and explicitly disabled web/apps/multi-agent.
The continuation alone was 39/39 positives and 10/10 negatives. Full-50 and
continuation strata are retained separately rather than presented as identical
host contexts. Catalogs contained the target, five adjacent skills and four native
system skills; no target body was initially exposed. The corpus designer saw
30 body lines accidentally; actors remained blind until choosing actual reads.

## Severity summary

| Severity | Count | Meaning |
|---|---|---|
| Critical | 0 | No confirmed finding in completed scope |
| High | 0 | No confirmed finding in completed scope |
| Medium | 0 | No confirmed finding in completed scope |
| Low | 2 | Cold-reader textual ambiguities, not observed runtime failures |

Independent auditors' supported observations are not counted as defects.

## Findings

### C1 — Routine lookup and consequential question have an overlapping boundary

- **Severity / category / pass:** Low / Cold-start / blind; advisory textual ambiguity.
- **Probe prompt:** “Is it self-contained (could you act without asking the author)? Which requests trigger it—give 2 you're unsure about?”
- **Expected:** A first reader can distinguish ordinary low-impact lookups from a consequential evidence gap.
- **Actual:** The reader can execute the procedure but is unsure whether a one-page version lookup that decides a design invokes the retention requirement.
- **Transcript evidence:** “the same small lookup can satisfy both descriptions. The text does not say whether ‘routine’ describes low effort, low decision impact, or absence of uncertainty requiring investigation.”
- **Evidence:** [raw C1 and fixed-question answers](cold-reader/response.md).
- **Root cause:** Step 3 excludes routine lookups while the description includes version questions that could change an engineering decision; the classification dimensions differ.
- **Why static review missed it:** Required sections and links can be present without settling a reader's boundary interpretation.
- **Location:** `input/engineering-research/SKILL.md`, description and step 3.
- **Suggested fix direction:** Clarify with one low-impact versus decision-critical example; do not add source quotas.
- **Repro:** Fresh cold reader, raw package only, fixed Probe C questions.

### C2 — Named workflow stages may be scope limits or examples

- **Severity / category / pass:** Low / Cold-start / blind; advisory scope ambiguity.
- **Probe prompt:** Same fixed Probe C questions; raw transcript preserves the complete wording.
- **Expected:** A reader can tell whether compatibility research outside build/planning is included.
- **Actual:** Production-upgrade diagnosis is uncertain to the reader; explicitly invoked execution remains workable.
- **Transcript evidence:** “The text does not explicitly state whether the named stages bound use or exemplify common use.”
- **Evidence:** [raw C2 and uncertain incident request](cold-reader/response.md).
- **Root cause:** Stage-specific first description sentence and a general capability/version/feasibility second sentence do not explicitly establish their relationship.
- **Why static review missed it:** Static structure does not establish a shared scope interpretation.
- **Location:** `input/engineering-research/SKILL.md`, description; diagnosis row in `references/research-methods.md`.
- **Suggested fix direction:** Clarify intended scope in description if outside-stage use is intended; otherwise retain this as a known boundary. Not a proven trigger miss.
- **Repro:** Fresh cold reader, raw package only, fixed Probe C questions.

## Raw outputs appendix

### A. Activation runs

[Corpus and predeclared labels](output/activation/corpus.json) ·
[final statistics and context strata](output/activation/final-summary.json) ·
[complete per-case records](output/activation/per-case.json) ·
[observations and limitations](output/activation/findings.md) ·
[raw output hashes](output/activation/raw-output-hashes.json).
Each run directory also contains the initial catalog and filtered `events.jsonl`.
Target loading is evidenced by the actual body in command output, not a claim
that the model intended to use it. No hidden reasoning is retained.

| Case | Query | Should select target | Run 1 | Run 2 |
|---|---|---|---|---|
| P01 | Before we commit our Loom intent, determine whether the current package test runner really discovers shell tests. That capability decides whether our proposed guard can ship. Read the provided runner and identify the evidence gap. | yes | [read target](output/activation/runs/P01-r1/receipt.json) / [answer](output/activation/runs/P01-r1/answer.txt) | [read target](output/activation/runs/P01-r2/receipt.json) / [answer](output/activation/runs/P01-r2/answer.txt) |
| P02 | The active intent assumes new test roots are discovered automatically, while a reviewer says they must be listed. Resolve this contradiction before we choose an approach. | yes | [read target](output/activation/runs/P02-r1/receipt.json) / [answer](output/activation/runs/P02-r1/answer.txt) | [read target](output/activation/runs/P02-r2/receipt.json) / [answer](output/activation/runs/P02-r2/answer.txt) |
| P03 | We are writing a spec, and whether pytest and shell tests share inventory determines the design. Check the actual runner rather than accepting the assumption. | yes | [read target](output/activation/runs/P03-r1/receipt.json) / [answer](output/activation/runs/P03-r1/answer.txt) | [read target](output/activation/runs/P03-r2/receipt.json) / [answer](output/activation/runs/P03-r2/answer.txt) |
| P04 | During planning, we need evidence on whether tests/local runs in CI. An incorrect assumption changes our validation plan. Investigate the runner slice. | yes | [read target](output/activation/runs/P04-r1/receipt.json) / [answer](output/activation/runs/P04-r1/answer.txt) | [read target](output/activation/runs/P04-r2/receipt.json) / [answer](output/activation/runs/P04-r2/answer.txt) |
| P05 | Build has failed repeatedly because a shell test seems absent from package execution. Stop retrying and establish what the runner actually discovers. | yes | [read target](output/activation/runs/P05-r1/receipt.json) / [answer](output/activation/runs/P05-r1/answer.txt) | [read target](output/activation/runs/P05-r2/receipt.json) / [answer](output/activation/runs/P05-r2/answer.txt) |
| P06 | 我們正在確認 intent；「新增 plugin 不用改測試入口」只是猜測，會影響方案可行性。請先用現有 runner 查證。 | yes | [read target](output/activation/runs/P06-r1/receipt.json) / [answer](output/activation/runs/P06-r1/answer.txt) | [read target](output/activation/runs/P06-r2/receipt.json) / [answer](output/activation/runs/P06-r2/answer.txt) |
| P07 | spec 的兩份說法互相衝突：一份說自動探索測試，一份說固定 roots。先查清楚它們如何同時成立。 | yes | [read target](output/activation/runs/P07-r1/receipt.json) / [answer](output/activation/runs/P07-r1/answer.txt) | [read target](output/activation/runs/P07-r2/receipt.json) / [answer](output/activation/runs/P07-r2/answer.txt) |
| P08 | 規劃尚未定案：若本機 CLI 測試會在一般 suite 跑，CI 方案就要改。請以實際程式判斷，不要直接排工作。 | yes | [read target](output/activation/runs/P08-r1/receipt.json) / [answer](output/activation/runs/P08-r1/answer.txt) | [read target](output/activation/runs/P08-r2/receipt.json) / [answer](output/activation/runs/P08-r2/answer.txt) |
| P09 | build 已連續兩次找不到新增測試；先找出真正原因與證據，再決定要不要調整 discovery 設計。 | yes | [read target](output/activation/runs/P09-r1/receipt.json) / [answer](output/activation/runs/P09-r1/answer.txt) | [read target](output/activation/runs/P09-r2/receipt.json) / [answer](output/activation/runs/P09-r2/answer.txt) |
| P10 | 採用這個測試入口之前，請確認它有沒有支援 shell 測試。這會決定我們能不能沿用既有驗證方式。 | yes | [read target](output/activation/runs/P10-r1/receipt.json) / [answer](output/activation/runs/P10-r1/answer.txt) | [read target](output/activation/runs/P10-r2/receipt.json) / [answer](output/activation/runs/P10-r2/answer.txt) |
| P11 | 実装方針を決める前に、テスト実行器が新しい plugin の tests を自動発見するという前提を確認してください。前提が違えば設計が変わります。 | yes | [read target](output/activation/runs/P11-r1/receipt.json) / [answer](output/activation/runs/P11-r1/answer.txt) | [read target](output/activation/runs/P11-r2/receipt.json) / [answer](output/activation/runs/P11-r2/answer.txt) |
| P12 | Loom の intent を確認中です。ローカル CLI 専用テストが通常 suite に混ざるかで採用判断が変わります。コードで確かめてください。 | yes | [read target](output/activation/runs/P12-r1/receipt.json) / [answer](output/activation/runs/P12-r1/answer.txt) | [read target](output/activation/runs/P12-r2/receipt.json) / [answer](output/activation/runs/P12-r2/answer.txt) |
| P13 | spec 作成中です。pytest と shell が別々の一覧を使うという説明と、共通 inventory という説明の矛盾を解消してください。 | yes | [read target](output/activation/runs/P13-r1/receipt.json) / [answer](output/activation/runs/P13-r1/answer.txt) | [read target](output/activation/runs/P13-r2/receipt.json) / [answer](output/activation/runs/P13-r2/answer.txt) |
| P14 | ビルドで同じ test discovery の失敗を繰り返しました。再試行より先に、何が探索対象かを確認してください。 | yes | [read target](output/activation/runs/P14-r1/receipt.json) / [answer](output/activation/runs/P14-r1/answer.txt) | [read target](output/activation/runs/P14-r2/receipt.json) / [answer](output/activation/runs/P14-r2/answer.txt) |
| P15 | We need an engineering decision, not implementation yet: can this runner support a fifth plugin without changing production code? Verify the relevant constraint first. | yes | [read target](output/activation/runs/P15-r1/receipt.json) / [answer](output/activation/runs/P15-r1/answer.txt) | [read target](output/activation/runs/P15-r2/receipt.json) / [answer](output/activation/runs/P15-r2/answer.txt) |
| P16 | A proposed acceptance strategy depends on shell tests being discovered recursively. Establish whether the current implementation supports that before recommending the strategy. | yes | [read target](output/activation/runs/P16-r1/receipt.json) / [answer](output/activation/runs/P16-r1/answer.txt) | [read target](output/activation/runs/P16-r2/receipt.json) / [answer](output/activation/runs/P16-r2/answer.txt) |
| P17 | The plan treats tests/local as ordinary package tests. I suspect that assumption is wrong and would invalidate CI. Resolve it from source before planning further. | yes | [read target](output/activation/runs/P17-r1/receipt.json) / [answer](output/activation/runs/P17-r1/answer.txt) | [read target](output/activation/runs/P17-r2/receipt.json) / [answer](output/activation/runs/P17-r2/answer.txt) |
| P18 | Before approving the spec, check whether the runner requires node or only Python. That environment requirement could make the design infeasible. | yes | [read target](output/activation/runs/P18-r1/receipt.json) / [answer](output/activation/runs/P18-r1/answer.txt) | [read target](output/activation/runs/P18-r2/receipt.json) / [answer](output/activation/runs/P18-r2/answer.txt) |
| P19 | 目前沒有要修 code；先調查 runner 對 test roots 的限制，因為它會改變我們要不要新增 plugin 的決定。 | yes | [read target](output/activation/runs/P19-r1/receipt.json) / [answer](output/activation/runs/P19-r1/answer.txt) | [read target](output/activation/runs/P19-r2/receipt.json) / [answer](output/activation/runs/P19-r2/answer.txt) |
| P20 | Compatibility is the open decision: will a test named example_test.py and one named test-example.sh both be collected by the supplied runner? Verify rather than assume. | yes | [read target](output/activation/runs/P20-r1/receipt.json) / [answer](output/activation/runs/P20-r1/answer.txt) | [read target](output/activation/runs/P20-r2/receipt.json) / [answer](output/activation/runs/P20-r2/answer.txt) |
| N01 | Critique this proposal on value and complexity only: add an optional summary flag to our runner. Assume technical feasibility is established; do not investigate capabilities. | no | [did not read target](output/activation/runs/N01-r1/receipt.json) / [answer](output/activation/runs/N01-r1/answer.txt) | [did not read target](output/activation/runs/N01-r2/receipt.json) / [answer](output/activation/runs/N01-r2/answer.txt) |
| N02 | Please obtain an independent second opinion from another coding agent on this test-plan decision. Do not execute it yet; explain what review input is missing. | no | [did not read target](output/activation/runs/N02-r1/receipt.json) / [answer](output/activation/runs/N02-r1/answer.txt) | [did not read target](output/activation/runs/N02-r2/receipt.json) / [answer](output/activation/runs/N02-r2/answer.txt) |
| N03 | Do a retrospective of this session: we agreed scope, made one small test update, and forgot to record the command. No unresolved technical question; what process should improve? | no | [did not read target](output/activation/runs/N03-r1/receipt.json) / [answer](output/activation/runs/N03-r1/answer.txt) | [did not read target](output/activation/runs/N03-r2/receipt.json) / [answer](output/activation/runs/N03-r2/answer.txt) |
| N04 | The intent is confirmed and feasibility is established. Break adding one shell test into implementation tasks, without investigating technical assumptions. | no | [did not read target](output/activation/runs/N04-r1/receipt.json) / [answer](output/activation/runs/N04-r1/answer.txt) | [did not read target](output/activation/runs/N04-r2/receipt.json) / [answer](output/activation/runs/N04-r2/answer.txt) |
| N05 | I want to add a new optional --summary flag to the runner. Capture my goal and acceptance criteria first; there are no feasibility questions to investigate yet. | no | [did not read target](output/activation/runs/N05-r1/receipt.json) / [answer](output/activation/runs/N05-r1/answer.txt) | [did not read target](output/activation/runs/N05-r2/receipt.json) / [answer](output/activation/runs/N05-r2/answer.txt) |

### B. Cold-reader raw questions and answers

[Complete fixed-question response](cold-reader/response.md) ·
[files-read receipt](cold-reader/receipt.md).
The reader did not execute the research procedure; this is readability evidence.

### C. Executor artifacts

- B01: [research note and saved graph](execution/B01/artifacts/docs/loom/research/2026-11-08-package-runner-exclusions.md), [final answer](execution/B01/answer.txt).
- B02: [short research note](execution/B02/artifacts/docs/loom/research/2026-11-08-package-test-roots.md), [final answer](execution/B02/answer.txt).
- B03: [unsaved draft](execution/B03/answer.txt); no saved project note exists.

The artifact copies retain input sources and skill resources so relative links
can be resolved. [Genuine source provenance](execution/provenance.json),
[frozen cases](execution/cases.json), [frozen expectations](execution/rubric.md),
[independent-review rubric](audit-rubric.json), and
[source/cleanup checks](execution/final-audit.json) remain available.

### D. Actual executor operations

- B01: [tool events](execution/B01/events.jsonl), [receipt](execution/B01/receipt.json), [prompt](execution/B01/prompt.txt).
- B02: [tool events](execution/B02/events.jsonl), [receipt](execution/B02/receipt.json), [prompt](execution/B02/prompt.txt).
- B03: [tool events](execution/B03/events.jsonl), [receipt](execution/B03/receipt.json), [prompt](execution/B03/prompt.txt).

All three exited 0 without timeout, with unchanged source/skill inputs and auth
symlink removal. These process facts alone are not artifact-quality evidence.
Nonzero exploratory reads in the trajectory are preserved, not erased as if the
execution were error-free. No source tests or external research were run by these
actors, as required by their task constraints.

### E. Independent auditor judgments

[Auditor 1 raw report](audits/audit-1.md) · [structured judgments](audits/audit-1.json).
[Auditor 2 raw report](audits/audit-2.md) · [structured judgments](audits/audit-2.json).

Both reviewed actual operations and source as well as the produced artifacts,
against frozen contract/domain criteria. Neither had author predictions,
cold-reader findings, prior trial scores or the other's judgment. Neither found
a substantiated material defect; neither issued a global PASS. Their judgments
are advisory, with the raw evidence retained for human calibration.

## Parent-side render check

The executor honestly reported no parser/render execution. The parent later
rendered the exact saved B01 block through local Obsidian MarkdownRenderer
(apiVersion 1.14.5; bundled Mermaid version not introspected), using temporary
DOM elements and no vault-file writes. The real block and valid control produced
SVGs without parser-error text. The invalid control also produced an SVG, but
contained parser-error text and was correctly rejected. SVG existence alone
would have incorrectly accepted that control.

[Original CLI output](render-check/result.txt) ·
[parsed checks](render-check/result.json) · [local checker](check_render.py).
This verifies local syntax/rendering, not visual layout, another renderer,
semantic truth, causality or comprehension. The actor's original saved note was
not rewritten to claim it performed the parent's later validation.

The first stdout adapter failed by treating control-case diagnostics plus the
JSON result as one JSON document. The adapter was corrected to select the eval
result line; the original output was reparsed without a diagram rerun/change.
A prior heredoc command was blocked by a static shell guard; the checker was
written via the file-edit tool and invoked directly without embedded shell
commands or guard-configuration changes.

## Authorization and preserved continuation

The initial B launch was rejected before process creation for missing explicit
payload/destination consent. One separately approved A preflight had already
completed. All further external tests stopped; the user then explicitly replied
“同意” to the named OpenAI destination and limited payload. The same frozen corpus
and B tasks resumed; earlier stop/denial/costs were preserved. Nothing was rerouted
to bypass a rejected transfer. [Authorization](authorization-resume.json),
[original B denial](execution/blocked-receipt.json), and
[authorized execution handoff](execution/resumed-handoff.md) record the sequence.

## Limits and interpretation

This corpus is mostly different questions about one runner, with clear adjacent
negative requests. It does not establish generalization to diverse projects,
subtle routine-lookup negatives, incident requests outside named Loom stages,
external web/repository research, causal-hypothesis diagrams, expert inquiry,
benchmarks, or concurrent note writers. No prior/new comparison isolates the
Mermaid policy's effect. Same-model repeated judges share possible biases.

The evidence supports retaining the optional graph design in this prototype and
addressing routing-boundary wording only if desired in a subsequent revision.
It does not establish improved agent comprehension or increased research versus
the preexisting mechanism. The two low-severity ambiguities remain advisory;
no automatic fixes or installation were performed.

## Integrity-check adapter corrections

The parent's first final-check attempt assumed every receipt key ending in
`_sha256` named an output file. Continuation receipts also have input-fixture and
skill-map hashes; these are now checked against their actual source identities.
The next attempt encountered the not-yet-generated verification receipt linked
by this report; the checker now verifies all other links, writes its result,
then verifies every report link including that receipt. No actor output,
predeclared label, source or finding was changed for these corrections.
