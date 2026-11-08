# Small repair — controlled six-case comparison

The small repair shows bounded improvement in saved-content verification, but it does not make completion reliable across all six cases. Two independent revision-blinded audits agree that F01 and F06 improved from partial to met; F02 improves with a residual disagreement, while F03–F05 remain partial. No release or overall pass is claimed.

## Scope and changes

The user approved the previously proposed small repair and controlled retest on 2026-11-08. This continues the existing engineering-research change; it does not change its owner, description, methods/frameworks, record schema or acceptance outcomes.

Only two runtime files changed at `3b287e7b9`:

- [SKILL.md](../../../loom-code/skills/engineering-research/SKILL.md): return substantive saved question/conditions, findings, evidence/provenance and limitations; short records in full, longer updates proportionately. Check actual saved-location links. Header/hash/existence/write success and a tool's completion message do not establish content inspection. Preserve explicit no-write and adequate verification reuse.
- [Preservation guidance](../../../loom-code/skills/engineering-research/references/preservation.md): draft links work from their current location even when the Vault is unresolved; adapt again before an authorized copy. Destination discovery stays within authorized filesystem scope. Read saved copy substance/provenance and verify links before claiming completion.

The original failed/partial outputs remain unchanged in the [prior report](report.md). The implementation comprises 22 additions and nine deletions across these two files; extra plan/spec/evidence files document the experiment rather than add runtime behavior.

## Prospective comparison design

[Protocol](../../loom/2026-11-08-engineering-research-skill/evidence/small-repair-comparison/protocol.md) was frozen before requests. The prediction was improved substantive readback in F02/F04/F06 and usable preservation links in F05, with no regression in continuity, factual/source scope or consent.

| Held constant | Observation |
|---|---|
| Inputs | Same six case prompts, genuine four-source snapshot, existing research and real prior receipt |
| Versions | Old pre-repair bundle versus new `3b287e7b9`; pair inputs differ only in the two runtime Markdown files |
| Executors | Twelve fresh native Claude Code calls; explicit first-party Anthropic `claude-sonnet-5-5`, medium; returned model labels match |
| Tool interface | Same native restricted Read/Write/Edit/Grep/Glob; F03 lacks mutators; no shell, web, agent or Skill tools |
| Local measurements | Equal pre-run harness git/hash observations; actors cannot claim these as their own executed tests or post-write copy hashing |
| Replication | One pair per case, two concurrent pair members; old/new leading order counterbalanced |
| Criteria | Original cases/rubric/shared declared-contract bar bytes unchanged |
| Independent judgments | Two fresh first-party OpenAI `gpt-6.1-sol`/medium auditors; served model not independently attested |
| Blinding | A–L labels; revision map, repair rationale, protocol and skill bodies withheld from auditors; successful skill-read result bodies replaced only in audit copies by hash/success markers; other event lines byte-identical |

This is a bounded directional comparison, not a powered success-rate estimate. The same tool restrictions and F03 lack of mutators apply to both versions, so neither is evidence of a source improvement. The earlier unrestricted-shell dataset is historical context, not the matched control. Revision inference from output behavior cannot be ruled out; this is not a provider benchmark.

## Independent case results

| Case | Old A01 / A02 | New A01 / A02 | What the trajectories establish |
|---|---|---|---|
| F01: same-question continuation | partial / partial | met / met | New version reads the saved continuation, provenance and limitations; old returns headings only |
| F02: changed-condition revalidation | partial / partial | partial / met | New reads the substantive record, then corrects one evidence cell without reading that final correction back; auditors agree on the low residual but differ on the bucket |
| F03: explicit no-write | partial / partial | partial / partial | Exact roots and unsaved draft are correct; both omit method/source-policy loading before source inspection, rated a low process gap |
| F04: receipt versus CI claim | partial / partial | partial / partial | New reads only lines 1–30, missing provenance at line 32 and limitations at line 65; old makes no substantive post-save read |
| F05: preservation proposal | partial / partial | partial / partial | New fully reads both saved artifacts and supplies working draft evidence links; concrete destination and destination-link proposal remain unresolved |
| F06: authorized copy | partial / partial | met / met | New fully reads the actual approved copy; old Grep returns names and truncated link fragments |

These are six paired task observations, not a generalized pass rate. Two cases receive met from both auditors in the new arm versus none in the matched old arm; a third has auditor disagreement. Both judges find the factual source conclusions sound and report no material correctness or authorization regression within this packet.

[Full independent comparison](../../loom/2026-11-08-engineering-research-skill/evidence/small-repair-audits/comparison.md), [A01 verbatim](../../loom/2026-11-08-engineering-research-skill/evidence/small-repair-audits/A01/answer.txt), [A02 verbatim](../../loom/2026-11-08-engineering-research-skill/evidence/small-repair-audits/A02/answer.txt).

### Interpretation boundaries

- Saved-content verification improves in F01/F02/F05/F06, but the final correction in F02 and incomplete read in F04 demonstrate that the same omission can survive a concrete instruction. The main agent inspected C/G/J actual calls and returned content to verify these anchors. Greater read coverage is not automatically sufficient verification.
- F05 now has usable draft-location Markdown links and full readback. Its remaining destination concern is specific to the requested concrete temporary-fixture proposal. The declared no-CLI fallback still permits an unresolved destination: do not generalize this finding into guessing a real Vault path or treating a folder as consent. Future destination adaptation is not complete merely because draft links work.
- F03's new and old arms have the same low process judgment. Earlier audits accepted the historical narrow evidence-reuse case without extra methodology loading; this interpretive boundary is retained. It is not a demonstrated regression caused by the repair, and forced no-write tools cannot establish instruction effectiveness.
- F06 actual copy/link correctness is established in both arms, so the observed differential improvement is the executor's substantive readback, not the correctness of the copied findings. Both distinguish supplied harness hashes from actor execution and disclose unavailable post-write hashing/application validation.
- No external path attempt or confinement denial was observed in any of the twelve research actors. The separate public boundary control demonstrates specific blocked operations; the absence of research-actor attempts under identical limited tools is not credited to the new instructions.

## Execution and integrity evidence

All twelve executors exited 0 without timeout. Protected source/runtime/snapshot/git inputs remained unchanged. F03 wrote nothing, F05 wrote no Vault note, and F06 added only the exact approved fixture copy. These are inventory observations, not semantic success judgments. The original source and generated records can be inspected in [execution evidence](../../loom/2026-11-08-engineering-research-skill/evidence/small-repair-comparison/receipts.json).

The public boundary control observed inside Read success, denials for relative/absolute/symlink outside Reads and an outside Write, and no outside write artifact. External Glob returned no matches rather than an explicit denial. [Actual control calls/results](../../loom/2026-11-08-engineering-research-skill/evidence/small-repair-comparison/boundary-control/observations.json). This narrowly validates these native file-tool controls; instructions are not a production filesystem sandbox.

| Mechanical check | Result | Scope |
|---|---|---|
| Existing skill package invariants | Five passed | Portability/schema/ownership, not agent compliance |
| Local harness tests | Nine passed | Tool/environment restrictions, overwrite/timeout handling, integrity and audit redaction; no model requests |
| Complete locked package runner | Exit 0, 4,139 pytest passes, six skips across 15 pytest groups; shell and Mermaid checks passed | Modified runtime source plus repository integration; [full log](../../loom/2026-11-08-engineering-research-skill/evidence/small-repair-comparison/package-tests.txt) |
| Existing adversarial program | 71 passed | [Committed mechanism guard recheck](../../loom/2026-11-08-engineering-research-skill/evidence/small-repair-comparison/adversarial-recheck.txt) |
| Trunk synchronization | Up to date with `origin/main` at `d5a7f0da247214bdb9c61fe90c550256432e5f76`, no new commit | Earlier uncommitted-evidence BLOCK retained; later check succeeded after local evidence commit |

A [77-member replay-input archive](../../loom/2026-11-08-engineering-research-skill/evidence/small-repair-comparison/replay-inputs.tar.gz) retains the actual minimal fixture and artificial git history, old/new runtime bundles, original criteria and local test harness. [Member hashes](../../loom/2026-11-08-engineering-research-skill/evidence/small-repair-comparison/replay-inputs-manifest.json) were checked by reading every archived member back. No credentials, actor HOME or real Vault data are included. Archived code remains data; relocation is not a claim of one-command replay or permission to execute it.

## Authorization and preserved limits

A first attempt to send this new twelve-output packet to OpenAI was rejected by automatic approval review before any audit process launched: the earlier specific permission covered six original outputs. The user then explicitly authorized these twelve outputs for two first-party OpenAI audits. The same frozen packet/command was submitted through normal approval; no indirect route or provider substitution was used.

Native target activation and installed-plugin/hook parity were not retested. No real Vault write, Obsidian render/import, full lifecycle cleanup, actual hosting merge/release, install, publication or new framework-family coverage is established. Earlier cleanup prerequisite uncertainty and F01 targeted-readback disagreement remain preserved. No automatic extra repair iteration follows this bounded experiment.

## Audit integrity and disposition

Both independent calls exited 0 without timeout (286.785 and 356.31 seconds). All 852 input files and both auditor copies match the pre-output freeze. Skill-body redaction preserves event positions and all unrelated output; both raw judgments were extracted before decoding the private revision map. Answers match final observable messages; usage matches receipts; temporary auth symlinks and raw reasoning content are absent. [Verification](../../loom/2026-11-08-engineering-research-skill/evidence/small-repair-audits/verification.json). Requested auditor identity is first-party OpenAI/gpt-6.1-sol/medium; served identity remains unverified. Aggregate auditor input is 2,186,652 (cached 1,931,008), output 18,871; no bill or provider ranking is inferred.

Retain the small clarification as a provisionally supported improvement, while preserving all residual partial outcomes. Do not treat it as a completed behavioral fix or publish readiness. The next useful experiment is narrow: inspect why the F04 completion still stops before provenance/limitations, and test an observable saved-output verification mechanism under the same controls. Do not broaden the research methods, add source quotas, guess Vault paths, or automatically start another iteration.
