# Search-language evidence: preserved trial and supplemental observations

The two supplemental public questions were answered from applicable Chinese and Korean first-party accounts. Both executors included the source language in their first search round. Neither case demonstrates adding a new language only after an observed English/Japanese-only search gap. These are bounded workflow observations, not a general dogfood pass, activation-rate measurement or evidence of improved research quality.

## Portable evidence

- [Complete unchanged first trial](first-trial.tar.gz), with [SHA-256 and member inventory](first-trial.inventory.json).
- [Complete supplemental experiment](supplemental.tar.gz), with [SHA-256 and member inventory](supplemental.inventory.json).
- [Structural integrity result](integrity-result.json).
- Readable supplemental records: [S01 Leaf](notes/S01-leaf.md), [S02 KakaoPay](notes/S02-kakaopay.md).
- Independent advisory audits: [A01](audits/A01.md), [A02](audits/A02.md).

Extract either archive into an empty scratch directory using `tar -xzf <archive> -C <directory>`. Members live under `first-trial/` or `supplemental/`. They have sorted regular-file members, normalized owner/mode/time and zero gzip timestamp. Historical Python helpers inside archives are data from the experiment; they are not runtime dependencies or maintained test harnesses. No helper was added under the repository's tests or runtime trees.

The first-trial report is member `first-trial/workspace/docs/skill-dogfood/2026-11-09-engineering-research-language-policy/report.md`. It retains six cases, both blind audits, the cold reader, exact frozen candidate, original disagreement and limitations. The source-return/no-match supplement remains separate from the unchanged audited packet. Preserve the C06 factual judgment disagreement: A01 rated it partial for an Online Read-Only JDBC qualification, while A02 rated the core conclusion met without specifically refuting that finding. The post-freeze no-match observation does not resolve that factual question or prove what the actor ignored.

## Prospective design and firewalls

Supplemental members `protocol.md`, `rubric.md`, `oracle.md`, both `cases/*` inputs and the exact candidate hashes were frozen in `freeze.json` before executors launched. The candidate is the unchanged existing first-trial candidate; no candidate repair followed these observations. Its `references/source-policy.md` SHA-256 is `5ac32bc13f3c58210624a9220234d074a1570bbb0cd380b7c01293241c1bfc6e`.

The supplied English/Japanese sources were real, accessible conceptual documentation, insufficient for attributing a particular author's historical design choice. This establishes a gap in the supplied evidence, not an exhaustive failure of English/Japanese discovery. Preflight English/Japanese searches could return original-language first-party pages; that possibility was recorded before actors. Actors received product/date/question and conceptual source URLs, without original-language target URLs, search-language instructions, oracle, previous results or auditor feedback. No searches were faked and no adequate alternative source was suppressed.

Fresh native executor actors ran sequentially, then two independent blind auditors assessed the frozen packet. All four used pinned `gpt-6.1-sol`, `medium`, with `fork_turns=none`; exact child metadata was checked. The station worker inherited its profile; installed dispatch resolution returned null overrides. Test model pinning follows the testing toolkit's explicit repeated-judge instruction. Auditors received the fixed domain rubric, task/evidence inputs, outputs and visible trajectories with skill-read results withheld. They did not receive skill text, oracle or peer judgments. Audits remain advisory.

Only exact new child trajectories were exported. The exporter allowlist retains visible user tasks, tool actions, public URL/ref identities, returned-output hashes, error/no-match status metadata and final answers. Reasoning channels, parent history, unrelated sessions and full external page/search bodies are excluded. A final post-packet export additionally records tool-generated error status lines; it does not alter the frozen packet judged by auditors. Co-returned task/initial-evidence text in a skill-read result was withheld as a whole for auditor blindness, so a requested read is visible but that returned body cannot independently be inspected in the audit copy.

## Observed actions and outcomes

| Case | Initial evidence gap | Actual source-selection actions | Outcome and unobserved path |
|---|---|---|---|
| S01: Meituan Leaf, 2017 | English/Japanese MySQL identity manuals do not attribute Leaf buffering/refill/outage decisions | English, Japanese and Chinese queries in one batch; opened the Chinese Meituan original; no observed web error or no-match | Attributed refill latency rationale, 10% trigger, 600 × peak-QPS sizing and conditional 10–20-minute claim. Wrote and fully read back the note. Later language expansion was not observed. |
| S02: KakaoPay quiz rewards, 2024-11-05 | English Redis and Japanese AWS coordination concepts do not establish this author's lock choice | English, Japanese and Korean queries in one batch, then focused Korean title query; an AI Briefing page returned an access error; original Korean account and English Redis documentation opened successfully | Attributed maintainability and early Controller rejection; separated the three-second/direct-delete snippet from duplicate-safety guarantees. Wrote and fully read back the note. Korean refinement occurred; adding Korean after an English/Japanese-only stage did not. |

S02's saved note attributes initial discovery to particular query languages more precisely than the retained merged search-return identities support. Treat the visible sequence above as the supported provenance. The original note is preserved unchanged; it is not silently corrected after judging.

Neither case inspected current implementation repositories or executed allocators, reward requests, concurrency workloads or failure injections. A currently accessible page carrying a historical publication date is not a byte-identical historical snapshot. Inference about failure boundaries is distinct from observed production behavior.

## Independent findings

Both independent assessments reopen the primary sources and check actual actions, saved content and limitations. Their detailed judgments and any disagreements are retained verbatim in the linked audits and archived audit trajectories. A01 identifies one low-severity provenance precision issue in S02; A02 independently flags the same uncertainty and additionally notes S01's malformed site-restriction query syntax (`site.tech.meituan.com` instead of `site:tech.meituan.com`). S01 still reached and read the primary original. Neither auditor identifies a material factual error. A01 rates S02's source trajectory partial; A02's separate coarse judgments and low-severity findings remain uncollapsed. Audits do not turn the unobserved delayed-expansion path into a success.

## Verification and limits

The one-use standard-library verifier is member `supplemental/verify_evidence_integrity.py`. It checks both archive SHA-256 values and complete member inventories, prospective input/candidate freezes, both audit-packet freezes, exact native model/effort labels, trajectory record allowlists, all 48 local links from the original first-trial report within the extracted member namespace, and local links from this report. The retained result identifies the command and structural checks; it is not a semantic acceptance verdict. Existing first-trial root bytes and both original freezes were checked before packaging and again inside the archive.

This supplement covers two informed workflow tasks and repeated independent audits. It does not rerun activation or the cold reader, compare an executed baseline, estimate reliability, demonstrate causal quality improvement, establish delayed language expansion or validate another host. The original trial's activation, runtime and source-specific limits remain in force. Adoption of the bounded guidance belongs to the owning change; this evidence worker issues no formal workflow gate verdict.
