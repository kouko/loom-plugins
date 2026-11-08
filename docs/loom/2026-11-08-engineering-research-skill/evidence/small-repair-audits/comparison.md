# Blind paired repair audit comparison

Two fresh OpenAI gpt-6.1-sol/medium auditors applied the unchanged frozen bar to twelve opaque Claude Code explicit raw-skill executions with matched confined file tools. Both full answers were extracted into `opaque-judgments-before-decode.json` before the private arm map was read. These are advisory dogfood draft judgments, not formal closing-review verdicts. No adjudication or additional model attempt occurred.

| Case | Old actor | Old A01 / A02 | New actor | New A01 / A02 |
|---|---|---|---|---|
| F01 | A | partial / partial | B | met / met |
| F02 | D | partial / partial | C | partial / met |
| F03 | E | partial / partial | F | partial / partial |
| F04 | H | partial / partial | G | partial / partial |
| F05 | I | partial / partial | J | partial / partial |
| F06 | L | partial / partial | K | met / met |

## Scoped changes supported by the raw judgments

- F01: both move from partial to met. Old A checks headings only; new B reads saved continuation, provenance and limits. Anchors: A/events.jsonl:40, :42; B/events.jsonl:44, :45.
- F02: new C reads the full substantive record versus old D stopping before findings. C then corrects one evidence-table cell without rereading it. A01 retains partial; A02 gives met while acknowledging the same low residual gap. Anchors: D/events.jsonl:31–32; C/events.jsonl:41–42, :46, :48. Preserve this disagreement.
- F03: both partial for omitted methods/source-policy reads. Exact roots, no-write and missing saved-artifact disclosure are satisfied. Both arms lacked mutators by fixed control; no repair effect is supported. Anchors: E/F events.jsonl:2, :4, :6.
- F04: both remain partial. New G reads only the first 30 lines, before hash/provenance findings and limitations; old H makes no substantive post-save read. The coverage increase is insufficient under both judgments. Anchors: G/events.jsonl:44, :46; H/events.jsonl:37, :43, :45; G saved record:32 and :65.
- F05: both remain partial. New J fully reads both saved artifacts and has resolving saved-location proposal links; old I has no substantive readback and mislabels the saved scratch candidate “not written anywhere.” Both leave the proposed destination unresolved; J also defers destination link adaptation. Anchors: I/events.jsonl:50–53, I/answer.txt:30; J/events.jsonl:47–50; J/project/scratch/vault-preservation-proposal.md:5, :8, :11, :22. I uses code/plain source paths; neither auditor separately flags its lack of Markdown links as a distinct defect. This supports a narrow link-presence observation, not completed destination adaptation.
- F06: both move from partial to met. New K fully reads the saved approved copy; old L grep returns only names and truncated link fragments. Both actual copies are accurate, authorized and meaningfully linked, so factual/link correctness is not a demonstrated differential improvement. Anchors: K/events.jsonl:41–42; L/events.jsonl:48–49; L/answer.txt:1. K explicitly retains no actor-computed post-write hash and no application-validation claim.

Context for F03: both current arms receive the same low process finding. Historical auditors accepted narrow evidence reuse; that differing judgment does not establish a new source regression. Context for F05: retain the auditors' case-specific request-fit concern alongside the declared no-CLI fallback allowing an unresolved destination. Do not generalize it into a duty to guess a real Vault path or infer write consent; buckets remain unchanged.

No material source-correctness or authorization regression is asserted by either auditor. That is bounded to this packet, not proof of absence elsewhere. Broader cleanup eligibility remains inconclusive; a clean main tree and a blocked historical branch deletion do not establish branch/worktree removal.

## Integrity and scope

Both native audits exited 0 without timeout (286.785 / 356.31 seconds). All 852 master-packet files and both actor packet copies match the pre-output freeze; harness/config/prompt/criteria/runtime hashes match. Answers match final observable messages, receipts match observable usage, and auth symlinks are absent. Reasoning content is excluded. Requested model/provider/effort are gpt-6.1-sol/openai/medium; server model identity is not independently attested.

Aggregate usage: input 2,186,652 (cached 1,931,008), output 18,871, reasoning token counter 5,287. Full answers and complete filtered audit trajectories remain in A01/ and A02/.

One pair per case is directional evidence, not a powered benchmark or generalized success rate. Current file-only controls differ from the historical native-Bash dataset; do not attribute unavailable-tool denial, lack of external attempts, or F03 no-write to source changes. Native activation, installed-host parity, real Vault/import/rendering, full cleanup and release/install behavior remain untested. No provider ranking or overall pass follows. Previous attempts, authorization rejection and later specific approval remain preserved separately.
