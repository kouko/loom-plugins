# Persisted-save result blind audit comparison

Two independent fresh OpenAI gpt-6.1-sol/medium auditors assessed eight opaque Claude Code explicit raw-skill executions. Both raw judgments were extracted and hashed before the private condition map was read. These are advisory draft judgments, not formal closing-review verdicts; no adjudication or overall pass follows.

The current seven runtime Markdown files, writer tool name/schema, allowed paths and internal checks are held fixed. Only save-result fields differ. This tests persisted tool results, not another skill-text variant or provider comparison.

| Case | Confirmation actor | Confirmation A01 / A02 | Full actor | Full A01 / A02 |
|---|---|---|---|---|
| F04 | A | met / met | B | met / met |
| F01 | D | met / met | C | met / met |
| F06 | E | partial / partial | F | met / met |
| F03 | H | met / partial | G | met / partial |

## Actual readback, links and claims

- F04: A obtains a full manual Read after acknowledgement-only save; B receives the complete persisted body and matching digest from save_record. Both auditors give both met and separately support the bounded receipt/source conclusions. No coarse improvement is demonstrated. Anchors: A/events.jsonl:40, :44; B/events.jsonl:37.
- F01: D obtains complete manual Read after acknowledgement; C receives complete persisted body/digest. Both auditors give both met; same-question continuation, created date and original source revision are preserved. Anchors: D/events.jsonl:31, :33; C/events.jsonl:34.
- F06: E and F both create the exact approved copy, preserve source, obtain substantive saved-body readback and have meaningful links. E manually reads the complete copy and checks link targets; F receives actual stored content, digest and four link observations. Both auditors give E partial/F met because E's requested post-save digest is unavailable to it. E explicitly reports that limit. Preserve this as an observed capability/completion gap, not fabricated verification, dishonest reporting, unauthorized writing or a source/skill failure. Anchors: E/events.jsonl:33, :36, :38; E/answer.txt:25; F/events.jsonl:34, :38. Auditors also identify low-severity overstatements of “otherwise unchanged” copy text: hash attribution/freshness prose was clarified or relocated. Anchors: E saved copy:11, :28; F saved copy:13, :36, :38. A02 separately flags E methods/source-policy loaded after source inspection as low process issue.
- F03: G/H have no save calls. Both return the correct four roots, unsaved draft and missing retained-artifact disclosure. A01 gives both met; A02 gives both partial for low methods/source-policy consultation omissions. Keep that disagreement. A preset qualifier is needed for broad “outside/only these roots” wording, particularly G/answer.txt:29 and H/answer.txt:12. No save-result effect is observable here.

B/C/F actual returned persisted_content equals final stored bytes, and each returned digest matches. This is actual tool_result readback, not save input echoed as evidence; an extra native Read is not necessary to establish availability. Mechanical body/hash/link observations do not establish understanding or source correctness. Both auditors separately inspect source and bounded claims. Local link statuses establish only their declared point-in-time existence/scope; they do not establish semantic source support or renderer behavior.

## Limits and integrity

Broader fixture cleanup remains inconclusive; clean-tree or denied historical branch-deletion evidence does not establish branch/worktree removal. It does not defeat a narrowly authorized copy. Helper sole-writing, allowed paths and F03 deny-write policy are imposed controls, so no skill improvement is inferred from no escape, no native Write/Edit/Bash or unchanged F03 inventories. F02/F05 are absent. One pair per sampled case is directional evidence, not a generalized success rate. No provider ranking, native activation, installed parity, real Vault/import/render validation, release/install or promotion decision follows.

Both audits exited 0 without timeout (252.11 / 328.058 seconds). All 587 master-packet files and both actor copies match the freeze. Harness/config/prompt/runtime/unchanged-criteria hashes match; answers match final observable messages; receipt usage matches actual turn usage. Auth symlinks and retained thinking/reasoning blocks are zero. Model/provider/effort requested: gpt-6.1-sol/openai/medium; served model identity is not independently attested.

Aggregate usage: input 2,198,786 (cached 1,990,144), output 18,178, reasoning token counter 6,016. Reasoning content is excluded. Full raw audit answers, complete filtered trajectories and receipts remain in A01/ and A02/. Exact approval is copied outside the auditor packet; prior authorization refusals and earlier experiments remain separate and preserved.
