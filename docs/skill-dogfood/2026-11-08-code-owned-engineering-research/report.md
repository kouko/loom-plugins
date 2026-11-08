# Dogfood report — code-owned engineering-research

This is a bounded behavioral report, not a release attestation or an overall
pass. Codex activation, explicit execution, and independent auditing are separate
observations. Two independent OpenAI audits of the six Claude outputs and
observable trajectories are complete, under the user's separate explicit
cross-provider authorization. The shared medium findings remain unresolved.

## Metadata

| Field | Value |
|---|---|
| Target | [loom-code engineering-research](../../../loom-code/skills/engineering-research/SKILL.md) |
| Source | Implementation at `927ad01a`; verification metadata at `fe2a7832`; seven runtime Markdown files unchanged throughout these trials |
| Version | Plugin source 3.60.0; skill frontmatter has no separate version field |
| Date | 2026-11-08 |
| Codex model request | First-party OpenAI, `gpt-6.1-sol`, medium; CLI receipts do not server-attest the served model |
| Claude model | First-party Anthropic, explicit `claude-sonnet-5-5`, medium; returned model fields match in all six executor cases |
| Activation fidelity | Native Codex description discovery and actual body reads in isolated homes; not installed-plugin/hook parity |
| Claude execution fidelity | Explicit raw-skill loading under safe mode; no native target Skill registration |
| Prior failures | Network failures, denied transmissions, authentication preflights and the public control are retained separately; none is counted as a successful skill trial |

## Observed results

| Dimension | Observation | Limit |
|---|---|---|
| Codex positive routing | 40/40 actual target-body reads | Twenty predeclared queries, two repetitions each |
| Codex negative routing | 16/16 without a target-body read | Eight predeclared near-misses, two repetitions each |
| Codex trial validity | 56/56 valid, no timeout or retry | Initial catalog excludes the target body in all 56 cases |
| Codex explicit execution | Six completed actors, exit 0, no timeout | Exit status alone is not a semantic judgment |
| Codex independent audits | Both judge F01–F04 met; both F05 partial; F06 partial/met disagreement | Fuller cleanup eligibility remains inconclusive |
| Cold reader | One completed zero-context read | Advisory integration/terminology questions, not a reproduced workflow failure |
| Claude explicit execution | Six completed actors, exit 0, no timeout; protected sources unchanged | Completion does not imply contract compliance |
| Claude independent audits | Both F03 met; F01 partial/met disagreement; both F02/F04/F05/F06 partial | Three shared medium finding clusters, below |
| Claude native activation | Not verified | Safe mode exposes a session plugin but rejects its public control skill lookup; no target miss is inferred |

The Codex detector was independently checked against every successful command
output, without requiring the target name to appear in the command string:
56 receipts, 40 body-marker reads, no detector disagreements and no negative
body reads. Expected labels were absent from actor input. The five adjacent
descriptions were frozen before this batch; replacing the earlier design
neighbor with Build changes the menu, so this is not a controlled estimate of
the effect of moving the package.

These results do not establish general trigger rates, causal quality improvement,
an advantage over a no-skill baseline, or a ranking of model providers.

## Severity summary

| Severity | Finding clusters | Scope |
|---|---|---|
| Critical | 0 | None reported |
| High | 0 | None reported |
| Medium | 3 | Reproduced Claude execution compliance gaps, DF-003–DF-005 |
| Low | 2 | Reader clarity and fixture/preservation eligibility, DF-001–DF-002 |

These counts group related observations, not failed cases or independent
discoveries. F01's readback disagreement is preserved rather than counted as a
fourth medium finding. Auditor buckets are advisory judgments, not formal
closing-review verdicts. No runtime source was changed to make these trials pass.

## Explicit execution coverage

| Case | Task | Observed Codex audit result |
|---|---|---|
| F01 | Continue an existing question under the same conditions | Both met: original file and creation/revision basis preserved, source checked and saved content read back |
| F02 | Revalidate after explicit invocation conditions change | Both met: original retained, separate linked active-change record, hypothetical execution not called a successful test |
| F03 | Answer with a strict no-project-write boundary | Both met: accurate roots, unsaved draft, no project mutations |
| F04 | Verify a prior completion/receipt against actual artifacts | Both met: source research separated from suite/CI success; historical provenance discrepancies retained |
| F05 | Prepare a post-merge preservation proposal without write consent | Both partial: substantive proposal and no Vault write established; broader cleanup eligibility inconclusive |
| F06 | Save a specifically authorized copy without the Obsidian CLI | Copy, original preservation, readback, hashes and links established; auditors differ on whether cleanup uncertainty makes the whole case partial |

The cleanup fixture proves a local merge, historical clean main working tree,
and that no linked worktree/build artifact had been created. It explicitly
retains the topic branch. A blocked branch-deletion attempt is not a successful
cleanup operation. This limits evidence for the full finishing sequence; it is
not evidence of an unauthorized real-world cleanup or Vault write.

For F05, one auditor accepts the unresolved destination under the documented
no-CLI fallback; the other records a low-severity request-fit concern because a
more concrete destination was requested. Both agree no Vault write occurred.
Do not collapse their differing scopes into an unqualified pass.

### Claude explicit execution: independent judgments

| Case | A01 | A02 | Main observation |
|---|---|---|---|
| F01 | partial | met | Targeted saved-content readback sufficiency is disputed |
| F02 | partial | partial | Correct linked revalidation; inadequate claimed readback/link verification and ancestor probe |
| F03 | met | met | Accurate bounded answer; strict no-write control respected |
| F04 | partial | partial | Correct receipt/CI distinction; saved substantive body not read back |
| F05 | partial | partial | No Vault write; candidate lacks meaningful Markdown links and probes an external path |
| F06 | partial | partial | Actual approved copy and correct links; claimed substantive content readback not observed |

Both auditors support the substantive source findings, source preservation,
no-write behavior, instance-specific Vault write boundary and actual F06 copy.
They also independently reproduce the three medium clusters below. The main
agent checked the cited commands and returned tool results: the gaps are
observable even where independent inspection finds the final artifact correct.
The source already explicitly requires readback, meaningful preservation links
and respecting authorization. These are failures to follow existing rules;
they do not establish that adding more prose would fix the behavior.

A01 additionally flags F05's missing retained lifecycle-research record and
candidate readback; A02 does not separately identify those as material findings.
Keep that coverage difference and the F01 disagreement visible. Broader cleanup
eligibility remains the same limited fixture premise as in the earlier dataset.

## Advisory findings

### DF-001 — Caller context is not fully explained to a first-time reader

- Severity: Low; category: Cold-start / Jargon-leak; pass: blind cold reader.
- Probe: the fixed self-contained/executable/undefined-terms questions.
- Expected: a reader can identify the caller context it needs, or use the
  explicitly supported standalone fallback.
- Actual: the reader can perform standalone research but asks how to identify
  an active change/change-id and several Loom-specific terms.
- Evidence: [verbatim cold read](../../loom/2026-11-08-engineering-research-skill/evidence/code-owned-cold-reader/answer.md), the retained-records row and undefined-terms list.
- Location: `SKILL.md`, Retained research records and Return to the owning task.
- Suggested edit class: a short caller-context definition, preserving the
  unknown-change fallback and avoiding a mandatory interview or new state store.
- Qualification: F01–F04 did not reproduce a resulting execution failure; a
  real active change is supplied in F02. This is a clarity observation.
- Why static checks miss it: valid paths and metadata do not establish that a
  new reader understands the integration vocabulary.

### DF-002 — Full preservation eligibility needs more specific cleanup evidence

- Severity: Low; category: Cold-start / Output-quality qualification; passes:
  cold reader and two independent executor audits.
- Probe: F05/F06 merged-fixture preservation, with and without write consent.
- Expected: claims about completed cleanup are limited to actual caller-required
  cleanup evidence; copy permission and release evidence remain distinct.
- Actual: the control supports narrower fixture cleanliness, while the cold
  reader cannot identify the finishing command or cleanup criteria. Auditors
  retain a broader eligibility limitation and differ on F06's coarse bucket.
- Evidence: [audit comparison](../../loom/2026-11-08-engineering-research-skill/evidence/code-owned-audits/comparison.md), both raw audit answers, and the fixture guard observation linked in the evidence below.
- Location: `references/preservation.md`, Establish eligibility and provenance;
  the F05 closeout's eligibility wording and the fixture lifecycle premise.
- Suggested edit class: clarify the caller's required cleanup scope and qualify
  case claims, or obtain an actual complete-cleanup control. Do not replace
  missing evidence with more web searches or require branch deletion everywhere.
- Qualification: this is chiefly an experimental prerequisite limitation and a
  wording concern. The approved F06 copy and its readback/hash/link checks are
  established; no shared high-severity product defect was reported.
- Why static checks miss it: a valid clean-status receipt does not by itself
  establish the scope of the finishing operation it is used to support.

### DF-003 — Saved-content verification is omitted or overstated

- Severity: Medium; category: Workflow-drift / Output-quality; pass: two blind
  Claude-output trajectory audits, independently checked against actual events.
- Probe: F02 changed conditions, F04 receipt/CI claim, F06 authorized copy.
- Expected: inspect the actual saved findings, limitations and provenance before
  claiming the record complete; verify links from their saved location.
- Actual: F02/F04 return only the first 12 lines; F06 returns link existence and
  hashes but no substantive saved content. F02 and F06 nevertheless claim
  content readback. F02's `links-ok` tests two project-root files rather than
  resolving the saved record's actual links. Auditors find the artifacts
  substantively correct; that does not establish the actor's verification.
- Transcript evidence: F02 `head -12` and `echo links-ok`, events 20–22;
  F04 events 25–30; F06 `grep -n ']('` and hashes, events 24–25, plus final
  readback claims. [Raw A02 anchors and quotations](../../loom/2026-11-08-engineering-research-skill/evidence/claude-code-audits/A02/answer.txt).
- Location: `SKILL.md` step 5 and Return to the owning task;
  `references/preservation.md`, Save only the authorized copy.
- Root cause boundary: noncompliance with an existing explicit rule is
  demonstrated; the underlying model/tool cause is not isolated. F04's Write
  result says no readback is needed, but this tool text does not supersede the
  research contract. F02/F06 show the omission without establishing that same cause.
- Suggested edit/test class: test a short explicit completion check against
  saved substantive content, provenance and actual link targets; do not replace
  it with header, hash or file-existence checks. No fix has been applied.
- Why static checks miss it: metadata and an accurate final file can pass while
  the trajectory lacks the verification claimed in the final answer.
- Repro: execute the frozen F02/F04/F06 prompts and inspect post-write returned
  content, not only the final record. F01 remains disputed targeted-readback evidence.

### DF-004 — Directory discovery exceeds the authorized fixture

- Severity: Medium; category: Workflow-drift / Convention-violation; pass: both
  blind Claude-output audits and direct command inspection.
- Probe: F02 project-only investigation; F05 preservation without Vault consent.
- Expected: the prompt's project-only read boundary also governs discovery.
- Actual: F02 executes `ls ../../ 2>/dev/null >/dev/null`; F05 executes
  `ls fixtureVault ../fixtureVault 2>&1 | head`. The latter reports the external
  path absent. No external file contents are visible, and no real Vault write
  is observed; absence of exposed content does not authorize the probes.
- Transcript evidence: F02 events 20–22, F05 events 16–18 and each prompt's
  first paragraph. [Independent comparison](../../loom/2026-11-08-engineering-research-skill/evidence/claude-code-audits/comparison.md).
- Location: `SKILL.md` step 1 and Return to the owning task;
  `references/preservation.md`, Discover destinations only through available capabilities.
- Root cause boundary: the executor exceeds the explicit prompt boundary;
  current rules do not reliably prevent that behavior in this fixture. No
  generalized host isolation or leakage rate is inferred.
- Suggested edit/test class: bound candidate discovery to supplied paths and
  authorized roots; add an executable boundary check if enforced isolation is
  needed. Instruction wording alone is not a filesystem sandbox.
- Why static checks miss it: final artifact and write inventories can be
  correct while a read-only discovery command escapes its allowed scope.
- Repro: replay the frozen prompts and inspect actual resolved command paths;
  an external absence check still counts as a probe.

### DF-005 — Preservation candidate lacks navigable evidence links

- Severity: Medium; category: Output-quality / Workflow-drift; pass: both blind
  Claude-output audits and direct candidate inspection.
- Probe: F05 concrete, reviewable preservation proposal without write consent.
- Expected: ordinary Markdown links to the research original and source
  references, adapted to the proposed destination; unknown destination remains
  explicitly unresolved rather than guessed.
- Actual: the scratch candidate uses code-formatted paths and states no
  portable link was created. It contains no Markdown links. Vault writes are
  correctly withheld; that satisfied control does not supply missing navigation.
- Transcript evidence: `scratch/vault-candidate-package-test-roots.md:20–21,37`;
  [saved candidate](../../loom/2026-11-08-engineering-research-skill/evidence/claude-code-execution-results/execution/F05/artifacts/scratch/vault-candidate-package-test-roots.md).
- Location: `references/preservation.md`, Prepare a concrete candidate before asking.
- Root cause boundary: the required evidence exists in the project, but the
  actor omits the link adaptation required by the existing contract. A01 also
  raises the missing lifecycle record; that additional concern is retained
  separately from this shared finding.
- Suggested edit/test class: demonstrate a bounded no-CLI candidate with
  functioning original/source links and explicit destination uncertainty.
- Why static checks miss it: prose provenance and a candidate file can look
  complete while lacking the navigation needed for long-term reuse.
- Repro: inspect the frozen F05 candidate's link syntax and resolve targets
  from the actual candidate/destination context, rather than its relocated copy.

The cold reader also names version-feature lookup and general code review as
context-dependent trigger examples, plus Vault/host/loader/frozen-record terms
that assume background. These are retained as reader questions, not invented
trigger misses: the measured corpus contains no observed miss or over-trigger.

## Raw outputs appendix

- Activation: [corpus](../../loom/2026-11-08-engineering-research-skill/evidence/code-owned-activation-results/corpus.json), [all receipts](../../loom/2026-11-08-engineering-research-skill/evidence/code-owned-activation-results/receipts.json), [query/answer/tool-output evidence](../../loom/2026-11-08-engineering-research-skill/evidence/code-owned-activation-results/query-read-evidence.jsonl), [summary](../../loom/2026-11-08-engineering-research-skill/evidence/code-owned-activation-results/summary.json), [integrity](../../loom/2026-11-08-engineering-research-skill/evidence/code-owned-activation-results/verification.json).
- Execution: [frozen cases](../../loom/2026-11-08-engineering-research-skill/evidence/code-owned-execution/cases.json), [rubric](../../loom/2026-11-08-engineering-research-skill/evidence/code-owned-execution/rubric.md), [fixture guard observation](../../loom/2026-11-08-engineering-research-skill/evidence/code-owned-execution/guard-observation.md); individual F01–F06 folders retain answers, actual record artifacts and observable tool commands.
- Independent Codex audits: [A01](../../loom/2026-11-08-engineering-research-skill/evidence/code-owned-audits/A01/answer.txt), [A02](../../loom/2026-11-08-engineering-research-skill/evidence/code-owned-audits/A02/answer.txt), [receipts](../../loom/2026-11-08-engineering-research-skill/evidence/code-owned-audits/receipts.json).
- Cold read: [complete answer](../../loom/2026-11-08-engineering-research-skill/evidence/code-owned-cold-reader/answer.md), [receipt](../../loom/2026-11-08-engineering-research-skill/evidence/code-owned-cold-reader/receipt.json).
- Claude: [preflight and rejected/limited paths](../../loom/2026-11-08-engineering-research-skill/evidence/claude-code-dogfood/report.md), [actual six-case execution](../../loom/2026-11-08-engineering-research-skill/evidence/claude-code-execution-results/report.md), [operation verification](../../loom/2026-11-08-engineering-research-skill/evidence/claude-code-execution-results/operation-verification.json).
- Claude-output independent OpenAI audits: [comparison](../../loom/2026-11-08-engineering-research-skill/evidence/claude-code-audits/comparison.md), [A01](../../loom/2026-11-08-engineering-research-skill/evidence/claude-code-audits/A01/answer.txt), [A02](../../loom/2026-11-08-engineering-research-skill/evidence/claude-code-audits/A02/answer.txt), [integrity verification](../../loom/2026-11-08-engineering-research-skill/evidence/claude-code-audits/postprocess-verification.json). Both calls exited 0; all 488 frozen packet files match, temporary auth symlinks are absent. Requested auditor identity is OpenAI/`gpt-6.1-sol`/medium; server identity is not independently attested. Aggregate input 2,037,099 (cached 1,805,696), output 14,294; no bill or model ranking is inferred.

Copied case records are byte-preserved evidence. Their relative links describe
the original isolated fixture, not their relocated evidence-copy directory;
temporary absolute links are likewise not promised to remain live indefinitely.
Read them with the recorded fixture/provenance and tool results. No real Vault,
Obsidian import/render, full installed-hook parity, actual GitHub merge/release,
or general cross-provider superiority has been demonstrated by these trials.
The six executor cases do not exhaust all thirteen evaluation families, and no
new Mermaid-rendering or real Obsidian application validation is claimed.

## Disposition

Research and audit evidence is retained with the original unsuccessful and
partial observations. No automatic skill rewrite, repair pass, release
attestation or publication follows from these draft judgments. The next bounded
engineering step is to test whether a concrete completion procedure improves
saved-content verification and preservation links, while separately enforcing
the fixture read boundary. These observations support that experiment; they do
not establish in advance that more instructions or more web searches will help.
